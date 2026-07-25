from dataclasses import dataclasses

@dataclasses
class Profile:

    provider: str

    username: str | None = None

    name: str | None = None

    avatar: str | None = None

    url: str | None = None

    metadata: dict | None = None