# THE FULL FILE-BY-FILE AUDIT — scheduling protocol (2026-09-08)
## Operator: "go through everything contained in our databanks, memory, skills, dashboards, dogfooding them all and creating the map of the territory. So we may design the next one."

---

## WHAT THIS IS

A systematic, exhaustive, file-by-file walkthrough of the entire fleet. Every
file opened. Every organ dogfooded. Every room loaded. Every card read. Every
demon invoked. Every result recorded. The output is a MAP OF THE TERRITORY —
what exists, what works, what's dark, what's prose, what's load-bearing,
what can be deleted.

This is not a summary. This is the dig.

---

## SCOPE — the four surfaces

| Surface | Path | File count (approx) | Method |
|---------|------|--------------------:|--------|
| **watch/** (cards, doctrine, protocols) | `watch/` + `watch/inbox/` | ~120 .md | Read every card, verify links, check falsifiers |
| **dashboard/static/** (rooms, tools, surfaces) | `dashboard/static/` | ~40 .html + .js | Load every page, screenshot, dogfood interactives |
| **mag/** (organs, organs, organs) | `mag/` | ~60 .py | Import test, CLI help, one invocation per organ |
| **memory/** (corpus, biography, seals, runs) | `memory/` | ~200+ files | Inventory, classify, flag orphans, check seals |

Plus: `configs/`, `handoff/`, `docs/`, `scripts/`, `artifacts/`, `state/`

---

## THE AUDIT PROTOCOL (per file)

For every file encountered, record:

```
{
  path:           "...",
  exists:         true/false,
  loadable:       true/false,       // for .py: imports clean
  renderable:     true/false,       // for .html: loads without errors
  dogfooded:      true/false,       // for interactives: exercised
  organ_type:     "mirror|recorder|scorer|tavern|primer|canon|...",
  invariant:      "the one rule that never changes",
  falsifier:      "what breaks if you remove it",
  week_of_origin: "W1|W2|W3|W4|W5|W6|pre-history|unknown",
  status:         "LIVE | STAGED | DARK | PROSE | ORPHAN | DEAD",
  lessig_verdict: "EXECUTABLE | PROSE | FOLKLORE",
  notes:          "..."
}
```

---

## THE DOGFOOD SUB-CHECKS (per type)

**For .html rooms:**
- Load in browser, check for JS errors
- Exercise the core interaction (click, type, key)
- Verify the proof organ (prediction gate, fingerprint, etc.)
- Screenshot at peak state
- Verify the falsifier (what breaks when you break it)

**For .py organs:**
- `python -m mag.<organ> --help` (CLI alive?)
- One real invocation with real inputs
- Check output artifact exists and is non-trivial
- Verify the invariant (the law stated in the docstring matches the code)

**For .md cards:**
- Read fully
- Check every file path referenced (does it exist?)
- Check every falsifier (is it testable?)
- Check the tri-state (is every claim marked?)
- Check for stale pointers (files that moved, links that died)

**For memory/biography/:**
- Verify knot chain integrity (prev_hash → step_hash)
- Check for orphaned knots (no parent)
- Check for duplicate knots (same content, different hash)
- Flag the cold shelf (8 bodies, waiting for the dawn read)

**For dashboard/static/ nav.js:**
- Verify every nav entry resolves to a live file
- Check for dead links
- Verify the two nav lists are in sync

**For configs/:**
- Verify every YAML parses
- Verify every referenced key exists in .env (name only, never value)
- Flag any credential material that shouldn't be in configs

---

## THE 11 AM SCHEDULE — batch by batch

The audit runs in batches. Each batch is one surface, walked file by file.
The Operator can watch any batch live. Results land in
`watch/audit/FULL_AUDIT_20260908/` as they complete.

| Batch | Surface | Est. files | Est. time | What we're looking for |
|-------|---------|-----------:|----------:|----------------------|
| 1 | watch/ (doctrine cards) | ~120 | 30 min | Stale pointers, dead falsifiers, unmarked claims, missing cross-refs |
| 2 | dashboard/static/ (rooms) | ~40 | 45 min | JS errors, broken links, dead organs, unverified proofs, orphaned pages |
| 3 | mag/ (organs) | ~60 | 45 min | Import failures, CLI breakage, stale APIs, unused organs, prose-that-should-be-code |
| 4 | memory/biography/ | ~156 | 30 min | Orphaned knots, broken chains, missing seeds, cold shelf status |
| 5 | memory/runs/ | ~200+ | 30 min | Stale salons, dead receipts, orphaned artifacts, uncounted failures |
| 6 | configs/ + state/ + handoff/ | ~30 | 15 min | Parse errors, missing keys, stale handoffs, orphaned directives |
| 7 | corpus/ | ~15 | 15 min | Shelf integrity, PD status, provenance |

**Total estimated: ~500 files, ~3.5 hours**

---

## THE MAP OF THE TERRITORY (the output)

When the audit completes, the output is:

1. **A table**: every file, its status, its type, its verdict
2. **A graph**: which files reference which (the dependency map)
3. **A kill list**: files that are DEAD (broken, orphaned, superseded) — safe to delete
4. **A prose list**: files that are PROSE wearing code's clothes — need typing or demotion
5. **A resurrection list**: files that are DARK but load-bearing — need wiring or pitching
6. **A map**: the territory, drawn from the files that survived, showing what the fleet
   actually IS (not what it says it is)

This map is what we use to design the next system. Not from vision. From evidence.

---

## THE RULE

**No file is exempt.** Every .py, .md, .html, .json, .yaml, .jsonl, .mp3, .webm,
.png gets touched. The Operator said: "go through everything contained in our
databanks, memory, skills, dashboards, dogfooding them all."

That includes the ugly files. The dead files. The files that were built at 3 AM
and never looked at again. Especially those.

The map of the territory is drawn from the territory, not from the map's own
claims about itself. That is the whole lesson of the audit discipline.

---

## READY TO FIRE

Batch 1 (watch/ doctrine cards) can start at 11:00 AM sharp, alongside the
Astra standing-wave fire (the prompt is staged, the window opens at 11:00).
Both can run in parallel — the audit reads while Astra writes.

Say GO and the dig begins.
