# B7 — Canonical check wired into INTAKE_* writers

- Date: 2026-09-16
- Lane: B7
- Mission: wire `mag/link_library.py` canonical check into every code path that creates `watch/inbox/INTAKE_*.md`, annotating `links-canonical` + `links-duplicate-of` (annotate, never gate).
- Status: IN PROGRESS

## Writer inventory

Grep of mag/, scripts/, main.py (plus dashboard/, watch/, artifacts/ for completeness)
for code that creates `watch/inbox/INTAKE_*.md`:

**Finding: no code path in this repo writes INTAKE_*.md directly.** INTAKE cards are
filed by agent seats by hand (Write tool / shared surface contract). Every code
reference to `INTAKE_` is a READER/COUNTER:

| File | Role |
|---|---|
| mag/gene_pool_feeder.py | counts INTAKE cards for a residual gene (read-only) |
| mag/fleet_intel.py | globs `INTAKE_*.md` sorted by mtime (read-only) |
| mag/disposition_sweep.py | regex classifier, INTAKE_ is a transduce tag (read-only) |
| scripts/hunger_ledger.py (+ watch/cage_bin copy) | counts new INTAKE cards/day (read-only) |
| scripts/calcifer_receipt_backlog.py | globs `INTAKE_*{day}*.md` receipts (read-only) |
| scripts/edg_compiler.py | INTAKE id normalization mention (read-only) |
| mag/transfer_gate.py, mag/fuel_feed.py, mag/lattice_distance.py, mag/rotation_harness.py | docstring/provenance references only |
| artifacts/backfill_links_20260916.py | B6 backfill: reads INTAKE cards → LINKS.jsonl (already wired to the ledger) |
| main.py | has `links add/check/dupes` CLI (no card writer) |

**The one code organ in the intake-creation chain:** `mag/paste_pipeline.py` STEP 1
"INGEST-WRITE intake scaffold card -> watch/inbox/" — the paste→intake-card creator.
It writes the scaffold card (to memory/runs/paste_pipeline/ because watch/ is not
bind-mounted into the cage; the seat files it host-side). This is the highest-traffic
code path where links enter the intake pipeline (its step-2 triage rows ARE the pasted
URLs), so it is the writer wired below.

## Wired

`mag/paste_pipeline.py` — step 1 INGEST-WRITE (the intake scaffold card creator, the
only code path that builds intake card content).

- New `_canonical_footer(text)` helper: extracts unique http/https URLs from the paste
  digest, and per URL — `canonical = link_library.canonicalize(url)`;
  `hit = link_library.known_canonicals().get(canonical)` — then appends footer lines
  `links-canonical: <canonical>` and `links-duplicate-of: <first url or empty>`.
- Called in `run()` immediately before `card_path.write_text(...)`: pre-write annotation.
- Annotate, never gate: the whole per-URL check is try/except; import failure degrades
  to a "ledger unavailable … links unannotated" line; a bad URL degrades to
  "links-canonical: (unresolved: …)". A ledger outage can never block intake.
- Bonus verified 2026-09-16: tracking params (s=20, utm_*, t) are stripped in the
  canonical form, so a ?s=20 re-paste of an already-filed post annotates as duplicate.

## Not wired / reasons

| Code path | Why not wired |
|---|---|
| mag/gene_pool_feeder.py, mag/fleet_intel.py, mag/disposition_sweep.py, scripts/hunger_ledger.py (+cage_bin copy), scripts/calcifer_receipt_backlog.py, scripts/edg_compiler.py | readers/counters only — no card write to annotate |
| mag/transfer_gate.py, mag/fuel_feed.py, mag/lattice_distance.py, mag/rotation_harness.py | docstring/provenance mentions only |
| artifacts/backfill_links_20260916.py | B6 one-off backfill, already writes to the ledger with duplicate detection; retired after its run |
| main.py `links add/check/dupes` | already the ledger CLI itself (add_urls dedupes via canonical) |
| Agent seats filing INTAKE cards by hand | no code to wire; interim habit: run `python -m mag.link_library check <url>` before filing (exit 1 = already on file); the paste_pipeline footer now covers the scripted path |

## Smoke

Command (repo root, Mag venv):
`python -m mag.paste_pipeline run --paste "https://x.com/NachoQuixotic/status/2071636215309156788" --steps 1 --title "B7_SMOKE"`

stdout verbatim:
```text
PASTE PIPELINE steps 1-1
  step  1 [INGEST] EXECUTED: intake scaffold card (paste bytes -> watch/inbox card)
card: C:\Users\foste\Documents\projects\local_sovereign_agent\memory\runs\paste_pipeline\B7_SMOKE_https_x_com_NachoQuixotic_status_2071636.md
```

Card footer verbatim (memory/runs/paste_pipeline/B7_SMOKE_https_x_com_NachoQuixotic_status_2071636.md):
```text
## Link canonical check (link_library — annotate, never gate)
- https://x.com/NachoQuixotic/status/2071636215309156788
  links-canonical: https://x.com/NachoQuixotic/status/2071636215309156788
  links-duplicate-of: https://x.com/NachoQuixotic/status/2071636215309156788
```
The URL is on LINKS.jsonl (ledger check: known=true, writer "zcode-xmine-20260916"),
and the card correctly annotates it as a duplicate of the first filing. Smoke card left
in memory/runs/paste_pipeline/ (cage scratch) — intentionally NOT filed into
watch/inbox to keep the shared surface clean.

Status: DONE
