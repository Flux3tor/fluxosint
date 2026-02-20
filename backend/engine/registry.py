import importlib
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODULE_DIR = os.path.join(BASE_DIR, "modules")

def load_modules():
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Loading modules...")

    modules = []
    sys.path.append(BASE_DIR)

    for file in os.listdir(MODULE_DIR):
        if file.endswith(".py") and not file.startswith("__"):
            mod_name = file[:-3]
            try:
                print("[DEBUG] Loading module:", mod_name)
                mod = importlib.import_module(f"modules.{mod_name}")
                modules.append(mod.Module())
            except Exception as e:
                print("[DEBUG] Failed to load:", mod_name, e)

    print("[DEBUG] Total modules loaded:", len(modules))
    return modules
