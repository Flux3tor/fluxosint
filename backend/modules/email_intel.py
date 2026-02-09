from backend.engine.base import OSINTModule
import dns.resolver
import requests
import whois
from bs4 import BeautifulSoup

class Module(OSINTModule):
    name = "Email Intel"
    target_types = ["email"]

    def mx_lookup(self, domain):
        try:
            answers = dns.resolver.resolve(domain, "MX")
            return [str(r.exchange) for r in answers]
        except:
            return []

    def disposable_check(self, domain):
        disposable_domains = [
            "mailinator.com", "10minutemail.com", "tempmail.com",
            "guerrillamail.com", "yopmail.com"
        ]
        return domain.lower() in disposable_domains

    def gravatar_check(self, email):
        import hashlib
        h = hashlib.md5(email.strip().lower().encode()).hexdigest()
        url = f"https://www.gravatar.com/avatar/{h}?d=404"
        try:
            r = requests.get(url, timeout=5)
            return r.status_code == 200
        except:
            return False

    def domain_age(self, domain):
        try:
            w = whois.whois(domain)
            created = w.creation_date
            if isinstance(created, list):
                created = created[0]
            if not created:
                return "unknown"
            return (created.strftime("%Y-%m-%d"))
        except:
            return "unknown"

    def paste_search(self, email):
        query = f'"{email}" site:pastebin.com OR site:ghostbin.com'
        url = f"https://duckduckgo.com/html/?q={query}"
        try:
            r = requests.get(url, headers={"User-Agent": "FluxOSINT"}, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            return len(soup.find_all("a")) > 0
        except:
            return False

    def run(self, target):
        domain = target.split("@")[-1]

        mx = self.mx_lookup(domain)
        disposable = self.disposable_check(domain)
        gravatar = self.gravatar_check(target)
        age = self.domain_age(domain)
        paste = self.paste_search(target)

        risk = 0
        if disposable:
            risk += 30
        if not mx:
            risk += 20
        if paste:
            risk += 40
        if gravatar:
            risk += 5

        return {
            "status": "ok",
            "data": {
                "mx_records": mx,
                "disposable": disposable,
                "gravatar_found": gravatar,
                "domain_created": age,
                "paste_mentions": paste
            },
            "risk": risk
        }
