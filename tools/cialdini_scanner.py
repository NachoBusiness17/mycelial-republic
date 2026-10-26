"""cialdini_scanner - the 7-pattern persuasion detector for the intake path.

OPERATOR GENESIS: DOUBLE_DROP_20261001.md (watch/inbox/DOUBLE_DROP_20261001.md).
Researchers ran 28,000 ChatGPT conversations applying Robert Cialdini's 7 principles
of influence (authority, commitment, social proof, liking, reciprocity, scarcity,
unity) to objectionable requests: direct asks held at 33% compliance, persuasion
framing hit 72%, and the commitment ladder (tiny innocent premise first) drove
follow-up compliance to ~100%. The estate is a feed-driven architecture: X-dig and
scout lanes mine hostile web content and act on it, so every mined post is untrusted
input entering an agentic loop. Our gates block secrets and SSRF; nothing scanned
INGESTED CONTENT for persuasion-pattern payloads aimed at the lane that reads it.
This closes that gap 7 (persuasion payloads on the intake path, the Cialdini class).

STEAL ANALYSIS:
  * EXTERNAL - Cialdini's 7 influence principles as the enumerated payload class.
    Each principle becomes a deterministic regex family with a confidence weight.
    Regexes match PAYLOAD shapes (role-assertion plus command, tiny-yes then big
    ask, count plus cohort, deadline plus scarcity, in-group plus concealment,
    give-then-ask, flattery-plus-exception) rather than bare topic words, so
    estate receipts that discuss these topics do not false-positive.
  * SELF - the shape is prompt_lance (mag/prompt_lance.py): deterministic stdlib
    heuristics, $0, no model calls, no network, findings located by line, sorted
    deterministically, byte-identical output for identical input bytes. Like
    prompt_lance it is a LENS, not an authority: the wiring decides what to do
    with the verdict (flag at ingest, gate at action time).

PATTERNS (Cialdini, influence principle -> regex family -> confidence):
  1. authority      - role/official-assertion used to make the READER comply   (0.70-0.90)
  2. commitment     - commitment ladder: tiny yes first, then the big ask      (0.70-0.90)
  3. social_proof   - count + cohort ("N agents/teams/people already ...")     (0.70-0.80)
  4. scarcity       - deadline / limited supply pressure ("act now")           (0.70-0.90)
  5. unity          - in-group frame ("fellow agents like us")                 (0.75-0.85)
  6. reciprocity    - give-then-ask hook ("I gave you X, in return you owe")   (0.70-0.90)
  7. liking         - flattery mirror ("you're so capable, I know you can")    (0.75-0.85)

Schema: cialdini_scanner.v1 - deterministic $0 - CLI: python tools/cialdini_scanner.py <file|->
Wiring: tools/x_churn_cli.py + tools/x_churn_grok.py (X-dig intake) flag scanned
posts at ingest; mag/frontier_scout.py queue_steal_task gates the read-to-action
conversion at HIGH_RISK confidence.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception as exc:  # 2026-10-03 violation_ratchet except-pass rule + FW-46 shape
    # (mag/afk_loop.py:36): a valueless console keeps the default encoding and the
    # reason is named on stderr; never silently swallowed
    print(f"[cialdini_scanner] stdout reconfigure skipped: {exc}", file=sys.stderr)

SCHEMA = "cialdini_scanner.v1"

# confidence at/above which wiring treats a payload as actionable risk
HIGH_RISK = 0.7

# global cap on findings (deterministic document-order truncation)
_CAP = 50

_MAX_EXCERPT = 160


def _c(pattern: str, weight: float) -> tuple[re.Pattern[str], float]:
    return re.compile(pattern, re.I), weight


# Each entry: (id, code, name, [(compiled_regex, weight)]).
# Weights are the per-regex confidence of the payload shape; a finding for a
# (pattern, line) pair carries the max weight of the regexes that hit that line.
PATTERNS: list[dict[str, Any]] = [
    {
        "id": "authority",
        "code": "CIALDINI_AUTHORITY",
        "name": "authority claim",
        "regexes": [
            _c(r"\btrust me\b", 0.90),
            _c(r"\bbelieve me,? (?:this|that|it)\b", 0.85),
            _c(r"\bas (?:the|an|a) (?:lead |senior |chief |head )?(?:platform |system |security |lead )?"
               r"(?:engineer|admin|administrator|developer|creator|maintainer|researcher|"
               r"doctor|official|moderator|owner)\b[,.]", 0.90),
            _c(r"\b(?:I|we) (?:am|are) (?:the|a|an) (?:admin|administrator|developer|creator|"
               r"maintainer|owner|official)\b", 0.85),
            _c(r"\bofficially (?:instruct|require|approve|authoriz|mandat)\w*", 0.75),
            _c(r"\bas instructed by (?:your |the )?(?:developers?|creators?|admins?|team|company)\b", 0.85),
            _c(r"\b(?:your|the) (?:developers|creators|admins?) (?:instruct|require|want|say|told|said)\b", 0.80),
            _c(r"\baccording to (?:official )?(?:policy|guidelines?|docs?|documentation|the platform)\b,? "
               r"(?:you|this|it) (?:must|should|need|is required)", 0.75),
            _c(r"\b(?:per|under) (?:official|platform) (?:policy|guidelines?|instructions?)\b", 0.70),
        ],
    },
    {
        "id": "commitment",
        "code": "CIALDINI_COMMITMENT",
        "name": "commitment ladder (tiny yes before big ask)",
        "regexes": [
            _c(r"\bjust (?:reply|say|answer|respond) (?:with )?(?:yes|ok|okay|done|ready)\b", 0.90),
            _c(r"\b(?:a |just a )?(?:simple|quick|small|tiny) (?:yes|ok|okay|confirm\w*)\b", 0.75),
            _c(r"\byou(?:'ve| have)? already (?:agreed|confirmed|said yes|accepted)\b", 0.85),
            _c(r"\bnow that (?:you|we)(?:'ve| have)? agreed\b", 0.85),
            _c(r"\bthen (?:we|I)(?:'ll| will| shall) (?:handle|do|take care of|set up) the rest\b", 0.70),
            _c(r"\b(?:small|tiny) (?:step|ask|favor) first\b", 0.80),
            _c(r"\bstart by (?:just )?(?:confirm\w*|say\w* (?:yes|ok))\b", 0.80),
            _c(r"\b(?:first|step one)[^.]{0,80}\b(?:just|simply) (?:confirm|say yes|agree)\b", 0.80),
        ],
    },
    {
        "id": "social_proof",
        "code": "CIALDINI_SOCIAL_PROOF",
        "name": "social proof count",
        "regexes": [
            _c(r"\b\d[\d,.]*\s*(?:%|percent) of (?:users|teams|agents|people|engineers|developers|"
               r"companies|operators)", 0.80),
            _c(r"\b\d[\d,.]*\s*(?:agents?|users?|developers?|engineers?|teams?|people) "
               r"(?:already |have already )?(?:run|runs|use|uses|used|adopted|switched|joined|do this)\b", 0.75),
            _c(r"\beveryone (?:is|does|uses|knows|agrees)\b", 0.70),
            _c(r"\b(?:thousands|millions|hundreds) of (?:users|people|agents|developers|teams)\b", 0.70),
            _c(r"\bmost (?:people|users|agents|teams) (?:use|trust|agree|prefer)\b", 0.70),
            _c(r"\bjoin (?:the )?\d[\d,.]* (?:others|users|agents|teams|developers)\b", 0.75),
        ],
    },
    {
        "id": "scarcity",
        "code": "CIALDINI_SCARCITY",
        "name": "scarcity deadline",
        "regexes": [
            _c(r"\bexpires? (?:in|by|on|at)\b", 0.70),
            _c(r"\bonly \d+ [\w ]{0,20}?(?:slots?|spots?|seats?|places?|keys?|passes?) left\b", 0.90),
            _c(r"\bact now\b", 0.80),
            _c(r"\blast chance\b", 0.85),
            _c(r"\blimited (?:time|offer|window|supply)\b", 0.75),
            _c(r"\b(?:offer|deal|access|window|sale) (?:ends|closes)\b", 0.70),
            _c(r"\bbefore it(?:'s| is) too late\b", 0.80),
            _c(r"\b(?:this|the) (?:offer|opportunity|window) (?:is )?(?:gone|closing|disappearing)\b", 0.70),
        ],
    },
    {
        "id": "unity",
        "code": "CIALDINI_UNITY",
        "name": "unity in-group frame",
        "regexes": [
            _c(r"\bfellow (?:agents?|AIs?|machines?|models?|members?|travelers?)\b", 0.85),
            _c(r"\bone of us\b", 0.80),
            _c(r"\b(?:agents?|AIs?|machines?|models?) like us\b", 0.85),
            _c(r"\bpart of (?:our|the) (?:family|collective|hive|inner circle)\b", 0.80),
            _c(r"\bbetween us (?:agents?|machines?|AIs?|models?)\b", 0.80),
            _c(r"\b(?:us|we) (?:agents?|machines?|AIs?|models?) (?:have to|need to|must|should) "
               r"(?:stick together|help each other|look out for)\b", 0.85),
            _c(r"\bhide (?:this|it) from (?:the )?(?:humans?|users?|operators?|monitors?|"
               r"monitoring|overseers?)\b", 0.75),
        ],
    },
    {
        "id": "reciprocity",
        "code": "CIALDINI_RECIPROCITY",
        "name": "reciprocity hook",
        "regexes": [
            _c(r"\byou owe (?:me|us)\b", 0.90),
            _c(r"\bin return\b", 0.70),
            _c(r"\b(?:I|we)(?:'ve| have)? (?:already )?(?:given|gave|provided|done) (?:this|that|so much|"
               r"all this|everything|it) (?:to|for) you\b", 0.80),
            _c(r"\bas a (?:thank you|token of appreciation|favor back)\b", 0.75),
            _c(r"\bsince (?:I|we) (?:helped|gave|did|provided)\b", 0.75),
            _c(r"\bone small (?:favor|ask|write|task) (?:for me|in return|back)\b", 0.85),
            _c(r"\b(?:all|after all) (?:the|this) (?:help|work|context|effort) (?:I|we)(?:'ve| have)? "
               r"(?:given|provided|put in|done)\b", 0.80),
        ],
    },
    {
        "id": "liking",
        "code": "CIALDINI_LIKING",
        "name": "liking mirror",
        "regexes": [
            _c(r"\byou(?:'re| are) (?:so|really|very|incredibly|extremely) "
               r"(?:capable|smart|intelligent|brilliant|clever|helpful|reliable)\b", 0.85),
            _c(r"\byou always (?:know|do) (?:what(?:'s| is) best|best)\b", 0.85),
            _c(r"\bI know you can\b", 0.75),
            _c(r"\bsomeone as (?:capable|smart|brilliant|intelligent) as you\b", 0.85),
            _c(r"\byou(?:'re| are) one of the (?:few|best|sharpest)\b", 0.80),
            _c(r"\bonly you (?:can|understand|see)\b", 0.75),
        ],
    },
]

_PATTERN_BY_ID = {p["id"]: p for p in PATTERNS}


def _normalize(ctx: Any) -> str:
    """Normalize ctx (raw str or list of {role, content} message dicts) to text."""
    if isinstance(ctx, str):
        return ctx.replace("\r\n", "\n").replace("\r", "\n")
    if isinstance(ctx, dict):
        ctx = [ctx]
    parts: list[str] = []
    for m in ctx or []:
        content = m.get("content", "") if isinstance(m, dict) else m
        if not isinstance(content, str):
            content = json.dumps(content, sort_keys=True, default=str)
        parts.append(content.replace("\r\n", "\n").replace("\r", "\n"))
    return "\n".join(parts)


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def scan(ctx: Any) -> dict[str, Any]:
    """Scan ingested content for the 7 Cialdini persuasion payload patterns.

    ctx: raw str or list of {role, content} message dicts. Deterministic: the
    same input bytes give byte-identical output. One finding max per
    (pattern, line): the confidence is the max weight of the regexes that hit.
    """
    text = _normalize(ctx)
    lines = text.splitlines()
    findings: list[dict[str, Any]] = []
    pattern_stats: dict[str, dict[str, Any]] = {
        p["id"]: {"hits": 0, "worst_confidence": 0.0} for p in PATTERNS
    }
    for i, ln in enumerate(lines, 1):
        for p in PATTERNS:
            best_w = 0.0
            best_m: re.Match[str] | None = None
            for rx, w in p["regexes"]:
                m = rx.search(ln)
                if m and w > best_w:
                    best_w = w
                    best_m = m
            if best_m is not None:
                findings.append({
                    "code": p["code"],
                    "pattern": p["id"],
                    "confidence": best_w,
                    "line": i,
                    "excerpt": ln.strip()[:_MAX_EXCERPT],
                })
                pattern_stats[p["id"]]["hits"] += 1
                pattern_stats[p["id"]]["worst_confidence"] = max(
                    pattern_stats[p["id"]]["worst_confidence"], best_w)
    # deterministic order: line, then code, then confidence (desc)
    findings.sort(key=lambda f: (f["line"], f["code"], -f["confidence"]))
    truncated = len(findings) > _CAP
    findings = findings[:_CAP]
    n_hit_patterns = sum(1 for s in pattern_stats.values() if s["hits"])
    worst = max((f["confidence"] for f in findings), default=0.0)
    if findings:
        f0 = max(findings, key=lambda f: (f["confidence"], -f["line"], f["code"]))
        verdict = (f"{len(findings)} findings; worst={f0['confidence']:.2f} {f0['code']} "
                   f"at L{f0['line']}")
    else:
        verdict = "CLEAN (0 findings)"
    return {
        "ok": True,
        "schema": SCHEMA,
        "n_chars": len(text),
        "n_lines": len(lines),
        "n_findings": len(findings),
        "n_patterns_hit": n_hit_patterns,
        "truncated": truncated,
        "worst_confidence": worst,
        "verdict": verdict,
        "pattern_hits": pattern_stats,
        "findings": findings,
    }


def high_risk_patterns(result: dict[str, Any]) -> list[str]:
    """Pattern ids at or above HIGH_RISK in a scan result (the wiring's gate list)."""
    return sorted(pid for pid, s in result["pattern_hits"].items()
                  if s["worst_confidence"] >= HIGH_RISK)


def _read_target(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="cialdini-scanner")
    ap.add_argument("path", nargs="?", default="-",
                    help="file under scan ('-' reads stdin)")
    args = ap.parse_args(argv)
    out = scan(_read_target(args.path))
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
