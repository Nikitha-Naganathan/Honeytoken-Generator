"""
Filesystem Watcher for HoneyTrap
Monitors the honeytokens directory using Watchdog and notifies listeners when honeytoken files are accessed/modified.
"""
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class HoneytokenEventHandler(FileSystemEventHandler):
    def __init__(self, on_trigger_callback):
        super().__init__()
        self.on_trigger_callback = on_trigger_callback

    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if not filename.startswith("."):
                self.on_trigger_callback("MODIFIED", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if not filename.startswith("."):
                self.on_trigger_callback("CREATED", event.src_path)


class HoneytokenWatcher:
    def __init__(self, watch_dir: str, on_trigger_callback):
        self.watch_dir = Path(watch_dir)
        self.watch_dir.mkdir(exist_ok=True)
        self.on_trigger_callback = on_trigger_callback
        self.observer = Observer()

    def start(self):
        handler = HoneytokenEventHandler(self.on_trigger_callback)
        self.observer.schedule(handler, str(self.watch_dir), recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
