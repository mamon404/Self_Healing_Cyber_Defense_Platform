# orchestrator/decision_store.py
import sqlite3, os, json, time
DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "orchestrator.db")
os.makedirs(DB_DIR, exist_ok=True)

def _conn():
    c = sqlite3.connect(DB_PATH, timeout=5)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts REAL,
        alert TEXT,
        decision TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        decision_id INTEGER,
        ts REAL,
        action TEXT,
        params TEXT,
        result TEXT
    )
    ''')
    conn.commit()
    conn.close()

def record_decision(alert: dict, decision: dict) -> int:
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO decisions (ts, alert, decision) VALUES (?, ?, ?)",
                (time.time(), json.dumps(alert), json.dumps(decision)))
    did = cur.lastrowid
    conn.commit()
    conn.close()
    return did

def record_action(decision_id: int, action: str, params: dict, result: dict):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO actions (decision_id, ts, action, params, result) VALUES (?, ?, ?, ?, ?)",
                (decision_id, time.time(), action, json.dumps(params), json.dumps(result)))
    conn.commit()
    conn.close()

def recent_decisions(limit=20):
    init_db()
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, ts, alert, decision FROM decisions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    out = []
    for r in rows:
        out.append({"id": r["id"], "ts": r["ts"], "alert": r["alert"], "decision": r["decision"]})
    return out
