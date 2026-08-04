# Boot soil — density without full X archive

**Commitment:** `boot-soil-20260728-001`  
**Track:** Practice R0-lite + honest partial weight prep  
**Does not replace:** W0.0 full archive when PO exports it.

## Why

`data/raw` is empty. Exports already exist. Waiting on the zip is paralysis if the goal is **practice density** or progressive annotate.

## Path (existing tools only)

```powershell
cd Documents\projects\mycelial-republic
.\.venv\Scripts\Activate.ps1   # or mycelia.cmd

# Soil already on disk:
#   data/exports/from_chrome_bookmarks.jsonl
#   data/exports/from_manual_urls.jsonl
#   data/exports/nacho_merged_signal.jsonl
#   data/exports/nacho_x_3mo_signal.jsonl
#   data/exports/threads_full.jsonl

# Annotate / merge into train set (PO density tags)
python -m mycelial_republic.data.annotate `
  --in data/exports/nacho_merged_signal.jsonl `
  --out data/annotated/mirror_train.jsonl

# Optional: other export files as separate --in runs, then merge jsonl

# Validate when density is honest (use real count; 800 is weight-R0 gate)
python -m mycelial_republic.data.validate `
  --in data/annotated/mirror_train.jsonl `
  --min 100
```

When full archive lands under `data/raw/`:

```powershell
python -m mycelial_republic.data.prep --raw data/raw --out data/exports/posts.jsonl
# then annotate posts.jsonl → mirror_train.jsonl; validate --min 800
```

## Law

- Private data stays gitignored.  
- Do not claim W0.3 / weight R0 until `--min 800` green.  
- Do claim practice progress when selftest + annotated density rise with evidence paths.

## Linked

- Dual progress: `docs/MILESTONES.md`  
- Mag agent state: `../local_sovereign_agent/memory/agent_state/LATEST.md`
