# orchestrator/policy_engine.py
from orchestrator.risk_assessor import calculate_risk

def is_whitelisted(ip: str) -> bool:
    if not ip:
        return False
    if ip.startswith(("192.168.", "10.", "172.")):
        return True
    return False

def policy_for_alert(alert: dict) -> dict:
    risk = calculate_risk(alert)
    decision = {"trigger": False, "approval_required": False, "reason": "", "risk": risk}
    src = alert.get("source_ip") or alert.get("ip")
    if is_whitelisted(src):
        decision["trigger"] = False
        decision["reason"] = "source whitelisted"
        return decision

    lvl = risk["level"]
    decision["reason"] = f"risk {lvl} score {risk['score']}"
    if lvl in ("high", "critical"):
        decision["trigger"] = True
        decision["approval_required"] = (lvl == "critical")
    else:
        decision["trigger"] = False
    return decision
