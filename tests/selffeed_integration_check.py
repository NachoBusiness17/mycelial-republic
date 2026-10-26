"""Integration test: selffeed topic appends well-formed JSON to the work queue.

Verifies:
1. t_selffeed() runs without error when hermes is up
2. A new item is appended to state/fuel/stealth_work_queue.jsonl
3. The appended item is valid JSON with id, ask, tier fields
"""
import json
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

WORK_QUEUE = ROOT / "state" / "fuel" / "stealth_work_queue.jsonl"


def main():
    # Ensure hermes is reachable
    hermes_cmd = Path("C:/Users/foste/AppData/Local/hermes/bin/hermes.cmd")
    if not hermes_cmd.is_file():
        print("FAIL: hermes binary not found at", hermes_cmd)
        return 1

    # Record pre-state
    pre_lines = []
    if WORK_QUEUE.is_file():
        pre_lines = [l for l in WORK_QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()]
    pre_count = len(pre_lines)
    pre_ids = []
    for l in pre_lines:
        try:
            pre_ids.append(json.loads(l)["id"])
        except (json.JSONDecodeError, KeyError):
            pass
    print(f"PRE: {pre_count} lines in queue, last id: {pre_ids[-1] if pre_ids else '(none)'}")

    # Run t_selffeed
    from tools.stealth_driver import t_selffeed
    result = t_selffeed()
    print(f"t_selffeed() returned: {result}")

    # Post-state
    post_lines = [l for l in WORK_QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()]
    post_count = len(post_lines)
    print(f"POST: {post_count} lines in queue")

    if post_count <= pre_count:
        print("FAIL: no new line appended to work queue")
        return 1

    # Parse the newly appended line
    new_line = post_lines[-1]
    try:
        item = json.loads(new_line)
    except json.JSONDecodeError as e:
        print(f"FAIL: appended line is not valid JSON: {e}")
        print(f"  line: {new_line[:200]}")
        return 1

    # Validate required fields
    required = {"id", "ask", "tier"}
    missing = required - set(item.keys())
    if missing:
        print(f"FAIL: appended item missing fields: {missing}")
        print(f"  item: {json.dumps(item, indent=2)[:500]}")
        return 1

    # Validate field types / constraints
    if not isinstance(item["id"], str) or not item["id"]:
        print(f"FAIL: 'id' is not a non-empty string: {item['id']!r}")
        return 1
    if not isinstance(item["ask"], str) or len(item["ask"]) < 10:
        print(f"FAIL: 'ask' too short or not a string: {item.get('ask')!r}")
        return 1
    if item.get("tier") != "free":
        print(f"FAIL: 'tier' expected 'free', got {item.get('tier')!r}")
        return 1

    print("PASS: selffeed appended well-formed JSON item:")
    print(f"  id:    {item['id']}")
    print(f"  tier:  {item['tier']}")
    print(f"  ask:   {item['ask'][:80]}...")
    print(f"  status: {item.get('status', '(missing)')}")
    print(f"  selffed_ts: {item.get('selffed_ts', '(missing)')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())