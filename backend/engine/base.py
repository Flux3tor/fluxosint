class OSINTModule:
    name = "base"
    target_types = []

    def run(self, target: str) -> dict:
        return {
            "status": "ok",
            "data": {},
            "risk": 0
        }
