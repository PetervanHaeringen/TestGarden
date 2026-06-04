from translations.utils import get_current_language
from .http_status_data import STATUS_CODES, STATUS_CODE_GROUPS


def get_localized_value(value, lang, fallback="nl"):
    if isinstance(value, dict):
        return value.get(lang) or value.get(fallback) or ""
    return value


def get_status_code_info(code: str):
    code = (code or "").strip()

    if not code:
        return None

    lang = get_current_language()

    code_info = STATUS_CODES.get(code)
    if not code_info:
        return {
            "found": False,
            "code": code,
            "message": "Onbekende statuscode." if lang == "nl" else "Unknown status code.",
        }

    group_key = code_info["group"]
    group_info = STATUS_CODE_GROUPS.get(group_key, {})

    testing_tips = get_localized_value(code_info.get("testing_tips", []), lang)
    if not isinstance(testing_tips, list):
        testing_tips = []

    return {
        "found": True,
        "code": code,
        "title": get_localized_value(code_info.get("title", ""), lang),
        "meaning": get_localized_value(code_info.get("meaning", ""), lang),
        "group": group_key,
        "group_title": get_localized_value(group_info.get("title", ""), lang),
        "group_description": get_localized_value(group_info.get("description", ""), lang),
        "google_note": get_localized_value(group_info.get("google_note", ""), lang),
        "testing_tips": testing_tips,
    }