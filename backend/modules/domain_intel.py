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
        except socket.gaierror:
            result["ip"] = "Not resolved"

        try:
            w = whois.whois(domain)

            created = w.creation_date
            if isinstance(created, list):
                created = created[0]

            result["created"] = str(created)
            result["registrar"] = str(w.registrar)
        
        except Exception:
            result["created"] = "Unknown"
            result["registrar"] = "Unknown"
        
        return {
            "status": "ok",
            "data": result,
            "risk": 25
        }