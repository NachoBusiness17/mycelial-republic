"""Monoculture agreement-rate proxy - D6 adapter (eleven-doors, 2026-10-05).

The door: import mag/roshomon.py:140-176 primitives (_invariant_statements,
_clean, _tokens, _overlap) + reimplement the :205-214 grouping loop as an
adapter over the estate's OWN witness surfaces - NEVER compare() (its
_answers_for :179-186 is welded to the k8s PVC swarm). The agreement organs
already exist (tools/env_contract.py run_legality agreement_rate,
tools/overmind_judge.py:313 agreement_rate); this adds the third: a
MONOCULTURE proxy - how much of what the independent lanes say is the same
statements recurring across >=2 witnesses (the Roshomon core).

The door's falsifier made law: at threshold 0.55 the 24-wide-style long
chapters group all-or-nothing, which kills the estimate. So the adapter
SWEEPS thresholds (0.40/0.55/0.70) and reports sensitivity; when every
threshold reads either zero-core or one-mass, the corpus is UNMEASURABLE -
said honestly, never a fake agreement number.

Alert contract: on a core-size drop vs the last history row for the same
label, append one line to memory/attention.md (the operator's triage
board) - a shrinking core means the lanes' independent statements stopped
recurring, i.e. the witnesses stopped talking about the same world.

Usage:
  python tools/monoculture_proxy.py                 # lane surfaces
  python tools/monoculture_proxy.py --texts a.md b.md --label X
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from mag.roshomon import (  # noqa: E402  - the door-named primitives ONLY
    _clean,
    _invariant_statements,
    _overlap,
    _tokens,
)

LANES_DIR = ROOT / "dashboard" / "static" / "lanes"
HISTORY = ROOT / "memory" / "monoculture" / "history.jsonl"
ATTENTION = ROOT / "memory" / "attention.md"
THRESHOLD_SWEEP = (0.40, 0.55, 0.70)
SINGLE_GROUP_DOMINANCE = 0.90  # >90% of statements in one group = mass


def _group_witness_statements(
    witness_stmts: list[list[str]], threshold: float
) -> list[list]:
    """The roshomon :205-214 grouping loop, reimplemented (never imported:
    compare() drags the k8s PVC with it). Each group: [representative, set of
    witness indices, instance count]; a statement joins a group on token
    overlap >= threshold. Instance count matters because the agreement
    denominator is statement INSTANCES - a witness repeating a core line
    three times is three agreeing instances, not one (the tripled-text test
    caught the old distinct-pairs arithmetic reading 0.4 for identical
    witnesses)."""
    groups: list[list] = []
    for wi, stmts in enumerate(witness_stmts):
        for s in stmts:
            placed = False
            for g in groups:
                if _overlap(g[0], s) >= threshold:
                    g[1].add(wi)
                    g[2] += 1
                    placed = True
                    break
            if not placed:
                groups.append([s, {wi}, 1])
    return groups


def measure(witnesses: dict[str, str]) -> dict:
    """witnesses: {name: text}. Returns per-threshold grouping metrics."""
    names = sorted(witnesses)
    witness_stmts = [_invariant_statements(witnesses[n]) for n in names]
    n_statements = sum(len(s) for s in witness_stmts)
    per_threshold = {}
    for t in THRESHOLD_SWEEP:
        groups = _group_witness_statements(witness_stmts, t)
        core = [g for g in groups if len(g[1]) >= 2]
        core_instances = sum(g[2] for g in core)
        # dominance = every witness merged into the largest group (1.0 =
        # full mass); statement-share was a category error (witness counts
        # divided by statement totals) caught by the identical-texts test
        dominant_share = (
            max(len(g[1]) for g in groups) / len(names) if groups and names else 0.0
        )
        per_threshold[str(t)] = {
            "groups": len(groups),
            "core_groups": len(core),
            "core_witnesses": sorted({wi for g in core for wi in g[1]}),
            "core_statements": len(core),
            "core_instances": core_instances,
            "agreement_proxy": round(core_instances / n_statements, 4) if n_statements else 0.0,
            "dominant_witness_share": round(dominant_share, 4),
        }
    # the falsifier's verdict: all-or-nothing at EVERY threshold kills the
    # estimate - zero-core everywhere (nothing recurs) or mass everywhere
    # (every statement recurs across ~all witnesses: agreement ~ 1.0 with
    # every witness inside the same groups)
    zero_core_all = all(v["core_groups"] == 0 for v in per_threshold.values())
    mass_all = all(
        v["agreement_proxy"] > SINGLE_GROUP_DOMINANCE
        and v["dominant_witness_share"] >= SINGLE_GROUP_DOMINANCE
        for v in per_threshold.values()
    )
    measurable = not (zero_core_all or mass_all) and n_statements >= 10
    return {
        "schema": "monoculture.proxy.v1",
        "ts_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "witnesses": names,
        "n_statements": n_statements,
        "per_threshold": per_threshold,
        "measurable": measurable,
        "unmeasurable_reason": (
            "zero-core at every threshold" if zero_core_all
            else "single-group dominance at every threshold" if mass_all
            else "too few statements" if n_statements < 10
            else None
        ),
    }


def _last_core(label: str) -> int | None:
    if not HISTORY.exists():
        return None
    last = None
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if row.get("label") == label:
            last = row
    if not last:
        return None
    return last.get("core_statements_055")


def record(report: dict, *, label: str, alert: bool = True) -> dict:
    """Persist the history row; alert attention.md on a core-size drop."""
    core_now = report["per_threshold"]["0.55"]["core_statements"]  # core GROUP count, stable across instance arithmetic
    prev = _last_core(label)
    row = {
        "ts": report["ts_utc"],
        "label": label,
        "witnesses": report["witnesses"],
        "n_statements": report["n_statements"],
        "core_statements_055": core_now,
        "agreement_proxy_055": report["per_threshold"]["0.55"]["agreement_proxy"],
        "measurable": report["measurable"],
    }
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    alerted = False
    if alert and prev is not None and core_now < prev:
        sweep = [report["per_threshold"][str(t)]["agreement_proxy"] for t in THRESHOLD_SWEEP]
        line = (f"- MONOCULTURE {report['ts_utc']}: core-size drop {prev} -> {core_now}"
                f" on {label} (agreement proxy"
                f" {report['per_threshold']['0.55']['agreement_proxy']:.3f}"
                f" at t=0.55; sweep {sweep})\n")
        with ATTENTION.open("a", encoding="utf-8") as f:
            f.write(line)
        alerted = True
    row["prev_core_statements_055"] = prev
    row["alerted_attention"] = alerted
    return row


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="monoculture agreement-rate proxy (D6 adapter)")
    ap.add_argument("--texts", nargs="*", default=None,
                    help="witness text files; default = dashboard lane surfaces")
    ap.add_argument("--label", default="lane-surfaces")
    ap.add_argument("--no-alert", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.texts:
        witnesses = {Path(p).stem: Path(p).read_text(encoding="utf-8", errors="ignore")
                     for p in args.texts}
    else:
        witnesses = {p.stem: p.read_text(encoding="utf-8", errors="ignore")
                     for p in sorted(LANES_DIR.glob("*.md"))}
    if len(witnesses) < 2:
        print("need >=2 witnesses; got", len(witnesses))
        return 1
    report = measure(witnesses)
    row = record(report, label=args.label, alert=not args.no_alert)
    if args.json:
        print(json.dumps({"report": report, "history_row": row}, indent=1))
        return 0
    print(f"MONOCULTURE PROXY: {len(witnesses)} witnesses, {report['n_statements']} statements"
          f" (label {args.label})")
    for t in THRESHOLD_SWEEP:
        v = report["per_threshold"][str(t)]
        print(f"  t={t:.2f}: groups={v['groups']:4d} core={v['core_groups']:4d}"
              f" core_stmts={v['core_statements']:4d}"
              f" agreement={v['agreement_proxy']:.3f} dominant={v['dominant_witness_share']:.3f}")
    print(f"  MEASURABLE: {report['measurable']}"
          + (f" ({report['unmeasurable_reason']})" if report["unmeasurable_reason"] else ""))
    print(f"  history: core@0.55 {row['prev_core_statements_055']} -> {row['core_statements_055']}"
          f" | attention alert: {row['alerted_attention']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
