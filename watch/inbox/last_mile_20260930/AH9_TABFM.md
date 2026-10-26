# AH9 — TabFM (google/tabfm-1.0.0-pytorch) CPU trial on duels.jsonl

**Date:** 2026-09-30 · **Seat:** ZCode subagent (refire) · **Files owned:** `tools/tabfm_try.py`, this receipt
**Mission:** install tabfm per google-research/tabfm README, load on CPU, classify duel winner (A/B) from criterion scores in `logs/duel/duels.jsonl`, report accuracy + enum/hash handling, honest failure bank. 30-min wall cap.

## Loaded: YES (pure CPU, zero CUDA needed)

- **Install:** `pip install tabfm` (PyPI **1.0.1**) — the first attempt's clone-bootstrap + typeguard shim were obsolete; package is on PyPI now. Venv friction: pin downgraded **typeguard 4.6.0 → 2.13.3**, conflicting with `inflect>=4.0.1` (pre-existing dep). torch **2.13.0+cpu**, 8 threads.
- **Weights:** HF `google/tabfm-1.0.0-pytorch`, 2 files, **2.8 GB** download (**634 s**), cached in `~/.cache/huggingface/hub`.
- **Size:** **1,639 M params measured** (`sum(p.numel())`) — mission brief said 400 M; byte truth is 4x that.

## Task + results

`duels.jsonl` live file: 62 raw rows at run time, 61 usable (1 TIE dropped; file grew by 1 row mid-mission — it is an active log). Features: 13 numeric (per-criterion a/b scores, cost, chars) + `judge`/`mode` enums + `ask_id` hash (unique per row). Seeded split 51 train / 10 query (`RandomState(0)`).

| Model | Query accuracy (n=10) | Time |
|---|---|---|
| majority (B) | 0.500 | — |
| OneHot + LogReg | 1.000 | <1 s |
| **TabFM full (enum+hash cols)** | **1.000** | 104 s (n_est=8, batch=8) |
| TabFM numeric-only | 1.000 | 103 s |

Run log: `python tools/tabfm_try.py`, wall 847 s total incl. download. Exit 0, no failures — **failure bank stays empty** (no CUDA required anywhere).

## Enum/hash column handling (byte-verified, the Amazon_employee_access analog)

TabFM is **not a text-prompt LLM**: rows are serialized as a numeric table (Fourier-feature embeddings + `cat_mask` marking categorical cells; context rows get label-embeddings added — tabular ICL). Categorical path (source: `tabfm/src/classifier_and_regressor.py`):

- Auto-detects string cols → `CategoricalOrdinalEncoder` (`appearance` order by default).
- **`min_frequency=2`: singleton categories encode to -1 "unknown".** Probed on our data: `ask_id` (61 unique hashes) → **all 61 rows = -1**, one bucket; `mode` (4 raw levels) → 3 survive, the singleton → -1; `judge` (constant) → 0.
- So opaque ids are **neutralized, not memorized** — no per-id lookup table to overfit; unseen categories at transform time also → -1.
- `permute_categorical=True` (ensemble option, default off) re-permutes ordinal→value assignment across estimators so arbitrary code order can't leak fake signal.

## Honest caveats

- **Task too easy to differentiate:** logreg also scores 1.000 — `score_diff_sum` nearly determines the winner. n=10 query → 10/10 has a wide CI (~0.69–1.0, Wilson). TabFM's edge (opaque-id tables, no-feature-engineering regime) is untested by this table.
- **Cost:** ~1.6 GB weights, ~100 s CPU per fit+predict on a 61×16 table vs milliseconds for logreg. Fine for offline scoring; not a hot-path tool on this box.
- First HF download on Windows lacks symlink support (hub warning, harmless).

## Verdict

**Applicable — conditionally.** Loads and runs clean on CPU via a scikit-learn API; genuinely handles enum/hash columns by design (frequency-gated ordinal encoding + unknown bucket + optional permutation ensembling). Worth reaching for when a small table has many opaque-id/enum columns and there is no budget to engineer features; overkill for clean numeric tables this size.

**Artifacts:** `tools/tabfm_try.py` (rewritten for PyPI package; probe fixed, TIE dropped, 51/10 split) · log at `~/.zcode/cli/exec/…/call_c445…-stdout.log`.
