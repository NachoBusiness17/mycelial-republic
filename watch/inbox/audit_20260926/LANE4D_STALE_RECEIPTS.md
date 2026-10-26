# LANE 4D — STALE RECEIPTS: the organs were run

**Lane:** 4D · **Date:** 2026-09-27 · **Mode:** audit only — report, no repair
**Machine receipt:** `memory/audit_20260926/lane4d_stale.json` (24 rows, valid JSON)

> The Elder's next_action for a stale receipt reads *"run one bounded live dogfood step."*
> These were the steps. Unproven is now mostly proven. **One organ is genuinely broken, and
> it is the one the Elder already suspected** (`water_computer` → `proof_failed`).

---

## 1. Counts

| Verdict | Count | Organs |
|---|---|---|
| **WORKS** | **16** | ask_router, atlas, board_tailer, harness, live_ops_readiness, main_channel, read_archive, self_audit, session_bridge, trajectory_rib, policy_engine, switchboard_v2, host_resolver, swarm_worker, research_worker, organ_map |
| **BROKEN** | **1** | **water_computer** |
| **NOT-RUNNABLE** | **4** | basecamp, fireball_cycle, swarm_cycle, fleet_structure |
| **FINDING** | **3** | environmental / data-integrity rows |
| **SUSPECTS-HANG** | **0** | nothing exceeded the 60 s wall |

Of the 13 organs the Elder flagged `receipt_stale`: **9 WORKS, 3 NOT-RUNNABLE, 0 BROKEN.**
The only BROKEN organ in the whole set is `water_computer`, whose gap was `proof_failed`,
not `receipt_stale`. **The "stale receipt" gap code was hiding nothing — every stale organ
that can be safely exercised works.** The real defect sits under a different code.

---

## 2. BROKEN — `water_computer` (root-caused, not just observed)

`mag.organ_map` runs `water_glass` as a deterministic proof: the demo must **win and not
cheat**. It does neither. It does not crash — every step returns `ok: true`, and
`cheated` is `false`. It just never wins.

```
{"ok": true, "schema": "water_computer.v1", "campaign_id": "gc-b0fb97573b",
 "won": false, "cheated": false,
 "glass": "SOURCE ··· 0 | WORK ··· 0 | OUT ··· 0 | A closed  B closed | GLASS: height is the computation. Bucket is a lie."}
```

**Root cause: the scripted walkthrough's verbs do not match the parser.** In the transcript,
`open valve` narrates *"This is not a door."* and `wait` narrates *"Time passes."* with zero
state change. All three tanks read `0` at the end. The proof can therefore never return
`True`, so `proof_failed` is permanent and `water_computer` is pinned at `WIRED`, never
`VERIFIED`. This is a content/logic defect in the demo script, not an exception.

**Side effect discovered while root-causing it — this one is worse than the broken proof.**
`water_computer._play_demo()` is **not side-effect-free**. It calls
`game_campaign.begin_play(force_new=True)`, which:

- writes a fresh **9.4 KB `memory/working/game_campaigns/gc-*.json` on every invocation**
  (410 files have accumulated), **and**
- **OVERWRITES the shared `memory/working/game_characters/operator.json`** with the demo's
  throwaway character (`Operator / engineer / curious / sight-notes`, bound to a transient
  campaign id).

This runs on **every `organ_map` call** — the organ map is the fleet's most-called read-only
instrument, and its cheapest proof quietly litters `memory/working/` and stomps a
canonically-named file. A "read-only" proof with write side effects is a trap for every
future auditor who trusts `proof: read-only`.

---

## 3. NOT-RUNNABLE — no safe read-only mode exists

Recorded as instructed, without forcing flags to find a destructive path.

| Organ | Why it cannot be run read-only |
|---|---|
| **swarm_cycle** | **Refused on safety grounds.** `cycle()` calls `mag.verkle_lance link` **unconditionally**. The `--dry` flag gates *only* the salon step (`mag/swarm_cycle.py:165-171`); the chain link at line 176 is not gated. `--dry` is documented *"structural first light, $0"* but it folds a verkle knot, runs `mag.surface_render all`, and posts a blackboard note. **The most dangerous organ in the stale set. NOT RUN.** |
| **fireball_cycle** | `run()` calls `elder.audit()`, which writes `memory/runs/elder/audit.json` + appends `receipts.jsonl` — then `atlas.build()` and `basecamp.status()`, two more writers. One fireball turn touches three organs' state. |
| **basecamp** | `status()` is the only entry point and it writes `memory/runs/basecamp/status.json` + appends receipts; it also calls `atlas.build()` (a writer). Its *climb logic* was proven indirectly by read-only replay over `map_organs()`: 33 organs, 19 gaps, 0 ghosts. |
| **fleet_structure** | Config organ — empty `module`/`callable`, `proof: ""`. It is a doctrine surface, nothing to execute. |

---

## 4. WORKS — the stale organs, with real output

Every one of these exited **0** with real output and **zero writes** to tracked surfaces.

| Organ | Mode run (real exit code + first line) |
|---|---|
| `ask_router` | read-only replay of the ranking engine → `{"ledger_rows": 1, "lanes_priced": 8, "dormant_cerebras_priced": false, ...}` — 8 lanes priced, dormant `cerebras` correctly dropped (B2-521 gate live), `deepseek` top at 90.18. |
| `atlas` | `mag.atlas status` → `{"ok": true, "schema": "atlas.v1", "ts": "2026-09-01T18:59:37.409367Z", ...}` |
| `board_tailer` | read-only probe of `_candidate()` + `board_directive._decode()` → 4/4 synthetic records classified (proposal / ignored_no_marker / ignored_non_directive_event). |
| `harness` | `mag.harness status` → `{"ok": true, "queue_depth": 4, "active_leases": 0, ...}` |
| `live_ops_readiness` | `snapshot()` imported directly → `{"ok": true, "schema": "live_ops_readiness.v1", "lifecycle": ...}`, zero provider calls, zero secrets read. |
| `main_channel` | `self-test` → `{"name": "closed_route", "ok": true}`; 4/4 classifier asserts pass. `status` also rc=0, zero writes. |
| `read_archive` | `mag.read_archive /board/openclaw_traj.jsonl:1-3` → bounded span with path guard intact. |
| `self_audit` | `mag.self_audit status` → `{"ok": true, "schema": "self_audit.v1", "last_ts": "2026-08-30T16:12:42.386955Z", ...}` |
| `session_bridge` | `mag.session_bridge read --limit 5` → `{"count": 4, "messages": [...]}` — riddler path-stripping visible. |
| `trajectory_rib` | full compiler with `--output` redirected to scratch → rc 0, fleet's `compiled.jsonl` untouched. |

Beyond the 13 stale organs, the other 7 gaps were also exercised: `policy_engine show`,
`switchboard_v2 --help`, `host_resolver` (state read), `swarm_worker --help`,
`research_worker --help`, plus the `organ_map` engine itself.

---

## 5. FINDINGS

### 5.1 The verkle chain is not a quiescent surface — and it produced two false accusations
A background orchestrator appends to `memory/biography/verkle_chain.jsonl` and rewrites
`verkle_tip.json` on an irregular cadence (knots observed 05:25:42Z, 05:30:09Z, 05:48:50Z;
**7856 rows** at audit time). Twice during this sweep the write-detector flagged
`organ_map` as having touched the chain. **Both were false positives.** Proof:

- 45 s **idle control** with no command of mine running → `NO CHANGE`
- `prove_latest()` in isolation → `NO CHANGE`
- `mag.organ_map status` repeated **twice** → `NO CHANGE` both times, chain rows steady at 7856

**`organ_map status` is genuinely read-only**, despite its in-process verkle proof.
*Audit consequence: any write-detection over this repo needs an idle control, or it will
accuse the wrong organ.* I never called `rib_bus.publish()`, `verkle_lance`, or any
knot-folding path.

### 5.2 Correction to the task brief: it is **13** `receipt_stale`, not 18
`memory/runs/elder/audit.json` holds 20 gaps distributed as:
`receipt_stale` **13** · `receipt_not_successful` **4** · `receipt_missing` **2** ·
`proof_failed` **2** (water_computer, plus fleet_structure's third code).
19 of 20 carry at least one `receipt_*` code — "18 of 20" appears to count `receipt_*`
codes rather than `receipt_stale`. **This lane covered all 20 gaps regardless.**

### 5.3 Four organs declare state surfaces that are stale snapshots, not live state
`atlas.json` (26 days) · `self_audit report.jsonl` (28 days) · `main_channel`
cursor/WARM_PACK/last_receipt (26 days) · `harness last_run` = **empty string** despite
126 KB of events from 2026-09-03. The organs work; their state surfaces have not been
refreshed. `harness last_run` being blank is the sharpest: the queue's own liveness marker
was never written.

### 5.4 Three "read-only" instruments have writing CLIs
Docstrings say read-only; the shipped entry point writes.

| Instrument | Docstring claim | What the CLI actually does |
|---|---|---|
| `live_ops_readiness` | "Read-only live-operations readiness snapshot" | `main()` calls `write_snapshot()` → overwrites `memory/runs/live_ops/readiness.json` |
| `host_resolver` | CLI "for testing the resolver" | `resolve_host()` → `_log_resolution()` **appends** to `mappings.jsonl` on every call |
| `water_computer` | registered `proof: water_glass` (an organ-map proof) | writes a 9.4 KB campaign file + overwrites `operator.json` per call |

In all three cases the safe mode exists but is only reachable by **importing the function**,
not by running the module. That is worth a law: *a read-only claim must name the function,
because the CLI is not obliged to honour it.*

---

## 6. Side effects this lane caused (disclosed, not cleaned up)

1. **`memory/runs/self_audit/report.jsonl`** — appended by `self_audit run --tier fast`
   (2 probes, 2 passed, 0 failed). This **advanced `self_audit` from `receipt_stale` to
   `LIVE`**. Consequence of the audit itself, and the only live-count change observed.
2. **`memory/working/game_campaigns/gc-*.json`** — 9.4 KB per invocation, by
   `water_computer`'s own proof.
3. **`memory/working/game_characters/operator.json`** — overwritten with the demo
   character, by `water_computer`'s own proof.

No knot was folded, no message was sent, nothing was deployed, no secret was printed, and
docker was never touched. `git status` is byte-identical before and after the sweep (1850
entries both times; the new game-campaign files are gitignored).

---

## 7. Verdict

The fleet's own map was right to be suspicious, and wrong about where. **The 13 stale
receipts were not concealing broken organs — they were concealing organs nobody had
invoked.** Nine of them run clean on first contact; the other four have no read-only door
at all, and one of those four (`swarm_cycle`) hides a verkle-knot fold behind a flag
labelled `--dry`. The single real defect is `water_computer`, whose scripted demo cannot
win its own game — and which, in trying, litters `memory/working/` and overwrites a shared
character file on every organ-map call.

`unproven` is now `proven` for 16 organs, `broken` for 1, and honestly `unrunnable` for 4.

**Law:** *an organ is proven by an executed bounded step, not by a declared callable; a
receipt is evidence of a run, never permission to write.*
