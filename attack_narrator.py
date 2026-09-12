def generate_attack_narrative(summary):

    severity = summary.get("severity", "UNKNOWN")
    event_count = summary.get("event_count", 0)
    files = summary.get("files_accessed", [])
    pids = summary.get("process_ids", [])
    score = summary.get("maximum_threat_score", 0)

    process_text = (
        f"process {pids[0]}"
        if pids
        else "an unknown process"
    )

    file_names = []

    for file in files:
        file_names.append(file.split("/")[-1])

    if len(file_names) == 1:
        files_text = file_names[0]

    elif len(file_names) == 2:
        files_text = f"{file_names[0]} and {file_names[1]}"

    else:
        files_text = (
            ", ".join(file_names[:-1])
            + f", and {file_names[-1]}"
        )

    if event_count >= 3:
        behavior = (
            "This pattern is consistent with automated "
            "credential discovery."
        )

    elif event_count == 2:
        behavior = (
            "Multiple honeytoken accesses were detected, "
            "indicating potentially suspicious activity."
        )

    else:
        behavior = (
            "A honeytoken was accessed, indicating "
            "potentially unauthorized activity."
        )

    narrative = (
        f"{severity} ATTACK DETECTED: "
        f"{process_text} accessed {event_count} honeytoken "
        f"asset(s), including {files_text}. "
        f"The maximum threat score was {score}/100. "
        f"{behavior}"
    )

    return narrative


if __name__ == "__main__":

    test_summary = {
        "event_count": 3,
        "files_accessed": [
            "honeytokens/passwords.txt",
            "honeytokens/api_keys.txt",
            "honeytokens/database_credentials.txt"
        ],
        "process_ids": [47515],
        "maximum_threat_score": 80,
        "severity": "CRITICAL"
    }

    print(generate_attack_narrative(test_summary))
