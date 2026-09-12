# Processes that are considered trusted.
# This is a basic stub for now.
# D can later connect this to the agent/configuration.

ALLOWED_PROCESSES = {
    "explorer.exe",
    "trusted_backup.exe",
}


def is_allowed_process(process_name: str) -> bool:
    if not process_name:
        return False

    return process_name.lower() in ALLOWED_PROCESSES