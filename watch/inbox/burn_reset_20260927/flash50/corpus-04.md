# Operator Card audit - is the front door the house?

Item corpus-04, banked 2026-09-28. Source: `docs/ref/OPERATOR_CARD.md` (135 lines).

## The artifact under audit

- Last commit touching the card: `eb07ad62e` "Mag sovereign agent - clean publish baseline", 2026-08-04 11:47:25 -0400 (`git log -1 --format="%H %ad %s" --date=iso -- docs/ref/OPERATOR_CARD.md`). 55 days old tonight.
- Working tree: `git status --porcelain docs/ref/OPERATOR_CARD.md docs/DNA.md` returned empty. The card is byte-identical to the 08-04 publish baseline. Everything that happened since (workflow gate, burn waves, driving ladder, shared inbox contract, this flash50 corridor) postdates the card and none of it reached the card.

## Method (what actually ran)

1. Read the card whole.
2. Existence-checked every path the card names, from the repo root: 13 paths + 2 dirs. Results below.
3. Argument-surface-checked every command the card names against `main.py` source.
4. Recency-checked the card's FIND door data pipeline in the sibling repo.
5. Read tonight's operator-side law (`memory/rib/RIB_DRIVING_LADDER_20260928.md`, `state/CURRENT.md` head) and compared.
6. Not run: `mag.cmd context-pack`, `mag.cmd trail start`, `mag.cmd agent-state --load`, `mag.cmd nervous`, `mycelia.cmd x-pull` were not executed end to end (they write memory/state or hit X); their existence and argument shape is verified from source only. Stated as such.

## Verdict

The spine is accurate and still code-backed. The periphery is a 07-31/08-04 snapshot. A cold seat reading only this card would find the state model intact but would (a) dispatch work to unfunded decoders, (b) look for `mycelia.cmd` in this repo and not find it, (c) never learn that `watch/inbox/` is the durable write root, and (d) never learn that ribs, warm boot, and `state/CURRENT.md` are tonight's boot order. The card's own law is "Depth lives in linked docs, not here" - the amendments below are pointer-style, consistent with that law.

## Verified accurate tonight (13 claims, each checked this ask)

| # | Card claim | Evidence (read/ran this ask) |
|---|---|---|
| V1 | Residual = DNA, chat is heat (card line 81) | `mag/run_trail.py:9` "Ontology (DNA law): residual remains cold SessionEnd DNA" |
| V2 | LOAD = context-pack carries bonds + trail + tip (card line 56) | `mag/context_pack.py:627-634` residual bonds first-class; tip render at `mag/context_pack.py:410-424` (verkle leaves + root); `include_trail` config flags at `mag/context_pack.py:55-138` |
| V3 | `mag.cmd agent-state --load` before redesign (card line 58) | `main.py:621-628` agent-state subcommand, `--load` "Print LATEST.md (full recall pack)" |
| V4 | `memory/agent_state/LATEST.md` + `versions/` (card line 59) | Both exist; `versions/` holds 39,836 files (alive, heavily used) |
| V5 | `mag.cmd trail start "goal" --seat local` (card line 106) | `main.py:669-700`: trail subcommand, `start` in choices, `--seat` default `local` |
| V6 | `mag.cmd context-pack --agent` (card line 46) | `main.py:531` context-pack parser, `--agent` argument at `main.py:561` |
| V7 | `python main.py nervous` (card line 42) | `main.py:369-373` nervous subcommand with `--json` |
| V8 | `mag.cmd doctor`, `mag.cmd bonds` (card lines 103, 105) | `main.py:349` doctor; `main.py:570` bonds parser, dispatch at `main.py:3526` |
| V9 | dig-leaf edge kind exists in the pack reader (card lines 55, 96) | `mag/context_pack.py:556` reads `dig_leaf`/`dig`/`corpus_leaf` edge kinds |
| V10 | Bare PATH python is often Hermes, do not use it (card line 112) | Matches AGENTS.md Python env section; consistent, no contradiction found |
| V11 | Story drawer (card line 125) | `mag/story.py` exists; `memory/story/` exists (2 files - alive but thin) |
| V12 | Depth drawers all resolve (card lines 116-128) | All 9 linked docs exist: DNA.md, MIRROR_PRESENTED.md, memory_verkle_map.md, COORDINATION_ELIAS_ROPE.md, run_trail_lattice.md, MAG_OS_v2.md, FEATURE_COMPOSE.md, MAG_Card.md, plus the kimi eval leaf `memory/improve/evals/models/kimi-k3-2026-07-27.md` and journey leaf `memory/improve/evals/features/nacho-journey-vs-mag-narration-20260731.md` |
| V13 | Stateless-seat model: boundary holds state, decoder stateless (card lines 19-34) | Uncontradicted anywhere in tonight's law; the driving ladder constrains WHICH decoder is funded, not the state boundary itself |

## Stale (4 findings, each with evidence)

S1. **Decoder tier has no funding law.** Card line 26: "Decoder: Any model (remote specialist, local, public) - stateless worker". Tonight's code-as-law (`AGENTS.md` DRIVING LADDER 2026-09-28; `memory/rib/RIB_DRIVING_LADDER_20260928.md` Invariant 1, read this ask): ONLY Hermes is funded ($180 Nous credits, glm-5.3-prime / qwen3.8-max-prime); Anthropic keys in .env are UNFUNDED, no Opus rung; free stealth lanes are a sensing surface, outputs banked as findings never as done-work; "An answer is not an answer until the funded tier or the bytes verify it." The card's tierless "any model" line is exactly the trap the operator corrected three times on the 09-27/28 night (rib: "those aren't funded only hermes"). A fresh seat reading the front door alone walks straight into it.

S2. **FIND door is 08-06 vintage and its binaries are not in this repo.** Card lines 54 and 108-110: `mycelia.cmd x-pull / thread-pull`. Verified: `mycelia.cmd` does not exist in this repo (`ls mag.cmd mycelia.cmd` -> mag.cmd only); it exists in the SIBLING repo `C:/Users/foste/Documents/projects/mycelial-republic/mycelia.cmd` (listed this ask). Recency: newest artifact under sibling `data/` is `annotated/mirror_train_clobber_20260806.jsonl` (08-06); `raw/` is empty; nothing newer found. Tonight's actual intake surfaces (`state/CURRENT.md` head + AGENTS.md load order, both read this ask) are `state/CURRENT.md` live truth, `queue/todo.md`, and the ribs under `memory/rib/` - none named anywhere in the card.

S3. **FILE door's dig-leaf arm never shipped; the real FILE surface is unnamed.** Card line 55: "SessionEnd residual (auto); dig-leaf when P1 ships". Verified: no dig-leaf writer exists - `grep -n "dig"` over `main.py` returns no dig subcommand; `dig_leaf` appears only on the read side (`mag/context_pack.py:556`). "When P1 ships" is still pending 55 days later, so the card's FILE door has been half-vapor since 08-04. Meanwhile tonight's actual FILE surface is the shared artifact boundary: receipts banked to `watch/inbox/` and git commits with item-id prefixes (verified this ask: `watch/inbox/INDEX.json` and `watch/inbox/SHARED_SURFACE_CONTRACT.json` both exist; every one of the last 5 commits is an item banked this way). The card never mentions `watch/inbox` at all. On a machine whose contract says a session directory "must never be the sole copy", the front door omitting the durable write root is the biggest single gap.

S4. **Cross-repo path reads as in-repo.** Card line 15: "Law: `mycelial-republic/docs/AGENCY_SHAPE.md`". From this repo root that path does not exist (existence check: MISSING); the file exists at the sibling `C:/Users/foste/Documents/projects/mycelial-republic/docs/AGENCY_SHAPE.md` (verified). Same latent trap as S2: the "beads (this repo) + forest (mycelial-republic)" split (AGENTS.md Zeitgeist line) is never stated on the card, so the card's two forest references both misresolve for a cold seat.

## Missing (6 things tonight's front door needs, as pointers)

M1. Shared artifact boundary: `watch/inbox/INDEX.json` read-first, `watch/inbox/` durable write root, `watch/inbox/SHARED_SURFACE_CONTRACT.json` is the machine contract (existence verified this ask).
M2. Boot order: warm the ribs (`memory/rib/`, esp. RIB_DRIVING_LADDER_20260928) then `state/CURRENT.md` then act; warm boot `python -m mag.hermes_warm_boot` at session start (AGENTS.md header).
M3. Funding law pointer: DRIVING LADDER 2026-09-28 (fixes S1).
M4. Live truth address: `state/CURRENT.md` is live truth; `memory/briefs/latest.md` is FROZEN 2026-09-26 and must not be consumed as live (AGENTS.md load order).
M5. Workflow gate + receipt culture: gated CreateWorkflow, SaveWorkflow amendments, receipt lands in `watch/inbox/` (AGENTS.md build discipline).
M6. The two falsification laws a banked file must carry: no fabrication (OWED if unverifiable) and no em/en dashes in authored files - tonight's receipts (e.g. sibling `f-04.md` in this corridor) run these scans and cite them.

## Amendments (PROPOSED, not applied)

Not applied to `docs/ref/OPERATOR_CARD.md` itself: the card is the operator's spec (spec-before-behavior law, AGENTS.md build discipline), and this is a read-only audit item. Paste-ready, minimal, pointer-style:

1. Line 26 (Decoder row) - append: `Funded decoder is ONE tier tonight (RIB_DRIVING_LADDER_20260928): Hermes/Nous only; free lanes sense, never answer; verification climbs to the funded tier.`
2. Line 15 - annotate: `Law: ../mycelial-republic/docs/AGENCY_SHAPE.md (sibling repo, not this tree).`
3. Lines 54-55 (FIND/FILE rows) - FIND how: `mycelia.cmd lives in the sibling repo ../mycelial-republic/; its data pipeline last moved 2026-08-06`. FILE how: `Receipts bank to watch/inbox/ (shared surface contract, INDEX.json); dig-leaf writer still unshipped (P1 pending since 2026-08-04).`
4. New one-line block after "Three doors" - `Boot tonight: warm boot (python -m mag.hermes_warm_boot) -> ribs (memory/rib/) -> state/CURRENT.md (live truth; memory/briefs/latest.md FROZEN) -> queue/todo.md -> context-pack.`
5. Commands section - add the sibling annotation: `mycelia.cmd x-pull / thread-pull   # run from ../mycelial-republic/`

## Limits

- Commands verified from source only (see Method step 6); no command executed end to end.
- "Does it reflect how the operator actually works tonight" is answered from the operator's own written law of tonight (AGENTS.md as of this session, RIB_DRIVING_LADDER_20260928.md, state/CURRENT.md head, the flash50 corridor shape) plus the git record - not from observing the operator. That is the evidence the seat can reach; stated as such.
- `docs/ref/OPERATOR_CARD.md` was not modified by this item; the amendment block above is the banked deliverable.
- em/en dash scan on this file: run after write (law), result recorded in the commit message.
