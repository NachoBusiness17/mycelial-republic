# RESUME + UPDATE RECOVERY 2026-09-19 (evening window)

writer: zcode-seat (sess_55cc19b6) · order: "full warmed load and resume. Zcode
fucked us on the update" then "self steal, go wide go deep" and "we have 47%
compute on this pro lane... it resets tomorrow and we can go 50 concurrent"

## Update damage assessment (nothing lost)

- All 4 standing automations survived the update (union fullsend, free-resource
  scout, wave tide, drift patrol). FORGE DAEMON is gone from the automation
  list: acceptable, its job (burn GLM quota pre-reset) is dead until tomorrow's
  reset anyway. No re-seat needed.
- No orphaned disk damage: only the usual 19 runtime-churn files were dirty.
- Vision triage had been left at 1,040 rows inline with NO persisted driver and
  NO model provenance. Both defects fixed this window.

## VISION TRIAGE COMPLETE: media_full 1,980 / 1,980 (100%)

Wave resume executed as a seat-vision fan-out on the pro lane:
- 25 chunk agents (40 images each): 803 rows landed, 5 chunks died on the
  provider content filter (1301) with zero rows written (write-at-end design
  flaw, mine).
- Retry design: 20 agents x 10 images with INCREMENTAL writes. 160 rows landed;
  5 chunks refused again (same filter).
- Local sovereign mop-up: qwen2.5vl:3b via scripts/vision_triage_pool.py
  (SSRF-hardened per Mimosa interception: loopback-pinned local lane,
  global-checked groq lane, redirects refused). 31 rows.
- Final 3 images the local lane choked on (msg_423/428/537) read by the seat
  directly: star-trail burst, airliner over harbor sunset, "YOU GOT THIS" chalk.
- Ledger: 1,980 unique msg_ids, zero transport deaths counted as verdicts,
  3 local-lane errors honestly in vision_errors.jsonl.
- Census (negation-safe parser; "no eyes" never counts): numbers 260, water
  173, eye 164, trump 118, clock 109, pyramid 54, door 45, skull 43, key 28,
  bridge 19. Provenance per wave recorded in VISION_READING_B7/B8.json (new
  field the old batches lacked).
- Debt, honest: the old "2,011" denominator has 31 entries not locatable under
  media_full (media/ has zero jpgs). Universe needs re-derivation from
  ledger_full.jsonl next window. 23 historical duplicate rows left in place
  (pre-window idempotency gap, documented not rewritten).

## VERB STONE FOUR LANDED (mag/verb.py)

confident(): GP-semantics confidence. k independent pack-grounded reads,
predictive mean + variance over 0-100 self-scores, CONFIDENT_ASKED and
CONFIDENT_DIST rows in the kifu. Honest n: silent samples are transport deaths
and never fill k. low_confidence fires on n < k or var > 400. Live test:
n=2 of k=3 (one lane death), mean 90, var 0, low_confidence=True because a
sample was lost. The instrument refuses to bluff, exactly as designed.

## THE 50 RELAUNCHED AS A NATIVE DYNAMIC WORKFLOW

.zcode/workflows/the-50.dwf.ts (saved, name "the-50"): one builder subagent
per open task from THE_50_PROGRAM_20260918.md, live results table, fold phase
checks every claimed artifact on disk with files.glob before it counts,
claimed-but-missing listed separately from honest failures, Cerebras key stays
operator-gated. Run it at tomorrow's reset at 50 concurrency:
CreateWorkflow saved { name: "the-50" } with completed=[1,2,6,7] (stones 1-2,
stego scan, vision triage are done).

## GLM DEEP-READ RERUN

Deferred to the reset per operator word ("it resets tomorrow and we can go 50
concurrent"). The 429 verdict from RERUN_BLOCKED.json stands until then; one
capped-vs-uncapped probe on ONE call before the batch, per the driver note.

## ESOTERIC FILLS (partial, honestly filed)

scripts/esoteric_fills.py fired throttled and host-pinned. Result: 3 Steiner
How to Know Higher Worlds translation landing pages (rsarchive GA010, 1909 /
1947 / 1960 editions) plus 1 misc page landed in
memory/corpus/esoteric_canon/steiner_higher_worlds/; the actual chapter texts
are still owed (the translation pages expose no .php chapter links, so the
URL pattern needs one manual look). Duncan's Masonic Ritual FAILED:
sacred-texts 301-redirects even on the explicit index.htm and the crawler
refuses redirects by design, so it needs the redirect target resolved or a
browser-pane fetch (the session-close already classed this class of fetch as
"browser-pane page fetches only, if ever"). Honest logs:
memory/runs/the50/esoteric_fills.json + esoteric_fills_pass2.json.

## Law of the window (extends 2026-09-19)

Content-filter deaths are transport deaths: the 1301 refusals killed whole
agent chunks because writes were end-loaded. Standing rule: any fan-out worker
that accumulates rows must write incrementally, so a mid-flight refusal costs
one image, not forty.
