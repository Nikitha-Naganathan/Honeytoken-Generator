import os
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


def send_alert(event):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        print("❌ Discord webhook not configured")
        return

    message = {
        "content": (
            "🚨 **HONEYTRAP ALERT** 🚨\n\n"
            f"**File:** `{event.file}`\n"
            f"**Event:** `{event.event_type}`\n"
            f"**Process:** `{event.process_name}`\n"
            f"**PID:** `{event.pid}`\n"
            f"**Severity:** **{event.severity.upper()}**\n"
            f"**Time:** `{event.timestamp}`"
        )
    }

    try:
        response = requests.post(
            webhook_url,
            json=message,
            timeout=5
        )

        if response.status_code in (200, 204):
            print("✅ Discord alert sent")
        else:
            print(f"❌ Discord alert failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Discord alert error: {e}")