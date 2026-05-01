import json
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_FILE = os.path.join(BASE_DIR, "logs", "detection.log")
ALERTS_FILE = os.path.join(BASE_DIR, "logs", "alerts.jsonl")


def ensure_logs():
    os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)


def write_log(data: dict):
    ensure_logs()

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
        f.flush()

    with open(ALERTS_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
        f.flush()


def emit_alert(alert: dict):
    alert["timestamp"] = alert.get("timestamp") or time.strftime("%Y-%m-%dT%H:%M:%SZ")

    print("emitted alert:", alert)

    write_log(alert)
