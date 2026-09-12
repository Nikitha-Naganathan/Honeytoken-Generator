import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


# Processes that are known to be safe
ALLOWLIST = [
    "Windows Search",
    "SearchIndexer.exe",
    "MsMpEng.exe",
    "OneDrive.exe"
]


def is_allowed_process(process_name: str) -> bool:
    """
    Check whether a process is known to be safe.
    """

    if not process_name:
        return False

    process_name = process_name.lower()

    return any(
        allowed.lower() in process_name
        for allowed in ALLOWLIST
    )


def send_alert(event):
    """
    Send a Discord/Slack-compatible webhook alert.
    """

    if not WEBHOOK_URL:
        print("No WEBHOOK_URL configured. Skipping external alert.")
        return

    if is_allowed_process(event.process_name):
        print(
            f"Process '{event.process_name}' is allowlisted. "
            "Skipping external alert."
        )
        return

    message = {
        "content": (
            "🚨 HONEYTOKEN ALERT 🚨\n\n"
            f"Severity: {event.severity.upper()}\n"
            f"File: {event.filepath}\n"
            f"Event: {event.event_type}\n"
            f"Process: {event.process_name}\n"
            f"PID: {event.pid}\n"
            f"Time: {event.timestamp}"
        )
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=message,
            timeout=5
        )

        if response.status_code >= 400:
            print(
                f"Webhook failed: {response.status_code} "
                f"{response.text}"
            )
        else:
            print("External alert sent successfully.")

    except requests.RequestException as e:
        print(f"Webhook error: {e}")