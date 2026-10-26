# credrot final: 18-credential rotation decision packet (masked surface only), revision of credrot-two, 2026-09-27

Card credrot, the revision. This is the panel survivor
`watch/inbox/ractor_panel_20260926/cands/credrot-two.md` revised per the judge
ruling (`credrot.verdict.json`) and its six-bullet critique, with the killed
sibling `cands/credrot-one.md` absorbed where the critique names it. Every
check this packet cites was run by this revision lane with raw output filed
under `watch/inbox/ractor_panel_20260926/checks/`: the census
(`credrot.rev.census.txt`, from `credrot_rev_census.py`), the widened consumer
grep (`credrot.rev.grep.txt` plus `credrot.rev.grep2.attempt1.txt`,
`credrot.rev.grep3.txt`, `credrot.rev.grep4-configroots.txt`), the citation
verifications (`credrot.rev.verify.txt`, `credrot.rev.verify2.txt`), and the
final self-check (`credrot.final.selfcheck.txt`). Judge checks are cited as
judge-run (`checks/credrot.judge.txt`). Hard law held by this lane: no
corpus/ dump-carrier file was opened; the live .env was read into memory only
and never printed beyond 6-char canonical mask heads.

No credential value appears in this artifact. Dump heads below are exactly the
heads already published in
`watch/inbox/burn_wave_20260926/B2_73_secret_scan_20260926.md` Evidence lines
46-54. The only fresh heads quoted are the two current Groq rest-place heads,
in the policy rule 1 canonical form (6 chars plus length,
`watch/inbox/SECRET_SCAN_RULESET_ROTATION_20260926.md:87-90`): they are
at-rest heads, not dump heads, and are labeled as such at every use.

## Final

### The load-bearing delta over the B2-73 receipt, re-proved on live bytes

The receipt said the exposed values are "plausibly the still-live rest-place
entries" (line 15). The name-plus-masked-head .env census resolves it per
value, and this revision re-ran that census rather than carrying it:
**13 of 18 exposed heads byte-match a current .env name, each uniquely
(`credrot.rev.census.txt` R2: 13/13 MATCH unique); 5 match no current rest
place (R3: gsk_17bq, gsk_8LAQ, 088650c6, sk-c2bd8, xai-gO all orphan)**. The
13 at-rest values are rotations owed; the 5 orphans are console audits only
(no .env change, delete at the console if the key still exists). The judge
independently byte-confirmed the same split (judge CHECK 3,
`checks/credrot.judge.txt` lines 56-96). Zero rotation has occurred as of
this revision: `watch/inbox/KEY_ROTATION_JOURNAL.jsonl` does not exist
(census R1), matching B2-349 line 5 ("OWED, operator-gated ... Zero rotation
has occurred").

The census instrument and its law: it prints NAME plus a 6-char canonical
mask head plus length, never a value. Before any sitting, re-run it exactly
as filed (`.venv/Scripts/python.exe
watch/inbox/ractor_panel_20260926/checks/credrot_rev_census.py`) and require
13/13 MATCH unique and the five orphans unchanged; any drift re-tiers the
rows before a hand touches a console.

### Collision guard for the head-match method (current bytes as evidence)

The 8-14 char head-match method is only sound per family while heads stay
pairwise distinct at the length in use. Current-byte evidence
(`credrot.rev.census.txt` R4, this revision):

- ZAI family (5 rest places): pairwise distinct at 8 chars. Minimum distinct
  head length 8.
- GROQ family (2 rest places): pairwise distinct at 8 chars. Minimum 8.
- ANTHROPIC pair: COLLIDES at 8 chars (both values begin sk-ant-a); pairwise
  distinct from 14 chars. Rows 1 and 16 therefore key off the two
  receipt-published 17-char heads (sk-ant-api03-IWEF, sk-ant-api03-_NxL),
  never off 8-char heads.
- OPENROUTER pair: collides at 8, distinct from 10. Rows 14-15 key off the
  published 13-char heads (sk-or-v1-4167, sk-or-v1-6be0).

Standing guard: the pre-sitting census re-run (above) is the gate. If any
family shows a same-family collision at the head length a row relies on,
widen that family to 14 chars (the census ceiling) or resolve console-side
before acting. A collision does not kill the packet; it blocks that family's
rows until resolved.

### Rollback chassis, REVISED: console is the rollback rest place, no local copy

The survivor's R0 copied `.env` to `.env.prerotation-20260926` before edits.
That step is DELETED from this packet. It sat against rotation policy rule 1,
one rest place per key, never copied
(`watch/inbox/SECRET_SCAN_RULESET_ROTATION_20260926.md:87-90`): a copy is a
second at-rest instance of all 52 env values, including the never-exposed
OPENCODE and GEMINI families. This revision adopts the sibling's
console-as-rollback-rest-place law instead (credrot-one lines 93-99): the old
value remains recoverable at the provider console until revocation, and
revocation is deferred until after the verify gate, so the revert path never
needs a local byte copy. Negative result, first-class: the snapshot file does
NOT exist on disk (census R1: `.env.prerotation-20260926 exists: False`), so
the survivor proposed but never executed it, and nothing needs shredding. Had
it existed, this packet's first move would be deleting it. `.env` is untracked
(`git ls-files --error-unmatch .env` fails, `credrot.rev.verify.txt` item 5;
`.gitignore:19-21` lists .env, .env.local, .env.*), so no git history copy
exists either.

- **R0 (journal only):** append one line per action to
  `watch/inbox/KEY_ROTATION_JOURNAL.jsonl` (policy section 2 rule 2; absent
  today, census R1; first rotation creates it). Row shape: date, env name,
  old masked head, new masked head, action, verifier result. Declines get
  journal lines too, or the acceptance gate below cannot close.
- **R1 (mint-before-revoke):** where the console allows concurrent keys, mint
  and install the new value while the old still works. Console multi-key
  policy is an operator-console fact, not verifiable locally (no network this
  lane); if a console forces single-key, R3 is the rollback.
- **R2 (verify gate before revoke):** one cheap call through the real
  consumer path, instrument named per row. Only after PASS does the old key
  get revoked. This ordering is what keeps reinstall-old-from-console alive.
- **R3 (post-revoke fallback):** after revocation the old value is gone;
  recovery is cheap because lanes are value-agnostic by the KEY LAW
  (`mag/key_law.py:50` resolves names from `os.environ` at call time,
  re-verified `credrot.rev.verify2.txt`): any working value under the
  canonical name restores the lane. Last resort: mark the lane dormant and
  route around it (established pattern, `configs/providers.yaml:296`).
- **Retire shape:** for a name with no consumer anywhere on the searched
  surface, removal cannot break a lane; rollback is re-add with a fresh mint.

Timed consumers (unchanged from survivor, citation strength stated):
MagImproveDaily 08:00 weekly deep provider probe (`mag/doctor.py:591`
check_provider_endpoints, cadence `mag/improve.py:399-457`, both verified in
`credrot.rev.verify2.txt`); MagCensusPatrolDaily 08:30 and MagFtsIndexDaily
09:00 are local-only; MagMimoWatchHourly rides OPENCODE keys (not in the 18).
Live schtasks query returned no rows in this shell (not re-verified live;
timings cited from AGENTS.md, the register scripts, and the B2-351 receipt).
Quiet window for waves 3-4: after 09:30 local, and away from the Monday
06:40 secret-scan slot per the B2-351 schedule receipt.

### The two fresh Groq heads, restated canonically

The current Groq rest places hold `gsk_QI...(len=56)` (GROQ_API_KEY) and
`gsk_w2...(len=56)` (GROQ_API_KEY_2): at-rest heads from this revision's
census (R4/R5), NOT dump heads. They appear nowhere in the filed masked
surface (judge CHECK 3: src=NOWHERE-FILED for the survivor's 8-char forms),
which is exactly why the two dumped Groq values are orphans. Publication in
the policy's canonical 6-char-plus-length form is sanctioned by the mask law
itself (policy rule 1) and is required: wave 2 rows 4-5 are only checkable
against the current rest-place heads. Nothing longer than 6 chars of either
value is quoted anywhere in this packet.

### Wave 1, REVISED: no longer "zero-blast"; rows 1-2 demoted on widened-grep evidence

The survivor's rows 1-2 rested on a py-only grep (`grep -rw --include=*.py`
over `mag/ tools/ scripts/ main.py`). This revision ran the widened grep the
critique demanded, all file types, whole repo with corpus/ pruned, plus the
out-of-repo client-config roots; raw outputs `credrot.rev.grep.txt`
(REPO: 533 name-mention lines, 77 consumer-class by extension), `.grep3.txt`,
`.grep4-configroots.txt`. Findings that change the rows:

- **ANTHROPIC_API_KEY_2 has a live consumer outside the py surface:**
  `deploy/openclaw/openclaw.container.json:770-774` binds the openclaw
  anthropic lane's apiKey to env id ANTHROPIC_API_KEY_2 (source: env,
  baseUrl api.anthropic.com). "Zero blast" was wrong. Row 1 is now a
  rotation-or-retire-with-repoint executed as one sitting: edit the container
  config (repoint to ANTHROPIC_API_KEY or to the new mint), update .env,
  revoke at the console, journal.
- **ZAI_API_KEY_3 has four named references outside the py surface, none a
  live traffic consumer:** `configs/spend_overlay.yaml:42` lists it as a
  prepaid-credits watch entry (its own header says the dashboard refresher
  joins it; no reader found by grep over mag/ tools/ scripts/ main.py this
  lane); `memory/runs/_probe_zai_walls.py:47,50` enumerates it (probe code
  that already tolerates absent names: it lists ZAI_API_KEY_4 too, which is
  absent from .env today); `watch/invariant_probe_001.mjs:15` loads it as its
  key (a rerun after deletion would fail); and
  `memory/runs/fleet_round/burn2b_lanes.json` carries 50 lane rows with
  key_env ZAI_API_KEY_3, a historical manifest (mtime 2026-09-13;
  `mag/forge_daemon.py:156` defaults to forge_daemon_lanes.json, so burn2b
  was a one-off --lanes argument) that documents real dispatch traffic once
  rode this key. Row 2 stays a retirement candidate but is PROVISIONAL and
  conditional: the sitting removes the spend_overlay entry, notes both
  probes, journals the manifest as history, and only then deletes the name
  and the console key.

Per the survivor's own falsifier, a missed hit demotes rows; it does not kill
the packet. Both demotions are executed above.

| # | Credential (masked head, receipt-cited) | Rest place | Blast radius (widened surface) | Action | Rollback |
|---|---|---|---|---|---|
| 1 | Anthropic `sk-ant-api03-IWEF...` | `.env ANTHROPIC_API_KEY_2` (census R2 MATCH unique) | openclaw anthropic lane (`openclaw.container.json:770-774`); 0 py consumers; ABSENT from keys.json (`credrot.rev.verify.txt` item 2) | One sitting: repoint the openclaw lane (to ANTHROPIC_API_KEY or a fresh mint), update .env and the container json together, revoke the exposed key at the console, journal | Chassis R0-R3; before revoke, revert = restore old .env line + container json; after revoke, re-mint; retire shape only if the lane is repointed |
| 2 | ZAI `bafc5c96...` (1x) | `.env ZAI_API_KEY_3` (census R2) | PROVISIONAL: no live traffic consumer found on the widened surface; references to clear: spend_overlay.yaml:42, invariant_probe_001.mjs:15, _probe_zai_walls.py:47,50, burn2b_lanes.json (history); declared alias-pool `configs/keys.json:36-41` | Conditional retirement: sitting-time re-run of the widened grep must stay clean for live consumers; clear the four references (remove overlay entry; probes go keyless by design), delete the .env line, flip the keys.json block, console-delete if present, journal | Retire shape: nothing consumes it after the reference clears; re-add with a fresh mint if the alias pool is ever wanted |
| 3 | Vast.ai `6881759e...` | `.env VASTAI_API_KEY` (census R2) | 3 py consumers; keys.json vastai_1 active (`configs/keys.json:177-182`); providers.yaml vast lane reads VAST_OPENAI_API_KEY, absent from .env, so the lane is dark (`configs/providers.yaml:430`, verify item 4) | Mint new vast.ai key, update the name, fix the lane env-name mismatch in the same edit, verify one vast_cost/doctor call, revoke old, journal | Chassis R0-R3 |

### Wave 2: console audits for the 5 orphans (no .env change)

Gate: the pre-sitting census re-run must still show all five as orphans.

| # | Credential (masked head) | Why orphan (byte evidence) | Exposure | Action | Rollback |
|---|---|---|---|---|---|
| 4 | Groq `gsk_17bq...` | current GROQ_API_KEY holds `gsk_QI...(len=56)` (at-rest head, not a dump head) | 14 rule hits / 7 files (findings JSON) | List keys in the Groq console; delete 17bq if present; journal outcome; absence CLOSES the row (partial hit on B2-73 falsifier inversion 3) | Orphan shape: nothing local references it; re-mint if ever needed |
| 5 | Groq `gsk_8LAQ...` | current GROQ_API_KEY_2 holds `gsk_w2...(len=56)` (at-rest head, not a dump head) | 14 rule hits / 7 files | Same as row 4 | Same as row 4 |
| 6 | ZAI `088650c6...` | no current name carries it (five ZAI names hold 3254aca9/e3c50501/bafc5c96/e18faf05/4f8ac54f, census R2/R3) | 36 occurrences, most-repeated ZAI value in the dump | Console audit at z.ai; delete if present; journal | Orphan shape |
| 7 | DeepSeek `sk-c2bd8...` | only DEEPSEEK_API_KEY=sk-effc9 is at rest; no Swarm name exists | census 4 occurrences | Console audit; delete if present; journal | Orphan shape |
| 8 | xAI `xai-gO...` | only XAI_API_KEY=xai-68sO is at rest | 2 rule hits / 2 files (grok chat_history + prompt_history bare paste) | Console audit; delete if present; journal | Orphan shape |

### Wave 3: live-lane rotations, one per sitting, verify-gated (the remaining 10 at-rest values)

Order rationale unchanged: widest exposure and paid lanes early, widest code
surface in a quiet window, the failover pair split across sittings,
session-bearing coding keys last.

| # | Credential (masked head) | Rest place | Exposure (instrument named) | Blast radius | Verify instrument (R2) | Rollback |
|---|---|---|---|---|---|---|
| 9 | OpenAI `sk-proj-UjAW...` | `.env OPENAI_API_KEY` | 43 occurrences (census), widest of all 18; 14 rule rows / 7 files (json) | 6 py consumers; openai lane paid, quota 100 calls/mo (`configs/providers.yaml:264`) | `mag doctor` one-token ping on the openai lane | Chassis R0-R3 |
| 10 | ZAI `e18faf05...` | `.env ZAI_API_KEY_Pro` | 34 occurrences (census) | 4 py consumers; z_ai2 fleet cache-mining lane | one glm flash call through the z_ai2 lane | Chassis R0-R3 |
| 11 | ZAI `4f8ac54f...` | `.env ZAI_API_KEY_Lite` | 34 occurrences (census) | 13 py consumers; z_ai3 lane, lite_guard ceiling (`configs/keys.json:25-30`); re-check lite_guard after the swap | one glm flash call through the z_ai3 lane | Chassis R0-R3 |
| 12 | xAI `xai-68sO...` | `.env XAI_API_KEY` (lane also accepts XAI_API_KEY_2, GROK_API_KEY(_2), `configs/providers.yaml:503`) | 21 occurrences (census); 16 rule hits / 9 files (json) | 16 py consumers BUT grok_cash is PAYG_blocked_by_grok_route_law, armed-only-by-operator (`configs/keys.json:51-56`); blast minimal | operator-armed grok call when next armed | Chassis R0-R3 |
| 13 | DeepSeek `sk-effc9...` | `.env DEEPSEEK_API_KEY` | 23 occurrences (census); 16 rule hits / 9 files (json) | 30 py consumers, widest code surface of the 18; workhorse paid lane (`configs/keys.json:79-83`) | `mag doctor` deepseek ping; schedule away from burn waves | Chassis R0-R3; route-around: openrouter deepseek models on the OR chain while in flight |
| 14 | OpenRouter `sk-or-v1-4167...` | `.env OPENROUTER_API_KEY` | both OR keys total 28 rule rows / 7 files (json; the 6-char stored mask merges the pair) | 24 py consumers; the chain's funded account per the failover-chain comment (`configs/providers.yaml:174-178`) | `tools/openrouter_free_gate.py` (B2-295 instrument, PASS = HTTP 200 non-empty) | Built-in redundancy: the chain fails over to key _2 mid-flight; NEVER rotate both OR keys in one sitting |
| 15 | OpenRouter `sk-or-v1-6be0...` | `.env OPENROUTER_API_KEY_2` | as row 14 | 17 py consumers; free-tier account | same gate, on key _2 | Mirror of row 14 (key 1 carries the chain) |
| 16 | Anthropic `sk-ant-api03-_NxL...` | `.env ANTHROPIC_API_KEY` (census R2 MATCH unique) | codex dump copies (receipt lines 48-50) | 4 py consumers; anthropic_1 active (`configs/keys.json:147-152`) | `mag doctor` anthropic lane ping | Chassis R0-R3; route-around documented in-lane (`configs/providers.yaml:296`) |

### Wave 4: session-bearing coding keys, LAST, at a window close

| # | Credential (masked head) | Rest place | Exposure | Blast radius | Verify instrument (R2) | Rollback |
|---|---|---|---|---|---|---|
| 17 | ZAI `3254aca9...` | `.env ZAI_API_KEY` | 19 occurrences (census) | 15 py consumers; z_ai main coding-plan key, opencode_only (`configs/providers.yaml:541` area, verify2); rotating while z.ai sessions are live kills tethered seats (AGENTS.md fan-out law; this panel rides that account family) | opencode client path (B2-235 proven transport) | Chassis R0-R3 at window close; mid-flight failure = finish the window on the old key, retry next close |
| 18 | ZAI `e3c50501...` | `.env ZAI_API_KEY_2` | 16 occurrences (census) | 4 py consumers; coding-plan key 2, opencode harness only | same opencode transport on key _2 | Same as row 17 |

This order inverts B2-349's "ZAI first, largest blast first" (B2-349 Work-done
point 2) for the reason the sibling argued: all 18 values are equally dead the
moment their console revocation lands, so ZAI-first maximizes simultaneous
breakage for zero extra risk reduction.

### Two-stage acceptance for B2-349 (absorbed from the sibling, verified)

B2-349's falsifier arm (b), "a post-rotation rerun of B2_73_secret_scan.py
finds none of the 18 masked heads", cannot pass from rotation alone: console
revocation does not edit corpus bytes, and the 19 carriers stay on disk
(no-erase). Byte-clean requires the still-open redaction lane B2-350
(`watch/inbox/burn_wave_20260926/QUEUE.md` line 411, verified open this
revision, `credrot.rev.verify.txt` item 1). Acceptance is therefore two-stage:

- **Stage 1, rotation done:** 18 journal lines (or masked decline lines) in
  KEY_ROTATION_JOURNAL.jsonl plus console states. This is all rotation can
  deliver.
- **Stage 2, byte-clean:** after the B2-350 redaction pass, the Monday
  MagSecretScanWeekly beat (`watch/inbox/SECRET_SCAN_BEAT.jsonl`, B2-351
  receipt; beat file exists, 641924 bytes, verify item 9) shows the
  corpus-side provider-rule counts collapsing to zero. Current baselines,
  re-counted this revision from the stored results JSON (verify item 8):
  OPENROUTER-KEY 28, GROQ-KEY 28, XAI-KEY 18, DEEPSEEK-KEY 16,
  OPENAI-CLASSIC 14 (the OpenAI project key is stored under the
  OPENAI-CLASSIC kind label, masked sk-pro...(len=164)), across 12 carrier
  files. ANTHROPIC-KEY rows are 0 in the stored JSON (both Anthropic values
  ride the ENV-ASSIGN band), so the Anthropic collapse is read from a
  B2_73_dump_census.py rerun, not from the rule counts.

### keys.json healing moves (absorbed, verified)

- ANTHROPIC_API_KEY_2 is absent from `configs/keys.json` (grep count 0,
  verify item 2; judge CHECK 7 concurs) and now has a known consumer. KEY LAW
  (`configs/keys.json:2`): one key, one canonical name, declared once. Either
  declare it or retire it; this packet recommends retire-with-repoint (row 1
  action), which removes an undeclared live name instead of papering it.
- ZAI_API_KEY_3 is declared alias-pool at `configs/keys.json:36-41`; row 2's
  retirement flips or removes that block in the same sitting.
- Record and heal the vast lane name mismatch: `configs/providers.yaml:430`
  reads api_key_env VAST_OPENAI_API_KEY while the rest place is VASTAI_API_KEY
  (verify item 4); the lane is dark until healed. Fold the heal into row 3.

### Boundary exclusions (absorbed from the sibling)

Not among the 18 and explicitly out of this sitting: the X_BearerToken AAAA
placeholder (triage-shaped, receipt line 54); OPENCODE/OPENCODE2 (rest place
per the B2_253 receipt; powers MagMimoWatchHourly); GEMINI/GOOGLE (not
dump-exposed; gemini auth per the B2_63 receipt). Folding them in couples
unrelated blast radii into a rotation sitting.

### Falsifier

- Kill the at-rest mapping: the pre-sitting census re-run shows a mismatch
  where this packet claims MATCH, or a current name carrying one of the five
  orphans. One head contradiction re-tiers the rows.
- Kill rows 1-2's classification: any consumer of ANTHROPIC_API_KEY_2 or
  ZAI_API_KEY_3 outside the surfaces this revision searched. Named unsearched
  surfaces: corpus/ (hard law), .zcode top-level content trees (skills/,
  workspace/, v2/, plugin-workspace/, export-log-stage/, feedback/; not fully
  walked, `credrot.rev.grep3.txt` stop note), and any machine other than this
  one.
- Kill the collision guard: a sitting-time census shows a same-family
  collision at the head length a row relies on (blocks that family, not the
  packet).
- Kill the rollback chassis: demonstrate one lane whose recovery needs more
  than any-working-value-under-the-canonical-name.
- Close (not kill) wave 2: provider-side evidence an orphan was already
  revoked before 2026-09-26.
- Kill the rotate order: active abuse burning credit on a paid key right now
  (response: pull that one row forward).
- Void this artifact: any value shape or em-dash on these bytes; the
  self-check commands and outputs are filed (`credrot.final.selfcheck.txt`).

### Owed

- Console liveness of any exposed value, and each console's multi-key policy
  (R1): operator-console facts; no network in this lane.
- The .zcode top-level content-tree walk (named above) was not completed;
  three attempts' raw outputs are kept (`credrot.rev.grep.txt` stop note,
  `.grep2.attempt1.txt`, `.grep3.txt` stop note).
- schtasks timings not re-verified live (query returns no rows in these
  shells); quiet-window guidance inherits its citation strength from AGENTS.md
  and the register scripts.
- MagSecretScanWeekly registration: `scripts/` holds seven register_*.ps1
  today (verify2), none registering the secret-scan beat
  (MagCorpusRescanDaily is the B2-104 corpus-map rescan, not a secret scan);
  registering the weekly beat is owed alongside B2-351 (refines the sibling's
  "six scripts" count).
- The 19-vs-12 carrier-file delta: exact per-file attribution of the seven
  ENV-ASSIGN-band files needs a B2_73_dump_census.py rerun, which opens
  corpus files; not done, hard law.
- Stage 2 (B2-350 redaction + beat collapse) is a separate open lane; this
  packet only defines the acceptance shape.

## Critique addressed

1. **Em-dash law (19 found by judge CHECK 5).** This artifact was written
   ASCII-punctuation-only and self-checked: U+2014/U+2013 count on the final
   bytes is 0 (`credrot.final.selfcheck.txt` S4).
2. **R0 pre-snapshot vs policy rule 1.** Resolved by adoption, not
   justification: the local-copy step is deleted, the console is the rollback
   rest place (chassis section), and the snapshot's non-existence is on the
   record (census R1 False; nothing to shred). Policy cite 87-90; sibling
   lines 93-99.
3. **Fresh Groq heads.** Restated as `gsk_QI...(len=56)` and
   `gsk_w2...(len=56)`, the policy rule 1 canonical 6-char-plus-length form,
   labeled at-rest heads not dump heads at both uses (dedicated subsection
   and wave 2 rows 4-5); the publication is justified under the mask law and
   the checkability requirement. Self-check S7 asserts neither head appears
   in any longer form.
4. **Rows 1-2 on a py-only surface.** The widened grep was RUN this revision
   (commands and raw outputs filed; repo all-extensions with corpus pruned,
   .codex full, .zcode cli config surface, .config, .claude, VS Code User,
   Cursor User; .opencode absent; classic roots all zero mentions). It found
   a live consumer for row 1 (openclaw container) and four named references
   for row 2: row 1 is demoted to a rotation-or-retire-with-repoint, row 2 is
   PROVISIONAL and conditional on a sitting-time re-run of the same grep.
   The demotion follows the survivor's own falsifier rule.
5. **Collision guard.** Stated with current bytes: ZAI and GROQ pairwise
   distinct at 8 chars; ANTHROPIC collides at 8 and is keyed off the
   published 17-char heads; OPENROUTER collides at 8, keyed off the
   published 13-char heads (census R4, cited inline). The pre-sitting census
   re-run is prescribed as the standing gate.
6. **Sibling strengths absorbed.** Two-stage B2-349 acceptance with stage 1
   as 18 journal-or-decline lines and stage 2 on B2-350 (QUEUE.md:411
   verified open this revision) with beat-collapse baselines re-counted from
   the stored results JSON; keys.json healing moves (declare-or-retire
   ANTHROPIC_API_KEY_2, absence re-verified; ZAI_API_KEY_3 block flip; vast
   lane name mismatch at providers.yaml:430 re-verified); boundary
   exclusions (X_BearerToken, OPENCODE/OPENCODE2, GEMINI/GOOGLE) carried as
   an explicit out-of-sitting section.

## Decision for the estate

This card closes the credrot decision: rotate the 18 exposed credentials in
this packet's wave order under the revised chassis (no local .env copy; the
provider console is the rollback rest place; revocation deferred until after
each row's verify gate; one journal line or masked decline per credential in
watch/inbox/KEY_ROTATION_JOURNAL.jsonl). It changes three things already on
the books: (1) B2-349's acceptance is amended from the single-stage byte-clean
falsifier to the two-stage gate above (stage 1 journal, stage 2 B2-350 plus
beat collapse), because console revocation cannot edit corpus bytes; (2)
B2-349's ZAI-first execution order is inverted to ZAI-last for the session
safety reason stated; (3) the survivor's rows 1-2 zero-blast retirements are
demoted, row 1 to a rotation-or-retire-with-repoint of the openclaw anthropic
lane, row 2 to a provisional retirement gated on the sitting-time widened
grep, and the .env.prerotation snapshot step is struck. The sitting itself
remains operator-gated and owed: zero rotation has occurred as of this
revision, and no console action, .env edit, or journal write was performed by
this lane.
