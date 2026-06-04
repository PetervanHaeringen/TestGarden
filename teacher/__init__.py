from flask import Blueprint

teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher",
    template_folder="templates"
)

from . import routes