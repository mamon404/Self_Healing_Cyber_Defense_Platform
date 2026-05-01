# orchestrator/risk_assessor.py
from datetime import datetime

def calculate_risk(alert: dict) -> dict:
    score = 10
    sev = str(alert.get("severity", "")).lower()
    rid = str(alert.get("rule_id", "")).lower()

    if sev == "critical":
        score += 60
    elif sev == "high":
        score += 40
    elif sev == "medium":
        score += 20
    else:
        score += 5

    weights = {
        "bruteforce": 15,
        "ransom": 25,
        "ddos": 25,
        "portscan": 10,
        "malware": 20,
        "exploit": 20
    }
    for k, w in weights.items():
        if k in rid:
            score += w

    src = alert.get("source_ip") or alert.get("ip") or ""
    if src.startswith(("192.168.", "10.", "172.")):
        score -= 10

    score = max(0, min(100, score))
    if score >= 80:
        level = "critical"
    elif score >= 60:
        level = "high"
    elif score >= 40:
        level = "medium"
    else:
        level = "low"

    return {"score": score, "level": level, "evaluated_at": datetime.utcnow().isoformat() + "Z"}
