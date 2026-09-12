from threat_score import calculate_threat_score
from response_engine import respond_to_attack
from network_attributor import get_remote_ips

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pathlib import Path
from datetime import datetime, timedelta

from process_attributor import get_process_info
from security_event import create_security_event, print_security_event
from event_logger import log_security_event

import time


HONEYTOKEN_DIR = Path("honeytokens")
PID_FILE = Path("logs/simulator.pid")

LAST_EVENTS = {}
DEDUP_WINDOW = timedelta(seconds=1)


class HoneytokenHandler(FileSystemEventHandler):

    def __init__(self, event_callback=None):
        super().__init__()

        self.event_callback = event_callback

        # Keep track of processes that HoneyTrace has already contained.
        # This prevents delayed filesystem events from being processed again.
        self.contained_pids = set()

    def on_modified(self, event):
        self.check_honeytoken(event, "modified")

    def on_created(self, event):
        self.check_honeytoken(event, "created")

    def check_honeytoken(self, event, event_type):

        # Ignore directories
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only monitor files directly inside the honeytokens directory
        if file_path.resolve().parent != HONEYTOKEN_DIR.resolve():
            return

        # Prevent duplicate filesystem events
        event_key = str(file_path.resolve())
        now = datetime.now()

        if event_key in LAST_EVENTS:

            time_since_last = now - LAST_EVENTS[event_key]

            if time_since_last < DEDUP_WINDOW:
                return

        LAST_EVENTS[event_key] = now

        print("\n🚨 HONEYTOKEN TRIGGERED")
        print(f"File: {file_path}")
        print(f"Event: {event_type}")
        print(f"Time: {now}")

        # Check whether the simulator PID exists
        if not PID_FILE.exists():

            print("[!] Simulator PID not found")

            return

        # Read simulator PID
        try:

            pid = int(
                PID_FILE.read_text().strip()
            )

        except ValueError:

            print("[!] Invalid PID file")

            return

        # Ignore events from processes that HoneyTrace
        # has already contained.
        if pid in self.contained_pids:

            print(
                f"[*] Ignoring event from already "
                f"contained process {pid}"
            )

            return

        # -------------------------------------------------
        # PROCESS ATTRIBUTION
        # -------------------------------------------------

        process_info = get_process_info(pid)

        # The filesystem event can arrive slightly after
        # the process has disappeared.
        #
        # In that situation, do not create an Unknown
        # security event.
        if process_info.get("error") == "Process no longer exists":

            print(
                f"[*] Ignoring delayed event: "
                f"process {pid} no longer exists."
            )

            return

        # -------------------------------------------------
        # NETWORK ATTRIBUTION
        # -------------------------------------------------

        remote_ips = get_remote_ips(pid)

        print("\n========== NETWORK INFORMATION ==========")

        if remote_ips:

            for ip in remote_ips:
                print(f"Remote IP: {ip}")

        else:

            print("Remote IP: None detected")

        print("=========================================")

        # -------------------------------------------------
        # SECURITY EVENT
        # -------------------------------------------------

        security_event = create_security_event(
            file_path,
            event_type,
            process_info
        )

        # Add network information
        security_event["remote_ips"] = remote_ips

        # -------------------------------------------------
        # THREAT SCORING
        # -------------------------------------------------

        threat_result = calculate_threat_score(
            file_path,
            process_info
        )

        security_event["threat_score"] = (
            threat_result["threat_score"]
        )

        security_event["severity"] = (
            threat_result["severity"]
        )

        security_event["threat_reasons"] = (
            threat_result["reasons"]
        )

        # Display security event
        print_security_event(security_event)

        # -------------------------------------------------
        # ACTIVE RESPONSE
        # -------------------------------------------------

        response_result = respond_to_attack(
            security_event
        )

        security_event["contained"] = (
            response_result["contained"]
        )

        security_event["process_terminated"] = (
            response_result["process_terminated"]
        )

        # If the attacker was successfully terminated,
        # remember its PID so delayed filesystem events
        # are ignored.
        if response_result["process_terminated"]:

            self.contained_pids.add(pid)

        print("\n========== RESPONSE RESULT ==========")

        print(
            f"Contained: "
            f"{response_result['contained']}"
        )

        print(
            f"Process terminated: "
            f"{response_result['process_terminated']}"
        )

        print("=====================================")

        # -------------------------------------------------
        # LOCAL LOGGING
        # -------------------------------------------------

        log_security_event(
            security_event
        )

        # -------------------------------------------------
        # BACKEND CALLBACK
        # -------------------------------------------------

        if self.event_callback:

            self.event_callback(
                security_event
            )


def start_watcher(event_callback=None):

    # Make sure directories exist
    HONEYTOKEN_DIR.mkdir(
        exist_ok=True
    )

    Path("logs").mkdir(
        exist_ok=True
    )

    # Create event handler
    event_handler = HoneytokenHandler(
        event_callback=event_callback
    )

    # Create filesystem observer
    observer = Observer()

    observer.schedule(
        event_handler,
        str(HONEYTOKEN_DIR),
        recursive=False
    )

    observer.start()

    print(
        f"[*] Watching: "
        f"{HONEYTOKEN_DIR}"
    )

    print(
        "[*] HoneyTrace filesystem "
        "watcher is running..."
    )

    print(
        "[*] Waiting for honeytoken activity..."
    )

    print(
        "[*] Press Ctrl+C to stop."
    )

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()


if __name__ == "__main__":

    start_watcher()
