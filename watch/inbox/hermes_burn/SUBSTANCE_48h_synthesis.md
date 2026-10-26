# SUBSTANCE_48h_synthesis (anthropic/claude-opus-5.5, turn 1, channel: content)

# ENHANCEMENT PASS: 48h synthesis (THE OWED WALTZ + laws / lattice / steals chapters)

**Conditions of this pass.** These conditions apply to every claim below.

- **Instrument:** a read of four evidence files exactly as pasted into this prompt:
  - watch/inbox/48h_synth/STORY.md
  - watch/inbox/48h_synth/laws.md
  - watch/inbox/48h_synth/lattice.md
  - watch/inbox/48h_synth/steals.md
- **Moment:** after the ERRATA dated 2026-10-01 that STORY.md section 5 embeds.
- **Context:** no disk, git, or code access.
- **Citation rule:**
  - The evidence files arrived without line numbers, so citations into them are section anchors with quoted bytes.
  - Every code file:line below is "as asserted by the synthesis". This pass has not read it, so each one is UNVERIFIED.
  - I took no measurement of my own. Every number is the synthesis's number, carried with its stated conditions.

---

## PART 1. THE 5 W'S AUDIT

### 1a. The twelve inventoried laws (laws.md)

Column notes:
- **WHO** is the minting actor (operator order plus seat or lane) and the instrument that proved it.
- **WHEN** separates PROVED (an instrument fired and produced a result row) from ASSERTED (prose, commit message, or registration bytes only).
- **WHERE** paths are asserted by laws.md and "battery-verified" per laws.check.txt run 2 (misses=0). That battery file was not in my evidence, so every WHERE cite is UNVERIFIED.

| # | Law | WHO / instrument | WHAT (one sentence) | WHEN: proved vs asserted (evidence row) | WHERE (asserted file:line, UNVERIFIED this pass) | WHY for next window |
|---|---|---|---|---|---|---|
| 1 | One-bug law | Operator ("now everywhere one bug, many jackets") plus seat. Instrument: commit 98071f556 rib addendum | A verdict consumed without the instrument, moment and context that produced it is unfired. | General form ASSERTED (prose). Named instances PROVED by their own lanes. Row: laws.md §1, "the general law is PROSE in memory/rib/RIB_DRIVING_LADDER_20260928.md:53-76" | Prose: RIB_DRIVING_LADDER:53-76. Instances: tools/workflow_gate.py:281,312; tools/stealth_driver.py:460; conftest.py:14-23; tools/corpus_lens_run.py:45 | Highest-leverage law. Part 2 finds the synthesis itself violating it at least three times (R5, R6, R13). |
| 2 | SPEND THE MONEY | Operator third strike. Instrument: none | Judgment-class work dispatches to the funded tier, and every paid call banks tokens in/out. | ASSERTED only. laws.md §2: "PROSE-ONLY, honestly. No exit code." | UNWIRED (rib :39-51 plus AGENTS.md bullet, prose) | Its own check already fails on the record: grok-4.7 banked "usage 5,365 tokens" with no in/out split and no USD (STORY §8). See R16. |
| 3 | Seat law gate r1: bare python blocks | Seat, commit 185965898. Instrument: PreToolUse hook | A Bash/Write/Edit invoking bare `python` exits 2 with the AGENTS.md citation. | Rule bytes and registration "battery-verified". Live fire NOT re-proven: laws.md "Checks run": "Live fire of the seat law gate: not separately re-proven this session" | tools/seat_law_gate.py:37, :76-83. Registration C:/Users/foste/.zcode/cli/config.json:50 (outside the repo) | Enforcement of all other conduct law rides on this hook. Its registration lives outside git (R18). |
| 4 | Seat law gate r2: no em/en dash | Same commit. Same hook | A newly authored watch/inbox file with U+2013/U+2014 exits 2. | Same as #3. Mint act: the commit normalized 5 dashes in the elder receipt | seat_law_gate.py:38, :84-107; config.json:50 | Cheap, high-visibility. A live fire is owed (Part 3, C). |
| 5 | Seat law gate r3: *.dwf.ts gated pre-landing | Seat, commit 9a912c32e. Pre plus PostToolUse | A Write of a workflow script whose payload fails workflow_gate is blocked RED. | PROVED in effect by REGISTRY rows 36/37/39 FAIL/PASS/FAIL on temp .dwf.ts (STORY §6). Those rows are also the bug of #6 | seat_law_gate.py:43-65, :108-112; seat_law_postgate.py:30-45; config.json:84 | Closes the AmendWorkflow escape hatch, but PostToolUse "cannot block; it witnesses". |
| 6 | --no-register | Seat, commit 26eacaae7 "BUG KILL" | A payload gate-check is a verdict and must not append a REGISTRY row. | Defect PROVED ("4 live seatlaw_* rows confirmed", battery J1). Fix ASSERTED; no post-fix row-delta measured | tools/workflow_gate.py:281-286, :312-314; caller seat_law_gate.py:50 | Possibly already falsified by the 23:36Z rows. The timezone is unstated (R6). |
| 7 | Dash-introduce edge | Same commit | Only newly introduced dashes block. Historical re-saves pass. | PROVED at mint: "historical re-save 0 blocks, new dash 2, edit-fragment dash 2, LAW-12 scenario suite 7/7" | seat_law_gate.py:89-102 | Best-proved law in the inventory. It shows how a gate avoids teaching seats to route around it. |
| 8 | Hermetic-basetemp | suite-burn lane (wave5) plus driver-meter (ball3). Instrument: pytest, two basetemps | Suites must be hermetic to basetemp location, and code must be correct when basetemp is outside the repo. | PROVED two-direction: "the same 13 nodes green in-repo and red out-of-repo in the same session" (STORY §3). Ball3 "52 passed x2 under an external basetemp" | conftest.py:14-23; stealth_driver.py:460; mag/agent_state.py:177; tools/violation_ratchet.py:307-310; tools/config_seal.py:119-122 | ~1,072 tests were added between run 3 and the 09-30 census. Each new file is an unproven member of the class (Part 3, A). |
| 9 | Ordered-reports determinism | Ball driver authors. Instrument: none (control flow) | Concurrent phases dispatch on a stable division ORDER sort that never alters ask text. | ASSERTED. No two-run comparison is recorded. laws.md §9: "no exit code of its own" | .zcode/workflow-drafts/Ball3-suite-green.dwf.ts:101-104; Burn-48h-synthesis.dwf.ts:103-104 (drafts) | Covers drafts only. Whether the saved gated workflows (e.g. olm-mine) carry the sort is UNWIRED/UNVERIFIED. |
| 10 | Census denominator B2-216 | Burn wave 09-26 | Never difference two counts without naming instrument, moment and delta. | PROVED by incident: 1,837 collected vs 1,776/1,782 executed (B2_216_collect_delta_20260926.md) | AGENTS.md census bullet (no line); tools/census_drift_patrol.py parse_carrier (no line); MagCensusPatrolDaily 08:30 | The synthesis's own Coda breaks it (R5). |
| 11 | Minimal-exposure | Operator catch, commit 76e29cd0b | Scripts load only whitelisted env vars, never the full .env. | ASSERTED by commit. No post-fix probe of the "46 live values" count | scripts/run_mate.ps1:61-68 | This is key hygiene. Hermes move 1 (rotate xAI key) has no completion receipt in evidence (R17). |
| 12 | No-env-dump | Commit f4e2c247f | Mates never dump env into transcripts or receipts. | Persona line ASSERTED (prose). Redaction hook and precommit check ASSERTED by commit | configs/mates.yaml:17-19 (prose); hook in 76e29cd0b; precommit_secret_check in 03738963e (no file:line) | The code legs have no file:line in evidence, so they are UNWIRED-as-cited. |

### 1b. Laws minted in STORY/lattice but absent from the laws.md inventory

| Law | WHO / instrument | WHAT | WHEN | WHERE | WHY |
|---|---|---|---|---|---|
| Silent-eraser budget law | render-pipe lane. Instrument: 6-mode render check | "a budget smaller than the core it must deliver is not a budget, it is a silent eraser" (lattice Insight 1, quoting render-pipe.md) | PROVED: 0/6 to 6/6 modes, check in render-pipe.check.txt | mag/context_pack.py:1107-1131, :1142-1147, :1148-1153 | Most portable design law in the window. Not inventoried by laws.md. |
| Slug law (deterministic replay) | Operator order plus mine lane | "the script cannot read clocks", so the caller passes the date and each day banks to its own folder | ASSERTED via commit 6a1c70ec9. Slug format already diverges (R11) | .agents/skills/frontier-mine/SKILL.md "The ritual" | Prevents the overwrite that destroyed the predecessor fold. |
| Mine failure law | Two 09-29 deaths | Root-cause the script and AmendWorkflow with path; "never refire blind" | PROVED by lineage (REGISTRY lines 31-35, 38 PASS) | SKILL.md "Failure law" (prose) | Governs the daily cron that is now live. |
| Cadence law | Hermes prime judgment, paid | "things without cadence die" | ASSERTED (paid judgment, n=1) | UNWIRED as law. The tapestry bake is at 09:15 per SKILL.md | Lattice says tapestry is "owed its own dance". |

---

## PART 2. THE ROT

Each item gives: the claim, why the evidence alone falsifies or stales it, and the exact check that settles it. Commands use `.venv/Scripts/python.exe`, never bare python, which seat law r1 blocks.

**R1. Percolator line drift (FALSIFIED by sibling chapter).**
- **Claim:** STORY §5 cites "recurrence-only promote at mag/percolator.py:264-272" and "dormant paired-blind gate at mag/seed_percolator.py:6-16".
- **Contrary evidence:** steals.md M7: "the Z15 law (2026-09-29) moved it - the recurrence-only repeat branch now sits at mag/percolator.py:353-388" and "mag/seed_percolator.py:7-12 with thresholds at :33-35".
- **Check:** `sed -n '264,272p;353,388p' mag/percolator.py` and `sed -n '6,16p;33,35p' mag/seed_percolator.py`, then stamp each with `git log -1 --format=%cI -- <file>`.

**R2. "24 repair lanes danced" (FALSIFIED internally).**
- **Claim:** Coda: "24 repair lanes danced (12 + 9 + 3)".
- **Contrary evidence:** STORY §2: "9 lane JSONs, 8 danced and 1 buried". 12 + 8 + 3 = 23 danced. 24 is the lane-JSON count, not the danced count.
- **Check:** read the danced/buried line in watch/inbox/gala_20260925/ball-20260929_RECEIPT.md section 1.

**R3. Paid-judgment count (FALSIFIED internally).**
- **Claim:** §8 says "Three paid judgments banked". The Coda says "4 paid judgments banked (prime x2, grok-4.7, duel)".
- **Resolution:** pick one denominator: funded-tier judgments (3), or any paid dispatch (4, counting the 0.0248 USD duel).
- **Check:** `rg -l "cost" watch/inbox/HERMES_PRIME_JUDGMENT_20260929.md watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md watch/inbox/GROK47_LUNCHEON_INTEL_20260929.md watch/inbox/DAY_SYNTHESIS_20260929.md`, then count rows carrying a USD figure.

**R4. "5 mined laws in wave5" (FALSIFIED internally).**
- **Claim:** the Coda attributes five mined laws to wave5.
- **Contrary evidence:** STORY §2 says wave5 was "all division B", and the five laws were mined by "division A's heads-abliteratus" in ball-20260929.
- **Check:** `rg -n "mined" watch/inbox/gala_20260925/wave5-repair_RECEIPT.md watch/inbox/gala_20260925/ball-20260929_RECEIPT.md`.

**R5. Coda differences incompatible counts (VIOLATES law 10).**
- **Claim:** "2,568" (green, from Hermes move 2) is read against "3,550 tests collected" to conclude "the landing rate did not slow".
- **Why this breaks law 10:**
  - The two numbers come from different instruments: passed vs collected.
  - They come from different moments: 09-29 vs 09-30.
  - The 2,568 has no derivation in evidence. Run 3 reads 2452 passed + 14 failed + 12 skipped = 2,478 executed.
- **Positive example (lawful form):** "run 3, external basetemp, 2026-09-29: 2,452 passed of 2,478 executed. B17 census, `pytest --collect-only`, 2026-09-30: 3,550 collected. Not comparable: different verbs."
- **Negative example (what the Coda did):** "2,568 green ... 3,550 collected says the landing rate did not slow."
- **Check:** `rg -n "2,568|2568" watch/inbox/gala_20260925/ball3-suite-green_RECEIPT.md watch/inbox/HERMES_PRIME_JUDGMENT_20260929.md`, which names its instrument or proves it has none.

**R6. Seatlaw rows: count, framing, and a possible law-6 falsification. This is the window's highest-value rot.**
- **(a) Count.** STORY §6 names three rows (36, 37, 39). laws.md §6 says "4 live seatlaw_* rows confirmed".
- **(b) Framing.** STORY frames the rows as the gate "caught passing its own exam". laws.md classifies them as junk pollution minted by the bug ("a check mistaking itself for a landed fact"). Both cannot be the product.
- **(c) Timing.** The rows are stamped 23:36Z. The --no-register fix is "2026-09-29 20:04" with no timezone. If 20:04 is UTC, rows minted after it satisfy law 6's own falsifier ("any hook payload gate-check that appends a row ... means the flag stopped being passed"). If 20:04 is local UTC-4 or later, the fix landed after the rows and the law survives. The moment was stated without its condition. That is law 1's exact jacket.
- **Check:** `git show -s --format=%cI 26eacaae7` plus `rg -n "seatlaw_" memory/workflows/REGISTRY.jsonl`, comparing each row's ts in UTC against the commit's UTC instant.
- **Settles:** any seatlaw row whose ts is later than the commit falsifies law 6.

**R7. Lattice Strand 1 "nothing committed" (STALE).**
- **Claim:** the lattice says "the entire 48h lattice exists only as working-tree edits".
- **Contrary evidence:** the same synthesis cites later commits:
  - 185965898, 9a912c32e, 26eacaae7, 98071f556 (09-29)
  - 76e29cd0b, f4e2c247f (09-30)
  - 6a1c70ec9 (STORY §10)
  - 93f85e0dd ("already-banked", STORY §2)
- **Check:** `git log --since=2026-09-28T00:00:00Z --name-only --format=%h -- mag/context_pack.py tools/stealth_driver.py mag/seed_percolator.py tools/workflow_gate.py` plus `git status --porcelain | wc -l`.
- **Settles:** Strand 1 stays live only if wave5 organ files still appear in porcelain.

**R8. "Tapestry resurrection" headline vs the lattice's "owed its own dance" (OVERCLAIM).**
- **Claim:** STORY §4's title promises a resurrection. Its body concedes "No receipt in the window records the tapestry dying".
- **Contrary evidence:** the lattice ran `git log --since="2026-09-28" -- mag/tapestry.py mag/tapestry_visual.py`, which "returns nothing". STORY also cites suite-burn.check.txt lines 134-136 only and omits the lattice's 2131-2132 (test_tapestry_visual).
- **Check:** rerun the lattice's git log, plus `sed -n '134,136p;2131,2132p' watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt`.

**R9. Seed pointer and headroom (PERISHABLE BY DESIGN).**
- **Claim:** FRESHNESS_DAYS=3 on a pointer at seed_rib_20260929, with headroom of 97,364/100,000.
- **Why it rots:** after 2026-10-02 the SLO should void SEED_RIB_CURRENT unless it is re-rendered, and any rebuild that crosses 100,000 is refused.
- **Check:** the seed verify entry point named in watch/inbox/wave5_repair/seed-kernel.md (exact verb UNVERIFIED from this evidence). Record exit code plus decoded byte count plus UTC time.

**R10. Burns ledger "693 rows" plus "churning 24x7" (STALE count, falsified order).**
- **Claim:** the ledger is a live 24x7 burn. 693 rows (23 + 517 + 108 + 45; the arithmetic checks).
- **Contrary evidence:** "the ledger holds no 09-29 rows", which contradicts the 24x7 order on its own day.
- **Check:** `.venv/Scripts/python.exe -c "import json,collections;c=collections.Counter(json.loads(l)['ts'][:10] for l in open('memory/burns/LEDGER.jsonl',encoding='utf-8') if l.strip());print(sorted(c.items()))"`. The `ts` key name is UNVERIFIED; adjust it to the row schema.

**R11. Mine slug format already diverges (LIVE RISK, same class as the underscore grep miss).**
- **Claim:** each day banks to `frontier_olm_<slug>/`.
- **Contrary evidence:** STORY §10 uses frontier_olm_20260928, while steals.md cites `watch/inbox/frontier_olm_2026-09-30/`. A glob like `frontier_olm_????????` misses the hyphenated day. This is the same silent-zero-match shape as RECEIPT.md "Search note".
- **Check:** `ls -d watch/inbox/frontier_olm_*` plus read the slug the cron caller passes for automation-cac38363.

**R12. Law 1 "seven jackets" lists five (UNDER-EVIDENCED).**
- **Check:** `sed -n '53,76p' memory/rib/RIB_DRIVING_LADDER_20260928.md`, then count the named jackets.

**R13. Basetemp failure count disagrees across chapters (DENOMINATOR UNNAMED).**
- **Claim:** laws.md §8 says "failed 5 gate/dead-hand tests". STORY §3 says "13 of the relative_to class". driver-meter rooted 4.
- **Check:** `rg -c "not in the subpath of" watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt`, plus a node-id listing per run.

**R14. "Every repair moved a law into exit code" (lattice Insight 1) vs law 9 "no exit code of its own".**
- **Problem:** the lattice also says "across all five" but lists six organ bullets.
- **Check:** classify each of the twelve laws by whether its asserted file:line contains an exit path (`rg -n "sys.exit|return 2|exit 2"` at the cited lines).

**R15. steals.md conflation and a cross-reference error.**
- **(a) Conflation.** The reading note fuses grok-4.7's "five buildable moves" with "the paid judgment's 5 moves". Per STORY §8 those are two different paid runs. Hermes's five moves (rotate key, freeze recovery pack, steal-map with halt rule, heartbeat, injection test) have zero rows in the menu.
- **(b) Cross-reference error.** M9 says "folds into M17's tokens/sec readout", but tokens/sec is M16.
- **Check:** `rg -n "rotate|recovery pack|halt rule|injection" watch/inbox/48h_synth/steals.md` returns zero hits.

**R16. Law 2's banking rule unmet by the window's own paid calls.**
- **Claim:** every paid dispatch banks tokens in/out.
- **Contrary evidence:** Hermes "usage 6,581 tokens" and elder "2,654 tokens" are totals, not in/out. Grok has no USD at all.
- **Check:** `rg -n "prompt_tokens|completion_tokens|input|output" <the three receipts>`.

**R17. Hermes moves 1 and 2 have no completion receipt (UNVERIFIED as done).**
- **Problem:** the 2,568-green commit is now 1,072 collected tests behind the census.
- **Check:** `rg -ln "recovery pack|restore-tested" watch/inbox` and `rg -ln "rotat" watch/inbox | rg -i xai`.

**R18. Hook registration lives outside git.**
- **Claim:** C:/Users/foste/.zcode/cli/config.json:50,84.
- **Why it rots:** the daily compile cannot see or seal it, so it can drift with no estate-side signal.
- **Check:** `sed -n '50p;84p' C:/Users/foste/.zcode/cli/config.json` plus file mtime, stamped UTC.

---

## PART 3. THE DEEPENING (three strongest laws)

**Selection rule:** strongest means the most direct proof in the evidence plus the most downstream claims depending on it.

- **Chosen:**
  - Law 8: two-direction proof, reproduced by two lanes.
  - Law 1 with law 10 as its counted instance: lineage from 09-26, and the synthesis itself breaks it.
  - Seat law gate rules 1-3 with 6 and 7: the only laws in the tool path. Law 7 has the best mint battery.
- **Not chosen:**
  - Law 2: no instrument exists to run.
  - Law 9: drafts only.

### A. Hermetic-basetemp (law 8)

- **Hypothesis:** every test added after run 3 (the ~1,072 delta to the 09-30 census) is hermetic to basetemp location.
- **Instrument:** `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --basetemp=<X>`.
  - Exit contract: pytest 0 = all passed, 1 = failures.
  - Capture full node ids with `-rfE`.
- **Moment:** a single clean HEAD, recorded as SHA and UTC, with the tree state recorded (`git status --porcelain | wc -l`). Arms run back to back on that one HEAD.
- **Context assumptions:** same venv; no sibling lane writing the tree (enforce by running on a `git worktree` of HEAD); same machine.
- **Arms:**
  - A1: default in-repo basetemp (conftest.py:14).
  - A2: external basetemp on the same drive.
  - A3: external basetemp on a different drive letter, or a path containing a space and a junction (stresses the Windows relative_to cross-drive ValueError).
  - A4: A2 plus the process cwd outside the repo (tests root-relative cwd assumptions).
- **Repeats:** one full run per arm. Every node red in some arm and green in A1 is re-run 3x in each arm to separate flake from class.
- **Cost:** $0 API. At 2,478 executed per 2,327s, ~3,550 tests extrapolates to ~55 min per arm, so ~4h wall plus re-runs.
- **Decision rule and falsifier:** any node green in A1 and red in A2/A3/A4 with a `relative_to` / "not in the subpath of" traceback, reproduced 3/3, falsifies "code correct out-of-repo". The node names the new file that owes the class fix. Zero such nodes across all arms keeps the law and raises it to "proved at 3,550".
- **Negative example (not a falsification):** a node red in all four arms is an ordinary failure, not this law's.

### B. One-bug law (law 1, with law 10 as the counted instance)

- **Hypothesis:** numeric verdicts stamped with instrument plus exit, UTC moment, and context reproduce in one investigation. Unstamped ones take two or more, or fail.
- **Instrument:** a reproduction protocol run by a seat that authored none of the 48h_synth files.
  - Unit: one numeric verdict.
  - Measure: the count of separate command sessions until the number is reproduced, or the disagreement is resolved to a named condition difference.
  - Cap: 3, then mark IRREPRODUCIBLE.
- **Moment and context:** the same frozen HEAD as A. The reproducer sees only the receipt text plus the repo.
- **Arms:**
  - S (stamped): about 10 verdicts that already name all three conditions, e.g. run 3 "14 failed, 2452 passed, 12 skipped ... in 2326.98s" with its external basetemp.
  - U (unstamped): about 10 that lack at least one, e.g. "2,568", "4 live seatlaw_* rows", "20:04", "693 rows".
  - Classification is done by a different seat before reproduction, and the reproducer is not told the arm.
- **Cost:** $0 API, about 3 seat-hours.
- **Decision rule:** S median 1 and U median 2 or more, or U irreproducible at 3 or more of 10, keeps the law and promotes it toward an exit-coded linter.
- **Falsifier:** U reproduces in one investigation at a rate at or above S. The law is then overhead at receipt grain and stays prose.
- **Power note:** n=20 cannot detect small effects. A null here is INCONCLUSIVE and justifies n=60, not abandonment.

### C. Seat law gate cluster (rules 1-3 plus laws 6, 7)

- **Hypothesis:** the gate blocks through the real tool path, not just when invoked directly, and payload checks no longer write ledger rows.
- **Instrument:** two layers, because "rule bytes correct" and "hook registered and firing" are different verdicts.
  - L-direct: feed JSON payloads to `tools/seat_law_gate.py` on stdin and record the exit code.
  - L-path: issue real Bash/Write/Edit tool calls from a seat and record whether the tool call was refused.
- **Moment:** a single UTC window. Record `wc -l memory/workflows/REGISTRY.jsonl` before and after.
- **Arms, lawful vs lawless pairs for each:**
  - r1: `.venv/Scripts/python.exe -c "print(1)"` (expect pass) vs `python -c "print(1)"` (expect exit 2).
  - r2: write a dash-free scratch file under watch/inbox (pass) vs the same file with one U+2014 (block); re-save of a historically dashed file (pass); Edit fragment with a dash (block).
  - r3: compliant scratch *.dwf.ts (pass) vs empty payload (block, failing gate names printed).
  - law 6: REGISTRY line delta across the whole battery must be 0.
  - Fail-open probe: malformed stdin `{bad` to L-direct, expected exit 0 by design (seat_law_gate.py:26-27). This is recorded as the known hole, not as a failure.
- **Cost:** $0, about 20 minutes. Delete the scratch files after the run. Note that a deletion under watch/inbox may be governed by the append-only law (UNVERIFIED), so prefer a scratch path the law exempts.
- **Falsifier:** any one of the following.
  - Any lawless case returns 0 on L-path. The registration is dead even if L-direct passes, which settles R18.
  - Any lawful case is blocked.
  - The REGISTRY delta is above 0. Law 6 is then falsified, which also settles R6.

---

## PART 4. THE SUBSTANCE

What an outside researcher should steal first, ranked by portability times evidence strength:

1. **Name the denominator, including where the scratch space lives.**
   - The pitch: the same pytest suite, same code, same session, gave "the same 13 nodes green in-repo and red out-of-repo" depending only on basetemp location.
   - Mechanism: an in-repo temp dir silently satisfies every `path.relative_to(repo_root)`, so a whole class of production bugs is invisible to the suite that is supposed to catch it. It also makes failures look intermittent ("the test passed, which is why it looked intermittent across runs").
   - The steal: any suite-health number is incomplete without where it ran from. Run your suite at least once with the temp root outside the repo, and on Windows on another drive.

2. **Laws that work live in the tool path, with three refinements.**
   - The pitch: agents demonstrably do not self-police (laws.md, "sw-10"). This estate moved conduct rules into pre-tool hooks with exit codes, and the details are what make it survive contact.
   - Refinement 1: fail open on internal error, so a broken gate never halts the fleet.
   - Refinement 2: judge only newly introduced violations, so lawful re-saves of legacy content are not blocked and seats are not trained to route around the gate.
   - Refinement 3: a check must never register itself as a fact. That is the --no-register fix: a verdict is not a ledger row.

3. **A budget smaller than its mandatory core is a silent eraser.**
   - The pitch: directives were built into every context pack and reached 0 of 6 renders because a 1,200-char budget sat below a 2,217-byte objective, while a code comment claimed the tier "survives the ladder".
   - The fix pattern: make the layout the protection order, shed one named block at a time with a receipt per shed, and size budgets from the core upward.
   - Who should steal it: anyone truncating prompts to fit a context window.

4. **Fail-closed loaders get amended by name, never loosened.**
   - The pitch: a strict loader served 0 of 58 rows. The repair kept "unknown schema-less rows still raise" and admitted only "carrier-named debt ... by name, in-file", reaching 58 of 58 with the strictness contract intact.
   - The steal: when strictness blocks legitimate data, whitelist the debt explicitly rather than relaxing the rule.

5. **The honest non-answer is an instrument.**
   - The pitch: a paid model answered "I cannot confirm ... I will not invent dates or quotes" and then separated unsure signals, structure-derived moves, and standing constraints.
   - The follow-up protocol graded every row, banked negative results as first-class rows, and machine-checked the finish.
   - The steal: the register shape plus a validator that is itself tested against a tampered copy (steals.md M20).

### The one landable deliverable: SUITE-STAMP (operationalizes steals 1 and 2 and laws 1, 8, 10)

**What it does.** Every pytest run prints one machine-parseable line naming its own denominator:
- collected, deselected, and per-outcome counts
- basetemp, plus whether it is in-repo
- invocation args
- interpreter path
- HEAD
- UTC moment

**Landing steps.**
1. Check for collisions with `rg -n "pytest_terminal_summary|pytest_collection_finish" conftest.py`. If either hook already exists, merge the bodies.
2. Append the block below to `conftest.py`.
3. Run `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`. A code file changed, so the ratchet is owed.

**Design choices.**
- No subprocess, so it adds nothing to the bare-spawn register.
- HEAD is read from .git directly.
- It reads basetemp without calling `getbasetemp()`. That call can create or rm_rf the given basetemp at session end, which is a side effect, the "check side-effects" jacket.
- It uses `os.path.commonpath` under try/except, because cross-drive paths raise `ValueError`, the very class law 8 names.

```python
# --- SUITE-STAMP: every suite count carries its conditions (laws 1, 8, 10; B2-216) ---
import datetime as _ss_dt
import json as _ss_json
import os as _ss_os
import sys as _ss_sys
from pathlib import Path as _SsPath

_SS = {"collected": None}


def pytest_collection_finish(session):
    _SS["collected"] = len(session.items)


def _ss_git_head(root):
    try:
        head = (root / ".git" / "HEAD").read_text(encoding="ascii").strip()
        if head.startswith("ref: "):
            ref = root / ".git" / head[5:]
            if ref.is_file():
                return ref.read_text(encoding="ascii").strip()[:12]
            return "PACKED-REF:" + head[5:]
        return head[:12]
    except OSError:
        return "UNMEASURED"


def _ss_in_repo(path, root):
    try:
        p = _ss_os.path.normcase(str(_SsPath(path).resolve()))
        r = _ss_os.path.normcase(str(root.resolve()))
        return _ss_os.path.commonpath([p, r]) == r
    except (ValueError, OSError):  # cross-drive on Windows: by definition not in repo
        return False


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    root = _SsPath(str(config.rootpath))
    factory = getattr(config, "_tmp_path_factory", None)
    basetemp = getattr(factory, "_basetemp", None) or config.option.basetemp
    stats = terminalreporter.stats
    row = {
        "ts_utc": _ss_dt.datetime.now(_ss_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "head": _ss_git_head(root),
        "exit": int(exitstatus),
        "collected": _SS["collected"],
        "deselected": len(stats.get("deselected", [])),
        "passed": len(stats.get("passed", [])),
        "failed": len(stats.get("failed", [])),
        "error": len(stats.get("error", [])),
        "skipped": len(stats.get("skipped", [])),
        "basetemp": str(basetemp) if basetemp else "UNMEASURED",
        "basetemp_in_repo": _ss_in_repo(basetemp, root) if basetemp else None,
        "args": list(config.invocation_params.args),
        "python": _ss_sys.executable,
    }
    terminalreporter.write_line("SUITE-STAMP " + _ss_json.dumps(row, sort_keys=True))
```

**Examples.**
- **Positive:** a lawful suite claim quotes the line verbatim, e.g. `SUITE-STAMP {"basetemp_in_repo": false, "collected": 3550, "exit": 1, "failed": 14, ...}`. A reader can reproduce it or name the condition that differs.
- **Negative:** "2,568 hermetic green". It has no stamp, no instrument, and no basetemp. Under this deliverable it is unfired (R5).

**Falsifiers of this deliverable.** Any one of these kills or amends it.
1. **Inertness fails.** Run any fixed test subset twice on one HEAD, once with the block and once with it removed. Any difference in collected or per-outcome counts means the hook is not inert. Revert.
2. **Completeness fails.** Two runs whose stamps are identical in head, basetemp_in_repo, args and python produce different failed node sets, and the difference is not flake (3/3 re-runs). The stamp is then missing a condition: tree dirtiness and environment are the named suspects, because `dirty` is deliberately UNMEASURED without a subprocess. Add that field.
3. **Liveness fails.** A full-suite log from the next census lacks a `SUITE-STAMP` line. The hook is not loaded, or it was shadowed by a merged conftest hook.
