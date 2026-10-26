"""code_swarm - the standing codebase swarm-review instrument (SWARM-1, 2026-10-01).

Operator mission: "we can launch swarms against our codebase like we do our
5.3 lanes". Input = a file list or a DOLLAR_BURN_SWEEP grid filter
(--triple-violators) + the review contract. For each target file x family it
stages ONE gated ask: file bytes inline, sha-stamped, contract bytes
identical across families (the G2 law), fires through
tools/model_garden.run_ask (gated rail: inference_budget recipes, refusal +
EMPTY_REASONING terminals, usage ledger), grades the machine-checkable
parts, and rolls up cross-family convergence per file at CLAIM level: 2+
families naming the same defect = REAL; same line-window, different
diagnosis = CO-LOCATION (CROSS_RACTOR_MATRIX meta-finding 1; never
bucket-level agreement).

Families default to the near-free tier (kimi on Nous credits, glm-flash on
the z.ai coding endpoint, deepseek flash). DeepSeek rides the garden rail
rather than the ds_workhorse CLI because the rail applies the deepseek
recipe (thinking-off, review floor) and banks terminals; one attempt per
ask; --cap usd (default 2.0) checked against this run's metered ledger rows
before every dispatch, overrun skips and names the remainder.

Usage:
  python tools/code_swarm.py --run swarm1 --triple-violators --stage --fire
  python tools/code_swarm.py --run swarm1 --rollup
Stages under watch/inbox/model_garden/<run>/ (asks/, raw/, manifest.jsonl,
rollup.json); raw replies land at watch/inbox/model_garden/<ask_id>.md per
the carrier contract, then copy to raw/<family>/<file>.md.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from mag.inference_budget import plan_call  # noqa: E402  organ a: fire path rides the budget rail
from tools import model_garden as mg  # noqa: E402

GARDEN = ROOT / "watch" / "inbox" / "model_garden"
SWEEP_GRID = GARDEN / "dollar_burn_20261001" / "sweep_grid.json"
CAP_CHARS = 120_000
EM_DASH = "\u2014"
LINE_RE = re.compile(r"^(DEFECT \d+|DEAD-CODE|ONE-SITTING FIX):\s*(.*)$")
CITE_RE = re.compile(r"EVIDENCE:\s*`?([^\s|`]+)")
WINDOW = 15  # cross-family line-window overlap tolerance (claim-level cluster)
STOP = frozenset(("the and for with that this without never also its into from "
                  "are when which does then your you file line code path same "
                  "call calls data name named uses using used will would never "
                  "missing wrong right real only more most less least").split())

FAMILIES = {  # near-free tier, ids/base_urls byte-proven by the cheapgrid series
    "kimi": {"model": "moonshotai/kimi-k2", "base_env": "HERMES_API_KEY_2",
             "base_url": "https://inference-api.nousresearch.com/v1"},
    "glm-flash": {"model": "glm-5.3-flash", "base_env": "ZAI_API_KEY_Pro",
                  "base_url": "https://api.z.ai/api/coding/paas/v4"},
    "deepseek": {"model": "deepseek-chat", "base_env": "DEEPSEEK_API_KEY",
                 "base_url": "https://api.deepseek.com/v1"},
}

CONTRACT = (
    "You are reviewing one live file of the Mag estate (a local-first agent "
    "harness on Windows). This file already carries three KNOWN wiring "
    "violations, do NOT re-report them: (a) fires LLM calls without importing "
    "mag.inference_budget, (b) fetches remote URLs without a browser "
    "User-Agent, (c) writes shared jsonl/json surfaces without atomic "
    "tmp+replace.\n\n"
    "Reply with EXACTLY this shape, 6 lines max, nothing else (omit any "
    "DEFECT line you cannot ground):\n"
    "DEFECT 1: <one-line defect claim, worst first> | EVIDENCE: <path>:<line or range> | FIX: <one-line fix>\n"
    "DEFECT 2: <same shape>\n"
    "DEFECT 3: <same shape>\n"
    "DEAD-CODE: <one dead-code candidate> | EVIDENCE: <path>:<line or range>\n"
    "ONE-SITTING FIX: <the single highest-value fix doable in one sitting> | EVIDENCE: <path>:<line or range>\n\n"
    "LAWS:\n"
    "- Every EVIDENCE cite uses the exact path printed in the SOURCE header "
    "and real line numbers of the SOURCE below.\n"
    "- Rank by damage: DEFECT 1 is the worst real defect beyond the known "
    "organ violations.\n"
    "- No em-dash characters anywhere in the reply.\n"
    "- No praise, no docstring restatement, no speculation presented as "
    "fact; drop a claim you cannot ground, never guess.\n\n"
    "<SOURCE path={path} sha256={sha} lines={lines}>\n{body}</SOURCE>")


def _atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def load_targets(mode: str, files: list[str]) -> list[str]:
    if mode == "files":
        return files
    grid = json.loads(SWEEP_GRID.read_text(encoding="utf-8"))
    out = []
    for rel, row in grid.items():
        v = row.get("verdicts") or {}
        if all((v.get(k) or {}).get("v") == "NO-violation" for k in ("a", "b", "c")):
            out.append(rel.replace("\\", "/"))
    return sorted(out)


def build_manifest(run: str, files: list[str], families: list[str]) -> list[dict]:
    """Stage one ask dir per (file, family); returns the manifest rows."""
    run_root = GARDEN / run
    rows = []
    for rel in files:
        rel = rel.replace("\\", "/")
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        digest = sha256(text.encode("utf-8", "replace")).hexdigest()[:16]
        n_lines = len(text.splitlines())
        body = text if len(text) <= CAP_CHARS else (
            text[:CAP_CHARS] + f"\n... [truncated at {CAP_CHARS} chars of "
            f"{len(text)}; line cites must stay <= {n_lines}]")
        contract = CONTRACT.format(path=rel, sha=digest, lines=n_lines, body=body)
        for fam in families:
            cfg = FAMILIES[fam]
            ask_id = f"{run}-{fam}-{_slug(rel)}"
            d = run_root / "asks" / ask_id
            d.mkdir(parents=True, exist_ok=True)
            _atomic_write(d / "ask.json", json.dumps({
                "id": ask_id, "model": cfg["model"], "base_env": cfg["base_env"],
                "base_url": cfg["base_url"], "contract": contract,
                "evidence": [], "self_contained": True}, ensure_ascii=False))
            plan = plan_call(model=cfg["model"], prompt_chars=len(contract))
            rows.append({"file": rel, "sha256": digest, "lines": n_lines,
                         "truncated": len(text) > CAP_CHARS, "family": fam,
                         "ask_id": ask_id, "ask_dir": str(d.relative_to(ROOT)),
                         "recipe": plan.recipe_key, "shape": plan.shape,
                         "max_tokens": plan.max_tokens})
    _atomic_write(run_root / "manifest.jsonl",
                  "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    return rows


def _slug(rel: str) -> str:
    return rel.replace("/", "__").rsplit(".", 1)[0]


def _run_spend(run: str) -> float:
    spend = 0.0
    if mg.USAGE.exists():
        for line in mg.USAGE.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(row.get("id", "")).startswith(run + "-"):
                spend += row.get("cost_usd", 0) or 0
    return spend


def fire(run: str, rows: list[dict], concurrency: int, cap: float) -> list[dict]:
    """Fan out the asks across families; polite width, one attempt each."""
    lock = threading.Lock()
    orig_bank = mg._bank

    def _locked_bank(row: dict) -> None:  # serialize ledger appends across threads
        with lock:
            orig_bank(row)

    mg._bank = _locked_bank

    def one(row: dict) -> dict:
        if _run_spend(run) >= cap:
            return {"id": row["ask_id"], "ok": True,
                    "skipped": "budget cap reached before dispatch"}
        try:
            return mg.run_ask(Path(row["ask_dir"]))
        except Exception as exc:  # noqa: BLE001 - named per ask, never silent
            return {"id": row["ask_id"], "ok": False, "error": repr(exc)[:300]}

    results = []
    try:
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futs = {ex.submit(one, r): r for r in rows}
            for f in as_completed(futs):
                res = f.result()
                results.append(res)
                print(f"{'OK ' if res.get('ok') else 'FAIL'} {res['id']} "
                      f"[{res.get('cost_usd', 0):.4f} usd]"
                      + (" (" + str(res.get("skipped") or res.get("error"))[:80] + ")"
                         if res.get("skipped") or res.get("error") else ""),
                      flush=True)
    finally:
        mg._bank = orig_bank
    return results


def parse_reply(reply: str, path: str, n_lines: int) -> dict:
    """Machine-checkable grade of one reply against its target file."""
    defects, dead, fix = [], None, None
    shape = cites_ok = True
    for line in (l for l in reply.splitlines() if l.strip()):
        m = LINE_RE.match(line.strip())
        if not m:
            shape = False
            continue
        label, rest = m.group(1), m.group(2)
        c = CITE_RE.search(rest)
        nums, p_ok = [], True
        if c:
            token = c.group(1).rstrip(".,;")
            p, _, nums_part = token.partition(":")
            nums = [int(x) for x in re.findall(r"\d+", nums_part)]
            p_ok = p == path
            cites_ok = cites_ok and p_ok
        entry = {"raw": line.strip(), "start": min(nums) if nums else None,
                 "nums": nums, "path_ok": p_ok,
                 "lines_ok": all(1 <= n <= n_lines for n in nums)}
        if label.startswith("DEFECT"):
            entry["claim"] = rest.split("|")[0].strip()
            defects.append(entry)
        elif label == "DEAD-CODE":
            dead = entry
        else:
            fix = entry
    return {"defects": defects, "dead_code": dead, "one_sitting": fix,
            "checks": {"shape": shape, "cites_resolve": cites_ok,
                       "lines_in_range": all(d["lines_ok"] for d in defects
                                             + [x for x in (dead, fix) if x]),
                       "no_em_dash": EM_DASH not in reply,
                       "max_lines": len([l for l in reply.splitlines()
                                         if l.strip()]) <= 6}}


def _sig(claim: str) -> set[str]:
    return {w for w in re.findall(r"[a-z_]+", claim.lower())
            if len(w) > 3 and w not in STOP}


def converge(graded: list[dict]) -> list[dict]:
    """Claim-level clusters: 2+ families, window overlap; lexical overlap
    on the claim decides REAL vs CO-LOCATION (never bucket-level agreement)."""
    clusters = []
    by_file: dict[str, list[dict]] = {}
    for g in graded:
        for d in g["defects"]:
            if d["start"] is None:
                continue
            by_file.setdefault(g["file"], []).append({**d, "family": g["family"]})
    for path, defs in by_file.items():
        parent = list(range(len(defs)))

        def find(i: int) -> int:
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        for i in range(len(defs)):
            for j in range(i + 1, len(defs)):
                a, b = defs[i], defs[j]
                if (a["family"] != b["family"] and a["start"] is not None
                        and b["start"] is not None
                        and abs(a["start"] - b["start"]) <= WINDOW):
                    parent[find(j)] = find(i)
        groups: dict[int, list[dict]] = {}
        for i, d in enumerate(defs):
            groups.setdefault(find(i), []).append(d)
        for members in groups.values():
            fams = sorted({m["family"] for m in members})
            pairs = [(a, b) for k, a in enumerate(members)
                     for b in members[k + 1:] if a["family"] != b["family"]]
            lexical = [len(_sig(a["claim"]) & _sig(b["claim"])) >= 2
                       for a, b in pairs]
            clusters.append({
                "file": path, "lines": sorted({m["start"] for m in members}),
                "families": fams, "n_families": len(fams),
                "status": ("REAL" if len(fams) >= 2 and any(lexical)
                           else "CO-LOCATION" if len(fams) >= 2 else "UNIQUE"),
                "claims": [{"family": m["family"], "line": m["start"],
                            "claim": m["claim"]} for m in members]})
    return sorted(clusters, key=lambda c: (-c["n_families"], c["file"]))


def family_behavior_fold(run: str, graded: list[dict], clusters: list[dict],
                         cost_usd: float) -> list[dict]:
    """SELFSTEAL_53_ERA upgrade 5 (family-behavior fold-back): every swarm run
    becomes router training data. Appends one row per family per run to
    memory/runs/model_garden/family_behavior.jsonl. Field honesty: outcome
    counts, terminal kinds (channel), defects claimed, and cluster economics
    come from the graded rows; per-family 429 contacts / tokens / cost need a
    usage-ledger join that is NOT wired here - those legs are named absent
    rather than fabricated. Returns the rows it banked."""
    behavior_path = ROOT / "memory" / "runs" / "model_garden" / "family_behavior.jsonl"
    fams = sorted({g["family"] for g in graded})
    by_fam_cluster: dict[str, dict[str, int]] = {f: {"REAL": 0, "CO-LOCATION": 0, "UNIQUE": 0} for f in fams}
    for c in clusters:
        for m in c["claims"]:
            if m["family"] in by_fam_cluster:
                by_fam_cluster[m["family"]][c["status"]] = by_fam_cluster[m["family"]].get(c["status"], 0) + 1
    rows_out = []
    for f in fams:
        g_rows = [g for g in graded if g["family"] == f]
        channels = {}
        for g in g_rows:
            if g.get("ok"):
                channels[g.get("channel", "?")] = channels.get(g.get("channel", "?"), 0) + 1
        rows_out.append({
            "schema": "family_behavior.v1", "run": run, "family": f,
            "asks": len(g_rows), "landed": sum(1 for g in g_rows if g.get("ok")),
            "terminals": channels,
            "defects_claimed": sum(len(g.get("defects") or []) for g in g_rows if g.get("ok")),
            "cluster_membership": by_fam_cluster[f],
            "cost_usd_run": round(cost_usd, 4),
            "not_wired": ["per_family_429_contacts", "per_family_tokens", "per_family_cost"],
        })
    behavior_path.parent.mkdir(parents=True, exist_ok=True)
    with behavior_path.open("a", encoding="utf-8") as fh:
        for row in rows_out:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return rows_out


def rollup(run: str, rows: list[dict]) -> dict:
    """Grade every landed reply, converge, copy raw sidecars, bank rollup.json."""
    run_root = GARDEN / run
    graded = []
    for r in rows:
        out = mg.OUT_DIR / f"{r['ask_id']}.md"
        g = {"file": r["file"], "family": r["family"], "ask_id": r["ask_id"],
             "sha_at_ask": r["sha256"], "ok": False}
        if out.is_file():
            raw = out.read_text(encoding="utf-8", errors="replace")
            head, _, body = raw.partition("\n\n")
            g.update(ok=True, channel="reasoning" if "channel: reasoning" in head
                     else "content", **parse_reply(body, r["file"], r["lines"]))
            dest = run_root / "raw" / r["family"] / (_slug(r["file"]) + ".md")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(out, dest)
        # version-drift law: stamp whether the file moved since the ask
        cur = (ROOT / r["file"]).read_text(encoding="utf-8", errors="replace")
        g["sha_drift_since_ask"] = (sha256(cur.encode("utf-8", "replace"))
                                    .hexdigest()[:16] != r["sha256"])
        graded.append(g)
    clusters = converge([g for g in graded if g.get("ok")])
    cost = round(_run_spend(run), 4)
    out = {"run": run, "asks": len(rows), "landed": sum(g["ok"] for g in graded),
           "cost_usd": cost,
           "graded": graded, "clusters": clusters}
    # SELFSTEAL_53 upgrade 5: the run feeds the router-priors ledger at close
    behavior = family_behavior_fold(run, graded, clusters, cost)
    unique_n = sum(1 for c in clusters if c["status"] == "UNIQUE")
    if clusters:
        print(f"[economics] unique {unique_n} / {len(clusters)} clusters "
              f"({100 * unique_n // len(clusters)} pct unique-share; "
              f"rising dup-share = cut a family)", flush=True)
    _atomic_write(run_root / "rollup.json",
                  json.dumps(out, ensure_ascii=False, indent=1))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="code_swarm")
    ap.add_argument("--run", required=True, help="run id (dir under model_garden)")
    ap.add_argument("--triple-violators", action="store_const",
                    const="triple-violators", dest="mode")
    ap.add_argument("--files", nargs="*", dest="mode2", action="store",
                    help="explicit repo-relative file list")
    ap.add_argument("--families", nargs="*",
                    default=["kimi", "glm-flash", "deepseek"])
    ap.add_argument("--stage", action="store_true")
    ap.add_argument("--fire", action="store_true")
    ap.add_argument("--rollup", action="store_true")
    ap.add_argument("--concurrency", type=int, default=10)
    ap.add_argument("--cap", type=float, default=2.0)
    args = ap.parse_args(argv)
    run_root = GARDEN / args.run
    mpath = run_root / "manifest.jsonl"
    if args.stage:
        mode = args.mode or "files"
        files = load_targets(mode, args.mode2 or [])
        if not files:
            print("USAGE-ERROR: no target files (pass --triple-violators or --files)")
            return 2
        bad = [f for f in files if not (ROOT / f).is_file()]
        if bad:
            print(f"USAGE-ERROR: target files missing: {bad}")
            return 2
        rows = build_manifest(args.run, files, args.families)
        print(f"STAGED {len(rows)} asks "
              f"({len(files)} files x {len(args.families)} families) -> {mpath}")
    elif mpath.is_file():
        rows = [json.loads(l) for l in mpath.read_text(encoding="utf-8").splitlines()
                if l.strip()]
    else:
        print("USAGE-ERROR: no manifest; run --stage first")
        return 2
    if args.fire:
        fire(args.run, rows, args.concurrency, args.cap)
    if args.rollup:
        out = rollup(args.run, rows)
        real = [c for c in out["clusters"] if c["status"] == "REAL"]
        print(f"ROLLUP {out['landed']}/{out['asks']} landed, "
              f"{len(out['clusters'])} clusters, {len(real)} REAL, "
              f"${out['cost_usd']} metered -> {run_root / 'rollup.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
