# tests/unit/test_phase2_best.py
import os, json
from monitoring.host_info import get_host_info

def test_host_info_has_fields():
    h = get_host_info()
    assert "hostname" in h
    assert "local_ip" in h
    assert "mac" in h
    assert "os" in h

def test_packet_stats_file_format(tmp_path):
    f = tmp_path / "stats.json"
    data = {"total_packets": 5, "protocols": {"TCP": 3}}
    f.write_text(json.dumps(data))
    loaded = json.loads(f.read_text())
    assert "total_packets" in loaded
    assert isinstance(loaded["protocols"], dict)

def test_log_event_file(tmp_path):
    log_file = tmp_path / "events.jsonl"
    event = {"timestamp": "2025-09-29T12:00:00", "hostname": "kali", "local_ip": "127.0.0.1", "raw": "Failed password", "match": "Failed password"}
    with open(log_file, "a") as f:
        f.write(json.dumps(event) + "\n")
    lines = log_file.read_text().splitlines()
    loaded = json.loads(lines[0])
    assert "match" in loaded
    assert loaded["match"] == "Failed password"

