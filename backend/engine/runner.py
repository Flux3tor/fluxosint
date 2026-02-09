from backend.engine.registry import load_modules

def run_modules(target_type, value):
    results = []
    for module in load_modules():
        if target_type in module.target_types:
            result = module.run(value)
            results.append({
                "module": module.name,
                "result": result
            })
    return results
