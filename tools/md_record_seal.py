#!/usr/bin/env python3
"""md_record_seal — teeth for rib.md.record.v1 (2026-09-21).

Two modes, wired in the ZCode hook channel alongside prebuild_gate (Write|Edit):

  gate  PreToolUse  — blocks Write of content > 8 MB into watch/ (the hard-drive
                      guard). Everything else passes.
  seal  PostToolUse — any Write/Edit landing under the estate's durable roots
                      gets ONE append line in watch/inbox/index_events.jsonl:
                      op=autoseal, path, sha256 for text <=256 KB, size+mtime for
                      the rest. No copies, no duplication (~250 B/line). Deduped
                      against the recent tail so edit storms don't spam.
                      Since 2026-09-26 (writer-contract fix) a register event
                      joins the autoseal so the INDEX fold lifts the file into
                      active items. Since B2-41 (same day) the register carries
                      the inbox-relative path and fires only for files under
                      watch/inbox: absolute C:/ registers folded into phantom
                      INDEX items that needed manual invalidation (B2-50,
                      B2-145), and the fold drops non-inbox roots as outside.

Fail-open for availability, logged for honesty (prebuild_gate law): any internal
error exits 0 with a stderr note — a broken seal must never block the fleet.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

ESTATE = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
EVENTS = ESTATE / "watch" / "inbox" / "index_events.jsonl"
DURABLE = [ESTATE / "watch", ESTATE / "memory" / "rib",
           ESTATE / "memory" / "game_modules", ESTATE / "memory" / "corpus",
           ESTATE / "corpus", ESTATE / "queue"]
MAX_BYTES = 8 * 1024 * 1024
HASH_LIMIT = 256 * 1024
TAIL_DEDUP = 60

# B2-148 (2026-09-26): the register event adopts the B2-40 seq scheme. Before
# this fix the hook appended registers with NO seq field, so the fold's sort
# totality (B2-279) demoted them below every exact-seq event and decided
# last-register-wins by ts luck; the QUEUE.md absolute-path mismatch rows in
# the INDEX fold were the visible symptom. Mirrors scripts/index_fold_host.mjs
# seqOf/nextSeq exactly: usable seqs are integer Numbers and digit-only decimal
# strings; emission is a plain JSON number while it fits 2^53-1 and switches to
# a decimal STRING beyond (float64 quantizes raw literals past 2^53, ulp 256
# at production magnitude, so the string is the only exact carrier).
MAX_SAFE_SEQ = 2 ** 53 - 1


def _seq_of(ev: dict):
    s = ev.get("seq")
    if isinstance(s, bool):
        return None
    if isinstance(s, int):
        return s
    if isinstance(s, str) and s.isdigit():
        return int(s)
    return None


def next_seq(events: list) -> "int | str":
    best = None
    for ev in events:
        if not isinstance(ev, dict):
            continue
        s = _seq_of(ev)
        if s is not None and (best is None or s > best):
            best = s
    nxt = (0 if best is None else best) + 1  # fold nextSeq: (max ?? 0n) + 1n
    return nxt if nxt <= MAX_SAFE_SEQ else str(nxt)



def fail_open(note: str) -> None:
    print("md_record_seal: " + note, file=sys.stderr)
    sys.exit(0)


def seal_line(path: Path) -> dict:
    size = path.stat().st_size
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
           "op": "autoseal", "file": str(path).replace("\\", "/"),
           "bytes": size}
    try:
        if size <= MAX_BYTES:
            h = hashlib.sha256()
            with path.open("rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            rec["sha256"] = h.hexdigest()
        else:
            rec["sha256"] = "size-only(>8MB)"
    except OSError:
        rec["sha256"] = "unreadable"
    rec["purpose"] = "autoseal (rib.md.record.v1)"
    return rec


def register_sha256(path: Path, rec_sha: str) -> str:
    """A register event must carry a value verify can check (B2-294, 2026-09-26).

    CAUSE: seal_line() writes the cheap token "size-only(>256KB)" for big files
    and the register event reused it, so the first hook-registered inbox file
    over 256KB would mint an INDEX item whose sha is not a hash and fails
    verify forever (0 such events exist today -- the fix is preventive).
    FIX: hash real bytes for the register (one streaming read, same 8 MB cap
    the gate enforces); only a file beyond that cap falls back to the B2-156
    living-style prefix seal (sha256 of the first 256KB, size-named), which
    the fold's living machinery can still verify. EVIDENCE: zero
    '"size-only"' matches in index_events.jsonl at fix time (measured), and
    tests in tests/test_md_record_seal.py pin the behavior.
    """
    import re as _re
    if rec_sha and _re.fullmatch(r"[0-9a-f]{64}", rec_sha or ""):
        return rec_sha
    size = path.stat().st_size
    if size <= MAX_BYTES:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    # beyond the cap: B2-156 living-style prefix seal, sha256 of exactly the
    # first 256KB, size-named so the fold's living machinery can check it
    with path.open("rb") as f:
        head = f.read(262144)
    return "sha256(first 262144):" + hashlib.sha256(head).hexdigest() + f"@{size}B(living-style, B2-156)"


def inbox_rel(path: Path) -> str | None:
    """Inbox-relative posix path, or None when the fold cannot hold the file.

    Cause + evidence (B2-41, 2026-09-26): the register event reused the seal's
    absolute host path. The fold keeps C:/ paths (they match no OUTSIDE_RE
    segment), so every hook registration minted a phantom INDEX item that only
    resolves on this host: QUEUE.md was minted twice (events 2784 and the
    /board/inbox/C:/ double prefix at 3053) and LAW13_EXPERIMENT_ON_ABSENCE
    once (event 3070 area), each needing a manual invalidate by the B2-50 and
    B2-145 lanes. Only files under watch/inbox register (that is the surface
    the fold serves); other durable roots keep the autoseal journal line only.
    """
    try:
        return path.relative_to(ESTATE / "watch" / "inbox").as_posix()
    except ValueError:
        return None


def autoseal_file(p: Path) -> bool:
    p = p.resolve()
    if not p.exists():
        return False
    try:
        under = any(os.path.commonpath([str(p), str(root.resolve())]) == str(root.resolve())
                    for root in DURABLE if root.exists())
    except ValueError:
        under = False
    if not under:
        return False
    rec = seal_line(p)
    recent = EVENTS.read_text(encoding="utf-8", errors="replace").splitlines()[-TAIL_DEDUP:]
    if any(('"op": "autoseal"' in ln or '"op":"autoseal"' in ln)
           and str(p).replace("\\", "/") in ln
           and f'"bytes": {p.stat().st_size}' in ln
           and f'"sha256": "{rec["sha256"]}"' in ln
           for ln in recent):
        return False
    rel = inbox_rel(p)
    last_nonce = 0
    seq = None
    if rel is not None:
        parsed = []
        for ln in EVENTS.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                ev = json.loads(ln)
            except Exception:
                continue
            parsed.append(ev)
            if (ev.get("writer") == "md-record-seal"
                    and isinstance(ev.get("nonce"), int)):
                last_nonce = max(last_nonce, ev["nonce"])
        seq = next_seq(parsed)
    reg = {"ts": rec["ts"], "op": "register", "file": rel,
           "sha256": register_sha256(p, rec.get("sha256", "")),
           "class": "receipt",
           "purpose": "autoseal register (writer-contract fix 2026-09-26)",
           "writer": "md-record-seal", "nonce": last_nonce + 1}
    if seq is not None:
        reg["seq"] = seq
    with EVENTS.open("a", encoding="utf-8") as f:
        if rel is not None:
            f.write(json.dumps(reg) + "\n")
        f.write(json.dumps(rec) + "\n")
    return True


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "seal-files":
        for arg in sys.argv[2:]:
            try:
                ok = autoseal_file(Path(arg))
                print(f"autoseal {'OK' if ok else 'SKIP'}: {arg}")
            except Exception as e:
                print(f"autoseal ERR: {arg} ({e})", file=sys.stderr)
        sys.exit(0)
    try:
        event = json.load(sys.stdin)
    except Exception as e:
        fail_open(f"bad event json: {e}")
    ti = event.get("tool_input") or {}
    raw = str(ti.get("file_path") or ti.get("path") or "")
    if not raw:
        sys.exit(0)
    p = Path(raw)
    try:
        under = any(os.path.commonpath([str(p), str(root)]) == str(root)
                    for root in DURABLE if root.exists())
    except ValueError:
        under = False
    if not under:
        sys.exit(0)

    if mode == "gate":
        content = ti.get("content") or ti.get("new_string") or ""
        if isinstance(content, str) and len(content.encode("utf-8", "replace")) > MAX_BYTES:
            print(json.dumps({"decision": "block", "reason":
                f"rib.md.record guard: {MAX_BYTES//1024//1024} MB writes into the "
                "durable record are refused — park big bytes outside watch/ and "
                "file an md pointer instead"}))
            sys.exit(0)
        sys.exit(0)

    if mode == "seal":
        try:
            autoseal_file(p)
        except OSError as e:
            fail_open(f"seal skipped: {e}")
    sys.exit(0)


if __name__ == "__main__":
    main()
