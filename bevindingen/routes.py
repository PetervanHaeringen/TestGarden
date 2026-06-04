from flask import render_template, request, redirect, url_for, flash, session, Response
from . import bevindingen_bp
from users.roles import role_required
from github_service import (
    volgend_bevinding_id,
    sla_bevinding_op,
    upload_screenshot,
    koppel_bevinding_aan_stap,
    haal_alle_bevindingen,
    laad_bestand,
    screenshot_url,
    haal_screenshot_bytes,
)
from datetime import datetime


def huidige_tester() -> str:
    return session.get("username", "onbekend")


# ── Overzicht alle bevindingen ────────────────────────────────────────────────

@bevindingen_bp.route("/")
@role_required("teacher")
def overzicht():
    bevindingen = haal_alle_bevindingen()
    return render_template(
        "bevindingen/overzicht.html",
        bevindingen=bevindingen,
        screenshot_url=screenshot_url,
    )


# ── Nieuw formulier (vanuit testscript-stap) ──────────────────────────────────

@bevindingen_bp.route("/nieuw")
@role_required("teacher")
def nieuw():
    """
    Formulier om een bevinding aan te maken.
    Ontvangt context via querystring vanuit het testscript:
    ?map=inplannen&bestand=tc_2.0...yaml&ts=TC_2.1&stap=4
    """
    map_naam  = request.args.get("map", "")
    bestand   = request.args.get("bestand", "")
    ts_id     = request.args.get("ts", "")
    stap_nr   = request.args.get("stap", "")
    ronde_id  = request.args.get("ronde", "")

    # Haal de stap-context op uit het testscript voor voorinvulling
    voorinvulling = {}
    if map_naam and bestand and ts_id and stap_nr:
        try:
            data, _ = laad_bestand(map_naam, bestand)
            for ts in data.get("testsets", []):
                if ts["id"] == ts_id:
                    for stap in ts.get("stappen", []):
                        if str(stap.get("nr")) == str(stap_nr):
                            voorinvulling = {
                                "stappen":          stap.get("actie", ""),
                                "verwacht":         stap.get("verwacht", ""),
                                "module_naam":      data.get("module", ""),
                            }
                            break
        except Exception:
            pass

    bev_id = volgend_bevinding_id()

    return render_template(
        "bevindingen/nieuw.html",
        bev_id=bev_id,
        map_naam=map_naam,
        bestand=bestand,
        ts_id=ts_id,
        stap_nr=stap_nr,
        ronde_id=ronde_id,
        voorinvulling=voorinvulling,
        tester=huidige_tester(),
    )


# ── Opslaan nieuwe bevinding ──────────────────────────────────────────────────

@bevindingen_bp.route("/opslaan", methods=["POST"])
@role_required("teacher")
def opslaan():
    tester   = huidige_tester()
    bev_id   = request.form.get("bev_id", volgend_bevinding_id())
    map_naam = request.form.get("map_naam", "")
    bestand  = request.form.get("bestand", "")
    ts_id    = request.form.get("ts_id", "")
    stap_nr  = request.form.get("stap_nr", "")
    ronde_id = request.form.get("ronde_id", "")

    # ── Screenshots uploaden ──────────────────────────────────────────────────
    screenshot_paden = []
    bestanden = request.files.getlist("screenshots")
    for f in bestanden:
        if f and f.filename:
            pad = upload_screenshot(bev_id, f.filename, f.read(), tester)
            if pad:
                screenshot_paden.append(pad)
            else:
                flash(f"Screenshot '{f.filename}' kon niet worden geüpload.", "warning")

    # ── Bevinding YAML samenstellen ───────────────────────────────────────────
    bevinding = {
        "id":               bev_id,
        "datum":            datetime.now().strftime("%Y-%m-%d"),
        "tester":           tester,
        "prioriteit":       request.form.get("prioriteit", "gemiddeld"),
        "status":           "open",
        "testronde":        ronde_id,
        "testscript":       f"{map_naam}/{bestand}" if bestand else "",
        "testset":          ts_id,
        "stap":             int(stap_nr) if stap_nr.isdigit() else stap_nr,
        "omschrijving":     request.form.get("omschrijving", "").strip(),
        "stappen":          request.form.get("stappen", "").strip(),
        "verwacht":         request.form.get("verwacht", "").strip(),
        "daadwerkelijk":    request.form.get("daadwerkelijk", "").strip(),
        "screenshots":      screenshot_paden,
    }
    # Lege velden weglaten
    bevinding = {k: v for k, v in bevinding.items()
                 if v not in (None, "", [], 0)}

    # ── Opslaan in GitHub ─────────────────────────────────────────────────────
    succes = sla_bevinding_op(bevinding, tester)

    if succes:
        # Koppel het bevinding-ID terug aan de teststap
        if map_naam and bestand and ts_id and stap_nr:
            koppel_bevinding_aan_stap(
                map_naam, bestand, ts_id,
                int(stap_nr) if stap_nr.isdigit() else stap_nr,
                bev_id, tester,
            )
        flash(f"Bevinding {bev_id} aangemaakt ✅", "success")
    else:
        flash("Opslaan mislukt. Controleer de GitHub-verbinding.", "danger")

    # Terug naar het testscript — testronde als dat de context was
    if ronde_id and map_naam and bestand:
        return redirect(url_for(
            "testronden.script_detail",
            ronde_id=ronde_id,
            map_naam=map_naam,
            bestand=bestand,
            ts=ts_id or "alle",
        ))
    if map_naam and bestand:
        return redirect(url_for(
            "scripts.script_detail",
            map_naam=map_naam,
            bestand=bestand,
            ts=ts_id or "alle",
        ))
    return redirect(url_for("bevindingen.overzicht"))


# ── Detail van één bevinding ──────────────────────────────────────────────────

@bevindingen_bp.route("/<bev_id>")
@role_required("teacher")
def detail(bev_id):
    try:
        data, _ = laad_bestand("bevindingen", f"{bev_id}.yaml")
    except Exception:
        flash(f"Bevinding {bev_id} niet gevonden.", "danger")
        return redirect(url_for("bevindingen.overzicht"))

    return render_template(
        "bevindingen/detail.html",
        bev=data,
        screenshot_url=screenshot_url,
    )


# ── Screenshot proxy ──────────────────────────────────────────────────────────

@bevindingen_bp.route("/screenshot/<bestandsnaam>")
@role_required("teacher")
def screenshot_proxy(bestandsnaam):
    """
    Haal een screenshot op via de GitHub API en stuur het door naar de browser.
    Zo werkt het ook voor private repositories.
    """
    data = haal_screenshot_bytes(bestandsnaam)
    if data is None:
        return "Screenshot niet gevonden", 404

    # Bepaal het mime-type op basis van de extensie
    ext = bestandsnaam.rsplit(".", 1)[-1].lower()
    mime_types = {
        "png":  "image/png",
        "jpg":  "image/jpeg",
        "jpeg": "image/jpeg",
        "gif":  "image/gif",
        "webp": "image/webp",
    }
    mime = mime_types.get(ext, "image/png")

    return Response(data, mimetype=mime)

@bevindingen_bp.route("/rapport")
@role_required("teacher")
def rapport():
    # Optioneel filteren op testronde
    filter_ronde = request.args.get("ronde", "")
    alle = haal_alle_bevindingen()

    if filter_ronde:
        bevindingen = [b for b in alle if b.get("testronde") == filter_ronde
                       or b.get("ronde_id") == filter_ronde]
    else:
        bevindingen = alle

    # Groepeer op prioriteit
    per_prioriteit = {"kritiek": [], "hoog": [], "gemiddeld": [], "laag": []}
    for b in bevindingen:
        p = b.get("prioriteit", "gemiddeld")
        per_prioriteit.setdefault(p, []).append(b)

    # Haal beschikbare testronden op voor de filter-dropdown
    from github_service import haal_alle_testronden
    testronden = haal_alle_testronden()

    return render_template(
        "bevindingen/rapport.html",
        bevindingen=bevindingen,
        per_prioriteit=per_prioriteit,
        screenshot_url=screenshot_url,
        datum=datetime.now().strftime("%Y-%m-%d"),
        filter_ronde=filter_ronde,
        testronden=testronden,
    )
