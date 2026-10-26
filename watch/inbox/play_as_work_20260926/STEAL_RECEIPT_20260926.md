# STEAL RECEIPT: play-as-work v4.0 brief (DeepSeek) + live citation verification

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 · **Class:** RECEIPT / research steal
**Source:** operator dropped DeepSeek share https://chat.deepseek.com/share/wq0vlxko6mufedlxkh, then pasted the full v4.0 brief in-session (two pastes, one truncation point, disclosed in the brief header)
**Full text (byte copy of the paste):** `watch/inbox/play_as_work_20260926/BRIEF_v4_full_20260926.md`

## What it is

Operator drove a 5-turn DeepSeek session from a Factorio-to-coding research ask to a formal mechanism-design brief: skill compilation as a dynamic game with endogenous action-space expansion, four metrics (Compilation Gain, Capability Expansion, Artifact Reuse, Negative Compilation), a conjunctive play condition, a four-arm experiment whose crucial comparison is Play vs Compiling Play, and the claim that the Challenge -> Retain/Revise/Forget phase (adversarial revalidation of compiled capability) is MAG's specific contribution. The brief is explicitly written for other LLMs to recreate and extend the research.

## Live verification ledger (this seat, 2026-09-26)

**VERIFIED by fetch/search:**
- Jain & Parkes 2013, "A game-theoretic analysis of the ESP game", ACM TEAC 1(1) 3:1-3:35. DOI 10.1145/2399187.2399190, free text at Harvard DASH. Real, citation accurate.
- factorioctl, github.com/MarkMcCaskey/factorioctl. Real, MIT, Rust, kubectl-style CLI plus MCP server over RCON, "designed for AI agents (like Claude) to play Factorio autonomously". Author warns it is a vibe-coded weekend build. Key design lesson confirmed verbatim: "Don't make your LLM do path finding... just give it A*." Also: speed beats decision quality across thousands of tool calls; persistent zone/memory files outside the game stop agents building nonsense.

**FALSIFIED (IDs point at unrelated papers):**
- Ref 5 (TrustChain-Review) cited as arXiv:2502.04223 -> that ID is "Eclair" (document OCR). Nothing to do with code review.
- Ref 8 (Opponent Shaping in LLM Agents) had been carried on arXiv:2509.06636 in the v3 thread -> that ID is integer-arithmetic training for spiking neural networks.

Pattern: the v3 thread's arXiv IDs are hallucinated at a high rate even where title/topic may be real. The v4 References section carries venue+page form (no IDs) for most entries, which is harder to falsify but also unverified.

**UNVERIFIED (lean real for the classics, unconfirmed for the rest):** Monderer & Shapley 1996 (classic, real), Hinman 1978 PSC 5(2), Chapman et al. AAMAS 2009, Hazzan & Dubinsky XP 2005, Rass & Pinzger GameSec 2023, Kang et al. AAAI 37(5) 2023, Garcia Segura ICLR 2026, Hennes et al. CSRO AAMAS 2026, Li et al. Nature Communications LegoNE, Naserameri arXiv:2607.27310 (suspect: 2607 numbering = Jul 2026, existence unconfirmed).

## Fleet crosswalk (the refraction)

1. **Jain & Parkes = "meters going up is not work", formalized.** Their result: under match-early preferences, low effort is a Bayesian-Nash equilibrium. The fleet's meters (quote hit-rate at 52%, QUEUE earned rows, token burn) are a match-early incentive surface: they pay visible frequency over rare hard truth. The operator's no-bulk-self-processing law named this from experience before we had the theorem. Design lever: weight meter credit toward byte-backed, falsifiable, rare artifacts (the rare-words-first preference shift).
2. **Gap 8 (skill compilation) is lived, not hypothetical, here.** Corpus-forged skills (memweave, memlance, mesh-comms), tier packs, VERB compiled onto the RIB, context-pack: all are verified traces promoted to callable primitives. The metrics have fleet instruments: CG approx the context-pack/kernel cache-hit savings (99.4% prefix hit), AR approx skill reuse rows, NC is exactly what drift-patrol measures (29 gala drifts = compiled configs failing out-of-context, healed by name). NC>0 is empirically real in this repo, which is the strongest argument for the Challenge phase.
3. **Challenge -> Retain/Revise/Forget already exists, scattered:** violation ratchet (prune or accept-by-name), seal verify 47/47, census patrol (collect-vs-executed denominators), drift-patrol heals. The brief's claim that this is MAG's specific contribution is confirmed by events: every one of those gates exists because a compiled artifact rotted and someone caught it.
4. **factorioctl lessons = the tier ladder restated by an outside practitioner:** offload hard subtasks to real tools (A*, not LLM pathfinding), width over per-decision quality at thousands of calls, persistent zone memory files, examples up front. Steal candidate: a factorioctl lane as a long-horizon agentic bench (needs Factorio install + RCON port; operator gate on Steam/hosting).
5. **Four-arm experiment (C vs D): proposal only.** Per the no-bulk-self-processing law, no fleet self-spin without an external consumer or a concrete decision. Filed as an operator-gated option, see queue.

## Owed

- Re-derive correct IDs for the 2 falsified refs; verify the 8 unverified citations BEFORE this brief is shipped to any downstream LLM as a reproduction pack. Shipping it as-is would launder DeepSeek's fabricated citations through us (no-fabrication law). Owner: next research window.
- Operator gate: factorioctl lane go/no-go; four-arm experiment consumer.

## Inventory

- `BRIEF_v4_full_20260926.md` (verbatim capture, provenance + truncation disclosed)
- `STEAL_RECEIPT_20260926.md` (this file)
- LINKS row appended (writer zcode-seat-20260926, canonical = share URL)
- queue/todo.md: one gated line added
