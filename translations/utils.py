import json
from pathlib import Path

from flask import session


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_LANGUAGE = "nl"
SUPPORTED_LANGUAGES = {"nl", "en", "zh", "es", "ar", "ru"}

_translation_cache = {}


def load_translations(lang: str) -> dict:
    lang = lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE

    if lang in _translation_cache:
        return _translation_cache[lang]

    file_path = BASE_DIR / f"{lang}.json"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    _translation_cache[lang] = data
    return data


def clear_translation_cache():
    _translation_cache.clear()


def get_current_language() -> str:
    lang = session.get("lang", DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        return DEFAULT_LANGUAGE
    return lang


def extract_text(value):
    if isinstance(value, dict):
        return value.get("text", "")
    if isinstance(value, str):
        return value
    return ""


def t(key: str) -> str:
    lang = get_current_language()

    current_translations = load_translations(lang)
    if key in current_translations:
        return extract_text(current_translations[key])

    fallback_translations = load_translations(DEFAULT_LANGUAGE)
    if key in fallback_translations:
        return extract_text(fallback_translations[key])

    return key