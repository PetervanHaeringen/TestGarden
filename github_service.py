"""
github_service.py
Alle communicatie met de GitHub API zit hier.
TestGarden leest YAML-bestanden en schrijft commits via deze laag.
"""

import os
import re
import base64
import yaml
import requests
import time
from functools import lru_cache

# ── Configuratie (via omgevingsvariabelen op PythonAnywhere) ──────────────────
GITHUB_TOKEN  = os.environ.get('GITHUB_TOKEN')       # Personal Access Token
GITHUB_OWNER  = os.environ.get('GITHUB_OWNER')       # bijv. "GitAI47"
GITHUB_REPO   = os.environ.get('GITHUB_REPO')        # bijv. "testscripts"
GITHUB_BRANCH = os.environ.get('GITHUB_BRANCH', 'main')

BASE_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
# sluit de mappen bevindingen en screenshots uit van het inlezen in scripts
UITGESLOTEN_MAPPEN = {'bevindingen', 'screenshots'}

def _headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


# ── Lezen ─────────────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _haal_tree() -> tuple:
    """
    Haal de volledige repository tree op — eenmalig gecached per worker-proces.
    tuple ipv list zodat lru_cache het resultaat kan opslaan (lists zijn niet hashable).
    """
    r = requests.get(
        f"{BASE_URL}/git/trees/{GITHUB_BRANCH}",
        headers=_headers(),
        params={"recursive": "1"},
    )
    r.raise_for_status()
    return tuple(r.json().get("tree", []))


def _wis_tree_cache():
    """Leeg de tree-cache — aanroepen na een commit zodat de volgende lezing vers is."""
    _haal_tree.cache_clear()


def haal_mappen() -> list[str]:
    """Geef alle mappen (module-groepen) in de repository terug."""
    tree = _haal_tree()
    return sorted({
        item["path"].split("/")[0]
        for item in tree
        if item["type"] == "blob"
        and item["path"].endswith(".yaml")
        and "/" in item["path"]
        and item["path"].split("/")[0] not in UITGESLOTEN_MAPPEN
    })


def haal_bestanden(map_naam: str) -> list[str]:
    """Geef alle YAML-bestanden in een map terug."""
    tree = _haal_tree()
    return sorted([
        item["path"].split("/")[1]
        for item in tree
        if item["type"] == "blob"
        and item["path"].startswith(f"{map_naam}/")
        and item["path"].endswith(".yaml")
    ])


# ── Tijdgebonden bestandscache (5 minuten) ───────────────────────────────────
_CACHE_TTL = 300  # seconden — pas aan indien nodig
_bestand_cache: dict = {}  # {pad: (data, sha, timestamp)}


def _laad_bestand_cached(pad: str) -> tuple:
    """
    Laad een bestand uit GitHub met tijdgebonden cache.
    Na 5 minuten wordt het bestand opnieuw opgehaald.
    """
    nu = time.time()
    if pad in _bestand_cache:
        data, sha, ts = _bestand_cache[pad]
        if nu - ts < _CACHE_TTL:
            return data, sha  # Cache nog geldig

    # Cache verlopen of leeg — ophalen bij GitHub
    r = requests.get(
        f"{BASE_URL}/contents/{pad}",
        headers=_headers(),
        params={"ref": GITHUB_BRANCH},
    )
    r.raise_for_status()
    resp = r.json()
    inhoud = base64.b64decode(resp["content"]).decode("utf-8")
    data = yaml.safe_load(inhoud) or {}
    sha = resp["sha"]
    _bestand_cache[pad] = (data, sha, nu)
    return data, sha


def laad_bestand(map_naam: str, bestand: str) -> tuple[dict, str]:
    """
    Laad een YAML-bestand vanuit GitHub.
    Resultaat wordt 5 minuten gecached — daarna automatisch ververst.
    """
    pad = f"{map_naam}/{bestand}"
    return _laad_bestand_cached(pad)


def _wis_bestand_cache(map_naam: str = None, bestand: str = None):
    """Wis de bestandscache — volledig of één bestand."""
    if map_naam and bestand:
        pad = f"{map_naam}/{bestand}"
        _bestand_cache.pop(pad, None)
    else:
        _bestand_cache.clear()


# ── Schrijven ─────────────────────────────────────────────────────────────────

def sla_bestand_op(
    map_naam: str,
    bestand: str,
    data: dict,
    sha: str,
    tester_naam: str,
    ts_id: str = "",
) -> bool:
    """
    Schrijf gewijzigd YAML terug naar GitHub als een commit.
    De tester_naam verschijnt in het commit-bericht.
    Geeft True terug bij succes.
    """
    pad = f"{map_naam}/{bestand}"
    inhoud = yaml.dump(
        data,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )
    inhoud_b64 = base64.b64encode(inhoud.encode("utf-8")).decode("utf-8")

    onderwerp = f"{ts_id} " if ts_id else ""
    bericht = f"testresultaat: {onderwerp}bijgewerkt door {tester_naam}"

    payload = {
        "message": bericht,
        "content": inhoud_b64,
        "sha": sha,
        "branch": GITHUB_BRANCH,
        "committer": {
            "name": f"TestGarden ({tester_naam})",
            "email": "testgarden@noreply.local",
        },
    }

    r = requests.put(
        f"{BASE_URL}/contents/{pad}",
        headers=_headers(),
        json=payload,
    )
    succes = r.status_code in (200, 201)
    if succes:
        _wis_tree_cache()
        _bestand_cache.clear()  # Bestand cache wissen na commit
    return succes


# ── Status hulpfuncties ────────────────────────────────────────────────────────

def bereken_tellers(data: dict) -> dict:
    t = {"goed": 0, "fout": 0, "goed_met_opmerking": 0, "niet_getest": 0}
    for ts in data.get("testsets", []):
        for stap in ts.get("stappen", []):
            s = stap.get("status") or "niet_getest"
            t[s] = t.get(s, 0) + 1
    return t


# ── Bevindingen ────────────────────────────────────────────────────────────────

def volgend_bevinding_id() -> str:
    """
    Bepaal het volgende BEV-nummer op basis van wat er al in bevindingen/ staat.
    Geeft bijv. 'BEV-007' terug.
    """
    try:
        r = requests.get(
            f"{BASE_URL}/git/trees/{GITHUB_BRANCH}",
            headers=_headers(),
            params={"recursive": "1"},
        )
        r.raise_for_status()
        tree = r.json().get("tree", [])
        nummers = []
        for item in tree:
            pad = item.get("path", "")
            if pad.startswith("bevindingen/BEV-") and pad.endswith(".yaml"):
                try:
                    nr = int(pad.replace("bevindingen/BEV-", "").replace(".yaml", ""))
                    nummers.append(nr)
                except ValueError:
                    pass
        volgend = max(nummers) + 1 if nummers else 1
        return f"BEV-{volgend:03d}"
    except Exception:
        # Fallback op timestamp als de API niet bereikbaar is
        from datetime import datetime
        return f"BEV-{datetime.now().strftime('%H%M%S')}"


def sla_bevinding_op(bevinding: dict, tester_naam: str) -> bool:
    """
    Schrijf een nieuwe bevinding als YAML naar bevindingen/<id>.yaml
    """
    bev_id = bevinding["id"]
    pad = f"bevindingen/{bev_id}.yaml"
    inhoud = yaml.dump(
        bevinding,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )
    inhoud_b64 = base64.b64encode(inhoud.encode("utf-8")).decode("utf-8")

    payload = {
        "message": f"bevinding: {bev_id} aangemaakt door {tester_naam}",
        "content": inhoud_b64,
        "branch": GITHUB_BRANCH,
        "committer": {
            "name": f"TestGarden ({tester_naam})",
            "email": "testgarden@noreply.local",
        },
    }
    r = requests.put(
        f"{BASE_URL}/contents/{pad}",
        headers=_headers(),
        json=payload,
    )
    return r.status_code in (200, 201)


def upload_screenshot(
    bev_id: str,
    bestandsnaam: str,
    data_bytes: bytes,
    tester_naam: str,
) -> str | None:
    """
    Upload een screenshot naar screenshots/<bev_id>_<bestandsnaam>.
    Geeft het opgeslagen pad terug, of None bij mislukking.
    """
    # Schone bestandsnaam: spaties en rare tekens weg
    import re
    schone_naam = re.sub(r'[^\w.\-]', '_', bestandsnaam)
    pad = f"screenshots/{bev_id}_{schone_naam}"
    inhoud_b64 = base64.b64encode(data_bytes).decode("utf-8")

    payload = {
        "message": f"screenshot: {pad} bij {bev_id}",
        "content": inhoud_b64,
        "branch": GITHUB_BRANCH,
        "committer": {
            "name": f"TestGarden ({tester_naam})",
            "email": "testgarden@noreply.local",
        },
    }
    r = requests.put(
        f"{BASE_URL}/contents/{pad}",
        headers=_headers(),
        json=payload,
    )
    return pad if r.status_code in (200, 201) else None


def koppel_bevinding_aan_stap(
    map_naam: str,
    bestand: str,
    ts_id: str,
    stap_nr: int,
    bev_id: str,
    tester_naam: str,
) -> bool:
    """
    Voeg het bevinding-ID toe aan de betreffende stap in het testscript.
    """
    data, sha = laad_bestand(map_naam, bestand)
    for ts in data.get("testsets", []):
        if ts["id"] == ts_id:
            for stap in ts.get("stappen", []):
                if stap.get("nr") == stap_nr:
                    bestaand = stap.get("bevindingen", [])
                    if bev_id not in bestaand:
                        bestaand.append(bev_id)
                    stap["bevindingen"] = bestaand
                    break
    return sla_bestand_op(map_naam, bestand, data, sha, tester_naam, ts_id)


def haal_alle_bevindingen() -> list[dict]:
    """
    Laad alle bevindingen uit bevindingen/ gesorteerd op ID.
    """
    try:
        r = requests.get(
            f"{BASE_URL}/git/trees/{GITHUB_BRANCH}",
            headers=_headers(),
            params={"recursive": "1"},
        )
        r.raise_for_status()
        tree = r.json().get("tree", [])
        paden = sorted([
            item["path"] for item in tree
            if item["path"].startswith("bevindingen/BEV-")
            and item["path"].endswith(".yaml")
        ])
        resultaat = []
        for pad in paden:
            delen = pad.split("/")
            if len(delen) == 2:
                try:
                    data, _ = laad_bestand("bevindingen", delen[1])
                    resultaat.append(data)
                except Exception:
                    pass
        return resultaat
    except Exception:
        return []


def screenshot_url(pad: str) -> str:
    """
    Geef de Flask proxy-URL terug voor een screenshot.
    Werkt ook voor private repositories — authenticatie via de app.
    """
    from flask import url_for
    bestandsnaam = pad.split("/")[-1]
    return url_for("bevindingen.screenshot_proxy", bestandsnaam=bestandsnaam)

def haal_screenshot_bytes(bestandsnaam: str) -> bytes | None:
    """
    Haal de ruwe bytes van een screenshot op via de GitHub API.
    Werkt ook voor private repositories.
    """
    pad = f"screenshots/{bestandsnaam}"
    r = requests.get(
        f"{BASE_URL}/contents/{pad}",
        headers=_headers(),
        params={"ref": GITHUB_BRANCH},
    )
    if r.status_code != 200:
        return None
    inhoud_b64 = r.json().get("content", "").replace("\n", "")
    return base64.b64decode(inhoud_b64)


# ── Testronden ────────────────────────────────────────────────────────────────

UITGESLOTEN_MAPPEN = {'bevindingen', 'screenshots', 'testronden'}


def haal_mappen() -> list:
    """Geef alle TC-mappen terug (tc_01..tc_15), gesorteerd op nummer."""
    tree = _haal_tree()
    mappen = sorted({
        item["path"].split("/")[0]
        for item in tree
        if item["type"] == "blob"
        and item["path"].endswith(".yaml")
        and "/" in item["path"]
        and item["path"].split("/")[0] not in UITGESLOTEN_MAPPEN
    })
    # Sorteer op TC-nummer (tc_01, tc_02, ... tc_15)
    import re
    def tc_sort(m):
        match = re.search(r'(\d+)', m)
        return int(match.group(1)) if match else 999
    return sorted(mappen, key=tc_sort)


def haal_tc_label(map_naam: str) -> str:
    """
    Geef een leesbaar label voor een TC-map.
    Laadt de module-naam uit het YAML-bestand.
    """
    match = re.search(r'(\d+)', map_naam)
    nr = int(match.group(1)) if match else 0
    try:
        bestanden = haal_bestanden(map_naam)
        if bestanden:
            data, _ = laad_bestand(map_naam, bestanden[0])
            naam = data.get('module', map_naam)
            return f"TC_{nr:02d} — {naam}"
    except Exception:
        pass
    return f"TC_{nr:02d}"


def haal_alle_testronden() -> list:
    """Geef alle testronden terug gesorteerd op ID (nieuwste eerst)."""
    try:
        r = requests.get(
            f"{BASE_URL}/git/trees/{GITHUB_BRANCH}",
            headers=_headers(),
            params={"recursive": "1"},
        )
        r.raise_for_status()
        tree = r.json().get("tree", [])
        ronde_ids = sorted({
            item["path"].split("/")[1]
            for item in tree
            if item["path"].startswith("testronden/")
            and len(item["path"].split("/")) >= 3
        }, reverse=True)
        resultaat = []
        for ronde_id in ronde_ids:
            try:
                meta, _ = laad_bestand(f"testronden/{ronde_id}", "meta.yaml")
                resultaat.append(meta)
            except Exception:
                pass
        return resultaat
    except Exception:
        return []


def haal_testronde(ronde_id: str) -> tuple:
    """Laad de meta van één testronde. Geeft (data, sha)."""
    return laad_bestand(f"testronden/{ronde_id}", "meta.yaml")


def maak_testronde_aan(ronde_id: str, meta: dict, tester_naam: str) -> bool:
    """Maak een nieuwe testronde aan door meta.yaml te schrijven."""
    pad = f"testronden/{ronde_id}/meta.yaml"
    inhoud = yaml.dump(meta, allow_unicode=True, default_flow_style=False,
                       sort_keys=False, width=120)
    inhoud_b64 = base64.b64encode(inhoud.encode("utf-8")).decode("utf-8")
    payload = {
        "message": f"testronde: {ronde_id} aangemaakt door {tester_naam}",
        "content": inhoud_b64,
        "branch": GITHUB_BRANCH,
        "committer": {
            "name": f"TestGarden ({tester_naam})",
            "email": "testgarden@noreply.local",
        },
    }
    r = requests.put(f"{BASE_URL}/contents/{pad}",
                     headers=_headers(), json=payload)
    succes = r.status_code in (200, 201)
    if succes:
        _wis_tree_cache()
    return succes


def update_testronde_meta(ronde_id: str, meta: dict, sha: str,
                          tester_naam: str) -> bool:
    """Schrijf gewijzigde meta terug (bijv. module claimen of afsluiten)."""
    pad = f"testronden/{ronde_id}/meta.yaml"
    inhoud = yaml.dump(meta, allow_unicode=True, default_flow_style=False,
                       sort_keys=False, width=120)
    inhoud_b64 = base64.b64encode(inhoud.encode("utf-8")).decode("utf-8")
    payload = {
        "message": f"testronde: {ronde_id} bijgewerkt door {tester_naam}",
        "content": inhoud_b64,
        "sha": sha,
        "branch": GITHUB_BRANCH,
        "committer": {
            "name": f"TestGarden ({tester_naam})",
            "email": "testgarden@noreply.local",
        },
    }
    r = requests.put(f"{BASE_URL}/contents/{pad}",
                     headers=_headers(), json=payload)
    succes = r.status_code in (200, 201)
    if succes:
        _wis_tree_cache()
    return succes


def volgend_ronde_id() -> str:
    """Geef het volgende TR-nummer terug, bijv. TR-003."""
    try:
        rondes = haal_alle_testronden()
        nummers = []
        for r in rondes:
            try:
                nr = int(r.get("id", "TR-000").replace("TR-", ""))
                nummers.append(nr)
            except ValueError:
                pass
        volgend = max(nummers) + 1 if nummers else 1
        return f"TR-{volgend:03d}"
    except Exception:
        from datetime import datetime
        return f"TR-{datetime.now().strftime('%H%M%S')}"


def laad_resultaten(ronde_id: str, map_naam: str, bestand: str) -> tuple:
    """
    Laad het resultatenbestand voor een specifieke module in een testronde.
    Geeft (data, sha) — data is {} als het bestand nog niet bestaat.
    """
    pad = f"testronden/{ronde_id}/{map_naam}/{bestand}"
    r = requests.get(
        f"{BASE_URL}/contents/{pad}",
        headers=_headers(),
        params={"ref": GITHUB_BRANCH},
    )
    if r.status_code == 404:
        return {}, None
    r.raise_for_status()
    resp = r.json()
    inhoud = base64.b64decode(resp["content"]).decode("utf-8")
    data = yaml.safe_load(inhoud) or {}
    return data, resp["sha"]


def sla_resultaten_op(ronde_id: str, map_naam: str, bestand: str,
                      data: dict, sha, tester_naam: str,
                      ts_id: str = "") -> bool:
    """
    Sla testresultaten op in testronden/<ronde_id>/<map>/<bestand>.
    Het testscript zelf blijft ongewijzigd.
    """
    pad = f"testronden/{ronde_id}/{map_naam}/{bestand}"
    inhoud = yaml.dump(data, allow_unicode=True, default_flow_style=False,
                       sort_keys=False, width=120)
    inhoud_b64 = base64.b64encode(inhoud.encode("utf-8")).decode("utf-8")
    onderwerp = f"{ts_id} " if ts_id else ""
    bericht = f"resultaat: {ronde_id} {onderwerp}door {tester_naam}"
    payload = {
        "message": bericht,
        "content": inhoud_b64,
        "branch": GITHUB_BRANCH,
        "committer": {
            "name": f"TestGarden ({tester_naam})",
            "email": "testgarden@noreply.local",
        },
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(f"{BASE_URL}/contents/{pad}",
                     headers=_headers(), json=payload)
    succes = r.status_code in (200, 201)
    if succes:
        _wis_tree_cache()
    return succes


def bereken_tellers_resultaten(scriptdata: dict, resultaten: dict) -> dict:
    """
    Bereken tellers op basis van scriptstructuur + aparte resultaten.
    """
    t = {"goed": 0, "fout": 0, "goed_met_opmerking": 0, "niet_getest": 0}
    res_per_ts = {ts.get("id"): ts for ts in resultaten.get("testsets", [])}
    for ts in scriptdata.get("testsets", []):
        ts_id = ts["id"]
        res_ts = res_per_ts.get(ts_id, {})
        res_stappen = {s.get("nr"): s for s in res_ts.get("stappen", [])}
        for stap in ts.get("stappen", []):
            nr = stap.get("nr")
            res = res_stappen.get(nr, {})
            s = res.get("status") or "niet_getest"
            t[s] = t.get(s, 0) + 1
    return t
