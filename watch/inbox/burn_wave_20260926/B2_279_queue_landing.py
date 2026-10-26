# B2-279 2026-09-26: the landing QUEUE edits, one write, live CRLF preserved.
# RACE NOTE: while this lane worked, the B2-251 checkbox-audit pass 2 found the
# B2-279 row pre-checked [x] with no receipt on disk (true at audit time),
# flipped it, and left a standalone annotation line in the row's place. This
# script is the rebased landing: it retires the lane's three CLAIM lines,
# RESTORES the B2-279 brief row checked with the landing note and receipt
# pointer directly AFTER the audit annotation (their bytes stay, append-only),
# and self-feeds 2 briefs UNCHECKED at highest+1 (B2-328, B2-329; high-water
# re-checked immediately before this write).
import io

QUEUE = "watch/inbox/burn_wave_20260926/QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_279_sort_totality_20260926.md"

BRIEF = (
    "- [x] B2-279 Fold event sort is non-transitive: (self-fed by B2-254; first drafted B2-277, "
    "number taken mid-lane by the concurrent B2-249 self-feed, renumbered highest+1 per the B2-167 "
    "law) readEvents (scripts/index_fold_host.mjs) compares null-seq events (autoseals, "
    "md-record-seal registers) by ts and seq-carrying events by BigInt seq, a mix Array.sort cannot "
    "total-order, so within the 2^53 quantization band (raw literal 1789823567015749400 family and "
    "the 12:03:24Z gala batch 1789823567015749473-477, which all parse to the same double) "
    "last-register-wins is decided by sort luck refold to refold: B2-254 measured "
    "burn_wave_20260926/QUEUE.md and phone_relay_log.jsonl flipping failing to living across the "
    "14:33, 14:48, 14:53 and 15:13Z refolds with zero register events in between; give every event a "
    "total-order key (exact decimal-string seqs; inexact doubles demoted below every exact seq with "
    "a counted fold warning; null-seq events keyed by (ts, file order) strictly below all seq "
    "events) and pin the fix with a refold-stability test; falsifier: refold the production log five "
    "times with a dummy append between and any active item changes; pointers "
    "scripts/index_fold_host.mjs readEvents/compareBySeqTs, "
    "watch/inbox/burn_wave_20260926/B2_254_fold_order_probe.js, "
    "watch/inbox/burn_wave_20260926/B2_254_living_regression_20260926.md."
)
LANDING = (
    " Landed 2026-09-26 (row history: B2-254 self-fed it unchecked per its receipt; a concurrent "
    "writer pre-checked it, the B2-238 disease; the B2-251 audit pass 2 then flipped it unchecked "
    "mid-lane while this fix was in flight because no receipt existed at audit time, leaving its "
    "annotation line above this restored row; this landing earns the check): every event now "
    "carries one total-order key in scripts/index_fold_host.mjs (null-seq events keyed (ts, file "
    "order) strictly below all seq events; integer doubles past 2^53 kept as their parsed BigInt but "
    "demoted below every exact seq with the counted fold warning, production census 561 events "
    "across 1 distinct parsed double 1789823567015749376; exact decimal strings and safe integers "
    "by BigInt), the comparator's C<A<B<C non-transitivity pinned broken in tests; refold stability "
    "pinned in tests/test_index_fold_host.py and executed on the production log: 5 refolds with "
    "exact-string dummy note appends between, active items plus fold warnings identical across all "
    "5 (B2_279_refold_after_results.json); old-vs-new fold attribution over the same log bytes: 54 "
    "of 1018 active rows change winning register (35 band refresh loses to an older exact register, "
    "19 band invalidate demoted resurrecting an exact register, full lists "
    "B2_279_order_attribution_results.json and B2_279_changed_paths.json); LINKS.jsonl, "
    "phone_relay_log.jsonl and burn_wave_20260926/QUEUE.md are NOT among them, all three B2-254 "
    "living re-pins hold and QUEUE.md prints LIVING OPEN post-fix; receipt "
    "watch/inbox/burn_wave_20260926/B2_279_sort_totality_20260926.md."
)
BRIEFS = [
    "- [ ] B2-328 Wire the refold-stability falsifier into a gate: (self-fed by B2-279) the "
    "sort-totality pins exist (tests/test_index_fold_host.py::test_refold_stability_with_dummy_appends_between "
    "on throwaway inboxes, watch/inbox/burn_wave_20260926/B2_279_refold_falsifier.py on the "
    "production log) but nothing runs either one when scripts/index_fold_host.mjs changes, so a "
    "future comparator edit can reintroduce sort luck with no gate firing; wire the falsifier into "
    "githooks/pre-push on the --changed pattern (same shape as the B2-260 verifier gate, node is "
    "already a test dependency) or a scheduled patrol run, and define the operator response when it "
    "fires; falsifier: mutate seqOrderKey so tier 1 outranks tier 2, save, and no gate names the "
    "mutation; pointers scripts/index_fold_host.mjs (seqOrderKey, compareBySeqTs), githooks/pre-push, "
    "watch/inbox/burn_wave_20260926/B2_279_sort_totality_20260926.md.",
    "- [ ] B2-329 Strip the fold's internal fields from the events dump: (self-fed by B2-279) the "
    "`events` command JSON.stringify's each event as readEvents left it, so every dumped line since "
    "B2-157 carries the fold plumbing fields _outside and _unresolved (B2-279 considered and "
    "rejected adding more), and downstream consumers of the dump parse fold internals as event "
    "content; strip underscore-prefixed fields in the events command output only (the log bytes stay "
    "untouched) or register the dump shape as contract with a test pinning the exact key set; "
    "falsifier: node scripts/index_fold_host.mjs events piped through a strict JSON consumer that "
    "rejects unknown keys fails today on _outside; pointers scripts/index_fold_host.mjs (events "
    "command, readEvents), watch/inbox/burn_wave_20260926/B2_279_sort_totality_20260926.md.",
]

with io.open(QUEUE, "r", encoding="utf-8", newline="") as fh:
    text = fh.read()

crlf = "\r\n" in text
eol = "\r\n" if crlf else "\n"
lines = text.split(eol)

# 0) preconditions on live bytes
assert not any(l.startswith("- [x] B2-279") or l.startswith("- [ ] B2-279") for l in lines), \
    "a B2-279 row already exists; rebase instead of inserting"
assert "B2-328" not in text and "B2-329" not in text, "self-feed numbers taken; renumber highest+1"
ann = [i for i, l in enumerate(lines) if "B2-251 checkbox audit, second pass" in l and "compareBySeqTs" in l]
assert len(ann) == 1, f"audit annotation anchor hits {len(ann)}"
anchor = ann[0]

# 1) retire the claims
retired = 0
for i, ln in enumerate(lines):
    if ln.startswith("- CLAIM B2-279 "):
        lines[i] = ln.replace("- CLAIM B2-279 ", "- CLAIMED B2-279 ", 1) + f" -> {RECEIPT}"
        retired += 1
assert retired == 3, f"expected 3 claim lines, retired {retired}"

# 2) restore the row (checked, with landing note) AFTER the audit annotation,
#    then the two self-feeds
lines[anchor + 1 : anchor + 1] = [BRIEF + LANDING] + BRIEFS

text = eol.join(lines)
with io.open(QUEUE, "w", encoding="utf-8", newline="") as fh:
    fh.write(text)
print("queue landing rebased: 3 claims retired, B2-279 row restored checked after the audit annotation, briefs B2-328/B2-329 inserted, eol", repr(eol))
