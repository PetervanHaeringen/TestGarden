from flask import Blueprint

testronden_bp = Blueprint(
    'testronden',
    __name__,
    template_folder='templates',
)

from . import routes  # noqa
