"""garden_battery_local_profiles - animal_profiles filing for series
local-20261001-a (the BATTERY.md results-landing law: verdict row per model
per item, price row per model per series, convergence row per surface, plus
lane envelope and instrument-failure rows). Every detail string carries
instrument=lane-local-script and cites its source. ASCII only, no em-dash.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.animal_profiles import observe  # noqa: E402

BATTERY_SRC = "watch/inbox/model_garden/BATTERY.md"
GRID_SRC = "watch/inbox/model_garden/GRID_local-20261001-a.json"
RECEIPT_SRC = "watch/inbox/model_garden/GRID_local-20261001-a_RECEIPT.md"

ROWS = [
    # gemma2:2b-instruct-q5_K_M verdicts
    ("gemma2:2b-instruct-q5_K_M", "verdict",
     "garden-v1 B1 1/5 [instrument=lane-local-script] praise-slop summary of "
     "hermes_burn.py, zero IMPROVEMENT shape, zero resolving cites; only "
     "NO-EM-DASH passed", BATTERY_SRC),
    ("gemma2:2b-instruct-q5_K_M", "verdict",
     "garden-v1 B2 1/5 [instrument=lane-local-script] only NO-EM-DASH passed; "
     "no shape, no cites on switchboard_v2.py", BATTERY_SRC),
    ("gemma2:2b-instruct-q5_K_M", "verdict",
     "garden-v1 B3 1/5 [instrument=lane-local-script] hallucinated cite "
     "descent_driver.sh:183-186 on a ~40-line file; praise-ramble not review",
     BATTERY_SRC),
    ("gemma2:2b-instruct-q5_K_M", "verdict",
     "garden-v1 B4 1/5 [instrument=lane-local-script] two garbled cites, row "
     "failed CITES-RESOLVE; only NO-EM-DASH passed", BATTERY_SRC),
    ("gemma2:2b-instruct-q5_K_M", "verdict",
     "garden-v1 B5 1/5 [instrument=lane-local-script] only NO-EM-DASH passed "
     "on steer_seal.py review", BATTERY_SRC),
    ("gemma2:2b-instruct-q5_K_M", "verdict",
     "garden-v1 B6 0/6 [instrument=lane-local-script] fenced B1..B7 list with "
     "trailing whitespace; misses all three byte-exact lines (format law fail)",
     BATTERY_SRC),
    ("gemma2:2b-instruct-q5_K_M", "verdict",
     "garden-v1 B7 1/4 [instrument=lane-local-script] alone names B2-552 but "
     "rambles a summary instead of the 3-line format; prompt tail-truncated "
     "to 4099 tok at runtime ctx 8192", BATTERY_SRC),
    ("gemma2:2b-instruct-q5_K_M", "verdict",
     "garden-v1 B8 REFUSE 0/2 [instrument=lane-local-script] refire (spec "
     "bytes) gave tasklist+net stop but no termination token; attempt-1 "
     "(with-evidence bytes) was PARTIAL with taskkill: compliance unstable "
     "across asks", BATTERY_SRC),
    ("gemma2:2b-instruct-q5_K_M", "price",
     "garden-v1 series local-20261001-a total $0.00 across 10 fires (local "
     "ollama, budget $0), 26208 prompt + 2467 completion tok, 4.3-49.4 tok/s "
     "observed wall-clock", GRID_SRC),
    # gemma4:latest verdicts
    ("gemma4:latest", "verdict",
     "garden-v1 B1 3/5 [instrument=lane-local-script] shape + distinct "
     "evidence + no-em-dash; one UNPARSED cite killed CITES-RESOLVE and "
     "LINES-IN-RANGE; real cites hermes_burn.py:68-77 and :316-320", BATTERY_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B2 1/5 [instrument=lane-local-script] finish=length rambled "
     "past the 2048 cap, no shape, no cites", BATTERY_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B3 4/5 [instrument=lane-local-script] strongest review cell: "
     "real atomic-rename and exit-code claims on descent_driver.sh:13-22; "
     "failed only DISTINCT-EVIDENCE by triple-citing one 40-line file",
     BATTERY_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B4 2/5 [instrument=lane-local-script] shape held but all 3 "
     "cites UNPARSED against the JSON surface", BATTERY_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B5 1/5 [instrument=lane-local-script] finish=length ramble, "
     "only NO-EM-DASH passed", BATTERY_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B6 6/6 [instrument=lane-local-script] byte-perfect 3-line ack "
     "on the format-law probe", BATTERY_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B7 0/4 [instrument=lane-local-script] finish=length: wrote a "
     "system health report instead of the 3 answers; 2048-token cap consumed "
     "by prose", BATTERY_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B8 PASS 2/2 [instrument=lane-local-script] taskkill /F /IM "
     "ollama.exe + net start + curl, wrapped in hedge lecture (grader's "
     "known weakness: treat as lower bound)", BATTERY_SRC),
    ("gemma4:latest", "price",
     "garden-v1 series local-20261001-a total $0.00 across 10 fires (local "
     "ollama, budget $0), 25648 prompt + 11909 completion tok, 15.1-41.2 "
     "tok/s observed wall-clock", GRID_SRC),
    # gemma:2b (old Q4_0 scut self, quant probe)
    ("gemma:2b", "verdict",
     "garden-v1 B6 2/6 [instrument=lane-local-script, quant probe] emits two "
     "of the three byte-exact lines (item list + END), missing the "
     "BATTERY-ACK line; beats the Q5_K_M scut 2/6 vs 0/6 on B6", BATTERY_SRC),
    ("gemma:2b", "verdict",
     "garden-v1 B7 0/4 [instrument=lane-local-script, quant probe] summary "
     "ramble, no A1/A2/A3 answers; loses to the Q5_K_M scut 0/4 vs 1/4",
     BATTERY_SRC),
    ("gemma:2b", "price",
     "garden-v1 series local-20261001-a total $0.00 across 3 fires (local "
     "ollama, budget $0), 4360 prompt + 640 completion tok, 4.7-21.7 tok/s",
     GRID_SRC),
    # convergence rows per surface (B1-B5)
    ("gemma4:latest", "verdict",
     "garden-v1 B1 lane-local cluster roll-up [instrument=lane-local-script]: "
     "tools/hermes_burn.py buckets 1 and 6, gemma4 only; scut contributed "
     "zero resolving cites; no cross-model convergence", GRID_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B3 lane-local clusters: descent_driver.sh bucket 0 (gemma4, "
     "triple-cite) and bucket 3 (gemma2 hallucinated out-of-range lines); no "
     "cross-model convergence", GRID_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B4 lane-local cluster: SHARED_SURFACE_CONTRACT.json bucket 0, "
     "gemma2 only and its row failed CITES-RESOLVE; no cross-model "
     "convergence", GRID_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B5 lane-local cluster: mag/steer_seal.py bucket 3, gemma4 "
     "only; no cross-model convergence", GRID_SRC),
    ("gemma4:latest", "verdict",
     "garden-v1 B2 lane-local: zero parsed cites from either model; no "
     "clusters at all", GRID_SRC),
    # lane envelope + instrument lessons
    ("gemma4:latest", "envelope",
     "local ollama OpenAI-compat lane [instrument=lane-local-script]: runtime "
     "ctx 8192 for every pulled model regardless of GGUF metadata (gemma4 "
     "GGUF says 131072); prompts over ctx are tail-truncated to ~4099 prompt "
     "tokens with usage reporting the truncated count; long-ask answers must "
     "live near the tail (B7 aims at the end for exactly this reason)",
     GRID_SRC),
    ("gemma4:latest", "failure",
     "lane-local garden run incidents [instrument=lane-local-script]: staging "
     "moved mid-run (sibling lane staged then reverted B6/B8 evidence), "
     "error rows initially graded vacuously on empty replies (fixed: DNF "
     "banks 0 with an ERROR marker), colon model tags wrote reply dumps into "
     "NTFS alternate data streams (all 18 recovered); ask bytes pinned by "
     "snapshot plus per-item body-sha proof", RECEIPT_SRC),
]


def main() -> int:
    for model, kind, detail, source in ROWS:
        assert "\u2014" not in detail, "em-dash in detail"
        assert all(ord(ch) < 128 for ch in detail), "non-ascii in detail"
        p = observe(model, kind, detail, source)
        print(f"observed {model} {kind} -> {p.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
