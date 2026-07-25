from dataclasses import dataclass

@dataclass
class Evidence:

    title: str

    value: str

    source: str

    confidence: float