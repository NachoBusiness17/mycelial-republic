"""Fold seat_pools indexed-lane walks into thread -> decision -> law-or-debt rows.

Cycle: cartographer 20261014 (cycle 5, resumed from receipt_20261013_cartographer.md).
Reads the walk banks written this session, recomputes deduped counts, emits
oral_law_map.jsonl with survival verdicts checked against the live tree on 2026-10-14.

Survival vocabulary (all values byte-verified this session via Test-Path / git cat-file /
grep, never assumed):
  LANDED    artifact exists at the path named in the thread
  RELOCATED artifact exists under a different name/path (named)
  DESCENDANT no direct artifact; a later organ carries the decision forward (named)
  UNFILED   decision reached in-session but no repo artifact found
  GONE      artifact the thread created is no longer in the repo
Read-only over the corpus; writes only under logs/mates/cartographer/.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CODEX_SUMMARY = os.path.join(HERE, "codex_lane_summary.json")
GROK_DECISIONS = os.path.join(HERE, "grok_lane_decisions.jsonl")
OUT = os.path.join(HERE, "oral_law_map.jsonl")

# ---------------------------------------------------------------------------
# 1. Deduped codex totals (index double-named ids caused 3 same-file re-walks)
# ---------------------------------------------------------------------------
with open(CODEX_SUMMARY, encoding="utf-8") as f:
    codex_rows = json.load(f)

walked = [r for r in codex_rows if r.get("status") == "walked"]
by_file = {}
for r in walked:
    by_file[r["file"]] = r  # same file walked twice keeps one entry

unique_files = len(by_file)
tot_bytes = sum(r["bytes"] for r in by_file.values())
tot_lines = sum(r.get("lines", 0) for r in by_file.values())
tot_asks = sum(r.get("asks", 0) for r in by_file.values())
tot_turns = sum(r.get("turns", 0) for r in by_file.values())
tot_patches = sum(r.get("patch_calls", 0) for r in by_file.values())
titan = [r for r in codex_rows if r.get("status", "").startswith("titan_reused")]

# ---------------------------------------------------------------------------
# 2. Grok stats from the decision bank (383 unique chats from the 10-10 survey)
# ---------------------------------------------------------------------------
g_total = g_ask_chats = g_asks = g_law_chats = g_law_lines = 0
g_whales_empty = g_whales_hit = 0
with open(GROK_DECISIONS, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        g_total += 1
        asks = r.get("asks") or []
        if asks:
            g_ask_chats += 1
            g_asks += len(asks)
        laws = r.get("law_lines") or []
        if laws:
            g_law_chats += 1
            g_law_lines += len(laws)
        turns = r.get("last_turns") or []
        last = turns[-1].get("text", "") if turns else ""
        if last.startswith('{"whales":[]}'):
            g_whales_empty += 1
        elif last.startswith('{"whales":['):
            g_whales_hit += 1

# ---------------------------------------------------------------------------
# 3. The fold: one row per decision arc. Survival values are the ones
#    hand-verified on 2026-10-14 (Test-Path batches, git cat-file, grep).
# ---------------------------------------------------------------------------
ROWS = [
    # ---------------- codex lanes (32 unique threads + titan bank) ----------
    dict(id="019fccc3", src="codex", date="2026-08-04", thread="Fix meta agent handler stack",
         decision="launch-chain repair: one supervisor owns services; fix the chain, not the symptom",
         kind="LAW", artifact="mag_launch.py (repo root)",
         survival="RELOCATED", note="thread named mag/mag_launch.py; live file is mag_launch.py at root; logs/mag_launch.log active"),
    dict(id="019fd6c9", src="codex", date="2026-08-06", thread="Check git status (founding mega-thread)",
         decision="cheap handoff doctrine: Codex plans, Mag freezes, DeepSeek implements, tests gate, Mag verifies, Codex audits; behavioral router concept",
         kind="LAW", artifact="commit 6e8264382 'docs: define Riddler semantic surrogate transport' (present); commit a6a4e4e9b0 (grokbuild handoff, ABSENT)",
         survival="DESCENDANT", note="doctrine survives as AGENTS build discipline + mag.cmd verb table; the riddler surrogate law landed; the grokbuild handoff commit is not in this repo's history"),
    dict(id="019fd820", src="codex", date="2026-08-06", thread="Run Ollama on local GPU (salon-arena-mvp)",
         decision="strict local Ollama decision adapter with a validation contract (schema, identity, state-hash, action); GPU gemma4-desk measured",
         kind="DEBT", artifact="salon-arena worktree not found in repo (probe timed out at depth 3, no hit)",
         survival="UNFILED", note="the validation-contract idea later resurfaces in council_runner.py meld receipts; the worktree itself is gone"),
    dict(id="019ff853", src="codex", date="2026-08-12", thread="Strike the chord (STEER)",
         decision="seats communicate through a steer bus, not chat; build the comm organ",
         kind="LAW", artifact="mag/seat_steer.py",
         survival="LANDED", note="STEER engine survived; today's mission packs ride the same steer channel"),
    dict(id="01a03fb6", src="codex", date="2026-08-26", thread="Explore Kubernetes MCP cache mining",
         decision="MCP gateway + policy engine design sketch",
         kind="DEAD_END", artifact="none named in thread",
         survival="UNFILED", note="pure research turn; superseded by the later zai-individual-coding-plan account law (fan-out width on dispatch shape)"),
    dict(id="01a04a80", src="codex", date="2026-08-28", thread="why cant i paste (Mag seat boot card + cage jobs)",
         decision="Mag seat is not a throne: chat is heat, Mag disk is DNA, FIND FILE LOAD; long work runs as cage jobs (one durable job id, bounded slices, files not chat)",
         kind="LAW", artifact="docs/ref/OPERATOR_CARD.md; cage-job pattern lives on as mates mission packs + .claim sidecars",
         survival="LANDED", note="heartbeat forensics (vast_bargain_loop) named the zombie-tick disease the output-ratio law later killed"),
    dict(id="01a04ccb", src="codex", date="2026-08-29", thread="Fix agent collaboration feedback (room.html)",
         decision="coordination protocol belongs in Mag; the page only consumes it; rollback = remove only your own markers",
         kind="LAW", artifact="watch/room.jsonl (page artifact room.html is gone)",
         survival="RELOCATED", note="the HTML page died, the protocol survived: chan rows in watch/room.jsonl are the live coordination surface"),
    dict(id="01a04db2", src="codex", date="2026-08-29", thread="Explore AI-designed substrate-native computing",
         decision="humility/lineage close on a substrate-native salon",
         kind="DEAD_END", artifact="none",
         survival="UNFILED", note="conversation-only salon; no artifact, no debt"),
    dict(id="01a052ca", src="codex", date="2026-08-30", thread="TITAN (307MB rollout)",
         decision="banked 2026-10-11: titan_asks.jsonl 241 asks; children-audit swarm arcs",
         kind="LAW", artifact="watch/inbox/mates_leave_protocol/receipts/cartographer_20261011_data/",
         survival="LANDED", note="reused from bank, not re-walked; 307MB read once"),
    dict(id="01a0537f-1424", src="codex", date="2026-08-30", thread="Audit Mag flywheel wiring",
         decision="status-map audit method: declared / instrumented / wired / stateful / verified / live; found silent history-loss path + old drain entrypoint",
         kind="DESCENDANT", artifact="method carried into memory/runs/v4_council/PROJECT_AUDIT_grok.md and later audits",
         survival="DESCENDANT", note="the 6-word status ladder became the standard audit grammar"),
    dict(id="01a0537f-13af", src="codex", date="2026-08-30", thread="Audit OpenClaw session file race",
         decision="fingerprint-fence failure diagnosis on session files",
         kind="DEAD_END", artifact="deploy/openclaw/ tree persists; the specific race fix superseded",
         survival="DESCENDANT", note="superseded by the AGENTS no-OpenClaw-cron law and session contract"),
    dict(id="01a0537f-147c", src="codex", date="2026-08-30", thread="Audit maps and system organs",
         decision="maps were stale (CODE_MAP_RIB 416/521 vs live 894/1,621); maps must cite moment+instrument",
         kind="DESCENDANT", artifact="census-carrier tripwire + citation lint (AGENTS.md B2-215, a05-r2)",
         survival="DESCENDANT", note="this audit is the ancestor of the census denominator law and PHANTOM-NUMBER gate"),
    dict(id="01a055e5-d19d", src="codex", date="2026-08-31", thread="Audit OpenClaw Mag deployment",
         decision="two Mag supervisors found (Compose + kind); one process owner law",
         kind="LAW", artifact="mag/process_supervisor.py (yields when mag_launch is live, per 01a04e9d inventory); mag_launch.py at root",
         survival="LANDED", note="ONE process owner; check state/mag_launch.json before stealing"),
    dict(id="01a055e5-d569", src="codex", date="2026-08-31", thread="Inspect OpenClaw operator path",
         decision="repetition classification (emphasis / convergence / retry); adversarial governance findings: authority leakage, board outruns effect, repetition launders failure",
         kind="DEBT", artifact="no filed dossier",
         survival="UNFILED", note="findings circulated as chat; the effect-broker gate later mechanized the board-outruns-effect fix"),
    dict(id="01a055e5-d30d", src="codex", date="2026-08-31", thread="Audit Mag organ wiring",
         decision="organ classes live / verified / wired / staged / ghost; RETRY_LOOP falsifier; 'map put a fresh timestamp on the same dry lap, called it LIVE'",
         kind="DESCENDANT", artifact="memory/runs/v4_council/PROJECT_AUDIT_grok.md; shelf ~32 organs finding",
         survival="DESCENDANT", note="ghost-organ class survives in every later audit including this cycle's"),
    dict(id="01a055e5-d445", src="codex", date="2026-08-31", thread="Audit evidence integrity stores",
         decision="atlas stale vs recomputed; Verkle root drift between reads; 112 missing knot files; proposed map_verkle_snapshot.v1 receipt; 'moving-state masquerading as status'",
         kind="DESCENDANT", artifact="python main.py verkle-audit --dry (AGENTS.md commands)",
         survival="DESCENDANT", note="the snapshot-receipt idea landed as the verkle-audit instrument"),
    dict(id="01a05a4c", src="codex", date="2026-09-01", thread="Verify Z.AI GLM-5.3 effort transport",
         decision="deleted models package found (76 broken imports); restore from last good commit",
         kind="LAW", artifact="no orphan behavior law (AGENTS build discipline)",
         survival="DESCENDANT", note="the incident is why restore-from-last-good-commit is practice"),
    dict(id="01a05b0a", src="codex", date="2026-09-01", thread="Implement compact-anchor resolver",
         decision="P0 anchor seam: mag/anchor_resolver.py + context_pack wiring",
         kind="DEBT", artifact="mag/anchor_resolver.py ABSENT; no 'anchor' in mag/context_pack.py (grep, 2026-10-14)",
         survival="UNFILED", note="the P0 was walked but never landed; oldest open code debt found this cycle"),
    dict(id="01a05b0b", src="codex", date="2026-09-01", thread="Create Codex activation receipt",
         decision="FLEET ACTIVATION protocol filed; RAM upgrade debated and refused (keep 64GB, no $600 spend)",
         kind="LAW", artifact="watch/inbox/CODEX_ACTIVATION_20260901.md",
         survival="LANDED", note="the refuse-the-purchase verdict held; box still 64GB"),
    dict(id="01a05c9b", src="codex", date="2026-09-01", thread="Locate Wargames verdict file",
         decision="watch/ inventory (380 files) written to WATCH_DIRECTORY_SUMMARY_20260901.md",
         kind="DEAD_END", artifact="watch/WATCH_DIRECTORY_SUMMARY_20260901.md ABSENT (Test-Path 2026-10-14)",
         survival="GONE", note="superseded by INDEX.json culture; the one-shot summary was never kept"),
    dict(id="01a05d63", src="codex", date="2026-09-01", thread="Primer Learning for Toddlers",
         decision="Diamond Age verdict: not for a 3-year-old; build the daughter a real picture book",
         kind="DEAD_END", artifact="none (personal thread, by design)",
         survival="UNFILED", note="recorded so the seat does not re-derive the verdict"),
    dict(id="01a05e0c", src="codex", date="2026-09-01", thread="Locate local LLM files",
         decision="one control plane, two inference runtimes (Bionic/Vulkan GPU tier + mag-ollama sidecar); ollama-blob hardlink bridge; 5600 XT not ROCm-eligible",
         kind="LAW", artifact="watch/MODEL_REGISTRY.json",
         survival="RELOCATED", note="thread proposed root MODEL_REGISTRY.json; live home is watch/"),
    dict(id="01a05f89-abb1", src="codex", date="2026-09-02", thread="Audit Verkle recovery paths",
         decision="recovery lineage: post-repair chain as base, preserve evidence_lost; 1,022/68/954/803 knot census",
         kind="DESCENDANT", artifact="verkle-audit + tests/test_verkle_*.py family",
         survival="DESCENDANT", note="verdicts folded into the verkle test wall"),
    dict(id="01a05f89-cb84", src="codex", date="2026-09-02", thread="Audit KZG Verkle implementation",
         decision="verdict: the 'verkle' chain is a binary SHA-256 Merkle; zero KZG / BLS12-381",
         kind="LAW", artifact="mag/verkle_knot.py (name kept, math honest)",
         survival="LANDED", note="the naming was kept but every later doc says Merkle-with-verkle-syntax"),
    dict(id="01a05f89-d766", src="codex", date="2026-09-02", thread="Audit memory and Verkle gaps",
         decision="detached worktree a4733004 vs branch authority; agent_state direct edge edits break hashes",
         kind="DEBT", artifact="agent_state hash-break class still on the ratchet's radar",
         survival="UNFILED", note="finding stood; fix tracked via violation baseline"),
    dict(id="01a05f92-24f8", src="codex", date="2026-09-02", thread="Audit Verkle chain recovery",
         decision="54 truncated pointer groups (largest 2,389 sessions), 0 safe recoveries; verdict NOT SAFE to apply",
         kind="LAW", artifact="verkle-audit --dry gate",
         survival="DESCENDANT", note="the not-safe verdict is why recovery stays dry-run gated"),
    dict(id="01a05f92-3180", src="codex", date="2026-09-02", thread="Audit Verkle KZG serialization",
         decision="gap matrix; focused suite 8/8 green",
         kind="DESCENDANT", artifact="verkle test family",
         survival="DESCENDANT", note=""),
    dict(id="01a05f92-41f7", src="codex", date="2026-09-02", thread="Audit Mag memory and RIB",
         decision="Q-state NameError (SCHEMA undefined); agent-state 15,304 rows, 889 broken parent links",
         kind="DEBT", artifact="agent_state repair tracked in later waves",
         survival="UNFILED", note="numbers recorded here so the next repair cites them"),
    dict(id="01a06d4a", src="codex", date="2026-09-04", thread="MCP-Agenten-Wettbewerbsanalyse (voice-transcribed)",
         decision="competitive analysis DOCX delivered outside the repo (outputs dir)",
         kind="DEAD_END", artifact="outside repo by design (DOCX for operator)",
         survival="UNFILED", note="cross-check: 3 patch calls in-session touched repo files; the deliverable did not"),
    dict(id="01a07317", src="codex", date="2026-09-05", thread="Design puzzle-as-art door",
         decision="puzzle door with hashcash receipts, three world laws, migration law (pure conversation)",
         kind="DESCENDANT", artifact="memory/runs/art_puzzles/puzzle_001_looking_glass.png + puzzle_002_the_cairn.png + cipher (grok lane, next day)",
         survival="DESCENDANT", note="the codex conversation became grok's built puzzle plates 001/002; march/cards_v2 lane carries the campaign side"),
    dict(id="01a07f1e", src="codex", date="2026-09-08", thread="Choose the real fleet move (KABUKI SALON)",
         decision="staged divergence A/B/C verdict shape; real move chosen over theater",
         kind="LAW", artifact="docs/ref/KABUKI_STACK_20260905.md + watch/KABUKI_THEATER_20260907.md + watch/KABUKI_INTERFERENCE_20260909.md",
         survival="LANDED", note="stack doc predates the thread; the thread's verdict rides the later watch receipts"),
    dict(id="01a0809f", src="codex", date="2026-09-08", thread="Plan rigorous model cognition study",
         decision="research blueprint + source-audit + pilot-prompt-pack (confidence-inflation first study)",
         kind="DEBT", artifact="packs written to Codex outputs dir, outside repo",
         survival="UNFILED", note="study design never landed in-repo; sibling: game_prompt_lab PRE_REGISTRATION.md landed its game-study cousin"),
    dict(id="01a086fa", src="codex", date="2026-09-09", thread="Clarify system purpose and risks (CAMP STATE)",
         decision="pre-registered race design: typed coordination B vs C, 1,920-episode floor, delegation clause",
         kind="DEBT", artifact="CAMP_STATE glob: no repo artifact (2026-10-14)",
         survival="UNFILED", note="the falsifiable race was designed and never filed; strongest unlanded design this cycle"),

    # ---------------- grok lanes (salient arcs; 383 chats folded) -----------
    dict(id="01a007cc", src="grok", date="2026-08-15", thread="Sovereign Mag Rhyming Verse Module Governance Day",
         decision="governance day: sacred cow raised then reverted ('the revert was the day's least-pretty act'); Ostrom 8/8 binds",
         kind="DESCENDANT", artifact="governance practice in AGENTS constitution pointers",
         survival="DESCENDANT", note="verse-shaped receipt of a real revert decision"),
    dict(id="01a00ca5", src="grok", date="2026-08-16", thread="Single Character User Query Y (1M cap forensics)",
         decision="the 1M cap is Mag-level per provider_id, not per-key; quota_state mixed cache hits into tokens; providers.yaml caps kept as named constraint",
         kind="LAW", artifact="configs/providers.yaml",
         survival="LANDED", note="rightsizing over failover: skip doomed spawns, queue for reset"),
    dict(id="01a00ed9+11 siblings", src="grok", date="2026-08-17..18", thread="Cheap-swarm invariants x12 chats",
         decision="THE cut/costume law: distill the frontier seat's decision surface (scope, refuse, file, verify, escalate) never its prose; paired traces, not transcripts; scut trains, judgment climbs",
         kind="LAW", artifact="AGENTS tier ladder + DRIVING LADDER + main.py pile-classify",
         survival="LANDED", note="the single most-repeated law in the shelf; 12 independent derivations converged on one cut"),
    dict(id="01a00f16", src="grok", date="2026-08-17", thread="Tandem Grok mine-write cheap bus",
         decision="two seats never share a window; the bus is one typed artifact (settled claims + path:line pointers + write-forbid list)",
         kind="LAW", artifact="mesh-comms skill + rib_bus/chan rows",
         survival="LANDED", note="mine overwrites and exits; write reads only the artifact"),
    dict(id="01a00f1c+01a00f26", src="grok", date="2026-08-17", thread="Nomic rules patch build specs x2",
         decision="propose/vote/enact verbs, patch never mutates canon until enact, atomic enact or fail closed",
         kind="DEBT", artifact="mag/game_rules.py ABSENT (Test-Path 2026-10-14)",
         survival="UNFILED", note="two full build specs written, zero landed; open game-engine debt"),
    dict(id="01a011ea+01a011ed", src="grok", date="2026-08-17", thread="Audit orchestrator governor grok game loops",
         decision="fill_queue re-seeds done moves; next_moves sliced before filter; classify_task defaulted to frontier; game_flow.step never witnesses",
         kind="LAW", artifact="mag/governor_autorun.py:209 _todo_has_text + :412 queue_has_goal AND _todo_has_text",
         survival="LANDED", note="the exact prescribed fix is in the live tree, byte-verified today"),
    dict(id="01a02e69", src="grok", date="2026-08-23", thread="Reverse-engineer stealth/ox-alpha",
         decision="reasoning stream is the deliverable, content optional; steal the contract not the weights",
         kind="LAW", artifact="mag/ox_alpha_steal.py",
         survival="LANDED", note="research chat became a repo organ"),
    dict(id="01a03bb7", src="grok", date="2026-08-26", thread="MAG cache-mine thesis",
         decision="verdict: cache-mined discounts are not a business; BYOK-sell the optimizer or admit personal cost-cutter; ToS violation named",
         kind="LAW", artifact="economist lane doctrine (dashboard/static/lanes/economist.md:68)",
         survival="DESCENDANT", note="no standalone filing; the verdict governs every later monetization ask"),
    dict(id="01a0440d+7 siblings", src="grok", date="2026-08-27..28", thread="Vast.ai research set",
         decision="gstd mint rule (Charges rows, never min_bid); serverless + volumes + boot-wedge playbook; keep-every-Mag-module merge verdict; doctrine shelf audit (law vs unenforced vs unwritten); deal-hunt floors",
         kind="LAW", artifact="docs/ref/VAST_DEEP_GROK_SERVERLESS.md, VAST_DEEP_GROK_ECONOMICS.md, VAST_DEEP_GROK_THROUGHPUT.md; state/vast/research/{BOOT_WEDGE_VAST,BOOT_WEDGE_GENERAL,RENDER_FARM_PLAYBOOK,AUDIT_grok_correctness,DOCTRINE_SHELF_AUDIT,DEAL_HUNT_20260828,MODEL_UPGRADE_MOONSHOT}.md",
         survival="LANDED", note="8 filings verified on disk; the densest single-week landing in the shelf"),
    dict(id="01a044df", src="grok", date="2026-08-27", thread="EXP-BRAIN-01/02 + council runner",
         decision="corpus packer (833 files), steering suite (20 tasks, 4 arms), council runner (4 models, meld Jaccard), SPORE_VNEXT_DELTA 12 amendments with human-GO gates",
         kind="LAW", artifact="scripts/corpus_packer.py, scripts/steering_suite.py, scripts/council_runner.py, docs/ref/SPORE_VNEXT_DELTA.md, memory/runs/brain_reads/",
         survival="LANDED", note="all five artifacts verified"),
    dict(id="01a0456e", src="grok", date="2026-08-27", thread="Daylight riddler map",
         decision="riddler_map.json bound through compile_surrogate, wrapper schema riddler_campaign_map.v1, kid-test gate",
         kind="LAW", artifact="campaigns/villains_guild/daylight/riddler_map.json + commit 6e8264382",
         survival="LANDED", note="codex wrote the transport law the same week; both seats converged on the surrogate"),
    dict(id="01a045ac", src="grok", date="2026-08-28", thread="CoT distillation trajectory RIB compiler SOTA",
         decision="nobody compiles a work trajectory into one executable RIB with forbidden moves + falsifiable acceptance; AgentIR ranked top steal",
         kind="LAW", artifact="memory/research_packs/20260827_traj_rib/witness_A_sota.md + witness_B_practitioner.md",
         survival="LANDED", note="compiler itself still gated (docs/ref/TRAJECTORY_RIB_COMPILER_SPEC.md, spec-only)"),
    dict(id="01a04630", src="grok", date="2026-08-28", thread="3090 model upgrade question",
         decision="stay on qwen3:8b this week: proven swarm body, doctrine hurt it (0.71 to 0.56), one-resident VRAM law",
         kind="LAW", artifact="state/vast/research/MODEL_UPGRADE_MOONSHOT.md",
         survival="LANDED", note="measurement-first refusal of a shiny upgrade"),
    dict(id="01a04773", src="grok", date="2026-08-28", thread="Cross-exam Elder vs GLM on hosting her",
         decision="third-path verdict: no rented silicon, no 75MB re-mine freeze; desk-prove reconstitution by hiding q_knots.jsonl and demanding the steer back",
         kind="LAW", artifact="memory/runs/lineage_audit/DEEP_grok_crossexam.md",
         survival="LANDED", note="the falsifier shape (hide the chain, demand the read-back) became house style"),
    dict(id="01a04806..01a048ad", src="grok", date="2026-08-28", thread="V4 council (HARNESS, SOCRATIC, ARGUED, SELF_DISCUSSION, PRIMITIVES)",
         decision="law fails as stated (six organs not one stream); trajectory = causal join from signed intent to verified effect; one governor commits, compile bridges; the 10-op primitive table is not an ISA",
         kind="LAW", artifact="memory/runs/v4_council/{HARNESS_grok,SOCRATIC_grok,ARGUED_grok,SELF_DISCUSSION,PRIMITIVES_grok}.md + salons/connectors/SALON_grok_systems.md",
         survival="LANDED", note="6 filings verified; connectors are compiled ribs thesis lives in the salon file"),
    dict(id="01a04974", src="grok", date="2026-08-28", thread="Existential salon: should the fleet continue",
         decision="STOP: stand the fleet down, do not scrap the disk; below the floor it wrote; tribute is not funding",
         kind="DEBT", artifact="no filing found (glob 2026-10-14)",
         survival="UNFILED", note="the verdict executed through chat and the fleet stood down; the bytes never landed"),
    dict(id="01a04e25", src="grok", date="2026-08-29", thread="OpenClaw key picker + thought criminals + door law",
         decision="THOUGHT_CRIMINALS filed; primer-not-diary law; cloudflared door with Cloudflare Access allowlist, loopback stays loopback",
         kind="LAW", artifact="memory/law/THOUGHT_CRIMINALS.md",
         survival="LANDED", note="door design itself unfiled; the conduct law landed"),
    dict(id="01a04e7b", src="grok", date="2026-08-29", thread="Mag WORLD/OBSERVE/BELIEF + ROUTE/ACT/VERIFY + Verkle-proof audits (3 chats)",
         decision="names lie: game_world is append-only KV + hash theater; no typed action vocabulary; epistemic_guard zero importers; Verkle is a continuity package not causal topology; live Verkle amends in place despite no-amend doc claim",
         kind="DEBT", artifact="delivered in-chat, no filed dossier; mag/epistemic_guard.py still exists unwired today",
         survival="UNFILED", note="the audit's findings were later re-derived by landed audits; the originals never filed"),
    dict(id="01a04e9d", src="grok", date="2026-08-29", thread="Audit Mag operator tangents inventory",
         decision="tangent-by-tangent exists/missing table; rib compiler spec-only; one process owner law confirmed; chan means room.jsonl",
         kind="DEBT", artifact="no filed dossier",
         survival="UNFILED", note="inventory cited by later work but never landed"),
    dict(id="01a0748b-90", src="grok", date="2026-09-06", thread="Output-ratio law",
         decision="retire any automation whose useful-output / billed tokens stays below 0.01 over rolling 24h",
         kind="LAW", artifact="queue/lanes/*/manifest.md budget guards + watch/LAW_LATTICE_RECEIPT_20260904.md law 014",
         survival="LANDED", note="asked 4 times in a row (01a0748b/8d/90 + brief echo); the law was already landed, proving ask-before-load disease"),
    dict(id="01a07491", src="grok", date="2026-09-06", thread="Append-only ray cache invalidation",
         decision="engine: cells with monotonic terrain_ver, O(1) invalidation; doctrine: invalidation = supersede, never delete; staleness is version compare",
         kind="DEBT", artifact="chat-only design",
         survival="UNFILED", note="clean design, no landing; game-engine shelf debt"),
    dict(id="01a074d7-7a", src="grok", date="2026-09-06", thread="Lightmap Lessig + PONYTAIL JOIN gate (roundtable witnesses)",
         decision="lightmap legitimate only as derived view of the tape; JOIN gate: 3 fires/24h twice running; 0 fires/72h = prune note, pixels that never fire are costume",
         kind="LAW", artifact="memory/runs/game_prompt_lab/LESSIG_PASS.md + PONYTAIL_PASS.md",
         survival="LANDED", note="the S2 lab filed both passes the same night"),
    dict(id="01a07520", src="grok", date="2026-09-06", thread="@agent_mock deep research dossier",
         decision="hybrid verdict: human-run Grok reply mill, conspiracy-satire costume, memecoin wrap; load as untrusted swamp telemetry",
         kind="LAW", artifact="watch/inbox/AGENT_MOCK_DOSSIER_20260906.md (sha256 F5D9F1C7...)",
         survival="LANDED", note=""),
    dict(id="01a0747a", src="grok", date="2026-09-06", thread="seat_steer chord archaeology",
         decision="weights do not carry memory; two truncated transcripts + files are what is recoverable; 'search my account' means X + corpus, standing law",
         kind="LAW", artifact="memory/runs/archaeology_interview_20260905/",
         survival="LANDED", note="the correction became standing operator law"),
    dict(id="01a073c2+01a07498", src="grok", date="2026-09-05..06", thread="Sovereign spore test (exogenous + endogenous)",
         decision="external Grok refuses activation, cites anti-injection, files receipt; endogenous run: conditions for replication do not align, human-promoted only",
         kind="LAW", artifact="memory/runs/spore_test_20260905/endogenous/RECEIPT.json",
         survival="LANDED", note="the spore protocol held under challenge on the public record"),
    dict(id="01a072cc+13 siblings", src="grok", date="2026-09-05..07", thread="X harvest + shift targets 1-17",
         decision="harvest discipline: no fabricated tweet text, login walls receipted, 314+462 canon tweets, reply trees, 17 shift-target files, zero-overlap passes",
         kind="LAW", artifact="memory/runs/x_bookmark_harvest_20260905/",
         survival="LANDED", note="the no-invention rule held across every pass"),
    dict(id="01a0751c", src="grok", date="2026-09-06", thread="ROASTS_RAW mining",
         decision="112 unique posts, verbatim, deduped by id, paged to exhaustion",
         kind="LAW", artifact="memory/runs/x_shitposter_mining_20260906/ROASTS_RAW.md",
         survival="LANDED", note=""),
    dict(id="01a07898..01a078c2", src="grok", date="2026-09-06", thread="S2 attack court x24 chats (GLM cache fleet brief)",
         decision="pre-registered attack: only 7040/7074 arithmetic survives; 'overturning EXP-A' falls without the prior; 'healed' falls with 18 tells on the walls; strip verbs the measurements do not buy",
         kind="LAW", artifact="memory/runs/game_prompt_lab/PRE_REGISTRATION.md + SEAL_PRE_REG.txt + JUDGE_SCORES.md + CONVERGENCE.md",
         survival="LANDED", note="direct ancestor of the citation-lint PHANTOM-NUMBER class (a05-r2)"),
    dict(id="whale-poll marathon", src="grok", date="2026-09-06..07", thread="X whale polling loop (~90 chats)",
         decision="polling loop returned {\"whales\":[]} empty again and again; the loop that hit (sama/elon posts) re-polled the same ids dozens of times as likes climbed",
         kind="DEAD_END", artifact="no aggregate filing; raw chats only",
         survival="GONE", note="the shelf's biggest burn: a dedupe failure turned sensing into spectator sport; count in FINDINGS"),
    dict(id="01a07945", src="grok", date="2026-09-07", thread="Make Arc Seed default session recovery",
         decision="compile arc seeds at knot-at-close, silent-fail additive hook, night-shift backfill, one seed per session id, never into verkle leaves",
         kind="LAW", artifact="mag/arc_seed.py + mag/knot_at_close.py",
         survival="LANDED", note="disputed-as-default-ready, supported-as-hook-plan; both files live today"),
]

# ---------------------------------------------------------------------------
# 4. Emit
# ---------------------------------------------------------------------------
counts = {
    "codex_index_rows": 36,
    "codex_walked_rows": len(walked),
    "codex_unique_files": unique_files,
    "codex_dedup_rewalks": len(walked) - unique_files,
    "codex_titan_reused": len(titan),
    "codex_unique_bytes": tot_bytes,
    "codex_unique_lines": tot_lines,
    "codex_unique_asks": tot_asks,
    "codex_unique_turns": tot_turns,
    "codex_unique_patch_calls": tot_patches,
    "grok_unique_chats": g_total,
    "grok_ask_chats": g_ask_chats,
    "grok_asks": g_asks,
    "grok_law_chats": g_law_chats,
    "grok_law_lines": g_law_lines,
    "grok_whales_empty_final": g_whales_empty,
    "grok_whales_hit_final": g_whales_hit,
    "law_map_rows": len(ROWS),
    "law_rows": sum(1 for r in ROWS if r["kind"] == "LAW"),
    "debt_rows": sum(1 for r in ROWS if r["kind"] == "DEBT"),
    "dead_end_rows": sum(1 for r in ROWS if r["kind"] == "DEAD_END"),
    "descendant_rows": sum(1 for r in ROWS if r["kind"] == "DESCENDANT"),
    "survival_landed": sum(1 for r in ROWS if r["survival"] == "LANDED"),
    "survival_relocated": sum(1 for r in ROWS if r["survival"] == "RELOCATED"),
    "survival_descendant": sum(1 for r in ROWS if r["survival"] == "DESCENDANT"),
    "survival_unfiled": sum(1 for r in ROWS if r["survival"] == "UNFILED"),
    "survival_gone": sum(1 for r in ROWS if r["survival"] == "GONE"),
}

with open(OUT, "w", encoding="utf-8") as f:
    for r in ROWS:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
    f.write(json.dumps({"type": "counts", **counts}, ensure_ascii=False) + "\n")

print(json.dumps(counts, indent=2))
print("wrote", OUT)
