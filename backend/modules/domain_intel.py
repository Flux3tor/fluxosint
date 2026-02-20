import socket
import whois
from backend.engine.base import OSINTModule

class Module(OSINTModule):
    name = "Domain Intel"
    target_types = ["domain"]

    def run(self, domain):
        result = {}

        try:
            result["ip"] = socket.gethostbyname(domain)
        except:
            result["ip"] = "Not resolved"

        try:
            w = whois.whois(domain)
            result["created"] = str(w.creation_date)
            result["registrar"] = str(w.registrar)
        except:
            result["created"] = "Unknown"
            result["registrar"] = "Unknown"

        return {
            "status": "ok",
            "data": result,
            "risk": 25
        }
