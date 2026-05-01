import os, requests
from cachetools import cached
from intel.cache import CACHE, make_cache_key
OTX_KEY = os.getenv("OTX_KEY")
BASE = "https://otx.alienvault.com/api/v1"
def _headers():
    return {"X-OTX-API-KEY": OTX_KEY} if OTX_KEY else {}
def _cache_key(ip):
    return make_cache_key("otx", ip)
@cached(CACHE, key=lambda ip: _cache_key(ip))
def lookup_ip(ip: str):
    try:
        url = f"{BASE}/indicators/IPv4/{ip}"
        r = requests.get(url, headers=_headers(), timeout=10)
        if r.status_code == 200:
            return {"status": "ok", "data": r.json()}
        else:
            return {"status": "error", "code": r.status_code, "text": r.text}
    except Exception as e:
        return {"status": "error", "exception": str(e)}
