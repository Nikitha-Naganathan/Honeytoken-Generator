import requests
import ipaddress


def get_ip_location(ip):
    try:
        address = ipaddress.ip_address(ip)

        # Private/local IPs don't have useful public geolocation
        if address.is_private:
            return {
                "country": "Private Network",
                "region": "Local",
                "city": "Unknown"
            }

        response = requests.get(
            f"https://ipwho.is/{ip}",
            timeout=3
        )

        data = response.json()

        if not data.get("success", True):
            return {
                "country": "Unknown",
                "region": "Unknown",
                "city": "Unknown"
            }

        return {
            "country": data.get("country", "Unknown"),
            "region": data.get("region", "Unknown"),
            "city": data.get("city", "Unknown")
        }

    except Exception:
        return {
            "country": "Unknown",
            "region": "Unknown",
            "city": "Unknown"
        }