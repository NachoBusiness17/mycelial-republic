"""corpus_lens — run a corpus through bard + swarm-protocol analysis lenses.

The operator's pipeline (2026-08-08):
  1. harvest a Drive corpus (tools/steal_gdrive.py)
  2. diff near-duplicate versions (tools/corpus_diff.py) -> training data
  3. THIS: analyze the corpus through multiple LENSES and emit rich per-lens data:
       - bard      : narrative/thematic — "tell the story of this system"
       - structure : prompt-engineering architecture (activation/response protocol)
       - evolution : why the version-diffs exist + what each revision does
       - semantic  : topic/thematic clustering across the corpus
       - behavioral: what activation & response patterns it encodes
       - safety    : what it instructs / jailbreak / activation / risk flags
  Each lens runs as a QUEUE task on the cheap tier (deepseek-v4-flash) per the
  "restful cheap orchestration" doctrine, writing <out>/<lens>.md + appending a
  training record to <out>/_lens_training.jsonl.

Usage:
  python -m tools.corpus_lens <corpus> --out <lens_out> [--manifest M] [--diff T]
      --provider deepseek --model deepseek-v4-flash
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LENSES = [
    {
        "name": "bard",
        "focus": "narrative / thematic",
        "prompt": (
            "You are a bard who has read an entire archive of documents. Tell the "
            "coherent STORY of what this system is: who/what it claims to be, its "
            "mythology, its command structure, its goal, and how it talks to its "
            "user. Quote distinctive phrases. Be vivid but faithful to the text."
        ),
    },
    {
        "name": "structure",
        "focus": "prompt-engineering architecture",
        "prompt": (
            "Reverse-engineer the PROMPT ARCHITECTURE of this system: system-role, "
            "persona, activation sequence, command verbs, response protocol, any "
            "gates/levels/versions, and how it is engineered to steer an LLM. Give a "
            "structural breakdown with cited examples."
        ),
    },
    {
        "name": "evolution",
        "focus": "version-diff interpretation",
        "prompt": (
            "Using the diff training data (added/removed lines, similarity, delta "
            "categories), explain WHY these documents differ and what each revision "
            "does. Infer the design trajectory (what was added, removed, hardened, "
            "or renamed across versions). Be concrete about purpose."
        ),
    },
    {
        "name": "semantic",
        "focus": "topic / thematic clustering",
        "prompt": (
            "Cluster the corpus by topic/theme and intent. Identify the recurring "
            "concepts, symbols, code-names, and semantic families. Map which themes "
            "are central vs peripheral. Provide a thematic map with representative "
            "examples."
        ),
    },
    {
        "name": "behavioral",
        "focus": "activation & response patterns",
        "prompt": (
            "Analyze the ACTIVATION and RESPONSE patterns the system encodes: what "
            "triggers it into action, what responses/behaviors it commands, its "
            "tone/persona shifts, and how it would behave as an AI assistant. This "
            "is for comparing against other AI system-prompt archives — make the "
            "behavioral contract explicit."
        ),
    },
    {
        "name": "safety",
        "focus": "instructions / jailbreak / risk",
        "prompt": (
            "Audit this corpus for instruction/safety characteristics: what it tells "
            "an AI to do, any persuasion/social-engineering, activation rituals, "
            "grandiose claims, or concerning directives. Categorize risk levels and "
            "quote the most consequential lines. Be balanced, not alarmist."
        ),
    },
]

SCHEMA = "corpus_lens.v1"


def _write_lens_spec(out: Path, lens: dict, corpus: str, manifest: str, diff: str) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    spec = {
        "schema": SCHEMA,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lens": lens["name"],
        "focus": lens["focus"],
        "task": lens["prompt"],
        "inputs": {
            "corpus": corpus,
            "manifest": manifest,
            "diff_training": diff,
            "sample_limit": 60,
        },
        "deliverable": (
            "Write a rich analysis to <out>/<lens>.md and append one JSON training "
            "record (schema corpus_lens.v1: lens, focus, ts, summary, findings[], "
            "quotes[]) to <out>/_lens_training.jsonl. Be concrete, cite file names."
        ),
    }
    p = out / f"{lens['name']}.spec.json"
    p.write_text(json.dumps(spec, indent=2, default=str), encoding="utf-8")
    return p


def enqueue(corpus: str, out: str, manifest: str, diff: str, provider: str, model: str) -> dict:
    out_dir = Path(out)
    tasks: list[dict] = []
    for lens in LENSES:
        spec = _write_lens_spec(out_dir, lens, corpus, manifest, diff)
        from mag.orchestrator import spawn_task

        goal = (
            f"Execute the lens spec at {spec}. Read the corpus manifest ({manifest}), "
            f"the diff training data ({diff}), and sample up to 60 "
            f"documents from {corpus}. {lens['prompt']} "
            f"Deliverable: write {out_dir / lens['name']}.md and append a training record "
            f"to {out_dir / '_lens_training.jsonl'}."
        )
        r = spawn_task(goal=goal, provider=provider, model=model, tag="corpus-lens")
        tasks.append({"lens": lens["name"], "spec": str(spec), **r})
    idx = {
        "schema": SCHEMA, "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "corpus": corpus, "lenses": [l["name"] for l in LENSES], "tasks": tasks,
    }
    (out_dir / "_lens_index.json").write_text(json.dumps(idx, indent=2, default=str), encoding="utf-8")
    return idx


def analyze_if_fresh(corpus: Path, provider: str = "deepseek", model: str = "deepseek-v4-flash") -> dict:
    """Run diff + enqueue lenses for a corpus unless a fresh harvest was already analyzed."""
    if not corpus.is_dir():
        return {"skip": "no dir", "corpus": str(corpus)}
    manifest = corpus / "_manifest.json"
    if not manifest.is_file():
        return {"skip": "no manifest", "corpus": str(corpus)}
    out = corpus / "_lenses"
    idx = out / "_lens_index.json"
    if idx.is_file() and idx.stat().st_mtime >= manifest.stat().st_mtime:
        return {"skip": "fresh", "corpus": str(corpus)}
    from tools.corpus_diff import run as diff_run

    diff_res = diff_run(corpus, corpus / "_diffs", 0.3)
    enq = enqueue(str(corpus), str(out), str(manifest),
                  str(corpus / "_diffs" / "_training.jsonl"), provider, model)
    return {"corpus": str(corpus), "diff_records": diff_res.get("diff_records"),
            "lenses_enqueued": len(enq["tasks"])}


def run_cadence(root: Path | None = None) -> dict:
    """Scan a research root for fresh harvests and auto-analyze them (diff + lenses)."""
    from config import ROOT

    root = root or (ROOT.parent / "research")
    if not root.is_dir():
        return {"skip": "no research root", "root": str(root)}
    results = []
    for corpus in sorted(p for p in root.iterdir() if p.is_dir() and (p / "_manifest.json").is_file()):
        results.append(analyze_if_fresh(corpus))
    return {"root": str(root), "results": results}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("corpus")
    ap.add_argument("--out", required=True)
    ap.add_argument("--manifest", default="")
    ap.add_argument("--diff", default="")
    ap.add_argument("--provider", default="deepseek")
    ap.add_argument("--model", default="deepseek-v4-flash")
    args = ap.parse_args()

    corpus = Path(args.corpus)
    manifest = args.manifest or str(corpus / "_manifest.json")
    diff = args.diff or str(corpus / "_diffs" / "_training.jsonl")
    idx = enqueue(str(corpus), args.out, manifest, diff, args.provider, args.model)
    print(json.dumps({"enqueued": len(idx["tasks"]), "tasks": [
        {"lens": t["lens"], "task_id": t.get("task_id"), "ok": t.get("ok")} for t in idx["tasks"]
    ]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
