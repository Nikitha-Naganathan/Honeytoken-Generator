import requests


def get_ip_location(ip):
    """
    Get approximate geographic information for an IP address.
    """

    # Local/loopback addresses do not have useful
    # public geolocation information.
    if ip.startswith("127.") or ip == "localhost":
        return {
            "ip": ip,
            "location": "Local machine",
            "city": None,
            "region": None,
            "country": None,
            "isp": None
        }

    try:
        response = requests.get(
            f"https://ipwho.is/{ip}",
            timeout=5
        )

        data = response.json()

        if not data.get("success", False):
            return {
                "ip": ip,
                "location": "Unknown",
                "city": None,
                "region": None,
                "country": None,
                "isp": None
            }

        return {
            "ip": ip,
            "location": (
                f"{data.get('city', 'Unknown')}, "
                f"{data.get('region', 'Unknown')}, "
                f"{data.get('country', 'Unknown')}"
            ),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "isp": data.get("connection", {}).get("isp")
        }

    except requests.RequestException as error:
        return {
            "ip": ip,
            "location": "Lookup failed",
            "city": None,
            "region": None,
            "country": None,
            "isp": None,
            "error": str(error)
        }


if __name__ == "__main__":

    test_ip = "8.8.8.8"

    print("[*] Testing IP geolocation...")
    result = get_ip_location(test_ip)

    print(result)
