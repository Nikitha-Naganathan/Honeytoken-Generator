import requests

from honeytoken_generator import generate_honeytokens
from filesystem_watcher import start_watcher


# Person B's backend address
BACKEND_URL = "http://172.18.229.85:8000/events"


def send_event_to_backend(event):

    # Convert Agent A's event format
    # into Person B's backend format
    backend_event = {
        "timestamp": event["timestamp"],
        "filepath": event["file"],
        "event_type": event["event_type"],
        "process_name": event["process_name"],
        "pid": event["pid"],
        "severity": event["severity"]
    }

    try:

        response = requests.post(
            BACKEND_URL,
            json=backend_event,
            timeout=5
        )

        if response.status_code in (200, 201):

            print("[+] Security event sent to backend")

        else:

            print(
                f"[!] Backend rejected event: "
                f"{response.status_code}"
            )

            print(response.text)

    except requests.RequestException as error:

        print(
            f"[!] Could not connect to backend: {error}"
        )


def start_agent():

    print("======================================")
    print("        HONEYTRACE SECURITY AGENT")
    print("======================================")

    print("[*] Generating honeytokens...")

    tokens = generate_honeytokens()

    for token in tokens:
        print(f"    [+] {token}")

    print("[*] Honeytokens ready")

    print("[*] Starting filesystem monitoring...")

    start_watcher(
        event_callback=send_event_to_backend
    )


if __name__ == "__main__":
    start_agent()
