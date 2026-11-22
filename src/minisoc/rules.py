"""Règle de détection : un même compte connecté depuis deux IP en moins d'une minute."""

import json
from datetime import datetime, timedelta

from generator import OUTPUT_FILE

MAX_GAP = timedelta(seconds=60)


def load_events():
    """Lit le fichier JSON Lines et renvoie la liste des événements."""
    events = []
    with OUTPUT_FILE.open(encoding="utf-8") as file:
        for line in file:
            events.append(json.loads(line))
    return events


def is_too_close(previous, current):
    """Vrai si les deux connexions sont séparées de moins de MAX_GAP."""
    start = datetime.fromisoformat(previous["timestamp"])
    end = datetime.fromisoformat(current["timestamp"])
    return end - start < MAX_GAP


def is_different_ip(previous, current):
    """Vrai si les deux connexions viennent de deux IP différentes."""
    return previous["source_ip"] != current["source_ip"]


def main():
    last_login = {}
    for current in load_events():
        if current["event"] != "login_success":
            continue
        previous = last_login.get(current["username"])
        if previous and is_too_close(previous, current) and is_different_ip(previous, current):
            print(
                f"ALERTE : {current['username']} connecté depuis {previous['source_ip']} "
                f"à {previous['timestamp']}, puis depuis {current['source_ip']} à {current['timestamp']}"
            )
        last_login[current["username"]] = current


if __name__ == "__main__":
    main()