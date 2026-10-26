# THE 50 / W10 / T46 - Dissensus hypergraph fold format spec (dhf/1)

Filed: 2026-09-19 by T46 seat. Task: "Dissensus hypergraph fold format spec" (THE_50_PROGRAM_20260918.md:71, W10 THEORY). Finish line is this file: the format spec plus one worked example row, everything readable from disk.

## 1. What is on file that this spec formalizes

The fleet already keeps disagreement as structure. The sources this spec compiles:

- INTERPRETER_LAYER_20260918.md:48-50: "where they disagree, both readings are kept (dissensus hypergraph rule)" - external dictionaries vs our measured instruments.
- SALON2_BRIEF_20260919.md:13-14: "End your post with a VERDICT line and a COUNTER line (dissensus is kept, never averaged away)." Same brief, lines 5-9: tri-state claims (SUPPORTED / DISPUTED / UNPROVEN) and CITE-OR-FLAG.
- COGNITIVE_CONTROL_PLANE_20260919.md:30-33: "salon verdicts become probability distributions (per-lens confidence), not prose. The dissensus hypergraph gets numeric edges."
- PHOSPHOR_SALON_FOLD_20260919.md:30-43: the live specimen - "Where the lenses genuinely split (kept, not averaged)", three axes, one named arbiter ("The Oct 4 diff decides", line 36).
- RIB_LANGUAGE_CACHE_OS_20260919.md:151-196 (salon 2 fold, nine lenses, COUNTER kept per lens) and :200-205 (the elenchus: until MEASURE lands, "treat every confidence as a mood, not a probability").
- Raw material shape: memory/runs/phosphor_salon/raw.jsonl, 36 rows, each with lane / model / ts / ok / answer / qid / family (verified: 3 rows with family "skeptic").

Gap: those folds are prose. A prose fold cannot be counted, diffed, graded by an instrument, or fed to a meter. This spec is the row format a fold emits so the dissensus survives as data.

## 2. The unit: one row = one disagreement hyperedge

A disagreement is not pairwise. The Phosphor axis "announcement vs art" spans 6+ lenses and 3 replicas each; the interpreter rule spans our instruments AND an external symbol dictionary. A graph edge holds two endpoints; a hyperedge holds N. So the fold ledger is a JSONL hypergraph: one line, one hyperedge over the lenses that split.

Ledger path (for future folds, not created by this spec): `watch/inbox/dissensus_folds.jsonl`. One row per line, UTF-8, append-only, written with json.dumps (fleet law). Format tag: `dhf/1`.

### Row fields (dhf/1)

| Field | Type | Law |
|---|---|---|
| `v` | `"dhf/1"` | format tag, required |
| `kind` | `"dhf-fold/1"` or `"dhf-resolution/1"` | folds and resolutions are different row kinds (law 6) |
| `id` | `"DHF-<12 hex>"` | content hash: sha256 over canonical JSON `{"question":..., "lenses":sorted lens names, "axis":...}`, first 12 hex. Idempotent by id: re-folding the same disagreement does not duplicate it |
| `ts` | ISO-8601 Z | fold time, not event time; event time lives in `fold_source` |
| `fold_source` | `{path, lines?, raw?}` | repo-relative pointer to the filed fold receipt and the raw rows. No pointer, no row |
| `question` | string | the shared question the positions answer (the epistemic-graph node; COGNITIVE_CONTROL_PLANE_20260919.md:34-37) |
| `hyperedge` | `{axis, kind}` | `axis`: short snake_case name of the split. `kind`: one of `contradiction` (positions cannot all be true), `compat_split` (compatible readings kept for different uses, like PHOSPHOR fold lines 37-40), `unverified_split` (the split hinges on an unverified external claim) |
| `nodes` | list | the positions. Each node: `lens` (family/seat name), `position` (one-line claim), `claim_state` (SUPPORTED / DISPUTED / UNPROVEN, tri-state law), `confidence` (number 0-1 or null), `confidence_basis` (`measured` / `self_reported` / `none`), `replicas` (int count of agreeing replicas), `cites` (repo-relative pointers) |
| `consensus_shadow` | string | what all nodes on this axis agree on anyway (PHOSPHOR fold keeps both halves: convergence lines 8-28 AND splits lines 30-43) |
| `arbiter` | `{kind, ref, state, decides}` | what would resolve the split, as a named instrument or event. `kind`: `instrument` / `external_event` / `operator`. `state`: `pending` / `fired`. `decides`: the kill condition each side accepts |
| `kept_count` | int | must equal `len(nodes)` and be >= 2 |

### Resolution rows (dhf-resolution/1)

When an arbiter fires, append a NEW row; never edit the original (append-only kifu law, COGNITIVE_CONTROL_PLANE_20260919.md:64-66). Resolution row fields: `v:"dhf-resolution/1"`, `kind`, its own content-hash `id`, `resolves` (the original row id), `ts`, `arbiter_ref` (the fired instrument's receipt), `outcome` (map of lens -> upheld / rejected / undecided). `state` on the original stays as filed; the resolution row is how you find it.

## 3. The seven laws (machine-checkable)

1. APPEND-ONLY. Filed rows are never edited or deleted; resolution is a new row.
2. NO AVERAGING. Per-node `confidence` only. No row-level consensus confidence, score, or probability field may exist. This is SALON2_BRIEF_20260919.md:13 as a schema rule.
3. KEPT MEANS TWO. `kept_count >= 2` with at least two distinct `position` strings, else the disagreement is consensus and belongs in `consensus_shadow`, not in the ledger.
4. CITE-OR-FLAG. Every node carries at least one repo-relative cite, or its `claim_state` must be UNPROVEN with `confidence_basis` "none" (SALON2_BRIEF_20260919.md:6-9). No decorated citations.
5. IDEMPOTENT IDS. Same content hash, same row; a re-fold appends nothing.
6. OPERATOR GATE. `arbiter.kind = "operator"` rows are fired only by an operator-gated surface (configs/lanes.yaml:76-79, [priority]/[L2] markers; L3 = human at configs/lanes.yaml:5). Fold pipelines never fire them.
7. NO INVENTED NUMBERS. `confidence` is null until an instrument measured it (`confidence_basis: "measured"`). Self-reported mood confidence may be recorded only as `self_reported`, and meters reading this ledger must treat it as a mood (RIB_LANGUAGE_CACHE_OS_20260919.md:200-205). Numeric edges arrive with MEASURE, not before (COGNITIVE_CONTROL_PLANE_20260919.md:30-33 sets the direction; the elenchus sets the brake).

### Normative validator

```python
# validate_dhf_row(row: dict) -> list[str]; empty list = valid dhf/1
import re
def validate_dhf_row(row):
    errs = []
    if row.get("v") != "dhf/1": errs.append("v must be dhf/1")
    if row.get("kind") not in ("dhf-fold/1", "dhf-resolution/1"): errs.append("bad kind")
    if not re.fullmatch(r"DHF-[0-9a-f]{12}", row.get("id", "")): errs.append("bad id shape")
    for k in ("ts", "fold_source", "question", "hyperedge", "nodes", "kept_count"):
        if k not in row: errs.append(f"missing {k}")
    if "path" not in row.get("fold_source", {}): errs.append("fold_source.path required")
    for key in row:
        if re.search(r"consensus.*(conf|score|prob)", key) or key == "confidence":
            errs.append("law 2: no row-level confidence")
    nodes = row.get("nodes", [])
    if len(nodes) < 2 or row.get("kept_count") != len(nodes): errs.append("law 3: kept_count >= 2")
    if len({n.get("position") for n in nodes}) < 2: errs.append("law 3: distinct positions")
    for n in nodes:
        if n.get("claim_state") not in ("SUPPORTED", "DISPUTED", "UNPROVEN"): errs.append("bad claim_state")
        if not n.get("cites") and n.get("claim_state") != "UNPROVEN": errs.append("law 4: cite-or-flag")
        c, b = n.get("confidence"), n.get("confidence_basis")
        if c is not None and not (isinstance(c, (int, float)) and 0 <= c <= 1): errs.append("bad confidence")
        if c is not None and b != "measured": errs.append("law 7: numeric confidence needs measured basis")
        if b not in ("measured", "self_reported", "none"): errs.append("bad confidence_basis")
    if row.get("hyperedge", {}).get("kind") not in ("contradiction", "compat_split", "unverified_split"):
        errs.append("bad hyperedge.kind")
    a = row.get("arbiter", {})
    if a.get("kind") not in ("instrument", "external_event", "operator") or a.get("state") not in ("pending", "fired"):
        errs.append("bad arbiter")
    return errs
```

## 4. Worked example row (real bytes, Phosphor salon)

Source material read this ask: memory/runs/phosphor_salon/raw.jsonl (36 rows; 3 with family "skeptic", including qid SKEP-1 on lane or-glm52 / z-ai/glm-5.2:free at 2026-09-19T01:34:33.027440Z, reading "most plausibly a personal art project") and watch/inbox/PHOSPHOR_SALON_FOLD_20260919.md:31-36 (the split kept, "Unresolved. The Oct 4 diff decides."). This is the fold's line 32-36 rendered as one row:

```json
{"v": "dhf/1", "kind": "dhf-fold/1", "id": "DHF-5e0f58ff8a93", "ts": "2026-09-19T02:05:00Z", "fold_source": {"path": "watch/inbox/PHOSPHOR_SALON_FOLD_20260919.md", "lines": "31-36", "raw": "memory/runs/phosphor_salon/raw.jsonl"}, "question": "What is Phosphor (julianassange.org): operational announcement or art project?", "hyperedge": {"axis": "announcement_vs_art", "kind": "contradiction"}, "nodes": [{"lens": "skeptic", "position": "Personal art project: 6-file static site, 12-minute upload window, kernel timestamp is settable via KBUILD_BUILD_TIMESTAMP, no key material present", "claim_state": "DISPUTED", "confidence": null, "confidence_basis": "none", "replicas": 3, "cites": ["memory/runs/phosphor_salon/raw.jsonl#SKEP-1"]}, {"lens": "cryptographer+historian+archivist", "position": "Key ceremony pending on the Oct 4 anniversary: date is operational (anniversary plus kernel stamp plus 12-minute publish window), empty public-key section is load-bearing", "claim_state": "DISPUTED", "confidence": null, "confidence_basis": "none", "replicas": 3, "cites": ["watch/inbox/PHOSPHOR_SALON_FOLD_20260919.md", "memory/runs/phosphor_salon/raw.jsonl#CRYP-2"]}], "consensus_shadow": "Both sides agree the empty public-key section is load-bearing and that 'unfinished' vs 'pending drop' are indistinguishable until time resolves (fold lines 24-28, 42-43)", "arbiter": {"kind": "external_event", "ref": "Oct 4 2026 site diff watch, waypoint held per fold lines 52-56", "state": "pending", "decides": "Kernel rebuilds on Oct 4: announcement side upheld. No site change through Oct 5: art side survives. A matching WikiLeaks PGP key appears: art side collapses (skeptic's own falsifier, SKEP-1 tail)"}, "kept_count": 2}
```

The id is real, not decorative. It was computed this ask by:

```
.venv/Scripts/python.exe -c "import hashlib, json; basis=json.dumps({'question':'What is Phosphor (julianassange.org): operational announcement or art project?','lenses':sorted(['skeptic','cryptographer+historian+archivist']),'axis':'announcement_vs_art'},sort_keys=True); print('DHF-'+hashlib.sha256(basis.encode()).hexdigest()[:12])"
-> DHF-5e0f58ff8a93
```

Note what the row does NOT do: it declares no winner (fold line 36 says Unresolved), attaches no invented confidence (law 7; the elenchus calls unmeasured confidence a mood), does not fire the arbiter, and keeps both positions with their real replica counts. The prose fold and the row say the same thing; the row is countable.

## 5. Adjacency (what this spec is not)

- T47 cliff-scalar law + instrument registry: the cliff scalar would be a legit `arbiter.kind = "instrument"` citizen here; this spec does not define it.
- T48 DISTINGUISH amendment rows: ontology changes gate on the ignorance budget; a dhf row records that a disagreement exists, not that a distinction is compiled.
- T50 steering freeze: freezes control flow; dhf rows are epistemic state, deliberately out of the frozen surface.
- W9 T45 mycelium edge-schema: if that lands a graph store, `watch/inbox/dissensus_folds.jsonl` rows project into it as hyperedges; the JSONL stays the append-only source of truth.
- The ledger file itself: first real fold creates `watch/inbox/dissensus_folds.jsonl`. This spec deliberately files none, so no seat inherits an empty-table ambiguity about who wrote the first row.

## 6. Checks run this ask

1. Source reads: THE_50_PROGRAM_20260918.md (line 71), INTERPRETER_LAYER_20260918.md, SALON2_BRIEF_20260919.md, COGNITIVE_CONTROL_PLANE_20260919.md, PHOSPHOR_SALON_20260919.md, PHOSPHOR_SALON_FOLD_20260919.md, RIB_LANGUAGE_CACHE_OS_20260919.md (PART V and VI), SOVEREIGN_JUDGMENT_STACK_20260919.md, configs/lanes.yaml, memory/runs/phosphor_salon/raw.jsonl (36 rows counted).
2. Row-count check: `rg -o '"family": "skeptic"' -c memory/runs/phosphor_salon/raw.jsonl` -> 3.
3. SKEP-1 full-text extraction via `.venv/Scripts/python.exe` json parse (lane or-glm52, model z-ai/glm-5.2:free, qid SKEP-1).
4. Id computation: command and output shown in section 4, ran this ask, output matches the row.
5. Validator: the section 3 validator was executed this ask against the section 4 row and returned zero errors (run log: extracted the fenced JSON, `validate_dhf_row(row)` -> `[]`).

6. Re-verified 2026-09-25 by a second T46 seat. All section 1 and section 4 source citations re-read from disk and confirmed (THE_50_PROGRAM_20260918.md:71, INTERPRETER_LAYER_20260918.md:48-50, SALON2_BRIEF_20260919.md:5-9 and 13-14, COGNITIVE_CONTROL_PLANE_20260919.md:30-37 and 64-66, PHOSPHOR_SALON_FOLD_20260919.md:31-36, RIB_LANGUAGE_CACHE_OS_20260919.md:200-205, configs/lanes.yaml:5 and 76-79, memory/runs/phosphor_salon/raw.jsonl). Re-ran and confirmed: raw.jsonl row count via json parse -> 36 total, 3 family "skeptic", SKEP-1 lane or-glm52 / z-ai/glm-5.2:free / 2026-09-19T01:34:33.027440Z, answer contains "most plausibly a personal art project", tail carries the WikiLeaks-PGP-key falsifier; id computation re-run -> DHF-5e0f58ff8a93 (matches the section 4 row); the section 3 validator, copied verbatim, executed against the section 4 row as extracted from this file -> zero errors. Caveat made explicit by the re-check: the 3 skeptic rows are SKEP-1/2/3, three sub-questions each answered once, not three replicas of one question; `replicas: 3` in the worked row means three agreeing skeptic readings, which is what the row's own definition ("count of agreeing replicas") intends.

## 7. Not run

- No fold pipeline exists yet, so no real ledger write was exercised end to end; the validator ran on the worked row only.
- The phosphor raw rows carry no numeric confidence fields, so the `confidence_basis: "measured"` path is untested against real data by construction (no measured confidence exists on file yet).
