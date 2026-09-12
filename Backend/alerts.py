import os
import requests
from dotenv import load_dotenv

load_dotenv()


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
            f"**Threat Score:** `{event.threat_score}`\n\n"

            "🛡️ **RESPONSE STATUS**\n"
            f"**Containment:** `{event.containment_status}`\n"
            f"**Process Termination:** `{event.process_terminated}`\n"
            f"**IP Status:** `{event.ip_blocked}`\n\n"

            "🌐 **SOURCE**\n"
            f"**Source IP:** `{event.source_ip}`\n"
            f"**Location:** "
            f"`{event.city}, {event.region}, {event.country}`\n\n"

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

            print(
                f"❌ Discord alert failed: "
                f"{response.status_code}"
            )

    except Exception as e:

        print(
            f"❌ Discord alert error: {e}"
        )