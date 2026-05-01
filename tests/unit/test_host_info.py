# tests/unit/test_host_info.py
from monitoring.host_info import get_host_info

def test_get_host_info_contains_fields():
    info = get_host_info()
    assert "hostname" in info
    assert "local_ip" in info
    assert "mac" in info
    assert "os" in info
    assert isinstance(info["cpu_count"], int)
    assert isinstance(info["memory_total_mb"], int)

