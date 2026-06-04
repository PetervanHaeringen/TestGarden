from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
TRACKS_DIR = BASE_DIR / "tracks"


def load_track(track_id):
    path = TRACKS_DIR / f"{track_id}.yaml"

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_all_tracks():
    tracks = []

    if not TRACKS_DIR.exists():
        return tracks

    for path in TRACKS_DIR.glob("*.yaml"):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            tracks.append(data)

    return sorted(tracks, key=lambda t: t.get("title", ""))