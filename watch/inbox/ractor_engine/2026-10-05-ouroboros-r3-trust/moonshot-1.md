# OUROBOROS R3 - TRUST INSTRUMENTS - moonshot-1 (2026-10-05)

Lens verdict: this estate keeps hardening the FAIL face of its trust instruments
(R1 stop-cert teeth, R2 case fix, R1 fold de-blind) and never probes the PASS
face. I spent this sitting minting degenerate inputs and asking the instruments
to certify them. Five of five obliged. The certification layer does not yet
distinguish a law from its spelling. Every probe below was run this sitting by
this seat on this tree; fixtures were destroyed after (no REGISTRY or
FIRE_LEDGER rows minted: every gate run carried --no-register).

Claim checks re-run at the ask's scale, this moment:
- Scenario suite: `./.venv/Scripts/python.exe tools/workflow_gate.py check
  --scenarios configs/workflow_gate_scenarios` -> "9 cards validated
  read-only", "pass_control: all 8 gates clean", exit 0.
- Seal patrol: default window -> 1 drift (MASTER_EXECUTE_REGISTER.md); window
  1000 -> 11 drifts, exit 1. The ask's "10" measured 11 at this moment, and
  the ledger is MOVING under the patrol: my two runs 2 minutes apart read
  10790 then 10796 sha rows (append-only ledger, live lanes writing).

## RANKED BLINDNESS TABLE (ranked by which blindness corrupts an operator decision first)

| # | Instrument | The fooling shape (probed) | Cheapest probe that proves it | The fix |
|---|---|---|---|---|
| 1 | workflow_gate stop-cert (tools/workflow_gate.py:244-285) | ARMED AGAINST AN EMPTY SURFACE: the live REGISTRY.jsonl carries 90 rows and ZERO "status" fields (censused by json parse this sitting), so load_stopcert_index() always returns empty sets and stop_cert_reason() is always "". The operator's retire verdicts exist only in prose: .zcode/workflow-drafts/RETIRED.md:11-15 pens 5 retired drafts (Q7 sweep, 2026-09-27) that were never written into the registry the tooth reads. The R1 end-to-end proof ran on a fixture registry, not this one. | Ran: `workflow_gate.py check --script .zcode/workflow-drafts/ractor_panel_20260926.dwf.ts --no-register` (RETIRED.md:15, verdict "RETIRED, unused") -> fresh "workflow_gate PASS", all 8 gates ok, exit 0, no STOPCERT line. The ungated Tree-Doctrine original (the 429-storm class) would pass the same way. | Mint the 5 RETIRED.md verdicts as registry status rows (the operator pen, one sitting, ~10 min); then add the pen to the retire ritual: no RETIRED.md row without its registry status row. |
| 2 | workflow_gate G1-G8 (tools/workflow_gate.py:84-127) | DEAD-TEXT CERTIFICATION: every check is a regex over raw text, comments included. A file that is 100% comments containing the 8 magic strings passes all 8 gates. CONVERGENT x2: accuracy.md row 3 and the communication lens's probes/ fixtures found the same class (g8_vacuous_envelope.dwf.ts); my probe extends it to all-of-G1-G8 on one file. Without --no-register this mints a PASS REGISTRY row and a FIRE_LEDGER row (workflow_gate.py:476-505), so the ledger of record rots with certified theater. | Ran: `workflow_gate.py check --script tmp_r3_probe/vacuous_all_comments.dwf.ts --no-register` (fixture: 10 comment lines, zero executable code, each carrying one gate's magic string) -> PASS, all 8 ok, exit 0. | Strip comments (and ideally string literals) before the G1-G7 regexes; bank both fixtures as scenario cards so every future gate change re-proves the refusal. |
| 3 | G8 width law (tools/workflow_gate.py:176-193) | TWO EVADES, both probed: (a) the envelope stamp is EXISTENCE-ONLY: os.path.isfile() at :191 accepts any existing watch/inbox file; `envelope-receipt: watch/inbox/INDEX.json` (a directory index, not a measurement) unlocked max_concurrency 50. CONVERGENT with accuracy.md row 3 and communication's g8_stamp fixtures. (b) SYMBOL WIDTH: the regex only reads digits; `const width = Number(args.width \|\| 50); max_concurrency: width` declares an unbounded runtime width, matches no digit, passes G8, and FIRE_LEDGER records max_concurrency: null (max_declared_width :288-291), so the width-join is dark for exactly the scripts that width-smuggled. CONVERGENT with accuracy.md's smaller-teeth note (its FIRE_LEDGER row shows live `width: "50"` riding a max_concurrency 3 script). | Ran both fixtures -> PASS exit 0 both. Fixture B output: "ok G8-width-shape" with max_concurrency 50 + INDEX.json stamp. Fixture C: symbol-valued width, same ok. | (a) The stamp must name a file whose BYTES carry a measured-envelope marker (a width table + a date token); (b) any `max_concurrency` token whose value is not a digit literal is UNKNOWN-width and hard-fails (fail closed, never skip). |
| 4 | seal patrol (tools/prepush_seal_patrol.py:108-137) | THE CHANNEL IS PERMANENTLY RED + A PROBE-PROVEN PREFIX-CASE MISROUTE (mechanism CORRECTED after the hostile pass, which killed the original Path-key attribution and confirmed the adjudication half). (a) AMENDED MECHANISM: Windows Path equality DOES collapse case (re-verified this sitting: Path("watch/inbox/Case.md") == Path("watch/inbox/case.md") -> True, hashes equal; a patrol() probe over two same-prefix case spellings returns distinct=1 drifted=0, the hostile pass's V1 reproduced). The false wolf enters one door lower: resolve_sealed_path tests the literal `p.startswith("watch/inbox/")` case-SENSITIVELY (:73), so a prefix-case-variant row ("Watch/InBOX/Case.md") diverts to the bare-relative branch and resolves to root/watch/inbox/Watch/InBOX/Case.md, a PHANTOM target (is_file() False, counted missing) - the file's chronologically newest seal is filed under the phantom key while the real file keeps the stale seal and flags DRIFT. Probe re-run this sitting: rows [watch/inbox/case.md stale, Watch/InBOX/Case.md current] -> distinct=2 drifted=1 missing=1, "WOLF: case.md sealed 7ae23546c628 vs actual f747db4a1b91 (newest matching seal exists: f747db4a1b91)"; row2 resolves to ...\watch\inbox\Watch\InBOX\Case.md, is_file() False. Probe-proven, LATENT live: the ledger spelling census (moonshot-1.md dump below) found only bare-relative + absolute pairs, no prefix-case variants today. (b) CONFIRMED BY HOSTILE PASS (split verdict, their refresh on 10876 sha rows): 12 drifts at their moment (mine read 11 at 10790/10796; moving ledger, both moments named); 5 writer-race (incl. this round's live break-accuracy.md +8s, seal at ledger line 11146), 5 live-append/standing, 1 confirmed post-seal-edit: r2-gaps/moonshot-1.md, last seal 12:03:12Z bbcd0453ccf9 (ledger lines 10763/10764; the 13:16 a9e5 seal belongs to break-moonshot-1.md), actual a345000db1a5, edited +4756s, cold 7.1h - byte-for-byte this lens's catch, independently re-derived (CONVERGENT x2). 1 borderline (lens/laws.md +116s then cold 6.2h). The permanently-red-channel claim stands (hostile pass wording). | Ran: patrol default + `--rows 1000`; ledger spelling census; pure-core patrol() probes V1 (same-prefix collapse, no wolf) and V2 (prefix-case variant, wolf) with the resolve_sealed_path routing printout. | The one-line-class fix for (a): compare the prefix case-insensitively (p.lower().startswith("watch/inbox/")) or normcase the file field before the branch; then V2 must return distinct=1 drifted=0. For (b): skip-and-count files whose mtime is newer than patrol start (live-write race) as "live"; split the channel - drift on a CLOSED round dir (SYNTHESIS.md present) is the hard class, standing drift on never-re-sealed hot surfaces is its own bucket with a re-seal-or-resign decision per surface. A permanently red WARN is an unread alarm: the B2-338 channel-discipline lesson, already cited by the estate's own prepush_workflow_metadata.py:87-89. |
| 5 | fold de-blind key-match + shape exclusion (tools/mickey17_v2_fold.py:339-358) | FAIL-OPEN, PROVEN LIVE (accuracy.md row 5 predicted the fragility by code-read and census; this seat ran the fold and proved the inclusion direction): the R1 de-blind matches persisted deep_tier2 verdicts to rows by a DERIVED 6-word-prefix key (deep_keys :339-342). A persisted unconfirmed whose row_key words are reordered ("the laws seven hold" vs the claim's "the seven laws hold") matches nothing and rides INCLUDED; the same output file's verifier table shows "deep_tier2 1 (verdict split: unconfirmed 1)" while PRISMA excluded shows 0 verifier-unconfirmed. Also: any lane with exactly 1 row is excluded by SHAPE alone as "1 phantom-source (dead-lane negative row)" (:346,350) regardless of its content; my probe's single high-TRUE row was auto-excluded. | Ran: built memory/runs/mickey17_v2/runs/probe-r3 (2 lanes, one checks.json with reordered row_key), ran `mickey17_v2_fold.py --run probe-r3 --fired 2` -> "lanes=2 rows=3 included=2 excluded=1" where the excluded 1 is the shape exclusion and the unconfirmed row is inside the included 2. Probe dir deleted after. | Persist a stable key at verify time (lane id + row index, written by the runner's mechanical persist step, not derived by string surgery); until then FAIL CLOSED: a deep_tier2 unconfirmed that matches NO row files as "unmatched-unconfirmed", never silently includes. The single-row exclusion must require the row's negative-marker fields, not row-count==1. |
| 6 | golden vector (tools/prepush_golden_vector.py:50-73) | DEAD-TEXT PASS: check_text is `needle not in text` over the whole file, comments included. A file that is 100% comments SAYING THE SCENES WERE DELETED scores 11/11. The known-answer tripwire certifies spelling, not liveness. | Ran: `prepush_golden_vector.py --file tmp_r3_probe/golden_comment_only.py` (comment-only fixture: "The Lexical Stair was a scene we deleted" etc.) -> "GOLDEN-VECTOR: ok - 11/11 golden tokens". | Require each token on a non-comment, non-docstring line (ast.parse the target; a .py is parseable by construction), or count occurrences and require the code-line count to match the pinned count. |

## THE 10 REAL DRIFTS, ADJUDICATED (the ask's explicit charge)

The ask's "10 real drifts" measured 11 at my window-1000 moment (accuracy.md's
same window read 12 at its moment; the ledger moves, both moments named).
Adjudicated by seal-history census (ts, op, sha, register+autoseal pairs) +
git last-commit + the path-spelling dump:
- LIVE-APPEND standing drift (5): PACK_OFFLOAD.jsonl, STEALTH_MINED_FINDINGS.jsonl
  (both bare-relative ledger spellings, hot lane appends, never re-sealed),
  DOORS.jsonl (sealed 10-04 18:46, appended since), MASTER_EXECUTE_REGISTER.md
  (sealed 16:13:23Z, the EXECUTE run is live-appending it right now),
  frontier_olm_2026-10-05/lens/laws.md (sealed 14:13:49, edited +116s).
- WRITER-RACE (4): the two frontier_olm mds (seal 15:49:53 / 01:57:49, edit
  +28s / +31s after), RECEIPT.md (seal 06:30:54, edit +22s), ribvault
  r06_free_probe.py (seal 05:37:49, edit +3m). Seals taken before final flush.
- POST-SEAL-EDIT, the instrument's real target (1 confirmed): ractor_engine/
  2026-10-05-ouroboros-r2-gaps/moonshot-1.md, last seal 12:03:12Z, mutated
  after with no re-seal. Zero tampering evidence across all 11 (all owned by
  live lanes or late flushes), but the one real catch rides a channel that is
  permanently red, which is how a real catch gets dismissed.
- Ledger spelling census: every seal lands as a register + autoseal PAIR
  (bare-relative + absolute) that resolve to one dict key (benign); case
  VARIANTS do not collapse (probe above). STEALTH_SWEEP_LATEST.md's last seal
  is 2026-09-27 on a file whose declared purpose is daily rewrite: a standing
  8-day-old drift by design.

## THE SWING (the 10x version, grounded in one organ)

The estate's trust instruments have a functional suite (the scenario cards,
11/11 and 9/9 green) and NO vacuity suite: nothing anywhere asserts that an
instrument REFUSES degenerate input. Every finding above is the same disease:
a PASS face that was never probed. Build the VACUITY BATTERY as a third mode
of tools/workflow_gate.py (the organ that already owns the card machinery,
run_scenarios :362-422 is read-only and reusable): one card per instrument,
each card a degenerate input ASSERTED TO FAIL (comment-only script, envelope
stamp naming an index, symbol width, retired-name script, reordered row_key
fold fixture, comment-only golden file, single-sample consensus). Suite green
= every instrument still refuses its theater; a card that goes green-on-
degenerate files the instrument VACUOUS in the round fold. Cost: the fixtures
already exist (mine + the communication lens's probes/ dir), the machinery
exists, ~1 sitting. This is the G8 lesson turned into a standing organ: a
check that can pass without its subject must be forced to prove it.

## R3 DRIVER AMENDMENT (round-4-relevant)

The driver's own header is the exhibit: Ouroboros-round-3-trust.dwf.ts:12
still claims "workflow_gate PASS digest 5253afd2d68d G1-G7" while the gate is
G1-G8 and the file's bytes have been amended since (the digest names a corpse).
And the ask itself named "mag/consensus_merge.py", which exists nowhere (the
symbol lives at mag/memweave.py:208; dogfood.md row 5 hit the same miss).
AMENDMENT: every round driver must carry, per named instrument, (0) the
instrument's real path verified at fire time, and (1) one banked vacuity
probe asserted to produce the instrument's refusing verdict BEFORE the round's
lenses ride; an instrument whose vacuity probe passes-degenerate is filed
VACUOUS in the round fold together with its live-caller census, never assumed
as a standing defense. This subsumes accuracy.md's negative-control amendment
and dogfood.md's wiring clause into one pre-fire gate clause: instrument green
on its functional suite and blind on its vacuity suite is not a defense, it is
a costume.

## Honest blind spots

- The gate's comment-vacuity probe covers comment spans; string-literal
  vacuity (magic strings inside template literals) was code-read only, not
  probed.
- I did not run the fold on the REAL run archives (only the probe slug); the
  live mega-burn archives' actual unconfirmed-miss rate under the derived-key
  match is OWED (accuracy.md's census of 52 verdicts with 0 missing row_keys
  is the sibling evidence it holds TODAY).
- The stop-cert rename evasion (retired script re-saved under a new basename
  evades name+script keys, digest matches only identical bytes) is code-read
  (load_stopcert_index keys), not probe-run; moot while the surface is empty.
- mag/consensus_gate.py's ladder flat-extrapolation (params >= 120 inherits
  the 0.09 anti-signal AUROC forever, so no frontier-scale model can ever be
  CONFIRMED; 72-120B interpolates below threshold) is code-read at
  mag/consensus_gate.py:56-57; its blast radius is zero today because the
  module is unwired (dogfood.md row 5's census, not re-run by this seat).
- The tier-1/tier-2 verify ceremony inside mickey17-burn.dwf.ts persists
  verdicts by asking an agent to rewrite JSON whole (":445-:490 region by
  grep"); a hand-rewritten persistence layer under a trust instrument was
  read but not adversarially probed this sitting.
- cache_kpi.py's nominal-vs-receipted split was read and found sound in
  isolation (clamp at :182-185 honest); its producer mag/context_checkpoint.py
  was NOT audited (convergent with accuracy.md's blind spot).
