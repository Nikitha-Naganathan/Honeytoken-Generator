import os
import time

DEMO_DIR = "honeytokens"
PID_FILE = "logs/simulator.pid"

# Create logs folder
os.makedirs("logs", exist_ok=True)

# Save the simulator's process ID
with open(PID_FILE, "w") as file:
    file.write(str(os.getpid()))

print("===================================")
print("   BENIGN ATTACK SIMULATION")
print("===================================")

print(f"\nSimulator PID: {os.getpid()}")
print("\nSearching for honeytokens...\n")

# Find honeytoken files
files = os.listdir(DEMO_DIR)

for filename in files:

    filepath = os.path.join(DEMO_DIR, filename)

    print(f"Found: {filename}")
    print(f"Accessing: {filename}")

    # Safely read the fake honeytoken
    with open(filepath, "rb") as file:
        file.read()

    print(f"Completed access: {filename}\n")

    time.sleep(3)

# Make a harmless modification so watchdog detects activity
trigger_file = os.path.join(DEMO_DIR, ".env.backup")

with open(trigger_file, "a") as file:
    file.write("\n# benign simulation trigger")

print("Honeytoken modification generated.")
print("Keeping simulator alive for 60 seconds...")

time.sleep(60)

print("Simulation complete.")