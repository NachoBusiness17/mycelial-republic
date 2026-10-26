# WAVE2 LANE 3 — RIB COMPILER + SCHEDULED SURFACES

Audit 2026-09-26. Lane 3. Read-only. Nothing repaired, nothing published, no rib written
into the repo. Verkle chain untouched. Docker read-only census only.

---

## VERDICT (four answers up front)

1. **The compiler works.** It is not broken. Run read-only against the live tape it compiles
   **2 ribs today, rejecting 28** — the "0 ribs" figure in the skill and in
   `memory/runs/trajectory_rib/compiled.jsonl.meta.json` is a **24-day-stale receipt** from
   2026-09-02, written before the tape's last two bounded rows existed.
2. **The 28 rejections are correct behavior, not a bug.** They are OpenClaw compaction rows
   (`tokensBefore`/`tokensAfter`/`compactedCount`) that carry no `metadata` block at all. The
   gate is byte/line/hash verification; legacy rows cannot pass it and are not supposed to.
   `--include-legacy` exists precisely to inventory them as explicitly unbounded.
3. **The `not_run` gate cannot block anything — it is a hard-coded string literal.**
   `mag/trajectory_rib.py:169` reads `"metricGate": "not_run",` inside a dict literal. It is
   not computed, not read from state, not compared to a threshold. `grep -rn metricGate`
   over `mag/`, `main.py`, `docs/` returns exactly one hit: that line. It is a label
   pretending to be a gate.
4. **Nothing calls it.** It is reachable only as a hand-typed CLI verb
   (`main.py trajectory-rib`). No scheduled task, no script in `scripts/`, no PowerShell
   registrar, no hook, no orchestrator lane. It is a compiler with exactly one caller and
   that caller is a human at a keyboard.

---

## 1. WHAT THE COMPILER DOES

`mag/trajectory_rib.py` (190 lines, SCHEMA `trajectory_rib.v1`) is a trajectory-tape →
portable-rib projection, v0 pass from `docs/ref/TRAJECTORY_RIB_COMPILER_SPEC.md`.

**Input:** a JSONL tape, default `watch/openclaw_traj.jsonl`. One JSON object per line, each
an OpenClaw session-compaction record.

**The gate** (`_valid_bounds`, line 52) accepts a row only if ALL of:

| condition | why |
| --- | --- |
| `metadata.schema == "trajectory_span.v1"` | envelope identity |
| `metadata.lineRange == [line_no, line_no]` | the row must be exactly one physical line |
| `metadata.byteRange == [start_byte, end_byte]` | measured against the real file offset |
| `metadata.bodySha256` is 64 hex chars **and equals `_body_hash(row)`** | the row hashes its own body |

That last clause is the real teeth: a row cannot claim a span it does not occupy. The
`openclaw` writer (`deploy/openclaw/hooks/mag-file/handler.js`) computes the byte range
iteratively after inserting a placeholder, because writing the number changes the serialized
length — the same dance `tests/test_trajectory_rib.py` reproduces in `_bounded_row()`.

**Output:** `memory/runs/trajectory_rib/compiled.jsonl` + `.meta.json`. Secrets redacted by
three regexes (bearer, `key: value`, and `sk_/ghp_/gho_/hf_/gsk_` prefixes). Status is
demoted `verified → staged` when there are no acceptance commands. Source tape is never
edited; no verkle knot is folded; `publish_rib()` is never called.

**"Rib" in this system's vocabulary** is a *portable instruction*: an invariant plus a
source, a rank, and a timestamp, filed under a domain (`mag/rib_bus.py:47`,
`SCHEMA = "rib_bus.v1"`). 51 domain files, **818 frozen ribs** on disk. So the compiler's
job is to *mint new ribs from what the fleet actually did* rather than from what a human
decided to write down. That intent is explicit in the spec: `RIB_TRAJECTORY_20260827` is
listed as a "hand-compiled prototype" and the library step is "rib buffer on FILE, failures
→ standing refusals."

---

## 2. THE 28 REJECTED ROWS — VERDICT: CORRECT GATE, NOT A BUG

**Live tape today: 30 lines, 8,337 bytes, last modified 2026-09-03 13:06:12.**

| | |
| --- | --- |
| rows with no `metadata` (legacy compaction rows) | 16 |
| rows with `schema: trajectory_span.v1` | 14 |
| **rows that pass `_valid_bounds` right now** | **2** |
| rejected as unbounded | 28 |

The 28 are all of the form
`{"ts":…,"session":…,"tokensBefore":…,"tokensAfter":…,"compactedCount":…}` — token
counters. There is no `text`, no `summary`, no `pathsTouched`, no acceptance command. Even
`--include-legacy` would produce ribs with `anchors: []`, `text_len: 0`, and
`acceptance.status: "unproven"`. **The gate is right to refuse them.** A rib with no anchors
and no acceptance command is not a portable instruction; it is a line of telemetry wearing a
rib's clothes.

**The stale-receipt finding.** The receipt on disk says `compiled: 0, rejected_unbounded: 28,
sourceLines: 28`, ts `2026-09-02T08:22:45Z`, `sourceSha256: 40fffe33…`. The live tape
hashes `ccde6556…` with 30 lines. **The meta describes a tape that no longer exists.**
The 2 passing rows were appended 2026-09-02T18:27Z and 2026-09-03T17:06Z — *after* the
compiler last ran. The compiler has not been invoked since. `trajectory_rib` reads like a
dead organ purely because its receipt predates its own input.

**Why the tape stopped growing.** The bounded-row writer is
`deploy/openclaw/hooks/mag-file/handler.js`, `writer:` field in
`watch/openclaw_traj.jsonl.bounds.meta.json`. Its 8787 dashboard is dead
(`curl 127.0.0.1:8787` → exit 7, connection refused) and OpenClaw was retired 09-09. So
**the input stream is severed**: the tape can never grow again, and the compiler can never
receive a third bounded row. Even if the metric gate were real, there is nothing left to
gate.

---

## 3. THE 51 FROZEN RIBS — HAND-WRITTEN, AND THE COMPILER IS THE INTENDED FUTURE

All 818 frozen ribs are human/semi-automatic prose invariants. Source histogram:

| count | source |
| --- | --- |
| 585 | `fold_k8s_to_k3s (auto, 2026-08-12)` |
| 127 | `copilot-assistant` |
| 18 | `operator-bus` |
| 7 | `frontier-steal` |
| 7 | `harvest-fold` |
| 5 | `evo-seed` |
| 4 | `ghost-desktop` |
| … | (remainder singletons) |

`grep -l trajectory_rib memory/rib_bus/*.json` → **zero files.** No compiled rib has ever
entered the bus. So: not redundant-with-a-human-process *yet* — the human process is what
filled 818 ribs, and the compiler is the spec'd replacement for it (spec build-order step 1:
"compile pass prototype over ghost tapes → rib candidates"). **The compiler is the intended
future path, gated on operator GO, and the GO was never spent.** The receipt that does exist
is a *salon* receipt (`watch/salon_receipts/trajectory_rib_20260905.json`, 7/7 lanes
`gate: passed`) — that measured multi-model generation of a trajectory card, not the
compiler.

---

## 4. DID I RUN IT? YES — TO A TEMP PATH, NOT THE REPO

`compile_tape` has **no `--check` / `--dry` / `--status` mode.** `main()` takes only
`--tape`, `--output`, `--include-legacy`, and `compile_tape()` unconditionally does
`destination.parent.mkdir()` + `temp.write_text()` + `temp.replace()` + `report_path.write_text()`.
**There is no read-only path through this tool.** Default output is the repo path.

So I did not run it at defaults. I ran it with `--output` pointed at the Hermes scratch dir:

```
$ ./.venv/Scripts/python.exe -m mag.trajectory_rib \
    --tape watch/openclaw_traj.jsonl \
    --output $TMPDIR/tr_test/compiled.jsonl
{
  "ok": true, "schema": "trajectory_rib.v1",
  "ts": "2026-09-27T02:00:57.742865Z",
  "sourceSha256": "sha256:ccde65560e46a9f8733c283391682adce1719f7782112528f9d3e3871aa8bdf2",
  "sourceLines": 30,
  "compiled": 2,
  "rejected_unbounded": 28,
  "rejected_malformed": 0,
  "includeLegacy": false,
  "metricGate": "not_run",
  "verification": "staged; acceptance commands required",
  "output": "…\\hermes\\cache\\scratch\\tr_test\\compiled.jsonl"
}
```

Repo state after the run, byte-identical and mtime-unchanged:

```
-rw-r--r--  0  2026-09-02 04:22:45.571612500  compiled.jsonl
-rw-r--r-- 627 2026-09-02 04:22:45.573612700  compiled.jsonl.meta.json
```

**Why I declined the repo path:** running at defaults would have overwritten the 24-day-old
receipt that this very audit cites as evidence, replacing `compiled: 0` with `compiled: 2`
and destroying the only record that the compiler had never been re-invoked. On a
read-only lane that is a bad trade. The 2-rib result is reproducible at any time.

**And note what the 2 ribs actually are:**

| spanId | session | bounded | anchors | acceptance | text_len |
| --- | --- | --- | --- | --- | --- |
| `81981de2-5f0c-4612-b4e2-639badc7d963` | `agent:main:main` | true | **0** | unproven | **0** |
| `7f6d000e-6398-4457-9e20-ee8dd9bc3805` | `agent:main:explicit:seat-g3` | true | **0** | unproven | **0** |

**Two valid, hash-verified, completely empty ribs.** The two rows that pass the gate are
themselves compaction counters that happen to carry a valid envelope — they have no `text`
field, so `_anchors()` returns `[]` and the projected rib is a skeleton. The gate verifies
*provenance*; it never checked *content*. A rib with zero anchors compiles clean.

---

## 5. SOCRATIC: CAN THE `not_run` GATE BLOCK?

**It cannot block. It was never given the chance — it was never built.**

```
$ grep -n "metricGate\|not_run" mag/trajectory_rib.py
169:        "metricGate": "not_run",
```

One line, in a dict literal, inside a function that has no gate logic anywhere. There is no
`if`, no comparison, no import of a metric. The spec (§4, steal #4) defines the intended
gate precisely: *"DSPy `compile(teacher, student, metric)` … only verifier-passing traces
compile; a candidate rib must RAISE cheap-model success on held-out rollouts or it is not a
rib. Mag's own accept commands are the oracle. The steering suite IS this oracle, already
built."*

**The oracle does not exist.** `mag/steering_suite.py` — absent. `tests/test_steering_suite.py`
— absent. A repo-wide name search turns up only `.agents/skills/retrocausal-steering/SKILL.md`
and a config card `configs/workflow_gate_scenarios/G3_steering.card.json`, neither of which
is a pass/fail metric on a compiled rib. So the spec's own "already built" claim is stale:
the compiler shipped, the oracle didn't, and the field was hard-coded to the honest-sounding
`not_run` rather than `missing`.

**The same class of bug is already documented in the house skill:** *"Never read 'the guard
exists' as 'the guard saw it' — check the window the guard actually watches."* This is the
inverse and worse: a guard that was never written, wearing the JSON key of one that was.
`main.py:2776` returns `0 if res.get("ok")` — and `res` hard-sets `"ok": True` at line 159.
**The exit code is a constant too.** A green `main.py trajectory-rib` is not evidence of
anything.

**What it would take to make the gate real, in order of cost:**

1. A metric function with a signature and a threshold — `metric(rib, rollout) -> bool`.
2. A held-out task set with a cheap student (spec names `deepseek-chat` / `qwen3:8b`) and a
   pre-registered n and floor. Epoch-1 lesson: pre-register before the first run.
3. Wire the acceptance commands in as the oracle — `acceptance.commands` already exists on
   every compiled row and is currently always `unproven` because the tape carries none.
4. Replace line 169 with a real computation, and make `ok` depend on it.
5. A caller.

**Cost/benefit, honestly:** step 5 is the cheapest and the only one that makes the rest
observable. Steps 1-4 are a research program that needs an operator GO and a live input
stream. **With the input severed (OpenClaw dead), a real metric gate would correctly reject
every future run for having no candidates — which is a true statement, not a failure.**

---

## 6. SCHEDULED SURFACES — FULL CENSUS

`schtasks /query /fo CSV /v`, parsed to 242 real tasks (the raw `/v` output contains header
repeats that inflate naive counts to 338).

**23 fleet-owned tasks** (`\Mag*` / `\Estate*`). Everything else is Microsoft/Google.

### Firing clean — 14

`Estate Cooker` (hourly) · `Estate FullScan` · `Estate Gopher` · `Estate KeyAudit` ·
`Estate LaneSupervisor` (15 min) · `Estate Librarian` · `Estate Spine Index` ·
`Estate StealthSweep` · `mag-docker-watchdog` (5 min) · `MagCensusPatrolDaily` ·
`MagEndpointNewsDaily` · `MagFtsIndexDaily` · `MagMimoWatchHourly` · `MagVisionNightly`

All `Last Result: 0`, all with realistic last-run timestamps within the last 24h.

### Failing — 2, both exit 1, both diagnosed

**`Estate Ratchet`** — `logs/ratchet_daily.log`, `[2026-09-26 09:45:03] END seal=1 freshness=0 ratchet=1`.
Two independent gate failures, both **by design**:

- `CONFIG-SEAL: FAIL — re-seal by NAME: python tools/config_seal.py update --by WHO-NOT-WHY`
  and `UNSEALED events_malformed_baseline.json`. A config file changed and the seal was not
  re-signed with a name and a reason.
- `RATCHET check: FAIL — run 'baseline-update' ONLY after a human/agent accepts the debt by
  naming it.` New violations appeared since the accepted baseline.

This is a gate **working exactly as designed**: it refuses to auto-re-seal itself, because
the operator's name on the seal is the whole point. Do not "fix" it unattended.

**`MagImproveDaily`** — `logs/improve_daily.log`, `[2026-09-26 08:00:00] END exit=1`.
The work *ran and wrote its artifacts* (`day: 2026-09-26`, `latest_report`,
`field_brief`, `candidates` all emitted) but the pass exited nonzero. From
`memory/runs/improve_loop_trail.jsonl` the tail row shows
`"trust_blocked": true, "trust_reason": "desk trust tier 0 — slow→fast fail; pass desk
baseline before unmanned fill", "trust_probe": "python scripts/desk_baseline_probe.py"`.
**Self-declared abstention, surfaced as a failure code.** Read it as "the loop declined to
act", not "the loop broke."

### Never run — 5 (`Last Result 267011` = SCHED_S_TASK_HAS_NOT_RUN, `Last Run 11/30/1999`)

`\MagArmC200` (next 09-27 01:00) · `\MagCorpusRescanDaily` (09-27 03:30) ·
`\MagQCaptionVerifyDaily` (09-27 07:30) · `\MagMimoWatchClose` (09-28 17:25) ·
`\MagSecretScanWeekly` (09-28 06:40)

All `Status: Ready`, all `Enabled`, all scheduled. **All five are pending their first
scheduled fire.** `MagArmC200` points into `memory/runs/interference_replication_20260925/run_armC.py`
— a 09-25 experiment registered the same day. `MagQCaptionVerifyDaily` and
`MagSecretScanWeekly` were registered after their nominal trigger hour today, so 09-27 is
genuinely their first. Not yet evidence of breakage — but they are also not evidence of
working, and nobody has watched one fire.

### Disabled — 2 (both stale)

`\MagLabKit8765` (`res=-1`) and `\MagPrivateOffice8765` (`res=-1073741510`), both last run
**2026-08-01 09:31/09:32** — 56 days ago. Ports 8765/8766 are now served by `mag-mcp` and
`mag-sovereign` per `docker ps`. These are dead registrations of a retired arrangement.
Note the standing law: *"Fleet services live in Docker, loopback-only — never scheduled
tasks."* These two predate the rebuild and contradict the law by existing at all.

### Not fleet, but same host

`\OpenClaw Gateway` (last run 09-25, `res=0`, no next run) and `\StartCN` / `\StartDVR`
(both `res=1`, last run 09-25 at logon) — a retired stack's leftovers.
`\cua-driver-serve` and `\AMDRyzenMasterSDKTask` are Hermes/AMD, not Mag.

**None of the 23 fleet tasks invokes `main.py`, `trajectory-rib`, or any `mag/*.py` module
that would call the compiler.** Confirmed by `grep -rn "trajectory-rib|trajectory_rib"`
across `scripts/ tools/ watch/*.ps1 watch/*.vbs hooks/ .github/` → **zero hits.**

---

## FINDINGS

| # | finding | severity |
| --- | --- | --- |
| F1 | `metricGate: "not_run"` is a string literal at `mag/trajectory_rib.py:169`; the gate cannot fail because it does not exist. The spec's oracle (`steering_suite`) is absent from the repo. | **high** |
| F2 | `"ok": True` is likewise hard-set (line 159) and `main()` returns `0` from it — the exit code is a constant, so a green run carries zero information. | **high** |
| F3 | The 0-rib claim in the warm-boot skill and in `compiled.jsonl.meta.json` is a stale 24-day-old receipt. Live compile = **2 ribs**, 28 rejected. | **high** (misleads every future seat) |
| F4 | No caller. CLI verb only — no task, script, hook, or orchestrator lane. | **high** |
| F5 | The input stream is severed: the bounded-row writer lives in the retired OpenClaw deploy and its 8787 dashboard is dead. The tape cannot grow again. | **high** |
| F6 | The 2 ribs that compile are empty — `anchors: 0`, `text_len: 0`, `acceptance: unproven`. Provenance is verified; content is never checked. | medium |
| F7 | `compile_tape` has **no read-only mode** — it always writes. Any "just check it" invocation mutates the receipt. | medium |
| F8 | 5 of 23 fleet tasks have never fired (`267011`). 2 fail by design (Ratchet's config-seal, Improve's declared trust abstention). 2 disabled registrations are 56-day-stale and contradict the "no scheduled tasks" law. | medium |
| F9 | `watch/openclaw_traj.jsonl.bounds.meta.json` also reports the 28-line `40fffe33` tape — same staleness class as F3, one layer down. | low |

---

## WHAT I DID NOT VERIFY

- Whether `Estate Ratchet`'s config-seal failure corresponds to a real operator-visible
  change or a spurious edit. I read the failure text and the log; I did not diff
  `tools/config_seal.py`'s manifest against `state/CURRENT.md`.
- Whether the 5 never-run tasks will actually succeed at their first fire. None has fired.
- Any behavior requiring running the compiler at its repo-default path. I declined, and
  gave the reason above.
- `MagArmC200`'s script contents. The task has never run; I did not execute it.
- Chain state, orphan counts, missing knots. Out of lane; untouched.

## RECOMMENDED NEXT ACTIONS (not taken)

1. **Re-run the compiler at defaults once**, deliberately, to replace the stale receipt with
   the true 2-rib/28-rejected result. One command, one write, and F3 stops misleading seats.
2. **Decide the compiler's fate** before any more audit time is spent on it: either
   re-point `--tape` at a live stream (or `memory/trajectory/steps.jsonl`, which the
   `trajectory_step` wrapper does still write) or retire it. Right now it compiles a frozen
   30-line file nobody appends to.
3. **If kept:** give it a `--dry` flag and a real `metricGate` computation, or at minimum
   change line 169 to `"metricGate": "absent"` so the receipt stops implying a gate ran.
4. **Sweep the 2 disabled tasks** (`MagLabKit8765`, `MagPrivateOffice8765`) — 56 days stale
   and law-contradicting. Deletion is a change; naming it is a report.

---

## DELIVERABLE

`C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/audit_20260926/WAVE2_LANE3_RIB_COMPILER.md`
`C:/Users/foste/Documents/projects/local_sovereign_agent/memory/audit_20260926/w2l3_rib.json`

**Writes made:** these two files, plus scratch under
`$TMPDIR/tr_test/` and `$TMPDIR/task_census.py`. **The repo's
`memory/runs/trajectory_rib/compiled.jsonl{,.meta.json}` were read but not modified** —
verified byte-size and mtime unchanged after the temp-path compile.
No verkle knot folded, no rib published, no task created/disabled/deleted, no Docker action.
