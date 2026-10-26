# T2SP2_spec_shared_surface (anthropic/claude-opus-5.5, turn 1, channel: content)

# docs/ref/SHARED_SURFACE_SPEC.md

```
spec: shared_surface.spec.v1
status: PROPOSAL (lands as a reference doc; its authority source, the contract, is itself registered class PROPOSAL, see 0.3)
target_path: docs/ref/SHARED_SURFACE_SPEC.md
sources: watch/inbox/SHARED_SURFACE_CONTRACT.json (cited "C"), watch/inbox/INDEX.json (cited "IX")
```

---

## 0. Conditions of this spec

### 0.1 Citation convention

- **C:N** is a line in `watch/inbox/SHARED_SURFACE_CONTRACT.json`. Lines are counted from the evidence rendering, which is 92 lines with one key or array element per line. Quoted bytes follow every citation. If the on-disk file is laid out differently, the line numbers are UNVERIFIED and the quoted bytes govern.
- **IX:N** is a line in `watch/inbox/INDEX.json`. Lines 1 to 15 are counted from the evidence rendering.
- **IX items[path=P]** cites an item inside the `items` array. The line number for each item is UNVERIFIED, because the evidence was truncated at 400000 chars and I did not count lines inside `fold_warnings` or `items`. The quoted bytes govern.
- **IX fold_warnings[...]** cites a warning string by quoting it.

### 0.2 Instrument, moment, context

| Item | Value | Source |
|---|---|---|
| Instrument | The fold that produced INDEX.json. Its entry point is UNVERIFIED. | IX:5 `"Ethereum fold pattern, EXP-002A"` |
| Moment | `"derived_at": "2026-10-01T18:41:32.593Z"` | IX:11 |
| Log size at that moment | `"event_count": 8062` | IX:12 |
| Active items at that moment | `"active_items": 2419` | IX:13 |
| Context | No commands were run, so no hash in this spec was recomputed. Every claim that "registered sha equals current bytes" is a check obligation, not an observation. The items array was seen only up to the truncation point, so the counts above are the fold's own counts, not mine. | contract RULES |

### 0.3 Standing caveat

The contract this spec encodes is registered on the surface as a PROPOSAL: IX items[path=SHARED_SURFACE_CONTR
