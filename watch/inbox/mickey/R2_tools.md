# LANE R2 — GATEWAY 4-TOOL WIRING, DONE (2026-09-11)

Deliverable: `mag/desk_tools.py` — one file, four callable organs, $0, stdlib only,
hermes_steering conventions (ROOT-relative paths, CLI + importable registry).

## THE FOUR

| tool | reads | verified |
|---|---|---|
| `biblio.query(subsystem)` | docs/ref/BIBLIOGRAPHY_MAP.md | "paging" → 35 rows; section-aware (KV OS / Chain / Lanes / Mesh / Eval / Corpus / unnamed-debt bullets); malformed rows keep `raw` |
| `invariant.sheet(subsystem, bucket)` | watch/INVARIANT_SHEET_V2.md | all six buckets parse: LAW 20, VERDICT 20, FALSIFIER 12, MEASURED 20, CONTROVERTED 15, MOVEMENT 10 (97 lines); net/agree/refute extracted per line |
| `kvos.stats(recompute=False)` | state/kvos_blocks.jsonl | manifest mode: 3,990 files, 9,019 blocks, 8,806 unique, 2.4% dup. `recompute=True` re-runs mag/kvos_block.py walk in-process (chain_file reused, not duplicated) |
| `fence.strike(target_text)` | any text | 6 hall-pattern detectors + charcoal counter, each finding cites its verbatim THE_FENCE.md line; verdicts: charcoal-found / cut-for-you / fenced / unmarked |

## WIRING

- Import path: `import desk_tools; desk_tools.run_tool("fence.strike", target_text=...)`
- Registry: `desk_tools.TOOLS` maps dotted names → callables (gateway plugs mag/mcp_http.py onto this)
- CLI: `python mag/desk_tools.py biblio|sheet|kvos|fence ...`

## BUGS CAUGHT AND FIXED DURING VERIFY

1. `_NET_RE.match` anchored past the `- ` bullet prefix → every sheet line skipped. Fixed: search + widened gate.
2. CONTROVERTED inverts its stat order (`[agree=3 vs refute=12 · net=-9]`) — second regex added.

## WHAT I DID NOT DO

- Did not touch mag/mcp_http.py — the gateway registration itself is the next lane; these
  are the callable bodies it wires (per spec: "they exist as callable code").
- Did not run `kvos.stats(recompute=True)` (manifest fresh; recompute walks 4k files).
- Fence detectors are honest heuristics — counts, never judgment; disclaimer embedded in every result.

— lane R2, zcode seat, 2026-09-11
