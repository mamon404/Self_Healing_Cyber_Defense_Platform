# response/firewall_manager.py
import shutil, subprocess, json, os
LOG = "logs/actions.log"

def _log(record: dict):
    os.makedirs(os.path.dirname(LOG) or ".", exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

def _run_cmd(cmd: str, timeout: int = 20):
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"rc": proc.returncode, "out": proc.stdout.strip(), "err": proc.stderr.strip()}
    except Exception as e:
        return {"rc": -1, "err": str(e)}

def _detect_backend(prefer: str = "auto") -> str:
    if prefer == "iptables":
        return "iptables"
    if prefer == "nft":
        return "nft"
    if shutil.which("nft"):
        return "nft"
    if shutil.which("iptables"):
        return "iptables"
    return "none"

def block_ip(ip: str, dry_run: bool = True, comment: str = "auto_block") -> dict:
    backend = _detect_backend()
    rec = {"action": "block_ip", "ip": ip, "dry_run": dry_run, "backend": backend}
    if dry_run or backend == "none":
        rec["result"] = "dry-run"
        _log(rec)
        return rec
    if backend == "iptables":
        cmd = f"sudo iptables -I INPUT -s {ip} -j DROP -m comment --comment \"{comment}\""
    else:
        cmd = f"sudo nft add rule inet filter input ip saddr {ip} counter drop"
    out = _run_cmd(cmd)
    rec["cmd"] = cmd
    rec["result"] = out
    _log(rec)
    return rec

def unblock_ip(ip: str, dry_run: bool = True) -> dict:
    backend = _detect_backend()
    rec = {"action": "unblock_ip", "ip": ip, "dry_run": dry_run, "backend": backend}
    if dry_run or backend == "none":
        rec["result"] = "dry-run"
        _log(rec)
        return rec
    if backend == "iptables":
        cmd = f"sudo iptables -D INPUT -s {ip} -j DROP || true"
    else:
        cmd = f"sudo nft delete rule inet filter input ip saddr {ip} counter drop || true"
    out = _run_cmd(cmd)
    rec["cmd"] = cmd
    rec["result"] = out
    _log(rec)
    return rec
