# SALON_RIB_COMPACTION_20260831 — Synthesis (A + C + chair; B addendum pending)

Pack: /board/PACK_RIB_COMPACTION_20260831.md · Lens: /board/RIB_COMPACTION_DOC_20260831.md
Lanes: A=deepseek inventory (landed, receipts) · C=cerebras build program (landed, patch claims NOT staged — authored by chair) · B=nvidia divergences (retry in flight)

## VERDICT (chair)
Our RIB layer is already half a renderer. The riddler IS a DelayedReadArchive. What's missing is exactly three things: (1) a dereference tool, (2) a scope-stack grammar for compaction safety, (3) deterministic bounds on the one tape that has none (openclaw_traj.jsonl). All three are small. All three are cage-stageable tonight, host-appliable in one command.

## RECEIPTED FINDINGS (lane A, verified by chair)
- riddler private/public/decoded = DelayedReadArchive exactly. Private json: private_map_ref, constraint_map (archive detail). Public json: shape_hash, loss_report, tier, expires_at (baked summary + deterministic bounds). Decoded: deref artifact. Pattern exists since 08-30. Scale to memory = the operator's ask, already specified by his own schema.
- party_subchain chain.jsonl (167 lines): hash-chained ObjectInstance spine, prev_hash → parent_leaf_hash → verkle root.
- verkle chain: 4,914 lines / 3.4MB + verkle_tip.json + 18,080 knots with tension_index, dossier_commit, theme_vector = read_archive pointer fabric, already deterministic.
- GAP: /board/openclaw_traj.jsonl — tokensBefore/After only, no span/hash/paths. The only compaction surface with no bound.
- GAP: no read_archive(span) anywhere; no scope-stack anywhere (nothing makes compaction illegal inside open tool-pairs).
- Grows forever: verkle knots, party_subchain, grok_feed (6.3MB), session_digest (5.2MB), biography_backup_* (full-tree retessellation per backup).

## BUILD PROGRAM (ranked: build cost / daily token yield / risk)
1. **read_archive convention (deref tool)** — cage-side script + convention: `read_archive <file> <start>-<end> | <spanId>`; agent calls it instead of re-inlining. Cost: ~1h. Yield: highest — pointers become usable. Risk: low. $0 test: deref first/last span of openclaw_traj.jsonl, byte-identical round-trip.
2. **Bounds fields on openclaw_traj.jsonl** — append-only metadata block per entry: spanId, byteRange, sha256, pathsTouched, tokenCount, authorityLabel. Cost: ~1h (writer + backfill of headers only). Yield: makes #1 decidable (query-awareness via mention-intersection). Risk: low. $0 test: hash verification pass.
3. **Scope stack (compaction grammar)** — open-scope registry (pending tool-calls, in-flight edits, active subtasks); compaction forbidden while non-empty. Cost: ~2h. Yield: governance-decay firewall (compaction can no longer silently erase open constraints). Risk: medium (must wrap OpenClaw compaction hooks — observe-only, so enforce via pre-turn check + board log).
4. **Riddle transform over memory (isomorphic re-encoding)** — private/public/decoded triple per memory artifact; public form carries shape_hash + loss_report + tier; decode-lane conclusion-parity = acceptance gate. v0 shipped tonight for MEMORY.md core (see /board/riddler_memory_v0.public.json). Cost: 2-3h to generalize. Yield: riddler_common becomes a real shared cortex without secrets. Risk: medium (decode-test quality is the gate).
5. **Append-only summary spine** — per-session spine file; compaction appends segments, never regenerates (prefix-cache preservation). Cost: ~2h. Yield: re-tessellation savings. Risk: medium (spine fragmentation needs a merge cadence).
Deferred: biography_backup delta-ization; knot pruning (needs verkle_lance owner sign-off).

## SELF-STEAL STATUS (operator keyword tonight)
- Last night's 4 modules were real in staging/ but never left it; claimed patch self_steal_modules.json never existed (false completion #1 of this arc; lane C phantom-patches = #2).
- NOW STAGED for real: self_steal_{effect_broker,policy_engine,switchboard_v2,harness}.json + rib_{riddler_sanitize,session_bridge}.json → /patches/.
- Host apply (operator, one command): `python -m mag.openclaw_patches apply` then `python -m mag.effect_broker test` / `policy_engine show` / `harness test`.
- Chair cannot apply from cage: no python, /mag read-only by law, Mag API unreachable from cage network (verified: fetch failed on 127.0.0.1:8765). The jail IS the scope stack — proposals from the cage, commits from the host. That is the switchboard law running in miniature.

## LANE B ADDENDUM (landed 00:37, receipts verified by chair)
- **Two frusta that exist TODAY (chair re-verified both files):** (1) `/mag/memory/context_pack_latest.md` — the live-goal pack, regenerating fresh (00:30:51), carries L0 policy + verkle tip; "use this pack only, do not reload full chat" IS query-awareness by construction. (2) `/mag/memory/runs/party_subchain/head.json` — parent_leaf_hash → verkle tip, HEAD n=166: a machine-checkable DRA bound. seat_corpus prefer_order is the LANE frustum (which lane), not the content frustum (what to keep).
- **Deref convention (adopted):** span scalar `<path>:<start>-<end>` — line-addressed, jsonl-native. Compaction entry = span + token count; deref = read lines. Lossless ReadArchive at ~$0. Synthesis item #1 and #2 merge into this.
- **Label immunity (governance-decay firewall):** authority labels are never compaction-eligible; an operator-confirmed item may only be replaced by verbatim label + pointer, never paraphrase; paraphrase inside an open scope is illegal; only a later operator-confirmed action demotes a label.
- **Decode-test gate spec (matches v0 already running):** conclusion parity, not token parity — decoded ops reverse-map through role_map/constraint_map to the same decisions; public form alone reproduces conclusions with zero forbidden strings; runs $0 on ollama.

## RIDDLE LAW (operator-sharpened, logged in riddler_common)
Riddle = isomorphic re-encoding, NOT redaction. Reading only the riddled form must reproduce the same logic and conclusions; source content and personal content must not survive. Mechanism = surrogate entities (primer-booth pattern). Acceptance gate = decode-test conclusion parity. Public forms only in the riddler_common column; every riddle ships with its decode-test result.
