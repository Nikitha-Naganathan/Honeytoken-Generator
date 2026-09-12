import os
import socket
import time
from pathlib import Path


LOG_DIR = Path("logs")
PID_FILE = LOG_DIR / "simulator.pid"

HONEYTOKENS = [
    Path("honeytokens/passwords.txt"),
    Path("honeytokens/api_keys.txt"),
    Path("honeytokens/database_credentials.txt")
]

# Local test server
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999


LOG_DIR.mkdir(exist_ok=True)


# --------------------------------
# RECORD SIMULATOR PID
# --------------------------------

PID_FILE.write_text(str(os.getpid()))

print("[SIMULATION] Attacker process started")
print(f"[SIMULATION] PID: {os.getpid()}")


# --------------------------------
# CREATE HARMLESS NETWORK CONNECTION
# --------------------------------

try:
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client_socket.connect(
        (SERVER_HOST, SERVER_PORT)
    )

    print(
        f"[SIMULATION] Connected to "
        f"{SERVER_HOST}:{SERVER_PORT}"
    )

except Exception as error:
    print(
        f"[SIMULATION] Network connection failed: {error}"
    )

    client_socket = None


# --------------------------------
# WAIT BEFORE ATTACK
# --------------------------------

time.sleep(2)


# --------------------------------
# ACCESS HONEYTOKENS
# --------------------------------

for honeytoken in HONEYTOKENS:

    print(
        f"[SIMULATION] Accessing: {honeytoken}"
    )

    # READ ONLY — does NOT modify the honeytoken
    with honeytoken.open("r") as file:
        file.read()

    time.sleep(2)


# --------------------------------
# KEEP PROCESS ALIVE
# --------------------------------

print("[SIMULATION] Attack simulation complete")

time.sleep(5)


# --------------------------------
# CLEANUP
# --------------------------------

if client_socket:
    client_socket.close()

if PID_FILE.exists():
    PID_FILE.unlink()

print("[SIMULATION] Process finished")