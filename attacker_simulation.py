import os
import time
from pathlib import Path


LOG_DIR = Path("logs")
PID_FILE = LOG_DIR / "simulator.pid"
HONEYTOKEN = Path("honeytokens/passwords.txt")


LOG_DIR.mkdir(exist_ok=True)

# Record this process's PID for the controlled demo
PID_FILE.write_text(str(os.getpid()))

print("[SIMULATION] Process started")
print(f"[SIMULATION] PID: {os.getpid()}")

time.sleep(3)

print(f"[SIMULATION] Accessing: {HONEYTOKEN}")

with HONEYTOKEN.open("a") as file:
    file.write("\nSIMULATED ATTACK ACCESS\n")

print("[SIMULATION] Honeytoken accessed")

time.sleep(10)

# Remove the temporary PID file when the simulation ends
if PID_FILE.exists():
    PID_FILE.unlink()

print("[SIMULATION] Process finished")
