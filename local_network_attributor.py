import socket
import subprocess
import ipaddress
import psutil


def get_hostname(ip):
    """
    Try to resolve an IP address to a hostname.
    """

    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname

    except (socket.herror, socket.gaierror, OSError):
        return "Unknown"


def get_mac_address(ip):
    """
    Try to obtain a MAC address from the local ARP table.
    """

    try:
        result = subprocess.run(
            ["arp", "-n", ip],
            capture_output=True,
            text=True,
            timeout=3
        )

        output = result.stdout

        for line in output.splitlines():

            if ip in line:

                parts = line.split()

                for part in parts:

                    if part.count(":") == 5:
                        return part

        return "Unknown"

    except Exception:
        return "Unknown"


def get_mac_vendor(mac):
    """
    Basic OUI/vendor identification.

    For the demo, unknown vendors are returned
    instead of making an external lookup.
    """

    oui_vendors = {
        "AA:BB:CC": "Demo Device",
        "00:1C:42": "Parallels",
        "3C:22:FB": "Apple",
        "A4:83:E7": "Apple",
        "D8:BB:2C": "Dell Inc."
    }

    if not mac or mac == "Unknown":
        return "Unknown"

    oui = mac.upper()[0:8]

    return oui_vendors.get(oui, "Unknown")


def get_subnet(ip):
    """
    Determine the likely local subnet.
    """

    try:
        interfaces = psutil.net_if_addrs()

        target_ip = ipaddress.ip_address(ip)

        for interface, addresses in interfaces.items():

            for address in addresses:

                if address.family == socket.AF_INET:

                    local_ip = ipaddress.ip_address(address.address)

                    if address.netmask:

                        network = ipaddress.ip_network(
                            f"{local_ip}/{address.netmask}",
                            strict=False
                        )

                        if target_ip in network:
                            return str(network)

        return "Unknown"

    except Exception:
        return "Unknown"


def get_network_type(ip):
    """
    Determine whether the source is private or public.
    """

    try:
        address = ipaddress.ip_address(ip)

        if address.is_private:
            return "Internal LAN"

        return "Public Network"

    except ValueError:
        return "Unknown"


def get_local_network_attribution(ip):
    """
    Collect local network attribution information.
    """

    return {
        "source_ip": ip,
        "hostname": get_hostname(ip),
        "mac_address": get_mac_address(ip),
        "vendor": get_mac_vendor(
            get_mac_address(ip)
        ),
        "subnet": get_subnet(ip),
        "network_type": get_network_type(ip)
    }


if __name__ == "__main__":

    test_ip = "192.168.1.42"

    print("[*] Testing local network attribution...")

    result = get_local_network_attribution(test_ip)

    for key, value in result.items():
        print(f"{key}: {value}")
