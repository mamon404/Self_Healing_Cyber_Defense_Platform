# response/notifier.py
import os, json, time, requests
LOG = "logs/actions.log"

def _log(record):
    os.makedirs(os.path.dirname(LOG) or ".", exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

def send_to_slack(text: str, webhook: str = None) -> dict:
    wh = webhook or os.environ.get("SLACK_WEBHOOK", "")
    if not wh:
        return {"status": "no_webhook"}
    payload = {"text": text}
    try:
        r = requests.post(wh, json=payload, timeout=5)
        return {"status": "ok", "code": r.status_code, "text": r.text}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def send_notification(text: str) -> dict:
    res = send_to_slack(text)
    if res.get("status") == "no_webhook":
        print("[NOTIFY]", text)
        res = {"status": "local_print", "ts": time.time()}
    _log({"action": "notify", "text": text, "result": res, "ts": time.time()})
    return res
