from process_attributor import get_process_info


def should_contain(security_event):
    """
    Decide whether an event should trigger containment.
    """

    severity = security_event.get("severity", "").upper()
    score = security_event.get("threat_score", 0)

    return severity == "CRITICAL" or score >= 80


def contain_process(pid):
    """
    Controlled-demo process termination.
    """

    try:
        import psutil

        process = psutil.Process(pid)

        print("\n🔒 CONTAINMENT TRIGGERED")
        print(f"Process: {process.pid}")
        print(f"Name: {process.name()}")

        # Safety check:
        # Only terminate our simulated attacker process.
        command = " ".join(process.cmdline())

        if "attacker_simulation.py" not in command:
            print("[!] Process is not the controlled attacker.")
            print("[!] Termination cancelled.")
            return False

        process.terminate()

        print("[+] Simulated attacker process terminated.")

        return True

    except psutil.NoSuchProcess:
        print("[!] Process no longer exists.")
        return False

    except psutil.AccessDenied:
        print("[!] Access denied while terminating process.")
        return False


def respond_to_attack(security_event):
    """
    Main response function.
    """

    if not should_contain(security_event):
        print("[*] Threat below containment threshold.")
        return {
            "contained": False,
            "process_terminated": False
        }

    pid = security_event.get("pid")

    if not pid:
        print("[!] No process ID available.")
        return {
            "contained": False,
            "process_terminated": False
        }

    terminated = contain_process(pid)

    return {
        "contained": terminated,
        "process_terminated": terminated
    }
