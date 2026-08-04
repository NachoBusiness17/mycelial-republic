"""Run checklist self-tests; update vector map; emit reports (pytest-friendly)."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mycelial_republic.selftest.scorer import aggregate, expect_bonus, score_response
from mycelial_republic.vector_map.model import VectorMap, load_vector_map

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise ImportError("PyYAML required: pip install pyyaml")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


@dataclass
class ProbeResult:
    id: str
    session: str
    prompt: str
    passed: bool
    aggregate: float
    threshold: float
    dimensions: dict[str, float]
    detail: dict[str, Any] = field(default_factory=dict)
    fixture: str = ""
    error: str = ""


@dataclass
class SelftestReport:
    ok: bool
    passed: int
    failed: int
    total: int
    overall: float
    dirichlet_energy: float
    probes: list[ProbeResult]
    vector_map: dict[str, Any]
    timestamp: str
    config: str
    map_config: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "passed": self.passed,
            "failed": self.failed,
            "total": self.total,
            "overall": self.overall,
            "dirichlet_energy": self.dirichlet_energy,
            "timestamp": self.timestamp,
            "config": self.config,
            "map_config": self.map_config,
            "probes": [
                {
                    "id": p.id,
                    "session": p.session,
                    "prompt": p.prompt,
                    "passed": p.passed,
                    "aggregate": p.aggregate,
                    "threshold": p.threshold,
                    "dimensions": p.dimensions,
                    "detail": p.detail,
                    "fixture": p.fixture,
                    "error": p.error,
                }
                for p in self.probes
            ],
            "vector_map": self.vector_map,
        }


def _resolve_fixture(fixture_rel: str, checklist_dir: Path) -> Path:
    """Resolve fixture path relative to configs/ or project root."""
    rel = Path(fixture_rel)
    name = rel.name
    candidates = [
        checklist_dir / rel,  # configs/selftest/fixtures/... when rel is selftest/fixtures/...
        checklist_dir / "selftest" / "fixtures" / name,
        checklist_dir / "fixtures" / name,
        _project_root() / "configs" / rel,
        _project_root() / "configs" / "selftest" / "fixtures" / name,
    ]
    for c in candidates:
        if c.is_file():
            return c
    return candidates[-1]


def run_selftest(
    checklist_path: str | Path | None = None,
    map_path: str | Path | None = None,
    responses_dir: str | Path | None = None,
    out_dir: str | Path | None = None,
    live_responses: dict[str, str] | None = None,
) -> SelftestReport:
    root = _project_root()
    checklist_path = Path(checklist_path or root / "configs" / "selftest_checklist.yaml")
    map_path = Path(map_path or root / "configs" / "vector_map_hybrid.yaml")
    out_dir = Path(out_dir or root / "logs" / "selftest")
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = _load_yaml(checklist_path)
    vmap = load_vector_map(map_path)
    defaults = cfg.get("defaults") or {}
    threshold = float(defaults.get("pass_threshold", 0.55))
    dimensions = list(cfg.get("dimensions") or [])
    penalties = list(cfg.get("global_penalties") or [])
    probes_cfg = list(cfg.get("probes") or [])

    dim_scores_accum: dict[str, list[float]] = {}
    results: list[ProbeResult] = []

    for probe in probes_cfg:
        pid = probe["id"]
        dims = list(probe.get("dimensions") or [])
        expect = str(probe.get("expect") or "")
        text = ""
        fixture_used = ""
        err = ""

        if live_responses and pid in live_responses:
            text = live_responses[pid]
            fixture_used = "live"
        else:
            fix = probe.get("fixture") or ""
            fpath = _resolve_fixture(str(fix), checklist_path.parent)
            if responses_dir:
                alt = Path(responses_dir) / Path(str(fix)).name
                if alt.is_file():
                    fpath = alt
            if fpath.is_file():
                text = fpath.read_text(encoding="utf-8")
                fixture_used = str(fpath)
            else:
                err = f"missing fixture: {fpath}"

        if err:
            results.append(
                ProbeResult(
                    id=pid,
                    session=probe.get("session", ""),
                    prompt=probe.get("prompt", ""),
                    passed=False,
                    aggregate=0.0,
                    threshold=threshold,
                    dimensions={},
                    fixture=fixture_used,
                    error=err,
                )
            )
            continue

        scored = score_response(text, dimensions, selected=dims, global_penalties=penalties)
        agg = aggregate(scored)
        agg = max(0.0, min(1.0, agg + expect_bonus(text, expect)))
        detail = {
            d: {
                "score": round(r.score, 4),
                "weight": r.weight,
                "hits": r.hits,
                "penalties": r.penalties,
            }
            for d, r in scored.items()
        }
        for d, r in scored.items():
            dim_scores_accum.setdefault(d, []).append(r.score)

        results.append(
            ProbeResult(
                id=pid,
                session=probe.get("session", ""),
                prompt=probe.get("prompt", ""),
                passed=agg >= threshold and not err,
                aggregate=round(agg, 4),
                threshold=threshold,
                dimensions={d: round(r.score, 4) for d, r in scored.items()},
                detail=detail,
                fixture=fixture_used,
            )
        )

    # Mean dimension scores → vector map Mag update
    mean_dims = {d: sum(vs) / len(vs) for d, vs in dim_scores_accum.items() if vs}
    vmap.apply_dimension_scores(mean_dims, blend=0.4)

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    overall = sum(r.aggregate for r in results) / len(results) if results else 0.0
    report = SelftestReport(
        ok=failed == 0 and len(results) > 0,
        passed=passed,
        failed=failed,
        total=len(results),
        overall=round(overall, 4),
        dirichlet_energy=round(vmap.dirichlet_energy(), 6),
        probes=results,
        vector_map=vmap.snapshot(),
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        config=str(checklist_path),
        map_config=str(map_path),
    )

    # Write artifacts
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = out_dir / f"report_{stamp}.json"
    md_path = out_dir / f"report_{stamp}.md"
    map_json = out_dir / f"vector_map_{stamp}.json"
    map_md = out_dir / f"vector_map_{stamp}.md"
    latest_json = out_dir / "latest.json"
    latest_map = out_dir / "vector_map_latest.md"

    payload = report.to_dict()
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    latest_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    vmap.save_json(map_json)
    map_md.write_text(vmap.to_markdown(), encoding="utf-8")
    latest_map.write_text(vmap.to_markdown(), encoding="utf-8")
    md_path.write_text(_report_markdown(report), encoding="utf-8")

    return report


def _report_markdown(report: SelftestReport) -> str:
    lines = [
        "# Selftest Report",
        "",
        f"**When:** {report.timestamp}  ",
        f"**Overall:** {report.overall:.3f}  ",
        f"**Passed:** {report.passed}/{report.total}  ",
        f"**OK:** {report.ok}  ",
        f"**Dirichlet energy:** `{report.dirichlet_energy}`",
        "",
        "## Probes",
        "",
        "| Id | Session | Agg | Pass |",
        "|----|---------|-----|------|",
    ]
    for p in report.probes:
        mark = "✓" if p.passed else "✗"
        lines.append(f"| {p.id} | {p.session} | {p.aggregate:.3f} | {mark} |")
    lines.append("")
    lines.append("## Dimension means (from passed scoring)")
    lines.append("")
    # collect
    dim_vals: dict[str, list[float]] = {}
    for p in report.probes:
        for d, s in p.dimensions.items():
            dim_vals.setdefault(d, []).append(s)
    lines.append("| Dimension | Mean |")
    lines.append("|-----------|------|")
    for d, vs in sorted(dim_vals.items()):
        lines.append(f"| {d} | {sum(vs)/len(vs):.3f} |")
    lines.append("")
    lines.append("See companion `vector_map_*.md` for anchors and surrounding influences.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Run hybrid mirror selftest checklist")
    ap.add_argument("--checklist", default="")
    ap.add_argument("--map", dest="map_path", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--responses", default="", help="Dir of override response .txt files")
    args = ap.parse_args(argv)
    report = run_selftest(
        checklist_path=args.checklist or None,
        map_path=args.map_path or None,
        responses_dir=args.responses or None,
        out_dir=args.out or None,
    )
    print(
        f"selftest: {report.passed}/{report.total} passed | overall={report.overall:.3f} | "
        f"E={report.dirichlet_energy:.4f} | ok={report.ok}"
    )
    for p in report.probes:
        flag = "PASS" if p.passed else "FAIL"
        print(f"  [{flag}] {p.id:24s}  {p.aggregate:.3f}  {p.session}")
        if p.error:
            print(f"         error: {p.error}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
