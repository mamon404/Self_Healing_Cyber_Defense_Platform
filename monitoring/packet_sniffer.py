#!/usr/bin/env python3
# monitoring/packet_sniffer.py
import json
import time
from datetime import datetime
from pathlib import Path
from threading import Lock, Thread
from scapy.all import sniff, Ether, IP, TCP, UDP, ICMP, ARP, conf

OUTFILE = Path("logs/packet_stats.json")
LOCK = Lock()

# counters
stats = {
    "total_packets": 0,
    "protocols": {
        "TCP": 0,
        "UDP": 0,
        "ICMP": 0,
        "ARP": 0,
        "IP": 0,
        "OTHER": 0
    },
    "last_update": None
}

def persist():
    with LOCK:
        out = dict(stats)
        out["last_update"] = datetime.utcnow().isoformat()
        OUTFILE.parent.mkdir(parents=True, exist_ok=True)
        OUTFILE.write_text(json.dumps(out))
        # keep small sleep to avoid busy-write
def pkt_handler(pkt):
    with LOCK:
        stats["total_packets"] += 1
        # detect ARP separately (it's not IP)
        if pkt.haslayer(ARP):
            stats["protocols"]["ARP"] += 1
            return
        if pkt.haslayer(IP):
            stats["protocols"]["IP"] += 1
            # deeper protocols
            if pkt.haslayer(TCP):
                stats["protocols"]["TCP"] += 1
            elif pkt.haslayer(UDP):
                stats["protocols"]["UDP"] += 1
            elif pkt.haslayer(ICMP):
                stats["protocols"]["ICMP"] += 1
            else:
                stats["protocols"]["OTHER"] += 1
        else:
            stats["protocols"]["OTHER"] += 1

def periodic_persist(interval=2.0):
    while True:
        time.sleep(interval)
        persist()

def main(iface=None, promisc=True):
    print("Starting packet sniffer, iface:", iface or conf.iface)
    # start persister
    t = Thread(target=periodic_persist, args=(2.0,), daemon=True)
    t.start()
    # start sniffing
    sniff(iface=iface, prn=pkt_handler, store=False, promisc=promisc)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--iface", default=None, help="interface to sniff (default scapy conf.iface)")
    p.add_argument("--promisc", action="store_true", help="enable promisc")
    args = p.parse_args()
    try:
        main(iface=args.iface, promisc=args.promisc)
    except KeyboardInterrupt:
        print("stopped")
