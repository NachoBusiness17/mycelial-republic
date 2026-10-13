"""Re-resolve burn-wave file:line pointers against current bytes and flag rot.

B2-491 pointer-anchor law (2026-09-26, QUEUE.md header): every NEW file:line
pointer in a burn brief carries a byte anchor written path:NN[-MM]#token, where
token is the exact key name, symbol, or a double-quoted fragment the cited
lines contained at filing time. Disease this law closes: the B2-107 row cited
configs/providers.yaml:66-67 for the ollama base_url_env but the key sat at
line 84 by landing time (66-67 had become the tail of the saelis quota block),
and the B2-105 row's configs/providers.yaml:473-488 mistral pointer rotted
same-day to the z_ai region when the block moved to 534. A lane that trusts
the number reads the wrong block with no surface naming the rot; this checker
is that surface.

Verdict classes:
  ROT        anchored pointer whose anchor is absent from the cited range
             (report names the nearest matching line as the repair hint)
  ROT-SEED   legacy bare pointer whose expected token is known from SEEDS
             below and is absent from the cited range
  MISSING    cited file does not exist on disk (anchored or seeded only)
  OOB        cited end line is past EOF (anchored or seeded only)
  UNANCHORED legacy bare pointer with no anchor and no seed row; counted so
             the adoption gap stays visible, never fatal on its own
  OK         anchor found inside the cited range

Exit 0 clean, exit 1 while any ROT, ROT-SEED, MISSING or OOB stands.
UNANCHORED never moves the exit code (a board full of grandfathered history
must not cry wolf), it is printed so lanes can anchor on next touch.

Bare pointers are history: landed rows stay byte-untouched per the B2-255
precedent; the flag is the record, the repair hint is the correct target.

Usage:
  .venv/Scripts/python.exe tools/pointer_rot_check.py            # QUEUE only
  .venv/Scripts/python.exe tools/pointer_rot_check.py --briefs   # + B2_*.md receipts
  .venv/Scripts/python.exe tools/pointer_rot_check.py --json     # machine rows
  .venv/Scripts/python.exe tools/pointer_rot_check.py --selftest # fixture replay
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = REPO_ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
WAVE_DIR = DEFAULT_QUEUE.parent

# v1 resolves the first range of a pointer only: "f.yml:28-31,199,270" is
# checked as 28-31 and the suffix list is ignored (documented limitation).
POINTER_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_\-./\\]+\.(?P<ext>"
    r"py|yaml|yml|json|jsonl|md|txt|toml|cfg|ini|ps1|sh|bat|cmd|csv|tsv|sql|"
    r"lua|rbxlx|js|mjs|ts|html)"
    r"):(?P<start>\d+)(?:\s*-\s*(?P<end>\d+))?"
    r"(?:#(?P<anchor>\"[^\"]+\"|[^\s,)\];]+))?"
)

# Known-rot legacy pointers: cited range vs the token the brief says lived
# there. Provenance for every row; no fabricated entries.
SEEDS: dict[tuple[str, int, int], dict[str, str]] = {
    ("configs/providers.yaml", 66, 67): {
        "token": "base_url_env",
        "who": "B2-107 row (ollama base_url_env), named by the B2-491 brief",
    },
    ("configs/providers.yaml", 473, 488): {
        "token": "mistral",
        "who": "B2-105 row (mistral block), named in the B2-105 landing note and B2-456",
    },
}


def norm_path(raw: str) -> str:
    return str(Path(raw.replace("\\", "/"))).replace("\\", "/")


def resolve_target(raw: str) -> Path | None:
    cand = Path(raw.replace("\\", "/"))
    if cand.is_absolute():
        return cand if cand.exists() else None
    for base in (REPO_ROOT, WAVE_DIR):
        p = base / cand
        if p.exists():
            return p
    return None


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def anchor_variants(anchor: str) -> list[str]:
    a = anchor.strip()
    if a.startswith('"') and a.endswith('"') and len(a) >= 2:
        return [a[1:-1]]
    return [a]


def classify(path_raw: str, start: int, end: int, anchor: str | None) -> dict:
    """One pointer against current bytes. Never raises."""
    key = (norm_path(path_raw), start, end)
    seeded = SEEDS.get(key)
    token = None
    if anchor:
        token = anchor_variants(anchor)[0]
        kind = "anchored"
    elif seeded:
        token = seeded["token"]
        kind = "seeded"
    else:
        kind = "bare"

    rng = str(start) if start == end else f"{start}-{end}"
    out = {
        "pointer": f"{path_raw}:{rng}" + (f"#{anchor}" if anchor else ""),
        "kind": kind,
        "token": token,
        "verdict": "OK",
    }
    if seeded:
        out["seed"] = seeded["who"]

    target = resolve_target(path_raw)
    if target is None:
        out["verdict"] = "MISSING" if kind in ("anchored", "seeded") else "UNANCHORED"
        if out["verdict"] == "UNANCHORED":
            out["note"] = "file not found (bare pointer, counted not fatal)"
        return out

    lines = read_lines(target)
    if end > len(lines):
        out["verdict"] = "OOB" if kind in ("anchored", "seeded") else "UNANCHORED"
        out["file_lines"] = len(lines)
        if out["verdict"] == "UNANCHORED":
            out["note"] = f"end {end} past EOF {len(lines)} (bare pointer, counted not fatal)"
        return out

    window = lines[start - 1 : end]
    if token is not None and any(token in ln for ln in window):
        out["verdict"] = "OK"
        return out

    if kind == "bare":
        out["verdict"] = "UNANCHORED"
        out["note"] = "no anchor and no seed row; law requires one on next touch"
        return out

    out["verdict"] = "ROT-SEED" if kind == "seeded" else "ROT"
    # Hint discipline: a token mention in a comment is not the block. List
    # definition-like lines (token as a leading key) first, then raw hits,
    # capped; picking among candidates is the reader's confirmed-by-context job.
    hits = [i + 1 for i, ln in enumerate(lines) if token in ln]
    key_re = re.compile(r"^\s*" + re.escape(token) + r"\s*:")
    key_hits = [i + 1 for i, ln in enumerate(lines) if key_re.match(ln)]
    loc = key_hits or hits
    out["token_lines"] = loc[:8]
    out["token_lines_total"] = len(loc)
    if loc:
        shape = "definition-like" if key_hits else "occurrence"
        out["hint"] = (
            f"'{token}' {shape} at line(s) {', '.join(map(str, loc[:8]))}"
            + (f" (+{len(loc) - 8} more)" if len(loc) > 8 else "")
            + f"; re-issue {path_raw}:N#{token} with the line your block context names"
        )
    else:
        out["hint"] = f"'{token}' absent from the whole file"
    return out


def scan_text(text: str) -> list[dict]:
    found, seen = [], set()
    for m in POINTER_RE.finditer(text):
        start = int(m.group("start"))
        end = int(m.group("end") or start)
        if end < start:
            end = start
        raw_path = m.group("path")
        dedupe = (norm_path(raw_path), start, end, m.group("anchor"))
        if dedupe in seen:
            continue
        seen.add(dedupe)
        found.append(classify(raw_path, start, end, m.group("anchor")))
    return found


FATAL = ("ROT", "ROT-SEED", "MISSING", "OOB")


def summarize(findings: list[dict]) -> str:
    counts: dict[str, int] = {}
    for f in findings:
        counts[f["verdict"]] = counts.get(f["verdict"], 0) + 1
    order = ["OK", "ROT", "ROT-SEED", "MISSING", "OOB", "UNANCHORED"]
    return "pointers=%d " % len(findings) + " ".join(
        f"{k}={counts.get(k, 0)}" for k in order if counts.get(k)
    )


def selftest() -> int:
    """Replay the disease on a fixture: token at 84, brief cites 66-67."""
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        fixture = tdp / "fixture.yaml"
        lines = ["# filler line %d" % i for i in range(1, 84)]
        lines.append("    base_url_env: OLLAMA_HOST")  # line 84, the B2-107 shape
        lines += ["# tail %d" % i for i in range(85, 101)]
        fixture.write_text("\n".join(lines) + "\n", encoding="utf-8")
        brief = tdp / "brief.md"
        brief.write_text(
            "pointers fixture.yaml:66-67 + fixture.yaml:84#base_url_env"
            " + fixture.yaml:1-9999#base_url_env + nope.yaml:1-2#x"
            " + fixture.yaml:10\n",
            encoding="utf-8",
        )
        global REPO_ROOT, WAVE_DIR, SEEDS  # noqa: PLW0603 - selftest redirects roots
        real_root, real_wave, real_seeds = REPO_ROOT, WAVE_DIR, dict(SEEDS)
        REPO_ROOT, WAVE_DIR = tdp, tdp
        SEEDS[("fixture.yaml", 66, 67)] = {
            "token": "base_url_env",
            "who": "selftest replay of the B2-107 66-67 shape",
        }
        try:
            findings = scan_text(brief.read_text(encoding="utf-8"))
        finally:
            REPO_ROOT, WAVE_DIR = real_root, real_wave
            SEEDS.clear()
            SEEDS.update(real_seeds)
        got = {f["pointer"].split("#")[0]: f["verdict"] for f in findings}
        checks = [
            (got.get("fixture.yaml:66-67") == "ROT-SEED", f"seeded 66-67 reads ROT-SEED, got {got.get('fixture.yaml:66-67')}"),
            (findings[0].get("token_lines") == [84], f"hint names definition-like line 84, got {findings[0].get('token_lines')}"),
            (got.get("fixture.yaml:84") == "OK", "anchored 84 verifies OK"),
            (got.get("fixture.yaml:1-9999") == "OOB", "range past EOF reads OOB"),
            (got.get("nope.yaml:1-2") == "MISSING", "absent file reads MISSING"),
            (got.get("fixture.yaml:10") == "UNANCHORED", "bare no-seed pointer reads UNANCHORED, not fatal"),
        ]
        ok = True
        for cond, name in checks:
            print(("PASS " if cond else "FAIL ") + name)
            ok = ok and cond
        print("selftest verdicts: " + summarize(findings))
        return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--queue", default=str(DEFAULT_QUEUE), help="board file to scan")
    ap.add_argument("--briefs", action="store_true", help="also scan B2_*.md wave receipts")
    ap.add_argument("--json", action="store_true", dest="as_json", help="machine rows")
    ap.add_argument("--selftest", action="store_true", help="fixture replay of the disease")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    surfaces: list[tuple[str, str]] = []
    qpath = Path(args.queue)
    surfaces.append((str(qpath), qpath.read_text(encoding="utf-8", errors="replace")))
    if args.briefs:
        for p in sorted(WAVE_DIR.glob("B2_*.md")):
            surfaces.append((str(p), p.read_text(encoding="utf-8", errors="replace")))

    findings: list[dict] = []
    for surface, text in surfaces:
        for f in scan_text(text):
            f["surface"] = surface
            findings.append(f)

    fatal = [f for f in findings if f["verdict"] in FATAL]
    if args.as_json:
        print(json.dumps({"summary": summarize(findings), "exit": 1 if fatal else 0,
                          "findings": findings}, ensure_ascii=True, indent=1))
    else:
        for f in fatal:
            extra = f" | {f.get('hint', '')}" if f.get("hint") else ""
            seed = f" | seed: {f['seed']}" if f.get("seed") else ""
            print(f"{f['verdict']:10s} {f['pointer']}{seed}{extra}")
        print(summarize(findings))
        unanchored = [f for f in findings if f["verdict"] == "UNANCHORED"]
        if unanchored:
            print(f"UNANCHORED census: {len(unanchored)} bare pointer(s) carry no byte anchor;"
                  " the B2-491 law requires one on next touch")
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
