import importlib
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODULE_DIR = os.path.join(BASE_DIR, "modules")

def load_modules():

    modules = []

    sys.path.append(BASE_DIR)

    for file in os.listdir(MODULE_DIR):

        if file.endswith(".py") and not file.startswith("__"):

            mod_name = file[:-3]

            try:

                mod = importlib.import_module(f"modules.{mod_name}")
                modules.append(mod.Module())

            except Exception:
                pass

    return modules