from flask import render_template, request, redirect, url_for, flash, session
from . import scripts_bp
from users.roles import role_required
from github_service import (
    haal_mappen, haal_bestanden, laad_bestand,
    sla_bestand_op, bereken_tellers, haal_tc_label,
)
from datetime import datetime
import os
import markdown


def huidige_tester():
    return session.get('username', 'onbekend')


# ── Omgevingspagina ───────────────────────────────────────────────────────────

@scripts_bp.route('/omgeving')
@role_required('teacher')
def omgeving():
    """Laad de lokale omgevingsinformatie uit instance/van_der_valk.md"""
    pad = os.path.join(os.path.dirname(__file__), '..', 'instance', 'van_der_valk.md')
    pad = os.path.abspath(pad)
    inhoud_html = None
    fout = None
    try:
        with open(pad, encoding='utf-8') as f:
            tekst = f.read()
        inhoud_html = markdown.markdown(tekst, extensions=['tables'])
    except FileNotFoundError:
        fout = f"Bestand niet gevonden: {pad}"
    except Exception as e:
        fout = str(e)

    return render_template('scripts/omgeving.html',
                           inhoud=inhoud_html,
                           fout=fout)


# ── Overzicht ─────────────────────────────────────────────────────────────────

@scripts_bp.route('/')
@role_required('teacher')
def overzicht():
    mappen = haal_mappen()
    modules = []
    for map_naam in mappen:
        bestanden = haal_bestanden(map_naam)
        testsets = []
        if bestanden:
            try:
                data, _ = laad_bestand(map_naam, bestanden[0])
                for ts in data.get('testsets', []):
                    if ts.get('naam'):
                        testsets.append({
                            'id':      ts['id'],
                            'naam':    ts.get('naam', ''),
                            'bestand': bestanden[0],
                        })
            except Exception:
                pass
        modules.append({
            'map':              map_naam,
            'label':            haal_tc_label(map_naam),
            'aantal_bestanden': len(bestanden),
            'testsets':         testsets,
            'bestand':          bestanden[0] if bestanden else None,
        })
    return render_template('scripts/overzicht.html', modules=modules)


# ── Map: lijst van scripts ────────────────────────────────────────────────────

@scripts_bp.route('/<map_naam>')
@role_required('teacher')
def map_overzicht(map_naam):
    bestanden = haal_bestanden(map_naam)
    if len(bestanden) == 1:
        return redirect(url_for('scripts.script_detail',
                                map_naam=map_naam, bestand=bestanden[0]))
    scripts = []
    for b in bestanden:
        label = b.replace('.yaml', '').replace('_', ' ')
        scripts.append({'bestand': b, 'module': label})
    return render_template('scripts/map_overzicht.html',
                           map_naam=map_naam, scripts=scripts)


# ── Script detail ─────────────────────────────────────────────────────────────

@scripts_bp.route('/<map_naam>/<bestand>')
@role_required('teacher')
def script_detail(map_naam, bestand):
    data, sha = laad_bestand(map_naam, bestand)
    testsets = data.get('testsets', [])
    gekozen_ts = request.args.get('ts', 'alle')

    if gekozen_ts != 'alle':
        zichtbaar = [ts for ts in testsets if ts['id'] == gekozen_ts]
    else:
        zichtbaar = testsets

    return render_template(
        'scripts/script_detail.html',
        map_naam=map_naam,
        bestand=bestand,
        data=data,
        testsets=zichtbaar,
        alle_testsets=testsets,
        gekozen_ts=gekozen_ts,
        tellers=bereken_tellers(data),
        sha=sha,
        tester=huidige_tester(),
    )


# ── Opslaan naar GitHub ───────────────────────────────────────────────────────

@scripts_bp.route('/<map_naam>/<bestand>/opslaan', methods=['POST'])
@role_required('teacher')
def opslaan(map_naam, bestand):
    data, sha = laad_bestand(map_naam, bestand)
    tester = huidige_tester()
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    gewijzigde_ts = set()

    for ts in data.get('testsets', []):
        ts_id = ts['id']
        for stap in ts.get('stappen', []):
            nr = stap.get('nr', '?')
            status_key  = f"status_{ts_id}_{nr}"
            notitie_key = f"notitie_{ts_id}_{nr}"

            nieuwe_status  = request.form.get(status_key)
            nieuwe_notitie = request.form.get(notitie_key, '').strip()

            huidige_status = stap.get('status') or 'niet_getest'
            if nieuwe_status and nieuwe_status != huidige_status:
                stap['status']      = nieuwe_status
                stap['getest_op']   = now
                stap['getest_door'] = tester
                gewijzigde_ts.add(ts_id)

            if nieuwe_notitie:
                stap['notitie'] = nieuwe_notitie
            elif 'notitie' in stap and not nieuwe_notitie:
                del stap['notitie']

    if gewijzigde_ts:
        ts_label = ', '.join(sorted(gewijzigde_ts))
        succes = sla_bestand_op(map_naam, bestand, data, sha, tester, ts_label)
        if succes:
            flash(f'Opgeslagen ✅ — commit aangemaakt voor {ts_label}.', 'success')
        else:
            flash('Opslaan mislukt. Controleer de GitHub-verbinding.', 'danger')
    else:
        flash('Geen wijzigingen gevonden.', 'info')

    gekozen_ts = request.form.get('gekozen_ts', 'alle')
    return redirect(url_for(
        'scripts.script_detail',
        map_naam=map_naam,
        bestand=bestand,
        ts=gekozen_ts,
    ))
