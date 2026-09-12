from datetime import datetime, timedelta
import json
from pathlib import Path
from attack_narrator import generate_attack_narrative


CORRELATION_WINDOW = timedelta(seconds=30)
LOG_FILE = Path("logs/security_events.json")


def correlate_events(events):

    if not events:
        return []

    attacks = []
    current_attack = [events[0]]

    for event in events[1:]:

        previous_event = current_attack[-1]

        try:
            previous_time = datetime.fromisoformat(
                previous_event["timestamp"]
            )

            current_time = datetime.fromisoformat(
                event["timestamp"]
            )

        except (KeyError, ValueError):
            current_attack.append(event)
            continue

        same_process = (
            event.get("pid") == previous_event.get("pid")
        )

        within_time_window = (
            current_time - previous_time <= CORRELATION_WINDOW
        )

        if same_process and within_time_window:
            current_attack.append(event)

        else:
            attacks.append(current_attack)
            current_attack = [event]

    attacks.append(current_attack)

    return attacks


def summarize_attack(events):

    files = list(dict.fromkeys(
        event.get("file", "Unknown")
        for event in events
    ))

    pids = list(dict.fromkeys(
        event.get("pid")
        for event in events
        if event.get("pid") is not None
    ))

    scores = [
        event.get("threat_score", 0)
        for event in events
    ]

    return {
        "attack_start": events[0].get("timestamp"),
        "attack_end": events[-1].get("timestamp"),
        "event_count": len(events),
        "files_accessed": files,
        "process_ids": pids,
        "maximum_threat_score": max(scores, default=0),
        "severity": max(
            events,
            key=lambda event: event.get("threat_score", 0)
        ).get("severity", "UNKNOWN")
    }


def load_events():

    if not LOG_FILE.exists():
        return []

    try:
        with LOG_FILE.open("r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


if __name__ == "__main__":

    print("[*] Loading security events...")

    events = load_events()

    print(f"[*] Events found: {len(events)}")

    attacks = correlate_events(events)

    print(f"[*] Attacks detected: {len(attacks)}")

    for number, attack in enumerate(attacks, start=1):

        summary = summarize_attack(attack)

        print("\n========== ATTACK SUMMARY ==========")
        print(f"Attack: {number}")
        print(f"Events: {summary['event_count']}")
        print(f"Process IDs: {summary['process_ids']}")
        print(f"Files accessed:")

        for file in summary["files_accessed"]:
            print(f"    - {file}")

        print(
            f"Maximum threat score: "
            f"{summary['maximum_threat_score']}"
        )

        print(f"Severity: {summary['severity']}")
        print(
            f"Start: {summary['attack_start']}"
        )
        print(
            f"End: {summary['attack_end']}"
        )
        print("\n---------- THREAT NARRATIVE ----------")
        print(generate_attack_narrative(summary))
        print("---------------------------------------")
        print("=====================================")
