# Testgarden/instructions/routes.py
from flask import render_template, request, redirect, url_for, abort, session, send_from_directory, current_app
from . import instructions_bp
from core.menu import get_all_menus
from users.utils import login_required
#from database.models import db, Answer
from core.question_engine import (
    check_answer,
    upsert_answer,
    compute_progress,
    get_answer_map,
    compute_step_status,
)
from .logic import get_module, get_question
from .question_bank_testen import TESTEN_STEPS
import markdown
from core.content_loader import load_lesson, load_track_modules
import os

# ================================================================
#  SOFTWARETESTEN – OVERVIEW
# ================================================================
@instructions_bp.route("/testen/overview")
@login_required
def testen_overview():
    # Studenten navigeren via hun eigen dashboard — het overzicht is voor docenten/admins
    if session.get("role", "student") not in ("teacher", "admin"):
        return redirect(url_for("users.dashboard"))

    user_id = session["user_id"]

    steps = []
    for s in TESTEN_STEPS:
        module = get_module(s["module_slug"])
        status = compute_step_status(user_id, s["module_slug"], module) if module else "not"

        steps.append({
            "nr": s["nr"],
            "title": s["title"],
            "endpoint": s["endpoint"],
            "status": status,
        })

    return render_template("testen/overview.html", steps=steps)


# ================================================================
#  SOFTWARETESTEN – INDIVIDUELE MODULES
# ================================================================
@instructions_bp.route("/testen/module1")
@login_required
def testen_module1():
    module_slug = "testen_m1"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module1_intro_testing.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )



@instructions_bp.route("/testen/module2")
@login_required
def testen_module2():
    module_slug = "testen_m2"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module2_testlevels_smoketests.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )


@instructions_bp.route("/testen/module3")
@login_required
def testen_module3():
    module_slug = "testen_m3"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module3_testplan_risico.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )


@instructions_bp.route("/testen/module4")
@login_required
def testen_module4():
    module_slug = "testen_m4"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module4_testtechnieken.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )

@instructions_bp.route("/testen/module5")
@login_required
def testen_module5():
    module_slug = "testen_m5"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module5_exploratory_testing.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )

@instructions_bp.route("/testen/module6")
@login_required
def testen_module6():
    module_slug = "testen_m6"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module6_bugreporting.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )

@instructions_bp.route("/testen/module7")
@login_required
def testen_module7():
    module_slug = "testen_m7"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module7_api_testing.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )

@instructions_bp.route("/testen/module8")
@login_required
def testen_module8():
    module_slug = "testen_m8"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module8_automatisering_ai.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )

@instructions_bp.route("/testen/module9")
@login_required
def testen_module9():
    module_slug = "testen_m9"
    module = get_module(module_slug)
    if not module:
        abort(404)

    user_id = session["user_id"]

    progress = compute_progress(user_id, module_slug, module)
    answer_map = get_answer_map(user_id, module_slug)

    return render_template(
        "testen/module9_eindproject.html",
        module_slug=module_slug,
        questions=module["questions"],
        progress=progress,
        answer_map=answer_map,
    )



# ================================================================
#  Onderwerp B mapnaam – OVERVIEW 
# ================================================================

@instructions_bp.route("/git/overview")
def git_overview():
    steps = [
    {"nr": 1, "title": "Intro", "endpoint": "instructions.git_module1", "status": "done"},
    {"nr": 2, "title": "Basis", "endpoint": "instructions.git_module2", "status": "progress"},
    {"nr": 3, "title": "Samenwerken", "endpoint": "instructions.git_module3", "status": "not"},
    {"nr": 4, "title": "Titel module 4", "endpoint": "instructions.git_module4", "status": "not"},
    #{"nr": 5, "title": "Titel module 5", "endpoint": "instructions.mapnaam_module5", "status": "not"},
    #{"nr": 6, "title": "Titel module 6", "endpoint": "instructions.mapnaam_module6", "status": "not"},
    #{"nr": 7, "title": "Titel module 7", "endpoint": "instructions.mapnaam_module7", "status": "not"},
    #{"nr": 8, "title": "Titel module 8", "endpoint": "instructions.mapnaam_module8", "status": "not"},
    #{"nr": 9, "title": "Titel module 9", "endpoint": "instructions.mapnaam_module9", "status": "not"},
]

    return render_template("git/overview.html", steps=steps)


# ================================================================
#  Onderwerp B mapnaam – INDIVIDUELE MODULES
# ================================================================
@instructions_bp.route("/git/module1")
def git_module1():
    return render_template("git/module1_intro.html")


@instructions_bp.route("/git/module2")
def git_module2():
    return render_template("git/module2_basis.html")


@instructions_bp.route("/git/module3")
def git_module3():
    return render_template("git/module3_samenwerken.html")


@instructions_bp.route("/git/module4")
def git_module4():
    return render_template("git/module4_module4naam.html")

# ================================================================
#  Post om antwoorden te verzenden
# ================================================================

@instructions_bp.post("/testen/<module_slug>/<question_id>/answer")
@login_required
def testen_answer(module_slug, question_id):
    module = get_module(module_slug)
    if not module:
        abort(404)

    q = get_question(module_slug, question_id)
    if not q:
        abort(404)

    user_id = session["user_id"]
    user_answer = request.form.get("answer", "")

    is_correct = check_answer(q, user_answer)
    upsert_answer(user_id, module_slug, question_id, user_answer, is_correct)

    # Redirect terug naar de exactemodule en vraag (scroll-fix)
    
    module_to_endpoint = {
    "testen_m1": "instructions.testen_module1",
    "testen_m2": "instructions.testen_module2",
    "testen_m3": "instructions.testen_module3",
    "testen_m4": "instructions.testen_module4",
    "testen_m5": "instructions.testen_module5",
    "testen_m6": "instructions.testen_module6",
    "testen_m7": "instructions.testen_module7",
    "testen_m8": "instructions.testen_module8",
    "testen_m9": "instructions.testen_module9",
    }

    endpoint = module_to_endpoint.get(module_slug)
    if endpoint:
        return redirect(url_for(endpoint) + f"#q_{question_id}")

    return redirect(url_for("instructions.testen_overview"))


# ======================================================================================================
#  instructie om lessen in markdown en yaml format te lezen zodat lesinhoud op git geplaatst kan worden
# ======================================================================================================



@instructions_bp.route("/testen/content/<module_name>")
@login_required
def testen_content_module(module_name):
    lesson = load_lesson("softwaretesten", module_name)

    if not lesson:
        abort(404)

    html_content = markdown.markdown(
        lesson["content"],
        extensions=["extra"]
    )

    user_id = session["user_id"]
    answer_map = get_answer_map(user_id, lesson["module_slug"])

    return render_template(
        "testen/content_lesson.html",
        lesson=lesson,
        html_content=html_content,
        answer_map=answer_map
    )

    total_questions = len(lesson["questions"])

    correct_count = sum(
        1 for q in lesson["questions"]
        if answer_map.get(q["id"]) and answer_map[q["id"]].is_correct
    )
    return render_template(
        "testen/content_lesson.html",
        lesson=lesson,
        html_content=html_content,
        answer_map=answer_map,
        total_questions=total_questions,
        correct_count=correct_count
    )

# ======================================================================================================
#  instructie om overvieuw van de lessen te laden
# ======================================================================================================

@instructions_bp.route("/testen/content/overview")
@login_required
def testen_content_overview():
    modules = load_track_modules("softwaretesten")

    return render_template(
        "testen/content_overview.html",
        modules=modules
    )

# ======================================================================================================
#  instructie om lessen in markdown en yaml format de antwoorden te koppelen aan database
# ======================================================================================================


@instructions_bp.route("/submit-content-answer", methods=["POST"])
@login_required
def submit_content_answer():
    module_slug = request.form.get("module_slug")
    module_folder = request.form.get("module_folder")
    question_id = request.form.get("question_id")
    user_answer = request.form.get(question_id)

    track = request.form.get("track", "softwaretesten")
    lesson = load_lesson(track, module_folder)

    if not lesson:
        abort(404)

    question = next(
        (q for q in lesson["questions"] if q["id"] == question_id),
        None
    )

    if not question:
        abort(404)

    user_id = session["user_id"]

    route_map = {
        "softwaretesten": "instructions.testen_content_module",
        "git":            "instructions.git_content_module",
        "developer":      "instructions.developer_content_module",
    }
    endpoint = route_map.get(track, "instructions.testen_content_module")

    if question.get("type") == "open":
        upsert_answer(
            user_id=user_id,
            module_slug=module_slug,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=False
        )
        return redirect(
            url_for(endpoint, module_name=module_folder)
            + f"#{question_id}"
        )

    is_correct = check_answer(question, user_answer)
    upsert_answer(
        user_id=user_id,
        module_slug=module_slug,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct
    )
    return redirect(
        url_for(endpoint, module_name=module_folder)
        + f"#{question_id}"
    )

# ======================================================================================================
#  GIT — content routes (YAML + Markdown systeem)
# ======================================================================================================

@instructions_bp.route("/git/content/overview")
@login_required
def git_content_overview():
    modules = load_track_modules("git")
    return render_template(
        "git/content_overview.html",
        modules=modules
    )

@instructions_bp.route("/developer/content/overview")
@login_required
def developer_content_overview():
    modules = load_track_modules("developer")
    return render_template(
        "developer/content_overview.html",
        modules=modules
    )

@instructions_bp.route("/content-images/<track>/<module_name>/<filename>")
def content_image(track, module_name, filename):
    image_dir = os.path.join(
        current_app.root_path, "content", track, module_name, "images"
    )
    return send_from_directory(image_dir, filename)


@instructions_bp.route("/git/content/<module_name>")
@login_required
def git_content_module(module_name):
    lesson = load_lesson("git", module_name)

    if not lesson:
        abort(404)

    html_content = markdown.markdown(
        lesson["content"],
        extensions=["extra"]
    )

    user_id = session["user_id"]
    answer_map = get_answer_map(user_id, lesson["module_slug"])

    total_questions = len(lesson["questions"])
    correct_count = sum(
        1 for q in lesson["questions"]
        if answer_map.get(q["id"]) and answer_map[q["id"]].is_correct
    )

    return render_template(
        "git/content_lesson.html",
        lesson=lesson,
        html_content=html_content,
        answer_map=answer_map
    )


@instructions_bp.route("/submit-git-answer", methods=["POST"])
@login_required
def submit_git_answer():
    module_slug = request.form.get("module_slug")
    module_folder = request.form.get("module_folder")
    question_id = request.form.get("question_id")
    user_answer = request.form.get(question_id)

    lesson = load_lesson("git", module_folder)

    if not lesson:
        abort(404)

    question = next(
        (q for q in lesson["questions"] if q["id"] == question_id),
        None
    )

    if not question:
        abort(404)

    user_id = session["user_id"]

    if question.get("type") == "open":
        upsert_answer(
            user_id=user_id,
            module_slug=module_slug,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=False
        )
        return redirect(
            url_for("instructions.git_content_module", module_name=module_folder)
            + f"#{question_id}"
        )

    is_correct = check_answer(question, user_answer)
    upsert_answer(
        user_id=user_id,
        module_slug=module_slug,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct
    )

    return redirect(
        url_for("instructions.git_content_module", module_name=module_folder)
        + f"#{question_id}"
    )
