# orchestrator/api.py
from flask import Flask, request, jsonify
import asyncio, os, json
from orchestrator import decision_store, config_loader
from orchestrator.playbook_runner import run_playbook_for_alert

app = Flask(__name__)
CFG = config_loader.CFG

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "orchestrator_advanced"})

@app.route("/run", methods=["POST"])
def run_route():
    alert = request.get_json()
    if not alert:
        return jsonify({"error": "no_json"}), 400
    dry_cfg = CFG.get("orchestrator", {}).get("dry_run_default", True)
    dry = request.args.get("dry", str(dry_cfg)).lower() in ("1", "true", "yes")
    res = asyncio.run(run_playbook_for_alert(alert, dry_run=dry))
    return jsonify(res)

@app.route("/decisions", methods=["GET"])
def decisions():
    rows = decision_store.recent_decisions(limit=50)
    out = []
    for r in rows:
        try:
            r['alert'] = json.loads(r['alert'])
            r['decision'] = json.loads(r['decision'])
        except Exception:
            pass
        out.append(r)
    return jsonify(out)

if __name__ == "__main__":
    port = CFG.get("orchestrator", {}).get("port", 9000)
    host = CFG.get("orchestrator", {}).get("host", "127.0.0.1")
    app.run(host=host, port=port, debug=False)
