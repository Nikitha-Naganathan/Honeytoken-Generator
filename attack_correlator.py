from datetime import datetime, timedelta


# Events within this time window can belong to the same attack
CORRELATION_WINDOW = timedelta(seconds=30)


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


if __name__ == "__main__":

    print("[*] Attack correlator module works")
