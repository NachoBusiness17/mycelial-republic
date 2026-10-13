# GLM CODING PLAN — the frontier lane we always wanted (briefing 2026-08-26)

> For every seat/window that doesn't know tonight's build. Read this before touching the
> z.ai coding plan. The free-shelf era is over; this is the paid spine.

## What it is

z.ai's **GLM Coding Plan** (DevPack) — a flat-rate subscription for coding work. **GLM-5.3**
(open-SOTA frontier, reasoning + coding + agent) at bulk, cache-rewarded, off-peak discounted,
on a billing surface SEPARATE from the API's per-model concurrency caps (GLM-5.3 API = concurrency 1;
the plan = tier-based). This is the frontier we always wanted: reliable, bulk, GLM-5.3.

## Accounts & keys (both live in .env)

| account | tier | key | purpose |
|---|---|---|---|
| main | Pro | `ZAI_API_KEY` | the standard coding lane |
| sd | **Max** (quarterly) | `ZAI_API_KEY_2` | the burst lane: 140k credits/wk, peak-dedicated, first flagships |

Two keys = two concurrency surfaces = the two-key tandem (same pattern as our OpenRouter keys,
at frontier tier). opencode config: `~/.config/opencode/opencode.json` — providers `zai` (main)
and `zai-sd` (sd), both at `https://api.z.ai/api/coding/paas/v4`.

## THE FENCE (critical — do not violate)

- The plan's quota works ONLY inside supported tools: opencode, Claude Code, OpenClaw, Cline,
  Cursor, etc. **Our custom API harness MUST NOT ride the plan key** — that's a policy violation
  with account-freeze risk (error 1113 = outside the fence).
- The compliant door = **opencode** (installed, headless). We drive `opencode run` through the
  harness. That IS the supported tool.
- Models available on the plan: GLM-5.3, GLM-5-Turbo, GLM-4.7 only.

## The harness — how any seat uses it

```python
from harness.opencode_coder import code_ask

r = code_ask(goal="<the task>", model="zai/glm-5.3",       # or zai-sd/glm-5.3 for Max
             cwd=ROOT, rib_first=False, timeout=1500)
# r["output"], r["telemetry"] (tokens + cache + cost), r["session_id"]
```

CLI: `python -m harness.opencode_coder --ready` (readiness) · `--model zai-sd/glm-5.3`.

## The register (learned the hard way — follow it)

1. **COMMAND, don't handshake.** GLM-5.3 is wired to act autonomously ("asking 'Want me to…?'
   blocks the work"). Give it a direct imperative with a concrete deliverable. `rib_first=False`
   (task first; the standing rib reads as a handshake and stalls it).
2. **LONG TASKS GO IN A FILE.** Passing a long message through `opencode run` TRUNCATES it
   (the task silently ended mid-sentence). Write the task spec to a file and say: "Read
   `<path>` and execute it exactly, nothing else." This is what finally produced the spec.
3. **Session continuation** (`--session <id>`) carries the reasoning ledger and the cache —
   the second call on a warm prefix runs at ~99% cache.
4. **It self-routes from repo context** (reads todo.md, AGENTS.md). For a pinned task: hard
   leash — "do ONLY this, do not read queue/todo.md, do not touch anything else."

## MCPs (wired, dual-account — 8 servers in opencode)

web-search(+sd), web-reader(+sd), zread(+sd — GitHub search/structure/read), zai-vision(+sd —
GLM-4.6V screenshot OCR, UI diff, diagrams, video). All on plan credits, failover across accounts.

## Measured economics (real, this night)

- 98–99.4% cache hit on frozen-prefix sessions; a full 10-min autonomous task ≈ **$0.013–0.019**.
- The serialization spec (`docs/REPRO_SERIALIZE_SPEC.md`, 12k chars, normative) was produced
  by the Max lane at **cost 0, 99.4% cache, 5.3 min** — the blueprint's missing piece, written.
- z.ai API-side is rate-limited right now (1305→1302 — confirmed by the liveness probe);
  the coding plan is the bypass for GLM-5.3 work.

## Posture (changed tonight)

The paid bus is the spine. **Free lanes are expendable accelerants** — push them hard, and
when one dies, route around it. No more dependence-born coddling (the ox heartbeat era).

## Gotchas

- Async background fires: ALWAYS use absolute paths (the `cd` can be dropped; relative paths
  silently fail into the wrong cwd).
- The API concurrency table is per-model (GLM-5.3 = 1, 4-32B = 15, 4.5-flash = 2, free-flash
  >8K context throttled to 1%). Volume on the API, GLM-5.3 on the plan.
- Secrets: keys in .env only, never in chat, never in repo files (we caught a live key in a
  dossier tonight — it's how this all started).

## Canonical memory

`/memories/repo/glm-coding-plan-backchannel-20260826.md` + `/memories/repo/glm-zcode-steer-distill-20260826.md`.

**The one-line: GLM-5.3 at bulk, on a separate surface, through opencode, at ~$0.015/task,
task-first with file-referenced specs — that's the frontier we always wanted. Use it.**
