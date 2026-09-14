# HOLLOW MASS BODIES — did the null-theme knots hide real work? 2026-09-11

**Commission:** wave standing cycle slot 4. The Silence Dossier found 982 hollow leaves
(dominant_theme null) among 1,281 knots Aug 23-25. The pool decode claimed
`memory/agent_sessions/` (2,647 orc-t*.json, ~70MB) holds the FULL BODIES the chain
digests point at. This lane tested that claim: sample 30 hollow knots, pull session ids,
match against the pool, read what the bodies actually contain. Read-only except this file.

**Method:** all 1,281 Aug 23-25 knot leaves parsed; 982 hollows censused by session
family; a seeded random sample of 30 hollows matched against pool filenames AND pool
content; every orc-t hollow (17 leaves, 4 distinct sessions) matched and its transcript
read; pool-wide shape census (stub vs body) run over all 2,647 files; the surviving
runner code (`mag/memlang.py`, `mag/castle_foundation.py`, `mag/rib_os.py`) read to
identify the no-body families. Seeded (20260911) — reproducible.

---

## 1. The match rate

- Random sample of 30 hollows: **1/30 matched** the pool (3.3%).
- All orc-t hollows (17 leaves → 4 distinct sessions): **17/17 matched** (100%).
- The other 965 hollows: **0 bodies in the pool, and 0 anywhere in the repo.**
  (Content-grepped every pool file head for `memlang`/`castle-foundation`/`rib_os`/
  `work-loop`: zero hits; repo-wide find: only the runner code and knot leaves.)
- Control: all 39 themed (non-hollow) orc knots Aug 23-25 also match the pool — the
  knot↔pool linkage is real; the hollows fail to match because their sessions were
  never orc sessions.

## 2. Who the hollows actually were (982 leaves, exact census)

| Family | Leaves | Body? |
|---|---|---|
| memlang-* (9 opcodes: dispatch, compass, daemon, flex, dspy_sovereign, sovereign_handshake, sovereign_dashboard, api_gateway, signals) | 703 | none anywhere |
| castle-foundation-2026-08-2*T## hourly | 129 | none anywhere |
| rib_os | 75 | none anywhere |
| mag-agent-orc-t* | 17 (→ 4 sessions) | 4 stubs (see §3) |
| work-loop | 11 | none — backup index just repoints at the hollow leaf itself |
| proof | 10 | none |
| mag-agent-cli | 4 | cli.json plausible match, UNPROVEN |
| invariant:* / work:* / misc singles | ~34 | none |

## 3. The 10 case reads

The 4 matched orc bodies (all read in full — every one is a STUB):

1. **orc-t0e05c0cf60** (6 leaves, Aug 23 11:36) — ASKED: "[janitor] FKB signal
   '_:86902901b952' has 7 occurrences... find root cause, write diagnosis to
   memory/runs/ghost/autonomous_fixes/... $0." Ran on ollama/qwen2.5-coder:7b.
   Body = system prompt + ask only. Zero tool calls, zero assistant output.
2. **orc-tc829720ddb** (3 leaves, Aug 23 13:01) — same janitor shape, FKB
   `run_python:2e689948ccfa` x8, same diagnosis-writes, ollama. Stub again.
3. **orc-t2b1ecf8a72** (4 leaves, Aug 23 15:31) — ASKED: "run republic_os round to
   reinforce/prune graph", ollama, no model recorded. Stub.
4. **orc-t08ea29162c** (4 leaves, Aug 25 14:09-11) — deepseek_overmind loop-escalation:
   "SHADE NOVEL ORPHAN [percolator-novel]... fold it into an invariant or resolve the
   orphan. Use framework tips — do not repeat the failed tool pattern." Stub.

The 6 no-body families, identified from their surviving runner code:

5. **memlang-dispatch** (77) — mag/memlang.py: a binary trigger language; agents get a
   40-byte token (opcode + verkle anchor hash), decode it against shared state, execute.
   Each hollow leaf = one compile/decode/trigger round of a $0 deterministic loop.
6. **memlang compass/daemon/flex/dspy/handshake/dashboard/gateway/signals** (626) — the
   other 9 opcodes of the same language: probe, heartbeat, A/B flex tests, signal pushes.
   Machine-to-machine mem traffic; there was never dialogue to mine, hence null themes.
7. **castle-foundation hourly** (129) — mag/castle_foundation.py: "castles in the air +
   shadow work → deterministic foundations", one guarded beat per hour, folding zeitgeist
   into verkle-anchored invariants. The hourly T## timestamps ARE the beat cadence.
8. **rib_os** (75) — mag/rib_os.py: self-generating RIB OS, one guarded step per knot —
   generate a RIB from the invariant map, fold it, A/B verdict, measure growth. $0.
9. **work-loop** (11) — the Silence Dossier's 960-request marathon candidate. No body
   exists; the backup's by-session index for work-loop contains nothing but the same
   hollow leaf's own hash — the husk is the only record of itself.
10. **mag-agent-cli / proof / work:* singles** (~48) — cli.json is the only real BODY in
    reach (19 msgs, 8 assistant, 9 tool results, deepseek-v4-flash, a compass-steer
    session) but its session_id is "cli", so linking it to the 4 `mag-agent-cli` hollow
    knots is UNPROVEN. The rest: one-off test/proof pings with no archived trace.

## 4. The verdict

**The hollows were real work with unwritten bodies — and the pool is a dispatch log,
not a transcript archive. DISPUTED: the pool decode's "chain holds digests, pool holds
FULL BODIES."** Pool-wide census: 1,949 of 2,647 files (74%) are stubs — system+user
only, zero execution trace; 698 carry assistant/tool output, and none of them belong to
hollow sessions. Providers explain the machine character: ollama 1,907 (local
qwen2.5-coder:7b), deepseek 694, grok 16, deepseek_overmind 15.

So the marathon mass splits cleanly: (a) the memlang/castle_foundation/rib_os grind —
deterministic $0 loops whose OUTPUT was invariants and verkle anchors, not conversation;
the theme extractor found nulls because there was genuinely nothing conversational to
extract; (b) the janitor/escalation orc dispatches — real asks, minted session ids, and
then... nothing recorded. Whether those workers actually executed (the $0 FKB fix files,
the orphan folds) is checkable in `memory/runs/ghost/autonomous_fixes/` — that check is
the next lane; from the pool alone the asks are stored, the doings are not. The hollow
mass is therefore not evidence of idle machines: it is evidence of a record pipeline
that could commit a hash per session but captured neither dialogue nor deed.

**CYCLE GENETICS:** dossier(read)→sample(30,seeded)→match(1/30→17/17 orc-only)→bodies(4 stubs)→code-steal(memlang/castle/rib = the real doers)→verdict(null != empty: side-effect work, unwritten bodies; 74% of pool is stubs)→next(ghost/autonomous_fixes/ receipt check).
