# Sprint 0.1 — Data Foundation

**User story:** As an operator, I want my X archive cleaned and structured so the mirror can learn my rope and chord style.

## Acceptance criteria

- [ ] 800+ high-quality examples ready  
- [ ] Annotated with rope/knot language (`knot_tags`, optional notes)  
- [ ] Private data not committed to git  
- [ ] No capture fields (`token_balance`, `mirror_rank`, etc.)  

## Steps

### 0. Partial public harvest (bridge while archive pending)

You **can** pull high-signal public posts from `@NachoQuixotic` (or any public account) without waiting for the full archive:

| Method | Coverage | How |
|--------|----------|-----|
| Agent X search | Sparse (tool caps ~10/query) | Keyword/date windows → seed JSONL |
| `x_pull` + status IDs | Per-post full text | `python -m mycelial_republic.data.x_pull --ids-file ids.txt --out data/exports/posts.jsonl` |
| Official X archive | **Complete** history | Still required for 800+ density |

Current seed harvest (3-month signal cores):

```
data/exports/nacho_x_3mo_signal.jsonl
data/annotated/mirror_train_x_signal.jsonl   # ~16 high-signal after annotate
```

This is **not** 800 examples. It is a **boot corpus** (Elias, three machines, marble OS, Verkle, helpful strangers, Bernays/Jung). Expand by more search windows + IDs, then merge with full archive when available.

### 1. Export X data (complete path)

1. X → Settings → Your account → Download an archive of your data  
2. Wait for email; download the zip  
3. Place zip (or extracted folder) in `data/raw/`  
   - Example: `data/raw/twitter-2026-07-15-*.zip`

### 2. Extract & clean

```powershell
cd Documents\projects\mycelial-republic
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

python -m mycelial_republic.data.prep --raw data/raw/YOUR_ARCHIVE.zip --out data/exports/posts.jsonl
```

Drops pure RTs, ultra-short posts, link-only posts. Adjust `--min-chars` if needed.

### 3. Auto-annotate + hand-refine

```powershell
python -m mycelial_republic.data.annotate --in data/exports/posts.jsonl --out data/annotated/mirror_train.jsonl --auto-heuristics
```

Heuristics tag `chord`, `refusal`, `rope`, etc. **You must still hand-edit** high-value rows:

- `rope_note` — what tension is visible  
- `chord_note` — how the text strikes  
- `refusal_note` — what is refused  
- Prefer `signal: high` for chord/refusal/parable/meta  

Template: `configs/annotation_template.json`  
Sample rows: `data/annotated/examples/sample_train.jsonl`

### 4. Validate

```powershell
python -m mycelial_republic.data.validate --in data/annotated/mirror_train.jsonl --min 800
```

For dry runs with samples only:

```powershell
python -m mycelial_republic.data.validate --in data/annotated/examples/sample_train.jsonl --min 3
```

### 5. Density targets (quality, not just count)

| Tag | Suggested minimum in first 800 |
|-----|--------------------------------|
| chord | ≥ 30 |
| refusal | ≥ 20 |
| rope | ≥ 40 |
| parable / meta | ≥ 15 each |
| daily high-signal | remainder |

If short on refusals/chords: write **manual** examples in the same JSONL schema (source: `manual`).

## Definition of Done (Sprint 0.1)

- [ ] Validate passes at ≥800  
- [ ] Chord strike logged on the dataset process itself  
- [ ] Risk R5 (adoption friction) reviewed: this doc is clear enough for a second operator  
