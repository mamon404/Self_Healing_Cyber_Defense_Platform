# response/isolation.py
import subprocess, json, os
LOG = "logs/actions.log"

def _log(record):
    os.makedirs(os.path.dirname(LOG) or ".", exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

def isolate_interface(iface: str = "eth0", dry_run: bool = True) -> dict:
    rec = {"action": "isolate_interface", "iface": iface, "dry_run": dry_run}
    if dry_run:
        rec["result"] = "dry-run"
        _log(rec)
        return rec
    cmd = f"sudo ip link set {iface} down"
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
        rec["result"] = {"rc": proc.returncode, "out": proc.stdout.strip(), "err": proc.stderr.strip()}
    except Exception as e:
        rec["result"] = {"rc": -1, "err": str(e)}
    _log(rec)
    return rec
