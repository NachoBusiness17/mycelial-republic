#!/usr/bin/env python3
"""fold_prose_local: FOLD-FAST - the fold's prose half on the local janitor.

Operator order 2026-10-07 ("go"): workflow folds always hang. Decomposition:
the counting script (tools/mickey17_v2_fold.py) is deterministic and bounded;
the hang-prone half is the cloud folder agent that turns scripted numbers
into prose. When the fold gate is contended, this tool routes that prose to
the local janitor (Ollama qwen2.5:7b class) at $0 with no account queue -
driving-ladder law: summarization over script-written numbers is janitor
class, and the funded-tier fresh reader still verifies in REVIEW.

HARD LAWS carried here:
  - ENDPOINT IS A LITERAL IP CONNECTION: a raw http.client connection to
    127.0.0.1:11434 (the single sanctioned local Ollama). No URL assembly,
    no DNS, no redirects, nothing configurable (the Mimosa SSRF findings
    2026-10-07 rejected the configurable-URL shapes twice).
  - The sections file is AUTHORITATIVE and lands in the master VERBATIM;
    the model writes only the short summary header, under the rule that
    every number it writes must appear in the sections bytes.
  - One shot, bounded timeout; on any model failure exit 3 so the engine
    falls back to the cloud folder. Never half-write: the master is written
    only after a successful model call.
  - Counts are parsed from the sections deterministically (never asked of
    the model): top_steal_count = bullet rows in the TOP STEALS/EXECUTIONS
    section; disputed_count = bullet rows in DISPUTED; -1 when absent.

Usage:
  python -m tools.fold_prose_local --run <slug> --master <ws fold path> \
      --estate-copy <estate fold path> [--genre execute] [--model qwen2.5:7b]
  python -m tools.fold_prose_local --selftest   # parse checks, no model
Exit: 0 folded / 3 model failure / 2 usage or missing sections.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "memory" / "runs" / "mickey17_v2" / "runs"
SECTIONS_NAME = "FOLD_SECTIONS.md"

GENRE_TITLES = {
    "execute": "EXECUTE-THE-REGISTER fold (local janitor prose)",
    "audit": "MICKEY-17 claim-surface audit fold (local janitor prose)",
    "estate-read": "READ-THE-ESTATE fold (local janitor prose)",
}

SUMMARY_INSTRUCTION = (
    "You are writing the short summary header for a run fold document. "
    "Below are the AUTHORITATIVE counted sections. Write at most 3 plain "
    "sentences: what this run was, and its headline outcome. HARD RULE: "
    "every number you state must appear verbatim in the sections bytes; "
    "invent nothing; no em-dashes; no markdown headings."
)


def parse_counts(sections: str) -> tuple[int, int]:
    """Deterministic counts from the sections bytes (never the model)."""
    top = disp = -1
    current = None
    for line in sections.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            head = stripped.upper()
            if "TOP STEAL" in head or "EXECUTION" in head:
                current, top = "top", 0 if top < 0 else top
            elif "DISPUT" in head:
                current, disp = "disp", 0 if disp < 0 else disp
            else:
                current = None
            continue
        if stripped.startswith(("-", "*")) and current == "top":
            top = max(top, 0) + 1
        elif stripped.startswith(("-", "*")) and current == "disp":
            disp = max(disp, 0) + 1
    return top, disp


def ollama_summary(sections_head: str, model: str, timeout: int) -> str:
    """One bounded call to the single sanctioned endpoint.
    SSRF fence (Mimosa cure): no URL assembly surface at all - a raw
    http.client connection to the IP literal 127.0.0.1:11434. Nothing to
    resolve, nothing to redirect, nothing to rebind; scheme, host, and port
    are constants."""
    import http.client
    body = json.dumps({
        "model": model,
        "prompt": SUMMARY_INSTRUCTION + "\n\n=== SECTIONS (authoritative) "
                  "===\n" + sections_head[:8000],
        "stream": False,
        "options": {"num_predict": 220, "temperature": 0.2},
    }).encode()
    conn = http.client.HTTPConnection("127.0.0.1", 11434, timeout=timeout)
    try:
        conn.request("POST", "/api/generate", body=body,
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        raw = resp.read()
    finally:
        conn.close()
    if resp.status != 200:
        raise RuntimeError("ollama HTTP " + str(resp.status))
    d = json.loads(raw.decode())
    text = str(d.get("response", "")).strip()
    if not text:
        raise RuntimeError("empty completion")
    # the hard rule, enforced but fair: any number the model wrote must
    # exist somewhere in the authoritative sections. Tokens are stripped of
    # list punctuation first (the model may reformat "20261006" as
    # "2026-10-06" - the fragments all exist; only an INVENTED number,
    # absent from the sections entirely, fails) - and the check runs
    # against the FULL sections, not just the prompted head.
    numbers = {t.strip(".,") for t in re.findall(r"\d[\d,.]*", text)}
    numbers.discard("")
    missing = [n for n in numbers if n not in sections_head]
    if missing:
        raise RuntimeError("number rule violated: " + ", ".join(missing[:5]))
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="")
    ap.add_argument("--sections", default="")
    ap.add_argument("--master", required=True)
    ap.add_argument("--estate-copy", required=True)
    ap.add_argument("--genre", default="execute")
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.sections:
        sections_path = Path(args.sections)
    elif args.run:
        sections_path = RUNS / args.run / SECTIONS_NAME
    else:
        print("usage: --run or --sections required", file=sys.stderr)
        return 2
    if not sections_path.is_file():
        print("sections missing: " + str(sections_path), file=sys.stderr)
        return 2
    sections = sections_path.read_text(encoding="utf-8", errors="replace")
    top, disp = parse_counts(sections)

    if args.selftest:
        print(json.dumps({"selftest": "ok", "top_steal_count": top,
                          "disputed_count": disp}))
        return 0

    try:
        summary = ollama_summary(sections, args.model, args.timeout)
    except Exception as e:
        print("FOLD-FAST model failure: " + str(e)[:200], file=sys.stderr)
        return 3

    title = GENRE_TITLES.get(args.genre, GENRE_TITLES["audit"])
    master = (f"# {title}\n\n## SUMMARY (local janitor; numbers verified "
              f"against sections)\n\n{summary}\n\n"
              "## COUNTED SECTIONS (authoritative, verbatim from "
              "tools/mickey17_v2_fold.py)\n\n" + sections)
    master_path = Path(args.master)
    estate_path = Path(args.estate_copy)
    master_path.parent.mkdir(parents=True, exist_ok=True)
    estate_path.parent.mkdir(parents=True, exist_ok=True)
    master_path.write_text(master, encoding="utf-8")
    estate_path.write_text(master, encoding="utf-8")
    print(json.dumps({
        "estate_fold": str(estate_path),
        "workspace_fold": str(master_path),
        "top_steal_count": top,
        "disputed_count": disp,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
