# healing/snapshot.py
import os, time, json, socket, subprocess
from pathlib import Path
from datetime import datetime, timezone

SNAP_DIR = Path("logs/snapshots")
SNAP_DIR.mkdir(parents=True, exist_ok=True)

def _run(cmd, timeout=10):
    try:
        out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"rc": out.returncode, "out": out.stdout.strip(), "err": out.stderr.strip()}
    except Exception as e:
        return {"rc": -1, "out": "", "err": str(e)}

def collect_snapshot(tag="snapshot", services=None, extra_files=None):
    ts = int(time.time())
    snapshot = {
        "tag": tag,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "whoami": _run("whoami"),
        "process_list": _run("ps aux --no-heading"),
        "nft_ruleset": _run("sudo nft list ruleset"),
        "ip_addr": _run("ip -4 addr show"),
        "routes": _run("ip route show"),
    }

    snapshot["services"] = {}
    if services:
        for s in services:
            snapshot["services"][s] = {
                "systemctl_status": _run(f"sudo systemctl status {s} --no-pager -l"),
                "journal": _run(f"sudo journalctl -u {s} -n 200 --no-pager"),
            }

    snapshot["files"] = {}
    if extra_files:
        for f in extra_files:
            try:
                with open(f, "r", errors="ignore") as fh:
                    snapshot["files"][f] = fh.read()
            except Exception as e:
                snapshot["files"][f] = f"ERROR: {e}"

    outfile = SNAP_DIR / f"snapshot_{tag}_{ts}.json"
    with open(outfile, "w") as fh:
        json.dump(snapshot, fh, indent=2)
    return str(outfile)
