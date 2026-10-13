"""seed_salon — multi-model salon on the seed's enhancement questions (2026-09-25).
Runs the same brief across independent cheap/free lanes, files each position to
watch/inbox/, and prints where the file landed. Chair texts converge on the same
anchors; disagreement between seats is signal, unanimity under a leading question
is nothing (SALON.md).
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception as exc:  # 2026-09-25 ratchet debt cleared: silent pass hid why salon unicode names could mojibake on redirected stdout; valueless consoles keep default encoding, now named on stderr
    print(f"[seed_salon] stdout reconfigure skipped: {exc}", file=sys.stderr)

from models.env_load import load_dotenv
load_dotenv()
from mag import lite_guard  # noqa: E402
from mag.key_law import get  # noqa: E402

SEEDS = [
    ("deepseek", "https://api.deepseek.com/chat/completions", "deepseek", "deepseek-chat"),
    ("groq", "https://api.groq.com/openai/v1/chat/completions", "groq_1", "openai/gpt-oss-120b"),
    ("together", "https://api.together.xyz/v1/chat/completions", "together",
     "deepseek-ai/DeepSeek-V4-Flash-0731"),
]

INDUSTRY = """Industry standard practices to map against (from the estate's own 36-item prior-art sweep):
1. AGENTS.md standard (~60k repos): vendor-neutral filename tools auto-load; nested precedence.
2. Anthropic Agent Skills (agentskills.io): YAML frontmatter name/description IS the discovery API; progressive disclosure keeps context cheap.
3. Cookiecutter Data Science: installer CLI scaffolds a project in one command.
4. 12-Factor Agents: named-factor vocabulary as shared language.
5. Semantic versioning + changelog + tests-as-contract (any mature OSS).
6. GitHub Marketplace / skill registries: distribution is the moat.
7. Ralph loop: self-executing pass condition spread as folklore.
8. OpenClaw critique: self-hosted runtimes die on security; one-door + seal is the answer."""


def brief() -> str:
    method = (ROOT / "seed" / "THE_METHOD.md").read_text(encoding="utf-8")[:2200]
    return (f"You are one seat in a multi-model salon. The subject: a 60KB 'seed' package that ships a "
            f"human+AI operating METHOD (11 laws, 13 python engines, docs: accounts playbook for doubled "
            f"free tiers, VS Code path, data-tier sovereignty, salon rules, morning loop, tour).\n\n"
            f"=== THE METHOD (laws) ===\n{method}\n\n=== INDUSTRY PRACTICES ===\n{INDUSTRY}\n\n"
            "Your job: (1) MAP each industry practice onto the seed — adopt/adapt/reject with one line of "
            "teeth each; (2) propose the 5 highest-value ENHANCEMENTS that make the seed adoptable by "
            "strangers (concrete: file format, install step, distribution move); (3) name the ONE enhancement "
            "that matters most and why. Under 700 words, concrete, no preamble. End with 'CHAIR VERDICT:' "
            "and your one-line position.")


def seat(name: str, url: str, key_canon: str, model: str) -> None:
    if not lite_guard._safe_https_url(url):
        raise RuntimeError(f"SSRF guard rejected url: {url}")
    key = get(key_canon)
    if not key:
        print(f"{name}: no key — skipped")
        return
    body = json.dumps({"model": model, "messages": [
        {"role": "system",
         "content": "You are an independent reviewer. Do not defer to consensus; "
                    "push back where wrong."},
        {"role": "user", "content": brief()}], "max_tokens": 1500, "temperature": 0.5}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "User-Agent": "mag-estate-seed-salon/1.0"})
    t0 = time.time()
    with lite_guard._OPENER.open(req, timeout=180) as r:
        out = json.loads(r.read().decode())
    content = (out.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
    ms = round(time.time() - t0)
    outp = ROOT / "watch" / "inbox" / f"SEED_SALON_{name}_{time.strftime('%Y%m%d')}.md"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(
        f"# Seed salon — {name} seat ({model})\n\n*{ms}ms, free/cheap lane*\n\n{content}",
        encoding="utf-8", newline="\n")
    print(f"{name}: {len(content)} chars in {ms}ms -> {outp.name}")


if __name__ == "__main__":
    for n, u, k, m in SEEDS:
        try:
            seat(n, u, k, m)
        except Exception as e:  # noqa: BLE001 — one dead seat must not kill the salon
            print(f"{n}: FAILED {type(e).__name__}: {str(e)[:120]}")
