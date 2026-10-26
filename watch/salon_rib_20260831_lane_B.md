# Lane B — Query-Awareness, Losslessness, Silent Omission (salon, Mag seat)

## 1. Query-awareness: two cheapest frusta, existing TODAY
**A — active-goal pack.** `/mag/memory/context_pack_latest.md` (read 2026-08-31T00:24): "Use this pack only; do not reload full chat." Carries L0 policy + tip + leaves — the live-goal frustum for what to send. Read once, free.
**B — deterministic hash parent.** `/mag/memory/runs/party_subchain/head.json` (read): `parent_leaf_hash`→verkle tip, HEAD n=166 — a machine-checkable DRA bound, no prose.
Complement (not picked): `seat_corpus/latest.json` `prefer_order`/`never[]` is the *lane* frustum; A+B pick *what*.

## 2. Losslessness: already solved — pointer is enough
OpenClaw keeps full transcript at `/root/.openclaw/agents/main/sessions/*.jsonl`; `/board/openclaw_traj.jsonl` (read) writes only `ts, session, tokensBefore/After, compactedCount`. Party_subchain already dereferences by hash. **One convention: span `<path>:<start>-<end>`** (jsonl is line-addressed). Compaction entry = span + token count; dereference = read those lines → guaranteed lossless ReadArchive at ~$0.

## 3. Silent omission: what compaction NEVER drops
Never drop verbatim: **operator-authored + operator-confirmed authority labels and red lines**. Live today in:
- `/root/.openclaw/workspace/SOUL.md` — red lines (l.10 secrets).
- `/root/.openclaw/workspace/MEMORY.md` — switchboard law (l.19 labels).
- `/board/*.md` PACK files — per-field law.
That is the never-drop list; nothing else is auto-protected.

## 4. Governance decay → structural rule (scope-stack analogue)
Map onto MEMORY.md l.19 labels. **Rule: label is not compaction-eligible; an `operator-confirmed` item may be replaced only by a verbatim *copy* of the label + pointer to the live item, never a paraphrase.** Rewording inside an open scope (party chain / in-flight edit) is illegal — the divergence-5 grammar fix. Only a later operator-confirmed action demotes it. Anchor survives; wording never does.

## Riddler gate (operator sharpened)
Decode-test checks **conclusion parity**, not token parity: `*.decoded.json` ops must reverse-map through `role_map`/`constraint_map` (read) to the same decisions/outcomes as `*.private.json`. Read alone, `*.public.json` reproduces the same conclusions while revealing neither source tokens (loss_report) nor personal data. Run at $0 on **ollama** (free local, seat_corpus `cost: electricity`); existing decoded files already run it.