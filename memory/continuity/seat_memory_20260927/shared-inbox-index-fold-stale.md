---
name: shared-inbox-index-fold-stale
description: RESOLVED 2026-09-16 — INDEX fold works via tolerant host copy
    scripts/index_fold_host.mjs (156 events -> 140 items); writers still append
    index_events.jsonl; validate baseline stays at 73
metadata:
  node_type: memory
  type: project
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

**RESOLVED 2026-09-16, SELF-HEALING since 2026-09-17** (drift patrol runs 3–4): `watch/inbox/INDEX.json` refolded live — and the daily patrol now runs the rebuild itself before reporting, so staleness should not re-accumulate. Latest fold: 176 events → 159 active items, derived 2026-09-17. The 14-day staleness (2026-09-02 fold) is closed.

The working tool is **`scripts/index_fold_host.mjs`** — the canonical `watch/inbox/REVIEW_index_fold.mjs` with three host fixes: (a) `INBOX_DIR` patched from `/board/inbox` (container-only; the container has no node in PATH — SHERPA's `docker compose exec mag node …` command is disproven) to the host `watch/inbox`, (b) a **tolerant reader** — malformed log lines are skipped + counted instead of `die()`-aborts (the blocker was line 94, a Sep-1 codex event in Python-dict syntax with `sha256: PENDING_CODEX, seq: NEXT`), (c) **root pinned to `/board/inbox` at BOTH emission sites** — `root: INBOX_DIR,` AND `root: meta.root,` (run 3's first host rebuild silently re-emitted the old INDEX's root, which had become a host `C:/…` path, spiking validate +35; the meta.root inheritance is the subtle one). Refold: `node scripts/index_fold_host.mjs rebuild`. Nonce-GAP warnings in output are cosmetic.

**Open wrinkle:** two fold homes now exist (canonical inbox artifact vs host copy in scripts/) — one should win before they drift. Never edit the append-only log itself.

**Why:** any seat running `mag.shared_surface validate` still sees ok:False with **73 pre-existing errors** (Sep-1 deleted items + 3 hash mismatches, baseline 2026-09-14, unchanged across every round) — that is NOT new breakage and NOT fold-related anymore.

**How to apply:** Writers still append `register` events to `index_events.jsonl` (seq/ts/op/file/sha256/class/purpose/writer/nonce, file paths as `/board/inbox/...`; log is truth, INDEX.json is derived). Re-run the fold after big event bursts (`node scripts/index_fold_host.mjs rebuild`), diff validate errors against the 73 baseline before assuming breakage. See [[drift-patrol-cron-a7c71ad1]] (the patrol now folds) and [[zcode-session-recovery-path]].
