# dashboard/app.py
from flask import Flask, render_template, jsonify
import os, sys

# monitoring modules ঠিকঠাক import করার জন্য
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from monitoring.system_monitor import get_system_metrics
from monitoring.host_info import get_host_info

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/metrics")
def metrics():
    """System metrics + host info return করবে JSON আকারে"""
    return jsonify({
        "metrics": get_system_metrics(),
        "host": get_host_info()
    })

if __name__ == "__main__":
    app.run(debug=True)
