# =============================================================================
# core/content_loader.py — Laadt lesinhoud vanuit het content-systeem
# =============================================================================
# Dit bestand leest modules op uit de lokale content-map (of straks GitHub).
# Elke module bestaat uit drie bestanden:
#   - meta.yaml      : metadata (id, titel, volgorde, level, etc.)
#   - lesson.md      : de lesinhoud in Markdown
#   - questions.yaml : de vragen bij de les
#
# De canonieke sleutel voor een module is altijd het "id" veld uit meta.yaml,
# bijvoorbeeld "softwaretesten.m01". Dit id bevat de track-naam en is globaal
# uniek — ook als er meerdere tracks naast elkaar bestaan.
#
# legacy_slug wordt alleen nog gebruikt als nooduitgang voor oude yaml-bestanden
# die nog geen "id" veld hebben. Zodra alle modules een id hebben kan
# legacy_slug verwijderd worden.
# =============================================================================

from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"


def _resolve_slug(meta, fallback):
    """
    Bepaalt de canonieke slug voor een module.
    Volgorde van prioriteit:
      1. id           → "softwaretesten.m01"  (de juiste keuze)
      2. legacy_slug  → "testen_m1"           (nooduitgang voor oude yaml)
      3. fallback     → mapnaam               (laatste redmiddel)
    """
    return meta.get("id") or meta.get("legacy_slug") or fallback


def load_lesson(track, module):
    """
    Laadt één module volledig: metadata, lesinhoud en vragen.
    Geeft None terug als meta.yaml of lesson.md ontbreekt.
    """
    module_dir = CONTENT_DIR / track / module

    meta_path = module_dir / "meta.yaml"
    lesson_path = module_dir / "lesson.md"
    questions_path = module_dir / "questions.yaml"

    if not meta_path.exists() or not lesson_path.exists():
        return None

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)

    with open(lesson_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    questions = []
    if questions_path.exists():
        with open(questions_path, "r", encoding="utf-8") as f:
            question_data = yaml.safe_load(f) or {}
            questions = question_data.get("questions", [])

    module_slug = _resolve_slug(meta, module)

    return {
        "meta": meta,
        "content": markdown_content,
        "questions": questions,
        "module_slug": module_slug,
    }


def load_track_modules(track):
    """
    Laadt een overzicht van alle modules in een track.
    Sorteert op het "order" veld uit meta.yaml.
    Modules zonder meta.yaml worden overgeslagen.
    """
    track_dir = CONTENT_DIR / track

    if not track_dir.exists():
        return []

    modules = []

    for module_dir in track_dir.iterdir():
        if not module_dir.is_dir():
            continue

        meta_path = module_dir / "meta.yaml"

        if not meta_path.exists():
            continue

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f) or {}

        module_slug = _resolve_slug(meta, module_dir.name)

        modules.append({
            "folder": module_dir.name,
            "id": meta.get("id"),
            "module_slug": module_slug,
            "title": meta.get("title", module_dir.name),
            "order": meta.get("order", 999),
            "level": meta.get("level", ""),
            "status": meta.get("status", "active"),
        })

    return sorted(modules, key=lambda m: m["order"])
