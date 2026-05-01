# orchestrator/playbook_runner.py

import asyncio
import yaml
import os
import json
import time
import logging
import functools
from pathlib import Path

from orchestrator import policy_engine, decision_store, config_loader
from response import firewall_manager, isolation, notifier
from healing import service_recovery

LOG_FILE = "logs/actions.log"
PLAYBOOK_DIR = "playbooks"
CFG = config_loader.CFG

MAX_PARALLEL = CFG.get("orchestrator", {}).get("max_parallel", 4)
DEFAULT_RETRIES = CFG.get("orchestrator", {}).get("max_retries", 3)
DEFAULT_BACKOFF = CFG.get("orchestrator", {}).get("retry_backoff_sec", 2)

logging.basicConfig(level=logging.INFO)

# -------------------- helpers --------------------

def _log(obj: dict):
    os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(obj) + "\n")


def _load_playbook(alert: dict):
    """
    Load matching playbook based on rule_id.
    If nothing matches, return a safe default playbook.
    """
    rule_id = str(alert.get("rule_id", "")).lower()

    for pb_file in Path(PLAYBOOK_DIR).glob("*.yaml"):
        try:
            pb = yaml.safe_load(pb_file.read_text())
            if not pb:
                continue

            conditions = pb.get("conditions", {})
            rule_contains = str(conditions.get("rule_contains", "")).lower()

            if rule_contains and rule_contains in rule_id:
                return pb
        except Exception as e:
            logging.error(f"Playbook parse error {pb_file}: {e}")

    # 🔐 SAFE FALLBACK (VERY IMPORTANT)
    return {
        "name": "default_fallback",
        "actions": ["notify_admin"]
    }


def _prepare_actions(pb: dict, alert: dict):
    actions = []

    for item in pb.get("actions", []):
        if isinstance(item, dict):
            for action, params in item.items():
                params = params or {}
                if action == "block_ip":
                    params.setdefault("ip", alert.get("source_ip"))
                actions.append((action, params))
        else:
            if item == "block_ip":
                actions.append(("block_ip", {"ip": alert.get("source_ip")}))
            elif item == "collect_snapshot":
                actions.append(("collect_snapshot", {"tag": alert.get("rule_id", "event")}))
            elif item == "restart_service":
                actions.append(("restart_service", {"service": "ssh"}))
            elif item == "notify_admin":
                actions.append(("notify_admin", {"text": f"Alert {alert.get('rule_id')} from {alert.get('source_ip')}"}))
            else:
                actions.append((item, {}))

    return actions


def _dispatch_sync(action: str, **params):
    if action == "block_ip":
        return firewall_manager.block_ip(params.get("ip"), dry_run=params.get("dry_run", True))
    if action == "unblock_ip":
        return firewall_manager.unblock_ip(params.get("ip"), dry_run=params.get("dry_run", True))
    if action == "collect_snapshot":
        return service_recovery.collect_snapshot(params.get("tag", "snapshot"), dry_run=params.get("dry_run", True))
    if action == "restart_service":
        return service_recovery.restart_service(params.get("service", "ssh"), dry_run=params.get("dry_run", True))
    if action == "notify_admin":
        return notifier.send_notification(params.get("text", "No message"))
    return {"error": f"unknown_action:{action}"}


async def _run_with_retries(func, kwargs, retries, backoff):
    attempt = 0
    while True:
        try:
            loop = asyncio.get_running_loop()
            call = functools.partial(func, **kwargs)
            result = await loop.run_in_executor(None, call)
            return {"ok": True, "result": result, "attempts": attempt + 1}
        except Exception as e:
            attempt += 1
            if attempt >= retries:
                return {"ok": False, "error": str(e), "attempts": attempt}
            await asyncio.sleep(backoff * attempt)

# -------------------- MAIN --------------------

async def run_playbook_for_alert(alert: dict, dry_run: bool = True):
    policy = policy_engine.policy_for_alert(alert)
    decision_id = decision_store.record_decision(alert, policy)

    _log({"decision_id": decision_id, "event": "received", "alert": alert, "policy": policy})

    if not policy.get("trigger"):
        return {"status": "skipped", "reason": policy.get("reason")}

    playbook = _load_playbook(alert)
    actions = _prepare_actions(playbook, alert)

    results = []
    for action, params in actions:
        params["dry_run"] = dry_run
        res = await _run_with_retries(
            _dispatch_sync,
            {"action": action, **params},
            DEFAULT_RETRIES,
            DEFAULT_BACKOFF
        )
        decision_store.record_action(decision_id, action, params, res)
        _log({"decision_id": decision_id, "action": action, "params": params, "result": res})
        results.append({action: res})

        if not res.get("ok"):
            return {"status": "failed", "results": results}

    _log({"decision_id": decision_id, "status": "ok", "results": results})
    return {"status": "ok", "results": results}
