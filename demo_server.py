import socket
from pathlib import Path
from datetime import datetime
import json


HOST = "0.0.0.0"
PORT = 9999

HONEYTOKEN = Path("honeytokens/passwords.txt")

NETWORK_CONTEXT_FILE = Path("logs/network_context.json")

NETWORK_CONTEXT_FILE.parent.mkdir(exist_ok=True)


def save_network_context(source_ip, source_port):
    """
    Save the most recent network request so that
    HoneyTrace can correlate it with the honeytoken event.
    """

    context = {
        "timestamp": datetime.now().isoformat(),
        "source_ip": source_ip,
        "source_port": source_port
    }

    with NETWORK_CONTEXT_FILE.open("w") as file:
        json.dump(context, file, indent=4)

    print("\n========== NETWORK CONTEXT ==========")
    print(f"Source IP: {source_ip}")
    print(f"Source Port: {source_port}")
    print(f"Saved to: {NETWORK_CONTEXT_FILE}")
    print("=====================================")


def trigger_honeytoken():
    """
    Controlled demo action.

    The network request causes the demo server
    to ACCESS a fake credential file.

    The honeytoken itself is not modified.
    """

    print("\n========== HONEYTOKEN ACTION ==========")
    print(f"Accessing: {HONEYTOKEN}")

    with HONEYTOKEN.open("r") as file:
        file.read()

    print("[+] Honeytoken accessed.")
    print("=======================================")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))
server.listen(5)

print("[*] HoneyTrace demo server started")
print(f"[*] Listening on port {PORT}")
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

    if data:

        message = data.decode(
            errors="ignore"
        ).strip()

        print(
            f"Data received: {message}"
        )

        if message == "HELLO HONEYTRACE":

            save_network_context(
                source_ip,
                source_port
            )

            trigger_honeytoken()

            client.sendall(
                b"HoneyTrace detected and logged the request\n"
            )

        else:

            client.sendall(
                b"Unknown request\n"
            )

    client.close()