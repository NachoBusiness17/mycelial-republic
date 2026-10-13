# BOOT BUDGET CARD

Boot context is **budgeted per job mode**, never "dump the chat history". A seat loads
a short ordered doc chain, then asks for exactly one mode-sized context pack, and owes
one filed job before it ends.

## The start-here card (estate shape)

```text
LOAD doc1 → doc2 → doc3 → doc4 → AGENTS.md     (the estate's 5-doc chain; yours will differ)
Run: <one command> context-pack                 (estate: mag.cmd context-pack)
One job. FILE before end.                       (the deadline rule)
```

LLMs get the framework docs first; humans get the dashboard/proposal docs — same card,
two entry lines (LOAD.md:3-5).

## MODE_CONFIG — the budget table

Machine copy: `configs/mode_budgets.json`. Six modes; per-mode caps on each context
layer (brief / bonds / live / total chars) plus include-flags deciding which layers
enter at all.

| mode | max_brief | max_bonds | max_live | max_chars | layers on |
|---|---|---|---|---|---|
| janitor | 400 | 500 | 0 | 1,200 | none (compact nervous) |
| route | 600 | 800 | 200 | 1,800 | resonance, skills, coordination |
| build | 900 | 1,200 | 400 | 5,500 | + trail, ijl, build, scope |
| audit | 600 | 600 | 200 | 7,500 | trail, skills, coordination, build |
| plan | 1,200 | 1,600 | 600 | 11,000 | resonance, skills, ijl, heat, coordination, mirror-clue (no trail) |
| full | 1,200 | 1,600 | 800 | 4,500 | everything |

- The spread is the point: a janitor seat gets **1,200 chars**; a planning seat gets
  **11,000**. Same code path, budget chosen by job mode.
- Normalize rule: unknown/empty mode falls back to **`full`** — never an error, never a
  crash, always a valid pack.

## Receipt

- LOAD.md:3-13 (estate) — LLM/human split :3-5, the card :7-13 — read this session.
- mag/context_pack.py:1, :15, :18-112, :115-117 (estate) — "never full chat",
  VALID_PACK_MODES, MODE_CONFIG, normalize fallback — read this session (head only;
  the rendering functions below line ~125 were NOT examined — scope note preserved).
