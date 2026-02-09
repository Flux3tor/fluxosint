from backend.engine.base import OSINTModule
import requests

class Module(OSINTModule):
    name = "Username Echo"
    target_types = ["username"]

    def run(self, target):
        platforms = {
            "GitHub": f"https://github.com/{target}",
            "Reddit": f"https://www.reddit.com/user/{target}",
            "Twitter": f"https://x.com/{target}"
        }

        found = {}

        for name, url in platforms.items():
            try:
                r = requests.get(url, timeout=5)
                found[name] = (r.status_code == 200)
            except:
                found[name] = False

        return {
            "status": "ok",
            "data": found,
            "risk": sum(found.values()) * 5
        }
