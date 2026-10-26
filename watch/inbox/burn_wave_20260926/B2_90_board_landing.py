#!/usr/bin/env python
"""B2-90 board landing: retire 3 CLAIM lines, earn the pre-checked B2-90 row,
self-feed 3 briefs numbered highest+1 at apply time (B2-167 renumber law).

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_90_board_landing.py
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Q = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_90_album_captions_20260926.md"

claims = [
    "- CLAIM B2-90 watch/inbox/CAPTION_LEDGER_20260926.jsonl 2026-09-26T18:06:49Z",
    "- CLAIM B2-90 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T18:06:49Z",
    "- CLAIM B2-90 watch/inbox/index_events.jsonl 2026-09-26T18:14:41Z",
]
row_marker = "- [x] B2-90 Resolve the 9 unresolved mrpool album captions:"
standing = "## Standing law note (operator, 2026-09-26, binds every lane)"

landed = (
    " Landed 2026-09-26 (row was pre-checked [x] from dispatch; this landing earns it): "
    "all 9 resolved from local bytes, no fetch, no model calls, by widening the carrier "
    "search to the album run (maximal contiguous grouped=True run in ledger_full.jsonl, "
    "consecutive stamps no more than 60s apart); carriers @MrPool_Q#4622 (album 4618..4622, "
    "caption sits on the LAST member), #4595 (4595..4600), #3606 (3606..3610), #2977 "
    "(2977..2981), #1779 (1779..1785), #1389 (1389..1393), each the unique same-calendar-date "
    "text carrier of its run, msg_id distance 4..6, all strictly outside the +/-3 order that "
    "left them unresolved in B2-12; CAPTION_LEDGER_20260926.jsonl patched in place: 2726 rows "
    "and order unchanged, 2717 lines byte-identical, the 9 rows gain caption_via plus "
    "caption_via_v2=2026-09-26 and keep caption empty per the B2-12 via-row precedent, "
    "sha256 661004FD39F4DF741DB0B39979409417B71D8C900A1CA108812A6DEF217860FC to "
    "A2C96FA49E02D60B959AF887627DC95F004CBE56C173E29D507473DC80466743; INDEX item re-sealed "
    "seq 1790446500998860905 (living-hash law clause 5) after a first repo-root add "
    "(seq 1790446136785949201) was outside-dropped by the fold, watch/ x265 WARN, redone from "
    "the inbox root; fold verify 1026 hash-clean, 11 living-ok, 1 living-open, 5 mismatched, "
    "0 missing, the 5 the pre-existing INDEX self-hash plus concurrent-files set B2-89 named, "
    "none this lane's bytes; mag.shared_surface validate adds no new error; falsifier executed "
    "for real: the exact-datetime album key failed closed exit 2 on 3 targets before any "
    "write and was replaced by the run rule; the 2 non-grouped empty rows (1684, 2493) are "
    "out of scope and stay the only empty caption plus empty caption_via rows; receipt "
    + RECEIPT + "; self-fed B2-413, B2-414, B2-415."
)

briefs = [
    "- [ ] {n} caption_via invariant pin: all 111 caption_via pointers in "
    "CAPTION_LEDGER_20260926.jsonl (102 from B2-12, 9 from the B2-90 v2) must name a carrier "
    "that is grouped=True with non-empty text on the same calendar date in ledger_full.jsonl, "
    "and no check enforces that today while B2_12_caption_ledger_build.py still carries the "
    "+/-3 search order, so a rebuild regresses the 9 v2 rows to empty with every current gate "
    "green; add a verify pin in the B2-409 row's shape, wired wherever the ledger is rebuilt; "
    "falsifier: run the B2-12 builder unmodified and no check names the 9 rows losing their "
    "carriers; pointers watch/inbox/burn_wave_20260926/B2_90_album_captions_v2.py, "
    "watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py, the B2-409 row in this file.",
    "- [ ] {n} resolve or classify the last 2 empty-caption rows: msg 1684 and msg 2493 are "
    "metadata-only, non-grouped, caption_len 0, so no album sibling exists and no window "
    "widening can ever fill them; either pull their t.me/MrPool_Q anchors (curl -I first per "
    "AGENTS.md, SSO 302 possible; live text quoted as evidence only, the ledger stays the "
    "byte source for file rows) and patch a dated v3, or register a declared-unresolvable "
    "class so empty caption plus empty caption_via is exhaustive-by-rule; falsifier: a "
    "consumer cannot tell caption-pending from channel-message-has-no-caption for those rows; "
    "pointers watch/inbox/CAPTION_LEDGER_20260926.jsonl:2223 and :3495, "
    "watch/inbox/burn_wave_20260926/B2_90_album_captions_20260926.md.",
    "- [ ] {n} carrier-position honesty: across the 6 albums the B2-90 v2 resolved, the "
    "caption sits on the FIRST member in 5 (4595, 3606, 2977, 1779, 1389) and on the LAST "
    "member in 1 (4622 for album 4618..4622), so position is real sender variance, not a "
    "fold artifact; document the distribution in the B2-12 builder header or a ledger note "
    "so no future attribution rule assumes first-member; falsifier: a first-member-only rule "
    "leaves msg 4618 empty again while every other check stays green; pointers "
    "watch/inbox/burn_wave_20260926/B2_90_album_captions_v2.py, "
    "watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py.",
]

text = Q.read_text(encoding="utf-8")

for c in claims:
    assert text.count(c) == 1, ("claim line not unique", c)
    idx = text.index(c)
    line_end = text.index("\n", idx)
    line = text[idx:line_end]
    assert line.startswith("- CLAIM B2-90 ") and " -> " not in line, line[-60:]
    retired = line.replace("- CLAIM B2-90", "- CLAIMED B2-90", 1)
    retired = retired + " -> " + RECEIPT
    text = text[:idx] + retired + text[line_end:]

assert text.count(row_marker) == 1
idx = text.index(row_marker)
line_end = text.index("\n", idx)
row_line = text[idx:line_end]
assert "Landed 2026-09-26" not in row_line, "B2-90 row already landed by another writer"
text = text[:line_end] + landed + text[line_end:]

nums = sorted({int(m) for m in re.findall(r"B2-(\d+)", text)})
highest = nums[-1]
mine = [highest + 1, highest + 2, highest + 3]
assert not (set(mine) & set(nums))
block = "".join(
    brief.format(n=f"B2-{n}") + "\n"
    for n, brief in zip(mine, briefs)
)
assert block.count("\n") == 3 and "\n\n" not in block
assert text.count(standing) == 1
text = text.replace(standing, block + standing, 1)

for bad in ("\u2014", "\u2013"):
    assert bad not in block and bad not in landed, "em-dash in added text"

Q.write_text(text, encoding="utf-8", newline="")
print("claims retired: 3; row B2-90 earned; self-fed:", [f"B2-{n}" for n in mine],
      "(highest before:", f"B2-{highest})")
print("board ts:", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
