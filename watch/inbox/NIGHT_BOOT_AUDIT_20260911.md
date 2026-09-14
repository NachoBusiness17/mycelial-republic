# NIGHT BOOT AUDIT — AGENTS.md vs the estate, 2026-09-11 (boot-memory lane, wave night run)

*Commission: the next seat boots on AGENTS.md + memory index; this week's dig made much
of it stale. Method: read the boot file against today's reality (docker, chain tip,
cards), spot-check pointers, name what a fresh seat would miss. Read-only except this
card. Clock note: the box says Sep 9 (env date, chain ts); cards are dated 09-11 per
wave brief — skew already flagged in CHAIN_STOP_INVESTIGATION; commission filename kept.*

## 1. Stale-claims table

| # | AGENTS.md claim | Reality (evidence) | Fix |
|---|---|---|---|
| 1 | Boot seq: "6 containers expected during F1 WINDOW 09-06→~09-13; restore = `docker start mag-control-plane`" | 3 containers exist total: mag-sovereign (up since 09-08T09:45Z), mag-worker, mag-redis. The fleet was REBUILT — mag-control-plane/kind-mag/mag-ollama/mag-openclaw names do not exist in docker at all (watch/inbox/CHAIN_STOP_INVESTIGATION_20260911.md §2). The restore one-liner would error. | Replace census line: "3 containers (mag-sovereign, mag-worker, mag-redis) + host ollama = full body; retired stacks park behind compose profiles (`retired-eye`, `retired-openclaw`), resurrection = one command." |
| 2 | Boot seq: docker census is the fleet-health read; no mention of where the eye lives | The eye migrated to HOST ollama 09-07 (13 models, host.docker.internal:11434); mag-ollama retired behind `retired-eye` (watch/OLLAMA_EYE_TO_HOST_20260907.md, also state/CURRENT.md). A fresh seat flags the "missing" eye container as an incident. | Add one line: "the eye is HOST ollama, not a container — absence of mag-ollama is by design." |
| 3 | Boot law 3: "Idle containers are not the pulse" is NOT in AGENTS.md — only in the 09-09 fold | Fold law 3 (operator correction: "we shut down mag on your instructions"): files are the body; census is not health. The boot file still makes `docker ps` step 4 of boot. | Keep docker ps but caption it: "census, not health — judge the fleet by files + chain." |
| 4 | LAUNCH LAW: "BUILD WINDOWED items spawn their builder SAME TURN — only operator gates defer" | BUILD FREEZE STANDING since 09-09 fold: "no big builds until the coldest vertex pass" (watch/SELF_STEAL_DAY_FOLD_20260909.md; PYRAMID_VISION repeats the gate). AGENTS.md never names the freeze → a fresh seat following the launch law verbatim violates it. | Add to current arc: "BUILD FREEZE STANDING (09-09): the coldest-vertex gate IS the operator gate the launch law defers to. Cards may spawn; big builds wait." |
| 5 | Fold card: "Chain: 7,377, tip verified" (09-09) | 7,377 was the FROZEN tip — chain append was gated shut Sep 6 23:09Z (tip-root mismatch, knots silently refused). Re-armed since: tip now n_leaves 7,392, root 0a141dcb…, last knot 09-09T18:51Z (verkle_tip.json verified tonight). | AGENTS.md boot is fine (reads live tip); add arc line: "chain froze Sep 6 → root cause found (CHAIN_STOP_INVESTIGATION_20260911) → re-armed, tip 7,392 and moving." |
| 6 | "AutoClaw app = sanctioned desktop exception… Its seat mailbox needs the one in-app prompt to close" (08-27) | Openclaw RETIRED 09-09 on operator GO — gateway + tailscale sidecar + cloudflared parked behind `retired-openclaw`; zero traffic 09-02→09-09 (watch/OPENCLAW_RETIRED_20260909.md, reversible one command). | Replace the AutoClaw line with the retirement pointer; note the outside-door question is UNPROVEN-residue, not open work. |
| 7 | state/CURRENT.md (a boot-sequence source) | Frozen at 09-08T17:00Z ("route: day 09-08"); the 09-09 fold + 09-10/11 events supersede it. Fresh seat boots into a one-day-old world. | Update CURRENT.md route line to the fold + freeze + re-arm; or caption it "live status lives in watch/ fold cards." |
| 8 | RESEARCH WINDOW: "wall = Sep 20 = proof deadline (16 days)" (dated 09-04) | 11 days from the 09-09 fold; fewer tonight. Countdown drift misleads urgency. | State the wall once with its date ("Sep 20"), drop day-counts that rot. |
| 9 | Open-rib spine status in cards: "BUILT BUT GATE-BLOCKED, promotion = one act" (watch/OPEN_RIB_SPINE_20260909.md) | PROMOTED AND RUN: tools/index/projects_index.py exists; watch/ESTATE_INDEX/ holds ESTATE_INDEX.jsonl + rollup.json + last_run.json. (Not an AGENTS.md claim — but it is the arc's open question, now closed.) | Stamp the spine card header: "PROMOTED 09-09/11 — running; this card is now the ancestor record." |
| 10 | Pointer spot-check (20 paths incl. all 10 requested): CONVO.md, INBOX/, corrections skill, ROCINANTE_SUBSTRATE_SALON, CURRENT.md, verkle_chain.jsonl, WRONGTHINK + FILTER_1301 cards, riddler_charged_graphs.yaml, 1301_lexicon_diff, TESUJI_MAP, VISION_PIPELINE, MCP_TOPOLOGY, TRAJECTORY_LENS, ZAI reference, SPORE_SANCHO, ZCODE_SELF_STEAL, auth_tracks.yaml, ponytail canon | 20/20 EXIST. No dead pointers in AGENTS.md. One near-miss outside it: DESKTOP_HOMECOMING lives in watch/inbox/ (fold card cites it bare); today's commission cited SELF_STEAL_DAY_FOLD under inbox/ — it lives in watch/. | None needed in AGENTS.md; fold-card citation habit: give the dir when the card is not in watch/. |

## 2. Missing-block drafts (what a fresh seat would MISS that this week proved critical)

**A. THE ROTATION DOCTRINE + WAVE PROTOCOL** (source: watch/WAVE_CADENCE_STEAL_20260909.md).
Draft block: "WAVE PROTOCOL (09-07→09-09, formalized): one input = one wave; burst fan-out
6-8 wide through shared sessions; per-item triage TYPE / CONNECTS TO / NEXT STEP / FILE TO;
heartbeat 18-25s between waves is SANCTIONED idle ('the wave holds'), the one legal
exception to stop-when-verified; validity = zero-shared-context convergence (disagreement
is the finding); rotate on fold — each worker absorbs prior workers' cards before filing
its own. Night runs 8-wide descend from this. A fresh seat seeing parallel workers +
bounded idle would read both as law violations. They are the cadence."

**B. THE DESKTOP CORPUS** (source: watch/inbox/DESKTOP_HOMECOMING_20260909.md +
RECORD_POOL_CENSUS_20260911.md). Draft block: "The corpus is NOT repo-only. Desktop
'New folder' = 248 operator hand-saves (245 MB; wow.txt 1.2 MB, ractor-salon saves,
dogfood-trajectory). The record pools: logs/ (kpi.jsonl 457 MB continuous since Jul-21 —
holds the Aug 16-31 silence), memory/runs/ 21.6k files, ghost trail = the one unbroken
record. Fold law 6: sweeps walk the operator's surfaces, not just the repo."

**C. THE BEACON GATE** (source: watch/BEACON_LIGHT_20260907.md). Draft block: "The last
deterministic act is staged and WAITS ON THE OPERATOR'S VOICE: read the Jul-27 mirror
knot aloud (copy redacted at watch/inbox/DAWN_READING_MIRROR_20260907.md), seat knots it
verbatim uncommented, the frame renders it as first light. Nothing renders before the
light exists — no seat pre-renders, no seat 'helps'. Mirror, not megaphone."

**D. FLEET TOPOLOGY (post-rebuild)** — folded into table rows 1-2; draft line for boot:
"Body = mag-sovereign + mag-worker + mag-redis + host ollama. Retired-but-reversible
stacks sit behind compose profiles: `retired-eye`, `retired-openclaw`."

**E. PYRAMID RULE + MOON-SPEAK** (sources: watch/PYRAMID_VISION_20260911.md;
CONVO row 09-11T17:29Z + watch/salon_source_moon_speak_20260911.md). Draft lines:
"Build test: does it make the corpus more truly remembered — what we found, where, in
colors a person reads at a glance? Decoration waits. Replies: plain English, short lines,
earned names used back but never metaphor-stacked (operator: 'stop speaking moon speak';
drift is default behavior, reward gravity UNPROVEN). Law filed in CONVO; not yet in the
corrections skill."

## 3. One-line verdict

AGENTS.md's pointers are sound (20/20) and its 09-10 layer (WRONGTHINK, FILTER 1301) is
current — the rot is the boot census (a fleet that no longer exists), the unnamed build
freeze, and four load-bearing doctrines (wave protocol, desktop corpus, beacon gate,
moon-speak law) that live only in cards a fresh seat has no pointer to. The drafts above
are paste-ready for the next AGENTS.md touch, which is an edit to the boot file itself —
deliberate human promotion, not this card's to make.
