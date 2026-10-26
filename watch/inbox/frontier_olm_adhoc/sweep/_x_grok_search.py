"""_x_grok_search.py - adhoc sweep seat: X search via the grok CLI subscription seat.

Door: grok.EXE headless (harness/grok_cli.py invocation shape), the funded
default for X work per RIB_DRIVING_LADDER_20260928. Every post URL this returns
is verified through api.fxtwitter.com before banking; grok output is discovery
only, never the quote source.

Laws held: CREATE_NO_WINDOW on the subprocess spawn (win32), no secrets printed,
stdout captured to a file under sweep/raw/x_grok/.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import time
from pathlib import Path

# walk up until the repo root marker (AGENTS.md) so the path bug that created
# watch/watch/ on the first run cannot recur (root cause: one parent short)
ROOT = Path(__file__).resolve().parent
while not (ROOT / "AGENTS.md").is_file() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
OUT_DIR = ROOT / "watch" / "inbox" / "frontier_olm_adhoc" / "sweep" / "raw" / "x_grok"
OUT_DIR.mkdir(parents=True, exist_ok=True)
GROK = Path.home() / ".grok" / "bin" / "grok.exe"

TOPIC_FILE = {
    "broad": """You have live X (Twitter) search. Use it. Do NOT substitute web browsing for X search.

TASK: Find X posts from the last 30 days (2026-09-11 through 2026-10-11) about multi-agent LLM orchestration and agent swarms. Topics in scope: (a) multi-agent / swarm scaling and its economics (tokens, cost, wall-clock); (b) agent consensus, voting, or debate as a correctness signal, and its failures; (c) orchestration frameworks and harnesses (fan-out width, parallel agents, subagent steering, dispatch shape); (d) emergent behavior in agent populations; (e) multi-agent system failures and incident reports.

DELIVERABLE FORMAT (plain text, one block per post, 15 to 25 posts):
URL: https://x.com/<handle>/status/<id>
HANDLE: @<handle>
DATE: YYYY-MM-DD
TEXT: <the post's exact text, verbatim, up to 500 chars>
WHY: <one line: which topic (a-e) and what it claims>

RULES:
- Only include posts you actually retrieved via X search or post fetch in this session. NO invented or guessed URLs, no posts from memory. If you cannot access X search at all, output exactly: X-SEARCH-UNAVAILABLE and stop.
- Prefer posts with substance (numbers, mechanisms, incident detail, benchmarks) over vibes.
- Do not include posts dated before 2026-09-11.

SUMMARY: <one line: how many posts found, which topics>""",
    "consensus": """You have live X (Twitter) search. Use it. Do NOT substitute web browsing for X search.

TASK: Find X posts from the last 30 days (2026-09-11 through 2026-10-11) about whether multi-agent / multi-model CONSENSUS, voting, or debate improves LLM correctness: self-consistency at the agent level, majority-vote failures, LLM-as-judge agreement problems, heterogeneous model swarms voting, quorum protocols for agents, consensus being wrong while confident. Also: posts about agent swarm scaling measurements (cost per outcome, tokens per agent, width vs capability).

DELIVERABLE FORMAT (plain text, one block per post, 10 to 20 posts):
URL: https://x.com/<handle>/status/<id>
HANDLE: @<handle>
DATE: YYYY-MM-DD
TEXT: <the post's exact text, verbatim, up to 500 chars>
WHY: <one line: what it claims>

RULES:
- Only include posts you actually retrieved via X search or post fetch in this session. NO invented or guessed URLs, no posts from memory. If you cannot access X search at all, output exactly: X-SEARCH-UNAVAILABLE and stop.
- Prefer posts with numbers, measurements, or named failure cases.
- Do not include posts dated before 2026-09-11.

SUMMARY: <one line: how many posts found>""",
}


def run(topic: str, max_turns: int = 20, timeout_s: int = 420) -> int:
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
    out = OUT_DIR / f"grok_xsearch_{topic}.txt"
    out.write_text(
        f"cmd: grok --prompt-file <{topic}.txt> --max-turns {max_turns}\n"
        f"exit: {proc.returncode} latency_ms: {dt}\n"
        f"--- stdout ---\n{proc.stdout or ''}\n--- stderr tail ---\n{(proc.stderr or '')[-3000:]}\n",
        encoding="utf-8",
        errors="replace",
    )
    print(f"[{topic}] exit={proc.returncode} latency_ms={dt} -> {out.name}")
    print((proc.stdout or "")[:2000])
    if proc.returncode != 0:
        print("STDERR:", (proc.stderr or "")[-1500:])
    return proc.returncode


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "broad"
    sys.exit(run(topic))
