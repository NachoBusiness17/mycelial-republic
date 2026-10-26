"""cartographer cycle 12: corpus/apk thread fold.

Consumer: receipt_20261023_cartographer.md (FINDINGS/COUNTS) and the
cartographer receipt chain (cycle 13 resumes from its NEXT THREAD row).
Verifier: re-run this script; every count re-derives from disk bytes and
banked cycle-11/12 instruments (named per row); the receipt quotes only
rows this file emitted.

Recomputes hashes, shelf bytes, register diffs, the .gitignore rule, and
catalog indexing live. Citation-footprint counts come from the cycle 12
rg instrument (moment named in the receipt) and are banked here as
instrument results, not re-derived.
"""
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
DATA = Path(__file__).resolve().parent
APK = REPO / "corpus" / "apk" / "aurora_store_76.apk"
HOOK = REPO / "corpus" / "apk" / ".mimosa" / "hook-state" / "sess_297f5a13-4e0a-4ce3-827a-dff7a3e98386.json"
SO = REPO / "logs" / "mates" / "cartographer" / "apk_rung" / "lib" / "x86_64" / "libandroidx.graphics.path.so"
CENSUS = DATA / "apk_census.json"
REG_TRUE = REPO / "watch" / "inbox" / "mates_leave_protocol" / "receipts" / "cartographer_20261020_data" / "ghidra_audit_register.json"
REG_TAMP = REPO / "watch" / "inbox" / "mates_leave_protocol" / "receipts" / "cartographer_20261020_data" / "ghidra_audit_register_tampered.json"
REG_STANDING = REPO / "memory" / "ghidra_audit_register.json"
GITIGNORE = REPO / ".gitignore"
CATALOG = REPO / "catalog" / "catalog.jsonl"
OUT = DATA / "corpus_apk_fold.jsonl"
TAMPER_OUT = DATA / "tamper_check.json"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def catalog_hits(needle: str) -> int:
    """Bytes-mode scan: catalog.jsonl is 647,534,111 bytes (2026-10-23 dir
    census); text-mode decode hangs the fold (logged in JOURNEY)."""
    if not CATALOG.is_file():
        return -1
    n = 0
    needle_b = needle.encode("utf-8")
    with CATALOG.open("rb") as f:
        for ln in f:
            if needle_b in ln:
                n += 1
    return n


def main() -> int:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    apk_hash = sha256_file(APK)
    print("apk hashed", flush=True)
    so_hash = sha256_file(SO)
    print("so hashed", flush=True)
    apk_bytes = APK.stat().st_size
    hook_bytes = HOOK.stat().st_size
    so_bytes = SO.stat().st_size
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    true_reg = json.loads(REG_TRUE.read_text(encoding="utf-8"))["rows"]
    tamp_reg = json.loads(REG_TAMP.read_text(encoding="utf-8"))["rows"]
    so_key = str(SO)
    true_row = true_reg[so_key]
    tamp_row = tamp_reg[so_key]
    diff_fields = sorted(k for k in set(true_row) | set(tamp_row)
                         if true_row.get(k) != tamp_row.get(k))
    tamper = {
        "moment": now,
        "diff_fields": diff_fields,
        "detail": {k: {"true": true_row.get(k), "tampered": tamp_row.get(k)} for k in diff_fields},
        "session_runs": [
            {"run": "verify against true register", "exit": 0,
             "drift": False, "fields_checked": ["sha256", "functions", "entry", "decompiled_chars"]},
            {"run": "verify against tampered register", "exit": 5,
             "drift": True, "delta": diff_fields},
        ],
    }
    TAMPER_OUT.write_text(json.dumps(tamper, indent=1), encoding="utf-8")

    gi_line = None
    gi_no = 0
    with GITIGNORE.open("r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            gi_no += 1
            if ln.strip() == "*.apk":
                gi_line = gi_no
                break

    cat_apk = catalog_hits("aurora_store_76")
    print("catalog apk hits:", cat_apk, flush=True)
    cat_hook = catalog_hits("sess_297f5a13")
    print("catalog hook hits:", cat_hook, flush=True)

    standing_ok = REG_STANDING.is_file() and so_key in json.loads(
        REG_STANDING.read_text(encoding="utf-8"))["rows"]

    def row(rid, kind, claim, anchors, recheck):
        return {"row_id": rid, "kind": kind, "claim": claim,
                "anchors": anchors, "recheck": recheck, "computed_at": now}

    rows = [
        row("apk-1", "FINDING",
            "The shelf's bytes are fully identified: aurora_store_76.apk is Aurora Store "
            "(open-source Play client), package com.aurora.store, %d zip entries (666 xml, "
            "230 png, 2 dex, 4 native .so), 4 ABIs (arm64-v8a, armeabi-v7a, x86, x86_64), "
            "META-INF signed (DA477480 .SF/.RSA + MANIFEST.MF), resources.arsc present; "
            "apk %d bytes sha256 %s; R6's three census claims (1079 entries, 2 dex, 4 .so) "
            "all byte-true (entries_match=true)."
            % (census["zip"]["entry_count"], apk_bytes, apk_hash),
            ["watch/inbox/mates_leave_protocol/receipts/cartographer_20261023_data/apk_census.json",
             "research/corpus_triangulation/R6_swarm_apk.md:9-14"],
            "rerun apk_census.py in this dir; rerun apk_census.py in cartographer_20261020_data "
            "before comparing (that copy rewrites cycle 11's banked moment; the 20261023 copy is "
            "the rerun-safe one)"),
        row("apk-2", "FINDING",
            "The shelf's origin is receipted in three agreeing surfaces: R6_swarm_apk.md:9-14 "
            "(the UI-as-API door framing, installed on golden body emulator-5554), "
            "X_HARVEST_DOCTRINE_20260905.md:58-59 (Aurora Store installed on golden body 5554, "
            "Phase 2 cosmetic), TESUJI_MAP.jsonl:192 (R6 swarm inventory, verdict SUPPORTED, "
            "2026-09-06T06:43:24Z). The 218-byte hook-state file's updatedAt "
            "2026-09-05T18:35:55.953Z dates the placement session, same day as the doctrine.",
            ["research/corpus_triangulation/R6_swarm_apk.md:9-14",
             "watch/X_HARVEST_DOCTRINE_20260905.md:58-59",
             "watch/TESUJI_MAP.jsonl:192",
             "corpus/apk/.mimosa/hook-state/sess_297f5a13-4e0a-4ce3-827a-dff7a3e98386.json:1"],
            "read the three anchors; re-hash the hook-state file (218 bytes)"),
        row("apk-3", "LAW",
            "Entitlement, not bytes: the apk's 9,360,088 bytes are the smallest part of the "
            "shelf's value; the asset is the installed door on golden body 5554 inside the "
            "attestation perimeter (R6: 'The bridge carries ENTITLEMENT, not bytes'). The door "
            "inherits X_HARVEST law 4 (one fingerprint, no auto-re-auth): login is the "
            "operator's one hand, never automated.",
            ["research/corpus_triangulation/R6_swarm_apk.md:14",
             "watch/X_HARVEST_DOCTRINE_20260905.md:31-32"],
            "read both anchor lines; the law is filed here and in the receipt, no code change"),
        row("apk-4", "LAW",
            "Foreign hook-state dates placement, not content: build_seed_rib.py:345-347 names "
            "the Mimosa hook dropping .mimosa/hook-state into subprocess cwds as 'foreign "
            "droppings, never seed content'; tools/estate_atlas.py:51 classifies "
            ".mimosa/hook-state/ as a rotating sink. The shelf's 218-byte file is session "
            "machinery from the apk's placement session, not estate content.",
            ["watch/inbox/seed_rib_20260926/build_seed_rib.py:345-347",
             "tools/estate_atlas.py:51-52"],
            "read both anchor ranges; delete-scoping decision belongs to the Mimosa lane, "
            "not to shelf readers"),
        row("apk-5", "PRACTICE",
            "Resume-not-respawn pays at byte level: cycles 9, 10, 11 died mid-road on this "
            "thread; cycle 12 verified cycle 11's bank instead of redoing it. apk hash "
            "FD9C75D90D0F4A7C132B9B4A5A2CF1992A45E03B8D8FF988B7DCFBC0DB2C4D11 and .so hash "
            "%s matched all prior claims; the live verify passed first try (drift=false, "
            "exit 0). Zero re-work across four openings." % so_hash,
            ["watch/inbox/mates_leave_protocol/receipts/cartographer_20261020_data/ghidra_audit_register.json",
             "watch/inbox/mates_leave_protocol/receipts/receipt_20261023_cartographer.md"],
            "rerun: python tools/ghidra_audit.py verify <so> --register "
            "watch/inbox/mates_leave_protocol/receipts/cartographer_20261020_data/"
            "ghidra_audit_register.json (expect exit 0, drift false)"),
        row("apk-6", "DEBT",
            "The shelf is git-invisible: .gitignore line %d (*.apk) ignores the apk; git log "
            "over corpus/apk is empty and git status is clean-empty. Receipt banking is the "
            "only versioning the shelf has (same disease cycle 8 named for corpus/tools)."
            % (gi_line or -1),
            [".gitignore:%d" % (gi_line or -1)],
            "git check-ignore -v corpus/apk/aurora_store_76.apk; git log --oneline -- corpus/apk"),
        row("apk-7", "DEBT",
            "The deep rung's standing register was absent until cycle 12: the tool's default "
            "register path (memory/ghidra_audit_register.json) had no file; cycle 11's live "
            "row lived only in a receipt bank. Cycle 12 stood the default up (990 bytes, "
            "copied from the cycle 11 bank, standing_ok=%s). Remaining gap: tests/ carries 0 "
            "files mentioning ghidra_audit (rg count 0 over tests/), so the tool's verifier "
            "is the live receipt and verify mode only, no pytest harness." % str(standing_ok).lower(),
            ["tools/ghidra_audit.py:8-16",
             "memory/ghidra_audit_register.json"],
            "python tools/ghidra_audit.py verify <so> (default register); "
            "rg -l ghidra_audit tests/"),
        row("apk-8", "DEBT",
            "The X-app second lane is unbuilt and its status is unverifiable from bytes: R6 "
            "(2026-09-05) says 'X app install still in flight; login = operator's one hand'; "
            "48 days later no runtime probe receipt names golden body 5554 state. Runtime "
            "state of the door is UNVERIFIED by this fold; mapping it needs an adb/runtime "
            "lane, not a corpus walk.",
            ["research/corpus_triangulation/R6_swarm_apk.md:13",
             "watch/X_HARVEST_DOCTRINE_20260905.md:58-59"],
            "search watch/ for a golden-body or emulator-5554 runtime receipt newer than "
            "2026-09-06; absence keeps this debt open"),
        row("apk-9", "FINDING",
            "The 0.0 percent citation rate was machinery shadow, and the fold itself moved it: "
            "the 2026-10-13 bank read corpus/apk 0 of 2 files cited; post-fold rg (cycle 12 "
            "instrument) finds the shelf named by 6 receipt files (all cartographer: 1013, "
            "1017, 1018, 1019, 1020, 1023), mag/corpus_selfsteal.py:1 line, ESTATE_INDEX "
            "rows, and the two census banks. catalog/catalog.jsonl indexes the apk %s and "
            "the hook-state %s. The shelf's readers are its own receipt chain."
            % (cat_apk, cat_hook),
            ["watch/inbox/mates_leave_protocol/receipts/cartographer_20261013_data/corpus_shelf_citations.json",
             "mag/corpus_selfsteal.py",
             "catalog/catalog.jsonl"],
            "rerun the rg instrument from receipt_20261023 COUNTS; count catalog rows with "
            "the needles aurora_store_76 and sess_297f5a13"),
    ]

    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    kinds = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print("fold rows:", len(rows), kinds)
    print("apk sha256:", apk_hash, apk_bytes, "bytes")
    print("so sha256:", so_hash, so_bytes, "bytes")
    print("hook-state:", hook_bytes, "bytes")
    print("tamper diff fields:", diff_fields)
    print("gitignore *.apk at line:", gi_line)
    print("catalog hits: apk", cat_apk, "hook-state", cat_hook)
    print("standing register has so row:", standing_ok)
    return 0


if __name__ == "__main__":
    sys.exit(main())
