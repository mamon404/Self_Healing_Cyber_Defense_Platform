import json
import time
import os
from pathlib import Path
from dotenv import load_dotenv
import requests

# import intel modules
from intel import abuseipdb, otx, threatminer

# load environment variables
load_dotenv()

ALERTS_PATH = os.getenv("ALERTS_PATH", "logs/alerts.jsonl")
ENRICHED_PATH = os.getenv("ENRICHED_PATH", "logs/alerts_enriched.jsonl")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://127.0.0.1:9000/run")

POLL_INTERVAL = 1  # seconds

print("[+] Phase-4 Threat Intelligence Enrichment started")
print(f"[+] Watching {ALERTS_PATH}")

processed_lines = 0


def enrich_alert(alert: dict) -> dict:
    source_ip = alert.get("source_ip")

    enriched = {
        "original": alert,
        "_enriched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    if not source_ip:
        enriched["error"] = "no_source_ip"
        return enriched

    # --- AbuseIPDB ---
    try:
        enriched["abuseipdb"] = abuseipdb.lookup_ip(source_ip)
    except Exception as e:
        enriched["abuseipdb"] = {"status": "error", "error": str(e)}

    # --- OTX ---
    try:
        enriched["otx"] = otx.lookup_ip(source_ip)
    except Exception as e:
        enriched["otx"] = {"status": "error", "error": str(e)}

    # --- ThreatMiner ---
    try:
        enriched["threatminer"] = threatminer.lookup_ip(source_ip)
    except Exception as e:
        enriched["threatminer"] = {"status": "fallback", "error": str(e)}

    return enriched


def send_to_orchestrator(alert: dict):
    """
    Send alert to orchestrator for automated response
    """
    try:
        requests.post(ORCHESTRATOR_URL, json=alert, timeout=2)
    except Exception:
        pass  # silent fail (system continues)


def follow_alerts():
    global processed_lines

    Path(ALERTS_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(ALERTS_PATH).touch(exist_ok=True)
    Path(ENRICHED_PATH).touch(exist_ok=True)

    while True:
        with open(ALERTS_PATH, "r") as f:
            lines = f.readlines()

        new_lines = lines[processed_lines:]
        processed_lines = len(lines)

        for line in new_lines:
            line = line.strip()
            if not line:
                continue

            try:
                alert = json.loads(line)
            except json.JSONDecodeError:
                continue

            # 🔥 Enrich
            enriched = enrich_alert(alert)

            # 🔥 Save enriched data
            with open(ENRICHED_PATH, "a") as out:
                out.write(json.dumps(enriched) + "\n")

            # 🔥 AUTO SEND TO ORCHESTRATOR (THIS IS THE FIX)
            send_to_orchestrator(alert)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    follow_alerts()
