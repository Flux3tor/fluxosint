from backend.providers.base import Provider

class Provider(Provider):

    name = "GitHub"

    def search(self, email: str):

        return {
            "provider": self.name,
            "registered": False,
            "confidence": 0,
            "profile": None,
            "evidence": [],
            "events": [],
            "locations": [],
        }