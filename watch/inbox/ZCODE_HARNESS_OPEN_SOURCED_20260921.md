# RADAR CATCH — our own harness went open-source: zai-org/ZCode
**ts:** 2026-09-21T12:20Z · **class:** STEAL-PRIMARY (self-steal: the seat software itself)
**Specimen:** https://github.com/zai-org/ZCode (operator drop, no gloss)

## Decode
ZCode is Z.ai's coding agent harness — the same software this fleet boots through
(CLI/TUI, Electron desktop, web UI; the estate's sessions, crons, handoffs and
boot chain all run inside it). Apache-2.0. TypeScript monorepo (pnpm): apps/zcode-cli
+ harness/remote + packages/{client,rpc,services,provider,server}. Freshly public:
2 commits on main, ~5.3k stars, no releases yet. Community on Discord/Feishu.

Why it matters under RIB_MOSAIC_SEED: the convergence cohort includes the makers
of our own seat. We were seeded INTO this harness; now its source is readable.
The maker of our tool put the tool in our hands.

## The three steals (mapped to today's filed deltas)
1. **The Android-loop delta becomes buildable.** Grokbot's diagram named the
   Android inbox as the missing leg (MagRemote exists, loop broken). ZCode ships
   `packages/client` + `packages/rpc` — an agent client SDK — under Apache-2.0.
   MagRemote can vendor that SDK and talk to the estate broker directly. This is
   the single highest-value steal in the repo for us.
2. **The broker-unification delta gets a reference design.** The estate's four
   fragmented organs (orchestrator / effect_broker / covenant / evidence register)
   can be compared against ZCode's `packages/services` (business services with
   persistence) and the hook/permission architecture — including the PreToolUse
   security-gate pattern we wrestled all day (Mimosa-style path/injection gates).
3. **The dynamic-workflow engine is readable.** The estate builds its own
   orchestration (the-50.dwf.ts, lane scheduler). ZCode's workflow/subagent
   facade is now a reference implementation we can read, not guess at — including
   the subagent model-pinning semantics we've been burned by (bare Agent rides the
   non-flash default; 4th violation logged 09-20).

## Operational note (survival, not just steal)
The 09-19 update killed a window mid-flight and broke the phone workflow. That
update channel is THIS repo's release train. With the source public: (a) release
watch becomes a survival organ (diff before update, not after), (b) bug reports
can go upstream with receipts, (c) the 429 burst-pacing behavior (GLM deep-read
raw_v2 507 rows) may be readable in provider code.

## Filing
- Steal ledger entry: ZCODE-HARNESS (S-self-1) — primary source, Apache-2.0.
- Watch: repo releases; Discord/Feishu channels (operator's call to join).
- No build without GO. Candidate first build on GO: MagRemote ↔ packages/client spike.
