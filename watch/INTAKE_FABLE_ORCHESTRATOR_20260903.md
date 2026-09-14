# INTAKE — fable-orchestrator viral post

Date: 2026-09-03 | Evaluator: intake sub-agent (background spawn per Amendment 1)

## ITEM
https://x.com/painn_x/status/2095290696500498499 — "holy sh*t this is f**king dangerous. A Chinese guy figured out how to run fable 5.1 for FREE on gpt 5.6 luna subagents on every task. You'll never hit an agent usage limit. how you set it up (3 mins): 1. install the 'fable-orchestrator' repo 2. type /fable orchestrator [task] 3. done... Give this to your agent immediately." Author follow-up names the repo: github.com/codejunkie99/fable-orchestrator ("Fable 5.1 orchestrates. GPT-5.6 Luna and DeepSeek V4 Flash implement").

## RECEIPTS
Fetched: root post + thread via web_reader; repo README via WebFetch (GitHub page); web search for corroboration/pushback; second fetch pass for replies.

- Root post: 274.7K views, 57 replies, 238 reposts, 1.8K likes, 3.4K bookmarks. Replies are GATED ("Only some accounts can reply"). No community note. Visible replies are AMPLIFICATION, not verification: near-duplicate post by @Av1dlive (same text template), plus a Facebook copy-paste variant with "FR££" spelling — copy-paste template spreading across accounts.
- The repo is REAL and benign-shaped: tiny MIT-licensed Codex routing skill. Fable 5.1 plans/adjudicates; implementation delegates to OpenCode Go agents — GPT-5.6 Luna (implementation) and DeepSeek V4 Flash (loops/high-throughput). Bounded graph, evidence-collection discipline, dry-run installer, explicit "never put credentials in a packet", tests grep for credential-shaped strings. No proxy, no dashboard, no credential store. BUT: the "free" part is not the repo's — it consumes OpenCode Go agent lanes whose real limits/ToS the post never receipts.
- The headline claim is DISPUTED by vendor docs: Anthropic's own help center caps Fable models at 50% of weekly plan usage limits; trade press (The Rundown AI, 2026-07-10) covers the same orchestrator pattern as "use 60% less Fable tokens" — a REDUCTION, not the abolition of limits the post claims.
- Zero critical replies surfaced in two fetch passes; absence of pushback is a reply-gating artifact, not consensus.

## SCORE
F:3 P:2 C:4 W:2 N:1 = 12/25 — CALIBRATE band

## READ
This is our own doctrine, re-discovered by the mainstream and dressed as a leak. "Frontier model plans, free flash lanes implement" is already canon here — frontier thinks/flash digs, ask_router, the engine bay (free glm-4.7-flash A-lane + 32B B-lane), resident steered workers, seat_dispatch, the claude-zai plan door running 8 of 10 engine bays. The cache-landscape-scan verdict applies verbatim: pieces everywhere, composition ours. What the post adds is (a) market validation that orchestrator-split went mainstream (supports the operator's public-turn "mechanism public, moat = discipline" thesis), and (b) one genuinely portable micro-idea: the repo's credential-shape grep test as an install gate. The post's CTA — "install the repo, give this to your agent immediately" — is exactly the injection vector our repo-files-are-data law exists for; the README looks clean, but clean-looking is how injection ships. Viral mechanics note: reply-gating + copy-paste siblings + 3.4K bookmarks vs 1.8K likes = engagement-bait form factor with real latent demand underneath.

## TRI-STATE
- Repo exists, is a small MIT routing skill, no credential store — SUPPORTED (README fetched).
- "You'll never hit an agent usage limit" — DISPUTED (Anthropic caps Fable at 50% of weekly plan usage; orchestrator reduces usage ~60%, removes nothing).
- "Free GPT-5.6 Luna subagents, no limits" — UNPROVEN (depends on OpenCode Go lane limits/ToS; no receipt in post or repo).
- "3 mins, best thing you can do this week" — UNPROVEN (marketing register).
- Coordinated amplification / engagement-bait form — SUPPORTED (near-duplicate posts across accounts, gated replies, zero critical replies visible, no community note).
- Repo malice (credential harvesting) — UNPROVEN, leans clean by design evidence; unaudited third-party skill = never run pre-audit.

## VERDICT
CALIBRATE — do not wire the repo; we already run the pattern at $0 with receipts. Remember the validation, steal the micro-gate.

## ROUTE (no wire)
1. skills_guard: add the credential-shaped-string grep as an install/skill gate row (the one portable steal; free lane).
2. Public-turn hook, operator's hand only: the mainstream arriving at our routing doctrine is a receipt-backed reply opportunity for @NachoQuixotic ("we run this at $0 with signed receipts") — external posts flow through his hand, never ours.
3. Per intake amendment 1: driver should pull this card on cadence; suggested typed room row — `intake.card{slug:"fable_orchestrator",verdict:"CALIBRATE",score:12,route:"skills_guard.micro-steal+public-turn-hook"}`.
4. No engine, no lane, no queue action beyond the above.
