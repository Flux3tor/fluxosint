import requests
from backend.engine.base import OSINTModule

class Module(OSINTModule):
    name = "IP Intel"
    target_types = ["ip"]

    def run(self, ip):

        data = {}

        try:
            r = requests.get(
                f"http://ip-api.com/json/{ip}",
                timeout=6
            )

            j = r.json()

            data = {
                "country": j.get("country"),
                "city": j.get("city"),
                "isp": j.get("isp"),
                "org": j.get("org")
            }

        except requests.RequestException:

            data = {
                "country": "Unknown",
                "city": "Unknown",
                "isp": "Unknown",
                "org": "Unknown"
            }

        return {
            "status": "ok",
            "data": data,
            "risk": 15
        }