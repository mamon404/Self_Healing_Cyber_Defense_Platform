import time
import json
import os
from datetime import datetime

LOG_FILE = "/tmp/test_auth.log"
ALERTS_FILE = "logs/alerts.jsonl"
DETECTION_LOG = "logs/detection.log"

os.makedirs("logs", exist_ok=True)

def parse_line(line):
    if "Failed password" in line:
        return {
            "rule_id": "bruteforce_ssh",
            "description": "Detect repeated failed SSH authentication attempts",
            "raw": line.strip(),
            "severity": "high",
            "source_ip": extract_ip(line),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    return None

def extract_ip(line):
    parts = line.split()
    for p in parts:
        if p.count('.') == 3:
            return p
    return None

def tail_file(file_path):
    with open(file_path, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line

def main():
    print(f"Simulated signature scanner started, tailing: {LOG_FILE}")

    for line in tail_file(LOG_FILE):
        alert = parse_line(line)
        if alert:
            print(f"emitted alert: {alert}")

            # Write to alerts.jsonl
            with open(ALERTS_FILE, "a") as f:
                f.write(json.dumps(alert) + "\n")

            # Write to detection.log (NEW FIX)
            with open(DETECTION_LOG, "a") as f:
                f.write(json.dumps(alert) + "\n")

if __name__ == "__main__":
    main()
