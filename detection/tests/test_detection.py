# detection/tests/test_detection.py
import os
import json
import time
from detection.rule_loader import load_rules_from_dir
from detection.signature_scanner import SignatureScanner

def test_load_rules(tmp_path):
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    rfile = rules_dir / "r1.yaml"
    rfile.write_text("""
- id: t1
  description: test rule
  source: logs
  match:
    type: contains
    substring: "HELLO_TEST"
  window_seconds: 60
  threshold: 1
""")
    rules = load_rules_from_dir(str(rules_dir))
    assert len(rules) == 1
    assert rules[0]["id"] == "t1"

def test_signature_scan_basic(tmp_path):
    # create rule and log, then scan
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    (rules_dir / "r1.yaml").write_text("""
- id: tlog
  description: test
  source: logs
  match:
    type: regex
    pattern: "FAKE_FAIL"
  window_seconds: 60
  threshold: 1
""")
    log_file = tmp_path / "auth.log"
    log_file.write_text("normal\nFAKE_FAIL occurred\n")
    sc = SignatureScanner(rules_dir=str(rules_dir), logs_dir=str(tmp_path))
    hits = sc.scan_log_once(str(log_file))
    assert any(h[0]["id"] == "tlog" for h in hits)

