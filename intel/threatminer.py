"""
intel/threatminer.py – unified ThreatMiner lookup module
Handles API 500 gracefully with fallback cache
"""

import requests, json, time, os

THREATMINER_URL = "https://api.threatminer.org/v2/host.php"
CACHE_FILE = "cache/threatminer_cache.json"

os.makedirs("cache", exist_ok=True)

def _save_cache(ip, data):
    try:
        cache = {}
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
        cache[ip] = data
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print("[!] Cache save failed:", e)

def _load_cache(ip):
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
            return cache.get(ip)
    except Exception:
        pass
    return None


def lookup_ip(ip: str):
    """ThreatMiner IP lookup with retry and fallback"""
    params = {"q": ip, "rt": 1}

    # ৩ বার retry
    for attempt in range(3):
        try:
            r = requests.get(THREATMINER_URL, params=params, timeout=8)
            if r.status_code == 200:
                data = r.json()
                if data.get("status") == "success":
                    _save_cache(ip, data)
                    return {"status": "ok", "data": data}
                else:
                    return {"status": "error", "message": data.get("status")}
            elif r.status_code == 500:
                print(f"[!] ThreatMiner API 500 (server busy) retrying... {attempt+1}/3")
                time.sleep(2)
                continue
            else:
                return {"status": "error", "message": f"HTTP {r.status_code}"}
        except Exception as e:
            print(f"[!] ThreatMiner error: {e}")
            time.sleep(2)

    # 🔄 যদি API কাজ না করে তাহলে cached data ব্যবহার
    cached = _load_cache(ip)
    if cached:
        return {
            "status": "cached",
            "data": cached,
            "message": "ThreatMiner offline, used cached result"
        }

    # ❌ কোনো data না পেলে fallback
    return {
        "status": "fallback",
        "data": {
            "message": "ThreatMiner unreachable, please check manually",
            "risk": "medium",
            "country": "unknown"
        }
    }
