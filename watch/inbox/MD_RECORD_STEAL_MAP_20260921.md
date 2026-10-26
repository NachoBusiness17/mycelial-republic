# MD RECORD STEAL MAP — who else solved "records that can't lie" (2026-09-21)
**Operator GO:** "go nuts steal what is worthwhile map it to our systems"

| # | who | what they solved | our steal | status |
|---|---|---|---|---|
| 1 | Drug industry (21 CFR Part 11, ALCOA+) | lab notebooks with legal teeth | the checklist IS the audit: Attributable/Contemporaneous/Original/Accurate/Enduring tested per run | **LIVE** — md_record_audit v2, RECORD CLEAN at close |
| 2 | Diary databases (event sourcing, Datomic) | append-only facts, time-travel queries | state_asof.py — "what did the estate know on date D" | **LIVE** |
| 3 | AI flight recorders (LangFuse/W&B/Braintrust) | every model call: exact request+answer+cost+time | prompt-fingerprint field on provider_usage rows | **QUEUED** — writer lives in hermes install (operator-side, one field) |
| 4 | Programmers' daily seals (git signed tags) | provable day-state, tamper-evident | windowseal event each close (hash of handoff at commit) | **LIVE** — first seal this close |
| 5 | Perfect recipes (Nix) | reproducible builds from locked inputs | cathedral_build.lock.json (module hashes → html hash) | **LIVE** |
| 6 | Ticket stubs (OpenTelemetry) | one reference number across desks | trace id propagated into peer handoffs | **QUEUED** — next peer_handoff touch |
| 7 | Library cards (Zenodo/CERN) | citations bound to exact versions | cite = path+sha+line habit in decode cards | **LIVE (habit)** |
| 8 | Game-of-record (kifu, PGN) | whole sessions replayable from compact rows | replay-from-kifu test as the smoke bar | **LIVE (walker kifus)** |

Ground truth: 5 live, 2 queued, 1 habit. Audit verdict at close: RECORD CLEAN.

## Seal-hook wiring (verified live 2026-09-22, mining lane 19)

`tools/md_record_seal.py` (rib.md.record.v1 teeth, two modes) is registered in the
**ZCode hook channel — `C:/Users/foste/.zcode/cli/config.json` → `hooks.events`**,
both on matcher `Write|Edit`:

- **gate** → `hooks.events.PreToolUse[0].hooks[1]` (config.json:38): `python ".../tools/md_record_seal.py" gate`, timeout 15 — refuses >8 MB content writes into the durable roots (hard-drive guard).
- **seal** → `hooks.events.PostToolUse[0].hooks[0]` (config.json:51): `python ".../tools/md_record_seal.py" seal`, timeout 15 — appends one deduped `op=autoseal` line (path, bytes, sha256 ≤256 KB) to `watch/inbox/index_events.jsonl`.

Proof it is live, run 2026-09-22: `grep -n md_record_seal C:/Users/foste/.zcode/cli/config.json` → lines 38, 51; a single test Write (`watch/inbox/LANE19_SEAL_HOOK_TEST_20260922.md`) appended exactly one autoseal line (`index_events.jsonl:1361`, 1360→1361 lines, autoseal 33→34). No re-registration needed.

- **T-Mem (EMNLP 2026, Tencent, open source)** - associative-recall memory: each memory ships with a TRIGGER predicting when it will matter, matched at query time before similarity search. Steal: our kifu/md rows could carry a trigger field so the fleet recalls by situation, not just keyword. Filed 09-21 from operator link.
