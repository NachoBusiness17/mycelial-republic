# SELF-STEAL: THE SHAPE TRAIN (2026-09-03)
*Operator's manual relay (deepseek → claude → gpt → grok → z.ai → meta → gemini → file),
compiled into code. Steal law: the practice already exists; the runner is its reinterpretation.*

## THE SEVEN SHAPES — mined verbatim from the operator's advisor chats (Desktop/New folder)

| # | Shape | Source corpus | Moves |
|---|---|---|---|
| S1 | FIRST-PASS RESEARCHER | 2.txt, bubbles.txt (deepseek opening move) | parallel search, read pages, structured brief + bibliography + "questions for expert review" |
| S2 | ATTACKER | compuiter.txt (claude/gpt hop) | "Where I agree / Where I disagree / the sharper version", receipt-grade fact-checks (the LOI-vs-grant catch) |
| S3 | SOCRATIC GAP ANALYST | example-salon.txt v6→v7 | restate → "what is assumed without justification?" → rebuild v(n+1) → falsifier |
| S4 | COHORT ROUND | example-salon.txt next-action block | each seat: one forbidden pattern, one paid-rent claim, one extension, one disanalogy |
| S5 | SEAT-0 ELENCHUS | 2.txt Socratic salon | role-lane questions; answers yes/no/partly/wrong-question; Question Ledger genealogy |
| S6 | PASS-OFF SYNTHESIZER | bubbles.txt ("dig deeply… pass off to another llm") | full synthesis, well sourced, easily claim-checkable, journal-level — THE FOLD PROMPT, already written |
| S7 | EXPERT-REVIEW BRIEF | bubbles.txt deep-research brief | per-field bibliography → domain-expert questions → synthesis bridge |

Stage order (the relay's implicit grammar): S1 research → S2 attack → S3/S4 iterate → S5 interrogate → S6 file.

## ESTATE PRIMITIVES (verified in place 2026-09-03)

| Primitive | Path | Role in the train |
|---|---|---|
| cage fan-out | mag/salon_openclaw.py `_docker_openclaw` | per-model sessions, one docker exec each |
| universal dispatch | mag/seat_dispatch.py | task/route/status, OUTBOX finalize |
| gate v2 | watch/overnight_churn.py `is_boilerplate` + 150-char floor | substance gate |
| MAG CHORD v4 | watch/MAG_CHORD_V4_ADOPTED_20260903.md | blind divergence, source-status, promotion gate; collision ledger was queued — the runner is its first customer |
| Doctrine v2 salon format | memory/runs/salons/one_surface_20260902.md | QUESTION / PRIOR / ARMS / BLIND POST / INBOX / VERDICT |
| intake register | memory/ghost/intake/register.jsonl | {ts, status, kind, url, note, harvest} |
| economist doctrine | watch/ECONOMIST_DOCTRINE_20260902.md | lane table, zai-pro judge-only, burn-guard |
| swarm queue | mag/swarm_worker.py enqueue_task | sw-* task rows (economist consult rides here) |
| surfaces | dashboard/static/night/, ractor.html, watch/room.jsonl | artifact lands where the operator reads |

## EXTERNAL STEALS (folded in)

- **STORM** (stanford-oval/storm): personas ASK QUESTIONS before writing (~25% better-organized reports) → the BRIEF stage gets a question-ask step per shape.
- **Mixture-of-Agents** (togethercomputer/moa): layered proposers → aggregator beat GPT-4-Omni-class with open models → the FOLD is a two-layer read.
- **NeurIPS 2024 multi-LLM debate** + homogenization studies: same-model personas share failure modes → shapes = output diversity (default); engines = failure diversity (escalation "relay" tier only).
- **OpenClaw Browser Relay + awesome-openclaw-skills**: the tab train (operator's free web surfaces) = config flip + community skill, not custom engineering. Phase 2, operator GO gated, human-pace caps.

## CLAUDE CACHE CRAFT — consult receipt 2026-09-03 (claude-sonnet-5, 13.5K chars)

Standing consult prefix: the MAG architecture + seven-shape block (byte-stable, reused every future consult).

Laws adopted (full text in the consult transcript, watch/salon_receipts/):
1. Pad shared prefixes ≥1100 tokens; smoke-test `cache_creation_input_tokens > 0` on every first call.
2. Breakpoints: stable-to-volatile left→right; system/tools | brief | ledger; tail dead last. Tail before a breakpoint = 7 cache entries instead of 1.
3. Break-even: N_min = (w−r)/(1−r) ≈ 2 uses in-TTL; 7-shape fan-out = 1 write + 6 reads ≈ 74% prefix savings. **No keep-warm pings** for bursty salons — let it expire, eat one write.
4. Silent killers ranked: trailing whitespace, timestamps above the breakpoint, JSON key-order drift, unpinned model aliases, tool-schema regeneration, NFC/NFD unicode, mid-deploy breakpoint moves. Store prefixes as checksummed committed files; diff bytes sent, not source.
5. Fold loop: breakpoint at last round's ledger end, append-only ledger, corrections are new entries never edits — O(n²)→O(n), ~86% off at 7 rounds. Append-only and cache-friendly: same requirement, two hats.
6. Per-lane tagging: cache economics proven on Anthropic are Unproven on GLM/DeepSeek/ollama until measured.

## SCARS (the receipts that taught)

- Consult #1: 965-token prefix → `cache_creation: 0` (under the 1024 floor, silently). Consult #2: 2400 max_tokens → all thinking, zero visible text. Fixes: pad the prefix, disable/budget thinking, raise the ceiling.
- Board runaway (2.24GB) lesson carried: the runner appends bounded rows per run and documents the lockfile debt.
- Config-edit ≠ applied: the cage only sees the salon SKILL.md after a compose restart.

Decision: window — continue as salon-runner spine (trajectory lineage, never a sibling); extract 6 cache laws into docs/ref (ZERO_BACKREF_TRIAGE_20260905)
