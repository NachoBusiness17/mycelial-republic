---
license: cc0-1.0
pretty_name: Gigafish 3.8B d10
size_categories:
- 1B<n<10B
task_categories:
- tabular-regression
tags:
- chess
- stockfish
- lichess
- distillation
- position-evaluation
configs:
- config_name: default
  data_files:
  - split: train
    path: data-*.parquet
---

# Gigafish 3.8B d10

Gigafish holds 3.9 billion unique chess positions scored by Stockfish 16 at depth 10. Each row pairs a FEN (Forsyth-Edwards Notation) string with a Stockfish evaluation.

The blog post [Distilling Stockfish with One Billion Positions](https://blog.lukesalamone.com/posts/distilling-stockfish/)
describes how I built the dataset and trained a model on it.

| | |
|---|---|
| Rows | 3,919,006,164 unique positions |
| Files | 3,920 zstd-compressed parquet shards, 1M rows each (last shard smaller), about 101 GB |
| Label | Stockfish 16 evaluation at depth 10 |
| Source | Positions from 37 months of games in the [Lichess Open Database](https://database.lichess.org/) |
| Splits | `train` only |

## Schema

| column | type | description |
|---|---|---|
| `fen` | string | Full 6-field FEN: piece placement, side to move, castling rights, en passant square, halfmove clock, fullmove number |
| `eval` | string | Stockfish depth-10 evaluation, always from White's point of view |

The `eval` column uses two formats:

- **Number** (for example `0.6`, `-11.87`): score in pawns, with 1 or 2 decimal places. Multiply by 100 to get centipawns (cp, 1/100 of a pawn). A positive value means White is better. The sign does not depend on the side to move.
- **Mate** (for example `#3`, `#-4`): `#N` means White mates in N moves. `#-N` means Black mates in N moves. N is always 1 or more.

Example rows:

| fen | eval |
|---|---|
| `rn1qk1nr/p4pp1/2p1p1p1/1p6/3P4/6P1/PPP1B1PP/R1BQK2R b KQkq - 1 11` | `0.6` |
| `r3k1nr/pq3pp1/3p3p/4n3/8/2P1B3/P3BPPP/R3K2R b KQkq - 1 15` | `-11.87` |
| `8/8/8/8/8/1R6/2K5/k7 w - - 27 74` | `#1` |
| `8/8/8/8/4K3/6k1/5q1p/8 w - - 0 63` | `#-4` |

### Statistics (first shard, 1M rows)

| statistic | value |
|---|---|
| Mate labels | 8.6% of rows |
| Median mate distance | 5 moves (max 62) |
| Exact `0.0` evals | 4.0% of rows |
| Side to move | 49.8% White, 50.2% Black |
| Eval percentiles, non-mate (1st / 50th / 99th) | -13.63 / +0.03 / +13.76 pawns |
| Pieces on board, including kings (median, range) | 23 (2 to 32) |
| Fullmove number (median, max) | 21 (149) |

## Usage

Stream the full dataset with `datasets`:

```python
from datasets import load_dataset

ds = load_dataset("lukesalamone/gigafish-3.8b-d10", split="train", streaming=True)
for row in ds.take(3):
    print(row["fen"], row["eval"])
```

Download a single shard:

```python
import pandas as pd
from huggingface_hub import hf_hub_download

path = hf_hub_download(
    repo_id="lukesalamone/gigafish-3.8b-d10",
    filename="data-00000.parquet",
    repo_type="dataset",
)
df = pd.read_parquet(path)
```

Convert an eval to a win probability for White.
The constant K (0.00368208 per centipawn) comes from the Lichess win-probability formula.

```python
import math

K = 0.00368208

def white_win_prob(ev: str) -> float:
    """Return White's win probability (0 to 1). Mates map to 0 or 1."""
    if ev.startswith("#"):
        return 0.0 if ev.startswith("#-") else 1.0
    cp = float(ev) * 100
    return 1 / (1 + math.exp(-K * cp))
```

To train from the side to move's point of view, negate the eval (and swap mate sides) when Black is to move.

## How the dataset was built

1. **Extract positions.** A multithreaded Rust script pulled every FEN from 37 months of Lichess games.
2. **Deduplicate.** A Python script hashed each FEN with MD5. The first 12 bits of the hash picked one of 4,096 bucket files. Each bucket was then deduplicated on its own.
3. **Label.** Stockfish 16 scored each unique FEN at depth 10. The job ran on 24 cores for more than a day.
4. **Export.** A script wrote the `(fen, eval)` pairs to zstd parquet shards of 1M rows.

## Label quality

Depth 10 is a shallow search. To measure the label noise, I re-scored the 1M positions in `data-00000.parquet` at depths 5 to 30 and used depth 30 as ground truth.

The comparison maps each score to a win-probability bucket (1% wide), then back to centipawns. It clips scores to ±3000 cp and skips positions where depth 30 finds a mate.
cp_mae is the mean absolute error in centipawns.
within_50cp is the share of positions within 50 cp of the depth-30 score.

| Stockfish depth | cp_mae | within_50cp |
|---|---|---|
| 5 | 26.5 | 83.8% |
| **10 (this dataset)** | **21.2** | **87.8%** |
| 15 | 17.9 | 90.7% |
| 20 | 15.3 | 92.4% |
| 25 | 12.7 | 94.5% |

## Example use: distilling Stockfish

The [blog post](https://blog.lukesalamone.com/posts/distilling-stockfish/) trains a 79M-parameter model on 1 billion positions from this dataset. The model has 6 ResNet blocks followed by 16 Transformer blocks. It predicts 103 classes: 101 win-probability buckets (0% to 100%) and 2 forced-mate classes.

| metric (held-out set of about 50K positions) | value |
|---|---|
| Validation loss (cross-entropy + ordinal) | 2.648 |
| cp_mae | 64 cp |
| Directional accuracy (predicts which side is winning) | 92.97% |
| Win-probability error | about 4 to 5 percentage points |

## Comparison to ChessBench

[ChessBench](https://github.com/google-deepmind/searchless_chess) (DeepMind, 2024) labels (position, move) pairs with action values. Gigafish labels positions only, with one state value per position. The blog post describes Gigafish as the largest open (position, eval) chess dataset at a fixed search depth.

## Limitations

- **Shallow labels.** Depth-10 scores differ from depth-30 scores by 21 cp on average. See [Label quality](#label-quality).
- **Mate distances are approximate.** A depth-10 search may not find the shortest mate.
- **Lichess distribution.** The positions come from online games, most of them between amateur players. Positions that rarely occur in these games are rare in the dataset.
- **No frequency information.** Deduplication keeps one copy of each position. A common opening position counts the same as a position from one game.
- **Deduplication uses the full FEN string.** The same board with a different halfmove clock or fullmove number appears as separate rows.
- **White-relative scores.** Models that see the board from the side to move need to flip the sign.
- **One split.** The dataset has no official validation or test split. Hold out your own rows.

## License

The source games come from the Lichess Open Database, released under CC0.
This dataset is also released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

## Citation

```bibtex
@misc{salamone2026distilling,
  author = {Salamone, Luke},
  title  = {Distilling Stockfish with One Billion Positions},
  year   = {2026},
  month  = mar,
  url    = {https://blog.lukesalamone.com/posts/distilling-stockfish/},
  note   = {Dataset: https://huggingface.co/datasets/lukesalamone/gigafish-3.8b-d10}
}
```
