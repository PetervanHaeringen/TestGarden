# =============================================================================
# teacher/routes.py — Routes voor de teacher-omgeving
# =============================================================================
# Dit bestand bevat alle pagina's die teachers (en admins) kunnen zien.
#
# Naast de bestaande dashboards zijn hier de toewijzingsroutes toegevoegd:
#
#   /teacher/toewijzen
#       Overzicht van alle studenten — kies wie je wilt bewerken.
#
#   /teacher/toewijzen/<user_id>
#       Toewijzingsformulier voor één student:
#         - stel module_visibility in (wat ziet de student in Mijn Tuin?)
#         - vink modules aan die de student krijgt
#         - sla op
#
# Beschikbare modules komen uit twee bronnen:
#   1. Template-systeem : TESTEN_STEPS (hardcoded Python)
#   2. Content-systeem  : .yaml/.md bestanden via load_track_modules()
#
# De UserModule tabel gebruikt "id" uit meta.yaml als canonieke slug,
# bijvoorbeeld "softwaretesten.m01". Template-modules gebruiken hun eigen
# slug-conventie, zoals "testen_m1".
#
# Bij verwijderde modules: een toewijzing waarvan de slug niet meer bestaat
# in de beschikbare modules wordt getoond als "(module niet meer beschikbaar)".
# De teacher kan die toewijzing dan handmatig verwijderen.
# =============================================================================

from flask import render_template, redirect, url_for, request, flash, session
from database.models import db, User, UserModule, Answer
from instructions.question_bank_testen import TESTEN_STEPS, TESTEN_QUESTION_BANK
from . import teacher_bp
from core.content_loader import load_track_modules, load_lesson
from users.admin import admin_required
from users.utils import login_required
from datetime import datetime
from core.track_loader import load_all_tracks, load_track
from pathlib import Path
from translations.utils import clear_translation_cache
import json

# -----------------------------------------------------------------------------
# Vertaaloverzicht: bekijk en bewerk de vertalingen per doeltaal
# -----------------------------------------------------------------------------

TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent / "translations"


def load_translation_file(lang: str) -> dict:
    file_path = TRANSLATIONS_DIR / f"{lang}.json"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


@teacher_bp.route("/translations")
@login_required
def translation_overview():
    lang = request.args.get("lang", "en")

    nl_data = load_translation_file("nl")
    target_data = load_translation_file(lang)

    all_keys = sorted(set(nl_data.keys()) | set(target_data.keys()))

    rows = []
    for key in all_keys:
        nl_entry = nl_data.get(key, {})
        target_entry = target_data.get(key, {})

        nl_text = nl_entry.get("text", "") if isinstance(nl_entry, dict) else nl_entry
        target_text = target_entry.get("text", "") if isinstance(target_entry, dict) else target_entry

        used_in = ""
        if isinstance(nl_entry, dict):
            used_in = nl_entry.get("used_in", "")
        elif isinstance(target_entry, dict):
            used_in = target_entry.get("used_in", "")

        if not target_text:
            status = "missing"
        elif target_text == nl_text:
            status = "same_as_source"
        else:
            status = "translated"

        rows.append({
            "key": key,
            "used_in": used_in,
            "nl": nl_text,
            "target": target_text,
            "status": status,
        })

    return render_template(
        "translation_overview.html",
        selected_lang=lang,
        rows=rows,
    )


@teacher_bp.route("/translations/update", methods=["POST"])
@login_required
def update_translation():
    key = request.form.get("key")
    lang = request.form.get("lang")
    new_text = request.form.get("text")

    file_path = TRANSLATIONS_DIR / f"{lang}.json"

    data = load_translation_file(lang)

    entry = data.get(key, {})
    if isinstance(entry, dict):
        entry["text"] = new_text
    else:
        entry = {"text": new_text, "used_in": ""}

    data[key] = entry

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    clear_translation_cache()

    return redirect(url_for("teacher.translation_overview", lang=lang))


# -----------------------------------------------------------------------------
# Hulpfunctie: verzamel alle beschikbare modules uit beide systemen
# -----------------------------------------------------------------------------

def get_all_available_modules():
    """
    Geeft een gecombineerde lijst van alle modules uit beide systemen.
    Elk item heeft: slug, title, system ("template" of "content"), track
    """
    modules = []

    # 1. Template-modules (uit de Python question bank)
    for step in TESTEN_STEPS:
        slug = step["module_slug"]
        modules.append({
            "slug":   slug,
            "title":  step["title"],
            "system": "template",
            "track":  "softwaretesten",
            "order":  step.get("order", 999),
        })

    # 2. Content-modules (uit .yaml/.md bestanden)
    for track in ["softwaretesten", "git", "developer"]:  # uitbreidbaar: voeg tracks toe als ze komen
        for module in load_track_modules(track):
            # Voorkom dubbele slugs als content-module dezelfde slug heeft als template
            if any(m["slug"] == module["module_slug"] for m in modules):
                continue
            modules.append({
                "slug":   module["module_slug"],
                "title":  module["title"],
                "system": "content",
                "track":  track,
                "order":  module.get("order", 999),
            })

    track_priority = {"softwaretesten": 0, "git": 1, "developer": 2}
    modules.sort(key=lambda m: (track_priority.get(m["track"], 99), m.get("order", 999)))
    return modules


# =============================================================================
# CURSIST-VOLGEN — overzicht en detail per cursist
# =============================================================================
# Hier ziet de docent, gespiegeld aan de module-dashboards, wat één cursist
# heeft gedaan: aan welke modules is gewerkt, wanneer voor het laatst, en
# welke antwoorden zijn gegeven. De docent kan een antwoord handmatig op
# goed of fout zetten (override) waar het automatische oordeel tekortschiet.
#
# De data komt volledig uit de bestaande Answer-tabel. Geen migratie nodig.
# =============================================================================

from core.question_engine import get_question as _get_question_from_module
from instructions.question_bank_testen import TESTEN_QUESTION_BANK


def slug_titel_map():
    """Geeft {module_slug: titel} voor alle beschikbare modules."""
    return {m["slug"]: m["title"] for m in get_all_available_modules()}


def laad_module_vragen(module_slug):
    """
    Haalt de volledige module (met vragen) op voor een slug, uit welk
    systeem dan ook. Geeft (module_dict, titel) of (None, slug) terug.

    module_dict heeft minimaal {"questions": [...]}, waarbij elke vraag
    een "id", "text"/"vraag" en eventueel "answer" bevat.
    """
    # 1. Template-systeem (Python question bank)
    module = TESTEN_QUESTION_BANK.get(module_slug)
    if module:
        titel = module.get("title", module_slug)
        return module, titel

    # 2. Content-systeem (.yaml per track) — zoek de track waarin de slug zit
    for track in ["softwaretesten", "git", "developer"]:
        for m in load_track_modules(track):
            if m["module_slug"] == module_slug:
                lesson = load_lesson(track, m["folder"])
                if lesson:
                    return lesson, m["title"]
    return None, module_slug


def vraagtekst(vraag):
    """Robuust de leesbare vraagtekst pakken, ongeacht het veldnaam-schema."""
    for sleutel in ("text", "vraag", "question", "prompt", "title"):
        if vraag.get(sleutel):
            return vraag[sleutel]
    return vraag.get("id", "")


def _optie_tekst(vraag, optie_id):
    """Zoek bij een MCQ-vraag de tekst die bij een optie-id hoort.
    Geeft None terug als de optie niet gevonden wordt."""
    for optie in vraag.get("options", []):
        if str(optie.get("id")) == str(optie_id):
            return optie.get("text", "")
    return None


def leesbaar_antwoord(vraag, ruw_antwoord):
    """
    Maakt het opgeslagen antwoord leesbaar voor de docent.

    Voor MCQ: vertaalt de opgeslagen optie-id (bv. "c") naar de optietekst,
    en geeft erbij aan welke optie het juiste antwoord was.
    Voor andere vraagtypes: geeft het ruwe antwoord ongewijzigd terug.

    Geeft een dict terug:
      {
        "weergave":    tekst die getoond wordt als gegeven antwoord,
        "juist_tekst": tekst van het juiste antwoord (alleen bij mcq), of None,
      }
    """
    if vraag is None:
        return {"weergave": ruw_antwoord, "juist_tekst": None}

    if vraag.get("type") == "mcq":
        gegeven_tekst = _optie_tekst(vraag, ruw_antwoord)
        juiste_id = vraag.get("answer")
        juist_tekst = _optie_tekst(vraag, juiste_id)

        if gegeven_tekst is not None:
            weergave = f"{ruw_antwoord} — {gegeven_tekst}"
        else:
            # Onbekende optie-id (bv. nog niet beantwoord of oude data)
            weergave = ruw_antwoord

        if juist_tekst is not None:
            juist_weergave = f"{juiste_id} — {juist_tekst}"
        else:
            juist_weergave = None

        return {"weergave": weergave, "juist_tekst": juist_weergave}

    # Open vragen, true/false, etc. — laat staan
    return {"weergave": ruw_antwoord, "juist_tekst": None}


# -----------------------------------------------------------------------------
# Overzicht: alle cursisten, gesorteerd op laatste activiteit
# -----------------------------------------------------------------------------

@teacher_bp.route("/cursisten")
@login_required
def cursisten_overzicht():
    current_role = session.get("role")
    if current_role not in ("teacher", "admin"):
        flash("Geen toegang.", "danger")
        return redirect(url_for("core.index"))

    studenten = User.query.filter(User.role.in_(["student", "teacher"])) \
                          .order_by(User.username.asc()).all()

    overzicht = []
    for student in studenten:
        answers = Answer.query.filter_by(user_id=student.id).all()

        # Per module groeperen: tel antwoorden, goed, en pak laatste activiteit
        per_module = {}
        for a in answers:
            mod = per_module.setdefault(a.module_slug, {
                "aantal": 0, "goed": 0, "laatst": None,
            })
            mod["aantal"] += 1
            if a.is_correct:
                mod["goed"] += 1
            if mod["laatst"] is None or (a.updated_at and a.updated_at > mod["laatst"]):
                mod["laatst"] = a.updated_at

        laatst_actief = max(
            (m["laatst"] for m in per_module.values() if m["laatst"]),
            default=None,
        )

        overzicht.append({
            "student":        student,
            "modules_actief": len(per_module),
            "laatst_actief":  laatst_actief,
        })

    # Cursisten met recente activiteit bovenaan; nooit-actieven onderaan
    overzicht.sort(
        key=lambda r: (r["laatst_actief"] is not None, r["laatst_actief"]),
        reverse=True,
    )

    return render_template("cursisten_overzicht.html", overzicht=overzicht)


# -----------------------------------------------------------------------------
# Detail: één cursist — modules, voortgang, antwoorden, override
# -----------------------------------------------------------------------------

@teacher_bp.route("/cursisten/<int:user_id>", methods=["GET", "POST"])
@login_required
def cursist_detail(user_id):
    current_role = session.get("role")
    if current_role not in ("teacher", "admin"):
        flash("Geen toegang.", "danger")
        return redirect(url_for("core.index"))

    student = User.query.get_or_404(user_id)

    # ── POST: een antwoord handmatig op goed/fout zetten ─────────────────────
    if request.method == "POST":
        answer_id = request.form.get("answer_id")
        nieuw = request.form.get("oordeel")  # "goed" of "fout"
        row = Answer.query.filter_by(id=answer_id, user_id=user_id).first()
        if row and nieuw in ("goed", "fout"):
            row.is_correct = (nieuw == "goed")
            db.session.commit()
            flash("Beoordeling aangepast.", "success")
        else:
            flash("Kon de beoordeling niet aanpassen.", "warning")
        return redirect(url_for("teacher.cursist_detail", user_id=user_id))

    # ── GET: bouw het overzicht per module op ────────────────────────────────
    answers = Answer.query.filter_by(user_id=user_id) \
                          .order_by(Answer.module_slug).all()

    titels = slug_titel_map()

    # Groepeer antwoorden per module-slug
    modules = {}
    for a in answers:
        modules.setdefault(a.module_slug, []).append(a)

    module_blokken = []
    for slug, rijen in modules.items():
        module_def, titel = laad_module_vragen(slug)
        if titel == slug:  # geen titel gevonden via loader, val terug op map
            titel = titels.get(slug, slug)

        # Map question_id → vraagtekst en → volledige vraagdefinitie
        vraag_teksten = {}
        vraag_defs = {}
        totaal_vragen = len(rijen)
        if module_def:
            qs = module_def.get("questions", [])
            totaal_vragen = len(qs) or totaal_vragen
            for q in qs:
                vraag_teksten[q.get("id")] = vraagtekst(q)
                vraag_defs[q.get("id")] = q

        # Bouw per-antwoord regels, gesorteerd op question_id
        antwoorden = []
        for a in sorted(rijen, key=lambda r: str(r.question_id)):
            ruw = a.answer_text or a.last_answer or ""
            leesbaar = leesbaar_antwoord(vraag_defs.get(a.question_id), ruw)
            antwoorden.append({
                "id":          a.id,
                "vraag":       vraag_teksten.get(a.question_id, a.question_id),
                "question_id": a.question_id,
                "antwoord":    leesbaar["weergave"],
                "juist_tekst": leesbaar["juist_tekst"],
                "is_correct":  a.is_correct,
                "attempts":    a.attempts,
                "updated_at":  a.updated_at,
            })

        goed = sum(1 for a in rijen if a.is_correct)
        laatst = max((a.updated_at for a in rijen if a.updated_at), default=None)

        module_blokken.append({
            "slug":     slug,
            "titel":    titel,
            "goed":     goed,
            "totaal":   totaal_vragen,
            "laatst":   laatst,
            "antwoorden": antwoorden,
        })

    # Module waaraan het laatst gewerkt is bovenaan
    module_blokken.sort(
        key=lambda b: (b["laatst"] is not None, b["laatst"]),
        reverse=True,
    )

    laatst_actief = module_blokken[0]["laatst"] if module_blokken else None

    return render_template(
        "cursist_detail.html",
        student=student,
        module_blokken=module_blokken,
        laatst_actief=laatst_actief,
    )


# -----------------------------------------------------------------------------
# Overzicht: lijst van alle studenten
# -----------------------------------------------------------------------------

@teacher_bp.route("/toewijzen")
@login_required
def toewijzen_overzicht():
    """
    Toont alle studenten. De teacher klikt op een naam om modules toe te wijzen.
    Admins zien ook teachers in de lijst.
    """
    current_role = session.get("role")

    if current_role not in ("teacher", "admin"):
        flash("Geen toegang.", "danger")
        return redirect(url_for("core.index"))

    # Studenten (en teachers als je admin bent)
    students = User.query.filter(User.role.in_(["student", "teacher"])) \
                         .order_by(User.username.asc()).all()

    # Tel het aantal toegewezen modules per student
    toewijzingen = {}
    for student in students:
        toewijzingen[student.id] = UserModule.query.filter_by(user_id=student.id).count()

    return render_template(
        "toewijzen_overzicht.html",
        students=students,
        toewijzingen=toewijzingen,
    )


# -----------------------------------------------------------------------------
# Toewijzingsformulier voor één student (GET = toon, POST = opslaan)
# -----------------------------------------------------------------------------

@teacher_bp.route("/toewijzen/<int:user_id>", methods=["GET", "POST"])
@login_required
def toewijzen_student(user_id):
    """
    GET: Toon het formulier — welke modules heeft de student al, wat is beschikbaar?
    POST: Verwerk de wijzigingen en sla op in de database.
    """
    current_role = session.get("role")

    if current_role not in ("teacher", "admin"):
        flash("Geen toegang.", "danger")
        return redirect(url_for("core.index"))

    student = User.query.get_or_404(user_id)
    alle_modules = get_all_available_modules()

    # Slugs van al toegewezen modules voor deze student
    toegewezen = UserModule.query.filter_by(user_id=user_id) \
                                 .order_by(UserModule.volgorde).all()
    toegewezen_slugs = {t.module_slug for t in toegewezen}

    # Wees-kind toewijzingen: slug bestaat niet meer in beschikbare modules
    beschikbare_slugs = {m["slug"] for m in alle_modules}
    wees_toewijzingen = [t for t in toegewezen if t.module_slug not in beschikbare_slugs]

    if request.method == "POST":
        # Lees de ingevulde waarden uit het formulier
        nieuwe_visibility = request.form.get("module_visibility", "alleen_toegewezen")
        gekozen_slugs = set(request.form.getlist("modules"))  # aangevinkte checkboxes

        # Sla module_visibility op op de student
        student.module_visibility = nieuwe_visibility

        # Verwijder toewijzingen die niet meer aangevinkt zijn
        # (maar laat wees-toewijzingen staan totdat de teacher ze bewust verwijdert)
        for toewijzing in toegewezen:
            if toewijzing.module_slug in beschikbare_slugs:
                if toewijzing.module_slug not in gekozen_slugs:
                    db.session.delete(toewijzing)

        # Voeg nieuwe toewijzingen toe
        huidige_volgorde = len(toegewezen_slugs) + 1
        for slug in gekozen_slugs:
            if slug not in toegewezen_slugs:
                nieuwe = UserModule(
                    user_id=user_id,
                    module_slug=slug,
                    assigned_by=session["user_id"],
                    assigned_at=datetime.utcnow(),
                    volgorde=huidige_volgorde,
                )
                db.session.add(nieuwe)
                huidige_volgorde += 1

        db.session.commit()
        flash(f"Toewijzingen voor {student.username} opgeslagen.", "success")
        return redirect(url_for("teacher.toewijzen_overzicht"))

    return render_template(
        "toewijzen_student.html",
        student=student,
        alle_modules=alle_modules,
        toegewezen_slugs=toegewezen_slugs,
        wees_toewijzingen=wees_toewijzingen,
    )


# -----------------------------------------------------------------------------
# Wees-toewijzing verwijderen (module bestaat niet meer)
# -----------------------------------------------------------------------------

@teacher_bp.route("/toewijzen/<int:user_id>/verwijder/<int:toewijzing_id>", methods=["POST"])
@login_required
def toewijzing_verwijderen(user_id, toewijzing_id):
    """
    Verwijdert één wees-toewijzing: een module die niet meer bestaat
    maar nog wel gekoppeld is aan de student.
    """
    current_role = session.get("role")

    if current_role not in ("teacher", "admin"):
        flash("Geen toegang.", "danger")
        return redirect(url_for("core.index"))

    toewijzing = UserModule.query.get_or_404(toewijzing_id)

    if toewijzing.user_id != user_id:
        flash("Ongeldige actie.", "warning")
        return redirect(url_for("teacher.toewijzen_overzicht"))

    db.session.delete(toewijzing)
    db.session.commit()
    flash("Toewijzing verwijderd.", "success")
    return redirect(url_for("teacher.toewijzen_student", user_id=user_id))


# -----------------------------------------------------------------------------
# Bestaande dashboards (ongewijzigd)
# -----------------------------------------------------------------------------

@teacher_bp.route("/content-testen")
@login_required
def teacher_content_testen_dashboard():
    modules = load_track_modules("softwaretesten")
    users = User.query.all()

    module_stats = []

    for module in modules:
        lesson = load_lesson("softwaretesten", module["folder"])

        if not lesson:
            continue

        module_slug = lesson["module_slug"]
        total_questions = len(lesson["questions"])

        done = 0
        in_progress = 0
        not_started = 0

        for user in users:
            answers = Answer.query.filter_by(
                user_id=user.id,
                module_slug=module_slug
            ).all()

            if not answers:
                not_started += 1
                continue

            correct = sum(1 for a in answers if a.is_correct)

            if correct == total_questions:
                done += 1
            else:
                in_progress += 1

        module_stats.append({
            "title":       module["title"],
            "slug":        module_slug,
            "done":        done,
            "progress":    in_progress,
            "not_started": not_started,
            "available":   True
        })

    return render_template("testen_dashboard.html", modules=module_stats)

# =============================================================================
# Toevoeging Git aan dashboard
# =============================================================================

@teacher_bp.route("/content-git")
@login_required
def teacher_content_git_dashboard():
    modules = load_track_modules("git")
    users = User.query.all()

    module_stats = []

    for module in modules:
        lesson = load_lesson("git", module["folder"])

        if not lesson:
            continue

        module_slug = lesson["module_slug"]
        total_questions = len(lesson["questions"])

        done = 0
        in_progress = 0
        not_started = 0

        for user in users:
            answers = Answer.query.filter_by(
                user_id=user.id,
                module_slug=module_slug
            ).all()

            if not answers:
                not_started += 1
                continue

            correct = sum(1 for a in answers if a.is_correct)

            if correct == total_questions:
                done += 1
            else:
                in_progress += 1

        module_stats.append({
            "title":       module["title"],
            "slug":        module_slug,
            "done":        done,
            "progress":    in_progress,
            "not_started": not_started,
            "available":   True
        })

    return render_template("testen_dashboard.html", modules=module_stats)


@teacher_bp.route("/content-developer")
@login_required
def teacher_content_developer_dashboard():
    modules = load_track_modules("developer")
    users = User.query.all()

    module_stats = []

    for module in modules:
        lesson = load_lesson("developer", module["folder"])

        if not lesson:
            continue

        module_slug = lesson["module_slug"]
        total_questions = len(lesson["questions"])

        done = 0
        in_progress = 0
        not_started = 0

        for user in users:
            answers = Answer.query.filter_by(
                user_id=user.id,
                module_slug=module_slug
            ).all()

            if not answers:
                not_started += 1
                continue

            correct = sum(1 for a in answers if a.is_correct)

            if correct == total_questions:
                done += 1
            else:
                in_progress += 1

        module_stats.append({
            "title":       module["title"],
            "slug":        module_slug,
            "done":        done,
            "progress":    in_progress,
            "not_started": not_started,
            "available":   True
        })

    return render_template("testen_dashboard.html", modules=module_stats)


@teacher_bp.route("/testen")
@login_required
def teacher_testen_dashboard():
    module_stats = []
    users = User.query.all()

    for step in TESTEN_STEPS:
        slug = step["module_slug"]
        module = TESTEN_QUESTION_BANK.get(slug)

        if not module:
            module_stats.append({
                "title":       step["title"],
                "slug":        slug,
                "done":        0,
                "progress":    0,
                "not_started": 0,
                "available":   False,
            })
            continue

        total_questions = len(module["questions"])
        done = 0
        in_progress = 0
        not_started = 0

        for user in users:
            answers = Answer.query.filter_by(
                user_id=user.id,
                module_slug=slug
            ).all()

            if not answers:
                not_started += 1
                continue

            correct = sum(1 for a in answers if a.is_correct)

            if correct == total_questions:
                done += 1
            else:
                in_progress += 1

        module_stats.append({
            "title":       step["title"],
            "slug":        slug,
            "done":        done,
            "progress":    in_progress,
            "not_started": not_started,
            "available":   True,
        })

    return render_template("testen_dashboard.html", modules=module_stats)






# =============================================================================
# PRAKTIJKBEOORDELING — teacher interface
# =============================================================================
# Hier beoordeelt de docent de praktijkopdrachten van cursisten en vult
# het formele eindoordeel in per werkproces.
#
# Twee routes:
#   /teacher/praktijk              → overzicht van alle cursisten
#   /teacher/praktijk/<user_id>    → beoordelingsscherm per cursist
# =============================================================================

from core.praktijk_loader import laad_opdrachten, bereken_dekking, alle_werkprocessen
from database.models import PraktijkOpdracht, PraktijkBeoordeling


@teacher_bp.route("/praktijk")
@login_required
def praktijk_overzicht():
    """
    Toont alle cursisten met hun voortgang op praktijkopdrachten.
    De docent kiest een cursist om naar het beoordelingsscherm te gaan.
    """
    current_role = session.get("role")
    if current_role not in ("teacher", "admin"):
        flash("Geen toegang.", "danger")
        return redirect(url_for("core.index"))

    studenten = User.query.filter_by(role="student").order_by(User.username).all()

    overzicht = []
    for student in studenten:
        # Tel voldane opdrachten per leerpad
        voldaan = PraktijkOpdracht.query.filter_by(
            user_id=student.id, voldaan=True
        ).count()

        totaal_servicedesk = len(laad_opdrachten("servicedesk"))

        overzicht.append({
            "student":          student,
            "voldaan":          voldaan,
            "totaal":           totaal_servicedesk,
        })

    return render_template("praktijk_overzicht.html", overzicht=overzicht)


@teacher_bp.route("/praktijk/<int:user_id>", methods=["GET", "POST"])
@login_required
def praktijk_student(user_id):
    """
    Beoordelingsscherm voor één cursist.

    GET:  Toont alle opdrachten, de competentiedekking en het beoordelingsformulier.
    POST: Slaat afgevinkte opdrachten en/of formele beoordelingen op.
    """
    current_role = session.get("role")
    if current_role not in ("teacher", "admin"):
        flash("Geen toegang.", "danger")
        return redirect(url_for("core.index"))

    student = User.query.get_or_404(user_id)
    leerpad = request.args.get("leerpad", "servicedesk")  # uitbreidbaar: via request parameter

    opdrachten = laad_opdrachten(leerpad)

    # Huidige beoordelingen ophalen uit database
    bestaande = {
        p.opdracht_id: p
        for p in PraktijkOpdracht.query.filter_by(
            user_id=user_id, leerpad=leerpad
        ).all()
    }

    if request.method == "POST":
        actie = request.form.get("actie")

        # ── Opdrachten afvinken ──────────────────────────────────────────────
        if actie == "opdrachten":
            for opdracht in opdrachten:
                oid = opdracht["ticket_id"]
                voldaan = oid in request.form.getlist("voldaan")
                notitie = request.form.get(f"notitie_{oid}", "").strip()

                if oid in bestaande:
                    # Bijwerken
                    bestaande[oid].voldaan = voldaan
                    bestaande[oid].notitie = notitie
                    bestaande[oid].beoordeeld_door = session["user_id"]
                    bestaande[oid].beoordeeld_op = datetime.utcnow()
                else:
                    # Nieuw aanmaken
                    nieuw = PraktijkOpdracht(
                        user_id=user_id,
                        opdracht_id=oid,
                        leerpad=leerpad,
                        kader="mbo_25999",
                        beoordeeld_door=session["user_id"],
                        voldaan=voldaan,
                        notitie=notitie,
                    )
                    db.session.add(nieuw)

            db.session.commit()
            flash("Opdrachten opgeslagen.", "success")

        # ── Formele beoordeling per werkproces ───────────────────────────────
        elif actie == "beoordeling":
            werkprocessen = alle_werkprocessen(leerpad)

            for code in werkprocessen:
                tussen = request.form.get(f"tussen_{code}") or None
                eind   = request.form.get(f"eind_{code}") or None
                notitie_docent = request.form.get(f"notitie_{code}", "").strip()
                goed    = request.form.get(f"goed_{code}", "").strip()
                beter   = request.form.get(f"beter_{code}", "").strip()
                geleerd = request.form.get(f"geleerd_{code}", "").strip()

                bestaande_b = PraktijkBeoordeling.query.filter_by(
                    user_id=user_id,
                    leerpad=leerpad,
                    werkproces_code=code,
                ).first()

                if bestaande_b:
                    bestaande_b.tussenevaluatie = tussen
                    bestaande_b.eindbeoordeling = eind
                    bestaande_b.notitie_docent  = notitie_docent
                    bestaande_b.zelfevaluatie_goed    = goed
                    bestaande_b.zelfevaluatie_beter   = beter
                    bestaande_b.zelfevaluatie_geleerd = geleerd
                    if tussen and not bestaande_b.datum_tussen:
                        bestaande_b.datum_tussen = datetime.utcnow()

                    if eind and not bestaande_b.datum_eind:
                        bestaande_b.datum_eind = datetime.utcnow()
                else:
                    nieuwe_b = PraktijkBeoordeling(
                        user_id=user_id,
                        leerpad=leerpad,
                        kader="mbo_25999",
                        werkproces_code=code,
                        beoordeeld_door=session["user_id"],
                        tussenevaluatie=tussen,
                        eindbeoordeling=eind,
                        notitie_docent=notitie_docent,
                        datum_tussen=datetime.utcnow() if tussen else None,
                        datum_eind=datetime.utcnow() if eind else None,
                        zelfevaluatie_goed=goed,
                        zelfevaluatie_beter=beter,
                        zelfevaluatie_geleerd=geleerd,
                    )
                    db.session.add(nieuwe_b)

            db.session.commit()
            flash("Beoordeling opgeslagen.", "success")

        return redirect(url_for("teacher.praktijk_student", user_id=user_id))

    # ── GET: bouw het overzicht op ───────────────────────────────────────────

    voldane_ids = {oid for oid, p in bestaande.items() if p.voldaan}
    dekking = bereken_dekking(leerpad, voldane_ids)

    werkprocessen = alle_werkprocessen(leerpad)
    beoordelingen = {
        b.werkproces_code: b
        for b in PraktijkBeoordeling.query.filter_by(
            user_id=user_id, leerpad=leerpad
        ).all()
    }

    return render_template(
        "praktijk_student.html",
        student=student,
        opdrachten=opdrachten,
        bestaande=bestaande,
        voldane_ids=voldane_ids,
        dekking=dekking,
        werkprocessen=werkprocessen,
        beoordelingen=beoordelingen,
        leerpad=leerpad,
    )


# weergave track overzicht leerlijnen

@teacher_bp.route("/leerlijnen")
@login_required
def leerlijnen_overzicht():
    current_role = session.get("role")

    if current_role not in ("teacher", "admin"):
        flash("Geen toegang.", "danger")
        return redirect(url_for("core.index"))

    tracks = load_all_tracks()

    return render_template(
        "leerlijnen_overzicht.html",
        tracks=tracks
    )