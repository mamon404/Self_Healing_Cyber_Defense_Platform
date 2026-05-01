import re
from detection.alerting import emit_alert

# simple brute force rule
PATTERN = re.compile(r"Failed password")

def extract_ip(line: str):
    match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
    return match.group(1) if match else None


def process_line(line: str):
    if PATTERN.search(line):
        ip = extract_ip(line)

        alert = {
            "rule_id": "bruteforce_ssh",
            "description": "Detect repeated failed SSH authentication attempts",
            "raw": line.strip(),
            "severity": "high",
            "source_ip": ip
        }

        emit_alert(alert)
