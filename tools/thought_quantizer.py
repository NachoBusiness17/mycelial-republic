#!/usr/bin/env python3
"""thought_quantizer — the standing compiler for the tiered instruction packs.

HISTORY (the fossil this tool replaces): v0.2 was an INLINE one-night walk
(2026-09-18, NIGHT_FOLD_20260918.md section 3) that compiled
memory/percolator/invariants.json into instructions_{frontier,flash,local}
packs and was never run again; the packs fossilized with zero staleness
alarms and zero live consumers. This tool makes the compile repeatable
(FOSSIL_CENSUS_20260927.md P0-1).

SEMANTICS BY VERSION - the full per-version law text rides the compile
report (v3_amendment / v4_amendment / v7_amendment fields): v0.3 two-pass
classification (fragments + pure telemetry refuse, error-quoting LAWS keep
when imperative-shaped; weight = recency x shape, counts are provenance
only); v0.4 quantizer-hygiene (L1 shell-error fragments refuse unless
genuinely imperative; L3 one decay constant PACK_STALE_DAYS at all three
sites; L4 linker law kept==packed, disjoint bands); v0.5 R4-L1
MIN_KEPT_LAWS (an empty compile never serves as law; refusal fires BEFORE
any pack write); v0.6 R4b move 1 (the two law stacks merge at the compile:
mag.rib_boot.lawpack_amendment_rows() rides at weight 1.0 beside the
percolator feed; an unmounted rib refuses the compile).

v0.7 law (run ml-moonshot-20261007 lane ml7): THE PROPAGATION BRIDGE -
classical models are LAWS too. ml3's router + ml4's forecaster (artifacts
named in tools/classical_law_feed.py) ride as pack rows whose law text is
the artifact path + feature importances / regression coefficients, weight
1.0, pinned to the head of the flash band (structural, not rank luck);
absent artifacts are a census fact, never a silent skip or a refuser.

Run:  .venv/Scripts/python.exe tools/thought_quantizer.py compile
      .venv/Scripts/python.exe tools/thought_quantizer.py --check   # fossil arm
Exit: compile 0 ok / 2 input error; --check 0 fresh / 1 stale / 2 no report.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))  # mag.constants import below; tools/ is not self-contained

from mag.constants import PACK_STALE_DAYS  # noqa: E402  (the one decay bar, L3)
# v0.7: the classical-model feed lives in its own module (extraction cures
# the file-length debt); these re-exports keep one import surface, including
# _rel_posix (moved here with its outside-repo ValueError cause comment).
from tools.classical_law_feed import (  # noqa: E402
    ML3_METRICS, ML4_CHECKPOINTS, _rel_posix, compose_ml3_law, compose_ml4_law,
    live_classical_rows, ml3_router_row, ml4_ridge_coefficients,
    pin_classical_first)


DEFAULT_IN = ROOT / "memory" / "percolator" / "invariants.json"
OUT_DIR = ROOT / "memory" / "corpus" / "quantized_thought"

_VERBS = (
    r"(verify|refuse|never|always|run|read|check|gate|file|land|bank|"
    r"fold|elevate|keep|drop|rebuild|seal|register|name|trust|write|surface|"
    r"block|wire|test|prove|quote|append|declare|start|stop|kill|route|"
    r"drain|prune|accept|fix|recompile|tombstone|stat|diff)")
IMPERATIVE_RE = re.compile(r"(?i)\b" + _VERBS + r"\b")
TELEMETRY_RE = re.compile(
    r"(?i)(https?://|error|failed|failure|not reachable|unreachable|"
    r"traceback|exit code|reported|backend|timeout|exception|refused|"
    r"crashed|stack trace)")
LAW_SHAPE_RE = re.compile(
    r"(?i)\b(only with|must be|is not truth|never trust|before declaring|"
    r"until verified|counts? as|by definition|no longer)\b")
# L1 (v0.4): shapes that match the shell-error LINE itself - a machine
# event, not a norm - plus the escapes that make the text a genuine norm.
SHELL_ERROR_RE = re.compile(
    r"(?i)(\[errno\s*\d+\]|no such file or directory|is not recognized as|"
    r"command not found|permission denied|no module named|"
    r"traceback \(most recent call last\)|segmentation fault|"
    r"cannot find the (?:path|file)|file not found)")
NORM_MODAL_RE = re.compile(
    r"(?i)\b(must|shall|should|always|never|do not|don't|whenever)\b")
CONDITIONAL_LAW_RE = re.compile(
    r"(?i)^(?:when|if|whenever|before|after)\b.{0,200}?\b" + _VERBS + r"\b")

FRAGMENT_MIN_CHARS = 25
FLASH_MAX_CHARS = 220
LOCAL_MAX_WORDS = 10

# v0.5 (R4-L1 min-rows assertion): a compile that keeps fewer laws than this
# is refused before any pack file is written. 1 is the honest floor for "an
# empty compile can never serve as law" - a zero-law pack stamped fresh is
# worse than a stale pack, because the consumer's staleness debt pointer is
# the only alarm left and the fresh stamp silences it.
MIN_KEPT_LAWS = 1

def classify(text: str) -> tuple[str, str]:
    """Return (verdict, shape) where verdict in
    {keep, refuse-fragment, refuse-telemetry} and shape in
    {imperative-lead, imperative, law-statement, statement}."""
    t = text.strip()
    if len(t) < FRAGMENT_MIN_CHARS:
        return "refuse-fragment", "statement"
    lead = bool(IMPERATIVE_RE.match(t)) or bool(
        IMPERATIVE_RE.match(t.split(":", 1)[-1].strip()) if ":" in t else False)
    anywhere = bool(IMPERATIVE_RE.search(t))
    lawish = bool(LAW_SHAPE_RE.search(t))
    if lead:
        shape = "imperative-lead"
    elif anywhere:
        shape = "imperative"
    elif lawish:
        shape = "law-statement"
    else:
        shape = "statement"
    has_tele = bool(TELEMETRY_RE.search(t))
    # L1 (v0.4): a shell-error fragment is a machine event, not a norm. The
    # v0.3 imperative-shape escape alone let "[Errno 2] No such file or
    # directory: 'powershell'" pack as law (3 of 12 flash rows, w4-27 L1)
    # because "file" sits inside the error text; keeping one now requires
    # normative framing BEYOND the quote: law grammar, a normative modal,
    # or a conditional do-X frame.
    if SHELL_ERROR_RE.search(t) and not (
            lawish
            or NORM_MODAL_RE.search(t)
            or CONDITIONAL_LAW_RE.match(t)):
        return "refuse-telemetry", shape
    if has_tele and shape in ("statement", "law-statement"):
        return "refuse-telemetry", shape
    return "keep", shape


def recency_score(last_seen: str, now: float) -> float:
    try:
        ts = datetime.fromisoformat(last_seen.replace("Z", "+00:00")).timestamp()
    except (ValueError, AttributeError):
        return 0.15
    age_d = max(0.0, (now - ts) / 86400.0)
    if age_d <= 2:
        return 1.0
    if age_d <= 7:
        return 0.75
    if age_d <= 14:
        return 0.5
    if age_d <= 30:
        return 0.3
    return 0.15


SHAPE_W = {"imperative-lead": 1.0, "imperative": 0.8,
           "law-statement": 0.6, "statement": 0.4}


def signature(text: str) -> str:
    t = re.sub(r"(?i)^\[[^\]]+\]\s*", "", text.strip().lower())
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:60]


def to_flash(text: str) -> str:
    t = re.sub(r"(?i)^\[[^\]]+\]\s*", "", text.strip())
    first = re.split(r"(?<=[.!?])\s", t)[0]
    return (first[:FLASH_MAX_CHARS]).strip()


def to_local(text: str) -> str:
    words = [w for w in re.split(r"\s+", to_flash(text)) if w]
    return " ".join(words[:LOCAL_MAX_WORDS])


def compile_packs(in_path: Path, out_dir: Path, sizes: dict[str, int],
                  now: float | None = None,
                  rib_rows: dict[str, dict] | None = None,
                  classical_rows: dict[str, dict] | None = None) -> dict:
    now = now or time.time()
    data = json.loads(in_path.read_text(encoding="utf-8"))
    inv = data.get("invariants") if isinstance(data, dict) else data
    if not isinstance(inv, dict):
        raise SystemExit(f"input error: invariants shape unexpected in {in_path}")

    # v0.6: vault feed beside percolator (rib rows first; None = live vault)
    if rib_rows is None:
        from mag.rib_boot import lawpack_amendment_rows
        rib_rows, rib_feed = lawpack_amendment_rows(now)
    else:
        rib_feed = {"source": "caller-injected (test)", "rows": len(rib_rows)}

    # v0.7: classical-model feed beside both (None = live run artifacts)
    if classical_rows is None:
        classical_rows, classical_feed = live_classical_rows()
    else:
        classical_feed = {"source": "caller-injected (test)",
                          "rows": len(classical_rows)}

    census = {"in": len(inv), "refused_telemetry": 0, "refused_fragments": 0,
              "dedupes": 0, "kept": 0, "error_quoting_laws_kept": 0,
              "packed": 0, "rib_amendments_in": len(rib_rows),
              "rib_amendments_kept": 0,  # v0.6: the vault feed, counted
              "classical_models_in": len(classical_rows),  # v0.7 feed
              "classical_rows_kept": 0}
    merged: dict[str, dict] = {}
    for key, row in (list(rib_rows.items()) + list(classical_rows.items())
                     + list(inv.items())):
        text = str(row.get("text", "")).strip()
        if not text:
            continue
        sig = signature(text)
        if sig in merged:
            merged[sig]["sources"].append(key)
            merged[sig]["raw_count"] += int(row.get("count", 0))
            census["dedupes"] += 1
            continue
        if key in rib_rows:  # vault law: ranked at 1.0, never the refusals
            verdict, shape, weight = "keep", "vault-amendment", 1.0
            census["rib_amendments_kept"] += 1
        elif key in classical_rows:  # v0.7: machine-authored law, never refused
            verdict, shape, weight = "keep", "classical-model", 1.0
            census["classical_rows_kept"] += 1
        else:
            verdict, shape = classify(text)
            if verdict == "refuse-fragment":
                census["refused_fragments"] += 1
                continue
            if verdict == "refuse-telemetry":
                census["refused_telemetry"] += 1
                continue
            if TELEMETRY_RE.search(text) and shape in ("imperative-lead", "imperative"):
                census["error_quoting_laws_kept"] += 1  # the v0.3 heal, counted
            weight = round(recency_score(str(row.get("last_seen", "")), now)
                           * SHAPE_W[shape], 3)
        merged[sig] = {
            "id": key[:12], "class": "law",
            "raw_count": int(row.get("count", 0)),
            "count_verdict": "inflated echo - provenance only",
            "weight": weight, "shape": shape,
            "last_seen": str(row.get("last_seen", ""))[:10],
            "sources": [key], "frontier": text,
        }
        if key in classical_rows:  # training rows are provenance, not echo
            merged[sig]["count_verdict"] = "training rows - provenance only"
    census["kept"] = len(merged)
    # v0.5 min-rows assertion (R4-L1, 2026-10-05): refuse BEFORE any pack
    # file is touched. A zero-law compile writing empty packs + a fresh
    # report stamp would un-hide the consumer debt pointer and boot every
    # seat on zero law with a green freshness face - the exact silent
    # failure the ouroboros R4 synthesis move 2 demanded be made
    # impossible. Cause: an empty --in or a classifier shape drift kept 0
    # rows; fix evidence: tests/test_thought_quantizer.py
    # test_min_rows_refuses_empty_compile.
    if census["kept"] < MIN_KEPT_LAWS:
        raise SystemExit(
            f"input error: classification kept {census['kept']} laws "
            f"(< {MIN_KEPT_LAWS} min) from {census['in']} rows; refusing to "
            "write empty packs - an empty compile must never serve as law")
    ranked = sorted(merged.values(), key=lambda r: -r["weight"])
    # v0.7: the classical layer heads the flash band structurally - the full
    # pin law lives on pin_classical_first (tools/classical_law_feed.py).
    ranked = pin_classical_first(ranked)

    # L4 linker law (v0.4): every kept law lands in EXACTLY one tier pack -
    # kept == packed, no kept-but-unpacked limbo. The v0.3 rank cutoff
    # (ranked[:n] per tier, every tier mirroring the top rows) left 283 of
    # 307 kept laws in no pack with zero counters anywhere (w4-27 L4, the
    # s2-23 roll-up row 8). Bands: flash (the consumer seam every seat
    # boots) takes the top-ranked rows, frontier the next band, local the
    # remainder. A cap <= 0 takes all remaining.
    order = [t for t in ("flash", "frontier", "local") if t in sizes]
    bands: dict[str, list[dict]] = {}
    cursor = 0
    for tier in order:
        cap = sizes[tier]
        take = len(ranked) - cursor if not cap or cap <= 0 \
            else min(int(cap), len(ranked) - cursor)
        bands[tier] = ranked[cursor:cursor + take]
        cursor += take
    if cursor != len(ranked):
        raise SystemExit(
            f"linker error: kept {census['kept']} != packed {cursor} "
            "(every kept law must land in exactly one tier pack; pass a "
            "cap <= 0 on the last tier to take the remainder)")

    out_dir.mkdir(parents=True, exist_ok=True)
    packs_written = {}
    for tier in sizes:
        rows = []
        for r in bands.get(tier, []):
            row = dict(r)
            if tier != "frontier":
                row[tier] = to_local(r["frontier"]) if tier == "local" \
                    else to_flash(r["frontier"])
            row["status"] = "compiled-v0.7"
            rows.append(row)
        p = out_dir / f"instructions_{tier}.jsonl"
        p.write_text("\n".join(json.dumps(r, ensure_ascii=False)
                               for r in rows) + "\n", encoding="utf-8")
        packs_written[tier] = len(rows)
    census["packed"] = sum(packs_written.values())

    report = {
        "compiled": datetime.now(timezone.utc).isoformat(),
        "v": "0.7",
        "stats": census,
        "packs": packs_written,
        "law": ("quantize thought: frontier nuance -> flash imperatives -> "
                "local laws; dedupe by signature; fragments+telemetry refused; "
                "weight=recency x shape"),
        "v3_amendment": ("two-pass classification healed the v0.2 over-refuse: "
                         "error-quoting LAWS are kept when imperative-shaped "
                         "(error_quoting_laws_kept counts them); v0.2 refused "
                         "them wholesale"),
        "v4_amendment": ("ball-20260929 quantizer-hygiene: L1 shell-error "
                         "fragments refuse unless genuinely imperative; "
                         "L3 decay unified on PACK_STALE_DAYS "
                         "(mag/constants.py) at producer+consumer+boot; "
                         "L4 linker law kept==packed, disjoint bands"),
        "v7_amendment": ("ml-moonshot-20261007 propagation bridge: classical "
                         "models are LAWS too, riding as pinned flash rows "
                         "(artifact path + fitted weights as the law text)"),
        "rib_feed": rib_feed,
        "classical_feed": classical_feed,
        "input": _rel_posix(in_path),
    }
    (out_dir / "compile_report.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8")
    return report


def check(max_age_days: float | None = None) -> int:
    """Fossil arm: exit 1 when the packs are older than the ONE decay bar.

    The bar is PACK_STALE_DAYS (mag/constants.py) - the same constant the
    consumer (mag/context_pack._quantized_laws) and the boot meter
    (tools/freshness_check) read - so a pack can never be fresh for its
    compiler and stale for its readers, or the reverse (L3, w4-27).
    """
    rp = OUT_DIR / "compile_report.json"
    if not rp.is_file():
        print("THOUGHT-QUANTIZER: no compile report; packs never compiled here")
        return 2
    rep = json.loads(rp.read_text(encoding="utf-8"))
    try:
        ts = datetime.fromisoformat(rep["compiled"]).timestamp()
    except (KeyError, ValueError):
        print("THOUGHT-QUANTIZER: report unreadable ts")
        return 2
    bar_d = PACK_STALE_DAYS if max_age_days is None else float(max_age_days)
    age_d = (time.time() - ts) / 86400.0
    if age_d > bar_d:
        print(f"THOUGHT-QUANTIZER: STALE packs, {age_d:.1f}d old "
              f"(bar {bar_d:g}d) - recompile owed (fossil-in-feed law)")
        return 1
    print(f"THOUGHT-QUANTIZER: fresh, {age_d:.1f}d old (v{rep.get('v')})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", nargs="?", default="compile",
                    choices=["compile", "check"])
    ap.add_argument("--check", action="store_true",
                    help="staleness check instead of compile (fossil arm)")
    ap.add_argument("--in", dest="in_path", default=str(DEFAULT_IN))
    ap.add_argument("--out", default=str(OUT_DIR))
    ap.add_argument("--frontier", type=int, default=24)
    ap.add_argument("--flash", type=int, default=12)
    ap.add_argument("--local", type=int, default=0,
                    help="local tier cap; <= 0 takes all remaining kept "
                         "laws (the L4 linker law: kept == packed)")
    ap.add_argument("--max-age-days", type=float, default=None,
                    help="staleness bar override in days (default: the "
                         f"shared PACK_STALE_DAYS = {PACK_STALE_DAYS:g}d "
                         "from mag/constants.py)")
    a = ap.parse_args()
    if a.check or a.mode == "check":
        return check(a.max_age_days)
    rep = compile_packs(Path(a.in_path), Path(a.out),
                        {"frontier": a.frontier, "flash": a.flash,
                         "local": a.local})
    print(f"THOUGHT-QUANTIZER v{rep['v']} compiled:",
          json.dumps(rep["stats"], ensure_ascii=False))
    print("packs:", rep["packs"],
          "| kept==packed (linker law):",
          rep["stats"]["kept"] == rep["stats"]["packed"],
          "| classical rows pinned:", rep["stats"]["classical_rows_kept"],
          "| error-quoting laws kept (v0.3 heal):",
          rep["stats"]["error_quoting_laws_kept"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
