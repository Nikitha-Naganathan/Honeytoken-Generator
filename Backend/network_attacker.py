import socket
import time


# System A = protected endpoint
TARGET_HOST = "172.18.228.211"
TARGET_PORT = 9999


print("[SIMULATION] Network attacker started")
print(f"[SIMULATION] Target: {TARGET_HOST}:{TARGET_PORT}")

# Small delay so the demo looks clear
time.sleep(2)

try:
    # Create TCP connection
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    print("[SIMULATION] Connecting to target...")

    client.connect(
        (TARGET_HOST, TARGET_PORT)
    )

    print("[SIMULATION] Connected.")

    # Harmless simulated attack marker
    message = b"HELLO HONEYTRACE\n"

    print(
        "[SIMULATION] Sending simulated attack request..."
    )

    client.sendall(message)

    # Receive response from demo server
    response = client.recv(1024)

    print(
        "[SIMULATION] Server response:"
    )

    print(
        response.decode(errors="ignore")
    )

    client.close()

    print(
        "[SIMULATION] Network attack complete."
    )

except Exception as error:

    print(
        f"[SIMULATION] Connection failed: {error}"
    )