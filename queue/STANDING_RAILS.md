# STANDING RAILS - the drop-in surface (Lessig law, 2026-10-03)

Operator order: "Lessig this, this is everywhere. I always wanted standing
workflows we can just drop shit into and make it work dogfooding our shit
through our systems instead of having to tell you every time. the literal
oroboros."

## THE LAW

1. Default to the rails. A bespoke model-call path requires a written reason
   in its docstring. The front door is `mag.route_chat` (lane + goal; dormant
   gate; endpoint fence; per-lane call laws; usage banked).
   Depth clause (added 2026-10-04, parked-decision D3; the file carried no
   depth law before this line, ractor triple-verified): depth is a two-value
   enum {mechanical, design}, anything else refused (mag/route_chat.py
   route_chat ValueError). depth=mechanical sends thinking:{type:disabled}
   on the wire for every lane, sent by the carrier; omission is not the off
   state (d4 probe 2026-10-04,
   watch/inbox/go_wave_20261004/d4_thinking_probe.md). depth=design is the
   only enabled path, capability-attested per lane, budgets 32K+. Usage
   rows bank depth + thinking_sent + reasoning_tokens so the posture is
   audited from the response, not assumed from the request (mag/route_chat.py
   wire_thinking + the route_chat bank row).
2. Material must render. Any batch prompt carries {text} (or equivalent) and
   the seat verifies the render - outputs without their material are VOID
   (the hollow-batch law, caught 2026-10-03: a cheap seat fabricates when
   evidence is missing, and the run still prints ok=True).
3. Interrupts never cancel. Wide waves run background-executed; an operator
   interrupt steers, it does not kill (standing background rule, 2026-10-03).
4. Every session banks. Play, audits, folds, replays - if it ran, it lands a
   receipt (gwap payload, DONE row, usage ledger row, or register row).

## THE DROP-IN TABLE (what you drop, where it lands, what comes out)

| you have | drop it in | comes out |
|---|---|---|
| any one model call | mag.route_chat(lane=, goal=) | text, usage banked |
| N mechanical asks (fold/extract/triage) | tools/ds_workhorse batch | results jsonl, ~$0.0001/ask - enforces law 2 below (render guard, ok_api + ok_material; hollow batches refuse) |
| paid judgment asks (design, deep digs) | stage ask dirs under memory/plans/hermes_burn_*/ | the descent driver eats them; outputs in watch/inbox/hermes_burn/ |
| grok-ladder asks | tools/grok_burn.py | watch/inbox/xai_grok47/ |
| N >= 30 independent byte-checks | the fifty-wide wave protocol (Task agents, one-line contracts) | tally + receipt in watch/inbox/ |
| a design ask worth measuring | the frontier delta replay (ds + flash arms) | a Delta Register row |
| a play hour | tools/tavern.py + tools/dungeon.py (hourly cron) | DONE rows + gwap payloads |
| any finished session/run | tools/arena_gwap.py <run_dir> | chain-verified capability row -> GPS |
| real estate claims to verify | dungeon REAL_SCROLLS table | in-game audits with byte results |
| gap-register rows | PARTYCHAT threads (when the wire plan lands) | competing builds -> gate -> landed fix |

## THE OROBOROS CLAUSE

The rails compose: gap rows become threads, threads become competing builds,
builds are judged by the gate, landed fixes anchor the chain, sessions bank
capability rows, capability rows route the next ask's dollars. Dropping work
into any rail feeds the others. The operator drops; the estate routes.

## REGISTERED DEBTS

- tavern/dungeon/hermes_burn/grok_burn still self-call; each migrates to
  route_chat or documents its reason (fences differ per endpoint) - one per
  sitting, no batch rewrite.
- The Delta Register judge pass landed 39/39 - memory/runs/ds_batches/
  delta_judge_results.jsonl is the artifact of record (closed 2026-10-03T13:04Z;
  tally frontier 8 - flash 5, ds 0/26 from a max_tokens-capped arm, re-fired
  uncapped 2026-10-04 as frontier_delta_results_v3.jsonl, new ds tally 3/28;
  receipt watch/inbox/go_wave_20261004/ds_workhorse.md). Re-fire debt closed.
- tools/hermes_burn.py thinking rail: its computed plans dropped the
  reasoning rails one hop before the wire (plan_call computed
  thinking_control but the request carried only {model, messages,
  max_tokens}), the $0.464 double-burn carrier
  (memory/runs/hermes_burn/usage.jsonl:1151-1152, glm-5.3-prime 15998 +
  9826 reasoning tokens, $0.4639940 total, verified 2026-10-04). The
  merge-the-plan wire fix landed 2026-10-04 (tools/hermes_burn.py
  _build_body + the plan.extra_body pass into _call); the standing cure is
  migration to route_chat per the self-call debt above, one carrier, one
  depth law.

## OVERFLOW ROUTING LAW - operational (2026-10-07, operator order: deepseek/free lanes for overflow)

When account:zai-individual-coding-plan rate-limits (the starvation class:
6 concurrent workflows drew one plan's window; the external-steal ractor's
bank step starved 2h18m), overflow routes in this order:
1. PAUSE-RESUME JUGGLE: TaskStop the youngest run (lossless - resume keeps
   args and cache) to free the window for the starved run. Proven 10-07.
2. DEEPSEEK BATCH OVERFLOW: queue-shaped, batchable asks route through
   tools/ds_workhorse.py (thinking-off enforced, ok_api/ok_material split,
   instance-guarded). Proven live 10-07: the GROK ask-4 audit checklist
   drafted at $0.0007 (queue/ds_overflow/). Workflow SUBAGENTS cannot
   overflow (model is run-level on zai accounts) - batch-shaped work only.
3. FREE-LANE FLEET: sensing-class asks via the existing 30-min cadence.
4. HERMES: judgment-tier overflow via MagHermesBurn247 (funded meter).
Verification NEVER overflows: byte-checks stay local or on the funded tier.
