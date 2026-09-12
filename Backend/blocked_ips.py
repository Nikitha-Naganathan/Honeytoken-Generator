blocked_ips = set()


def block_ip(ip):
    if not ip:
        return False

    blocked_ips.add(ip)
    return True


def unblock_ip(ip):
    if ip in blocked_ips:
        blocked_ips.remove(ip)
        return True

    return False


def is_ip_blocked(ip):
    return ip in blocked_ips


def get_blocked_ips():
    return list(blocked_ips)