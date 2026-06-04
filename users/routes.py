# =============================================================================
# users/routes.py — Gebruikersroutes voor TestGarden
# =============================================================================
# Dit bestand bevat alles rondom inloggen, registreren, uitloggen,
# het dashboard (Mijn Tuin) en de admin-functies.
#
# Het dashboard is het hart van de leerervaring voor de cursist.
# Het laadt modules dynamisch op basis van:
#   - UserModule tabel  : welke modules zijn toegewezen aan deze cursist?
#   - module_visibility : wat mag de cursist zien?
#       "alleen_toegewezen" → alleen eigen modules
#       "vergrendeld"       → alles zichtbaar, niet-toegewezen zijn grijs
#       "alles"             → alles vrij toegankelijk
# =============================================================================

from flask import render_template, redirect, url_for, request, flash, session
from sqlalchemy.exc import IntegrityError
from . import users_bp
from database.models import db, User, UserModule
from users.admin import admin_required
from users.utils import login_required
from instructions.question_bank_testen import TESTEN_STEPS, TESTEN_QUESTION_BANK
from core.question_engine import compute_step_status, compute_progress
from core.content_loader import load_track_modules, load_lesson
from core.track_loader import load_track

DASHBOARD_THEMES = {
    "plain":  {"label": "cijfers", "icons": ["—", "▶", "✓"],  "labels": ["niet gestart", "bezig", "afgerond"]},
    "plant":  {"label": "Plant",   "icons": ["🫘", "🌱", "🌿"], "labels": ["zaadje", "groeit", "geoogst"]},
    "animal": {"label": "Eend",    "icons": ["🥚", "🐣", "🦆"], "labels": ["ei", "kuiken", "eend"]},
    "game":   {"label": "Game",    "icons": ["🔒", "🗺️", "⚔️"], "labels": ["locked", "active", "completed"]},
}


# -----------------------------------------------------------------------------
# Hulpfunctie: bouw een lookup van alle beschikbare modules
# Geeft een dict terug: slug → {title, url, system, questions}
# -----------------------------------------------------------------------------

def build_module_lookup(track_id="softwaretesten"):
    """
    Bouwt één module-lookup op basis van de centrale track-yaml.
    De track bepaalt de volgorde en welke modules bij het leerpad horen.
    """
    lookup = {}
    track = load_track(track_id)

    if not track:
        return lookup

    for module in track.get("modules", []):
        slug = module["slug"]
        system = module.get("system")
        order = module.get("order", 999)

        if system == "template":
            step = next(
                (s for s in TESTEN_STEPS if s["module_slug"] == slug),
                None
            )

            if not step:
                continue

            module_data = TESTEN_QUESTION_BANK.get(slug)

            lookup[slug] = {
                "title": module.get("title", step["title"]),
                "url": url_for(step["endpoint"]),
                "system": "template",
                "order": order,
                "questions": module_data["questions"] if module_data else [],
            }

        elif system == "content":
            content_modules = load_track_modules(track_id)
            content_module = next(
                (m for m in content_modules if m["module_slug"] == slug),
                None
            )

            if not content_module:
                continue

            lesson = load_lesson(track_id, content_module["folder"])

            content_route_map = {
                "softwaretesten": "instructions.testen_content_module",
                "git":            "instructions.git_content_module",
                "developer":      "instructions.developer_content_module",
            }
            content_endpoint = content_route_map.get(track_id, "instructions.testen_content_module")

            lookup[slug] = {
                "title":     module.get("title", content_module["title"]),
                "url":       url_for(content_endpoint, module_name=content_module["folder"]),
                "system":    "content",
                "order":     order,
                "questions": lesson["questions"] if lesson else [],
            }

    return lookup


# -----------------------------------------------------------------------------
# REGISTREREN
# -----------------------------------------------------------------------------

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Vul alle velden in.", "error")
            return redirect(url_for("users.register"))

        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam bestaat al.", "error")
            return redirect(url_for("users.register"))

        if User.query.filter_by(email=email).first():
            flash("E-mailadres is al geregistreerd.", "error")
            return redirect(url_for("users.register"))

        user = User(username=username, email=email)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Deze gebruiker bestaat al (username/email).", "error")
            return redirect(url_for("users.register"))

        flash("Registratie succesvol! Log nu in.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html")


# -----------------------------------------------------------------------------
# INLOGGEN
# -----------------------------------------------------------------------------

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Ongeldige login.", "error")
            return redirect(url_for("users.login"))

        session["user_id"]  = user.id
        session["username"] = user.username
        session["role"]     = getattr(user, "role", "student")
        flash("Je bent succesvol ingelogd!", "success")

        next_url = request.args.get("next")
        return redirect(next_url or url_for("core.index"))

    return render_template("login.html")


# -----------------------------------------------------------------------------
# UITLOGGEN
# -----------------------------------------------------------------------------

@users_bp.route("/logout")
def logout():
    session.clear()
    flash("Je bent uitgelogd.", "success")
    return redirect(url_for("core.index"))


# -----------------------------------------------------------------------------
# DASHBOARD — Mijn Tuin
# Toont de modules van de cursist op basis van toewijzingen en zichtbaarheid
# -----------------------------------------------------------------------------

@users_bp.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    user    = User.query.get(user_id)

    theme_key = user.dashboard_theme or "plant"
    theme     = DASHBOARD_THEMES.get(theme_key, DASHBOARD_THEMES["plant"])
    visibility = user.module_visibility or "alleen_toegewezen"

    # Alle beschikbare modules als opzoektabel
    module_lookup = {}
    for track_id in ["softwaretesten", "git", "developer"]:
        module_lookup.update(build_module_lookup(track_id))

    # Toegewezen modules voor deze cursist, gesorteerd op volgorde
    toegewezen     = UserModule.query.filter_by(user_id=user_id).order_by(UserModule.volgorde).all()
    toegewezen_slugs = {t.module_slug for t in toegewezen}

    # Bepaal welke slugs getoond worden
    if visibility == "alleen_toegewezen":
        # Alleen toegewezen, maar gesorteerd op module-order
        te_tonen = sorted(
            [t.module_slug for t in toegewezen],
            key=lambda slug: module_lookup.get(slug, {}).get("order", 999)
        )
    else:
        # Vergrendeld of alles: toon alle bekende modules op module-order
        te_tonen = sorted(
            module_lookup.keys(),
            key=lambda slug: module_lookup.get(slug, {}).get("order", 999)
        )

    # Bouw de steps-lijst op
    steps = []
    total_correct   = 0
    total_questions = 0

    for nr, slug in enumerate(te_tonen, 1):
        info = module_lookup.get(slug)
        if not info:
            continue  # module bestaat niet meer (wees-slug), overslaan

        locked    = (visibility == "vergrendeld") and (slug not in toegewezen_slugs)
        questions = info["questions"]

        if not locked and questions:
            module_data = {"questions": questions}
            status   = compute_step_status(user_id, slug, module_data)
            progress = compute_progress(user_id, slug, module_data)
            total_correct   += progress["correct"]
            total_questions += progress["total"]
            pct = progress["percent"]
        else:
            status = "not"
            pct    = 0

        steps.append({
            "nr":     nr,
            "name":   info["title"],
            "url":    info["url"],
            "status": status,
            "pct":    pct,
            "locked": locked,
            "system": info["system"],
        })

    done_count  = sum(1 for s in steps if s["status"] == "done")
    overall_pct = int((total_correct / total_questions * 100)) if total_questions else 0

    return render_template(
        "dashboard.html",
        user=user,
        steps=steps,
        done_count=done_count,
        total=len(steps),
        overall_pct=overall_pct,
        total_correct=total_correct,
        total_questions=total_questions,
        theme=theme,
        theme_key=theme_key,
        themes=DASHBOARD_THEMES,
    )


# -----------------------------------------------------------------------------
# THEMA WISSELEN
# -----------------------------------------------------------------------------

@users_bp.post("/dashboard/theme")
@login_required
def dashboard_set_theme():
    user_id   = session["user_id"]
    user      = User.query.get(user_id)
    new_theme = request.form.get("theme", "plant")
    if new_theme in DASHBOARD_THEMES:
        user.dashboard_theme = new_theme
        db.session.commit()
    return redirect(url_for("users.dashboard"))


# -----------------------------------------------------------------------------
# CONTENT OVERZICHT (softwaretesten)
# -----------------------------------------------------------------------------

@users_bp.route("/content/softwaretesten")
@login_required
def user_content_softwaretesten():
    modules = load_track_modules("softwaretesten")
    return render_template("user_content_overview.html", modules=modules)


# -----------------------------------------------------------------------------
# ADMIN — rollen beheren
# -----------------------------------------------------------------------------

@users_bp.route("/admin")
@admin_required
def admin_panel():
    users = User.query.order_by(User.username.asc()).all()
    return render_template("admin.html", users=users)


@users_bp.route("/admin/set_role/<username>/<role>")
@admin_required
def admin_set_role(username, role):
    if role not in ("student", "tester", "teacher", "admin"):
        flash("Ongeldige rol.", "warning")
        return redirect(url_for("users.admin_panel"))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Gebruiker niet gevonden.", "warning")
        return redirect(url_for("users.admin_panel"))

    user.role = role
    db.session.commit()
    flash(f"{username} is nu {role}.", "success")
    return redirect(url_for("users.admin_panel"))


@users_bp.route("/admin/make_teacher/<username>")
@admin_required
def make_teacher(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Gebruiker niet gevonden", "warning")
        return redirect(url_for("core.index"))

    user.role = "teacher"
    db.session.commit()
    flash(f"{username} is nu docent.", "success")
    return redirect(url_for("core.index"))

@users_bp.route("/admin/verwijder/<int:user_id>", methods=["POST"])
@admin_required
def admin_verwijder_gebruiker(user_id):
    from database.models import Answer, UserModule, Progress

    user = User.query.get_or_404(user_id)

    Answer.query.filter_by(user_id=user_id).delete()
    UserModule.query.filter_by(user_id=user_id).delete()
    Progress.query.filter_by(user_id=user_id).delete()

    db.session.delete(user)
    db.session.commit()

    flash(f"{user.username} is verwijderd.", "success")
    return redirect(url_for("users.admin_panel"))
