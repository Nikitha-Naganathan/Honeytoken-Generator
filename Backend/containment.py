from blocked_ips import block_ip


def contain_event(event):
    result = {
        "containment_status": "contained",
        "process_terminated": "requested",
        "ip_blocked": "pending"
    }

    # Block source if a usable IP exists
    if event.source_ip:
        block_ip(event.source_ip)
        result["ip_blocked"] = "blocked"

    return result