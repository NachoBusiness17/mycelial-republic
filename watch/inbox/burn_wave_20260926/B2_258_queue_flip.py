#!/usr/bin/env python
"""One-shot queue repair + flip for B2-258 (run once, then left in place)."""
from pathlib import Path

P = Path(__file__).resolve().parents[3] / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
raw = P.read_bytes()

# 1. repair the backspace byte in the B2-282 row -> literal \b (2 chars)
bs = bytes([8])
target = b"[a-z]*" + bs + b'"'
if bs in raw:
    assert raw.count(bs) == 1, f"unexpected backspace count {raw.count(bs)}"
    assert target in raw, "backspace context shifted; inspect manually"
    raw = raw.replace(bs, b"\\b")
    print("backspace repaired to literal \\b")

# 2. flip B2-258 with the landing pointer (CRLF aware)
text = raw.decode("utf-8")
nl = "\r\n" if "\r\n" in text else "\n"
anchor = "pointers watch/inbox/burn_wave_20260926/B2_243_bucket_audit_20260926.md Exclusions sentence-year entry, watch/inbox/burn_wave_20260926/B2_243_guard_probe.py."
landed = (" Landed 2026-09-26: 0.90 YEAR_FIRST rule in the generator, "
          "pre-edit sweep fired on exactly id 7175228 across 6,242 drops with "
          "zero numeric year-first variant sites, regen diff exactly one added "
          "row (7175228, 2041-12-31, 0.9) with 2019-12-31 pinned absent, "
          "verifier 7/7 PASS on 267 rows keepers byte-equal 76/76, check7 pin "
          "re-derived per the B2-259 law (scoped net); receipt "
          "watch/inbox/burn_wave_20260926/B2_258_yearfirst_20260926.md, probe "
          "watch/inbox/burn_wave_20260926/B2_258_yearfirst_probe.py.")
assert anchor in text, "B2-258 anchor not found"
assert text.count(anchor) == 1, "anchor not unique"
if landed.strip() not in text:
    text = text.replace(anchor + nl, anchor + landed + nl, 1)
    print("B2-258 row flipped with landing pointer")
else:
    print("B2-258 already flipped")

P.write_bytes(text.encode("utf-8"))
print("bytes:", bytes([8]) in P.read_bytes())
