## Verdict

steal

## Evidence

Edit 1, mag/lane_runner.py, `_save_state` now lines 109-113 verbatim:

```python
def _save_state(lane: str, st: dict) -> None:
    st.setdefault("seat", lane)
    p = LANES / lane / "runner_state.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
```

Local names `lane`/`st` matched pass f byte-exact; diff applied as sized, line 110 is the insert.

Edit 2, mag/context_pack.py: line 549 `seat: str | None = None,` appended after `fast: bool = False,` in the keyword-only `build_context_pack` signature; line 603 `bj["related_runs"] = [r for r in (bj.get("related_runs") or []) if not seat or r.get("seat") == seat]` inserted after line 602 `bj = load_bonds_json() or {}`, the line-589 comprehension shape. Default None keeps existing callers byte-stable; the signature `*` makes all calls keyword-only.

Parse: `.venv/Scripts/python.exe -c "import ast; ast.parse(...)"` printed `lane_runner.py: parse OK` and `context_pack.py: parse OK`. Grep confirms lines 110 / 549 / 603.

Honest preconditions, byte-checked 2026-09-27 ~21:05 EDT: research lane `runner_state.json` last_run `2026-09-28T00:53:27.904263+00:00` carries no seat, but its mtime 20:53:27 EDT predates the edit at 21:04:36 EDT, so no contradiction; the next lane run in a fresh process is the site-1 proof (a resident process holds pre-edit bytecode). `memory/runs/related_runs.jsonl` now 13 rows: 12 seat=local, 1 seat=grok_tui, zero seat=research. The pack return dict (line 860+) emits `bonds` (bonds_text), `bonds_meta`, `open_loops`; it has no dedicated related_runs emitter today, so the line-603 filter acts at the load site: any seat-passing reader of `bj` gets filtered rows, and the falsifier run must name its reader surface.

## Steal or Vacuous

Fleet adopts both diffs as the gated build for NPC=SEAT identity persistence: every lane's runner_state registry row now carries `seat` defaulting to the lane (site 1), and the pack assembly filters bond rows by seat when a seat passes, unfiltered otherwise (site 2). Bonds are seat-DNA-capable; the runner registry and the pack load site are now seat-pure at write and read. Remaining gap is data, not code: one research trail close seeds a seat=research row (the writer mag/run_trail.py already stamps seat at close).

## Falsifier

Pending, unchanged in substance: one research trail close seeds the seat=research data (zero such rows exist today, confirmed). Then a cold research reader receives trail head+tail, manifest.md, runner_state.json (must show seat=research), and one seat-scoped pack whose related_runs is non-empty and seat=research only; a second independent reader must match name/state/purpose/last_result anchors. Falsified on anchor divergence, any seatless cited registry artifact, or any foreign-seat row surviving the filter. Reader surface for the pack clause is named at run time (see Evidence emitter note).

## Bibliography

- watch/inbox/BURN_world-models-multi-agent_20260927_f.md (read 2026-09-27)
- watch/inbox/BURN_world-models-multi-agent_20260927_e.md (read 2026-09-27)
- mag/lane_runner.py lines 95-139 (read 2026-09-27)
- mag/context_pack.py lines 537-640 and 840-900 (read 2026-09-27)
- queue/lanes/research/runner_state.json + mtimes (read 2026-09-27)
- memory/runs/related_runs.jsonl seat grep (read 2026-09-27)
- WebSearch "per seat bond scoping multi-agent shared world model 2026", 2026-09-27, zero relevant hits, no links (thin; only a brainscape GRE flashcards noise hit)
