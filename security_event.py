from datetime import datetime


def create_security_event(file_path, event_type, process_info):
    return {
        "timestamp": datetime.now().isoformat(),
        "event_type": "honeytoken_access",
        "file": str(file_path),
        "filesystem_event": event_type,
        "pid": process_info.get("pid"),
        "process_name": process_info.get("name", "Unknown"),
        "username": process_info.get("username", "Unknown"),
        "command": process_info.get("command", "Unknown"),
        "severity": "HIGH"
    }


def print_security_event(event):
    print("\n========== SECURITY EVENT ==========")

    for key, value in event.items():
        print(f"{key}: {value}")

    print("====================================")
