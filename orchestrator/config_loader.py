# orchestrator/config_loader.py
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
CFG_PATH = ROOT / "config" / "config.yaml"

def load_config():
    cfg = {}
    try:
        with open(CFG_PATH, "r") as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:
        cfg = {}
    cfg.setdefault("orchestrator", {})
    cfg["orchestrator"]["host"] = cfg["orchestrator"].get("host", "127.0.0.1")
    cfg["orchestrator"]["port"] = int(os.environ.get("ORCH_PORT", cfg["orchestrator"].get("port", 9000)))
    cfg["orchestrator"]["dry_run_default"] = bool(cfg["orchestrator"].get("dry_run_default", True))
    cfg["orchestrator"]["max_retries"] = int(cfg["orchestrator"].get("max_retries", 3))
    cfg["orchestrator"]["retry_backoff_sec"] = int(cfg["orchestrator"].get("retry_backoff_sec", 2))
    cfg["orchestrator"]["max_parallel"] = int(cfg["orchestrator"].get("max_parallel", 4))
    cfg.setdefault("notifier", {})
    cfg["notifier"]["slack_webhook"] = os.environ.get("SLACK_WEBHOOK", cfg["notifier"].get("slack_webhook", ""))
    cfg.setdefault("actions", {})
    cfg["actions"]["firewall_backend"] = cfg["actions"].get("firewall_backend", "auto")
    return cfg

CFG = load_config()
