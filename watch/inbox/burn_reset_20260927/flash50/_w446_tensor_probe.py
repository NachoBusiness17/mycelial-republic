#!/usr/bin/env python3
"""_w446_tensor_probe -- read-only execution of the receipt-tensor query algebra.

Banks beside w4-46.md (watch/inbox/burn_reset_20260927/flash50/). Read-only:
opens three real receipt carriers, scatters their rows into labeled sparse
tensors, and runs the six query operators the design doc names. Stdlib only.
Spawns NO subprocess. Writes nothing.

Carriers and modes:
  T1 memory/burns/LEDGER.jsonl      -> T[slug, verdict, utc_day]     value=count
  T2 memory/workflows/REGISTRY.jsonl -> T[name, check_id, ok]       value=count
  T3 watch/GROUNDING_WAVE.jsonl      -> T[kind] + act-edge fibers   value=count

Operators executed (see w4-46.md section 4):
  Q1 slice          T[:, verdict] etc.
  Q2 marginal       contract slug+verdict axes -> per-day counts
  Q3 contraction    slug-chain edges (order-by-ts self-join); registry self-join
                    on digest (repeat submissions)
  Q4 negation       dangling landing pointers; interior silence days;
                    registry check-slot completeness
  Q5 liveness       wave act-edge target resolution (admission view sample)
  (Q6 grade-gating is a filter law, not a measurement; doc section 4.6)
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = []


def emit(key, value):
    OUT.append((key, value))
    print(f"{key}: {value}")


def load_jsonl(rel):
    p = ROOT / rel
    rows = []
    if not p.exists():
        return rows, 0
    raw = p.read_text(encoding="utf-8", errors="replace").splitlines()
    bad = 0
    for line in raw:
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            bad += 1
    return rows, bad


def key_union(rows):
    keys = set()
    for r in rows:
        if isinstance(r, dict):
            keys.update(r.keys())
    return sorted(keys)


# ---------------------------------------------------------------- T1 burns
burns, bad_burns = load_jsonl("memory/burns/LEDGER.jsonl")
emit("T1.rows", len(burns))
emit("T1.malformed_lines", bad_burns)
emit("T1.key_union", key_union(burns))

t1 = Counter()          # (slug, verdict, day) -> count
per_day = Counter()     # day -> count
slug_days = defaultdict(set)
slug_ts = defaultdict(list)
verdicts = Counter()
dangling = []
for r in burns:
    slug = r.get("slug", "?")
    verdict = r.get("verdict", "?")
    ts = r.get("ts", "")
    day = ts[:10] or "?"
    t1[(slug, verdict, day)] += 1
    per_day[day] += 1
    verdicts[verdict] += 1
    slug_days[slug].add(day)
    if ts:
        slug_ts[slug].append(ts)
    landing = r.get("landing")
    if landing:
        if not (ROOT / landing).exists():
            dangling.append(landing)

emit("T1.modes", {"slug": len(slug_days), "verdict": len(verdicts), "day": len(per_day)})
emit("T1.nnz", sum(t1.values()))
dense = len(slug_days) * len(verdicts) * len(per_day)
emit("T1.dense_frame", dense)
emit("T1.density_pct", round(100.0 * sum(t1.values()) / max(dense, 1), 4))
emit("Q1.burns_verdict_slice", dict(verdicts.most_common()))
emit("Q2.burns_day_marginal", {"days": len(per_day), "min": min(per_day), "max": max(per_day),
                               "top3": per_day.most_common(3)})

# Q3a contraction: per-slug chain edges from ts order
edges = 0
depth_hist = Counter()
for slug, tss in slug_ts.items():
    tss.sort()
    depth = len(tss) - 1
    edges += depth
    depth_hist[depth] += 1
emit("Q3.chain_edges_total", edges)
emit("Q3.chain_max_depth", max(depth_hist) if depth_hist else 0)
emit("Q3.chain_depth_hist_top", depth_hist.most_common(6))
top_slug = max(slug_ts.items(), key=lambda kv: len(kv[1]))
emit("Q3.top_slug", {"slug": top_slug[0], "rows": len(top_slug[1]),
                     "first": top_slug[1][0], "last": top_slug[1][-1]})

# Q4a negation: dangling landing pointers
emit("Q4.dangling_landings", {"count": len(dangling), "sample": dangling[:5]})

# Q4b negation: interior silence for top slugs
silence = []
for slug, days in sorted(slug_days.items(), key=lambda kv: -len(kv[1]))[:5]:
    ds = sorted(days)
    span = (int(ds[-1].replace("-", "")) - int(ds[0].replace("-", ""))) // 1
    # crude span via day ordinal comparison
    import datetime as dt
    d0 = dt.date.fromisoformat(ds[0])
    d1 = dt.date.fromisoformat(ds[-1])
    span_days = (d1 - d0).days + 1
    silence.append({"slug": slug, "rows": len(slug_ts[slug]), "active_days": len(ds),
                    "span_days": span_days, "silent_days": span_days - len(ds)})
emit("Q4.interior_silence_top5", silence)

# ---------------------------------------------------------------- T2 registry
reg, bad_reg = load_jsonl("memory/workflows/REGISTRY.jsonl")
emit("T2.rows", len(reg))
emit("T2.malformed_lines", bad_reg)
emit("T2.key_union", key_union(reg))

t2 = Counter()
ok_by_gate = defaultdict(lambda: [0, 0])   # gate -> [ok_count, total]
digest_mult = Counter()
fail_fail_digests = []
for r in reg:
    name = r.get("name", "?")
    digest = r.get("digest", "?")
    digest_mult[digest] += 1
    for c in r.get("checks", []):
        gate = c.get("id", "?")
        ok = bool(c.get("ok"))
        t2[(name, gate, ok)] += 1
        ok_by_gate[gate][0] += int(ok)
        ok_by_gate[gate][1] += 1
emit("T2.nnz", sum(t2.values()))
emit("Q1.gate_x_ok_marginal", {g: {"ok": v[0], "fail": v[1] - v[0]} for g, v in sorted(ok_by_gate.items())})

# Q3b contraction: registry self-join on digest
repeats = {d: n for d, n in digest_mult.items() if n > 1}
emit("Q3.digest_selfjoin", {"distinct_digests": len(digest_mult),
                            "digests_with_repeats": len(repeats),
                            "max_multiplicity": max(digest_mult.values()) if digest_mult else 0})
if repeats:
    by_digest = defaultdict(list)
    for r in reg:
        d = r.get("digest", "?")
        if d in repeats:
            by_digest[d].append((r.get("ts", ""), r.get("name", ""), r.get("verdict", "")))
    ff = []
    for d, lst in by_digest.items():
        vset = [v for _, _, v in lst]
        if "FAIL" in vset and len(lst) > 1 and all(v == "FAIL" for v in vset):
            ff.append({"digest": d, "rows": lst})
    emit("Q3.fail_fail_same_digest", ff[:4])

# Q4c negation: check-slot completeness (rows whose checks fiber is not 7)
incomplete = [r.get("name", "?") for r in reg if len(r.get("checks", [])) != 7]
emit("Q4.registry_checkslot_incompletes", {"count": len(incomplete), "names": incomplete[:5]})

# ---------------------------------------------------------------- T3 wave
wave, bad_wave = load_jsonl("watch/GROUNDING_WAVE.jsonl")
emit("T3.rows", len(wave))
emit("T3.malformed_lines", bad_wave)
kinds = Counter(r.get("kind", "claim") for r in wave)
emit("Q1.wave_kind_slice", dict(kinds.most_common()))
row_hashes = {r.get("hash") for r in wave if r.get("hash")}
act_edges = []
unresolved = 0
for r in wave:
    kind = r.get("kind")
    if kind in ("void", "contest", "witness"):
        key = {"void": "voids", "contest": "contests", "witness": "signs"}[kind]
        tgt = r.get(key)
        targets = tgt if isinstance(tgt, list) else ([tgt] if tgt else [])
        for t in targets:
            resolved = any(t and (h == t or (h and h.startswith(str(t)))) for h in row_hashes)
            act_edges.append((kind, str(t)[:12], resolved))
            if not resolved:
                unresolved += 1
emit("Q5.wave_act_edges", {"total": len(act_edges), "unresolved_targets": unresolved,
                           "by_kind": Counter(k for k, _, _ in act_edges).most_common()})

emit("probe.done", "read-only, no subprocess, nothing written")
sys.exit(0)
