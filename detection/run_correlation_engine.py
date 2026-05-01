# detection/run_correlation_engine.py
"""
Example runner that reads events from logs/log_events.jsonl and feeds them into the correlation engine.
In real deployment you would feed events live as they occur.
"""
import os
import time
import json
from detection.correlation_engine import CorrelationEngine

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVENTS_FILE = os.path.join(ROOT, "logs", "log_events.jsonl")

def main(poll_interval=5):
    engine = CorrelationEngine(lookback_seconds=300)
    print("[correlation] starting. watching", EVENTS_FILE)
    last_pos = 0
    try:
        while True:
            if os.path.exists(EVENTS_FILE):
                with open(EVENTS_FILE, "r") as fh:
                    fh.seek(last_pos)
                    for line in fh:
                        try:
                            evt = json.loads(line)
                            engine.ingest_event(evt)
                        except Exception:
                            pass
                    last_pos = fh.tell()
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("[correlation] stopped")

if __name__ == "__main__":
    main()

