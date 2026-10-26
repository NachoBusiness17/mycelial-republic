"""_sweff_x_grok_search.py - adhoc sweep seat (inference-efficiency): X search via grok CLI.

Door: grok.EXE headless, the funded default for X work per
RIB_DRIVING_LADDER_20260928 (laws.md:38). Discovery only; every post URL this
returns is verified through api.fxtwitter.com before banking (quote source of
record). Laws held: CREATE_NO_WINDOW on the win32 spawn, stdout captured under
sweep/raw/x_grok/.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / "AGENTS.md").is_file() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
OUT_DIR = ROOT / "watch" / "inbox" / "frontier_olm_adhoc" / "sweep" / "raw" / "x_grok"
OUT_DIR.mkdir(parents=True, exist_ok=True)
GROK = Path.home() / ".grok" / "bin" / "grok.exe"

COMMON = """You have live X (Twitter) search. Use it. Do NOT substitute web browsing for X search.

DELIVERABLE FORMAT (plain text, one block per post, 10 to 20 posts):
URL: https://x.com/<handle>/status/<id>
HANDLE: @<handle>
DATE: YYYY-MM-DD
TEXT: <the post's exact text, verbatim, up to 500 chars>
WHY: <one line: what it claims, with any numbers named>

RULES:
- Only include posts you actually retrieved via X search or post fetch in this session. NO invented or guessed URLs, no posts from memory. If you cannot access X search at all, output exactly: X-SEARCH-UNAVAILABLE and stop.
- Prefer posts with substance (measured numbers, benchmarks, mechanisms, incident detail) over vibes. Vendor marketing counts only if it carries a measurement.
- Do not include posts dated before 2026-09-11 (last 30 days). If the topic is thin, say so and list what you found anyway.

SUMMARY: <one line: how many posts found, what subtopics>"""

TOPIC_FILE = {
    "specdec": """
TASK: Find X posts from the last 30 days (2026-09-11 through 2026-10-11) about SPECULATIVE DECODING: acceptance rates, measured latency/speedup wins, draft-model choice (1B-3B drafts for 8B-70B targets, EAGLE/EAGLE-3, Medusa, self-speculative, ngram/prompt-lookahead), llama.cpp and Ollama speculative decoding experiences, vLLM/SGLang spec-decode benchmarks, when spec decode hurts (high batch, wrong draft family).""" + COMMON,
    "sched": """
TASK: Find X posts from the last 30 days (2026-09-11 through 2026-10-11) about INFERENCE SCHEDULING beyond prefix caching: distributed inference scheduling across multiple GPU nodes or multiple Ollama/llama.cpp instances, prefill/decode disaggregation, continuous batching tuning, multi-instance routing and load balancing for local LLM fleets, KV-cache-aware scheduling, heterogeneous GPU scheduling, queueing and SLO-aware serving, anything about orchestrating several small local models efficiently.""" + COMMON,
    "dskoff": """
TASK: Find X posts from the last 30 days (2026-09-11 through 2026-10-11) about (a) DeepSeek API with THINKING/DISABLED mode: measured speed, price per task, or quality of non-thinking mode vs thinking mode; (b) reasoning models whose hidden reasoning eats the completion budget and returns EMPTY content, re-fire costs, reasoning-token billing waste, API fields like reasoning_content or thinking:{"type":"disabled"}; (c) any measured comparison of the same job with thinking on vs off (tokens, cents, latency).""" + COMMON,
}


def run(topic: str, max_turns: int = 18, timeout_s: int = 420) -> int:
    prompt = TOPIC_FILE[topic]
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8", dir=str(OUT_DIR)
    ) as tf:
        tf.write(prompt)
        prompt_path = tf.name
    cmd = [
        str(GROK),
        "--prompt-file",
        prompt_path,
        "--cwd",
        str(OUT_DIR),
        "--output-format",
        "plain",
        "--max-turns",
        str(max_turns),
        "--no-auto-update",
        "--deny",
        "Bash(rm*)",
        "--deny",
        "Bash(*Remove-Item*)",
    ]
    t0 = time.monotonic()
    flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout_s,
        cwd=str(OUT_DIR),
        creationflags=flags,
    )
    dt = int((time.monotonic() - t0) * 1000)
    out = OUT_DIR / f"grok_xsearch_{topic}_20261011.txt"
    out.write_text(
        f"cmd: grok --prompt-file <{topic}.txt> --max-turns {max_turns}\n"
        f"exit: {proc.returncode} latency_ms: {dt}\n"
        f"--- stdout ---\n{proc.stdout or ''}\n--- stderr tail ---\n{(proc.stderr or '')[-3000:]}\n",
        encoding="utf-8",
        errors="replace",
    )
    print(f"[{topic}] exit={proc.returncode} latency_ms={dt} -> {out.name}")
    print((proc.stdout or "")[:1500])
    if proc.returncode != 0:
        print("STDERR:", (proc.stderr or "")[-1200:])
    return proc.returncode


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "specdec"
    sys.exit(run(topic))
