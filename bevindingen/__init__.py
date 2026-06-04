from flask import Blueprint

bevindingen_bp = Blueprint(
    "bevindingen",
    __name__,
    template_folder="templates",
)

from . import routes  # noqa
