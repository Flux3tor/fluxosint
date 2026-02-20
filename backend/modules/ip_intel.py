import requests
from backend.engine.base import OSINTModule

class Module(OSINTModule):
    name = "IP Intel"
    target_types = ["ip"]

    def run(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=6).json()
        except:
            r = {}

        data = {
            "country": r.get("country"),
            "city": r.get("city"),
            "isp": r.get("isp"),
            "org": r.get("org")
        }

        return {
            "status": "ok",
            "data": data,
            "risk": 15
        }
