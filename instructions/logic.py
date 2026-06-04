# instructions/logic.py

from .question_bank_testen import TESTEN_QUESTION_BANK
from core.question_engine import get_question as _get_question


def get_module(module_slug: str):
    return TESTEN_QUESTION_BANK.get(module_slug)


def get_question(module_slug: str, question_id: str):
    module = get_module(module_slug)
    if not module:
        return None
    return _get_question(module, question_id)