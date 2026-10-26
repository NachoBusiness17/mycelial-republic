# B2-328 2026-09-26: the landing QUEUE edits, one write, live CRLF preserved.
# Retires the lane's CLAIM line on githooks/pre-push, appends the landing note
# to the lane's row (the row was PRE-CHECKED [x] with no receipt, the B2-238
# disease; this landing earns the check, the note records that), and self-feeds
# 2 briefs UNCHECKED at highest+1 (B2-337, B2-338; high-water re-checked
# immediately before this write: B2-336 was the max).
import io

QUEUE = "watch/inbox/burn_wave_20260926/QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_328_refold_gate_20260926.md"

LANDING = (
    " Landed 2026-09-26 (checkbox was pre-checked [x] with no receipt before this landing, "
    "the B2-238 disease; this landing earns it): githooks/pre-push now carries a refold_gate "
    "block (WARN-ONLY first landing, the B2-260 --changed shape) running tools/refold_gate.py "
    "(the WHOLE tests/test_index_fold_host.py pin file) only when scripts/index_fold_host.mjs, "
    "the pin file or the gate itself differ from HEAD (staged or unstaged) or are untracked, or "
    "the pushed commit range touches any of the three (ref lines reused from the caption "
    "block's stdin capture); the brief's falsifier was executed for real: seqOrderKey mutated "
    "so tier 1 (2^53 band doubles) outranked tier 2 (exact seqs), file saved, git push "
    "--dry-run through the then-current hook named the mutation zero times; load-bearing "
    "finding: the swap is refold-STABLE (the mutated comparator is still a deterministic total "
    "order) so the stability pin alone PASSES on it, the demotion and total-order pins name it "
    "(6 failures incl. test_inexact_band_register_loses_to_later_exact_register), which is why "
    "the gate runs the whole file, never the stability test alone; payload is the "
    "throwaway-inbox pins, not the production-log falsifier (that one appends dummy events to "
    "the shared index_events.jsonl on every run, a push hook must never write the shared log); "
    "operator response defined in the hook comment and the gate FAIL output (revert or fix the "
    "comparator edit until ok, never loosen the hook); cost when idle git plumbing only, when "
    "fired ~6s; host bytes restored byte-identical sha256 F60955A2D8E0085B8FC11A0F9A23D14F4BCBF7D58A4F642918AEF9F901C3241D, "
    "gate ok 21 passed on the restored bytes; live concurrent-lane proof: the sibling B2-329 "
    "pin landed red mid-lane and the gate named it while every comparator pin stayed green; "
    f"receipt {RECEIPT}."
)

BRIEFS = [
    "- [ ] B2-337 File or retire the B2-279 receipt ghost: (self-fed by B2-328) the B2-279 "
    "landing trail (the QUEUE.md B2-279 row, the three CLAIMED B2-279 lines above it, the "
    "B2-328 and B2-329 brief pointers, and the memory/burns/LEDGER.jsonl row "
    "2026-09-26T16:19:48Z) all name watch/inbox/burn_wave_20260926/B2_279_sort_totality_20260926.md, "
    "which does not resolve on disk (checked 2026-09-26T16:31Z during B2-328), so the estate's "
    "landing record for the fold sort-totality law lives only in the LEDGER one_line and the "
    "B2_279_*.py/.json artifacts; reconstruct the receipt from those bytes or retire the "
    "pointers per the B2-238 ghost law, and record which path was taken; falsifier: every "
    "receipt pointer on the B2-279 row and its two self-feed rows resolves after the lane; "
    "pointer memory/burns/LEDGER.jsonl, watch/inbox/burn_wave_20260926/B2_238_checkbox_law_20260926.md.",
    "- [ ] B2-338 Fix the census patrol ok-line case so the hook stops crying wolf: (self-fed "
    "by B2-328) tools/census_drift_patrol.py prints its green line as \"CENSUS-PATROL: OK - ...\" "
    "(uppercase) while the githooks/pre-push census block case-matches on the lowercase prefix "
    "\"CENSUS-PATROL: ok\", so a fully green census prints \"PUSH-GATE: census WARN:\" plus the "
    "whole OK output on every push (observed live 2026-09-26 in the B2-328 stubbed E2E run), "
    "training operators to dismiss the census WARN channel, the exact failure mode an enforcing "
    "flip would inherit; align the tool's ok line to the lowercase contract or widen the hook "
    "case, and pin the pairing with a self-test; falsifier: a green census run through the hook "
    "prints the ok arm, not the WARN arm; pointers tools/census_drift_patrol.py, "
    "githooks/pre-push census block, watch/inbox/burn_wave_20260926/B2_215_census_tripwire_20260926.md.",
]

with io.open(QUEUE, "r", encoding="utf-8", newline="") as fh:
    text = fh.read()

crlf = "\r\n" in text
eol = "\r\n" if crlf else "\n"
lines = text.split(eol)

# 0) preconditions on live bytes
claims = [i for i, l in enumerate(lines) if l.startswith("- CLAIM B2-328 ")]
assert len(claims) == 1, f"expected exactly 1 claim line, found {len(claims)}"
# NOTE: the board carries a number collision (B2-75's refiled Gardenfors brief
# also carries the B2-328 number, line ~409), so the row match pins the brief
# text, not just the number.
ROW_PREFIX = "- [x] B2-328 Wire the refold-stability falsifier into a gate:"
rows = [i for i, l in enumerate(lines) if l.startswith(ROW_PREFIX)]
assert len(rows) == 1, f"expected exactly 1 B2-328 gate row, found {len(rows)}"
assert "B2-337" not in text and "B2-338" not in text, "self-feed numbers taken; renumber highest+1"
row = rows[0]

# 1) retire the claim
lines[claims[0]] = lines[claims[0]].replace("- CLAIM B2-328 ", "- CLAIMED B2-328 ", 1) + f" -> {RECEIPT}"

# 2) landing note on the row (append, no bytes erased), self-feeds directly after
lines[row] = lines[row] + LANDING
lines[row + 1 : row + 1] = BRIEFS

text = eol.join(lines)
with io.open(QUEUE, "w", encoding="utf-8", newline="") as fh:
    fh.write(text)
print("queue landing: claim retired, B2-328 landing note appended, self-feeds B2-337/B2-338 inserted unchecked, eol", repr(eol))
