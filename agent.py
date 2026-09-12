<<<<<<< ours
import requests
from filesystem_watcher import start_watcher


BACKEND_URL = "http://127.0.0.1:8000/events"


def send_event_to_backend(event):
    backend_event = {
        "timestamp": event["timestamp"],
        "event_type": event["event_type"],
        "file": event["file"],
        "filesystem_event": event["filesystem_event"],
        "pid": event["pid"],
        "process_name": event["process_name"],
        "username": event["username"],
        "command": event["command"],
        "severity": event["severity"],
        "threat_score": event["threat_score"],
        "threat_reasons": event["threat_reasons"]
    }

    print("\n========== BACKEND PAYLOAD ==========")
    print(backend_event)
    print("=====================================\n")

    try:
        response = requests.post(
            BACKEND_URL,
            json=backend_event,
            timeout=5
        )

        print(f"[+] Backend response: {response.status_code}")

        if response.status_code >= 400:
            print(f"[!] Backend error: {response.text}")

    except requests.RequestException as error:
        print(f"[!] Could not connect to backend: {error}")


if __name__ == "__main__":
    print("[*] Starting HoneyTrace agent...")

    start_watcher(
        event_callback=send_event_to_backend
    )
||||||| base
=======
import requests
from filesystem_watcher import start_watcher


BACKEND_URL = "http://172.18.229.85:8000/events"


def send_event_to_backend(event):
    backend_event = {
        "timestamp": event["timestamp"],
        "event_type": event["event_type"],
        "file": event["file"],
        "filesystem_event": event["filesystem_event"],
        "pid": event["pid"],
        "process_name": event["process_name"],
        "username": event["username"],
        "command": event["command"],
        "severity": event["severity"],
        "threat_score": event["threat_score"],
        "threat_reasons": event["threat_reasons"]
    }

    print("\n========== BACKEND PAYLOAD ==========")
    print(backend_event)
    print("=====================================\n")

    try:
        response = requests.post(
            BACKEND_URL,
            json=backend_event,
            timeout=5
        )

        print(f"[+] Backend response: {response.status_code}")

        if response.status_code >= 400:
            print(f"[!] Backend error: {response.text}")

    except requests.RequestException as error:
        print(f"[!] Could not connect to backend: {error}")


if __name__ == "__main__":
    print("[*] Starting HoneyTrace agent...")

    start_watcher(
        event_callback=send_event_to_backend
    )
>>>>>>> theirs
