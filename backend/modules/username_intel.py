import requests

class Module:
    name = "Username Intel"
    target_types = ["username"]

    def run(self, username):
        sites = {
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "Twitter": f"https://twitter.com/{username}"
        }

        found = {}

        for site, url in sites.items():
            try:
                r = requests.get(url, timeout=5)
                found[site] = r.status_code == 200
            except:
                found[site] = False

        return {
            "module": self.name,
            "result": {
                "status": "ok",
                "data": found,
                "risk": sum(found.values()) * 10
            }
        }
