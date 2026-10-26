## Verdict

steal

## Evidence

Emitter applied, mag/context_pack.py line 628, one physical line inserted into the existing bonds_meta literal, matching the line-623 filter's inline comprehension shape:

```python
"related_by_seat": {k: sum(1 for r in bj["related_runs"] if str(r.get("seat")) == k) for k in sorted({str(r.get("seat")) for r in bj["related_runs"]})},
```

Context, current line numbers byte-read 2026-09-28: 622 `bj = load_bonds_json() or {}`; 623 the landed seat filter, unchanged; 624-630 bonds_meta now carries session_id, n_loops, n_bonds, related_by_seat (628), path; the pack dict emits `"bonds_meta": bonds_meta` at 897. The counts derive from the exact rows line 623 produced, so the filter is observable in emitted output: a seat-passing pack shows only passing-seat buckets; an unfiltered pack shows all seats, including a "None" bucket for seatless rows.

Parse: `.venv/Scripts/python.exe -c "import ast; ast.parse(open('mag/context_pack.py').read())"` printed `context_pack.py: parse OK`. Grep confirms 628.

Caller check: repo-wide grep finds mag/brief_local.py:210-226 holding a same-named local built from ingest_bonds, a different surface, not a pack consumer. In-repo readers of the pack's bonds_meta: dict emission at 897 and the wholesale render at 1107 `f"- bonds_meta: {p.get('bonds_meta')}"`, so the new field appears in that rendering too. The field is additive; no existing caller breaks.

Honest line drift: the e receipt named bonds_meta at 604-609 and the return dict at 865; after the g edits landed, byte truth is 624-630 and 897.

## Steal or Vacuous

Fleet adopts the one-line emitter as the bonds_meta seat-count surface for NPC=SEAT: every pack now publishes related_by_seat, counts over the same rows the seat filter acts on. The 623 filter is no longer in-memory only; a cold reader byte-checks bonds_meta.related_by_seat instead of text-grepping the bonds field. No new reader surface, no fallback branch, no new imports, one line. Bonds are now seat-countable at the pack boundary.

## Falsifier

Pending precondition unchanged: one research trail close seeds a seat=research row (the g receipt names mag/run_trail.py as the seat-stamping writer; not re-byte-read this pass, so that stays owed). Then a cold reader runs build_context_pack(seat="research") and reads bonds_meta.related_by_seat: must equal {"research": n} with n >= 1; any "None" or foreign-seat bucket is a falsifier smell. The return bonds field must show a Related runs section where every row reads seat=`research`. A second independent reader applies the 623 predicate to bonds.load_bonds_json() and must match name/state/purpose/last_result anchors with the text rows. runner_state.json must carry seat=research. Falsified on anchor divergence, a foreign-seat bucket in related_by_seat, or a seatless cited registry artifact.

## Bibliography

- watch/inbox/BURN_world-models-multi-agent_20260928.md (read 2026-09-28)
- watch/inbox/BURN_world-models-multi-agent_20260927_g.md (read 2026-09-28)
- mag/context_pack.py lines 1-40, 560-660, 845-905, plus bonds_meta grep trace (read 2026-09-28)
- mag/brief_local.py bonds_meta grep trace (read 2026-09-28)
- WebSearch "pack metadata emitter counts multi-agent shared state 2026", 2026-09-28, thin: closest snippet hits [IETF AOCL draft, context bundle as shared state](https://datatracker.ietf.org/doc/draft-cowles-aocl-01/) and [activegraph-packs, pack counts metadata](https://github.com/yoheinakajima/activegraph-packs), snippet-level only, nothing read in full
