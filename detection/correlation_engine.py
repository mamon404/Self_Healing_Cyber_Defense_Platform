# detection/correlation_engine.py
"""
CorrelationEngine:
- Accepts events (dict) via ingest_event
- Keeps recent event window in memory
- Applies simple correlation rules (example included)
- Emits correlation alerts via detection.alerting.alert
"""
import time
from collections import deque
from detection.alerting import alert
from datetime import datetime, timezone

def _now_iso():
    return datetime.now(timezone.utc).isoformat()

class CorrelationEngine:
    def __init__(self, lookback_seconds=300):
        self.lookback = lookback_seconds
        self.events = deque()

    def _epoch(self, t):
        # normalize timestamp (accept iso string or epoch float)
        try:
            # try float
            return float(t)
        except Exception:
            try:
                # parse iso
                import dateutil.parser as dp
                return dp.parse(t).timestamp()
            except Exception:
                return time.time()

    def ingest_event(self, evt):
        # event must be dict; ensure _ts epoch present
        ts = evt.get("timestamp")
        if ts is None:
            ts_epoch = time.time()
        else:
            ts_epoch = self._epoch(ts)
        evt_copy = dict(evt)
        evt_copy["_ts"] = ts_epoch
        self.events.append(evt_copy)
        self._prune()
        self._evaluate_correlations()

    def _prune(self):
        cutoff = time.time() - self.lookback
        while self.events and self.events[0]["_ts"] < cutoff:
            self.events.popleft()

    def _evaluate_correlations(self):
        # Example correlation: many failed password events in lookback -> emit alert
        failed = [e for e in self.events if (e.get("match") and "failed password" in e.get("match","").lower()) or ("Failed password" in e.get("raw",""))]
        if len(failed) >= 5:
            alert({
                "type": "correlation",
                "name": "multiple_failed_passwords",
                "count": len(failed),
                "severity": "high",
                "description": f"{len(failed)} failed password events in last {self.lookback} seconds",
                "timestamp": _now_iso()
            })
            # remove these failed events to avoid repeated alerts
            for e in failed:
                try:
                    self.events.remove(e)
                except ValueError:
                    pass

