import os
from cachetools import TTLCache
from dotenv import load_dotenv
load_dotenv()
TTL = int(os.getenv("INTEL_CACHE_TTL", "3600"))
CACHE = TTLCache(maxsize=4096, ttl=TTL)
def make_cache_key(prefix: str, key: str) -> str:
    return f"{prefix}:{key}"
