# swarm1-deepseek-mag__desk_model_probe (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: `_bench_model` compares uncalibrated self-reported GPU split (`size_vram/size`) as a tiebreaker while tokens/sec is the only throughput signal, so a model fully offloaded still loses on higher tps | EVIDENCE: mag/desk_model_probe.py:146-176 | FIX: drop gpu_pct from the sort key; rank by tokens_per_sec then eval_ms only.
DEFECT 2: `_has_model` treats any tag sharing the base prefix as a match, so "qwen-desk-v2" satisfies the "qwen-desk" check | EVIDENCE: mag/desk_model_probe.py:45-46 | FIX: match exact name or `name + ":"` prefix, not bare `base + ":"`.
DEFECT 3: `ensure_qwen_desk` uses `_tags()` captured before the pull to decide the base exists, and the post-pull `ollama create` never re-verifies `qwen2.5:3b-instruct` is present | EVIDENCE: mag/desk_model_probe.py:49-88 | FIX: re-call `_tags()` after pull and loop `create` once on missing base.
DEAD-CODE: `PROBE_PROMPT`'s `has_canvas` test `"### Local"` is subsumed by the literal `"### Canvas edit"` also being required in practice, but the substring itself is never asserted on its own path | EVIDENCE: mag/desk_model_probe.py:159
ONE-SITTING FIX: remove `gpu_pct` from the winner sort tuple so ranking rests on measured throughput alone | EVIDENCE: mag/desk_model_probe.py:169-176
