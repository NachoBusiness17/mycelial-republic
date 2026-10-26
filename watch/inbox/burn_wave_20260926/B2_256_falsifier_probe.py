#!/usr/bin/env python
"""B2-256 falsifier probe: a refactor that resurrects "3rd Marine" as
2018-03-03 must fail verifier check7.

Simulates the coherent refactor the brief names: re-adds the exact B2-243
misdate row for id 894571 (copied verbatim from the pre-guard snapshot
B2_243_ledger_before.jsonl) to a TEMP COPY of the ledger and patches the
extractor to emit that row again, as the generator would after a guard
regression. Checks 1 through 6 stay green by construction, so only the
check7 pin can catch the resurrection. The live ledger is never modified;
its sha256 is re-verified after the run.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_256_falsifier_probe.py
Exits with the verifier's exit code (0 = pin did NOT fire, 1 = pin fired),
2 if the live file was disturbed.
"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WAVE = ROOT / "watch" / "inbox" / "burn_wave_20260926"
LIVE = ROOT / "watch" / "inbox" / "qdrop_export" / "q_caption_ledger.jsonl"
GEN = ROOT / "scripts" / "the50_t21_q_caption_ledger.py"
VER = ROOT / "scripts" / "the50_t21_q_caption_ledger_verify.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    live_bytes = LIVE.read_bytes()
    assert live_bytes.endswith(b"\n"), "live ledger must end with a newline"
    live_sha = hashlib.sha256(live_bytes).hexdigest()
    resurrection = None
    for line in (WAVE / "B2_243_ledger_before.jsonl").read_text(
        encoding="utf-8"
    ).splitlines():
        r = json.loads(line)
        if r["id"] == "894571" and r["date"] == "2018-03-03":
            resurrection = r
    if resurrection is None:
        print("FAIL: resurrection row not found in B2_243_ledger_before.jsonl")
        return 2

    fd, tmp_name = tempfile.mkstemp(suffix=".jsonl")
    os.close(fd)  # Windows: the open fd blocks unlink at cleanup
    tmp = Path(tmp_name)
    tmp.write_bytes(
        live_bytes
        + json.dumps(resurrection, ensure_ascii=False).encode("utf-8")
        + b"\n"
    )

    ver = load("b256_ver", VER)
    orig_extract = ver.extract

    def patched_extract(drop):
        yield from orig_extract(drop)
        if str(drop.get("id")) == "894571":
            yield (resurrection["date"], resurrection["claim"],
                   resurrection["confidence"])

    ver.extract = patched_extract
    ver.OUT = tmp
    rc = ver.main()
    out_sha = hashlib.sha256(LIVE.read_bytes()).hexdigest()
    print(f"live ledger untouched after probe: {out_sha == live_sha} "
          f"({live_sha[:12]})")
    tmp.unlink()
    return rc if out_sha == live_sha else 2


if __name__ == "__main__":
    sys.exit(main())
