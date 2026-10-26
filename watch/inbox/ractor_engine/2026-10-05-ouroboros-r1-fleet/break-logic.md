# BREAK-LOGIC hostile pass (ouroboros r1 fleet, logic lens), 2026-10-05

Instrument and moment: every cite below was byte-checked this sitting (2026-10-05) by direct file reads
(tools/mickey17_v2_fold.py full; .zcode/workflows/ractor-engine.dwf.ts full; tools/workflow_gate.py :150-385;
.zcode/workflows/olm-mine.dwf.ts targeted; .zcode/workflows/mickey17-v2.dwf.ts :240-250) and three fresh
censuses run with .venv/Scripts/python.exe against memory/workflows/REGISTRY.jsonl and
memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/ (scripts inline in the transcript, outputs pasted below).
Nothing was edited; no workflow was fired; the fold script and the gate's --script mode were NOT executed
(they mutate state), so all fold/gate claims below are source-reads, not run outputs.

## Verdicts

### 1. Fold PRISMA tautology + exclusion-hides-corrections: CONFIRMED

- Tautology byte-proven from the full source: tools/mickey17_v2_fold.py:187-193 increments exactly one of
  {excluded["1 phantom-source"], excluded["9 verifier-unconfirmed"], included} per row (if/elif/else),
  :194 sets identified = len(all_rows), so the assert at :200-201 holds on every possible input. The
  counter-partition argument is correct; the assert is dead bytes.
- The 6 rows riding included under excluded:0 are byte-confirmed in BOTH addenda, not just quoted:
  run-0 addendum watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md:52 (a08 r9, persisted
  verdict "unconfirmed" at a08-rails-laws.checks.json deep_tier2[2], fold printed excluded:0, its own
  fixed-string ledger :133-134, :149) and read-estate addendum watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md:70-71
  (5 substantive unconfirmations r04#1 + r05#0-#3 rode included while the fold printed excluded:0; decode
  recipe at :384-385). The mechanism is worse than the lens stated: TWO wiring defects (addendum :52, :65-68):
  the fold reads a top-level `unconfirmed` key that exists in 0 of 12 checks files, AND the match shapes can
  never meet (norm(claim)[:80] vs lane-prefixed row_key, no claim field at all on deep_tier2 entries).
- Disposition conflict byte-confirmed: MASTER_READ_ESTATE section 10 "Standing numbers (conditions, never
  averages)" renders the corrections as the standing numbers (910 not 917/376, 28 not 30, 250 not 160,
  86.01/89.3 not 89.4-with-ALL) and "the struck values do not get averaged back in"; TS-07 and TS-10 render
  two of the unconfirmed rows as TOP STEALS carrying their corrections. Code-9 exclusion would demote these
  to an aggregate count. Falsifier stands unmet: no instrument renders code-9 rows inside FOLD_SECTIONS.md
  (the fold script only prints per-reason counts, :198).
- Two precision dents, neither fatal: (a) the "LAW 3" label does NOT exist in either master fold or either
  addendum (grep this sitting: only "Law 7" at MASTER_READ_ESTATE:43 and MASTER_MICKEY17_V2:52); the substance
  is section 10's header + refuse-to-average clause, so cite the section, not a nonexistent law number.
  (b) the parenthetical names 4 corrections where the addendum (:395) counts 5 (the 136-line .env / struck
  137/137 is the omitted fifth).

### 2. Registry dual-instrument + write-only warn layer: CONFIRMED (one overbroad universal corrected)

- My census reproduces the lens's numbers EXACTLY: 88 rows, PASS 75 / FAIL 13, 74 non-ok checks, per-gate
  distribution G6 28 / G3 16 / G4 7 / G7 6 / G2 6 / G5 5 / G1 4 / G8 2 (python over REGISTRY.jsonl, this
  sitting). 32 non-ok check instances ride PASS rows: byte-confirmed. 17 ractor-engine rows, all PASS, all 17
  carrying G6 soft-false with the identical stamp reason: byte-confirmed.
- Precedence cites verified: tools/workflow_gate.py:192 (soft rows excluded from failed) feeding :354
  (verdict = "PASS" if not failed). Soft-flag minting at :176-185 (G6 t69, G3 B2-206).
- CORRECTION (the universal "none reads checks[].ok" is overbroad by one file): workflow_gate.py ITSELF reads
  persisted checks[].ok at :239-241 (validate_card over load_registry_index, scenario-card citation). But that
  sole reader interrogates only cited FAIL rows; zero files act on soft rows or warn counts. Re-censused
  UNTRUNCATED across tools/ + mag/ + scripts/ + tests/: consumers are visor.py:233 (tail display),
  mag/improve.py:2592-2604 (reads (ts,digest) keys only, never checks), tools/gate_canary.py:48 (path
  sentinel), workflow_gate.py (producer + FAIL-row card validation), plus two docstring/notes mentions. The
  falsifier's real challenge (a consumer acting on soft rows) remains unmet; the correction STRENGTHENS the
  finding: even the registry's only checks[].ok reader is blind to the warn layer.
- Precision: the warn layer on engine rows is 17 constant stamp warns + 1 substantive one (2026-10-02T01:47:21Z
  engine row also carries the G3 judge-independence soft warn, B2-60 D2). "Zero information per fire" is true
  of the G6 stamp warn specifically (17/17 identical), not of the engine's warn layer as a whole.

### 3. Ractor engine fabricates its output verdicts: CONFIRMED

- All line cites verified against the full file this sitting: :338 status "verified" as const and :339
  severity "medium" as const hardcoded on every ranked move; :341-346 verified[] claims; :290
  survivors.push(...pass.additions) pushes breaker-authored additions into the same "verified" pipeline with
  no check; :253-273 revision merged into a local `merged` LensReport with no file write; :316-323 the only
  banked-file check is the SYNTHESIS.md glob; the lens-phase bank ask at :188 is ungated (no glob for
  OUT/<id>.md anywhere).
- Falsifier sweep re-run WIDER than the lens's: `find watch/inbox/ractor_engine -name "*.rev.md" -o -name
  "WITHDRAWALS*"` across all 9 bank folders returns zero hits. No revision or withdrawal file exists anywhere
  in the engine's history; withdrawals have no schema representation at all (the revision ask at :253-259 can
  only return findings, so a withdrawal can only be an omission, and the omission is banked nowhere).

### 4. Tier-1 no-rate measures genre, not fidelity: CONFIRMED (delivered text truncated)

- My independent decode of memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes/ reproduces every number
  byte-exact: 8 lane files / 7 checks files (e06-fidelity-audit has no checks file), key-length census
  supports 15 / checks 10 / entries 5 / rows 5, 35 verdict-bearing entries with 26 yes / 9 no (25.7% no),
  deep_tier2 entries total 0. The verdict field is named `supports` (values yes/no) inside all four key
  families, matching the lens's decode method.
- Cross-run numbers byte-confirmed in the addenda: run-0 63 no / 12 yes of 75 (84%) at run-0 addendum :48;
  run-2 48 no / 12 yes of 60 (80%) at read-estate addendum :57.
- The genre mechanism is visible in the exec reasons themselves, which the lens did not quote:
  e01-index-compact.checks.json supports[0].reason: "Quote is execution output (the tool's PROFILE line),
  not prose, and it carries the claimed facts digit-for-digit ... -> yes" vs supports[1].reason: "Quote is a
  3-line source fragment ... written code, not the output of any command ... -> no". The verdict tracks the
  quote's genre exactly as the finding claims.
- Caveats: the finding text delivered to this breaker was TRUNCATED mid-sentence inside its own evidence
  ("...the fold prints the ratios beside a key-name lot" then nothing), so this verdict covers the delivered
  portion; the key-name-lottery tail is independently confirmed by the fold source :156-162 (vc[k] += len(v)
  counts list lengths, never verdict values). "Measures genre, not fidelity" is an n=3 causal claim with
  confounds (different checker seats, run-3 has zero tier-2 at my moment), but as a prohibition on cross-run
  ratio gates it stands and the mechanism is byte-visible.

## Additions (what the lens missed)

### A1. The 6000-char breaker slice makes un-verdicted findings SURVIVE by default, and it bit this round (CONVERGENT with finding 3)

ractor-engine.dwf.ts:240 slices the lens report to 6000 chars before the hostile pass sees it
(JSON.stringify(s.value).slice(0, 6000)); the survivor filter at :283-289 drops ONLY findings whose exact
string is in the killed set, so any finding past the cut is never byte-checked yet rides to synthesis.
Live evidence: this round's banked lens write-ups measure 11,497 to 20,788 bytes (accuracy.md 20,221;
logic.md 20,788), and the lens report delivered to THIS breaker ends mid-sentence inside finding 4, i.e. the
truncation fired on the logic lens's own report this sitting. This widens finding 3's fabrication from
"breaker additions" to "every finding the breaker never saw", all stamped verified by :338.
Falsifier: a lens report whose JSON under 6000 chars reaches the breaker intact (true for short reports; the
defect is silent exactly when reports are long, which the bank sizes show is the normal case).
Move: ~10 min: raise the slice to the synthesis budget (24000, :304) AND make survival verdict-positive
(survive only what a verdict says confirmed, plus revision outputs; anything absent from the verdicts is
tagged "unreviewed", never "verified"); while there, replace the exact-string weakened match at :266 with
id-based matching (paraphrased verdict strings silently never steer today).

### A2. The hardcoded-status class is fleet-wide: a second instance the blind-spot list concealed (CONVERGENT with finding 3)

.zcode/workflows/olm-mine.dwf.ts:496-497 hardcodes the identical status "verified" as const / severity
"medium" as const pair on its topSteals findings. Weaker instance: olm-mine DOES gate substance upstream
(:357-358 confirmed.push only on the confirmer's verdict; :350-354 unconfirmed tracked with evidence), so
only the status bytes are decorative there, whereas ractor-engine has no gate at all behind its stamp.
Census this sitting: grep '"verified" as const' over .zcode/workflows/*.dwf.ts returns exactly these two
files. The amendment should fix the class (compute status from the instrument), not one file.
Falsifier: a third saved workflow hardcoding status (census says no); or an olm-mine confirmed:false item
reaching topSteals (the :357 filter prevents it).
Move: rides finding 3's edit, +2 min to mirror the computed status in olm-mine.dwf.ts:496.

### A3. The dual-instrument split is airtight and quantified: 74 non-ok = 40 hard + 34 soft; PASS rows carry 32 non-ok, ALL soft

Fresh census this sitting: PASS rows hold 32 soft + 0 hard non-ok checks; FAIL rows hold 40 hard + 2 soft.
So verdict PASS iff zero hard fails is a perfect invariant over all 88 rows: the gate is internally
consistent, and the entire defect is that the 32 warns riding PASS rows are unreadable by any consumer
(A3's census in verdict 2). This also prices finding 2's amendment as zero-risk: no consumer reads a warns
field today, so adding one breaks nothing.
Falsifier: a PASS row carrying a hard (non-soft) non-ok check (census this sitting: zero such rows).
Move: rides finding 2's amendment (workflow_gate.py:354-372 "PASS (N warns)" + top-level warns array); the
census numbers above are the pre-edit baseline to pin in a test.

## Not run (stated honestly)

- The fold script and the gate's --script mode were not executed (both mutate estate state: FOLD_SECTIONS.md
  rewrite, registry append). All fold/gate claims are full-source reads plus the addenda's own run outputs.
- No workflow was fired; run 3 (dwfrun-e9656e14) state was read only from disk lanes; harness-side run state
  (ListWorkflowRuns) not attempted.
- The 13 unopened saved workflows stay unopened except olm-mine (targeted) and mickey17-v2 (:240-250 targeted);
  fleet-death verdicts for the rest remain the siblings' claims, not mine.
