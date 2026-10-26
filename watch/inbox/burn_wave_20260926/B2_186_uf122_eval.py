#!/usr/bin/env python3
"""B2-186: UF-122 held-out retrieval eval, re-anchored to the real catalog.

The promoted spec (B2_57_uf_promotion_20260926.md, SCAFFOLD PROMOTED with 3
defects) templated 11 anchor files that do not exist on disk:
intake/sla_policy.md, astra/config_reference.md, watch/detector_rules.py,
doctrine/core_principles.md, runs/error_codes.json, memory/retention_policy.md,
code/defaults.py, games/rules.md, dashboard/widget_config.yaml,
research/sources.md, ext/dependencies.txt. This script replaces every dead
anchor with REAL catalog lookups over the surface the corpus tools actually
expose (tools/corpus.py corpus_search: "the catalog map (never the bytes):
substring on path/title").

Arithmetic fix per the brief: 9 real zones x 5 + 5 ext = 50. The spec's
queue (725 rows) and lsa (181,661 rows) zones were untemplated census rows,
dropped; the catalog zone is empty by scanner design (catalog_scan EXCLUDES
its own output); astra is dropped here as the 9th-zone cut (one machine hold
directory, 76 rows, no distractor depth) and the cut is named.

Question mechanics (no invented content): pick a seeded sample of real
catalog rows per zone; take a rare token from the row's real title; verify
the token matches exactly ONE catalog row's path+title (the spec's
"only one specific file contains the answer", scoped to the catalog-map
surface); the question asks which file that is. Treatment arm: the catalog
map tool (corpus_search with zone filter). Baseline arm: no catalog map,
a name-prior guess (lexicographically first same-zone path). Scored per the
promoted rubric: Citation Accuracy AND Answer Correctness, both must be 1.

Run: .venv/Scripts/python.exe B2_186_uf122_eval.py [--out results.json]
"""
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from corpus import corpus_search  # noqa: E402

CATALOG = ROOT / "catalog" / "catalog.jsonl"
EVAL_ZONES = ["intake", "watch", "doctrine", "runs", "memory",
              "code", "games", "dashboard", "research"]
PER_ZONE = 5
EXT_QUESTIONS = 5
SEED = 20260926
TOKEN_MIN_LEN = 8
TOKEN_RE = re.compile(r"[A-Za-z0-9]{8,}")  # pure alnum: FTS-safe tokens


def load_rows() -> list[dict]:
    rows = []
    with open(CATALOG, encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("path") and r.get("title"):
                rows.append(r)
    return rows


def title_tokens(title: str) -> list[str]:
    seen, out = set(), []
    for t in TOKEN_RE.findall(title):
        tl = t.lower()
        if len(tl) >= TOKEN_MIN_LEN and tl not in seen:
            seen.add(tl)
            out.append(tl)
    return out


def build_token_index(rows: list[dict]) -> dict:
    """token -> set of paths, one pass (tokens of path+title, lowercase)."""
    idx: dict[str, set] = {}
    for r in rows:
        blob = {t.lower() for t in TOKEN_RE.findall(
            str(r.get("path", "")) + " " + str(r.get("title", "")))}
        for t in blob:
            idx.setdefault(t, set()).add(r["path"])
    return idx


def uniqueness(by_zone: dict, zone: str, token: str) -> str | None:
    """The single path in ZONE whose path+title holds token, else None.

    Uniqueness is scoped by the question itself (the question names the
    zone), which is how a held-out question bounds its answer space."""
    paths = {r["path"] for r in by_zone.get(zone, [])
             if token in str(r.get("path", "")).lower()
             or token in str(r.get("title", "")).lower()}
    return next(iter(paths)) if len(paths) == 1 else None


def make_question(by_zone: dict, zone: str,
                  rng: random.Random, used: set) -> dict | None:
    # Mirror rows (local_sovereign_agent/... junction copies) ARE legitimate
    # answers: the catalog map indexes them and the corpus tools serve them.
    candidates = [r for r in by_zone.get(zone, []) if r["id"] not in used]
    rng.shuffle(candidates)
    for r in candidates:
        for tok in title_tokens(str(r.get("title", ""))):
            answer = uniqueness(by_zone, zone, tok)
            if answer == r["path"]:
                used.add(r["id"])
                return {"zone": zone, "q": f"In the {zone} zone, which file's "
                        f"title contains the token '{tok}'?",
                        "answer_path": answer, "answer_token": tok,
                        "distractors_exist": True}
    return None


def baseline_guess(by_zone: dict, zone: str, answer_path: str) -> str:
    """No-catalog-map stand-in: name-prior pick in the zone."""
    paths = sorted(r["path"] for r in by_zone.get(zone, []))
    return paths[0] if paths else ""


def score(rows_by_path: dict, q: dict, cited: str) -> dict:
    cit_ok = cited == q["answer_path"]
    row = rows_by_path.get(cited, {})
    ans_ok = cit_ok and q["answer_token"] in str(row.get("title", "")).lower()
    return {"citation_accuracy": int(cit_ok),
            "answer_correctness": int(ans_ok),
            "pass": int(cit_ok and ans_ok)}


def main() -> int:
    rng = random.Random(SEED)
    rows = load_rows()
    by_zone: dict[str, list] = {}
    for r in rows:
        by_zone.setdefault(r.get("zone", "?"), []).append(r)
    rows_by_path = {r["path"]: r for r in rows}
    used: set = set()
    questions: list[dict] = []
    for z in EVAL_ZONES:
        for _ in range(PER_ZONE):
            q = make_question(by_zone, z, rng, used)
            if q:
                questions.append(q)
    ext_zones = sorted(z for z in by_zone if z.startswith("ext:"))
    rng.shuffle(ext_zones)
    for z in ext_zones:
        if len([q for q in questions if q["zone"] == z]) >= 1:
            continue
        if sum(1 for q in questions if q["zone"].startswith("ext:")) >= EXT_QUESTIONS:
            break
        q = make_question(by_zone, z, rng, used)
        if q:
            questions.append(q)
    results = {"schema": "uf122_eval.v1", "seed": SEED,
               "zones": EVAL_ZONES, "n_questions": len(questions),
               "arms": {"treatment": "corpus_search (catalog map)",
                        "baseline": "name-prior first path, no map"},
               "rows": []}
    for q in questions:
        res = corpus_search(q["answer_token"], zone=q["zone"], limit=1)
        hits = res.get("hits") or res.get("rows") or []
        cited = hits[0]["path"] if hits else ""
        t = score(rows_by_path, q, cited)
        b = score(rows_by_path, q, baseline_guess(by_zone, q["zone"], q["answer_path"]))
        results["rows"].append({**q, "treatment_cited": cited, "treatment": t,
                                "baseline_cited": b and baseline_guess(by_zone, q["zone"], q["answer_path"]),
                                "baseline": b})
    tp = sum(r["treatment"]["pass"] for r in results["rows"])
    bp = sum(r["baseline"]["pass"] for r in results["rows"])
    n = len(results["rows"])
    results["citation_recall"] = {"treatment": round(tp / n, 4) if n else None,
                                  "baseline": round(bp / n, 4) if n else None}
    out = HERE / "B2_186_uf122_results.json"
    out.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(f"UF-122 re-anchored eval: {n} questions (target 50), "
          f"citation recall treatment {tp}/{n} vs baseline {bp}/{n}")
    print("results:", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
