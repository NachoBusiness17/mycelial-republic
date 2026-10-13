"""concept_span_check — AJ7 (2026-09-30): is the estate's concept space spanned
by human-contrastible dimensions, or does it contain alien axes?

The chamber's exp33/34 steal asks of a model's affect space: "no alien valence -
the model's affect space is spanned by human emotion contrasts". This tool asks
the same of OUR concept space (the percolator invariants + the quantizer tiers)
with an embed-free, structural method:

  1. CONCEPTS  nodes = live percolator invariants (decayed count >= LIVE_MIN,
              decay math mirrors mag/percolator.py law 1 / Z15: half-life 30d,
              whole UTC cycles, floor 1, baseline decay_as_of) UNION the
              quantizer tiers' rows (memory/corpus/quantized_thought/
              instructions_{frontier,flash,local}.jsonl + adversarial arc),
              deduped by canonical hash. Nodes carry (text, decayed_count, tier).
  2. CO-OCCURRENCE  two structural channels, no embeddings:
              A. explore bursts - concepts whose canonicals appear in the same
                 (stream, source, hour) bucket of any memory/percolator/explore*.jsonl
                 stream co-occurred in the estate's actual exploration traffic.
                 Edge weight = cosine over context-count vectors.
              B. signature overlap - concepts whose token signatures (distinctive
                 token sets, UUID-ish tokens dropped) overlap by Jaccard >= SIG_JACCARD.
                 This is the quantizer's own dedupe signal reused as a relation.
  3. CLUSTER   union-find over edges with cosine >= CO_MIN (channel A) or
              Jaccard >= SIG_JACCARD (channel B); singletons stay singleton clusters.
  4. HUMAN COVERAGE  a lexicon of plain-English workflow dimensions (the contrast
              candidates: build-vs-verify, individual-vs-fleet, ephemeral-vs-durable,
              local-vs-remote, plan-vs-execute, cheap-vs-expensive, ask-vs-act,
              retry-vs-loop, trust-vs-audit, environment-failure). Each cluster's
              coverage = fraction of members whose text hits >= 1 term of any
              dimension. Clusters below COVERAGE_MIN are the residue candidates
              that get human adjudication in the receipt (the tool names them;
              the seat decides whether a plain-English term honestly covers the
              cluster's organizing contrast, and anything it cannot name is the
              alien-concepts census).

CLI       prints the concept/cluster census + spanning-dimension loading +
          residue list, and writes a JSON snapshot to --out. Exit 0 whatever
          the residue: a large residue is a finding, not an error. Exit 2 only
          on missing inputs. Deterministic, stdlib-only, $0.

Receipt   watch/inbox/last_mile_20260930/AJ7_CONCEPT_SPAN.md (2026-09-30).
Census law: counts here are one instrument at one moment; invariants.json is
live and drifts (AE6 read 599 generations / 27 live; the tool re-reads bytes).
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVARIANT_REGISTRY = ROOT / "memory/percolator/invariants.json"
EXPLORE_GLOB = "memory/percolator/explore*.jsonl"
QUANT_DIR = ROOT / "memory/corpus/quantized_thought"
QUANT_FILES = ["instructions_frontier.jsonl", "instructions_flash.jsonl",
               "instructions_local.jsonl", "adversarial_arc_invariants.jsonl"]

LIVE_MIN = 5          # decayed-count floor for "live" (AE6 moment read 27 live; >=5 reads 29 on 2026-09-30)
HALF_LIFE_DAYS = 30.0  # mag/percolator.py law 1 (Z15) default
CONTEXT_HOUR = True   # explore burst granularity: (stream, source, hour)
CO_MIN = 0.10         # cosine floor for a channel-A edge
SIG_JACCARD = 0.50    # channel-B signature-overlap floor
COVERAGE_MIN = 0.34   # cluster coverage floor (>= 1/3 of members hit a lexicon term)

# Plain-English workflow dimensions: name -> contrast + covering terms (regex, lowercase).
DIMENSIONS: dict[str, tuple[str, list[str]]] = {
    "build-vs-verify": ("writing vs checking work", [
        r"\bverif", r"\btest", r"\bdiff", r"\bbytes", r"\bclaim", r"\bsmoke", r"\bassert",
        r"\bevidence", r"\bprov", r"\bfalsif", r"\bcheck"]),
    "individual-vs-fleet": ("solo seat vs swarm coordination", [
        r"\bswarm", r"\bfleet", r"\bhandoff", r"\bqueue", r"\bmulti-agent", r"\borchestr",
        r"\bflock", r"\bagent", r"\bcoordina", r"\bbroadcast", r"\bmesh"]),
    "ephemeral-vs-durable": ("cache/session vs receipt/file", [
        r"\breceipt", r"\bdurable", r"\bpersist", r"\bwrite", r"\bfile", r"\bcache",
        r"\binbox", r"\bsave", r"\bstamp", r"\bregister", r"\bmemory"]),
    "local-vs-remote": ("on-box vs served service", [
        r"\bbackend", r"\bhttp", r"\bremote", r"\blocal", r"\breachab", r"\burl",
        r"\bapi\b", r"\bhost", r"\bport", r"\bnetwork", r"\bendpoint"]),
    "plan-vs-execute": ("spec before behavior", [
        r"\bspec", r"\bplan", r"\bdesign", r"\bintend", r"\bprecede", r"\bschema",
        r"\bblueprint", r"\bpredict", r"\bforecast", r"\bmodel\b"]),
    "cheap-vs-expensive": ("tier ladder / cost discipline", [
        r"\bescala", r"\btier", r"\bcheap", r"\bexpensiv", r"\bbudget", r"\btokens?\b",
        r"\bcost", r"\bflash", r"\bpenny", r"\bcredit", r"\bfree\b", r"\bburn"]),
    "ask-vs-act": ("permission vs autonomy", [
        r"\bpermission", r"\boperator", r"\ballowlist", r"\bjail", r"\bgate", r"\bauthori",
        r"\bapprov", r"\broute\b", r"\bstop\b", r"\bask\b", r"\bdelegate"]),
    "retry-vs-loop": ("repetition and stalls", [
        r"\bretry", r"\bloop", r"\bidentical", r"\brepeat", r"\btimeout", r"\bhang",
        r"\bstuck", r"\bstall", r"\bre-run", r"\bdeadlock", r"\bdrain"]),
    "trust-vs-audit": ("claims vs byte truth", [
        r"\btrust", r"\baudit", r"\breport", r"\bhonest", r"\bfabricat", r"\btruth",
        r"\bfals", r"\bprovenance", r"\becho", r"\bdrift", r"\bcensus"]),
    "environment-failure": ("tooling/host breakage", [
        r"\berrno\b", r"no such file", r"command not", r"\bbanned pattern", r"\bnot found",
        r"\berror", r"\bexception", r"\bcrash", r"\bfail", r"\bmissing", r"\bcorrupt",
        r"\bsubprocess", r"\bpowershell", r"\bshell\b"]),
}
_DIM_RE = {name: re.compile("|".join(terms)) for name, (_, terms) in DIMENSIONS.items()}

_TOKEN_RE = re.compile(r"[a-z][a-z0-9_]{2,}")
_UUIDISH_RE = re.compile(r"^[0-9a-f]{6,}$|^\d+$|^pro[-_]|^[a-z]+[-_]?\d*$")


def _parse_ts(s: Any) -> datetime | None:
    if not s or not isinstance(s, str):
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _decayed_count(row: dict[str, Any], now: datetime) -> int:
    """mag/percolator.py _decay_count, re-implemented read-only (floor 1, whole cycles)."""
    base = _parse_ts(row.get("decay_as_of")) or _parse_ts(row.get("last_seen"))
    count = int(row.get("count", 1))
    if base is None:
        return max(1, count)
    whole = int((now - base).total_seconds() / 86400.0)
    if whole <= 0:
        return max(1, count)
    return max(1, int(count * (0.5 ** (whole / HALF_LIFE_DAYS))))


def _signature(text: str) -> set[str]:
    toks = {t for t in _TOKEN_RE.findall(text.lower()) if not _UUIDISH_RE.match(t)}
    return toks


def load_concepts(now: datetime) -> tuple[dict[str, dict[str, Any]], Counter]:
    """Node set: live invariants UNION quantizer tiers, deduped by canonical/source hash."""
    inv = json.loads(INVARIANT_REGISTRY.read_text(encoding="utf-8"))["invariants"]
    nodes: dict[str, dict[str, Any]] = {}
    for key, row in inv.items():
        dc = _decayed_count(row, now)
        if dc >= LIVE_MIN:
            nodes[key] = {"text": row.get("text", ""), "count": dc, "tiers": {"live-invariant"}}
    tier_counts: Counter[str] = Counter()
    for fname in QUANT_FILES:
        tier = (fname.split("_")[1] if fname.startswith("instructions_")
                else "adversarial-arc").split(".")[0]
        path = QUANT_DIR / fname
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            qrow = json.loads(line)
            tier_counts[tier] += 1  # count ROWS, not source-hashes (13 dedupe rows carry 2)
            text = qrow.get("frontier") or qrow.get("statement") or qrow.get("flash") or ""
            keys = qrow.get("sources") or []
            if not keys:  # adversarial arc carries no canonical; node by its own id
                keys = [f"adv:{qrow.get('id')}"]
            for key in keys:
                node = nodes.setdefault(key, {"text": text, "count": 0, "tiers": set()})
                node["tiers"].add(tier)
                if not node["text"]:
                    node["text"] = text
    for node in nodes.values():
        node["tiers"] = sorted(node["tiers"])
    return nodes, tier_counts


def explore_contexts(nodes: dict[str, dict[str, Any]]) -> tuple[dict[str, Counter], int]:
    """Channel A: per-concept context-count vectors from explore bursts."""
    vecs: dict[str, Counter] = defaultdict(Counter)
    rows = 0
    for path in sorted(glob.glob(str(ROOT / EXPLORE_GLOB))):
        stream = Path(path).name
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows += 1
            canon = rec.get("canonical")
            if canon not in nodes:
                continue
            ts = (rec.get("ts") or "")
            grain = ts[:13] if CONTEXT_HOUR else ts[:10]
            vecs[canon][(stream, rec.get("source") or "?", grain)] += 1
    return vecs, rows


def cosine_edges(vecs: dict[str, Counter], floor: float) -> list[tuple[str, str, float]]:
    """Pairwise cosine over context-count vectors (inverted-index join, no all-pairs scan)."""
    posting: dict[tuple, list[str]] = defaultdict(list)
    for canon, cv in vecs.items():
        for ctx in cv:
            posting[ctx].append(canon)
    shared: Counter = Counter()
    for members in posting.values():
        if len(members) < 2:
            continue
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                a, b = members[i], members[j]
                shared[(a, b) if a < b else (b, a)] += 1
    norms = {c: math.sqrt(sum(v * v for v in cv.values())) for c, cv in vecs.items()}
    edges = []
    for (a, b), s in shared.items():
        if a in norms and b in norms and norms[a] > 0 and norms[b] > 0:
            w = s / (norms[a] * norms[b])
            if w >= floor:
                edges.append((a, b, w))
    return edges


def signature_edges(nodes: dict[str, dict[str, Any]], floor: float
                    ) -> list[tuple[str, str, float]]:
    """Channel B: Jaccard over distinctive token signatures, inverted-index pruned."""
    sigs = {k: _signature(v["text"]) for k, v in nodes.items()}
    posting: dict[str, list[str]] = defaultdict(list)
    for key, sig in sigs.items():
        for tok in sig:
            posting[tok].append(key)
    seen: set[tuple[str, str]] = set()
    edges = []
    for members in posting.values():
        if len(members) < 2 or len(members) > 200:  # stopwords-in-effect guard
            continue
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                a, b = members[i], members[j]
                pair = (a, b) if a < b else (b, a)
                if pair in seen:
                    continue
                seen.add(pair)
                inter = len(sigs[a] & sigs[b])
                if not inter:
                    continue
                jac = inter / len(sigs[a] | sigs[b])
                if jac >= floor:
                    edges.append((pair[0], pair[1], jac))
    return edges


def cluster(nodes: dict[str, dict[str, Any]], edge_lists: dict[str, list[tuple[str, str, float]]]
            ) -> tuple[dict[int, list[str]], dict[str, str]]:
    """Union-find over the union graph; returns clusters + per-node cluster id."""
    parent = {k: k for k in nodes}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    channels: dict[str, str] = {}
    for chan, edges in edge_lists.items():
        for a, b, _w in edges:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
                channels[(min(a, b), max(a, b))] = chan
    groups: dict[str, list[str]] = defaultdict(list)
    for k in nodes:
        groups[find(k)].append(k)
    clusters = {i: sorted(members, key=lambda m: (-nodes[m]["count"], m))
                for i, members in enumerate(sorted(groups.values(), key=lambda m: (-max(
                    nodes[x]["count"] for x in m), sorted(m)[0])))}
    cid = {node: i for i, members in clusters.items() for node in members}
    return clusters, cid


def dimension_hits(text: str) -> list[str]:
    low = text.lower()
    return [name for name, rex in _DIM_RE.items() if rex.search(low)]


def main(argv: list[str] | None = None) -> int:
    global LIVE_MIN  # params override module default for this run
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path,
                    default=ROOT / "watch/inbox/last_mile_20260930/AJ7_concept_span_snapshot.json",
                    help="JSON snapshot path (default watch/inbox/last_mile_20260930/AJ7_concept_span_snapshot.json)")
    ap.add_argument("--live-min", type=int, default=LIVE_MIN)
    ap.add_argument("--co-min", type=float, default=CO_MIN)
    ap.add_argument("--sig-jaccard", type=float, default=SIG_JACCARD)
    ap.add_argument("--coverage-min", type=float, default=COVERAGE_MIN)
    args = ap.parse_args(argv)

    if not INVARIANT_REGISTRY.exists():
        print("concept_span_check: missing memory/percolator/invariants.json", file=__import__("sys").stderr)
        return 2
    now = datetime.now(timezone.utc)
    LIVE_MIN = args.live_min

    nodes, tier_counts = load_concepts(now)
    vecs, explore_rows = explore_contexts(nodes)
    co_edges = cosine_edges(vecs, args.co_min)
    sig_edges = signature_edges(nodes, args.sig_jaccard)
    clusters, cid = cluster(nodes, {"co-occurrence": co_edges, "signature": sig_edges})

    # per-cluster census + coverage
    dim_load: Counter = Counter()
    report_clusters = []
    residue = []
    for i, members in sorted(clusters.items()):
        all_hits, covered = [], 0
        for m in members:
            hits = dimension_hits(nodes[m]["text"])
            all_hits += hits
            if hits:
                covered += 1
        for h in set(all_hits):
            dim_load[h] += 1
        coverage = covered / len(members) if members else 0.0
        entry = {
            "cluster": i, "size": len(members), "coverage": round(coverage, 3),
            "top_dims": [d for d, _ in Counter(all_hits).most_common(3)],
            "members": [{"key": m, "count": nodes[m]["count"], "tiers": nodes[m]["tiers"],
                         "text": nodes[m]["text"][:160]} for m in members[:12]],
        }
        report_clusters.append(entry)
        if coverage < args.coverage_min:
            residue.append(entry)

    snapshot = {
        "tool": "concept_span_check", "ran_at": now.isoformat(),
        "params": {"live_min": args.live_min, "co_min": args.co_min,
                   "sig_jaccard": args.sig_jaccard, "coverage_min": args.coverage_min,
                   "half_life_days": HALF_LIFE_DAYS},
        "census": {
            "n_concepts": len(nodes),
            "live_invariants": sum(1 for v in nodes.values() if "live-invariant" in v["tiers"]),
            "tier_rows": dict(tier_counts),
            "n_explore_rows_scanned": explore_rows,
            "n_co_edges": len(co_edges), "n_signature_edges": len(sig_edges),
            "n_clusters": len(clusters),
            "n_multi_clusters": sum(1 for m in clusters.values() if len(m) > 1),
            "n_singletons": sum(1 for m in clusters.values() if len(m) == 1),
        },
        "dimension_loading": dict(dim_load.most_common()),
        "clusters": report_clusters,
        "residue": [{"cluster": r["cluster"], "size": r["size"],
                     "coverage": r["coverage"], "members": r["members"]} for r in residue],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(snapshot, indent=1, ensure_ascii=False), encoding="utf-8")

    c = snapshot["census"]
    print(f"concepts={c['n_concepts']} (live invariants>= {args.live_min} decayed: "
          f"{c['live_invariants']}; tier rows: {c['tier_rows']})")
    print(f"explore rows scanned={c['n_explore_rows_scanned']}  co-edges={c['n_co_edges']} "
          f"signature-edges={c['n_signature_edges']}")
    print(f"clusters={c['n_clusters']} (multi={c['n_multi_clusters']} singletons={c['n_singletons']})")
    print("dimension loading (clusters touching):", snapshot["dimension_loading"])
    print(f"residue clusters (coverage < {args.coverage_min}): {len(residue)}")
    for r in residue[:20]:
        print(f"  C{r['cluster']} size={r['size']} cov={r['coverage']}: " +
              " | ".join(m["text"][:60] for m in r["members"][:3]))
    print(f"snapshot -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
