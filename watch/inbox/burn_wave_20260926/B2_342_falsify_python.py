#!/usr/bin/env python
"""B2-342 falsifier, python gate: a writer appends an event carrying a fresh
key and mag.shared_surface validate must NAME it.

Throwaway surface only (tmp dir via tempfile); the durable log is never
touched. Exit 0 when the gate names the key (law holds), 1 when it does not
(the gate is broken).
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import mag.shared_surface as ss  # noqa: E402

FRESH_KEY = "unregistered_probe_key_20260926"

def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        inbox = tmp / "inbox"; inbox.mkdir()
        configs = tmp / "configs"; configs.mkdir()
        (inbox / "SHARED_SURFACE_CONTRACT.json").write_text(
            json.dumps({"canonical": {"container": "/board/inbox"}}), encoding="utf-8")
        (inbox / "INDEX.json").write_text(
            json.dumps({"root": "/board/inbox", "items": []}), encoding="utf-8")
        ss.ROOT = tmp; ss.WATCH = tmp / "watch"; ss.INBOX = inbox
        ss.INDEX = inbox / "INDEX.json"
        ss.CONTRACT = inbox / "SHARED_SURFACE_CONTRACT.json"
        ss.WARM_PACK = tmp / "watch" / "WARM_PACK.json"
        ss.EVENTS_LOG = inbox / "index_events.jsonl"
        ss.MALFORMED_BASELINE = configs / "events_malformed_baseline.json"
        ss.EVENTS_KEY_SCHEMA = Path(
            "C:/Users/foste/Documents/projects/local_sovereign_agent/configs/events_key_schema.json")
        (inbox / "index_events.jsonl").write_text(
            json.dumps({"seq": 1, "ts": "2026-09-26T17:40:00Z", "op": "note",
                        "writer": "b2-342-falsifier", "nonce": 1,
                        FRESH_KEY: "appended today, never seen before"}) + "\n",
            encoding="utf-8")
        result = ss.inspect_surface()
        named = [e for e in result["errors"] if e.startswith("NEW event key") and FRESH_KEY in e]
        print("fresh key:", FRESH_KEY)
        print("gate verdict:", "NAMED" if named else "SILENT")
        for e in named:
            print("error:", e)
        print("events_log_keys:", result["events_log_keys"])
        return 0 if named else 1

if __name__ == "__main__":
    raise SystemExit(main())
