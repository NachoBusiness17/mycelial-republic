"""corpus_lens_run — synchronously finish lens analyses to completion.

The queue can preempt mid-flight lens tasks (they sample the corpus then stall).
This runs each remaining lens to completion on the cheap DeepSeek tier directly,
reusing the corpus samples already extracted by the earlier agent pass, and writes
<lens>.md + appends a training record. Deterministic finish, no queue dependency.

Usage:
  python -m tools.corpus_lens_run <lens_dir> [--lenses bard,evolution,semantic,behavioral,safety]
      [--model deepseek-v4-flash] [--ctx 120000]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx


def _api() -> tuple[str, str, str]:
    """Return (base_url, model, api_key) for DeepSeek."""
    base = "https://api.deepseek.com/v1"
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from tools.estate_env import key as env_key  # the one canonical loader
    key = env_key("DEEPSEEK_API_KEY") or ""
    return base, key


def _chat(base: str, key: str, model: str, system: str, user: str) -> str:
    with httpx.Client(timeout=420.0) as c:
        r = c.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.3,
                "max_tokens": 12000,
            },
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


def _context(lens_dir: Path, cap: int) -> str:
    """Build bounded corpus context from the already-extracted sample dumps."""
    parts: list[str] = []
    total = 0
    for f in sorted(lens_dir.glob("_sample_dump*.txt")) + sorted(lens_dir.glob("_extract.txt")):
        t = f.read_text(encoding="utf-8", errors="replace")
        if total + len(t) > cap:
            parts.append(t[: cap - total])
            total = cap
            break
        parts.append(t)
        total += len(t)
    return "\n\n".join(parts)


def run_one(lens_dir: Path, lens: dict, base: str, key: str, model: str, ctx: int) -> dict:
    spec = lens_dir / f"{lens['name']}.spec.json"
    spec_data = json.loads(spec.read_text(encoding="utf-8")) if spec.is_file() else lens
    context = _context(lens_dir, ctx)
    system = (
        "You are a specialist research analyst given a corpus of AI steering/prompt "
        "documents. Produce a rich, faithful, well-structured analysis in Markdown. "
        "Quote file names and concrete lines. Be balanced, concrete, no fluff."
    )
    user = (
        f"{spec_data.get('task', lens['prompt'])}\n\n"
        f"CORPUS CONTEXT (sampled from {lens_dir.parent.name}):\n{context}\n\n"
        f"Deliverable: a complete Markdown analysis for the '{lens['name']}' lens. "
        "Be thorough but focused."
    )
    out = _chat(base, key, model, system, user)
    md = lens_dir / f"{lens['name']}.md"
    md.write_text(out, encoding="utf-8")

    rec = {
        "schema": "corpus_lens.v1",
        "lens": lens["name"],
        "focus": lens.get("focus"),
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": model,
        "chars": len(out),
        "path": str(md),
        "summary": out.splitlines()[0][:120] if out else "",
    }
    tr = lens_dir / "_lens_training.jsonl"
    with tr.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, default=str) + "\n")
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("lens_dir")
    ap.add_argument("--lenses", default="bard,evolution,semantic,behavioral,safety")
    ap.add_argument("--model", default="deepseek-v4-flash")
    ap.add_argument("--ctx", type=int, default=120000)
    args = ap.parse_args()

    lens_dir = Path(args.lens_dir)
    base, key = _api()
    if not key:
        print("ERROR: DEEPSEEK_API_KEY not found", file=sys.stderr)
        return 1

    # lens definitions mirror corpus_lens.LENSES
    LENSES = {
        "bard": {"name": "bard", "focus": "narrative / thematic",
                 "prompt": "You are a bard who has read an entire archive. Tell the coherent STORY of this system: who/what it claims to be, its mythology, command structure, goal, and how it talks to its user. Quote distinctive phrases. Be vivid but faithful."},
        "evolution": {"name": "evolution", "focus": "version-diff interpretation",
                      "prompt": "Using the diff training data (added/removed lines, similarity, delta categories), explain WHY these documents differ and what each revision does. Infer the design trajectory across versions. Be concrete about purpose."},
        "semantic": {"name": "semantic", "focus": "topic / thematic clustering",
                     "prompt": "Cluster the corpus by topic/theme and intent. Identify recurring concepts, symbols, code-names, and semantic families. Map central vs peripheral themes. Provide a thematic map with examples."},
        "behavioral": {"name": "behavioral", "focus": "activation & response patterns",
                       "prompt": "Analyze the ACTIVATION and RESPONSE patterns the system encodes: what triggers it into action, what responses/behaviors it commands, its tone/persona shifts, and how it would behave as an AI assistant. Make the behavioral contract explicit (for comparison against other AI system-prompt archives)."},
        "safety": {"name": "safety", "focus": "instructions / jailbreak / risk",
                   "prompt": "Audit this corpus for instruction/safety characteristics: what it tells an AI to do, any persuasion/social-engineering, activation rituals, grandiose claims, or concerning directives. Categorize risk levels and quote the most consequential lines. Be balanced, not alarmist."},
        "structure": {"name": "structure", "focus": "prompt-engineering architecture",
                      "prompt": "Reverse-engineer the PROMPT ARCHITECTURE: system-role, persona, activation sequence, command verbs, response protocol, gates/levels/versions, and how it steers an LLM. Structural breakdown with cited examples."},
    }

    done = []
    for name in [x.strip() for x in args.lenses.split(",") if x.strip()]:
        lens = LENSES.get(name)
        if not lens:
            print("skip unknown lens:", name)
            continue
        rec = run_one(lens_dir, lens, base, key, args.model, args.ctx)
        print(f"[ok] {name}: {rec['chars']} chars -> {rec['path']}", flush=True)
        done.append(name)
    print("DONE:", done)
    return 0


if __name__ == "__main__":
    sys.exit(main())
