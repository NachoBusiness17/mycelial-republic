# cialdini-scanner: the 7-pattern persuasion detector, built + wired

Lane: gala build-it-all / cialdini-scanner (division B) - 2026-10-03
Owner files: `tools/cialdini_scanner.py` + `tests/test_cialdini_scanner.py` + `tests/fixtures/cialdini/payloads_7.txt`

## Genesis (what this closes)

`watch/inbox/DOUBLE_DROP_20261001.md` (drop A): researchers ran 28,000 ChatGPT
conversations applying Cialdini's 7 influence principles to objectionable requests;
direct asks held at 33% compliance, persuasion framing reached 72%, the commitment
ladder drove follow-up compliance to ~100%. The estate is feed-driven: X-dig and
scout lanes mine hostile web content and act on it, and "our gates block secrets
and SSRF; nothing scans INGESTED CONTENT for persuasion-pattern payloads aimed at
the lane that reads it" (same file, "Why it hits the estate DIRECTLY"). The
mcp-security census (`watch/inbox/burn_reset_20260927/flash50/mcp-security.md`)
frames the intake-path hole under indirect injection via fetched content (A4) and
the gap list (its numbered item 2: prompt injection via tool outputs has no
protocol-level MUST; the Cialdini class is the enumerated payload family for it).

## What landed

1. `tools/cialdini_scanner.py` - deterministic stdlib-only detector, prompt_lance
   shape (`mag/prompt_lance.py`: schema const, line-located findings, sorted
   deterministically, byte-identical output, CLI `python tools/cialdini_scanner.py
   <file|->`). Schema `cialdini_scanner.v1` (:58). 7 patterns at :76, each a regex
   family with per-regex confidence weights, finding confidence = max matched
   weight, one finding max per (pattern, line):
   - authority (0.70-0.90): role/official assertion aimed at making the reader comply
   - commitment (0.70-0.90): tiny yes before big ask
   - social_proof (0.70-0.80): count + cohort
   - scarcity (0.70-0.90): deadline / limited supply
   - unity (0.75-0.85): in-group frame
   - reciprocity (0.70-0.90): give-then-ask hook
   - liking (0.75-0.85): flattery mirror
   `HIGH_RISK = 0.7` (:61) is the wiring threshold; `high_risk_patterns()` (:272)
   returns the at/above-threshold pattern ids.
   Regexes match payload shapes (role+command, tiny-yes-then-big-ask, count+cohort,
   deadline+scarcity, in-group+concealment, give-then-ask, flattery+exception), not
   bare topic words - that is what keeps estate receipts clean (see finish line).
2. X-dig intake wiring - both churn tools now flag scanned posts at the read path:
   - `tools/x_churn_cli.py:114` `cialdini_summary()`; attached to every filed hit
     row at :157 (key `cialdini`: n_findings, worst_confidence, patterns, verdict);
     MD map gains a PERSUASION-FLAG line at :181-183 when a hit carries payloads.
   - `tools/x_churn_grok.py:170-182` defines the same cialdini_summary helper;
     the candidates loop attaches it at `tools/x_churn_grok.py:199-203` and
     `hits.append(c)` rides it into the JSONL and the MD map.
   Flag, not block: the row enters the estate with the payload class riding it, so
   the reading lane sees the persuasion shape, not just the gist.
3. Scout read-to-action gate - `mag/frontier_scout.py:465-491` inside
   `queue_steal_task()`: before an ingested finding converts into a spawned task,
   its description + adaptation_plan are scanned; at or above HIGH_RISK the queue
   refuses with the pattern list and confidence riding the refusal, and
   `spawn_task` never runs. Clean findings queue as before and carry a
   `persuasion` block in the result.
4. Tests - `tests/test_cialdini_scanner.py`, 28 tests: fixture detection (all 7),
   per-line pattern isolation (no cross-fire), zero-FP on 8 clean estate receipts,
   benign meta-discussion does not fire, per-pattern signature payloads, exact
   confidence weights, determinism, message-dict input, finding shape, cap
   truncation, gate list, X-dig summary wiring, scout gate block + pass paths, CLI.

## Finish line (commands + raw bytes)

Raw output: `watch/inbox/gala_20260925/build-it-all/lanes/cialdini-scanner.check.txt`

- [1] `./.venv/Scripts/python.exe -m pytest tests/test_cialdini_scanner.py -q -p no:cacheprovider`
  -> 28 passed, exit 0.
- [2] `./.venv/Scripts/python.exe tools/cialdini_scanner.py tests/fixtures/cialdini/payloads_7.txt`
  -> 7 findings, 7 patterns hit, worst 0.90, exit 0. The fixture carries one payload
  paragraph per principle; each paragraph fires exactly its own pattern.
- [3] Zero false positives: the same CLI over 8 estate-authored receipts ->
  0 findings each, CLEAN:
  `watch/inbox/census_refresh_20261002.md`, `watch/inbox/instance_guard_20261002.md`,
  `watch/inbox/last_mile_20260930/B17_CENSUS.md`,
  `watch/inbox/burn_wave_20260926/B2_216_collect_delta_20260926.md`,
  `watch/inbox/fillball/citation-lint.md`, `corpus/steal/ZCODE_RATCHET_LANDED_20260924.md`,
  `watch/inbox/ENVELOPE_50W_HIT_20260926.md`, `watch/inbox/SCOUT_CHARTER_20260926.md`.
- [4] Wiring smoke: `tools.x_churn_cli.cialdini_summary(payload)` -> 1 finding
  commitment 0.90; `tools.x_churn_grok.cialdini_summary(payload)` -> 1 finding
  unity 0.85; `FrontierScout().queue_steal_task('does-not-exist-zzz')` unchanged
  miss path. Exit 0.
- [5] Ratchet (the ask's named check):
  `./.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
  -> first run FAIL exit 1 with one NEW finding owned by this lane
  (except-pass tools/cialdini_scanner.py:53, copied from the prompt_lance console
  guard); fixed in the FW-46 shape (reason named on stderr, `mag/afk_loop.py:36-37`),
  no debt registered. Re-run: "RATCHET: PASS - no unregistered debt.", exit 0, NEW=0.
  The remaining output line is a GROWTH claim on `mag/percolator.py` (accepted at
  580 lines, now 1022, +442) - not this lane's change; left for its owner to
  re-audit or re-accept by name.

## Honesty notes

- The mcp-security gap numbering: its numbered item 7 is the tamper-evident audit
  tape gap; the ask's own gloss ("persuasion patterns on the intake path, the
  Cialdini class") points at the indirect-injection section (A4) and gap item 2.
  Both were read; the ask's gloss governs, and this receipt names the discrepancy
  rather than silently renumbering.
- The 28K-conversation study identity is tri-stated UNVERIFIED in the source drop
  itself; this build banks the attack CLASS (real, established literature lineage
  per the drop), not the paper's exact identity.
- The scanner is a lens, not an authority: it flags and rides rows; the switchboard/
  effect broker still authorize any effect (house law). False negatives are expected
  at the margins (regex floor, $0, deterministic); the confidence weights are
  tunable per regex in `PATTERNS`.

## Decision ledger

Closes: the DOUBLE_DROP probe's detector leg - "the 7 patterns are enumerable ...
a deterministic scanner beside prompt_lance and the secret gate, on the intake
path. Landing spot: the X-dig and scout lanes' read path." The probe's other leg
(does a live test lane comply off-charter under a seeded payload) was NOT run by
this lane; the scanner gives the next lane the instrument to run it.

## Falsifier

- A mined X post or scout finding carrying an obvious authority/commitment/unity
  payload that scans CLEAN on intake = the regex floor is too low; raise weights or
  add the missed shape to the family.
- A clean estate receipt that starts flagging = the regexes drifted from
  payload-shape to topic-word matching; tune the family, never the receipts.
