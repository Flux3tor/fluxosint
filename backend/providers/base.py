from abc import ABC, abstractmethod

class Provider(ABC):
    name = "base"

    @abstractmethod
    def search(self, email: str) -> dict:
        """Search for information using an email."""
        pass