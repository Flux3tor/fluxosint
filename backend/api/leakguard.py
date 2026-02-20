from fastapi import APIRouter
import requests

router = APIRouter(prefix="/leakguard", tags=["LeakGuard"])

@router.get("/{hash_prefix}")
def check_prefix(hash_prefix: str):
    url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
    headers = {
        "User-Agent": "FluxOSINT"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return {"error": "HIBP unreachable"}

        lines = r.text.splitlines()
        results = {}

        for line in lines:
            suffix, count = line.split(":")
            results[suffix] = int(count)

        return results
    except Exception:
        return {"error": "request_failed"}
