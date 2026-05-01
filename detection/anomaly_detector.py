# detection/anomaly_detector.py
"""
Lightweight anomaly detection using rolling-window statistics (mean/std).
- Samples system metrics via monitoring.system_monitor.get_system_metrics()
- Maintains rolling windows for CPU and memory and computes z-score
- Fires alerts when z-score crosses configured threshold
"""
import time
from collections import deque
from detection.alerting import alert
from monitoring.system_monitor import get_system_metrics
from datetime import datetime, timezone

def _now_iso():
    return datetime.now(timezone.utc).isoformat()

class RollingWindow:
    def __init__(self, maxlen=12):
        self.maxlen = maxlen
        self.q = deque(maxlen=maxlen)

    def add(self, v):
        try:
            self.q.append(float(v))
        except Exception:
            pass

    def mean(self):
        if not self.q:
            return 0.0
        return sum(self.q) / len(self.q)

    def std(self):
        if not self.q:
            return 0.0
        m = self.mean()
        return (sum((x - m) ** 2 for x in self.q) / len(self.q)) ** 0.5

class AnomalyDetector:
    def __init__(self, sample_interval=5, window_seconds=60, cpu_z_threshold=3.0, mem_z_threshold=3.5):
        # compute window size in samples
        samples = max(3, int(window_seconds / sample_interval))
        self.cpu_win = RollingWindow(maxlen=samples)
        self.mem_win = RollingWindow(maxlen=samples)
        self.sample_interval = sample_interval
        self.cpu_z_threshold = cpu_z_threshold
        self.mem_z_threshold = mem_z_threshold

    def sample(self):
        m = get_system_metrics()
        cpu = float(m.get("cpu_percent", 0.0))
        mem = float(m.get("memory_percent", 0.0))
        self.cpu_win.add(cpu)
        self.mem_win.add(mem)
        # compute z-scores
        cpu_std = self.cpu_win.std()
        mem_std = self.mem_win.std()
        cpu_z = (cpu - self.cpu_win.mean()) / cpu_std if cpu_std > 0 else 0.0
        mem_z = (mem - self.mem_win.mean()) / mem_std if mem_std > 0 else 0.0

        if cpu_z >= self.cpu_z_threshold:
            alert({
                "type": "anomaly",
                "metric": "cpu",
                "value": cpu,
                "zscore": cpu_z,
                "severity": "high",
                "timestamp": _now_iso()
            })
        if mem_z >= self.mem_z_threshold:
            alert({
                "type": "anomaly",
                "metric": "memory",
                "value": mem,
                "zscore": mem_z,
                "severity": "medium",
                "timestamp": _now_iso()
            })

    def run(self, iterations=None):
        i = 0
        while True:
            self.sample()
            time.sleep(self.sample_interval)
            i += 1
            if iterations and i >= iterations:
                break

