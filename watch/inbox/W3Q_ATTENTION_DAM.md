# W3Q — the attention dam (Mickey17 W3, 2026-09-30)

**Lane:** W3 · **Files owned:** `tools/attention_dam.py` (new), `tests/test_attention_dam.py` (new) · **No commit made.**

## Telemetry finding (read first, confirmed)

`memory/attention.md` floods with a `### Session record ready (first)` block
every ~90s from `mag/biography.py` `_ping_attention` (one ping per biographer
cycle, prepended newest-first). Real alerts — `[priority][probe-alarm]`
provider_probe DOWN mistral / QUOTA-DEAD cerebras lines, the 2026-09-29
`CENSUS-PATROL: COLLECT-DRIFT` verdict block, `[priority][gate-canary]`
DEAD/BLIND canary lines — sank under hundreds of session lines.

## The dam

1. **Classification** (`classify`): blocks split on markdown `---` separators
   plus the harness-owned sentinel boundary (`<!-- attention:alerts-preserved-below -->`,
   `mag/act.py` — alert lines glue directly after the last record body, so the
   split there recovers that block). Noise is a CLOSED class: a block is
   noise only if it carries a `### Session record ready (first|amended)`
   heading AND no signal marker (`[priority]`, probe-alarm, patrol,
   gate-canary, DOWN, DRIFT, sentinel). Everything else — unknown headings,
   mixed blocks — stays. Signal-by-default.
2. **One pass** (`dam_pass`): noise blocks MOVED verbatim to
   `memory/attention_archive_20260930.md` (move, not delete); signal kept in
   order; sentinel intact so `evict_for_prepend` / bottom-appenders keep
   working; pointer note left in the attention.md header naming the archive.
3. **--stats**: read-only signal:noise report; a pass prints before AND after.
4. **Idempotent**: zero noise + pointer present → writes nothing; back-to-back
   runs leave both files byte-identical. Later floods archive only the new
   blocks (append + run marker in the archive).

## Real pass (2026-09-30T02:30:17Z)

| | before | after |
|---|---|---|
| attention.md total lines | 1123 | 43 |
| signal | 38 lines / 2 blocks | 38 lines / 2 blocks (0 lost) |
| noise (session records) | 722 lines / 90 blocks | 0 / 0 |
| ratio signal:noise | **1:19** | **38:0** |

- 90 blocks / 722 lines archived to `memory/attention_archive_20260930.md`
  (1001 lines with header/separators; all 90 session headings verified in
  archive, 0 remain in attention.md).
- Signal verified kept: all probe-alarm DOWN lines, the COLLECT-DRIFT patrol
  block, all gate-canary DEAD/BLIND lines, sentinel intact.
- Second immediate run: `archived 0 noise blocks (0 lines)`, file byte-stable.

## Tests

`tests/test_attention_dam.py` — 7 passed (fixture flood: signal preserved,
noise archived verbatim, pointer left; ratio reported before/after;
idempotence byte-identical; re-flood archives only new blocks; conservative
mixed-block keep; --stats read-only; exact stats/ratio arithmetic).
All via tmp-path redirection; no real memory/ file touched by tests.
