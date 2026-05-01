# monitoring/host_info.py
import platform
import socket
import uuid
import psutil
import json
from datetime import datetime, timezone

def _get_default_ip() -> str:
    """Best-effort local IP address detection."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connect() এখানে শুধু interface pick করার জন্য, আসলেই ডেটা পাঠায় না
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def _get_mac() -> str:
    """Return MAC address (best effort)."""
    node = uuid.getnode()
    return ":".join(("%012x" % node)[i:i+2] for i in range(0, 12, 2))

def get_host_info() -> dict:
    """Return dictionary with host identity & system resources."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "local_ip": _get_default_ip(),
        "mac": _get_mac(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu_count": psutil.cpu_count(logical=True),
        "memory_total_mb": int(psutil.virtual_memory().total / 1024 / 1024),
    }

if __name__ == "__main__":
    
    print(json.dumps(get_host_info(), indent=2))
