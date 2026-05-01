import os, requests
from dotenv import load_dotenv
load_dotenv()
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
def send_to_slack(text: str):
    if not SLACK_WEBHOOK:
        return {"status":"no_webhook"}
    payload = {"text": text}
    try:
        r = requests.post(SLACK_WEBHOOK, json=payload, timeout=10)
        return {"status": "ok" if r.status_code in (200,204) else "error", "code": r.status_code, "text": r.text}
    except Exception as e:
        return {"status":"error","exception": str(e)}
