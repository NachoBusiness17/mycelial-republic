#!/usr/bin/env python3
"""oral_law_dedupe.py - W3 consolidation pass over the oral-law index (W3S, 2026-09-29).

Spec (Mickey17 W3 lane, watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl, 33 rows
/ 59 LAWS + 29 DEBTS, byte-verified 2026-09-29):

  1. group identical/near-identical laws into clusters: exact match OR
     token-overlap >= THRESHOLD (default 0.8). "Token-overlap" is defined here
     as the overlap coefficient |A n B| / min(|A|,|B|) over case-folded
     alphanumeric token sets (default metric "overlap"): oral laws re-birth with
     wording drift where a short phrasing is later elaborated, and the overlap
     coefficient keeps those in one cluster while Jaccard would split a subset
     pair at 0.78. --metric jaccard (|A n B| / |A u B|) is kept as the stricter
     alternative; the receipt names the metric because the metric IS a result
     parameter. Clustering is transitive (union-find).
  2. rank clusters by birth_count (number of law births across threads; the
     laws that recur across threads are the real founding law).
  3. flag laws that contradict current estate law as "SUPERSEDED?" with a
     grep-verified citation. Contradiction is not derivable from token overlap,
     so it lives in SUPERSEDED_CHECKS below, each entry carrying the estate
     file + line evidence found by grep on 2026-09-29 (curation is the receipt;
     a silent heuristic would fabricate). An automated estate_echo scan
     (best-overlap line in AGENTS.md + memory/rib/*.md) is attached to every
     cluster for confirmation leads; echo is agreement evidence, never a
     contradiction verdict.
  4. emit the deduped index as JSONL, one ranked cluster object per line.

Output row shape:
  {rank, cluster_id, kind: "LAW", canonical, birth_count, n_threads, thread_ids,
   thread_names, variants: [{text, thread_id, thread_name, ts}], metric,
   similarity_threshold, superseded: null | "SUPERSEDED? ...", estate_echo}

Fail-closed: a missing/unparseable input row is a hard error, never skipped.
DEBTs are counted and reported but NOT clustered (this pass dedupes law).

Usage: python tools/oral_law_dedupe.py [--input PATH] [--output PATH]
       [--threshold 0.8] [--metric overlap|jaccard] [--root PATH] [--quiet]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = TOOL_ROOT / "watch" / "inbox" / "operator_model" / "ORAL_LAW_INDEX.jsonl"
DEFAULT_OUTPUT = TOOL_ROOT / "watch" / "inbox" / "operator_model" / "ORAL_LAW_DEDUPED.jsonl"
DEFAULT_ESTATE_FILES = [TOOL_ROOT / "AGENTS.md"]
DEFAULT_RIB_GLOB = "memory/rib/*.md"
ECHO_THRESHOLD = 0.4  # estate_echo floor: agreement LEADS, not verdicts.
                      # 0.4 not 0.5 because the strongest true confirmation
                      # measures 0.471: "Never bare PATH python ..." vs
                      # AGENTS.md:74 "call .venv\Scripts\python.exe ... never
                      # bare python on PATH (Hermes)" - the live line says
                      # "(Hermes)." while the oral law says "(Hermes trap)",
                      # and that wording drift is exactly what echo absorbs
ECHO_MIN_TOKENS = 4   # echo lines must carry real content: a "## Law" heading
                      # is a 1-token subset of every law and scored 1.0 under
                      # the overlap coefficient before this floor existed
                      # (found on the real run 2026-09-29, every cluster echoing
                      # RIB_CAUSAL_GRAPH_MOONSHOT.md:9)

# Each check: (name, compiled regex applied to the canonical law text, verdict
# string). Evidence was found by grepping AGENTS.md + memory/rib/ on 2026-09-29.
SUPERSEDED_CHECKS = [
    (
        "local-first-no-remote",
        re.compile(r"local-first: no scarce remote seat is invoked", re.IGNORECASE),
        "SUPERSEDED? The blanket no-remote-seat law (born 2026-08-12, free-tier "
        "austerity era) contradicts the DRIVING LADDER (AGENTS.md, 2026-09-28 "
        "operator code-as-law, 2026-09-29 SPEND amendment): paid dispatch to the "
        "funded tiers is now MANDATED - 'hoarding funded budget while free lanes "
        "grind is the 03:00Z drain bug in money form'. Receipts: "
        "memory/rib/RIB_DRIVING_LADDER_20260928.md + AGENTS.md DRIVING LADDER bullet.",
    ),
]

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> frozenset[str]:
    return frozenset(_TOKEN_RE.findall(text.lower()))


def similarity(a: frozenset[str], b: frozenset[str], metric: str) -> float:
    """Overlap coefficient ('overlap') or Jaccard ('jaccard') on token sets."""
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if metric == "jaccard":
        return inter / len(a | b)
    return inter / min(len(a), len(b))


class LawBirth:
    __slots__ = ("text", "tokens", "thread_id", "thread_name", "ts")

    def __init__(self, text: str, thread_id: str, thread_name: str, ts: str):
        self.text = text
        self.tokens = tokenize(text)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.ts = ts


def load_rows(path: Path) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:  # fail-closed, never skip
                raise SystemExit(f"cannot verify: {path}:{lineno} unparseable JSON: {exc}")
    return rows


def iter_law_births(rows: list[dict]) -> tuple[list[LawBirth], int]:
    """Extract LAW births; the extractor's empty 'laws_or_debets' typo field is
    ignored (rows 2/31 carry it alongside the real laws_or_debts list)."""
    births, debts = [], 0
    for row in rows:
        extracted = row.get("extracted") or {}
        for item in extracted.get("laws_or_debts", []):
            if item.startswith("LAW: "):
                births.append(
                    LawBirth(item, row["thread_id"], row.get("thread_name", ""), row.get("ts", ""))
                )
            elif item.startswith("DEBT: "):
                debts += 1
    return births, debts


def cluster(births: list[LawBirth], threshold: float, metric: str) -> list[list[LawBirth]]:
    """Union-find transitive clustering on exact or token-overlap >= threshold.

    Exact text equality is subsumed: identical texts tokenize to identical
    sets, scoring 1.0 under both metrics, so one similarity test covers both
    clauses of the spec without a redundant exact-match pass.
    """
    parent = list(range(len(births)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(births)):
        for j in range(i + 1, len(births)):
            if find(i) == find(j):
                continue
            if similarity(births[i].tokens, births[j].tokens, metric) >= threshold:
                parent[find(i)] = find(j)
    groups: dict[int, list[int]] = {}
    for i in range(len(births)):
        groups.setdefault(find(i), []).append(i)
    return [[births[i] for i in idxs] for idxs in groups.values()]


def canonical_text(members: list[LawBirth]) -> str:
    """Most frequent exact variant; tie -> shortest; tie -> lexicographic."""
    counts: dict[str, int] = {}
    for m in members:
        counts[m.text] = counts.get(m.text, 0) + 1
    return sorted(counts, key=lambda t: (-counts[t], len(t), t))[0]


def build_estate_lines(root: Path) -> list[tuple[str, str]]:
    """(source, line) pairs from AGENTS.md + all memory/rib/*.md files."""
    pairs = []
    sources = list(DEFAULT_ESTATE_FILES)
    sources.extend(sorted(root.glob(DEFAULT_RIB_GLOB)))
    for src in sources:
        try:
            text = src.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(src.relative_to(root)) if str(src).startswith(str(root)) else src.name
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.strip():
                pairs.append((f"{rel}:{lineno}", line))
    return pairs


def estate_echo(canonical: str, estate_lines: list[tuple[str, str]]) -> dict | None:
    """Best estate agreement lead. Jaccard, not the clustering metric: an echo
    must coincide with the law (both directions), because a tiny subset line
    scores a false 1.0 under the overlap coefficient; lines with fewer than
    ECHO_MIN_TOKENS are skipped for the same reason."""
    toks = tokenize(canonical)
    best, best_score = None, 0.0
    for source, line in estate_lines:
        line_toks = tokenize(line)
        if len(line_toks) < ECHO_MIN_TOKENS:
            continue
        score = similarity(toks, line_toks, "jaccard")
        if score > best_score:
            best, best_score = (source, line.strip()), score
    if best is None or best_score < ECHO_THRESHOLD:
        return None
    return {"source": best[0], "score": round(best_score, 3), "line": best[1][:220]}


def dedupe(births: list[LawBirth], threshold: float, metric: str, estate_lines: list[tuple[str, str]]) -> list[dict]:
    clusters = cluster(births, threshold, metric)
    rows = []
    for members in clusters:
        canonical = canonical_text(members)
        superseded = None
        for _name, pattern, verdict in SUPERSEDED_CHECKS:
            if pattern.search(canonical):
                superseded = verdict
                break
        rows.append(
            {
                "cluster_id": "",
                "kind": "LAW",
                "canonical": canonical,
                "birth_count": len(members),
                "n_threads": len({m.thread_id for m in members}),
                "thread_ids": sorted({m.thread_id for m in members}),
                "thread_names": sorted({m.thread_name for m in members if m.thread_name}),
                "variants": [
                    {"text": m.text, "thread_id": m.thread_id, "thread_name": m.thread_name, "ts": m.ts}
                    for m in sorted(members, key=lambda m: (m.ts, m.thread_id))
                ],
                "metric": metric,
                "similarity_threshold": threshold,
                "superseded": superseded,
                "estate_echo": estate_echo(canonical, estate_lines),
            }
        )
    rows.sort(key=lambda r: (-r["birth_count"], r["canonical"]))
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
        row["cluster_id"] = f"cl_{rank:03d}"
    # keep rank first for human readers of the JSONL
    return [{ "rank": r["rank"], **{k: v for k, v in r.items() if k != "rank"}} for r in rows]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--threshold", type=float, default=0.8)
    ap.add_argument("--metric", choices=("overlap", "jaccard"), default="overlap")
    ap.add_argument("--root", type=Path, default=TOOL_ROOT)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    rows = load_rows(args.input)
    births, debts = iter_law_births(rows)
    if not births:
        print("cannot verify: zero LAWS parsed from input", file=sys.stderr)
        return 2
    estate_lines = build_estate_lines(args.root)
    out = dedupe(births, args.threshold, args.metric, estate_lines)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        for row in out:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    if not args.quiet:
        print(f"index rows: {len(rows)} | law births: {len(births)} | debts (not clustered): {debts}")
        print(f"clusters: {len(out)} | metric: {args.metric} | threshold: {args.threshold}")
        print(f"output: {args.output}")
        flagged = [r for r in out if r["superseded"]]
        print(f"SUPERSEDED? flags: {len(flagged)}")
        print("top-5 by birth count:")
        for row in out[:5]:
            print(f"  {row['birth_count']}x [{','.join(t[:8] for t in row['thread_ids'])}] {row['canonical'][:110]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
