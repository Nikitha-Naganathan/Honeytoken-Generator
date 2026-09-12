import os
import time
from pathlib import Path


LOG_DIR = Path("logs")
PID_FILE = LOG_DIR / "simulator.pid"

HONEYTOKENS = [
    Path("honeytokens/passwords.txt"),
    Path("honeytokens/api_keys.txt"),
    Path("honeytokens/database_credentials.txt")
]


LOG_DIR.mkdir(exist_ok=True)

# Record this process's PID for the controlled demo
PID_FILE.write_text(str(os.getpid()))

print("[SIMULATION] Attacker process started")
print(f"[SIMULATION] PID: {os.getpid()}")

time.sleep(2)


for honeytoken in HONEYTOKENS:

    print(f"[SIMULATION] Accessing: {honeytoken}")

    with honeytoken.open("a") as file:
        file.write("\nSIMULATED ATTACK ACCESS\n")

    time.sleep(2)


print("[SIMULATION] Attack simulation complete")

time.sleep(5)


if PID_FILE.exists():
    PID_FILE.unlink()

print("[SIMULATION] Process finished")
