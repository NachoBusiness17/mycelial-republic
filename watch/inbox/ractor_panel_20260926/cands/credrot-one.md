# credrot-one: the 18-credential rotation decision packet (masked surface only)

Built 2026-09-26 for the operator decision B2-349 gates. Source surface: the
B2_73 masked receipt family plus estate config and code. No corpus dump-carrier
file was opened by this lane (hard law held; the one check I ran on the B2_73
family before reading it is named in Approach). Masked heads below are exactly
the heads already filed in watch/inbox/burn_wave_20260926/B2_73_secret_scan_20260926.md
Evidence lines 46-54; no value, no value fragment longer than the filed head,
no hash of any value appears in this artifact.

## Approach

The rotation is still owed: B2_349_rotation_owed_20260926.md:5 says "OWED,
operator-gated ... Zero rotation has occurred", watch/inbox/KEY_ROTATION_JOURNAL.jsonl
does not exist (verified this lane, ls: absent, matching B2_349 Evidence line 10),
so this packet is live decision support, not post-hoc review. Method: for each
of the 18 exposed values, chain five masked-surface facts into one row: (1) the
masked head from the B2_73 receipt Evidence (the dump-census instrument), (2)
the rest-place name from a names-only root .env census (values never emitted;
54 names enumerated, script printed only the text left of "="), (3) role and
status from configs/keys.json (a names-and-roles registry, no values, verified
by sanitized walk), (4) live consumers from configs/providers.yaml lines plus
grep over mag/ tools/ scripts/ configs/ (corpus excluded from every grep to
keep the hard law), (5) exposure surface from the stored
B2_73_secret_scan_results.json rows (first-6-char masks; provider-rule rows
only, 104 rows across 12 carrier files, counted this lane). The decision frame
is blast radius times rollback quality, not raw exposure count, because all 18
values sit in the same 19 corpus files equally (B2_73 receipt line 9-11); what
differs per credential is what breaks when the value changes and how the
change unwinds.

Pre-read safety check (run before opening any B2_73 file): a python scan of
B2_73_secret_scan_results.json, B2_73_secret_scan_20260926.md, and
B2_73_entropy_watch.json for full provider-token shapes
(sk-or-v1-12+, gsk_12+, sk-ant-12+, sk-proj-12+, xai-12+, sk-hex-20+, bare
hex-32) returned 0 matches on all three, confirming the family is masked
before this lane consumed it. I did not run B2_73_secret_scan.py or
B2_73_dump_census.py: both walk corpus/ and would open the dump carriers.

Count instruments differ and are named wherever a count is cited (census
denominator law): "census" = the dump-census tallies recorded in B2_73 receipt
Evidence (first-8 heads, name-prefixed patterns); "json" = stored scanner
findings (first-6 masks, bare-value rule shapes, storage-capped). Example of
the divergence: DeepSeek sk-effc9 is 23x census vs 16x json for the sk-eff
mask; the JSON's OpenRouter mask "sk-or-" cannot split the two OpenRouter keys
at all (both share the 6-char prefix), so OpenRouter per-key occurrence is not
recoverable from the stored masked surface.

### The packet: 18 credentials, rotate order, blast radius, rollback

Rest-place names: .env lines from this lane's names-only census (XAI 7,
DEEPSEEK 13, VASTAI 16, ZAI 32/35/38/41/44, OPENROUTER 63/64, OPENAI 69,
ANTHROPIC 72/75, GROQ 78/81). keys.json roles quoted from the sanitized walk.

TIER A: zero active blast, rotate immediately, any hour of any day.

| # | Masked head | Rest-place name | Role/status (keys.json) | Live consumers | Exposure | Rollback |
|---|---|---|---|---|---|---|
| 1 | vast 6881759e | VASTAI_API_KEY (.env:16) | vastai_1 "legacy live env key, active" | vast_launcher.py:280-302 (buyer stood down, its own comment at :302 names the console path "vast.ai, Account, API, rotate"), vast_cost.py:125, subscriptions.py:145; NOTE providers.yaml vast lane reads VAST_OPENAI_API_KEY (:430), not this name, so no providers.yaml lane resolves to it | 1 value, carriers not split per-name in stored rows | Console dual not evidenced; deferred revocation: mint, install, verify vast_cost reads it, revoke old. Revert before revoke = reinstall old from console; after revoke = re-mint |
| 2 | xai xai-gO | no current name candidate | unknown (bare paste) | none found; it exists only as the prompt_history bare paste (receipt line 53, json: 2 files) | 1x census, 2 files json | Verify-then-decline: if the console key list does not show this head, journal a decline line; nothing to roll back |
| 3 | xai xai-68sO | XAI_API_KEY (.env:7), lane also accepts XAI_API_KEY_2, GROK_API_KEY(_2) (providers.yaml:503) | grok_cash "PAYG_blocked_by_grok_route_law", status "armed-only-by-operator" | art_forge.py:118, depin.py:358, doctor.py:207/841/934, grok_rightsize.py:91/324, nervous_system.py:33, offline.py:113; but grok_route.py:4 says PAYG cash burned ~$17 Aug 30 to Sep 1 and is now route-blocked, and grok_mirror.py:116 says XAI_API_KEY is now "funded team 715bf1ab", so the current .env value may already differ from the dumped head (dump era matches the burn window) | 21x census, 16x json across 9 files | Console compare first: if the current key is the team key and this head is gone, journal a decline. If still present: mint, install, probe doctor grok check, revoke. Revert = reinstall old until revoke |
| 4 | ZAI bafc5c96 | one of the 5 ZAI names, unresolvable masked-side | one of zai_plan/zai_pro/zai_lite/zai_second_1/zai_second_2 | see ZAI consumers row below | 1x census (the singleton; likely stale or alias) | Console compare; decline-line if no such head; else standard ZAI rollback (row 18) |
| 5 | deepseek sk-c2bd8 | no current name: .env carries only DEEPSEEK_API_KEY, and providers.yaml:364-366 says the second name (Swarm env) was wiped 2026-08-10 | deepseek (single row) | none for a value with no name slot | 4x census | Likely the wiped Swarm key. Console compare; if absent, decline-line closes it; if present, revoke outright (no lane depends on it), revert impossible after revoke, re-mint if ever needed |
| 6-7 | anthropic sk-ant-api03-_NxL and sk-ant-api03-IWEF | ANTHROPIC_API_KEY (.env:72), ANTHROPIC_API_KEY_2 (.env:75) | anthropic_1 "legacy live env key, active"; _2 has NO keys.json row (undocumented rest-place, gap to heal) | providers.yaml:283-296 (lane note: "Claude API (CLI)"), nervous_system.py:34, seat_corpus.py:179 ("when filled"), subscriptions.py:133 (CHECK); no always-on consumer found | codex dump carries both values, grok copy has them empty (receipt line 49-50) | Two names prove two concurrent keys exist estate-internally: dual-key window per name. Mint, install slot 1, probe lane, revoke old; repeat slot 2. Revert until revoke = reinstall old value from console |

TIER B: bounded blast, dual-key window, rotate in a task-quiet window (after
09:30 local; the 08:00 improve, 08:30 census patrol, 09:00 FTS tasks per
AGENTS.md and scripts/register_improve_task.ps1:1, register_census_patrol_task.ps1,
register_fts_index_task.ps1; avoid Monday 06:40 secret-scan slot per B2_351).

| # | Masked head | Rest-place name | Role/status | Live consumers | Exposure | Rollback |
|---|---|---|---|---|---|---|
| 8-9 | openrouter sk-or-v1-4167 and sk-or-v1-6be0 | OPENROUTER_API_KEY (.env:63), OPENROUTER_API_KEY_2 (.env:64) | openrouter_1/_2 "agentic_auto" | providers.yaml:174-182 (18 free lanes rotate across both names by design), health.py:160, free_tier.py:67-73, nervous_system.py:29, handoff_escalation_watcher.py:122 | 28 rule rows json, 7 files, not splittable per key by mask; census heads as named | The estate already runs both names concurrently (providers.yaml:178), so: rotate _2 first (mint, install, run the health.py openrouter check and one free-lane chat gate), revoke old _2, then _1 the same way. Revert until revoke = reinstall old value. Free lanes keep firing off the sibling key during each half |
| 10-11 | groq gsk_17bq and gsk_8LAQ | GROQ_API_KEY (.env:78), GROQ_API_KEY_2 (.env:81) | groq_1/_2 "fast_bulk" | providers.yaml:304, free_tier.py:58, fuel_feed.py:57 (comment: "dual-key (GROQ_API_KEY + _2)"), lane_probe.py:37, nervous_system.py:33 | 14x each json, 7 files each | Dual-key window exactly as fuel_feed's dual-key design assumes: one name at a time, sibling carries bulk while the other swaps. Revert until revoke = reinstall old |
| 12 | deepseek sk-effc9 | DEEPSEEK_API_KEY (.env:13) | deepseek "workhorse_paid_cheap" | providers.yaml:363-366, doctor.py:214/844, depin.py:362, offline.py:113, lane_probe.py:25, nervous_system.py:30 | 23x census, 16x json, 9 files | Highest-traffic single-name key. No local proof DeepSeek supports concurrent keys (only one name ever in .env), so: mint new, install, run lane_probe deepseek leg, only then revoke old. Until revoke, revert = reinstall old; after revoke, revert = re-mint (minutes, paid console) |
| 13 | openai sk-proj-UjAW | OPENAI_API_KEY (.env:69) | openai_1 "legacy live env key, active" | providers.yaml:264, ox_swarm.py:71 (second independent seat), subscriptions.py:118/137 (WATCH), handoff_escalation_watcher.py:100 (optional cloud, gated by MAG_ESCALATE_CLOUD), offline.py:113, nervous_system.py:35 | 43x census (the most-repeated value in the dump), 14x json, 7 files | Same single-name pattern as row 12: mint, install, probe (subscriptions watcher or one gated call), revoke. Revert until revoke = reinstall old |

TIER C: the seat's own account family. Rotate last, windowed, plan-key at a
session boundary.

| # | Masked head | Rest-place name | Role/status | Live consumers | Exposure | Rollback |
|---|---|---|---|---|---|---|
| 14-18 | ZAI 088650c6 (36x), e18faf05 (34x), 4f8ac54f (34x), 3254aca9 (19x), e3c50501 (16x), plus bafc5c96 row 4 above | ZAI_API_KEY (.env:32), ZAI_API_KEY_2 (:35), ZAI_API_KEY_3 (:38), ZAI_API_KEY_Pro (:41), ZAI_API_KEY_Lite (:44); 6 values, 5 names, so one value maps to no current name | zai_plan "coding_plan_session", zai_pro "paid_lane", zai_lite "metered_lite_burst, ceiling lite_guard", zai_second_1 "gopher_and_task_wall", zai_second_2 "alias-pool, same_account_as_second_1" | autoglm.py:37, fanout.py:38 (DEFAULT_KEY_ENV ZAI_API_KEY_Lite), flight_recorder.py:343-344 (Pro and main), free_tier.py:52/80 (Lite and plan lanes), gopher_lite.py:43 (_2), lane_runner.py:602, lite_guard.py:47, lite_scale.py:52, art_forge.py:119, lane_probe.py:31, providers.yaml:541/553/568/581; ZAI_API_KEY_3 has no providers.yaml lane reference (orphan rest-place name) | 6 values per census; ZAI class not covered by any json provider rule (rides the ENV-ASSIGN band) | Five concurrent names prove multi-key consoles: rotate one name per sitting in blast order Lite (free-tier gopher lanes), then Pro (flight recorder), then _2 (task wall; note _3 is alias-pool same-account, one console action may cover both, check before minting), and ZAI_API_KEY LAST at a session boundary because it is the coding-plan account this very panel and every Task-agent width ride (AGENTS.md fan-out law); rotating it mid-wave orphans running children. Revert until revoke = reinstall old value from console; after revoke, re-mint. lite_guard ceiling (keys.json zai_lite) must be re-checked after the Lite swap |

Order summary (the actual answer to "what order"): rows 1-7 now, rows 8-13 in
the next task-quiet window, rows 14-18 across separate sittings ending with
ZAI_API_KEY at a session boundary. This inverts B2_349's "ZAI first, largest
blast radius first" order (B2_349 Work-done point 2): rotating the fleet's own
account family first maximizes simultaneous breakage for zero additional
risk reduction, since all 18 values are equally dead the moment their console
revocation lands and nothing about ZAI-first kills exposure faster.

Rollback law for every row (no recommendation without it): the provider
console is the rollback rest-place, not any local byte copy. Policy rule 1
(one rest place per key, SECRET_SCAN_RULESET_ROTATION_20260926.md:87-90) forbids
a .env backup copy, and .env is untracked (git ls-files empty; .gitignore:19),
so value recovery after an edit mistake is console-side only. Therefore every
rotation above defers revocation until the post-install probe passes, which
keeps "reinstall old value" live as the revert path; after revocation the
revert degrades to re-mint, which is acceptable only after the probe passed
once. Journal one line per credential in watch/inbox/KEY_ROTATION_JOURNAL.jsonl
naming provider, masked old head, masked new head, date (B2_349 Work-done 2
shape). Declines (rows 2-5 where the head is already gone) get journal lines
too, or B2_349 stays open.

Acceptance, corrected: B2_349's falsifier arm (b) "a post-rotation rerun of
B2_73_secret_scan.py over the corpus finds none of the 18 masked heads" cannot
pass from rotation alone: console revocation does not edit corpus bytes, and
B2_350 (redact-on-harvest, still open in QUEUE.md line 411) is the byte-level
fix. Two-stage acceptance instead: stage 1, rotation done = 18 journal lines
(or masked decline lines) plus console states; stage 2, byte-clean = after the
B2_350 redaction pass the Monday MagSecretScanWeekly beat
(watch/inbox/SECRET_SCAN_BEAT.jsonl, B2_351 receipt) shows the provider-rule
counts for OPENROUTER-KEY 28, GROQ-KEY 28, XAI-KEY 18, DEEPSEEK-KEY 16,
OPENAI-CLASSIC 14 collapse toward zero for these classes.

Boundary facts so the operator does not over- or under-rotate: the X_BearerToken
AAAA placeholder (keys.json x_bearer "read_search_v2") is triage-shaped, NOT
one of the 18 (receipt line 53-54); OPENCODE/OPENCODE2 and GEMINI/GOOGLE keys
were not dump-exposed (not in the 18; OPENCODE rest-place per B2_253 receipt,
gemini per B2_63 receipt) and need no action from this packet.

## Moves with estate paths

1. Operator console sitting in this packet's order (Tier A rows 1-7 now, Tier B 8-13 next quiet window after 09:30 local, Tier C 14-18 across sittings, ZAI_API_KEY last at a session boundary), journaling every action and decline to watch/inbox/KEY_ROTATION_JOURNAL.jsonl (path fixed by watch/inbox/SECRET_SCAN_RULESET_ROTATION_20260926.md section 2 rule 2; line shape fixed by watch/inbox/burn_wave_20260926/B2_349_rotation_owed_20260926.md Work-done 2).
2. Deferred-revocation rollback procedure for every rotation: mint, install into the single .env name slot (the names-only census in this packet plus B2_349 Evidence line 10 is the name inventory), probe with the named instrument per row (the openrouter check in the health module, the deepseek/zai/groq legs of the lane probe, the grok check in doctor, one free-lane chat gate per providers.yaml:182), only then revoke old; this keeps reinstall-old-from-console live as the revert path and honors policy rule 4's real ordering concern (revocation before any history rewrite; no rewrite is proposed until all 18 close).
3. Close B2_349 honestly with the two-stage acceptance: 18 journal lines (or masked declines) as stage 1; then land the still-open redaction lane QUEUE.md B2-350 (watch/inbox/burn_wave_20260926/QUEUE.md line 411) as stage 2 and read the drop in the Monday beat watch/inbox/SECRET_SCAN_BEAT.jsonl (instrument proven by watch/inbox/burn_wave_20260926/B2_351_secret_scan_schedule_20260926.md).
4. Heal registry gaps while rotating, all in configs/keys.json (names-and-roles file, no values): add the missing ANTHROPIC_API_KEY_2 row, resolve the ZAI name-to-masked-head map console-side and record it in the journal (masked heads only), decide ZAI_API_KEY_3 (alias-pool, no providers.yaml consumer at configs/providers.yaml lines 541-581) keep-or-retire, and record the vast lane name mismatch (VAST_OPENAI_API_KEY at providers.yaml:430 vs rest-place VASTAI_API_KEY).
5. Do not touch what this packet excludes: X_BearerToken placeholder, OPENCODE/OPENCODE2, GEMINI/GOOGLE keys (not dump-exposed; their lanes carry separate open questions in watch/inbox/burn_wave_20260926/B2_63_gemini_auth_20260926.md and B2_253_transport_decision_20260926.md); folding them into the rotation sitting would couple unrelated blast radii.

## Falsifier

This packet dies if any of these hold. (a) Any listed zero-blast consumer claim is wrong: show one live traffic path through VASTAI_API_KEY (buyer re-armed), or through XAI_API_KEY (route law lifted without this lane seeing it), and rows 1-3 mis-tier the sitting. (b) The dual-key window is infeasible for a provider I marked dual (OpenRouter, Groq, Anthropic, ZAI): a console that forces revoke-before-mint degrades every affected rollback story to re-mint; the five-concurrent-names evidence (providers.yaml:178, .env ZAI rows) is then misread as console policy rather than account configuration. (c) Any of the 18 heads is already revoked or is a documented fixture (B2_73 receipt Falsifier arm 2): the order collapses to a decline-journaling exercise. (d) The name-to-head unknowability claim is wrong: if a masked-surface byte somewhere maps, say, 088650c6 to ZAI_API_KEY_Pro, my Owed list overstates and the ZAI sitting order can be pre-planned. (e) This artifact itself carries a value shape or an em-dash: the self-check commands and their outputs are filed below; a nonzero count on the final bytes voids the artifact under this card's own kill condition.

Self-checks run on the final bytes (both re-run after the last edit):
- Value-shape scan: .venv/Scripts/python.exe running the same 7 provider-token regexes used in the pre-read check over this file: 0 matches (output filed in the lane transcript of this candidate run).
- Em-dash scan: a python scan of this file for U+2014 and U+2013: 0 matches.

## Owed

- Name-to-masked-head map for all 18: not resolvable from the masked surface; needs the provider consoles (most consoles show key prefixes). The packet's tiering therefore orders name slots, and step 0 of the sitting is console-side head resolution.
- Liveness of any of the 18 values: unverified, by design (no remote calls this lane; B2_73 receipt lines 60-62 made the same call).
- Whether the corpus dump carriers ever left the machine (policy event 3c escalator): no receipt I read determines it; if they did, severity rises above event-driven routine and the Tier C session-boundary courtesy may need to be waived.
- Per-name carrier files for ZAI, Anthropic, VastAI values: the stored B2_73_secret_scan_results.json carries 0 corpus-side ENV-ASSIGN rows for the exposed family names (counted this lane; the ENV-ASSIGN storage band was consumed or capped by other rules), so only the dump-level carrier list in the receipt prose (grok session 01a04e25 files, codex rollouts 08-30 x2, 09-01 x4, 09-02 x3, marathon_body, nacho preflight, prompt_history) names the surface; per-value splits do not exist in any filed byte I found.
- Scheduled-task facts: my own schtasks query returned no rows in this shell (exit 1, no output), so the 08:00/08:30/09:00/06:40-Monday timings are cited from AGENTS.md, scripts/register_improve_task.ps1:1, the other register scripts, and the B2_351 receipt, not re-verified live; the quiet-window recommendation inherits that citation strength.
- MagSecretScanWeekly has no register script in scripts/ (six register_*.ps1 files exist, none for it): if the machine rebuilds, the weekly beat that my stage-2 acceptance reads is unregistered; re-registering it is owed alongside B2_351.
- The post-rotation byte-level rescan and the B2_350 redaction pass: not run and not runnable by this lane (both open corpus dump carriers; hard law). They stay operator or dump-cleared-lane work.
- Rollback rehearsed only on paper: no probe named in the rollback column was executed this lane, so "revert until revoke = reinstall old" is policy-grounded (consoles retain unrevoked keys) but not yet instrument-proven for any single provider.
