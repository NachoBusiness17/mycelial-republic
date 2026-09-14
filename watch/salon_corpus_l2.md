# SALON — World-Games Prompt Corpus, LAW/ARCHITECTURE lens (L2) — 2026-09-01

> Lens run by the worker seat (cerebras lane rate-limited, this seat took the brief).
> Source: /board/corpus/00_PRIMER.md (§6 = the 9 operating rules; §4 diagram targets;
> §7 T0; §8 agenda) + /board/GAMES_SALON_SYNTHESIS_20260901.md + /board/SALON_RIGHT_TIME_SYNTHESIS_20260901.md
> + the two DRAFT assets. Nothing below is invented; unverified items are marked U.

## (1) RULE-BY-RULE — primer §6 mapped to our enforcement

| # | Primer rule | Verdict | Hook (our lane) |
| :-- | :-- | :-- | :-- |
| 1 | Never improvise randomness | ✅ ALREADY-RAILED | L0 Universal RNG protocol: seeded `value = TABLE[game-id][mode][seed][index]`, LLM reports never rolls. = our meter law (RNG integrity). |
| 2 | Never invent objects + canonical restatement first | ✅ ALREADY-RAILED | L0 OUTPUT CONTRACT #3: pieces exist only if in cached `board`/`order`; `^`-line restatement mandatory. |
| 3 | Never solve; verify | ✅ ALREADY-RAILED | L0 F3 verifier-signature + primer Fact 5; = our truth/narration split (SALON RIGHT-TIME ractor/archivist, Lessig one-chokepoint). Verifier-delegation is architecture, not prompt-nudge. |
| 4 | Never canonize disputed history | 🟡 PARTIAL | `attested/reconstructed/speculative` flags live in L0 notes + packs. But the honesty note is prompt-text, not gate; no verifier forces the flag to surface. Needs a check, not a wish. |
| 5 | Static-first / variable-last | ✅ ALREADY-RAILED | = prefix-exactness (Fact 2). Ours: immutable `prefix_sha`, `[PROMPT-BODY-START]` byte-stable markers, appends-only dynamic tail. |
| 6 | Games as packs, not prompts | ✅ PARTIALLY-RAILED | L1 race/dice engine + 6 pack-deltas prove the pattern. Wants an L2 schema flag; build-row has prefix_sha but no `is_delta_over_engine` field. |
| 7 | Patch the corpus, not the request | 🔴 NEEDS-NEW-HOOK | **Corpus governance gap.** Once L0/L1 are byte-stable and metered, who can touch a static block? K_T rot guards kill on drift but give no patch path/owner. No VCS/branch/review rule in any file. |
| 8 | Surface uncertainty | 🟡 PARTIAL | Written into OUTPUT CONTRACT #5 (reconstructed note) but unenforced; same gap as #4. Say-so-note lives in the model's discretion. |
| 9 | Respect attribution / commercial reskins | ✅ PARTIAL | Editorial notes exist (Kalah/Ludo/Sudoku "reskin" tagged). No lint that a new pack MUST carry `origin_culture` + sources before landing. |
| — | **Research-status field as a live field** | 🔴 NEEDS-NEW-HOOK | Concept exists everywhere; **no schema slot in the build-row** (`game,prefix_sha,tokens…` has no `research_status`) and no editor/owner rule. The primer treats it as data; we treat it as prose. |

## (2) CONTRADICTIONS — targets vs our measurements

- **Primer §4 diagram targets:** L0 ≥99% / L1 ≥95% / L2 ≥90% / L3 ≥70% hits; within-genre ≥85%, cross-genre ≥50% (cross-genre = L0+L1 only). §7/T0 adds L0 ≥99% *legal acceptance*.
- **What we measured:** E6 = 100% hit at 9.2k-prefix, single flat prefix, 4.7× discount (Together V4-Flash). E5 z.ai = 99.7% at 2.1k prefix. Both are WHOLE-PREFIX probes — one static blob, not the L0→L3 layering.
- **The contradiction is a measurement artifact, not a design clash.** Our evidence says "a full frozen prefix hits ~100%." The primer targets say "each layer's *share* of a layered prefix hits ≥(descending) 99/95/90/70." We have never run a layered probe, so per-layer numbers are UNVERIFIED (U) — the targets are not violated or confirmed, only unmetered.
- **What we must measure first:** (a) a real layered request — L0 + L1-race + one L2 (e.g., Ludo) + one L3 pack — and read `usage.prompt_tokens_details.cached_tokens` to confirm every static layer is a contiguous, byte-identical prefix; any L2/L3 clause swap or interleave that breaks prefix contiguity tanks the whole stack, so layer-hits only mean anything if the prefix stays contiguous. (b) Legal-acceptance rate via verifier rejection logs (T0's ≥99% legal) — currently zero instrumentation on legal PASS/FAIL, only on cache-hit.
- **Known rot-guard conflict:** GAMES SALON says prefix-drift <50% hit ×3 = K_T2 kill. But a *new layer under* a stable layer (L2 worded differently) is legitimate, not drift. The kill rule needs a "drift = change above a frozen byte-boundary" qualifier or it kills good growth.

## (3) THE GAP — what the primer assumes our cage cannot do

- **Anthropic `cache_control` breakpoints (Fact 3):** primer assumes explicit breakpoint control. Our live providers (DeepSeek, Together, z.ai-2) cache **automatically on exact-prefix**; we hold no `cache_control` and cannot place explicit breakpoints. That is fine *because* Fact 2 (exact-prefix) makes corpus layout provider-agnostic — but it means the "breakpoint" is a property of the layout, not something we invoke. Any claim that our cage gives breakpoint-level control is UNVERIFIED.
- **Artifact recursion / `window.claude.complete()` (Fact 10):** primer's biggest assumed capability. Requires Claude Code / artifact runtime. **No Claude Code here** — this is a $0 API-lane cage (RNG/lane rails, no browser, no artifact VM). We can approximate recursion only as *model self-calls via API* (a generated game issuing cached-prefix API calls), which is unproven at this lane and tied to a live key. Fact 10 stays a design sketch, not an enforced rail. Mark U for this cage.
- **On-PCB runtime state (L4 0% hits):** primer treats L4 as never-cached instance state. Automatic-prefix caching across providers may *opportunistically* cache repeated identical L4 strings; we have no instrumentation to assert L4 stays fresh. Needs a row field, not an assumption.

## (4) VERDICT — ONE PARAGRAPH

**Adoptable but NOT as-written — reserve on Rules 4/8 (flag enforcement), 7 (corpus governance), 9 (attribution lint), and the missing research-status schema slot; everything else is already on our rails.** The corpus is byte-stable by construction and matches our measured prefix-exactness reality (E6 100%, E5 99.7%), so the layer targets aren't contradicted — they're just unmeasured per-layer, and measurement (a contiguous layered probe reading `cached_tokens` + a legal-acceptance log) is the first required amendment. The primer's two big assumptions our cage cannot honor — explicit `cache_control` breakpoints and `window.claude.complete()` recursion — are provider/runtime facts, not design flaws; the layout survives them. To adopt cleanly I require three edits before freeze: (1) add `research_status` + `is_delta_over_engine` + `patch_owner` to the build-row schema; (2) write a corpus-governance rule (Rule 7) — static blocks are immutable once metered, any patch is a new byte-boundary with its own prefix_sha, reviewed, and the K_T2 kill qualifier fixed so appended-under layers aren't called drift; (3) add a legal-acceptance meter (T0's ≥99%) beside the cache-hit meter, because cache-hit percent is not legal-correctness percent. With those three, L0 + L1-race ship.

## Required-first amendment list (compact)
1. Layered prefix probe (L0+L1+L2+L3 contiguous) reading `cached_tokens` → per-layer %, U until run.
2. Legal-acceptance log (verifier PASS/FAIL) → T0 ≥99% legal, U until run.
3. Build-row schema += `research_status | is_delta_over_engine | patch_owner` and a governance/immutability clause for Rule 7.
4. K_T2 qualifier: drift = change above a frozen byte-boundary; appended-below is legitimate, not kill.
