import importlib
import os

MODULE_PATH = "modules"

def load_modules():
    modules = []
    for file in os.listdir(MODULE_PATH):
        if file.endswith(".py") and not file.startswith("__"):
            mod_name = file[:-3]
            mod = importlib.import_module(f"{MODULE_PATH}.{mod_name}")
            modules.append(mod.Module())
    return modules
