import time
import urllib.request

TARGET = "http://decoy:8080"

print("===================================")
print("   HONEYTRACE ATTACKER SIMULATION")
print("===================================")

print("[SIMULATION] Starting controlled attacker...")
time.sleep(2)

try:
    print(f"[SIMULATION] Connecting to decoy: {TARGET}")

    response = urllib.request.urlopen(TARGET, timeout=5)

    print(f"[SIMULATION] Decoy responded with HTTP {response.status}")
    print("[SIMULATION] Decoy environment reached successfully.")

except Exception as error:
    print(f"[SIMULATION] Connection failed: {error}")

print("[SIMULATION] Simulating suspicious activity...")

for step in range(1, 4):
    print(f"[SIMULATION] Attack step {step}/3")
    time.sleep(2)

print("[SIMULATION] Controlled attack simulation complete.")