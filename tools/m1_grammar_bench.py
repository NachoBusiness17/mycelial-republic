#!/usr/bin/env python3
"""M1 grammar-decode bench (steals.md M1, one sitting, $0 local):
30 fleet-shape prompts x 2 arms (unconstrained vs format=<schema>) on gemma:2b.
Measures JSON-parse success rate. Hypothesis (arXiv 2609.23742): schema
validity is a sampler property - arm B should hit ~100 pct vs arm A's low base.
Banked: watch/inbox/48h_synth/m1_bench.json. CREATE_NO_WINDOW on win32."""
import json
import re
import subprocess

PROMPTS = [
    "Summarize session {n} as a tool call: pick the right tool and arguments for filing a burn receipt.",
    "Route this task {n}: which janitor lane and what confidence?",
    "Extract the entities from burn note {n} into structured form.",
    "Classify failure {n}: signature, severity, remedy class.",
    "Score this candidate {n}: promoted or rejected, with reasons array.",
    "Plan step {n} of a sweep: tool, target, expected output.",
    "Tag this receipt {n} with domain and era fields.",
    "Summarize drift pair {n} as a structured verdict row.",
    "Convert note {n} into a registry entry with id and stamp.",
    "Build the index row {n} for this artifact: path, bytes, kind.",
] * 3
SCHEMA = {
    "type": "object",
    "properties": {
        "tool": {"type": "string"},
        "confidence": {"type": "number"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
    },
    "required": ["tool", "confidence", "tags", "summary"],
}


def ask(prompt: str, schema, retries: int = 3):
    body = {"model": "gemma:2b", "prompt": prompt, "stream": False, "temperature": 0}
    if schema:
        body["format"] = schema
    for attempt in range(retries):
        try:
            r = subprocess.run(
                ["curl", "-s", "--max-time", "180",
                 "-X", "POST", "http://localhost:11434/api/generate",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps(body)],
                capture_output=True, text=True, timeout=200,
                creationflags=int(subprocess.CREATE_NO_WINDOW) if hasattr(subprocess, "CREATE_NO_WINDOW") else 0)
            d = json.loads(r.stdout)
            break
        except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError) as exc:
            if attempt < retries - 1:
                import time
                time.sleep(5 * (attempt + 1))
                continue
            print(f"WARN: all {retries} attempts failed: {exc}")
            return False
    text = d.get("response", "")
    try:
        json.loads(text)
        return True
    except Exception:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                json.loads(m.group(0))
                return True
            except Exception:
                return False
    return False


def arm(name, schema):
    results = []
    for i, p in enumerate(PROMPTS):
        ok = ask(p.format(n=i + 1), schema)
        results.append(ok)
    hits = sum(results)
    print(f"{name}: {hits}/{len(results)} valid JSON ({100.0 * hits / len(results):.1f} pct)")
    return hits, len(results)


if __name__ == "__main__":
    a_hits, a_n = arm("UNCONSTRAINED", None)
    b_hits, b_n = arm("FORMAT-SCHEMA", SCHEMA)
    out = {
        "schema": "m1_grammar_bench.v1",
        "model": "gemma:2b",
        "prompts": len(PROMPTS),
        "unconstrained_valid": a_hits,
        "unconstrained_n": a_n,
        "format_schema_valid": b_hits,
        "format_schema_n": b_n,
        "verdict": ("M1 CONFIRMED: schema arm wins" if b_hits > a_hits
                    else "M1 NOT REPRODUCED on gemma:2b"),
    }
    with open("watch/inbox/48h_synth/m1_bench.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("BANKED watch/inbox/48h_synth/m1_bench.json")
    print(json.dumps(out))
