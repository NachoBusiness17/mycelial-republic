"""One-off B2-239 LEDGER.jsonl append (run once, deletes nothing)."""
import datetime
import json
from pathlib import Path

LEDGER = Path("memory/burns/LEDGER.jsonl")
line = json.dumps({
    "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "b2-239-line-endings",
    "verdict": "landed",
    "fresh_failure_mode": False,
    "landing": "watch/inbox/burn_wave_20260926/B2_239_line_endings_20260926.md",
    "one_line": ("B2-239 LANDED: the B2-220 pre-regen CRLF state of "
        "q_caption_ledger.jsonl proven a content-preserving ending flip "
        "(LF-normalized snapshot sha e1677ba76cf7 equals the B2-68 post sha) "
        "carried through git's filters: the 291-row LF content survives as "
        "dangling blob aba4dbbd, no blob holds the CRLF form, core.autocrlf=true "
        "with .gitattributes guarding only rbxlx/rbxm, generator exonerated "
        "(newline backslash-n in HEAD and working tree), nearest reflog event "
        "reset moving to HEAD 2026-09-26 09:53:05 -0400 inside the window; "
        "guard: verifier check8 LF-only assertion landed (docstring spec first), "
        "green 8/8 exit 0 on the live 267-row ledger sha 489d5af9, red FAIL 291 "
        "CR bytes on the historic disease bytes, control LF leg PASS, pytest "
        "10 passed (test_pin_law_fail_output + test_hook_prefix_pairing); "
        "queue row sat pre-checked [x] with no receipt, this landing earns it; "
        "self-feeds first drafted B2-541/542, taken by the concurrent B2-521 "
        "band, landed renumbered as B2-544/545 per the B2-167 law"),
}, ensure_ascii=False)

lb = LEDGER.read_bytes()
assert b"b2-239-line-endings" not in lb, "ledger row already present"
leol = "\r\n" if lb.count(b"\r\n") >= (lb.count(b"\n") - lb.count(b"\r\n")) else "\n"
with LEDGER.open("a", encoding="utf-8", newline="") as f:
    if lb and not lb.endswith(b"\n"):
        f.write(leol)
    f.write(line + leol)
last = [l for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()][-1]
parsed = json.loads(last)
assert parsed["slug"] == "b2-239-line-endings" and parsed["verdict"] == "landed"
print("ledger row appended + parse-back ok, ts", parsed["ts"])
