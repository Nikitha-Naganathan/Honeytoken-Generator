from pathlib import Path


def calculate_threat_score(file_path, process_info):
    score = 0
    reasons = []

    file_path = Path(file_path)

    # Honeytoken access is already a strong signal
    score += 50
    reasons.append("Honeytoken accessed")

    # Credential-related files are more sensitive
    sensitive_keywords = [
        "password",
        "api",
        "credential",
        "secret",
        "key"
    ]

    if any(keyword in file_path.name.lower() for keyword in sensitive_keywords):
        score += 20
        reasons.append("Sensitive credential-related honeytoken")

    # Process information was successfully identified
    if process_info.get("pid"):
        score += 10
        reasons.append("Responsible process identified")

    # Check for suspicious process names
    process_name = process_info.get("name", "").lower()

    suspicious_processes = [
        "curl",
        "wget",
        "nc",
        "netcat"
    ]

    if any(process in process_name for process in suspicious_processes):
        score += 20
        reasons.append("Suspicious process detected")

    # Maximum score is 100
    score = min(score, 100)

    # Convert score into severity
    if score >= 80:
        severity = "CRITICAL"
    elif score >= 60:
        severity = "HIGH"
    elif score >= 30:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "threat_score": score,
        "severity": severity,
        "reasons": reasons
    }


if __name__ == "__main__":
    test_process = {
        "pid": 12345,
        "name": "Python",
        "username": "demo",
        "command": "attacker_simulation.py"
    }

    result = calculate_threat_score(
        "honeytokens/passwords.txt",
        test_process
    )

    print(result)
