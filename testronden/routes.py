from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import testronden_bp
from users.roles import role_required
from github_service import (
    haal_mappen, haal_bestanden, laad_bestand,
    haal_alle_testronden, haal_testronde,
    maak_testronde_aan, update_testronde_meta,
    volgend_ronde_id, laad_resultaten, sla_resultaten_op,
    bereken_tellers, bereken_tellers_resultaten,
    haal_tc_label,
)
from datetime import datetime


def huidige_tester() -> str:
    return session.get('username', 'onbekend')


# ── Overzicht alle testronden ─────────────────────────────────────────────────

@testronden_bp.route('/')
@role_required('teacher')
def overzicht():
    rondes = haal_alle_testronden()
    return render_template('testronden/overzicht.html', rondes=rondes)


# ── Nieuwe testronde aanmaken ─────────────────────────────────────────────────

@testronden_bp.route('/nieuw', methods=['GET', 'POST'])
@role_required('teacher')
def nieuw():
    if request.method == 'POST':
        ronde_id  = volgend_ronde_id()
        naam      = request.form.get('naam', '').strip()
        versie    = request.form.get('versie', '').strip()
        type_     = request.form.get('type', 'regressie')
        tester    = huidige_tester()

        # Alle beschikbare modules ophalen
        mappen = haal_mappen()
        modules = {}
        for m in mappen:
            modules[m] = {
                'tester':      None,
                'status':      'open',
                'gestart_op':  None,
                'afgesloten_op': None,
            }

        meta = {
            'id':          ronde_id,
            'naam':        naam,
            'versie':      versie,
            'type':        type_,
            'datum_start': datetime.now().strftime('%Y-%m-%d'),
            'datum_einde': None,
            'aangemaakt_door': tester,
            'status':      'actief',
            'modules':     modules,
        }

        succes = maak_testronde_aan(ronde_id, meta, tester)
        if succes:
            flash(f'Testronde {ronde_id} aangemaakt ✅', 'success')
            return redirect(url_for('testronden.detail', ronde_id=ronde_id))
        else:
            flash('Aanmaken mislukt. Controleer de GitHub-verbinding.', 'danger')

    return render_template('testronden/nieuw.html')


# ── Detail: overzicht van een testronde ──────────────────────────────────────

@testronden_bp.route('/<ronde_id>')
@role_required('teacher')
def detail(ronde_id):
    try:
        meta, sha = haal_testronde(ronde_id)
    except Exception:
        flash(f'Testronde {ronde_id} niet gevonden.', 'danger')
        return redirect(url_for('testronden.overzicht'))

    tester = huidige_tester()

    # Tellers per module ophalen
    module_info = []
    for map_naam, mod_data in meta.get('modules', {}).items():
        bestanden = haal_bestanden(map_naam)
        totaal = {'goed': 0, 'fout': 0, 'goed_met_opmerking': 0, 'niet_getest': 0}
        for b in bestanden:
            try:
                script, _  = laad_bestand(map_naam, b)
                resultaten, _ = laad_resultaten(ronde_id, map_naam, b)
                t = bereken_tellers_resultaten(script, resultaten)
                for k in totaal:
                    totaal[k] += t[k]
            except Exception:
                pass
        module_info.append({
            'map':        map_naam,
            'label':      haal_tc_label(map_naam),
            'tester':     mod_data.get('tester'),
            'status':     mod_data.get('status', 'open'),
            'tellers':    totaal,
            'is_eigen':   mod_data.get('tester') == tester,
            'is_vrij':    mod_data.get('tester') is None,
        })

    # Bestanden per map voor het dropdown-menu
    bestanden_per_map = {}
    for mod in module_info:
        bestanden_per_map[mod['map']] = haal_bestanden(mod['map'])

    response = make_response(render_template(
        'testronden/detail.html',
        meta=meta,
        sha=sha,
        ronde_id=ronde_id,
        module_info=module_info,
        bestanden_per_map=bestanden_per_map,
        tester=tester,
    ))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response


# ── Module claimen ────────────────────────────────────────────────────────────

@testronden_bp.route('/<ronde_id>/claim/<map_naam>', methods=['POST'])
@role_required('teacher')
def claim_module(ronde_id, map_naam):
    meta, sha = haal_testronde(ronde_id)
    tester = huidige_tester()
    modules = meta.get('modules', {})

    if map_naam not in modules:
        flash('Module niet gevonden.', 'danger')
        return redirect(url_for('testronden.detail', ronde_id=ronde_id))

    mod = modules[map_naam]
    if mod.get('tester') is not None:
        flash(f'Module al in gebruik door {mod["tester"]}.', 'warning')
        return redirect(url_for('testronden.detail', ronde_id=ronde_id))

    modules[map_naam]['tester']     = tester
    modules[map_naam]['status']     = 'in_behandeling'
    modules[map_naam]['gestart_op'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    meta['modules'] = modules

    succes = update_testronde_meta(ronde_id, meta, sha, tester)
    if succes:
        flash(f'{map_naam.replace("_"," ").title()} geclaimd ✅', 'success')
    else:
        flash('Claimen mislukt.', 'danger')

    return redirect(url_for('testronden.detail', ronde_id=ronde_id))


# ── Module vrijgeven ──────────────────────────────────────────────────────────

@testronden_bp.route('/<ronde_id>/vrijgeven/<map_naam>', methods=['POST'])
@role_required('teacher')
def vrijgeven_module(ronde_id, map_naam):
    meta, sha = haal_testronde(ronde_id)
    tester = huidige_tester()
    modules = meta.get('modules', {})
    mod = modules.get(map_naam, {})

    if mod.get('tester') != tester:
        flash('Je kunt alleen je eigen module vrijgeven.', 'warning')
        return redirect(url_for('testronden.detail', ronde_id=ronde_id))

    modules[map_naam]['tester']     = None
    modules[map_naam]['status']     = 'open'
    modules[map_naam]['gestart_op'] = None
    meta['modules'] = modules

    succes = update_testronde_meta(ronde_id, meta, sha, tester)
    if succes:
        flash(f'{map_naam.replace("_"," ").title()} vrijgegeven.', 'info')
    else:
        flash('Vrijgeven mislukt.', 'danger')

    return redirect(url_for('testronden.detail', ronde_id=ronde_id))


# ── Module afsluiten ──────────────────────────────────────────────────────────

@testronden_bp.route('/<ronde_id>/afsluiten/<map_naam>', methods=['POST'])
@role_required('teacher')
def afsluiten_module(ronde_id, map_naam):
    meta, sha = haal_testronde(ronde_id)
    tester = huidige_tester()
    modules = meta.get('modules', {})
    mod = modules.get(map_naam, {})

    if mod.get('tester') != tester:
        flash('Je kunt alleen je eigen module afsluiten.', 'warning')
        return redirect(url_for('testronden.detail', ronde_id=ronde_id))

    modules[map_naam]['status']        = 'afgesloten'
    modules[map_naam]['afgesloten_op'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    meta['modules'] = modules

    succes = update_testronde_meta(ronde_id, meta, sha, tester)
    if succes:
        flash(f'{map_naam.replace("_"," ").title()} afgesloten ✅', 'success')
    else:
        flash('Afsluiten mislukt.', 'danger')

    return redirect(url_for('testronden.detail', ronde_id=ronde_id))


# ── Testronde afsluiten ───────────────────────────────────────────────────────

@testronden_bp.route('/<ronde_id>/afsluiten', methods=['POST'])
@role_required('teacher')
def afsluiten_ronde(ronde_id):
    meta, sha = haal_testronde(ronde_id)
    tester = huidige_tester()
    meta['status']      = 'afgesloten'
    meta['datum_einde'] = datetime.now().strftime('%Y-%m-%d')

    succes = update_testronde_meta(ronde_id, meta, sha, tester)
    if succes:
        flash(f'Testronde {ronde_id} afgesloten ✅', 'success')
    else:
        flash('Afsluiten mislukt.', 'danger')

    return redirect(url_for('testronden.detail', ronde_id=ronde_id))


# ── Script testen binnen een testronde ────────────────────────────────────────

@testronden_bp.route('/<ronde_id>/<map_naam>/<bestand>')
@role_required('teacher')
def script_detail(ronde_id, map_naam, bestand):
    # Controleer of de tester recht heeft op deze module
    meta, _ = haal_testronde(ronde_id)
    tester  = huidige_tester()
    mod     = meta.get('modules', {}).get(map_naam, {})

    if mod.get('tester') != tester:
        flash('Deze module is niet aan jou toegewezen.', 'warning')
        return redirect(url_for('testronden.detail', ronde_id=ronde_id))

    # Structuur uit testscript, resultaten uit testronde
    scriptdata, _    = laad_bestand(map_naam, bestand)
    resultaten, res_sha = laad_resultaten(ronde_id, map_naam, bestand)

    testsets    = scriptdata.get('testsets', [])
    gekozen_ts  = request.args.get('ts', 'alle')

    if gekozen_ts != 'alle':
        zichtbaar = [ts for ts in testsets if ts['id'] == gekozen_ts]
    else:
        zichtbaar = testsets

    # Resultaten indexeren per testset en stap
    res_index = {}
    for ts in resultaten.get('testsets', []):
        ts_id = ts['id']
        for stap in ts.get('stappen', []):
            res_index[(ts_id, stap['nr'])] = stap

    tellers = bereken_tellers_resultaten(scriptdata, resultaten)

    response = make_response(render_template(
        'testronden/script_detail.html',
        ronde_id=ronde_id,
        map_naam=map_naam,
        bestand=bestand,
        meta=meta,
        data=scriptdata,
        testsets=zichtbaar,
        alle_testsets=testsets,
        gekozen_ts=gekozen_ts,
        res_index=res_index,
        tellers=tellers,
        tester=tester,
    ))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response


# ── Resultaten opslaan ────────────────────────────────────────────────────────

@testronden_bp.route('/<ronde_id>/<map_naam>/<bestand>/opslaan', methods=['POST'])
@role_required('teacher')
def opslaan(ronde_id, map_naam, bestand):
    meta, _  = haal_testronde(ronde_id)
    tester   = huidige_tester()
    mod      = meta.get('modules', {}).get(map_naam, {})

    if mod.get('tester') != tester:
        flash('Deze module is niet aan jou toegewezen.', 'warning')
        return redirect(url_for('testronden.detail', ronde_id=ronde_id))

    scriptdata, _       = laad_bestand(map_naam, bestand)
    resultaten, res_sha = laad_resultaten(ronde_id, map_naam, bestand)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    gewijzigde_ts = set()

    # Bouw resultaten op vanuit formulier
    res_per_ts = {ts['id']: ts for ts in resultaten.get('testsets', [])}

    for ts in scriptdata.get('testsets', []):
        ts_id = ts['id']
        if ts_id not in res_per_ts:
            res_per_ts[ts_id] = {'id': ts_id, 'naam': ts.get('naam'), 'stappen': []}

        res_stappen = {s['nr']: s for s in res_per_ts[ts_id].get('stappen', [])}

        for stap in ts.get('stappen', []):
            nr          = stap.get('nr', '?')
            status_key  = f"status_{ts_id}_{nr}"
            notitie_key = f"notitie_{ts_id}_{nr}"

            nieuwe_status  = request.form.get(status_key)
            nieuwe_notitie = request.form.get(notitie_key, '').strip()

            if nr not in res_stappen:
                res_stappen[nr] = {'nr': nr}

            huidige = res_stappen[nr].get('status') or 'niet_getest'
            if nieuwe_status and nieuwe_status != huidige:
                res_stappen[nr]['status']     = nieuwe_status
                res_stappen[nr]['getest_op']  = now
                res_stappen[nr]['getest_door'] = tester
                gewijzigde_ts.add(ts_id)

            if nieuwe_notitie:
                res_stappen[nr]['notitie'] = nieuwe_notitie
            elif 'notitie' in res_stappen[nr] and not nieuwe_notitie:
                del res_stappen[nr]['notitie']

        res_per_ts[ts_id]['stappen'] = list(res_stappen.values())

    resultaten['testsets'] = list(res_per_ts.values())
    resultaten['ronde_id'] = ronde_id
    resultaten['module']   = map_naam

    if gewijzigde_ts:
        ts_label = ', '.join(sorted(gewijzigde_ts))
        succes = sla_resultaten_op(ronde_id, map_naam, bestand,
                                   resultaten, res_sha, tester, ts_label)
        if succes:
            flash(f'Opgeslagen ✅ — {ts_label}', 'success')
        else:
            flash('Opslaan mislukt.', 'danger')
    else:
        flash('Geen wijzigingen.', 'info')

    gekozen_ts = request.form.get('gekozen_ts', 'alle')
    return redirect(url_for(
        'testronden.script_detail',
        ronde_id=ronde_id,
        map_naam=map_naam,
        bestand=bestand,
        ts=gekozen_ts,
    ))


# ── Rapport van een testronde ─────────────────────────────────────────────────

@testronden_bp.route('/<ronde_id>/rapport')
@role_required('teacher')
def rapport(ronde_id):
    meta, _ = haal_testronde(ronde_id)
    modules_rapport = []

    for map_naam in meta.get('modules', {}):
        bestanden = haal_bestanden(map_naam)
        for b in bestanden:
            try:
                script, _     = laad_bestand(map_naam, b)
                resultaten, _ = laad_resultaten(ronde_id, map_naam, b)
                t = bereken_tellers_resultaten(script, resultaten)
                modules_rapport.append({
                    'map':       map_naam,
                    'bestand':   b,
                    'module':    script.get('module', b),
                    'tellers':   t,
                    'script':    script,
                    'resultaten': resultaten,
                })
            except Exception:
                pass

    return render_template(
        'testronden/rapport.html',
        meta=meta,
        ronde_id=ronde_id,
        modules_rapport=modules_rapport,
        datum=datetime.now().strftime('%Y-%m-%d'),
    )


# ── Snel opslaan (voor auto-save vanuit bevinding-knop) ───────────────────────

@testronden_bp.route('/<ronde_id>/<map_naam>/<bestand>/autosave', methods=['POST'])
@role_required('teacher')
def autosave(ronde_id, map_naam, bestand):
    """
    Sla resultaten op zonder redirect — gebruikt door de auto-save
    wanneer een tester op de bevinding-knop klikt.
    Geeft JSON terug zodat fetch() het kan afhandelen.
    """
    from flask import jsonify
    meta, _  = haal_testronde(ronde_id)
    tester   = huidige_tester()
    mod      = meta.get('modules', {}).get(map_naam, {})

    if mod.get('tester') != tester:
        return jsonify({'ok': False, 'reden': 'niet jouw module'}), 403

    scriptdata, _       = laad_bestand(map_naam, bestand)
    resultaten, res_sha = laad_resultaten(ronde_id, map_naam, bestand)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    gewijzigde_ts = set()

    res_per_ts = {ts['id']: ts for ts in resultaten.get('testsets', [])}

    for ts in scriptdata.get('testsets', []):
        ts_id = ts['id']
        if ts_id not in res_per_ts:
            res_per_ts[ts_id] = {'id': ts_id, 'naam': ts.get('naam'), 'stappen': []}

        res_stappen = {s['nr']: s for s in res_per_ts[ts_id].get('stappen', [])}

        for stap in ts.get('stappen', []):
            nr         = stap.get('nr', '?')
            status_key = f"status_{ts_id}_{nr}"
            nieuwe_status = request.form.get(status_key)

            if nr not in res_stappen:
                res_stappen[nr] = {'nr': nr}

            huidige = res_stappen[nr].get('status') or 'niet_getest'
            if nieuwe_status and nieuwe_status != huidige:
                res_stappen[nr]['status']      = nieuwe_status
                res_stappen[nr]['getest_op']   = now
                res_stappen[nr]['getest_door'] = tester
                gewijzigde_ts.add(ts_id)

            notitie = request.form.get(f"notitie_{ts_id}_{nr}", '').strip()
            if notitie:
                res_stappen[nr]['notitie'] = notitie

        res_per_ts[ts_id]['stappen'] = list(res_stappen.values())

    resultaten['testsets'] = list(res_per_ts.values())
    resultaten['ronde_id'] = ronde_id
    resultaten['module']   = map_naam

    if gewijzigde_ts:
        ts_label = ', '.join(sorted(gewijzigde_ts))
        succes = sla_resultaten_op(ronde_id, map_naam, bestand,
                                   resultaten, res_sha, tester, ts_label)
        return jsonify({'ok': succes})

    return jsonify({'ok': True, 'info': 'geen wijzigingen'})
