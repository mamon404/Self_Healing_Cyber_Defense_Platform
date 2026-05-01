import time
import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    return {}

config = load_config()

LOG_FILE = config.get("log_file", "/var/log/auth.log")


def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line


def start_log_collector():
    print(f"[collector] reading log file: {LOG_FILE}")

    if not os.path.exists(LOG_FILE):
        print(f"[ERROR] Log file not found: {LOG_FILE}")
        return

    with open(LOG_FILE, "r") as f:
        for line in follow(f):
            yield line
