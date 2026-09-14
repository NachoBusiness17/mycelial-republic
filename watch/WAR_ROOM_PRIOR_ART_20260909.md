# WAR ROOM PRIOR ART — the dig (2026-09-09)

> **[AUDIT-TYPED]** status: SUPPORTED (per-cluster receipts below; the novelty
> deltas are UNPROVEN until their own cite-gate passes — witness law holds:
> no public claim ahead of proof) · trigger: operator "dig deeply, there has to
> be people doing this" on the war-room conversation compiler · 7 clusters,
> 3 search sweeps, cite-gated to primary sources where fetched.

## VERDICT

Every COMPONENT of the war room exists in the wild — belief-state negotiation
agents, debate-as-game with a human judge, steering/debugging interfaces for
live agent conversations, social sims with belief/memory substrate, even
production machine-conducted human negotiations at Walmart scale. **What
nobody appears to have assembled: the human-composable board.** The operator
as PLAYER firing rhetorical devices as game actions, with conditional trap
payloads, compiling in both directions (board→prose for humans, board→
injection for agents). The field built every part and left the cockpit empty.

## The clusters (all SUPPORTED — primary sources linked)

**A. Cicero (Meta FAIR, Science 2022)** — the closest single ancestor. An agent
that plays Diplomacy at human level by maintaining a belief state over other
players' intents inferred FROM dialogue, then generating negotiation messages
conditioned on its strategic plan. [Meta's page](https://ai.meta.com/research/cicero/) ·
[Science paper](https://www.science.org/doi/10.1126/science.ade9097) ·
[code](https://github.com/facebookresearch/diplomacy_cicero).
Notably: it revealed its own strategic intent in messages as a persuasion
tactic — our walk-away clause, independently found. DELTA: Cicero is the
machine playing; nobody gave the human the board.

**B. AI safety via debate (Irving/Christiano/Amodei 2018)** — two agents play
an adversarial argument game; a HUMAN JUDGE's belief is the target being
steered; honest arguments are structurally cheaper than lies.
[OpenAI](https://openai.com/index/debate/) ·
[arXiv 1805.00899](https://arxiv.org/abs/1805.00899).
DELTA: the human is the JUDGE there, the TARGET there. Our inversion — the
operator as SHOOTER — is not in this literature.

**C. Negotiation benchmarks** — NegotiationArena (Bianchi et al., ICML 2024:
multi-turn LLM-vs-LLM negotiation, agents exploit each other per scenario
setup) [code](https://github.com/vinid/negotiationarena) · [paper](https://arxiv.org/abs/2402.05863);
plus 2025 successors: seller-agent bargaining benchmark
[arXiv 2509.06341](https://arxiv.org/html/2509.06341v1), multi-issue
negotiation game benchmarks on OpenReview. DELTA: they EVALUATE agents;
they don't hand a human a steering surface. STEAL: their metrics become
F-CONV-2's measurement kit.

**D. Production machine-negotiation** — Pactum's agents run autonomous
supplier negotiations in production at Walmart and Maersk (~3% savings,
HBS case study exists). [pactum.com](https://pactum.com/) ·
[IEEE Spectrum](https://spectrum.ieee.org/ai-contracts) ·
[HBS case](https://hbsp.harvard.edu/product/TB0756-PDF-ENG).
DELTA: corporate, template-driven, no visible move/board layer, closed.
Prior art that machine-vs-human negotiation PAYS; none that it's PLAYABLE.

**E. Social deduction / hidden-role LLM games** — AvalonBench, Avalon-LLM,
Bayesian social deduction with graph-informed LMs, ParliamentBench
(Secret Hitler), emergent-dynamics studies ("Trust, Lies, and Long
Memories"). Belief-conditioned agents, deception, persuasion under hidden
information — one team lifted the good team's win rate 13%→48% via LLM
agents. [survey-grade entry](https://arxiv.org/html/2607.10814v1) ·
[Avalon-LLM](https://github.com/jonathanmli/Avalon-LLM) ·
[Bayesian deduction](https://camplab.ai/bayesian-social-deduction/).
DELTA: all inside game victory conditions; steering the conversation is
the MEANS, never a product. STEAL: their belief-tracking formats for our
READ layer.

**F. Generative agents / social sims** — Stanford Smallville (Park et al.
2023: memory stream + reflection = evolving beliefs, 25 agents, 7,700+
citations) [paper](https://arxiv.org/abs/2304.03442) ·
[code](https://github.com/joonspk-research/generative_agents);
DeepMind Concordia — open-source GABM library, agents grounded in social/
digital systems, v2.0 with multi-actor environments
[library](https://github.com/google-deepmind/concordia) ·
[paper](https://arxiv.org/html/2312.03664v2).
DELTA: substrate exists, open-source — but no adversarial steering layer,
no move/device taxonomy. STEAL: Concordia is a candidate substrate for
F-CONV-2 control rounds; Smallville's retrieval scoring for our READ.

**G. Steering/debugging live multi-agent conversations** — "Interactive
Debugging and Steering of Multi-Agent AI Systems" (arXiv 2503.02068, March
2025) — interactive intervention into running agent conversations;
AutoGen's shared-state discussion threads; Pipecat's explicit message
injection. [paper](https://arxiv.org/html/2503.02068v1) ·
[AutoGen](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/).
DELTA: intervention is for DEBUGGING (fixing errors), not strategic steering
toward a summit; no move taxonomy, no assumption traps. FULL READ OWED —
this is the nearest neighbor and the follow-up door.

## The five novelty deltas (each UNPROVEN until cite-gated)

1. **The human-composable board** — operator as PLAYER (shooter), machine as
   compiler. Nobody surveyed hands the human this interface.
2. **Conditional traps** — payloads that detonate when the transcript shows
   the target COMMITTING to an assumption. Persuasion work measures outcomes;
   nothing found that pre-plants commitment-triggered payloads.
3. **Dual-target compile** — one board, two compilers: prose for humans
   (Adam-class letters), injection for live agent sessions. All prior art is
   one or the other.
4. **Register/device taxonomy** — moves typed by persona (ractor DNA: voice ×
   device × target-assumption). Negotiation benchmarks use scenario setups,
   not persona-registered move vocabularies.
5. **SHERPA governance** — steering constrained to a declared summit,
   audited on-chain. No steering framework in the set carries an ethical
   constraint layer at all.

## Canonical human-layer (not fetched this dig — known texts, tri-state noted)

Schelling, *The Strategy of Conflict* (1960): credible commitments — the
walk-away clause IS Schelling's "the power to bind oneself is the power to
bind others." Cialdini's pre-suasion: planting assumptions before the message
= the trap mechanic. Negotiation wargaming: standard practice in diplomacy
and strategy consulting. Litigation decision trees: lawyers already model
cases as probability boards. These are the DEEP ancestors — the war room is
their first playable assembly. [inferred, canonical texts not re-fetched]

## What the dig changes about the war room card

- The design is NOVEL AS AN ASSEMBLY, not as any component — claims to the
  public must say exactly that (Tesla admission gate: no announcing ahead).
- Concordia and NegotiationArena are open-source → F-CONV-2 doesn't need
  building from zero; the control rounds can run on their rails.
- arXiv 2503.02068 gets a full read before any build — nearest neighbor,
  and its authors may already be two steps down our road.

---

# ZEITGEIST TRIANGULATION + THE STEAL LIST (added ~11:4xZ, same day)

> The 1112 protocol, three points: **A** = our build line (war room, kabuki
> interference, tavern+brawl, ractor DNA, shitpost desk as projectiles,
> following audit, tesuji field, RIB WORLD's buried DM engine) · **B** = the
> zeitgeist (the seven clusters above) · **C** = our goals (sovereign local
> fleet, honest record, $0, Sep 20 falsifier deadline, Rocinante, loudness,
> the seed field). Where all three meet: the findings and the takes.

## AGDebugger decoded (the nearest neighbor, cite-gated)

arXiv 2503.02068 = **AGDebugger**: message browsing UI + EDIT/RESET of prior
agent messages ("time-travel debugging") + overview visualization, designed
from 5 developer interviews, validated with 14 participants. It is a FIXING
tool — developers repairing errors. No move taxonomy, no adversarial strategy,
no assumption traps, no prose compilation, no governance. **The delta holds.**
Steals: the time-travel primitive (our twist: the NECROMANCER reset — roll
back WITH a receipt of what learned, rollback-with-memory is fleet-native),
and its validation shape (interviews + n=14 study) as the template for our
F-CONV falsifier writeups.

## The three-point fix (findings)

1. **TIMING — we are the field's next step, not its imitator.** The arc reads:
   static benchmarks (2023) → multi-agent evals (2024, NegotiationArena) →
   steering/intervention for debugging (2025, AGDebugger) → **strategy-level
   steering with move semantics and governance (2026 = our card).** The
   zeitgeist is walking toward the war room from the debugging side while we
   arrived from the game/kabuki side. The Sep-20 proof deadline rides a crest,
   not a rear-guard.
2. **THE SOVEREIGNTY WEDGE IS EMPTY.** Production machine-negotiation is
   corporate-closed (Pactum); research artifacts are study-grade and
   developer-facing. The open, local, personal, game-native cockpit for ONE
   operator does not exist anywhere in the surveyed field. That quadrant is
   exactly our goals (sovereign, local, honest record) — the public-lab
   claim writes itself: *the sovereign cockpit*. It is also the career
   differentiator: "decision systems at three scales" now has a playable
   demo behind it.
3. **THE ASSEMBLY COST JUST COLLAPSED.** Concordia (Apache-2.0) already has
   the Game Master engine — tabletop-RPG-inspired, Entity/Component/Engine —
   which is BOTH the war room's steer layer AND the buried RIB WORLD DM
   module resurrected on modern rails. NegotiationArena (MIT) supports
   custom games = our trap scenarios = F-CONV-2's harness. One thief, two
   cards, both open-licensed.

## THE STEAL LIST (everything useful, ranked by leverage)

1. **Concordia's Game Master engine** (Apache-2.0) — war room STEER layer AND
   RIB WORLD's storyteller in one take. Biggest single steal on the board.
2. **NegotiationArena** (MIT, Bianchi/Jurafsky) — F-CONV-2 harness, custom
   scenarios; Stanford NLP lineage = academic cover for the public claim.
3. **AGDebugger's message-reset/time-travel** — the board gets UNDO; fleet
   twist: necromancer-rollback (with receipt of what learned).
4. **Smallville's retrieval scoring** (recency × importance × relevance) —
   the READ layer's reply-parsing formula, proven at 25-agent scale.
5. **Cicero's belief-state-over-intents** (code open) — formalizes hp/agit
   into first-class belief display on the HUD.
6. **Debate paper's judge protocol** — the design for every blind-judge
   falsifier we run (F-KABUKI-1/2, F-FOLLOW-2, F-CONV-2).
7. **Avalon belief-tracking formats** — serialization for ractor belief state.
8. **Pactum's 3% economics** — a RECEIPT, not code: machine negotiation pays,
   enterprise-proven. Straight into the Nutanix/enterprise letters.
9. **Schelling/Cialdini vocabulary** — tavern_moves.yaml gets academic teeth:
   device → Schelling move class (commitment/threat/focal point) → payload
   template.
10. **The timing datum itself** — "the field arrives at our card in 2026" is
    the answer to the gas-station chorus, and it goes in the recap and the
    letters.
11. **The following-audit seed list** — Concordia team, Bianchi/Jurafsky,
    AGDebugger authors: the first account walls to paste. The dig feeds the
    audit; the loop closes.

## What stays ours (the parts worth claiming)

The payload bridge (tavern_moves.yaml — device→assumption→payload), the
kabuki interference layer (coherence budget, fringe-reading, labels
backstage), the SHERPA governance (declared summit, chain-audited), and the
necromancer rollback. Steal the rails; the cockpit is ours.

## Lawful now vs gated

- **NOW ($0 file work):** tavern_moves.yaml draft with Schelling mapping;
  clone Concordia/NegotiationArena repos into the vault (no runtime); this
  card; the audit seed list.
- **GATED (behind the coldest-vertex pass, operator GO):** running F-CONV-1
  round-trip, F-CONV-2 control rounds on Concordia rails, the compiler
  itself, any public claim (Tesla gate: "novel assembly," never "new field").
