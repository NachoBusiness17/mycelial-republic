# IMP3 D3 identity-bytes amendment (2026-09-30)

Mission (operator): Opus AA1 read-side kill 3, "identity is a label, not
bytes - model_id repointable". Draft AMENDMENT 10 on
watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md (FILE OWNERSHIP:
this lane). Requirements: model_fingerprint column (sha256 of a canonical
probe battery response), rows group by (model_id, fingerprint), fingerprint
change = new capability cell at cold start, never silently merged; probe
battery spec'd cheap (5 fixed prompts, temperature 0, first-token logprob
digest); migration note (existing rows grandfathered UNKNOWN until first
re-probe). Spec-only; no code touched.

## 1. The kill, source-cited

watch/inbox/last_mile_20260930/AA1_OPUS_REFIRE.md section 4, kill 3:
"IDENTITY IS A LABEL, NOT BYTES. The ledger keys on a model_id string any
operator can repoint to different weights; violates our own trust-bytes
law. Section 2 PK lacks environment identity."

## 2. Spec state read before drafting

BASELINE_SPEC.md through batch AH11 (AMENDMENT 7). Facts checked and
reused: capability PK was (model_id, task_shape, task_shape_version)
(section 2); 3.3's environment hash includes only the model TAG (the
repointable label itself); AMENDMENT 5's exploration band n < m is the
cold-start territory a new cell lands in; AMENDMENT 2's single serialized
transaction is where the battery binds; AMENDMENT 3 set the precedent for
an in-amendment DDL delta (principal.operator_id), which this lane follows
instead of AMENDMENT 6's in-place edit, so sibling lanes 8/9 (D1, D2) do
not collide on section 2.

## 3. What landed (BASELINE_SPEC.md batch IMP3, AMENDMENT 10)

- MODEL FINGERPRINT definition (part 1): sha256 over the probe battery
  response; observational identity of served weights, not proof of the
  weight matrix; endpoint excluded (same weights, two endpoints = one
  machine).
- Probe battery recipe (part 2): five frozen prompt literals, temperature
  0, max_tokens 1, top_logprobs 20; digest input = "gps-battery-v1" +
  compact JSON [[prompt_sha256, rank, logprob_string, token_string], ...];
  logprob decimal kept exactly as returned, never reformatted; battery
  version inside the digest makes any battery change auto-open fresh
  cells.
- Schema delta (part 3): capability PK becomes (model_id,
  model_fingerprint, task_shape, task_shape_version); verdict gains
  model_fingerprint inside signed row_sha256 coverage; probe_log gains
  probe_kind ('fingerprint' rows).
- Never-merge law (part 4): fingerprint change = new cell at n = 0 in the
  AMENDMENT 5 band; no transfer from the old cell; battery runs at session
  open and at the head of every verdict-insert transaction; a cell is
  routable only while its fingerprint equals the model's last measured one
  (reason_code fingerprint_mismatch); false splits cost a cold start,
  silent merges are impossible by construction.
- 3.3 environment hash gains the fingerprint (part 5); receipt
  chosen/considered entries gain fingerprint_short (part 6).
- Migration (part 7): existing rows grandfathered UNKNOWN, keep routing
  standing until first re-probe, then close to new verdicts; v0 db is
  fixture data so this is a fixture rebuild. New section 8 row F6 plus K5
  red-team additions (planted cross-fingerprint verdict rejected; mid-test
  weight swap forces old cell to history, new cell at n = 0).

## 4. Honest limits (named, not papered)

- Observational, not cryptographic: a repoint preserving every returned
  first-token logprob string is invisible.
- Cross-provider float formatting differences can split cells; splits are
  the safe direction (cold start), merges are not silently possible.
- Read-side exposure between battery runs is bounded by the next
  session-open battery; routing-time re-probe per decision was considered
  and left out (it would add a battery call to every route for a latency
  win the decay loop already approximates; revisit if K3-style incidents
  appear).

## 5. Costs and gates

$0 model spend; spec edit only. Em-dash count in the landed batch: 0
(file-wide grep 0). Amendment numbers 8/9 left reserved for sibling D1/D2
lanes per AA1 section 6. Receipt lane: watch/inbox/last_mile_20260930/.
