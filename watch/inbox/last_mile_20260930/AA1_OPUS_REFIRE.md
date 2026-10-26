# AA1 OPUS REFIRE: landed PARTIAL on the third transport (2026-09-30)

Status: FIRED AND BANKED. The identical W4 ask (sha256 b805548a93fddb575af09c77
c84a013398f6aa2ed0a558af79079183e002f4f7, 31070 bytes, 12729 prompt tokens)
with max_tokens 32000 and NO reasoning cap. The return is REAL but TRUNCATED:
reasoning burned 29476 of 32000, the body started (5955 chars, sections A and
B through delta D4) and finish_reason=length cut sections C to G. Section A
(the verdict on the baseline) is COMPLETE. Verbatim bytes:
watch/inbox/last_mile_20260930/W4_OPUS_RETURN_20260930.md + raw3.json.

## 1. Transport saga (the fix took three attempts)

- a1 whole-response, socket 1800s: TimeoutError, 0 bytes, $0 metered. Banked.
- a2 whole-response, socket 3600s: TimeoutError, 0 bytes, $0 metered. Banked
  (AA1_OPUS_REFIRE_raw2.json). W4's 16k call returned in 194.6s non-streaming
  on the same route, so this is the known gateway disease: whole-response
  reads die when generation outlives the window (v1 duel grok-4.7 precedent).
- a3 STREAMING SSE (per-read timeout 300s, v1_multifamily_duel.py call_long
  pattern): LANDED. 362.4s, 3733 chunks, $0.690916 metered (catalog $4/$20 per
  M, no markup). Streaming is the fix; whole-response is dead for 32k Opus.

## 2. Byte stability held twice (sha guard earned its keep)

At 08:06 a sibling lane landed AMENDMENT 5 into the working-tree
BASELINE_SPEC.md (34678 bytes). The a3 sha guard caught the drift (2f43d2d9,
40578 bytes) with ZERO spend, and the baseline was pinned to git blob
c72a49d65 (25170 bytes), which rebuilds the exact W4 prompt sha b805548a. The
frontier judged the document W4 judged; amendment 5+ is a known delta on top.

Sibling-collision note: AA1_REFIRE_VERDICT.md (07:30, another seat) closed this
lane prematurely on the a1 timeout alone and its own re-run overwrote the a1
raw row (1800.1s vs my 1800.3s). Its option 2 (streaming retry) is what landed
here. Its verdict file stays untouched as their bytes.

## 3. Costs

W4 $0.370916 + AA1a3 $0.690916 = $1.061816 confirmed vs the $2.00 mission
absolute. Both timeouts returned usage={} ($0 metered; if the route billed
them server-side it is unconfirmable from here). Remaining headroom: $0.94.

## 4. The verdict on our baseline (section A, complete, verbatim banked)

Headline: the frontier CONFIRMS we are weak exactly where we suspected and
names three structural kills, all on the READ side; the write side survives.

- 26 section rows: 22 TIGHTEN, 0 KILL, 4 KEEP (sections 0, 4.2, 9, 10).
- Kill 1: DRIFT IS INVISIBLE INSIDE OUR OWN BUDGET. Fail verdicts REFRESH
  freshness under 4.1 decay, so a collapsing cell looks young; total collapse
  of a 300-verdict cell at 0.95 needs ~21 fresh fails to demote, breaching K3's
  10-verdict ceiling by arithmetic. Its fix: a recent-window guard, demote at
  the 4th fail in the last 10 (pre-registered binomial, not a bandit).
- Kill 2: CALIBRATION IS CERTIFIED FROM THE WRONG REGION. T1 verifies answers
  below min_confidence, but low-confidence stops go ungated, so evidence is
  sampled almost entirely ABOVE the threshold: survivorship bias in cell rates
  and ECE.
- Kill 3: IDENTITY IS A LABEL, NOT BYTES. The ledger keys on a model_id string
  any operator can repoint to different weights; violates our own trust-bytes
  law. Section 2 PK lacks environment identity.
- Also named: the G3 cap is satisfiable by 1 G0 verdict plus 999 G3 verdicts;
  Am2 rebase invalidates signatures covering prev_sha256 (D1 fixes scope);
  4.1 decay LIFTS cells below 0.5 as they age (one-token eff_lb95 fix); the
  USD probe leash cannot bind a 95 percent local fleet.

## 5. What the return does NOT deliver (honest)

Acceptance gates 2 (three hostile attacks, section D) and 4 (self-doubt,
section F) are NOT deliverable from this return: those sections were composed
(the reasoning tail shows section F flags ready: the USD leash "breaks down
for a mostly-local fleet", SuperScout citation marked UNPROVEN, the em-dash
ban called a weak proxy) but the length cap ate them. Gate held: 0 em-dashes
in the delivered body.

## 6. Next-step arithmetic (operator decision, not fired)

A 64k refire worst case is $1.33 (12729 in + 64000 out), which EXCEEDS the
$0.94 remaining under the $2.00 cap. Options: raise the cap; fire the :batch
variant (catalog rates, typically 50 percent off per W4 receipt); or accept
the partial, since the three structural kills are family-independent and the
delta D1 to D3 text needed to act on them is already banked.
