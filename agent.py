import requests

from filesystem_watcher import start_watcher


BACKEND_URL = "http://172.18.229.85:8000/events"


def send_event_to_backend(event):

    network_context = event.get(
        "network_context"
    )

    if not isinstance(network_context, dict):
        network_context = {}

    local_network_attribution = event.get(
        "local_network_attribution",
        []
    )

    if not isinstance(local_network_attribution, list):
        local_network_attribution = []

    attribution = {}

    if local_network_attribution:
        if isinstance(local_network_attribution[0], dict):
            attribution = local_network_attribution[0]

    source_ip = network_context.get(
        "source_ip"
    )

    source_port = network_context.get(
        "source_port"
    )

    mac_address = attribution.get(
        "mac_address"
    )

    subnet = attribution.get(
        "subnet"
    )

    network_type = attribution.get(
        "network_type"
    )

    backend_event = {

        "timestamp": event["timestamp"],

        "event_type": event["event_type"],

        "file": event["file"],

        "filesystem_event": event[
            "filesystem_event"
        ],

        "pid": event["pid"],

        "process_name": event[
            "process_name"
        ],

        "username": event["username"],

        "command": event["command"],

        "severity": event["severity"],

        "threat_score": event[
            "threat_score"
        ],

        "threat_reasons": event[
            "threat_reasons"
        ],

        # Network attribution

        "source_ip": source_ip,

        "source_port": source_port,

        "mac_address": mac_address,

        "subnet": subnet,

        "network_type": network_type,

        # Detailed network information

        "remote_ips": event.get(
            "remote_ips",
            []
        ),

        "network_locations": event.get(
            "network_locations",
            []
        ),

        "network_context": network_context,

        "local_network_attribution":
            local_network_attribution,

        # Response

        "response": event.get(
            "response"
        )
    }

    print(
        "\n========== BACKEND PAYLOAD =========="
    )

    print(
        f"Source IP: {source_ip}"
    )

    print(
        f"Source Port: {source_port}"
    )

    print(
        f"MAC Address: {mac_address}"
    )

    print(
        f"Subnet: {subnet}"
    )

    print(
        f"Network Type: {network_type}"
    )

    print(
        "=====================================\n"
    )

    try:

        response = requests.post(
            BACKEND_URL,
            json=backend_event,
            timeout=5
        )

        print(
            f"[+] Backend response: "
            f"{response.status_code}"
        )

        if response.status_code >= 400:

            print(
                f"[!] Backend error: "
                f"{response.text}"
            )

    except requests.RequestException as error:

        print(
            f"[!] Could not connect to backend: "
            f"{error}"
        )


if __name__ == "__main__":

    print(
        "[*] Starting HoneyTrace agent..."
    )

    start_watcher(
        event_callback=send_event_to_backend
    )
