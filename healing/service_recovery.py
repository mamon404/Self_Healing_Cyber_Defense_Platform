# healing/service_recovery.py
import time
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import subprocess

# try to import snapshot collector (separate module)
try:
    from healing import snapshot as snapshot_mod
except Exception:
    snapshot_mod = None

def _run(cmd, timeout=30):
    """
    Helper to run shell commands safely.
    Returns dict with rc, out, err.
    """
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"rc": p.returncode, "out": p.stdout.strip(), "err": p.stderr.strip()}
    except Exception as e:
        return {"rc": -1, "out": "", "err": str(e)}

def restart_service(service, dry_run=True):
    """
    Restart a service. If dry_run True -> simulate.
    Returns structured dict suitable for orchestrator logs.
    """
    if dry_run:
        return {"action": "restart_service", "dry_run": True, "result": "dry-run"}

    res = _run(f"sudo systemctl restart {service}")
    # small wait then check active state
    time.sleep(1.5)
    status = _run(f"sudo systemctl is-active {service}")
    return {"action": "restart_service", "dry_run": False, "result": {"rc": res["rc"], "out": res.get("out",""), "err": res.get("err",""), "active": status.get("out","")}}

def collect_snapshot(tag="snapshot", dry_run=True, services=None, extra_files=None):
    """
    Unified collect_snapshot used by orchestrator.
    - If dry_run True -> returns simulated response
    - If dry_run False -> uses healing.snapshot.collect_snapshot (if available) to create a snapshot file and returns its path.
    Returns dict in the shape expected by playbook_runner.
    """
    # dry-run behaviour
    if dry_run:
        # return a lightweight simulated result so orchestrator can continue
        return {"action": "collect_snapshot", "dry_run": True, "result": "dry-run"}

    # if snapshot module unavailable, return error
    if snapshot_mod is None:
        return {"action": "collect_snapshot", "dry_run": False, "ok": False, "error": "snapshot_module_missing"}

    try:
        # call actual snapshot collector; allow passing services/extra_files
        out_path = snapshot_mod.collect_snapshot(tag=tag, services=services, extra_files=extra_files)
        return {"action": "collect_snapshot", "dry_run": False, "result": {"ok": True, "outfile": out_path}}
    except Exception as e:
        return {"action": "collect_snapshot", "dry_run": False, "ok": False, "error": str(e)}
