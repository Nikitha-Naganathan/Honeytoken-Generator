from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from datetime import datetime
from process_attributor import get_process_info
from security_event import create_security_event, print_security_event
from event_logger import log_security_event
import time


HONEYTOKEN_DIR = Path("honeytokens")
PID_FILE = Path("logs/simulator.pid")


class HoneytokenHandler(FileSystemEventHandler):

    def on_modified(self, event):
        self.check_honeytoken(event, "modified")

    def on_created(self, event):
        self.check_honeytoken(event, "created")

    def check_honeytoken(self, event, event_type):

        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.resolve().parent == HONEYTOKEN_DIR.resolve():

            print("\n🚨 HONEYTOKEN TRIGGERED")
            print(f"File: {file_path}")
            print(f"Event: {event_type}")
            print(f"Time: {datetime.now()}")

            if PID_FILE.exists():

                try:
                    pid = int(PID_FILE.read_text().strip())

                    process_info = get_process_info(pid)

                    security_event = create_security_event(
                        file_path,
                        event_type,
                        process_info
                    )

                    print_security_event(security_event)
                    log_security_event(security_event)

                except ValueError:
                    print("[!] Invalid PID file")

            else:
                print("[!] Simulator PID not found")


def start_watcher():

    HONEYTOKEN_DIR.mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

    event_handler = HoneytokenHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        str(HONEYTOKEN_DIR),
        recursive=False
    )

    observer.start()

    print(f"[*] Watching: {HONEYTOKEN_DIR}")
    print("[*] HoneyTrace filesystem watcher is running...")
    print("[*] Waiting for honeytoken activity...")
    print("[*] Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_watcher()
