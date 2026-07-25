from abc import ABC, abstractmethod

class OSINTModule(ABC):
    name = "base"
    target_types = []

    @abstractmethod
    def run(self, target: str) -> dict:
        """Run the module against the target."""
        pass