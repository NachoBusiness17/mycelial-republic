## Verdict

steal

## Evidence

The step pointer said site 1 is `_save_state` in mag/bonds.py; grep finds zero `_save_state` there. Correct home (matching pass e): mag/lane_runner.py lines 109-112, verbatim:

```python
def _save_state(lane: str, st: dict) -> None:
    p = LANES / lane / "runner_state.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
```

No seat write. Every caller (lines 348, 596, 722, 892, 1068) passes lane, so `lane` is the value source already in scope. Rows written are pass e's runner_state keys (inbox_offset, last_run, last_day, last_result; no seat).

Site 2: mag/context_pack.py bonds assembly, lines 598-601 verbatim:

```python
        if refresh_bonds or not BONDS_MD.is_file():
            ingest_bonds(write=True)
        bonds_text = load_bonds_text(max_chars=max_bonds)
        bj = load_bonds_json() or {}
```

No seat filter anywhere; bonds_meta (602-607) counts residual_bonds only, related_runs loads unfiltered. Copyable filter pattern in the same function, line 589: `roles = {r["role"]: r["model"] for r in (inv.get("roles") or []) if r.get("present")}`. The signature (537-549) has no seat parameter; the sizing must name that touch. Seat origin on bond rows: mag/bonds.py 292-294 pull `list_related_runs(last_n=6)`; mag/run_trail.py line 849 already stamps `seat=str(run.get("seat") or "local")` at close; bonds.py line 449 renders it.

WebSearch "seat scoped memory bonds agent" (2026-09-27): thin, reported honestly. Top hits: Deakin parliamentary letters, a corporate responsibility report, a parks official named Bonds. Fleet-canon "seat" is not industry vocabulary; the live external seam stays pass e's "per-agent memory scoping" direction.

## Steal or Vacuous

Two edits, pre-registered so the gated build is mechanical:

1. mag/lane_runner.py: insert `st.setdefault("seat", lane)` as the first body line of `_save_state` (after line 109). Field `seat`, value source the `lane` param. A true one-liner; all five call sites gain the field.

2. mag/context_pack.py: add keyword-only `seat: str | None = None` to the `build_context_pack` signature (line 548; default None keeps existing callers byte-stable), then one filter line after 601 in the line-589 comprehension shape: `bj["related_runs"] = [r for r in (bj.get("related_runs") or []) if not seat or r.get("seat") == seat]`. Site 2 is honestly a signature touch plus one line; seat-pure callers (the research pack) pass it.

Data half unchanged from pass e pricing: one research-lane trail close seeds a seat=research row into memory/runs/related_runs.jsonl; no code needed there, the writer already stamps seat.

## Falsifier

Amended falsifier restated against these diffs. After both edits land and one research trail close runs: a cold research reader receives trail head+tail, manifest.md, runner_state.json, and one seat-filtered pack. runner_state must carry `seat: "research"` (site 1 proof). The pack's related_runs section must be non-empty and contain only seat=research rows (site 2 proof; the seed run closes the empty-set trap pass d's original clause died on). A second independent reader must match name/state/purpose/last_result anchors. Falsified on anchor divergence, any seatless cited registry artifact, or any foreign-seat row surviving the pack filter.

## Bibliography

- watch/inbox/BURN_world-models-multi-agent_20260927_e.md (read 2026-09-27)
- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (read 2026-09-27)
- mag/lane_runner.py lines 99-134 (read 2026-09-27)
- mag/context_pack.py lines 537-626 (read 2026-09-27)
- mag/bonds.py lines 435-484 plus seat/related_runs grep (read 2026-09-27)
- mag/run_trail.py lines 823-855 (read 2026-09-27)
- WebSearch "seat scoped memory bonds agent", 2026-09-27, no relevant hits (thin)
