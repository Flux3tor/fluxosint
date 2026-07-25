from backend.models.dossier import dossier
from backend.providers.registry import load_providers

def build(email: str):

    dossier = Dossier(target=email)

    providers = load_providers()

    for provider in providers:

        result = provider.search(email)

        if result.get("profile"):
            dossier.profiles.append(result["profile"])

        dossier.evidence.extend(result.get("evidence", []))
        dossier.events.extend(result.get("events", []))
        dossier.locations.extend(result.get("locations", []))

        if result.get("profile"):

            profile = result["profile"]

            if profile.username:
                dossier.usernames.add(profile.username)

            if profile.name:
                dossier.names.add(profile.name)

            if profile.avatar:
                dossier.avatars.add(profile.avatar)

    return dossier