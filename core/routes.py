from flask import render_template, session, redirect, request, url_for
from . import core_bp
from translations.utils import SUPPORTED_LANGUAGES


@core_bp.route("/set-language/<lang>")
def set_language(lang):
    if lang in SUPPORTED_LANGUAGES:
        session["lang"] = lang

    next_url = request.args.get("next")
    if next_url:
        return redirect(next_url)

    return redirect(url_for("core.index"))


@core_bp.route("/")
def index():
    return render_template("index.html")



@core_bp.route("/about")
def about():
    return render_template("about.html")


