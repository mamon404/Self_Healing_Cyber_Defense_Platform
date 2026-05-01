# monitoring/metrics_exporter.py
import os, json, time
from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CollectorRegistry
from monitoring.system_monitor import get_system_metrics
from monitoring.host_info import get_host_info

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
STATS_FILE = os.path.join(LOG_DIR, "packet_stats.json")

app = Flask(__name__)

registry = CollectorRegistry()

cpu_gauge = Gauge("system_cpu_percent", "System CPU percent", registry=registry)
mem_gauge = Gauge("system_memory_percent", "System memory percent", registry=registry)
packet_total = Gauge("sniffer_total_packets", "Total packets seen by sniffer", registry=registry)
packet_proto = Gauge("sniffer_protocol_packets", "Packets count by protocol", ["proto"], registry=registry)
host_info_gauge = Gauge("system_host_info", "Static host identity", ["hostname", "local_ip", "os"], registry=registry)

@app.route("/metrics")
def metrics():
    m = get_system_metrics()
    cpu_gauge.set(m["cpu_percent"])
    mem_gauge.set(m["memory_percent"])

    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE) as f:
                stats = json.load(f)
            packet_total.set(stats.get("total_packets", 0))
            for proto, cnt in stats.get("protocols", {}).items():
                packet_proto.labels(proto=proto).set(cnt)
        except Exception:
            pass

    h = get_host_info()
    host_info_gauge.labels(hostname=h["hostname"], local_ip=h["local_ip"], os=h["os"]).set(1)

    return Response(generate_latest(registry), mimetype="text/plain")

if __name__ == "__main__":
    app.run(port=8000)
