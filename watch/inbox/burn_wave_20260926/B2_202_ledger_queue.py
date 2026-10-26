# B2-202 close: append the LEDGER row (json.dumps, never heredoc) and self-feed
# briefs to QUEUE.md under Open. Queue numbers are computed from the live file
# max at write time (B2-61 pattern) to avoid the concurrent-number race. The
# em-dash guard runs over every appended string (B2-167 law).
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LEDGER = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")
QUEUE = os.path.join(HERE, "QUEUE.md")

ROW = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "slug": "B2-202-free-rotation",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_202_free_rotation_20260926.md",
    "one_line": (
        "openrouter :free rotation second pass landed live on 2026-09-26 bytes under the "
        "lane's own CLAIM configs/providers.yaml 22:55:17Z: the 9 catalog ids holding no "
        "row in B2_295_gate_results*.json (17 catalog ids minus the 8 the B2-295 first "
        "pass gated) ran tools/openrouter_free_gate.py one chat gate each at 4s spacing, "
        "8/9 PASS earned their providers.yaml openrouter lines with dated gate comments "
        "(dots-studio/dots-3-note-preview:free, inclusionai/ling-3.0-flash-fin:free, "
        "inclusionai/ling-3.0-flash-sante:free, "
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, "
        "nvidia/nemotron-3-super-120b-a12b:free, nvidia/nemotron-3-ultra-550b-a55b:free, "
        "nvidia/nemotron-3.5-content-safety:free, poolside/laguna-s-2.1:free; "
        "thinkingmachines/inkling:free FAIL 403 agents-only, no line), byte evidence "
        "watch/inbox/burn_wave_20260926/B2_202_gate_results.json; existing 6 lines "
        "untouched, the claim's one in-block comment edit spent extending the no-line "
        "list to all five gate-FAILED ids across both passes (adding the B2-295-run-2 "
        "gemma-4-26b-a4b 429); validation load_providers() 28 providers, openrouter "
        "roster 6 to 14, raw yaml.safe_load green; full 17-id catalog census now "
        "gate-covered across B2-295 + B2-202; QUEUE B2-202 row found pre-checked on "
        "fresh read, landing note anchored per the B2-238 law; self-feeds B2-5xx "
        "retest-cadence, reasoning-budget-floor, quota-arithmetic"
    ),
}

BRIEFS = [
    (
        "Retest cadence for the openrouter gate-FAILED list: the openrouter block "
        "no-line comment now names 5 ids across both passes and the classes differ "
        "(qwen/qwen3.8-27b:free 429, google/gemma-4-31b-it:free 429, "
        "google/gemma-4-26b-a4b-it:free 429 are shared-pool contention that flips with "
        "time of day; thinkingmachines/inkling-small:free 403 and "
        "thinkingmachines/inkling:free 403 are agents-only tier gates that never flip), "
        "so run one spaced off-peak retest over just the 429 trio with "
        "tools/openrouter_free_gate.py and split the comment into retriable-429 vs "
        "permanent-403 so sweeps stop re-testing the never-pass ids; falsifier: a 403 "
        "id left in the retriable list, or a 429 id still untested 48h later; pointers "
        "configs/providers.yaml openrouter no-line comment + "
        "watch/inbox/burn_wave_20260926/B2_202_gate_results.json."
    ),
    (
        "Reasoning budget floor for the 4 new reasoning-bearing :free lanes: the "
        "B2-202 gate shows nvidia/nemotron-3-super-120b-a12b:free and "
        "nvidia/nemotron-3-ultra-550b-a55b:free spend part of a 16-token budget on "
        "visible reasoning-style content while still answering, and the openrouter "
        "block already carries the openrouter/auto scar (thinks anyway, 600 tokens "
        "empty, disable_thinking ignored); probe nemotron-3-nano-omni-30b-a3b-reasoning, "
        "nemotron-3-super-120b-a12b, nemotron-3-ultra-550b-a55b and "
        "nemotron-3.5-content-safety at 64/256/1536 max_tokens naming where content "
        "goes empty vs nonempty and whether disable_thinking changes anything, then pin "
        "the min budget in the block comment like the deepseek law; falsifier: a lane "
        "at its measured safe budget returning empty content with finish_reason length; "
        "pointers configs/providers.yaml openrouter block (auto scar comment + "
        "disable_thinking flag) + watch/inbox/burn_wave_20260926/B2_202_gate_results.json."
    ),
    (
        "Openrouter capacity arithmetic reconciliation: the lane header comment still "
        "advertises free lanes at 18 lanes x 1000/day while the openrouter quota block "
        "is monthly max_calls 200 / max_tokens 500000 and the chat-gated roster just "
        "grew to 14 ids (B2-295 + B2-202), so the provider-level budget gate in the "
        "quota block binds long before any per-lane free-tier limit; read which number "
        "is real for routing (grep the header claim's origin), reconcile header vs "
        "quota block vs roster in one comment or split them into honest labels; "
        "falsifier: any doc still quoting the 18-lane figure without the quota-block "
        "caveat; pointers configs/providers.yaml openrouter block + models/quota.py "
        "budget gating."
    ),
]


def guard(text):
    if "\u2014" in text:
        raise SystemExit("em-dash law violation in appended text")
    return text


def main():
    row = dict(ROW)
    row["one_line"] = guard(row["one_line"])
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("LEDGER row appended")

    with open(QUEUE, encoding="utf-8", errors="replace") as f:
        q = f.read()
    nums = [int(m) for m in re.findall(r"B2-(\d+)", q)]
    start = max(nums) + 1
    lines = [""] + [
        "- [ ] B2-%d %s" % (start + i, guard(brief))
        for i, brief in enumerate(BRIEFS)
    ]
    with open(QUEUE, "a", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines) + "\n")
    print("QUEUE self-feed appended: B2-%d..B2-%d" % (start, start + len(BRIEFS) - 1))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
