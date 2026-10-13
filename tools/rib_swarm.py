"""rib_swarm - law-row intercommunication + genetic lensing (GENOME-1, 2026-10-01).

Spec owner: docs/ref/RIB_SWARM_SPEC.md (rib_swarm.law_row.v1 + rib_swarm.genome.v1).
(1) RIB COMMUNICATION: units exchange findings as LAW ROWS (the ractor50 shape,
memory/runs/salon1/); outputs land in a per-run rib ledger; round-2 consumes
siblings' LAW ROWS only; convergence ranks cross-unit law agreement. (2) GENETIC
LENSING: contract genomes evolved by select/crossover/mutate; fitness = REAL
clusters per dollar (code_swarm); cheap fires under a hard cap. Prototype only.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools import code_swarm as cs  # noqa: E402  the fitness instrument, reused
from tools import model_garden as mg  # noqa: E402  the gated fire rail

GARDEN = ROOT / "watch" / "inbox" / "model_garden"
EM_DASH = "\u2014"
LAW_RE = re.compile(r"^L(\d+):\s*(.*)$")
FIELD_RE = re.compile(r"^(CLAIM|STEAL|FALSIFIER|SOURCE|LEVERAGE):\s*(.*)$")
LEV_RANK = {"high": 0, "medium": 1, "low": 2}
LENS_POOL = ("cost-leak", "security-boundary", "correctness-race", "dead-code",
             "wiring-organs", "error-swallow", "shape-law")
LENS_TEXT = {"cost-leak": "unmetered spend, unenforced cost caps, discarded token counts", "security-boundary": "endpoint fences, DNS rebinding, SSRF, injection paths",
             "correctness-race": "nondeterminism, salted hashes, TOCTOU, type confusion", "dead-code": "unreachable branches, unused returns, vestigial parameters",
             "wiring-organs": "budget import, browser UA, atomic tmp+replace writes", "error-swallow": "silent except, discarded failures, lost error context",
             "shape-law": "contract drift, unparseable output shapes, format discipline"}
MOCK_COST = {"deepseek": 0.0012, "glm-flash": 0.0002, "kimi": 0.0}
MOCK_LANDSCAPE = {"cost-leak": 2, "security-boundary": 2, "correctness-race": 1,
                  "dead-code": 1, "wiring-organs": 0, "error-swallow": 0, "shape-law": 0}
LAW_CLAIMS = {"cost-leak": "spend accumulates without cap enforcement",  # mock stems
              "security-boundary": "host validation allows private network targets",
              "correctness-race": "hash seeding breaks reproducible key selection",
              "dead-code": "unused branch remains after refactor",
              "wiring-organs": "shared jsonl surface lacks atomic replace",
              "error-swallow": "silent except discards the failure",
              "shape-law": "output contract grammar drifted from the parser"}
ROUND1 = ("You are one blind unit of a law-mining swarm over the Mag estate. Review the SOURCE file and mint findings as LAW ROWS.\n"
          "Reply with EXACTLY 3 to 5 rows in this grammar, nothing else:\n"
          "L1: <short title, under 12 words>\nCLAIM: <the law, one to three sentences>\nSTEAL: <the one-sitting action another seat can take>\n"
          'FALSIFIER: <the observation that would kill the claim>\nSOURCE: <path plus verbatim short quote in "double quotes">\nLEVERAGE: high | medium | low\n\n'
          "LAWS:\n- Ground every claim in the SOURCE bytes; drop what you cannot ground, never guess.\n- No em-dash characters anywhere.\n- Start directly with L1, no preamble.\n\n"
          "<SOURCE path={path} sha256={sha} lines={lines}>\n{body}</SOURCE>")
ROUND2 = ("ROUND 2: INTERCOMMUNICATION. You are the same swarm unit. Below are (a) YOUR round-1 law rows, then (b) your SIBLINGS' round-1 law rows "
          "rendered in the same grammar. The sibling block is the ONLY thing you know about them: no prose, no context beyond these rows.\n"
          "Reply with 3 to 5 NEW law rows in the same grammar: refinements, contradictions, or connections that need both views; cite siblings in CLAIM or SOURCE like (U2 L3).\n\n"
          "== YOUR ROUND-1 LAWS ==\n{own}\n\n== SIBLING ROUND-1 LAWS ==\n{sibs}")
GEN_CONTRACT = ("You are reviewing one live file of the Mag estate. Prioritize this lens above all: {lens} ({lens_text}).\n\n"
                "Reply with EXACTLY this shape, {rows} DEFECT lines max, nothing else (omit any line you cannot ground):\n"
                "DEFECT 1: <one-line defect claim, worst first> | EVIDENCE: <path>:<line or range> | FIX: <one-line fix>\n"
                "DEAD-CODE: <one dead-code candidate> | EVIDENCE: <path>:<line>\n"
                "ONE-SITTING FIX: <highest-value one-sitting fix> | EVIDENCE: <path>:<line>\n\n"
                "LAWS:\n- Every EVIDENCE cite uses the exact path in the SOURCE header and real line numbers.\n"
                "- No em-dash characters anywhere. No praise, no speculation as fact.\n\n"
                "<SOURCE path={path} sha256={sha} lines={lines}>\n{body}</SOURCE>")


def parse_law_rows(text: str) -> list[dict]:
    """Lenient parse, strict grade: unknown lines are shape violations, never fatal."""
    rows: list[dict] = []
    cur: dict | None = None
    for line in text.splitlines():
        m = LAW_RE.match(line.strip())
        if m:
            cur = {"law_id": f"L{m.group(1)}", "title": m.group(2).strip(), "CLAIM": "", "STEAL": "", "FALSIFIER": "",
                   "SOURCE": "", "LEVERAGE": "", "raw": [line.strip()], "shape_violations": 0}
            rows.append(cur)
        elif (f := FIELD_RE.match(line.strip())) and cur is not None:
            cur[f.group(1)] = f.group(2).strip()
            cur["raw"].append(line.strip())
        elif line.strip() and cur is not None:
            cur["shape_violations"] += 1  # prose inside a row: tolerated, graded
    for r in rows:
        src = r["SOURCE"].split('"')[0]
        c = {"claim": bool(r["CLAIM"]), "falsifier": bool(r["FALSIFIER"]),
             "leverage": r["LEVERAGE"] in LEV_RANK, "source": "/" in src or "." in src,
             "no_em_dash": EM_DASH not in "\n".join(r["raw"]),
             "title_short": len(r["title"].split()) <= 12}
        r["checks"], r["passes"] = c, c["claim"] and c["falsifier"] and c["leverage"] and c["no_em_dash"]
    return rows


def render_law_rows(rows: list[dict]) -> str:
    """Round-trip law; accepts parsed (upper) and banked ledger (lower) keys."""
    get = lambda r, f: r.get(f, r.get(f.lower(), ""))  # noqa: E731
    return "\n".join(line for r in rows for line in [f'{r["law_id"]}: {r["title"]}']
                     + [f"{f}: {get(r, f)}" for f in ("CLAIM", "STEAL", "FALSIFIER", "SOURCE", "LEVERAGE") if get(r, f)])


def _lsig(row: dict) -> set[str]:
    return {w for w in re.findall(r"[a-z_]+", f'{row["title"]} {row["claim"]}'.lower())
            if len(w) > 3 and w not in cs.STOP}


def converge_laws(rows: list[dict]) -> list[dict]:
    """Cross-instance (unit, family) law agreement (spec section 3)."""
    inst = lambda r: (r.get("unit"), r.get("family"))  # noqa: E731
    parent = list(range(len(rows)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    sigs = [_lsig(r) for r in rows]
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            shared = len(sigs[i] & sigs[j])
            # containment guard (live riblive1: all 90 rows chained into one
            # cluster without it): shared tokens must cover half the smaller sig
            if (inst(rows[i]) != inst(rows[j]) and shared >= 2
                    and shared * 2 >= min(len(sigs[i]), len(sigs[j]))):
                parent[find(j)] = find(i)
    groups: dict[int, list[int]] = {}
    for i in range(len(rows)): groups.setdefault(find(i), []).append(i)
    out = []
    for members in groups.values():
        ms = [rows[i] for i in members]
        units = sorted({m.get("unit", "?") for m in ms})
        fams = sorted({str(m.get("family", "?")) for m in ms})
        lev = min(LEV_RANK.get(m.get("leverage", "low"), 2) for m in ms)
        n_inst = len({inst(m) for m in ms})
        out.append({"units": units, "n_units": len(units), "families": fams, "n_instances": n_inst,
                    "leverage": {v: k for k, v in LEV_RANK.items()}[lev],
                    "status": "CONVERGED" if n_inst >= 2 else "SINGLE", "laws": [{"unit": m.get("unit"),
                    "law_id": m["law_id"], "title": m["title"], "claim": m["claim"]} for m in ms]})
    return sorted(out, key=lambda c: (-len(c["families"]), -c["n_units"], LEV_RANK[c["leverage"]],
                                      -len(c["laws"]), c["laws"][0]["law_id"]))


def bank_ledger(run_root: Path, metas: list[dict]) -> list[dict]:
    """Append parsed law rows to rib_ledger.jsonl (atomic full rewrite)."""
    path = run_root / "rib_ledger.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)  # standalone ledger writes are legal
    existing = ([json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.is_file() else [])
    for m in metas:
        [m.pop(k, None) for k in ("raw", "checks", "shape_violations")]
        existing.append(m)
    cs._atomic_write(path, "".join(json.dumps(m, ensure_ascii=False) + "\n" for m in existing))
    return existing


def stage_ask(run: str, ask_id: str, fam: str, contract: str) -> dict:
    cfg = cs.FAMILIES[fam]
    d = GARDEN / run / "asks" / ask_id
    d.mkdir(parents=True, exist_ok=True)
    cs._atomic_write(d / "ask.json", json.dumps({"id": ask_id, "model": cfg["model"], "base_env": cfg["base_env"],
        "base_url": cfg["base_url"], "contract": contract, "evidence": [], "self_contained": True}, ensure_ascii=False))
    return {"ask_id": ask_id, "family": fam, "ask_dir": str(d.relative_to(ROOT))}


def _reply_text(ask_id: str, mock: bool, run: str) -> str | None:
    p = (GARDEN / run / "mockraw" / f"{ask_id}.md" if mock else GARDEN / f"{ask_id}.md")
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None


def mock_reply(kind: str, lens: str, target: str, n_lines: int, rng: random.Random) -> str:
    """Deterministic offline replier: lens-shaped, parse-grade honest (spec 4.6)."""
    y, stem, noise = MOCK_LANDSCAPE.get(lens, 0), LAW_CLAIMS.get(lens, "no grounded finding"), f"{rng.randrange(1 << 30):x}"
    if kind == "law":
        rows = [f"L{i + 1}: {lens} finding {i + 1}\nCLAIM: {stem} ({noise})\nSTEAL: one-sitting fix a seat can take tomorrow\n"
                f"FALSIFIER: a {lens} probe that returns clean\nSOURCE: {target} \"verbatim quote {noise}\"\nLEVERAGE: high"
                for i in range(3 if y else 2)]
        if not y:  # zero-yield lenses mint non-convergent noise claims
            rows = [r.replace(stem, f"unrelated observation {noise}") for r in rows]
        return "\n\n".join(rows)
    defs = [f"DEFECT {i + 1}: {stem} ({noise}{i}) | EVIDENCE: {target}:{min(n_lines, 3 + i * 20)} | FIX: enforce the missing rail"
            for i in range(y)] or \
           [f"DEFECT 1: {noise} report | EVIDENCE: {target}:1 | FIX: none grounded"]
    return "\n".join(defs + [f"DEAD-CODE: vestigial {noise} | EVIDENCE: {target}:2",
                             f"ONE-SITTING FIX: candidate {noise} | EVIDENCE: {target}:1"])


def fire(run: str, staged: list[dict], mock: bool, concurrency: int, cap: float, seed: int) -> list[dict]:
    """Fire staged asks. Real: mg.run_ask under the cap. Mock: write raw only."""
    if mock:
        rng = random.Random(seed)
        for s in staged:
            body = mock_reply(s["kind"], s.get("lens", ""), s["target"], s["n_lines"], rng)
            (GARDEN / run / "mockraw").mkdir(parents=True, exist_ok=True)
            (GARDEN / run / "mockraw" / f'{s["ask_id"]}.md').write_text(f'# {s["ask_id"]} (MOCK, turn 1, channel: content)\n\n{body}\n', encoding="utf-8")
        return [{"id": s["ask_id"], "ok": True, "mock": True, "cost_usd": MOCK_COST[s["family"]]} for s in staged]
    lock, orig_bank = threading.Lock(), mg._bank

    def _locked(row: dict) -> None:
        with lock:
            orig_bank(row)

    mg._bank = _locked

    def one(s: dict) -> dict:
        if cs._run_spend(run) >= cap:
            return {"id": s["ask_id"], "ok": True, "skipped": "budget cap reached before dispatch"}
        try:
            return mg.run_ask(Path(s["ask_dir"]))
        except Exception as exc:  # noqa: BLE001 - named per ask, never silent
            return {"id": s["ask_id"], "ok": False, "error": repr(exc)[:300]}

    results: list[dict] = []
    try:
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            for f in as_completed({ex.submit(one, s): s for s in staged}):
                res = f.result()
                results.append(res)
                print(f"{'OK ' if res.get('ok') else 'FAIL'} {res['id']} [{res.get('cost_usd', 0):.4f} usd]", flush=True)
    finally:
        mg._bank = orig_bank
    return results


def parse_landed(ask_id: str, mock: bool, run: str, kind: str, target: str, n_lines: int) -> dict | None:
    """Read one landed reply, parse per kind (law rows or code_swarm defects)."""
    raw = _reply_text(ask_id, mock, run)
    if raw is None: return None
    _, _, body = raw.partition("\n\n")
    digest = sha256(raw.encode("utf-8", "replace")).hexdigest()[:16]
    parsed = parse_law_rows(body) if kind == "law" else cs.parse_reply(body, target, n_lines)
    return {("rows" if kind == "law" else "graded"): parsed, "reply_sha256": digest}


def rib_round(run: str, targets: list[str], families: list[str], mock: bool,
              concurrency: int, cap: float, seed: int) -> dict:
    units = [f"U{i + 1}" for i in range(len(targets))]
    staged = []
    for target, unit in zip(targets, units):
        text = (ROOT / target).read_text(encoding="utf-8", errors="replace")
        contract = ROUND1.format(path=target, lines=len(text.splitlines()),
                                 sha=sha256(text.encode("utf-8", "replace")).hexdigest()[:16],
                                 body=text[:cs.CAP_CHARS])
        staged += [{"unit": unit, "target": target, "kind": "law", "n_lines": 0, "lens": "cost-leak",  # mock shaping only
                    **stage_ask(run, f"{run}-{unit}-r1-{fam}", fam, contract)} for fam in families]
    fire(run, staged, mock, concurrency, cap, seed)
    ledger = _mint_ledger(run, staged, mock, 1, prior=None)
    # round 2: law rows only, built from the ledger (raw prose cannot leak)
    staged2 = []
    for unit, target in zip(units, targets):
        own = [r for r in ledger if r["unit"] == unit and r["round"] == 1]
        sibs = [r for r in ledger if r["unit"] != unit and r["round"] == 1]
        contract = ROUND2.format(own=render_law_rows(own), sibs=render_law_rows(sibs))
        n = len((ROOT / target).read_text(encoding="utf-8", errors="replace").splitlines())
        staged2 += [{"unit": unit, "target": target, "kind": "law", "n_lines": n, "lens": "cost-leak",  # mock shaping only
                     **stage_ask(run, f"{run}-{unit}-r2-{fam}", fam, contract)} for fam in families]
    fire(run, staged2, mock, concurrency, cap, seed)
    ledger = _mint_ledger(run, staged2, mock, 2, prior=ledger)
    # convergence over ROUND-1 rows only: r2 cites siblings by contract
    r1 = [r for r in ledger if r["round"] == 1]
    conv = [c for c in converge_laws(r1) if c["status"] == "CONVERGED"]
    out = {"run": run, "mode": "rib-round", "mock": mock, "ledger_rows": len(ledger), "converged_laws": len(conv), "top": conv[:5]}
    cs._atomic_write(GARDEN / run / "rounds.json", json.dumps(out, ensure_ascii=False, indent=1))
    return out


def _mint_ledger(run: str, staged: list[dict], mock: bool, rnd: int, prior: list[dict] | None) -> list[dict]:
    metas = prior or []
    for s in staged:
        parsed = parse_landed(s["ask_id"], mock, run, "law", s["target"], 0)
        if not parsed: continue
        metas += [{"schema": "rib_swarm.law_row.v1", "run": run, "round": rnd, "unit": s["unit"], "family": s["family"],
                   "ask_id": s["ask_id"], "mock": mock, "law_id": r["law_id"], "title": r["title"], "claim": r["CLAIM"],
                   "steal": r["STEAL"], "falsifier": r["FALSIFIER"], "source": r["SOURCE"], "leverage": r["LEVERAGE"],
                   "passes": r["passes"], "reply_sha256": parsed["reply_sha256"]} for r in parsed["rows"]]
    return bank_ledger(GARDEN / run, metas)


def render_genome_contract(g: dict, text: str) -> str:
    kw = dict(lens=g["lens"], lens_text=LENS_TEXT[g["lens"]], rows=g["max_defects"], path=g["target"], sha=sha256(text.encode("utf-8", "replace")).hexdigest()[:16], lines=len(text.splitlines()))
    assert EM_DASH not in GEN_CONTRACT.format(body="", **kw), "authored contract text carries an em-dash"
    return GEN_CONTRACT.format(body=text[:cs.CAP_CHARS], **kw)


def seed_population(targets: list[str], families: list[str], anchor: str, pop: int) -> list[dict]:
    probes = [f for f in families if f != anchor]
    return [{"id": f"g0-{i}", "gen": 0, "origin": "seed", "parents": [], "lens": LENS_POOL[i % len(LENS_POOL)],
             "target": targets[i % len(targets)], "max_defects": 2 + (i % 4), "anchor_family": anchor, "probe_family": probes[i % len(probes)]} for i in range(pop)]




def crossover(a: dict, b: dict, rng: random.Random, n: int) -> dict:
    pick = lambda k: a[k] if rng.random() < 0.5 else b[k]  # noqa: E731
    return {"id": f"g{max(a['gen'], b['gen']) + 1}-{n}", "gen": max(a["gen"], b["gen"]) + 1, "origin": "crossover",
            "parents": [a["id"], b["id"]], "lens": pick("lens"), "target": pick("target"), "max_defects": pick("max_defects"),
            "anchor_family": a["anchor_family"], "probe_family": pick("probe_family"), "fitness": None}


def mutate(g: dict, rng: random.Random, targets: list[str], families: list[str]) -> dict:
    child = {**g, "parents": [g["id"]], "origin": g["origin"] + "+mutate"}
    clause = rng.choice(["lens", "max_defects", "probe_family", "target"] if len(targets) > 1 else ["lens", "max_defects", "probe_family"])
    if clause == "lens":
        child["lens"] = rng.choice([x for x in LENS_POOL if x != g["lens"]])
    elif clause == "max_defects":
        child["max_defects"] = min(5, max(2, g["max_defects"] + rng.choice((-1, 1))))
    elif clause == "probe_family":
        pool = [f for f in families if f not in (g["probe_family"], g["anchor_family"])]
        if pool: child["probe_family"] = rng.choice(pool)
    else:
        child["target"] = rng.choice([t for t in targets if t != g["target"]])
    child["id"], child["gen"] = f"g{g['gen'] + 1}-{rng.randrange(1 << 30) % 10000}", g["gen"] + 1
    return child


def measure(run: str, pop: list[dict], mock: bool, concurrency: int, cap: float, seed: int) -> list[dict]:
    staged = []
    for g in pop:
        text = (ROOT / g["target"]).read_text(encoding="utf-8", errors="replace")
        contract = render_genome_contract(g, text)
        staged += [{"genome": g["id"], "target": g["target"], "kind": "defect", "lens": g["lens"],
                    "n_lines": len(text.splitlines()), **stage_ask(run, f"{run}-{g['id']}-{fam}", fam, contract)}
                   for fam in (g["anchor_family"], g["probe_family"])]
    fire(run, staged, mock, concurrency, cap, seed)
    graded_by: dict[str, list[dict]] = {}
    for s in staged:
        parsed = parse_landed(s["ask_id"], mock, run, "defect", s["target"], s["n_lines"])
        if parsed: graded_by.setdefault(s["genome"], []).append({"file": s["target"], "family": s["family"], **parsed["graded"]})
    for g in pop:
        pair = graded_by.get(g["id"], [])
        clusters = cs.converge(pair)
        real = sum(c["status"] == "REAL" for c in clusters)
        coloc = sum(c["status"] == "CO-LOCATION" for c in clusters)
        parse_rate = (sum(x["checks"]["shape"] for x in pair) / len(pair)) if pair else 0.0
        cost = (sum(MOCK_COST[x["family"]] for x in staged if x["genome"] == g["id"])
                if mock else cs._run_spend(f"{run}-{g['id']}"))  # spec 4.3: genome's asks only
        g["fitness"] = round((real + 0.25 * coloc + 0.05 * parse_rate) / max(cost, 0.01), 4)
        g["measured"] = {"real": real, "colocation": coloc, "parse_rate": round(parse_rate, 2), "cost_usd": round(cost, 4)}
    return pop


def genetic(run: str, targets: list[str], families: list[str], anchor: str, pop_size: int,
            gens: int, cap: float, seed: int, mock: bool, concurrency: int, stagnation: int) -> dict:
    rng, pop = random.Random(seed), seed_population(targets, families, anchor, pop_size)
    gdir = GARDEN / run / "genetic"
    gdir.mkdir(parents=True, exist_ok=True)
    best_ever, exit_reason, hist = -1.0, "GENERATIONS", []
    for gen in range(gens):
        pop = measure(run, pop, mock, concurrency, cap, seed)
        best = max(g["fitness"] for g in pop)
        hist.append({"gen": gen, "best": best, "mean": round(sum(g["fitness"] for g in pop) / len(pop), 4)})
        cs._atomic_write(gdir / f"genomes_gen{gen}.json", json.dumps(pop, ensure_ascii=False, indent=1))
        with (gdir / "generations.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(hist[-1]) + "\n")
        if best > best_ever:
            best_ever = best
        elif gen >= stagnation:
            exit_reason = "STAGNANT"; break
        if not mock and cs._run_spend(run) >= cap:
            exit_reason = "BUDGET"; break
        elites = sorted(pop, key=lambda g: (-g["fitness"], g["id"]))[:pop_size // 2]
        children, n = [], 0
        while len(elites) + len(children) < pop_size:
            child = crossover(elites[n % len(elites)], elites[(n + 1) % len(elites)], rng, n)
            children.append(mutate(child, rng, targets, families) if rng.random() < 0.5 else child)
            n += 1
        pop = elites + children
    out = {"run": run, "mode": "genetic", "mock": mock, "seed": seed, "exit": exit_reason,
           "generations": hist, "best_ever": best_ever, "cap_usd": cap}
    cs._atomic_write(gdir / "run_receipt.json", json.dumps(out, ensure_ascii=False, indent=1))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="rib_swarm")
    for flag, kw in [("--run", {"required": True}), ("--rib-round", {"action": "store_true"}), ("--genetic", {"action": "store_true"}), ("--mock", {"action": "store_true"}),
                     ("--targets", {"nargs": "*", "default": ["tools/census_drift_patrol.py",
                        "tools/corpus_fts_rebuild.py", "mag/preload_selector.py"]}),
                     ("--families", {"nargs": "*", "default": ["deepseek", "glm-flash", "kimi"]}),
                     ("--anchor", {"default": "deepseek"}), ("--pop", {"type": int, "default": 8}),
                     ("--gens", {"type": int, "default": 3}), ("--stagnation", {"type": int, "default": 1}),
                     ("--seed", {"type": int, "default": 7}), ("--concurrency", {"type": int, "default": 4}),
                     ("--cap", {"type": float, "default": 0.5})]:
        ap.add_argument(flag, **kw)
    args = ap.parse_args(argv)
    bad = ([f for f in args.families + [args.anchor] if f not in cs.FAMILIES] + [t for t in args.targets if not (ROOT / t).is_file()])
    if not (args.rib_round or args.genetic) or not args.targets or bad:
        print(f"USAGE-ERROR: pass --rib-round and/or --genetic; bad={bad}")
        return 2
    if args.rib_round:
        out = rib_round(args.run, args.targets, args.families, args.mock, args.concurrency, args.cap, args.seed)
        print(f"RIB-ROUND {out['ledger_rows']} rows, {out['converged_laws']} converged -> {GARDEN / args.run / 'rounds.json'}")
    if args.genetic:
        out = genetic(args.run, args.targets, args.families, args.anchor, args.pop, args.gens,
                      args.cap, args.seed, args.mock, args.concurrency, args.stagnation)
        print(f"GENETIC exit={out['exit']} best_ever={out['best_ever']} -> {GARDEN / args.run / 'genetic' / 'run_receipt.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
