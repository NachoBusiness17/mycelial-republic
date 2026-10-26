---
name: provider-chat-capture-cap
description: main.py provider-chat truncates the captured answer text at exactly 4,000 chars (4,004-byte log) — long answers die mid-stream; use smaller-output forms or split the episode
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_727c2fc5-be79-4f45-a7a4-229c471b2b9b
---

`main.py provider-chat --provider openrouter --model <model> "$(cat prompt.txt)"` truncates the returned/logged answer at exactly **4,000 chars of text (4,004-byte log file)** — confirmed 3× identically on 2026-09-15 (I6 full 20-vignette form died mid-table at V16/V13/V14 across original + 2 retries; file size 4,004 bytes every time, JSON unterminated, no usage block at tail).

**Symptoms:** raw log fails `json.loads` ("Unterminated string"); `tail` ends mid-answer; no `"usage"` block. Retries do NOT help — it's a capture cap, not transport.

**Workarounds that worked:**
- Re-route to a smaller-output form — the I6 card's own §6g desk sub-form (8 vignettes instead of 20) completed fine (3,431 bytes) and is the card-sanctioned qa path.
- **Terse-output constraint in the prompt works:** "HARD OUTPUT CONSTRAINT: keep the whole answer card under 3,500 characters" + compact row formats (`<index> OK` / `<index> BAD <reason>`, exceptions-only lists) — I1 run3 and I3 run2 captured whole with this (receipt the constraint as a capture mitigation in the desk grade).
- Short answers (<4,000 chars of text) capture whole: I1 2,058 / I4 1,767 / I5 1,703 / I2 (~4.9KB text but reported fine that window — cap behavior varied once; always check parse).
- Raw logs that fail to parse: `json.loads(raw, strict=False)` handles embedded control chars; a truly unterminated log means the cap fired. Regex fallback for unterminated logs: `re.search(r'"text": "(.*?)",\n  "provider"', raw, re.S)` + unicode_escape decode.
- **Second failure mode (distinct):** `"ok": false, "error": "empty content — reasoning model consumed the budget (max_tokens too small; raise it or disable thinking)"` — free-lane reasoning exhaustion returns EMPTY content; plain retry (same request, per retry law) landed it.

**Working episode recipe (free flash, $0):** `.venv/Scripts/python.exe main.py provider-chat --provider openrouter --model "inclusionai/ling-3.0-flash-sante:free" "$(cat prompt_file)" > raw.log` → extract `json.load(raw)['text']` → grade vs the desk key → append `==== DESK GRADE ====` to the log. Night total: 8+ graded episodes. OpenRouter budget after the full session: 182/200 calls, ~357K/500K tokens remaining. Windows argv limit ~32,767 chars — long prompts via `$(cat file)` must stay under it (30,943-char prompt failed rc=126; 28,971 passed), and relative script paths depend on cwd — use absolute main.py paths.

Related: [[astra-repair-lane-20260915]], [[bash-hook-guard-workarounds]], [[no-overnight-deferral]].
