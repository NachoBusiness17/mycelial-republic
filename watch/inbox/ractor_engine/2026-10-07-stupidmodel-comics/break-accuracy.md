# BREAK-ACCURACY PASS: stupid-model comics lens (hostile second seat, 2026-10-07)

Seat: break-accuracy. Every check below was executed this sitting; commands named
inline. No paid keys touched; the only network calls were localhost ollama
(/api/tags, the reproduction probe), api.github.com, pypi.org, and two web
searches. No em-dashes. Nothing edited belonging to the lens; my artifacts bank
beside theirs (break_accuracy_checks.py, break_accuracy_defect_test.py,
break_accuracy_rerun.py, break_accuracy_rerun_results.json).

## Verdicts

### F1 falsifier PASSES (qwen2.5:3b 7/8 spec_valid): CONFIRMED, upgraded to CONVERGENT

- Byte-check: probe_panel_spec_results.json holds 32 rows, ts 2026-10-07T14:56Z,
  file mtime 10:56:43 -0400 (matches ts). I mechanically re-derived the summary
  from the rows: all four arms MATCH (qwen 8/8 parses, 7/8 spec_valid, mean
  6.8s; gemma:2b format_json 7/5/1 error; gemma unconstrained 8/6/11.9;
  deepseek 6 parses/1 spec). Command: break_accuracy_checks.py section 2.
- Independent refire (the hostile arm): break_accuracy_rerun.py, same prompts,
  same arms, scorer bubbles-loop guarded, 32 fresh calls at local ollama, $0.
  qwen2.5:3b-instruct format:json: 8/8 parses, 7/8 spec_valid (mean 9.0s).
  EXACT spec_valid reproduction on fresh generations. gemma:2b unconstrained:
  8/8 parses, 6/8 spec (mean 12.0s) also exact. deepseek: 7/8 parses, 1/8 spec.
  Results: break_accuracy_rerun_results.json.
- Scorer-defect story: unit-proven this sitting. The persisted
  probe_panel_spec.py:89-91 has the unguarded `for b in bub:` (file mtime
  10:52:26 -0400, before the results file; not edited after the run). A 3-panel
  payload with `"bubbles": null` raises exactly `TypeError: 'NoneType' object
  is not iterable` (break_accuracy_defect_test.py); the one-line guard fixes it
  and that shape scores spec_valid False. So the banked error row (gemma
  format_json prompt_i 3) is a scorer crash, not a model failure, and the
  parses correction 7 -> 8 is sound: my guarded refire independently reads
  8/8 parses, 0 errors.
- Residual: the specific corrected cell "6/8 spec" for gemma:2b format_json is
  NOT in any persisted artifact (accuracy.md:54-57 admits the rerun raw was not
  persisted); my fresh guarded arm reads 5/8. Both arms bracket 62-75 percent;
  the correction's direction is confirmed, its exact number is not.
- Payroll claim: /api/tags read this sitting confirms qwen2.5:3b-instruct
  (1.93 GB), gemma:2b, deepseek-r1:1.5b, gemma4:latest (9.6 GB) all local. The
  ask's named free seats (llama-3.2-11b-vision, qwen2.5:7b) were covered by the
  sibling econ arm A (seats listed in econ_probe_results_arm_a.json), so the
  lane as a whole fired the named payroll; the format-door arm used the 3B.

### F2 M1-transfer correction (gemma:2b parses unconstrained): CONFIRMED with two sharpenings

- Byte-check: gemma:2b unconstrained 8/8 parses, 6/8 spec_valid, mean 11.9s is
  in the persisted summary and rows, and my refire reproduced 8/8, 6/8, 12.0s.
- m1_bench.json read: 0/30 unconstrained vs 30/30 is byte-true, BUT the M1
  winning arm is `format_schema_valid` (a TYPED JSON schema), not format:"json".
  The comic probe fired the GENERIC json door. The lens's "half wrong" verdict
  is right in direction and under-sharp in mechanism: the M1 flip was measured
  on a different door. Estate bytes settle the three doors: generic json buys
  parse + latency (probe; 11.9s -> 5.8s), the typed schema buys vocabulary
  (moonshot-1.md M3: generic json dropped the pose key on 8/8 rows;
  econ arm B typed schema: 10/10 in-vocabulary). The comic lane's citation
  chain should be the typed-schema door, not M1's generic flip.
- Detail defect byte-found: "(one fenced ```json output)" is wrong. TWO
  unconstrained rows are fenced (prompt_i 0 and prompt_i 5, raw_head starts
  ```json in probe_panel_spec_results.json). Both still extracted (parses true).

### F3 operator model = Gemma 4 26B-A4B, snapshot-priced: WEAKENED (facts confirmed, one headline clause false, move trips a dead gate)

- Snapshot bytes confirmed: watch/inbox/endpoint_news/snapshot_openrouter.json
  (mtime 2026-10-07 09:01:56 -0400 = 13:01Z) entry google/gemma-4-26b-a4b-it
  has prompt_price "0.00000009", and google/gemma-4-26b-a4b-it:free has
  free: true. Command: break_accuracy_checks.py section 1.
- Family facts live-verified: huggingface.co/google/gemma-4-26B-A4B fetched
  this sitting: Total Parameters 25.2B, Active Parameters 3.8B, License Apache
  2.0, image-text-to-text. The lens's "~26B total, ~4B active MoE, Apache-2.0"
  holds (precise: 25.2B/3.8B). ai.google.dev/gemma/docs/core TIMED OUT from
  this seat: not verified, OWED.
- Identification is inference, not proof, and the snapshot does not uniquely
  pick 26B-A4B: the same snapshot also lists google/gemma-4-31b-it and
  google/gemma-4-31b-it:free, plus gemma-3-4b-it. The operator's phrase was
  never confirmed by the operator. Best candidate, yes; asserted identity, no.
- The "reachable through the two already-wired openrouter providers" clause is
  FALSE today: memory/runs/free_lane_fleet/health.json reads openrouter-free-1
  consecutive_fails 6 (no last_ok), openrouter-free-2 consecutive_fails 5
  (last_ok 2026-10-05T07:00:27Z); the cycle loop skips any provider at fails
  >= 5 (tools/free_lane_fleet.py:306-308). Wiring exists (:116-121 byte-read);
  reachability does not. The move's "15 min, let the 30-min clock score it"
  would silently never fire until keys are re-provisioned and health reset.
  Sibling receipt economics.md E3 (82-99) found the same dead pair.
- Local tag identity: resolved by a sibling arm, not by this lens:
  moonshot-1.md M2 (/api/show) reads gemma4:latest parameter_count
  7,996,157,674 (~8B): the local seat is NOT the 26B-A4B. The lens's
  UNVERIFIED caution was correct and is now answered.

### F4 carrier correction (SVG fails at Discord hop; PNG twin needed): CONFIRMED on facts, cite struck, move contradicted by siblings

- venv census reproduced exactly by me (break_accuracy_checks.py section 4):
  cairosvg False, svglib False, resvg not on PATH, PIL present and
  ImageDraw importable True.
- mag/phone_relay.py read in full (249 lines): _api sends JSON bodies only
  (:93-95); every post is {"content": ...} (:175, :195, :211, :214, :220);
  no attachment/embed/multipart path anywhere. Text-only confirmed.
- Discord SVG refusal: corroborated at web level this sitting (400 "Could not
  process image" outside PNG/JPEG/GIF/WEBP; the standing 2019 support thread
  "Allow SVG input for thumbnails in embeds"). BUT the specific cite
  "discord-api-docs issue #25935" is a PHANTOM from this seat: GitHub API
  returns Not Found for that number; the repo has issues enabled (298 open);
  repo-scoped searches for "Could not process image" return 0 and "Could not
  process" return 2 unrelated issues. The claim stands, the citation does not.
- The MOVE ("phone_relay multipart extension posting to the DM lane") is
  contradicted by the same ractor's sibling receipts: the DM lane is
  approvals-only BY LAW (mag/phone_relay.py:137-159 "Never a shared guild
  channel"; communication.md F2: comics traffic there would violate the lane's
  founding law), and the guild channel has been 403-locked (50001) since 09-15
  with an operator-gated two-click unblock (communication.md F3, FW30 runbook
  watch/inbox/fifty_wide_20260917/FW30_discord_runbook.md). Convergent sibling
  verdict: Discord is LAST in build order; dashboard and watch/inbox are the
  live faces. The two-renderer carrier is right; the wiring point in the move
  is wrong.

### F5 external prior-art verdict (no product; pieces exist): CONFIRMED, scoped, with missed prior art

- cmx.js live-verified field-for-field via GitHub API this sitting: darwin/cmx.js,
  798 stars, JavaScript, description "[prototype] A library/markup for building
  xkcd-style comic strips", pushed 2013-04-22, license NOASSERTION, homepage
  cmx.io. Every number the lens cited is byte-exact.
- SVGBob verified: ivanceras/svgbob, Rust, Apache-2.0, 4235 stars, pushed
  2026-04-22 (alive); pypi vye-svgbob verified (0.1.4, "Render ASCII art
  diagrams to SVG using the Rust crate svgbob").
- GAUNTLET receipt: dice "2/2 PASS" and the "$0.00" register headline
  byte-found (watch/inbox/GAUNTLET_FREE_LANDED_20261006.md:31-33).
- The "NO product" universal survived my attack: two fresh web searches this
  sitting (discord bot comic summary; changelog/release-notes comic generator)
  found fetch-only xkcd bots, prompt-to-raster generators (LlamaGen, Vondy),
  Canva/Firefly templates, and the assessment "Nothing off-the-shelf currently
  combines all of this". Per quantifier law the claim survives SCOPED to the
  searches run (mine + the lens's); the lens's own falsifier already names the
  top.gg blind spot.
- Missed prior art (my additions): gramener/comicgen (open-source SVG comic
  engine with character libraries; deterministic, maintained; closer to this
  lane's renderer than cmx.js) and matplotlib's xkcd style mode (deterministic
  wiggle + font conventions for the PIL/SVG look). A davidwalsh.name "Comix
  I/O" result is likely cmx.io coverage; flagged, not verified distinct.

## Blind-spot adjudication

- Census: my rerun of `git grep -li <term> -- mag tools corpus watch` reads
  xkcd 26 / stickfigure 0 / mermaid 84 / voxel 83 / comic 75 / electron 283
  (comics alone: 16), matching accuracy.md's rerun exactly. The ask's
  stickfigure 3 is now EXPLAINED: 2 tracked hits live outside the four-dir
  scope (memory/corpus/shadertoy21k/.../3tdXDl.fragment and .../XdByzy.fragment)
  and the ractor's own lane docs are untracked (git grep default excludes
  untracked; with --untracked the scoped count is 3). Different instruments,
  both honest; the discrepancy is reconciled, not a defect.
- n=8 doubt: answered for qwen by the independent refire (pooled 14/16
  spec_valid across two arms). The n=50 gate remains the right admission bar.

## Additions (what the lens missed), each falsifiable

1. DEAD-PROVIDER GATE: the :free seat move never fires until keys are
   re-provisioned (health.json fails 6/5; skip gate free_lane_fleet.py:306-308).
   Falsifier: a health.json reset + one fleet cycle scoring a gemma-4 row.
   Move: pair the 15-min row add with key re-provision + health reset (15 min
   + operator), else the seat is theater.
2. DM-LANE LAW + 403 WALL: finding 4's delivery move violates the DM lane's
   founding law and ignores the 22-day guild 403. Falsifier: a live multipart
   post to #game-c-overview after the FW30 two-click unblock. Move: retarget
   the 90 min to the dashboard/watch-inbox face first; attach the FW30 unblock
   ask to the next DAWN_REPORT (10 min, communication F3's move).
3. TYPED-SCHEMA DOOR IS THE REAL M1 INHERITANCE: generic format:"json" does
   not lock vocabulary (moonshot M3: pose key dropped 8/8; econ arm B typed
   schema: 10/10). Falsifier: the n=50 run under the typed schema regressing
   below the generic-json rate. Move: freeze the panel spec as a typed schema
   with enums + required (same 60-90 min, different artifact than a prose
   instruction).
4. CONVERGENT REPRODUCTION: qwen 7/8 is now two independent arms (this pass's
   refire + the lens's probe). Falsifier: the n=50 gate regressing qwen below
   6/8. Move: none beyond running the owed n=50; cite both arms in the
   gauntlet register.
5. PHANTOM CITE: discord-api-docs #25935 unverifiable (Not Found; repo searches
   empty). Falsifier: producing the live issue URL. Move: strike the number
   from accuracy.md, cite the web-corroborated 400 + the 2019 support thread
   (5 min).
6. PRIOR-ART ADDITIONS: gramener/comicgen and matplotlib xkcd style belong in
   the steal map beside cmx.js/SVGBob. Falsifier: neither rendering a
   3-panel stick strip from a parametrized spec. Move: read comicgen's panel
   schema before freezing the estate's field names (20 min).

## Commands run this sitting (evidence chain)

- ./.venv/Scripts/python.exe watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/break_accuracy_checks.py
- ./.venv/Scripts/python.exe .../break_accuracy_defect_test.py (TypeError repro + guard proof)
- ./.venv/Scripts/python.exe .../break_accuracy_rerun.py (32 calls, $0, background, exit 0)
- git grep -li <term> -- mag tools corpus watch (7 terms) + --untracked variant
- curl api.github.com: /repos/darwin/cmx.js, /repos/ivanceras/svgbob,
  /repos/discord/discord-api-docs, /repos/discord/discord-api-docs/issues/25935,
  /search/issues (2 queries)
- curl pypi.org/pypi/vye-svgbob/json
- WebFetch huggingface.co/google/gemma-4-26B-A4B (live: 25.2B/3.8B/Apache-2.0);
  WebFetch ai.google.dev/gemma/docs/core TIMED OUT (OWED)
- WebSearch x2 (discord comic-summarizer product; changelog comic generator)
- Byte reads: m1_bench.json, snapshot_openrouter.json, free_lane_fleet.py
  (:55,:114-139,:300-315), health.json, phone_relay.py (249 lines),
  GAUNTLET_FREE_LANDED_20261006.md, accuracy.md, economics.md, moonshot-1.md,
  communication.md (F2/F3/F5), all 4 probe result JSONs' summaries + seats.
