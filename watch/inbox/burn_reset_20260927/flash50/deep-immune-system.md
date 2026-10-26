# deep-immune-system: from innate to adaptive immunity in the Mag estate

DEEP item, banked 2026-09-28. Every organ named in the ask was read in full this
session, and three of the four were executed live; receipts are inline. The
question: the estate has innate immunity (fixed receptors built after each
outbreak). What would ADAPTIVE immunity look like, the kind that learns a
pathogen it has never met?

## 1. Diagnosis: what exists today is innate immunity

Read this session, all four organs plus the ratchet:

- **Secret gate** (`tools/secret_gate.py`, `tools/secret_gate_rules.py`,
  `tools/secret_gate_scan.py`): 31 hand-authored regex rules borrowed verbatim
  from `watch/inbox/burn_wave_20260926/B2_73_secret_scan.py` (rule table at
  `tools/secret_gate_rules.py:41-72`), a shannon-entropy floor of 4.3
  (`ENTROPY_MIN`), severity tiers, exit 1 blocks at high+, exit 2 means
  "detector blind" and callers must never read it as success
  (`tools/secret_gate.py:40-45`).
- **Fossil arm** (`tools/fossil_check.py` + `configs/fossil_registry.json`):
  6 hand-registered artifacts with per-entry staleness bars, dispositions
  recompile/tombstoned/fixed-oracle/watch (`tools/fossil_check.py:8-10`),
  optional `check_cmd` probes, and an operator-gated auto-healer
  (`--recompile`, `tools/fossil_check.py:16-19`). Its own law is fail-open:
  "a broken check never blinds the patrol" (header line 14).
- **Chain guard** (`mag/chain_guard.py`): a canary. The 2026-08-25 incident
  (header lines 3-11) was a pre-repair lineage restored over the live verkle
  chain by an unknown hand. The marker `verkle_repair_state.json` records what
  the repaired chain SHOULD look like; `check()` recomputes the merkle root
  from rows and compares to the tip (lines 96-107), and a raw-byte CR scan
  catches text-mode writers before reads are trusted (B2-83 tripwire, lines
  78-88).
- **Drift patrol** (`tools/census_drift_patrol.py`): a single-carrier tripwire.
  STALE = census older than 7 days AND the world moved under it (growth by
  git-add or disk shrink, `patrol()` at lines 250-288). Fail-closed on any
  claim that does not match the canonical grammar
  (`CENSUS_CLAIM_RE`, lines 117-119); a future-dated census is called a
  fabrication smell (lines 267-269).
- **Ratchet** (`tools/violation_ratchet.py`): fingerprint-gated violation
  register. Only NEW violations fail; debt enters the 941-claim baseline only
  by NAMED acceptance (`baseline-update --by WHO`, header lines 5-8), leaves by
  prune.

The immunological reading: every receptor here is a **pattern-recognition
receptor** with a fixed repertoire, and every one of them encodes a specific
pathogen the estate already survived. The secret gate's entropy gate S3 exists
because one rule emitted 48,427 hits, 80 percent of all findings, and buried
the one critical (`tools/secret_gate.py:16-22`). The no-CR tripwire exists
because B2-83 proved a text-mode write rewrote every LF to CRLF while content
verify stayed green (`mag/chain_guard.py:78-82`). The tip-vs-chain canary
exists because CHAIN_STOP proved silent tip divergence
(`mag/chain_guard.py:90-95`). The census grammar anchor exists because prose
numbers poisoned the parse (B2-245, `tools/census_drift_patrol.py:86-92`). This
is Burnet's clonal selection done at design time: the lymphocyte that survived
encodes the antigen. It works, but only against replays of diseases already
endured.

**Live receipts from this session's runs:**

- `python -m mag.chain_guard check` (run 2026-09-28): state **regression**,
  8,249 rows, 762 dangling, 522 dangling without the evidence_lost flag,
  tip_matches_chain true, crlf false, marker from 2026-09-26T16:39:15Z. The
  canary is standing in alarm today. Report only: resolving it is operator
  territory, and it is itself evidence for section 5 (an alarm that stays red
  for days trains dismissal, the exact disease B2-338 fixed in the census
  channel, `tools/census_drift_patrol.py:321-324`).
- `python tools/fossil_check.py`: green, 0 WARN, 0 HARD, 6 registered.
- `python tools/census_drift_patrol.py`: green; census 1 day old, 5 test files
  added since, disk 369 vs carrier 352 named as instrument lag inside the
  window. Note what just happened: the patrol named a 17-file disk delta as
  benign-by-construction, a judgment the code makes, not the operator.

## 2. The antigen presentation layer the estate is missing

Immunology's first move is not detection, it is presentation: innate cells
digest pathogens and display antigen so adaptive cells can learn. The estate
generates enormous antigen and digests almost none of it. The streams exist:
`watch/inbox/SECRET_SCAN_BEAT.jsonl` (2 rows; the tail row is still the legacy
pre-S4 fat shape carrying a whole file list, the 641,924-byte disease
`tools/secret_gate.py:24-27` was written to cure), census patrol logs,
fossil-check stdout, trails jsonl, the FKB signature baseline that Q-028/FW-47
rebuilt from 17 to 1,421 signatures (commit d90bc8607), the FW-03 grounding
chain of 137 hash-faithful rows (commit b34ccd3ba).

Design: one **antigen schema**, generalized from the one good example. The
secret gate already stamps rows `"schema": "secret_gate_beat.v1"` with counts
plus a results path (`tools/secret_gate.py:237, 255`). Extend that shape to an
estate-wide append-only `immunity/antigen.jsonl`: every organ appends
{tool, surface, verdict, counts, runtime, scope_basis, thresholds}. The APC is
then a single small reader (call it the lymph node) that renders per-day
self/non-self balance and, critically, keeps the time series the T-cells in
section 3 train on. Without a shared schema, no detector can ever see more than
one organ's world, which is exactly the silo the current system lives in.

## 3. The T-cells: trained detectors, each one specifiable from bytes the
estate already holds

A T-cell is a trained receptor whose repertoire is generated, not authored.
Five concrete candidates, all trainable on data that exists on disk today:

1. **Entropy-threshold T-cell.** The current 4.3-bit floor is a hand constant
   (`ENTROPY_MIN` in `tools/secret_gate_rules.py`). But the S3 run left a
   labeled corpus: 48,427 known-negative 40-char hits (git OIDs, hex SHAs,
   `tools/secret_gate.py:18-20`). Fit the null distribution of shannon entropy
   per file class from history and set the threshold by quantile. This converts
   the gate's weakest constant into a learned receptor and makes the floor
   provable instead of asserted.
2. **Beat-rate CUSUM T-cell.** Model each rule's hit rate across beats of the
   antigen stream with an EWMA or CUSUM (Page 1954; Roberts 1959 for EWMA;
   Chandola, Banerjee and Kumar 2009 survey the anomaly-detection ground). A
   per-rule sudden rate excursion means either a leak campaign or a rule
   misfire. Run against the S3 beat data, this detector fires on day one of
   the 80 percent flood, three days before a human hand-writes the entropy
   fix. This is the purest "learn a NEW threat" case in the repo's own history.
3. **Cadence T-cell.** The fossil arm watches 6 hand-registered artifacts with
   hand-set bars. But the estate runs a dozen scheduled surfaces (census patrol
   08:30, FTS index 09:00, improve 08:00 per AGENTS.md) whose logs already
   record START stamps. A detector that models inter-arrival time per surface
   and flags a gap whose probability under the surface's own history is below
   bar would have caught the B2-465 FTS decay class (AGENTS.md: the index
   decays to scan fallback and only detects, never heals) and the "no START
   stamp today means the surface is dark" case, automatically, for every
   scheduled surface, with no registry to maintain. mtime bars are the crude
   innately-authored version of a hazard-rate model.
4. **Semantic-drift T-cell for hash-faithful chains.** FW-03 verified all 137
   grounding rows hash-faithful, none edited in place (commit b34ccd3ba). Byte
   law holds. But hashes cannot see a LEGAL write of poisoned content through
   the sanctioned writer. A per-row embedding compared against a rolling
   centroid of neighbors detects content that is intact in bytes and wrong in
   kind. This is the one pathogen class no current organ even claims.
5. **Alarm-channel health T-cell (the idiotypic layer).** Jerne's idiotypic
   network (1974) says the immune system also regulates itself: antibodies
   have anti-antibodies. The estate's version: watch the watchers. B2-338 is
   the founding incident (`tools/census_drift_patrol.py:321-324`): a
   case-sensitivity mismatch took the WARN arm on every green push,
   "training operators to dismiss the channel." And the chain canary has stood
   red since 09-26. A detector that tracks per-channel false-positive rate,
   time-in-alarm, and operator-response latency treats cry-wolf decay and
   alarm-fatigue as the pathogens they are.

## 4. T-cell education: the thymus is half-built

An adaptive system that deploys naive detectors autoimmunizes. The estate
already owns the maturation machinery, unmerged into one pathway:

- **Negative selection** (Forrest, Perelson, Allen and Cherukuri 1994;
  Hofmeyr and Forrest's artIS, Evolutionary Computation 2000): candidate
  detectors are first exposed to SELF and any that bind self are destroyed or
  edited. The estate's forms: the percolator holds 352 invariants plus 13
  recorded false positives (`memory/percolator/invariants.json`, read this
  session: entries carry count/first_seen/last_seen/domain; false_positives
  count 13). The ratchet's day-one baseline is a negative-selection corpus for
  code debt: known-sick fingerprints are tolerized by registration
  (`configs/violation_baseline.json`, 7,590 lines of named claims). B2-387
  (`mag/chain_guard.py:162-174`) is negative selection in one sentence:
  marker-vs-chain root difference is EXPECTED drift, "ok/state/alarm never key
  on it."
- **Co-stimulation**: in Hofmeyr's AIS, a detector that fires must receive a
  secondary human signal within a tolerance window or it is tolerized away.
  That is already estate constitution, stated twice: fossil enforce is
  "operator-gated" (`tools/fossil_check.py:18-19`) and ratchet debt is
  accepted "by NAME" (`tools/violation_ratchet.py:6-8`). The design need only
  formalize it: a candidate T-cell runs WARN-only in shadow; each hit needs a
  named operator classification (self / pathogen / unknown) inside the window;
  self-classified hits append to the detector's tolerance set; unclassified
  hits age the detector out. This is exactly how the secret gate's ALLOW_RE
  grew its REDACTED/MASKED exemption concept
  (`tools/secret_gate.py:10-14`).
- **Promotion**: maturation completes when the percolator promotes a verified
  detector to a standing invariant with its receipt, which is the workflow
  gate's own contract (every check registers a row in
  `memory/workflows/REGISTRY.jsonl`, receipts land in `watch/inbox/`).

## 5. The antibodies: standing responses, and their regulation

Antibodies are cheap, fast, permanent effector shapes. The estate's existing
effectors, ranked by autonomy:

- exit 1 blocks the push (secret gate at high+, ratchet on new violations);
- the FTS daily task is the one true auto-antibody loop already running:
  detect exit 2, rebuild through the one sanctioned writer, escalate only if
  the heal fails (AGENTS.md B2-465 bullet);
- `--recompile` auto-heal, operator-gated (`tools/fossil_check.py:86-95`);
- census refresh ritual and pile habit are operator antibodies.

The adaptive law for new antibodies should copy the secret gate's block-tier
doctrine (`tools/secret_gate.py:29-31`): only SPECIFIC shapes may block,
generic shapes report; and its baseline doctrine: day one is zero, acceptance
is named. Class-switch is the act of encoding a confirmed novel pathogen as a
permanent innate receptor in the organ that owns its surface: a regex into
RULES, a check_cmd into the fossil registry, a canary into chain_guard, each
with the fix-comment-carries-receipt rule AGENTS.md build discipline already
mandates. Every current receptor in the estate is a former antibody from
exactly this process; the design's contribution is to make the pipeline
explicit instead of archaeological.

**Autoimmunity guardrails**, each with a founding incident in-repo:
scope restriction so an effector can only act inside its own domain
(`scanner_domain()`, `tools/violation_ratchet.py:64-68`, born from B2-95 when
a prune reaped 25 foreign mimosa claims); expected-drift carve-outs so a
healthy change never alarms (B2-387); and the channel-health T-cell of
section 3.5 so the system cannot quietly rot into dismissal (B2-338, and the
chain canary's 2-day red standing today).

One doctrinal note on danger theory: Matzinger's danger model says respond to
damage signals, not to foreignness per se. The estate already leans this way
and should keep it: chain_guard alarms on unflagged dangling rows (damage),
census patrol alarms on "old AND world moved" (mismatch), and everything fails
CLOSED because exit 2, cannot-verify, is itself a damage signal
(`tools/secret_gate.py:44-45`, `tools/census_drift_patrol.py:23-28`). An
adaptive layer must not invert this into novelty-hunting: unknown is not
automatically non-self; damage is the alarm key.

## 6. Smallest real build order

1. Antigen schema: generalize `secret_gate_beat.v1` to all organs, one
   append-only stream. Pure schema, no new detection.
2. Beat-rate CUSUM over that stream (pure python, no deps) with WARN-only
   output. Replays S3 correctly and would have caught it early.
3. Cadence T-cell over existing cron logs (MagFtsIndexDaily,
   MagCensusPatrolDaily, MagImproveDaily): hazard-rate gap alarm.
4. Wire candidate T-cell outputs through the percolator as shadow invariants;
   13 false positives already recorded there become the first tolerance set.
5. Entropy-quantile refit from the 48,427-hit S3 corpus.
6. Class-switch ritual doc: verified pathogen to permanent receptor, named,
   receipted, in the organ that owns the surface.

## 7. Not done here

No new gates were landed; this is a design item. The chain-guard regression
observed live (522 unflagged dangling rows, marker 2026-09-26) is reported,
not resolved; per the tool's own law
(`mag/chain_guard.py:143-150`) that state is a genuine regression alarm and
belongs to the operator, not to a design essay. The percolator invariant count
in live bytes is 352, not the 47 quoted in fleet skill prose; the live file is
the truth (`memory/percolator/invariants.json`).
