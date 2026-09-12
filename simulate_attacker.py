import os
import time

DEMO_DIR = "/app/demo"

print("===================================")
print("   BENIGN ATTACK SIMULATION")
print("===================================")

print("\nSearching for honeytokens...\n")

files = os.listdir(DEMO_DIR)

for filename in files:
    filepath = os.path.join(DEMO_DIR, filename)

    print(f"Found: {filename}")
    print(f"Accessing: {filename}")

    # Read only the designated fake honeytoken
    with open(filepath, "r") as file:
        file.read()

    print(f"Completed access: {filename}\n")

    time.sleep(3)

print("Simulation complete.")