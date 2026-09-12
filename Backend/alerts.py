import os

import requests

from dotenv import load_dotenv


load_dotenv()


def send_alert(event):

    webhook_url = os.getenv(
        "DISCORD_WEBHOOK_URL"
    )


    # -----------------------------------------------------
    # CHECK WEBHOOK
    # -----------------------------------------------------

    if not webhook_url:

        print(
            "❌ Discord webhook not configured"
        )

        return


    # -----------------------------------------------------
    # CREATE DISCORD MESSAGE
    # -----------------------------------------------------

    message = {

        "content": (

            "🚨 **HONEYTRACE ALERT** 🚨\n\n"

            "🔎 **DETECTION**\n"

            f"**File:** `{event.file}`\n"

            f"**Event:** `{event.event_type}`\n"

            f"**Process:** `{event.process_name}`\n"

            f"**PID:** `{event.pid}`\n"

            f"**Severity:** "
            f"**{event.severity.upper()}**\n"

            f"**Threat Score:** "
            f"`{event.threat_score}`\n\n"


            "🌐 **NETWORK SOURCE**\n"

            f"**Source IP:** "
            f"`{event.source_ip}`\n"

            f"**Source Port:** "
            f"`{event.source_port}`\n"

            f"**MAC Address:** "
            f"`{event.mac_address}`\n"

            f"**Subnet:** "
            f"`{event.subnet}`\n"

            f"**Network Type:** "
            f"`{event.network_type}`\n\n"


            "📍 **LOCATION**\n"

            f"**Location:** "
            f"`{event.city}, "
            f"{event.region}, "
            f"{event.country}`\n\n"


            "🛡️ **RESPONSE STATUS**\n"

            f"**Containment:** "
            f"`{event.containment_status}`\n"

            f"**Process Termination:** "
            f"`{event.process_terminated}`\n"

            f"**IP Status:** "
            f"`{event.ip_blocked}`\n\n"


            "🕒 **TIME**\n"

            f"`{event.timestamp}`"
        )
    }


    # -----------------------------------------------------
    # SEND ALERT
    # -----------------------------------------------------

    try:

        response = requests.post(

            webhook_url,

            json=message,

            timeout=5
        )


        if response.status_code in (200, 204):

            print(
                "✅ Discord alert sent"
            )

        else:

            print(
                f"❌ Discord alert failed: "
                f"{response.status_code}"
            )


    except Exception as e:

        print(
            f"❌ Discord alert error: {e}"
        )