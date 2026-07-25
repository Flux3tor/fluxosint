import os
import importlib

BASE_DIR = os.path.dirname(__file__)

def load_providers():
    providers = []

    for file in os.listdir(BASE_DIR):
        if (
            file.endswith(".py")
            and not file.startswith("__")
            and file not in ("base.py", "registry.py")
        ):
            module = importlib.import_module(
                f"backend.providers.{file[:-3]}"
            )

            providers.append(module.Provider())

    return providers