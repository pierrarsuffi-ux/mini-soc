"""Générateur de logs de connexion synthétiques pour le projet Mini-SOC."""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# --- Paramètres ---
USERS = {
    "alice": "10.0.0.11",
    "bob": "10.0.0.12",
    "chloe": "10.0.0.13",
    "david": "10.0.0.14",
    "emma": "10.0.0.15",
}
ATTACKER_IPS = ["203.0.113.7", "203.0.113.42", "198.51.100.23"]
BRUTE_FORCE_USERNAMES = ["root", "admin", "test", "oracle"]
START_TIME = datetime(2026, 11, 1, 8, 0, 0)
NB_EVENTS = 200
NB_BRUTE_FORCE = 3
NB_SUSPICIOUS_LOGINS = 5
OUTPUT_FILE = Path("data/raw/auth_logs.jsonl")


def make_event(moment, username, source_ip, event, label):
    """Construit un événement au format commun à tous les logs."""
    return {
        "timestamp": moment.isoformat(timespec="seconds"),
        "service": "ssh",
        "username": username,
        "source_ip": source_ip,
        "event": event,
        "label": label,
    }


def generate_normal_login(moment):
    """Crée un événement de connexion ordinaire."""
    username = random.choice(list(USERS))
    success = random.random() < 0.95
    event = "login_success" if success else "login_failed"
    return make_event(moment, username, USERS[username], event, "normal")


def generate_brute_force(start):
    """Simule une force brute : beaucoup d'échecs, très vite, depuis une même IP."""
    attacker_ip = random.choice(ATTACKER_IPS)
    events = []
    moment = start
    for _ in range(random.randint(30, 60)):
        moment += timedelta(seconds=random.randint(1, 3))
        username = random.choice(BRUTE_FORCE_USERNAMES)
        events.append(make_event(moment, username, attacker_ip, "login_failed", "brute_force"))
    return events


def generate_suspicious_login(moment):
    """Simule un compte volé : connexion réussie depuis une IP inconnue."""
    username = random.choice(list(USERS))
    attacker_ip = random.choice(ATTACKER_IPS)
    return make_event(moment, username, attacker_ip, "login_success", "suspicious_login")


def random_moment(start, end):
    """Renvoie un instant tiré au hasard entre start et end."""
    return start + (end - start) * random.random()


def main():
    random.seed(31)

    # 1. Le trafic normal
    events = []
    moment = START_TIME
    for _ in range(NB_EVENTS):
        moment += timedelta(seconds=random.randint(30, 600))
        events.append(generate_normal_login(moment))
    end_time = moment

    # 2. Les attaques, placées à des moments aléatoires
    for _ in range(NB_BRUTE_FORCE):
        events.extend(generate_brute_force(random_moment(START_TIME, end_time)))

    for _ in range(NB_SUSPICIOUS_LOGINS):
        events.append(generate_suspicious_login(random_moment(START_TIME, end_time)))

    # 3. On remet tout dans l'ordre chronologique
    events.sort(key=lambda event: event["timestamp"])

    # 4. On écrit le fichier
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")

    print(f"{len(events)} événements écrits dans {OUTPUT_FILE}")


if __name__ == "__main__":
    main()