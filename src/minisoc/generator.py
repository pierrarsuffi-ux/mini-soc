"""Générateur de logs de connexion synthétiques pour le projet Mini-SOC."""
import json 
import random
from datetime import datetime, timedelta 
from pathlib import Path 
#---Paramètres---
USERS = {
    "alice": "10.0.0.11",
    "bob": "10.0.0.12",
    "chloe": "10.0.0.13",
    "david": "10.0.0.14",
    "emma": "10.0.0.15",
}
START_TIME = datetime(2026, 11, 1, 8, 0, 0)
NB_EVENTS = 200
OUTPUT_FILE = Path("data/raw/auth_logs.jsonl")
def generate_normal_login(moment):
    """créé un événement de connexon ordinaire"""
    username = random.choice(list(USERS))
    success = random.random() < 0.95  
    return {
        "timestamp": moment.isoformat(), 
        "service": "ssh",
        "username": username, 
        "source_ip": USERS[username], 
        "event": "login_success" if success else "login_failed",
    }
def main():
    random.seed(31)
    events = []
    moment = START_TIME
    for _ in range(NB_EVENTS):
        moment+= timedelta(seconds=random.randint(30, 600))
        events.append(generate_normal_login(moment))
    OUTPUT_FILE.parent.mkdir(parents = True,exist_ok = True)
    with OUTPUT_FILE.open("w", encoding = "utf-8") as file :
     for event in events :
      file.write(json.dumps(event) + "\n")
    print(f"{len(events)} événements écrits dans {OUTPUT_FILE}")
if __name__ == "__main__" :
   main()