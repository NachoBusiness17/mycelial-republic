"""Pressure-test the token-generation business thesis on BOTH grok Pro seats (2026-08-25).

Operator: "we have two pro seats and 2 cli's" — no gating, dispatch to both, two independent
frontier takes. Isolated via GROK_HOME per seat (nacho=~/.grok, sd=~/.grok-sd).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))

from mag.grok_seat_burner import SEATS, _launch_one, seats_status  # noqa: E402

GOAL = (
    "Pressure-test a business thesis with maximum honesty. Be blunt. Do not cheerlead. "
    "MAG is a local sovereign agent stack that cache-mines cheap inference: a frozen "
    "byte-stable instruction prefix rides multiple provider lanes at ~96.93% cache hit; "
    "cached input is 5-31x cheaper than fresh (GLM 4.5-air $0.03/M cached, DeepSeek $0.007/M "
    "cached off-peak vs $0.22 miss); it steers cheap models with per-vendor tuned system "
    "prompts (CL4R1T4S corpus + distilled seat profiles) so they answer closer to frontier. "
    "Thesis: we are a 'distributed generator' like rooftop solar feeding the grid - we "
    "generate competent inference at near-zero marginal cost and sell the capacity. "
    "Answer exactly three things, numbered: "
    "(1) Is 'sell the generation layer' (BYOK: customer pastes their own provider key, we "
    "charge flat for the optimization stack) the right first product, vs 'feed the grid' "
    "(hosted resale at 50% of list)? Pick one and defend it. "
    "(2) Is renting a Vast.ai GPU (~$0.25-0.80/hr for 48GB, open Apache-2.0 weights, ~$2-6/M "
    "self-hosted, NO provider ToS wall) the right cheap test of the serving loop? Note "
    "self-hosting LOSES to cache-mined APIs on input cost but wins on output-heavy work, "
    "control, and legality. Is it the right first experiment or a distraction? "
    "(3) What is the single thing we are missing that kills this business if we don't see "
    "it now? "
    "Facts: output tokens are never cache-discounted ($4.4/M on GLM-5.3); z.ai ToS prohibits "
    "account sharing and restricts the coding plan to supported tools; free tiers are "
    "revocable promos; a planned experiment (MAX_DISTILL) measures how much of a frontier "
    "model's verified advantage is recoverable as cheap-lane policy (RAR). "
    "Deliverable: three numbered answers + a one-line verdict. No framework loading, no "
    "process narration, no hedging."
)


def main() -> int:
    status = seats_status()
    print("SEAT STATUS:", status.get("seats"))
    for seat in ("nacho", "sd"):
        cfg = SEATS[seat]
        auth = Path(cfg["home"]) / "auth.json"
        if not auth.is_file():
            print(f"\n=== {seat}: NOT AUTHENTICATED (no auth.json at {cfg['home']}) — skipped")
            continue
        print(f"\n=== {seat} ({cfg['email']}) — launching grok...")
        r = _launch_one(seat, GOAL, model="", max_turns=6, timeout=600, no_subagents=True)
        ok = r.get("ok")
        print(f"--- {seat} exit_code={r.get('exit_code')} ok={ok}")
        out = (r.get("output") or "").strip()
        print(out[-6000:] if out else f"(no output) stderr={r.get('stderr') or r.get('error')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
