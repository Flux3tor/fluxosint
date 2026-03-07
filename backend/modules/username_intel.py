import requests
from backend.engine.base import OSINTModule

class Module(OSINTModule):
    name = "Username Intel"
    target_types = ["username"]

    sites = {
        "GitHub": "https://github.com/{}",
        "Reddit": "https://reddit.com/user/{}",
        "Twitter": "https://x.com/{}",
        "GitLab": "https://gitlab.com/{}",
        "Instagram": "https://instagram.com/{}"
    }

    def run(self, username):

        headers = {"User-Agent": "FluxOSINT"}

        found = {}

        for site, url in self.sites.items():

            try:
                r = requests.get(url.format(username), headers=headers, timeout=6)

                if r.status_code == 404:
                    found[site] = False
                else:
                    found[site] = username.lower() in r.text.lower()

            except requests.RequestException:
                found[site] = False
        
        return {
            "status": "ok",
            "data": found,
            "risk": sum(found.values()) * 10
        }