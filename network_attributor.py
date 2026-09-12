import psutil

from ip_geolocation import get_ip_location


def get_network_connections(pid):
    """
    Get network connections associated with a process.
    """

    connections = []

    try:
        process = psutil.Process(pid)

        for connection in process.net_connections(kind="inet"):

            remote_ip = None
            remote_port = None

            if connection.raddr:
                remote_ip = connection.raddr.ip
                remote_port = connection.raddr.port

            connections.append({
                "local_address": (
                    f"{connection.laddr.ip}:{connection.laddr.port}"
                    if connection.laddr
                    else None
                ),
                "remote_ip": remote_ip,
                "remote_port": remote_port,
                "status": connection.status
            })

        return connections

    except psutil.NoSuchProcess:
        return []

    except psutil.AccessDenied:
        return []

    except Exception as error:
        print(f"[!] Network attribution error: {error}")
        return []


def get_remote_ips(pid):
    """
    Return unique remote IP addresses for a process.
    """

    connections = get_network_connections(pid)

    remote_ips = []

    for connection in connections:

        remote_ip = connection.get("remote_ip")

        if remote_ip and remote_ip not in remote_ips:
            remote_ips.append(remote_ip)

    return remote_ips


def get_network_locations(pid):
    """
    Get approximate geographic locations
    for remote IP addresses associated with a process.
    """

    remote_ips = get_remote_ips(pid)

    locations = []

    for ip in remote_ips:

        location = get_ip_location(ip)

        locations.append(location)

    return locations


if __name__ == "__main__":

    import os

    current_pid = os.getpid()

    print(
        f"[*] Checking network connections "
        f"for PID {current_pid}"
    )

    connections = get_network_connections(current_pid)

    if not connections:

        print("[*] No network connections found.")

    else:

        for connection in connections:
            print(connection)

    print("\n[*] Checking IP geolocation...")

    locations = get_network_locations(current_pid)

    if not locations:

        print("[*] No remote IP locations found.")

    else:

        for location in locations:
            print(location)
