# tests/unit/test_monitoring.py
from monitoring.system_monitor import get_system_metrics

def test_get_system_metrics_keys():
    m = get_system_metrics()
    assert isinstance(m, dict)
    assert "cpu_percent" in m and "memory_percent" in m

