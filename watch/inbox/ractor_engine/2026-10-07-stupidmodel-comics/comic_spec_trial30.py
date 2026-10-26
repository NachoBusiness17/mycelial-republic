#!/usr/bin/env python3
"""comic_spec_trial30: the mandated full-scale panel-spec trial (2026-10-07).

Hostile-pass verdict on comic_spec_probe: two n=3 headline numbers are
run-unstable (gemma:2b unconstrained schema_ok 0/3 vs the pass's 1/3;
gemma4 strict in_character 3/3 vs the pass's 2/3); the structural lift
reproduced. This trial replaces n=3 cells with rates at n=13 per arm
(10 fresh session-fact sources + the 3 original sources repeated 3x each =
variance measurement on the contested cells). Temperature 0, seed UNPINNED
(the production shape: the comic lane will not pin seeds; run-to-run
variance is a measured property, not noise to hide).

Contested claims under test:
  A: gemma:2b schema_ok flip under FORMAT (both arms)
  B: gemma4:latest strict in_character under FORMAT ("the only seat passing
     the strict digit rule" fails at n=3; what is the real rate?)

Seats/arms: gemma:2b x {UNCONSTRAINED, FORMAT}, gemma4:latest x FORMAT,
qwen2.5:7b x FORMAT (its unconstrained cell was not contested; kept as the
fallback-seat rate). The battery is 19 prompts (10 fresh + 3 sources x 3
repeats) x 4 seat-arm cells = 76 calls, $0 local. (Docstring arithmetic
corrected post-run: the first draft said 13x5=65; the fired truth in
comic_spec_trial30.jsonl is 76 rows.)
Rows append incrementally to comic_spec_trial30.jsonl; summary banked to
comic_spec_trial30.json at end. Same SCHEMA/PROMPT/scoring as the banked
probe module (imported, not copied).
"""
import json
import re
import sys
import time
from pathlib import Path

DIR = Path("watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics")
sys.path.insert(0, str(DIR))
import comic_spec_probe as csp  # noqa: E402

FRESH = [
    ("dance-octave",
     "Session fact: the tempo estimator read flat_beat_loop.mp3 at 64.6 BPM, "
     "below the 80 BPM window - the defect. The v2 rule scores b0/2, b0, b0*2 "
     "clipped to the window; the track now reads 129.20, the true tempo, "
     "exactly double.",
     ["tempo", "bpm", "window", "double"]),
    ("phone-relay-token",
     "Session fact: the approval relay's substring match let the literal "
     "reply 'deny' approve an ask, because 'y' is a substring of 'deny'. The "
     "fix is exact-token decision: approve and deny word sets compared as "
     "whole tokens; both present means deny.",
     ["token", "deny", "approve", "substring", "reply"]),
    ("m1-grammar",
     "Session fact: the grammar bench ran 30 prompts on gemma:2b in two arms. "
     "Unconstrained: 0 of 30 outputs were valid JSON. With a JSON schema "
     "passed as the format field: 30 of 30 valid. The sampler holds the "
     "schema, not the model.",
     ["json", "schema", "format", "prompts", "valid"]),
    ("fullscan-429",
     "Session fact: the scheduled FullScan task burned 20,578 ledger rows "
     "over 11 days with 20,432 rows failing on HTTP 429 while Windows "
     "reported Last Result 0 the whole time. The task is now Disabled; the "
     "exit code lied about the outcome for 11 days.",
     ["429", "task", "rows", "exit", "fail"]),
    ("pack-shed",
     "Session fact: the boot context pack rendered 9471 chars against a 7200 "
     "char budget, so the shed ladder dropped the rib vault amendments block "
     "at stage 3 and the pack landed without the mechanism laws. Every seat "
     "boots through this door.",
     ["pack", "budget", "shed", "chars", "laws"]),
    ("stash-sweep",
     "Session fact: three git stashes sat parked on the shared tree across "
     "sibling seats. The new detector censuses stashes but has no drop or "
     "pop verb by design: it detects, it cannot prevent.",
     ["stash", "tree", "detector", "drop", "pop"]),
    ("hermes-402",
     "Session fact: the paid dispatch reserve math says a sonnet ask needs "
     "about 0.34 dollars while the balance is bounded between 0.16 and 0.17 "
     "dollars. The result is a deterministic 402 on every hourly fire, eight "
     "fires logged, never self-healing.",
     ["402", "balance", "reserve", "dollars", "dispatch"]),
    ("fold-mutex",
     "Session fact: the fold gate holds a mutex during the fold phase. When "
     "the gate is already held, prose routes to the local janitor with an "
     "enforced number rule that refused a summary which reformatted numbers "
     "with punctuation - the rule bites.",
     ["mutex", "gate", "fold", "numbers", "rule"]),
    ("gemma-garden",
     "Session fact: the local model garden holds 17 models including "
     "gemma:2b, qwen2.5:7b, and gemma4 at zero dollar cost. The new Google "
     "model that runs on nothing was already installed before the operator "
     "asked for it.",
     ["models", "garden", "local", "zero", "installed"]),
    ("roll-shape",
     "Session fact: the gauntlet register reads mistral laying exact 123.05 "
     "BPM grids to 8 counts and collapsing at 12, while qwen2.5:7b contested "
     "a hidden roll - a low-roll tell, not a capability gap. The register is "
     "the per-animal shape under pressure.",
     ["grid", "counts", "roll", "collapse", "register"]),
]
# 10 fresh + 3x the original contested sources = 13 prompts per cell
BATTERY = FRESH + [s for s in csp.SOURCES for _ in range(3)]

PLAN = [
    ("gemma:2b", "UNCONSTRAINED", None),
    ("gemma:2b", "FORMAT-SCHEMA", csp.SCHEMA),
    ("gemma4:latest", "FORMAT-SCHEMA", csp.SCHEMA),
    ("qwen2.5:7b", "FORMAT-SCHEMA", csp.SCHEMA),
]

JSONL = DIR / "comic_spec_trial30.jsonl"
SUMMARY_PATH = DIR / "comic_spec_trial30.json"


def main():
    summary = {}
    for seat, arm, schema in PLAN:
        hits = {"parseable": 0, "schema_ok": 0, "in_character": 0, "minimal": 0}
        n = 0
        for sid, fact, kws in BATTERY:
            t0 = time.time()
            text = csp.ask(seat, csp.PROMPT.format(fact=fact), schema)
            r, sample = csp.score(text, set(re.findall(r"\d+", fact)), kws)
            row = {"seat": seat, "arm": arm, "source": sid, **r,
                   "elapsed_s": round(time.time() - t0, 1),
                   "sample": sample[:160]}
            with JSONL.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            for k in hits:
                hits[k] += 1 if r[k] else 0
            n += 1
            print(seat, arm, sid, r, flush=True)
            time.sleep(1.0)
        summary[seat + " | " + arm] = dict(hits, n=n)
        print("CELL DONE", seat, arm, hits, "/", n, flush=True)
        SUMMARY_PATH.write_text(json.dumps(
            {"schema": "comic_spec_trial30.v1", "summary": summary,
             "note": "10 fresh + 3x original sources; seed unpinned; "
                     "same module as comic_spec_probe"},
            indent=2, ensure_ascii=False), encoding="utf-8")
    print("BANKED", SUMMARY_PATH)


if __name__ == "__main__":
    main()
