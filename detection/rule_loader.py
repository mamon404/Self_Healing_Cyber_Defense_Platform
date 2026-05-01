# detection/rule_loader.py
"""
YAML rule loader for detection rules.

Rules are simple YAML documents. Each rule is a mapping with keys:
- id: unique id string
- description: text
- source: 'logs' | 'packets' | 'metrics' (where rule applies)
- match: for logs: {type: 'regex'|'contains', pattern: '...'} or contains substring
- condition: for packets/metrics rules (custom)
- window_seconds: sliding window in seconds (for counting events)
- threshold: integer threshold
- severity: low|medium|high
"""
import os
import yaml

def load_rules_from_dir(rules_dir):
    rules = []
    if not os.path.isdir(rules_dir):
        return rules
    for fname in sorted(os.listdir(rules_dir)):
        if fname.lower().endswith((".yml", ".yaml")):
            path = os.path.join(rules_dir, fname)
            try:
                with open(path, "r") as fh:
                    docs = yaml.safe_load(fh)
                    if docs is None:
                        continue
                    if isinstance(docs, list):
                        for d in docs:
                            if isinstance(d, dict) and "id" in d:
                                rules.append(d)
                    elif isinstance(docs, dict):
                        if "id" in docs:
                            rules.append(docs)
            except Exception as e:
                # ignore invalid rule files but log to console
                print(f"[rule_loader] failed to load {path}: {e}")
    return rules

