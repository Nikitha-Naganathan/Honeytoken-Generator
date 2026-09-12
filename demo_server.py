import socket
import json
from pathlib import Path
from datetime import datetime


HOST = "0.0.0.0"
PORT = 9999

HONEYTOKEN = Path("honeytokens/passwords.txt").resolve()
NETWORK_CONTEXT_FILE = Path("logs/network_context.json").resolve()
ACCESS_EVENT_FILE = Path("logs/honeytoken_access.json").resolve()


# Make sure required directories exist
HONEYTOKEN.parent.mkdir(parents=True, exist_ok=True)
NETWORK_CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)


# Create fake honeytoken if it doesn't exist
if not HONEYTOKEN.exists():
    HONEYTOKEN.write_text(
        "HoneyTrace fake credential file\n"
        "This file contains no real credentials.\n",
        encoding="utf-8"
    )


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))
server.listen(5)


print("[*] HoneyTrace demo server started")
print(f"[*] Listening on port {PORT}")
print(f"[*] Honeytoken: {HONEYTOKEN}")
print("[*] Waiting for System B...")


while True:

    client, address = server.accept()

    source_ip = address[0]
    source_port = address[1]

    print("\n========== NETWORK REQUEST ==========")
    print(f"Source IP: {source_ip}")
    print(f"Source Port: {source_port}")
    print("=====================================")

    data = client.recv(1024)

    message = data.decode(
        errors="ignore"
    ).strip()

    print(f"Data received: {message}")

    # --------------------------------------------------
    # Record network context
    # --------------------------------------------------

    network_context = {
        "timestamp": datetime.now().isoformat(),
        "source_ip": source_ip,
        "source_port": source_port
    }

    NETWORK_CONTEXT_FILE.write_text(
        json.dumps(
            network_context,
            indent=4
        ),
        encoding="utf-8"
    )

    # --------------------------------------------------
    # Controlled honeytoken access
    # --------------------------------------------------

    if message == "HELLO HONEYTRACE":

        print(
            "\n[!] Simulated suspicious request detected"
        )

        print(
            f"[!] Accessing fake honeytoken: "
            f"{HONEYTOKEN}"
        )

        # Read ONLY the fake honeytoken
        fake_data = HONEYTOKEN.read_text(
            encoding="utf-8"
        )

        print(
            "[!] Fake honeytoken accessed."
        )

        # --------------------------------------------------
        # Create explicit HoneyTrace access event
        # --------------------------------------------------

        access_event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "honeytoken_access",
            "file": str(HONEYTOKEN),
            "filesystem_event": "read",
            "source_ip": source_ip,
            "source_port": source_port,
            "process_name": "demo_server.py",
            "message": message
        }

        ACCESS_EVENT_FILE.write_text(
            json.dumps(
                access_event,
                indent=4
            ),
            encoding="utf-8"
        )

        print(
            "[+] HoneyTrace access event recorded."
        )

        response = (
            b"HoneyTrace detected and logged "
            b"the request\n"
        )

    else:

        response = (
            b"HoneyTrace demo server received "
            b"request\n"
        )

    client.sendall(response)

    client.close()