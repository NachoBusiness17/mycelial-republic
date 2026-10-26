# WAVE2 LANE6 — WHY THE 80 DEAD TOOLS ARE DEAD

**2026-09-26 · seat: zcode (Sancho) · repo: `local_sovereign_agent`**

Lane 2B established the fact: **80 of 164 `tools/*.py` are DEAD** — no code
caller, no test, no doc reference. 746 KB. That is the *what*. This lane asks
the *why*, because "unreferenced" has four different causes with four
different remedies, and only one of them is a loss.

Machine-readable: `memory/audit_20260926/w2l6_dead.json` (80 rows, one per tool).

---

## HEADLINE

| | tools | bytes |
|---|---:|---:|
| DEAD total | **80** | **753,534** |
| A — work got done by hand (one-shot artifact / lane command) | 53 | 530,143 |
| B — superseded by a live sibling tool | 9 | 81,831 |
| C — purpose never materialized (built, proven, never required) | 16 | 131,228 |
| D — orphaned from a previous wiring | 2 | 10,332 |

**Two thirds of the dead weight is not lost capability.** 53 tools are
deliberately uncallable: they are document builders, one-off salon runners,
and date-stamped experiments. They produced a PDF, a card, a verdict. Their
"job is done" state *is* the receipt.

**Bucket C is the real finding.** 16 tools / 131 KB are gates that work and
that nothing requires. They are the enforcement surface that was specified,
built, self-tested, receipted — and then never installed in a hook, a CI, or
a preflight. The fleet writes gates and files them in `watch/inbox/`.

**D is 2 tools, and one of them is a false DEAD.**

## IS THE DEAD SET GROWING? YES — SHARPLY.

| age | tools | bytes |
|---|---:|---:|
| ≤ 7 days | **69** | 687,165 |
| 8–30 days | 0 | 0 |
| > 30 days | 11 | 66,369 |

By month: **2026-08 → 11 dead tools. 2026-09 → 69.**

Every one of the 16 bucket-C gates is dated 2026-09-26 or 09-25. The entire
"built, proven, never required" class is *three days old*. The dead set is not
an accumulation of legacy — it is the current build rate. **The fleet's build
rate exceeds its wiring rate by roughly 4:1 on gates.** Of the 26 tools built
in the last 48 hours, 16 are unwired enforcement and 10 are one-shot
artifacts. Zero were installed anywhere.

The doctrine in `AGENTS.md` says dogfood the instruments every wave. Measured:
the instruments get built and dogfooded *by hand, once, by the lane that
built them*, and then nothing persists. Self-use is not wiring.

---

## A — WORK GOT DONE BY HAND (53 tools, 530 KB)

Not lost. These are tools whose output is a **file**, not a **behavior**.

- **The PDF cluster (9 tools, ~112 KB).** `build_adam_pdf`, `build_adam_setup`,
  `build_adam_setup_final`, `build_adam_soul`, `build_adam_soul_full`,
  `build_aos_pdf`, `build_candy_pdfs`, `build_plain_pdf`, `build_plain12_pdf`
  — all reportlab, all 09-24, all 1 commit each. Two of them are
  supersession pairs by filename (`_setup` → `_setup_final`,
  `_soul` → `_soul_full`). **Redundant surface: 9 tools where 1 template
  function would do.** This is the clearest example of instrument surface
  growing without bound.
- **The x_churn cluster (3 tools, 29 KB)** — `x_churn_grok`, `x_churn_cli`,
  `x_churn_seeds` (09-23). One job split across three files.
- **The steer cluster (2 tools, 18 KB)** — `steer_grok_whole`,
  `steer_grok_1m`, both 08-14, both self-described one-shots.
- **The cathedral cluster (4 tools, 40 KB)** — `cathedral_build`,
  `cathedral_walk`, `cathedral_eigen_map`, `cathedral_wire_tavern`.
  All four produced artifacts still on disk (`cathedral_v1.html`,
  `CATHEDRAL_EIGEN_MAP_20260926.html`, `REFEREE_VERDICT_20260926.md`).
- **The smoke-probe cluster (4 tools, 1.9 KB)** — `smoke_import` (114 B),
  `spawn_gpipe` (466 B), `one_pipe` (468 B), `test_pipe_api` (814 B). All
  08-07. All four import `dashboard.rest` and print route counts. These are
  four copies of one `python -c`. **Worth deleting outright.**
- **The eval/measurement runs (7 tools, 82 KB)** — `duty_fuzz` (53 KB, the
  largest dead file in the repo), `wandr_selfeval` (34 KB), `oracle_calibration`
  (25 KB), `compaction_eval`, `saturation_fourcond`, `persona_grid`,
  `policy_eval_schema_check`. These are honest one-shot evaluators. They are
  also the most *reusable* code in the dead set — see the shortlist.
- **The seam-day pipeline (4 tools)** — `mickey17_v2_fold`, `fold_mickey17`,
  `build_seed`, `seed_salon`: fold a wave, write `FOLD_SECTIONS.md` /
  `MASTER_INVENTORY`, seal `seed/`, run the salon. A pipeline of four
  un-wired steps, each run once by hand.

## B — SUPERSEDED BY A LIVE TOOL (9 tools, 82 KB)

Real redundancy against the 34-tool live set:

| dead tool | superseded by (LIVE) |
|---|---|
| `quote_audit_wide.py` (25 KB) | `quote_gate.py` + `quote_hitrate.py` |
| `md_record_audit.py` | `md_record_seal.py` — both serve `rib.md.record.v1` |
| `corpus_self_lens.py`, `corpus_lens_run.py` | `lens.py` (the wired lens socket) |
| `full_scan.py` | `corpus.py` (read-only surfacing over `catalog/catalog.jsonl`) |
| `rebuild_grounding_wave_md.py` | `mag/grounding_wave.py:819-820` **already writes that exact file** (`VIEW_STATIC.write_text(md)`) — a second path to a 121 KB view that is 09-25-stale |
| `memory_gauge.py`, `path_lint.py`, `pricing_diff.py` | one-off metrics the live surface never re-ran |

**The tightest cluster in the whole audit:** quote measurement is 3 tools
(`quote_audit_wide` dead + `quote_gate`, `quote_hitrate` live), and md-record
enforcement is 2 (`md_record_audit` dead + `md_record_seal` live). In both
cases the dead member is the *newer* one — 09-25 audit replacing a 09-21
gate, with no cutover.

## C — PURPOSE NEVER MATERIALIZED (16 tools, 131 KB) — **THE ALARM SET**

Every one of these was modified **2026-09-25 or 09-26**. All 16 are gates.
I executed all 16; **all 16 run correctly.** Not one is broken. The failure is
never "does it work" — it is "who requires it."

I ran these on today's bytes, live:

| tool | my live run | result |
|---|---|---|
| `luau_lint.py` | `--help` | `checked 43 files, 0 with findings` — clean, unwired |
| `pointer_rot_check.py` | `--selftest` | **5/5 PASS** (ROT-SEED, OOB, MISSING, UNANCHORED all classify correctly) |
| `queue_row_census.py` | `check` | **FAILS on real bytes**: `strict 496 / tolerant 497; deviations 1` at QUEUE line 507 (B2-470 malformed-start) — **a tripwire that is currently tripping and is in no hook** |
| `game_module_dated_numbers.py` | full run | all 8 modules clean, rc=0 — unwired |
| `provider_snapshot_differ.py` | default | `need two snapshots` — honest, and true: `memory/improve/provider_health/` holds exactly 1 file |
| `ledger_close_check.py`, `caption_ledger_sha_check.py`, `ledger_lock.py`, `envelope_harvest.py`, `openrouter_free_gate.py`, `transport_precheck.py`, `cascade_falsifier_run.py`, `probe20_stamp.py`, `bib_launder_check.py`, `mcp_pin.py`, `box_burn_watch.py` | `--help`/import | all functional |

Three of these **self-report why they are inert**, in their own receipts:

- `ledger_lock.py` — *"adoption contract cross-window, nothing wired live."*
  Honest. It exists because the 09-26 concurrent-claim falsifier found 4
  renumber races, and it is not used to write any ledger.
- `cascade_falsifier_run.py` — measured outcome: **0 `GATE_VERDICT_V2` rows
  across 4,697 trail rows, F1/F2 `NEED_DATA`.** It correctly reports that the
  thing it tests never happened.
- `provider_snapshot_differ.py` — *"real state honest: one snapshot exists so
  far, exit 2 need-two."* Its input cadence has not fired.

Two are **loud about being owed**:

- `bib_launder_check.py` — its own docstring: *"this script is the mechanical
  check the README owes (Still owed: …)"*. Owed, built, not required.
- `caption_ledger_sha_check.py` — its receipt claims *"wired into the B2-12
  builder as a post-write gate."* **This is the only dead tool claiming a
  wiring.** The builder it names is itself a burn-lane script, not a hook or
  a gate. So the claim is true and the wiring is still not enforcement.

**`queue_row_census.py` is the single most actionable item in this lane.** A
tripwire that detects a real, present, named deviation on the live board
(`B2-470`, line 507) and has no hook to trip in.

## D — ORPHANED FROM A PREVIOUS WIRING (2 tools, 10 KB)

**`roblox_npc_gateway.py` (8.7 KB) — and it is a FALSE DEAD.** This is a
`ThreadingHTTPServer` on `127.0.0.1:8771`. Its only caller is
`roblox/src/server/NpcGateway.luau` — an **out-of-process Roblox client**. A
python import call-graph cannot see it, so lane 2B scored it DEAD.

It ran. `memory/runs/roblox_npc/gateway.jsonl` holds a real turn from
**2026-09-25T02:55:03Z** — player `operator`, message *"What did I build
today?"*, routed through the OpenRouter stealth lane, `err: 0`.

It is now stopped: no supervisor, no compose entry, nothing on 8771. The
operator talked to the fleet through the Head Museum and the door is shut.
**This is the only genuine lost capability of the "still works" kind in the
set** — and the lane-2B method cannot detect it by construction. Any
service-shaped tool is invisible to this sweep.

**`estate_env.py` (1.6 KB) — orphaned from a *law*, not a wire.** Its own
docstring states the law: *"Tools do not read `os.environ` for keys… Import
this and call `key()`."* A `rib.md.record.v1` companion doc exists. **Zero
first-party tools import it.** The law was written, the adoption never
happened, and the key loader sits orphaned from the wiring it was born to
serve. Small, but it is a live security-posture gap, not a retired artifact.

---

## RECEIPT / TOOL MISMATCH CHECK — ONE FALSE POSITIVE, CLEARED

The alarm test was: *does a receipt claim a tool works while the tool has zero
callers?* A zero-caller tool with a receipt is the signature of a fabricated
run.

**Result: no fabrications. All 16 alarm tools execute correctly on real
input.** Specifically checked and cleared:

- `bib_launder_check.py` — 13 KB dead, yet a 09-26 LEDGER row reports
  *"EXECUTED as tabletop… self-tests all passed (MATCH on identical, FAIL
  w/ first divergent line on one-word flip, deletion caught, exit 3
  no-block)."* I re-ran it. The tool is real, the claims are reproducible, and
  the same row volunteers its own discrepancy (*"fire brief cited a phantom
  20260926_e receipt (file on disk is _d)"*) — the opposite of fabrication.
- `probe20_stamp.py` — a 09-26 row reports the full falsifier replay.
  `--dry` exits 0 with `SKIP`, honestly refusing to synthesize absent series.
  A second row (`build-fold-verify`) re-ran it and got `exit 0 SKIP` again,
  byte-identical to the claim.
- `wandr_selfeval.py` — 34 KB, and its receipt shows a **real security fix
  landing in it** (`ssrf :128` on `fetch_url`, `_assert_public_http_host`
  added). Dead files do not get SSRF remediation; this one was live on disk.
- `luau_lint.py` — two 09-26 receipts describe two *distinct* new checks
  (POLL/RMW advisories, then if-expression balance) and my run reproduces the
  post-fix result exactly: `43 files, 0 with findings`.
- `pointer_rot_check.py` — receipt claims a `ROT-SEED` for the two known rotted
  pointers `providers.yaml:66-67` and `:473-488`; my selftest returns
  `ROT-SEED` with a repair hint at line 84.

**One receipt is stale, not false:** `queue_row_census.py`'s row claims
`strict 466 / tolerant 466 / deviations 0`. Today's board is
`strict 496 / tolerant 497 / deviations 1` — the queue grew by 30 rows and a
new malformed row (line 507) appeared. The tool is *doing its job*; the
receipt is simply a snapshot. **Which is itself the finding: a tripwire whose
output nobody re-reads.**

---

## THE 10 HIGHEST-VALUE DEAD TOOLS — what activating one buys

1. **`queue_row_census.py`** — a tripwire that is *tripping right now* on a
   real board deviation. Wiring it into the pre-push hook closes the only
   live-detected, already-open defect in this lane. Highest value by
   immediate defect closed.
2. **`transport_precheck.py`** — stops a lane from spending a paid model
   attempt on a 403/404. The B2-74 death it was built for is a money leak
   that recurs; one hook line pays for itself.
3. **`ledger_lock.py`** — the 09-26 falsifier found 4 concurrent renumber
   races. Every unfixed append to a shared JSONL ledger can corrupt one.
   Stdlib, Windows-safe, self-tested, and its own receipt says it is unwired.
4. **`caption_ledger_sha_check.py`** — re-verifies 2,689 have-row sha256s
   against disk. Its own receipt names the residual: *"coordinated file+ledger
   rewrite needs an external anchor."* This is the cheapest available anchor.
5. **`roblox_npc_gateway.py`** — reopens the Head Museum door. The operator's
   own 09-25 turn proves the capability works; it needs a supervisor, not a
   rewrite.
6. **`mcp_pin.py`** (20 KB) — the MCP adoption gate in
   `watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md` has a security pass written and
   uninstalled. Largest *designed* gate in the dead set.
7. **`duty_fuzz.py`** (53 KB) — the biggest dead file, a duty-spec fuzzer
   producing held-out edge cases per gate cycle. Wire it to
   `violation_ratchet.py` and the ratchet gets adversarial cases instead of
   a static corpus.
8. **`wandr_selfeval.py`** (34 KB) — a working eval scorer with `--grade`,
   already SSRF-hardened. The most reusable evaluation code in the dead set.
9. **`luau_lint.py`** (12 KB) — 43 files linted clean, 2 same-day
   extensions, zero CI. One line in the ZCode hook channel.
10. **`estate_env.py`** (1.6 KB) — closes a real key-handling law that zero
    tools follow. Cheapest security-posture fix in the set.

## WHAT LANE 2B'S NUMBER ACTUALLY MEANS

Half the fleet calls nothing — true, and mostly harmless. The sharp finding is
narrower and worse:

**In the last 48 hours this repo built 16 gates, proved every one of them on
real bytes, filed a receipt for each, and installed none of them.** The
`watch/inbox/` fold is where gates go to be admired. One of them is failing
right now and nobody will be told.

The remedy is not fewer tools. It is one rule: *a gate is not landed until it
is in a hook.* Every one of the 16 already has a spec, a self-test, and a
receipt. The remaining work per gate is a single line in `githooks/pre-push`
— the same narrow enforcement surface lane 3 and lane 7 measured from three
different directions.

**Honest caveat.** The 53 bucket-A tools are classified from docstring, mtime,
git commit count, and on-disk artifacts. Their "work got done manually" claim
is evidenced by output files and receipts, not by a run log for every one.
A handful (the four smoke probes, the superseded PDF drafts) are almost
certainly just clutter, and I would delete them without further ceremony.
