import os
import requests
from cachetools import cached
from intel.cache import CACHE, make_cache_key

# APIs
ABUSIX_URL = "https://threat-intel-api.abusix.com/beta/query"
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"


def _cache_key(ip: str):
    return make_cache_key("intel_lookup", ip)


@cached(CACHE, key=lambda ip: _cache_key(ip))
def lookup_ip(ip: str) -> dict:
    """
    Multi-source IP intelligence:
    1. Try Abusix
    2. Fallback to AbuseIPDB
    """

    abusix_key = os.getenv("ABUSIX_KEY")
    abuseipdb_key = os.getenv("ABUSEIPDB_API_KEY")

    # ------------------ ABUSIX ------------------
    if abusix_key:
        try:
            res = requests.get(
                f"{ABUSIX_URL}/{ip}",
                headers={"x-api-key": abusix_key},
                timeout=5
            )

            if res.status_code == 200:
                return {
                    "status": "ok",
                    "provider": "abusix",
                    "ip": ip,
                    "data": res.json()
                }

        except Exception:
            pass  # fallback

    # ------------------ ABUSEIPDB ------------------
    if abuseipdb_key:
        try:
            res = requests.get(
                ABUSEIPDB_URL,
                headers={
                    "Key": abuseipdb_key,
                    "Accept": "application/json"
                },
                params={"ipAddress": ip, "maxAgeInDays": 90},
                timeout=5
            )

            if res.status_code == 200:
                return {
                    "status": "ok",
                    "provider": "abuseipdb",
                    "ip": ip,
                    "data": res.json()
                }

            return {
                "status": "error",
                "provider": "abuseipdb",
                "ip": ip,
                "http_code": res.status_code,
                "response": res.text
            }

        except Exception as e:
            return {
                "status": "error",
                "provider": "abuseipdb",
                "ip": ip,
                "exception": str(e)
            }

    # ------------------ NO KEY ------------------
    return {
        "status": "no_key",
        "message": "No API key available"
    }
