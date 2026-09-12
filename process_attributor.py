import psutil


def get_process_info(pid):
    try:
        process = psutil.Process(pid)

        return {
            "pid": process.pid,
            "name": process.name(),
            "username": process.username(),
            "command": " ".join(process.cmdline())
        }

    except psutil.NoSuchProcess:
        return {
            "pid": pid,
            "error": "Process no longer exists"
        }

    except psutil.AccessDenied:
        return {
            "pid": pid,
            "error": "Access denied"
        }




    info = get_process_info(pid)

    print("\n[*] Process Information")
    print(f"PID: {info.get('pid')}")
    print(f"Name: {info.get('name', 'N/A')}")
    print(f"User: {info.get('username', 'N/A')}")
    print(f"Command: {info.get('command', 'N/A')}")
    print(f"Error: {info.get('error', 'None')}")
