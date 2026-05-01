# healing/rollback.py
import json
import subprocess
from pathlib import Path

def _run(cmd, timeout=30):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"rc": p.returncode, "out": p.stdout.strip(), "err": p.stderr.strip()}
    except Exception as e:
        return {"rc": -1, "out": "", "err": str(e)}

def restore_nft_from_snapshot(snapshot_file):
    """Try to restore nft rules from snapshot data (safe-mode)."""
    p = Path(snapshot_file)
    if not p.exists():
        return {"ok": False, "error": "snapshot_missing"}

    data = json.loads(p.read_text())
    nft = data.get("nft_ruleset", {})
    if nft.get("rc") != 0 or not nft.get("out"):
        return {"ok": False, "error": "no_nft_in_snapshot"}

    # SAFE: write ruleset to a temp file and restore via nft -f
    tmpfile = "/tmp/selfheal_nft_restore.rules"
    with open(tmpfile, "w") as fh:
        fh.write(nft.get("out"))

    res = _run(f"sudo nft -f {tmpfile}", timeout=60)
    return {"ok": res.get("rc")==0, "result": res}

def restore_file(snapshot_file, path_to_restore, dest_path):
    p = Path(snapshot_file)
    if not p.exists():
        return {"ok": False, "error": "snapshot_missing"}
    data = json.loads(p.read_text())
    files = data.get("files", {})
    if path_to_restore not in files:
        return {"ok": False, "error": "file_not_in_snapshot"}
    content = files[path_to_restore]
    try:
        with open(dest_path, "w") as fh:
            fh.write(content)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

