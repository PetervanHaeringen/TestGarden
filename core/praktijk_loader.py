# =============================================================================
# core/praktijk_loader.py — Laadt praktijkopdrachten en berekent competentiedekking
# =============================================================================
# Dit bestand leest de YAML-bestanden met praktijkopdrachten (bijv.
# servicedesk_tickets.yaml) en berekent op basis van voldane opdrachten
# welke competenties (gedragingen en vaardigheden) aangetoond zijn.
#
# De koppeling opdracht → competenties staat bewust NIET in de database
# maar in YAML-bestanden. Zo kan Sander of Peter de koppeling aanpassen
# zonder dat er een database-migratie nodig is.
#
# Gebruik:
#   from core.praktijk_loader import laad_opdrachten, bereken_dekking
#
#   opdrachten = laad_opdrachten("servicedesk")
#   dekking    = bereken_dekking("servicedesk", voldane_opdracht_ids)
# =============================================================================

from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
PRAKTIJK_DIR = BASE_DIR / "content" / "praktijk"


def laad_opdrachten(leerpad):
    """
    Laadt alle opdrachten voor een leerpad uit het bijbehorende YAML-bestand.
    Geeft een lijst van opdrachten terug, elk als dict.
    Geeft een lege lijst terug als het bestand niet bestaat.
    """
    yaml_pad = PRAKTIJK_DIR / f"{leerpad}_tickets.yaml"

    if not yaml_pad.exists():
        return []

    with open(yaml_pad, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("tickets", [])


def bereken_dekking(leerpad, voldane_ids):
    """
    Berekent welke gedragingen en vaardigheden aangetoond zijn,
    op basis van de voldane opdrachten en de YAML-koppeling.

    voldane_ids: set van opdracht_id strings die als voldaan zijn gemarkeerd
                 bijv. {"servicedesk.basis.t01", "servicedesk.basis.t03"}

    Geeft een dict terug, gestructureerd per werkproces:
    {
        "B1-K2-W1": {
            "gedragingen": {"omschrijving van gedraging", ...},
            "vaardigheden": {"omschrijving van vaardigheid", ...},
        },
        ...
    }
    """
    opdrachten = laad_opdrachten(leerpad)
    dekking = {}

    for opdracht in opdrachten:
        if opdracht["ticket_id"] not in voldane_ids:
            continue

        for wp in opdracht.get("werkprocessen", []):
            code = wp["code"]
            if code not in dekking:
                dekking[code] = {"gedragingen": set(), "vaardigheden": set()}

            for g in wp.get("gedragingen", []):
                dekking[code]["gedragingen"].add(g)
            for v in wp.get("vaardigheden", []):
                dekking[code]["vaardigheden"].add(v)

    return dekking


def alle_werkprocessen(leerpad):
    """
    Geeft een gesorteerde lijst van alle werkprocescodes die voorkomen
    in de opdrachten van dit leerpad. Gebruikt voor het opbouwen van
    het beoordelingsformulier.
    """
    opdrachten = laad_opdrachten(leerpad)
    codes = set()

    for opdracht in opdrachten:
        for wp in opdracht.get("werkprocessen", []):
            codes.add(wp["code"])

    return sorted(codes)
