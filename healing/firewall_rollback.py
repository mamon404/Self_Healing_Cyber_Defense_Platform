# healing/firewall_rollback.py
import subprocess
import time

def unblock_ip(ip: str, dry_run: bool = True):
    cmd = f"sudo nft delete rule inet filter input ip saddr {ip}"
    if dry_run:
        return {
            "action": "unblock_ip",
            "ip": ip,
            "dry_run": True,
            "result": "dry-run"
        }
    try:
        p = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=20
        )
        return {
            "action": "unblock_ip",
            "ip": ip,
            "dry_run": False,
            "result": {
                "rc": p.returncode,
                "out": p.stdout.strip(),
                "err": p.stderr.strip()
            }
        }
    except Exception as e:
        return {"action": "unblock_ip", "error": str(e)}

