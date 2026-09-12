import json
from pathlib import Path


LOG_FILE = Path("logs/security_events.json")


def log_security_event(event):
    LOG_FILE.parent.mkdir(exist_ok=True)

    events = []

    if LOG_FILE.exists():
        try:
            with LOG_FILE.open("r") as file:
                events = json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            events = []

    events.append(event)

    with LOG_FILE.open("w") as file:
        json.dump(events, file, indent=4)


def get_security_events():
    if not LOG_FILE.exists():
        return []

    try:
        with LOG_FILE.open("r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


if __name__ == "__main__":
    print("[*] Event logger module works")
