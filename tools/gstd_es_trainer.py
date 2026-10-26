#!/usr/bin/env python3
"""gstd_es_trainer: Evolution Strategies over the gstd mesh (gated skeleton).

The mesh-native trainer, the pennies-leasing shape (run ml-moonshot-20261007,
lane ml6-es-mesh-trainer; spec docs/ref/GSTD_ES_MESH_TRAINER_SPEC.md). Genomes
are prompt-cue vectors (the wired kind) or routing-policy vectors (staged
steering). Fitness is task success minus a cost term (cost staged with the
settlement RFC, fleet spec section 6). ONLY the fitness score enters the
trainer's update: each mesh node evaluates its perturbed cue prompt locally and
the mean update below consumes returned scores alone. No gradient, no weight
delta, no population state ever crosses the wire. That is ES's gift per the
2026-10-07 drop (watch/inbox/LINKS.jsonl seq 1791377243089599): ES finds
parameter neighborhoods 3.9x wider than PPO and won the stability-plasticity
trade-off in 8 of 18 continual settings where gradient RL won ZERO.

Laws carried from tools/gstd_fleet_provider.py. This module holds NO sockets
of its own: every byte on the wire goes through the fleet provider's gated
submit_task / poll_task legs, so the wallet gate is inherited fail-closed and
the SSRF allowlist, the strip-at-load key law, the scrub law, and the
retry-never law all bind here unchanged.

Usage:
  .venv\\Scripts\\python.exe -m tools.gstd_es_trainer --status
  .venv\\Scripts\\python.exe -m tools.gstd_es_trainer --cost
  .venv\\Scripts\\python.exe -m tools.gstd_es_trainer --round --task "..." --answer "..."
  # --round exits 3 while the wallet gate is closed, mirroring the fleet lane
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import math
import random
import sys
import time
from pathlib import Path

from tools import gstd_fleet_provider as gfp

_LOG = logging.getLogger("tools.gstd_es_trainer")

ROOT = Path(__file__).resolve().parent.parent

# The genome: named prompt-cue slots. Weight > 0 includes the fragment in the
# rendered prompt; weight magnitude orders fragments (deterministic render).
GENOME: tuple[str, ...] = (
    "step_by_step",
    "answer_first",
    "check_work",
    "format_strict",
    "terse",
    "show_example",
    "restate_task",
    "no_preamble",
)
CUE_FRAGMENTS: dict[str, str] = {
    "step_by_step": "Think step by step before answering.",
    "answer_first": "State the final answer on the first line.",
    "check_work": "Verify your answer before responding.",
    "format_strict": "Reply with only the number.",
    "terse": "Be maximally terse.",
    "show_example": "Show one worked example.",
    "restate_task": "Restate the task in one line first.",
    "no_preamble": "No preamble.",
}

SIGMA = 0.5          # perturbation scale on the unit cue box
ALPHA = 0.25         # ES learning rate
POP_PER_GEN = 6      # 3 antithetic pairs per generation
TASK_SHAPE = "probe"  # fleet lane shape; es work rides probes
COST_LAMBDA = 0.0    # cost term staged with the settlement RFC (fleet spec s6)

ES_RUNS = ROOT / "memory" / "runs" / "gstd_es_trainer"
STATE_PATH = ES_RUNS / "state.json"
ROUNDS_LEDGER = ES_RUNS / "es_rounds.jsonl"
GATE_EXIT = gfp.GATE_EXIT


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# -- genome rendering -----------------------------------------------------

def render_prompt(task_prompt: str, vector: list[float]) -> str:
    """Deterministic prompt render: fragments of positive weights, heaviest
    first. Same vector, same bytes; the evidence hash downstream depends on
    it."""
    pairs = sorted(zip(GENOME, vector), key=lambda kv: -kv[1])
    frags = [CUE_FRAGMENTS[name] for name, w in pairs if w > 0]
    return (task_prompt.rstrip() + " " + " ".join(frags)).strip()


def route_device(nodes: list[str], vector: list[float]) -> str:
    """Routing-policy genome: argmax over the first len(nodes) weights.
    Ties resolve to sorted-node order (stable argmax). Staged steering: the
    round loop still round-robins until the routing genome is wired at
    wire time (spec section 6)."""
    if not nodes:
        raise ValueError("route_device needs at least one node")
    w = list(vector[: len(nodes)]) + [0.0] * max(0, len(nodes) - len(vector))
    best = 0
    for i in range(1, len(nodes)):
        if w[i] > w[best]:
            best = i
    return nodes[best]


# -- the ES core (scores only) ---------------------------------------------

def sample_perturbations(seed: int, dim: int, pop: int) -> list[list[float]]:
    """Antithetic sampling: pop must be even; pairs are (eps, -eps) so the
    population sums to zero and the paired update halves variance. Local RNG,
    deterministic per seed: a perturbation is re-derivable from its seed, so
    the ledger stores seeds, never eps floats."""
    if pop % 2:
        raise ValueError("pop must be even (antithetic pairs)")
    rng = random.Random(seed)
    out: list[list[float]] = []
    for _ in range(pop // 2):
        eps = [rng.gauss(0.0, 1.0) for _ in range(dim)]
        out.append(eps)
        out.append([-x for x in eps])
    return out


def update_mean(mean: list[float], perturbations: list[list[float]],
                fitnesses: list[float], alpha: float = ALPHA,
                sigma: float = SIGMA) -> tuple[list[float], float]:
    """The no-gradient clause in one function: theta moves by
    (alpha / (n * sigma)) * sum_i centered_f_i * eps_i and NOTHING else. The
    only inputs are the returned scores and the locally re-derived eps; no
    gradient, no model delta, no node state. Returns (new_mean, delta_l2)."""
    n = len(fitnesses)
    if n == 0 or n != len(perturbations):
        return list(mean), 0.0
    center = sum(fitnesses) / n
    centered = [f - center for f in fitnesses]
    new = list(mean)
    for j in range(len(mean)):
        g = sum(centered[i] * perturbations[i][j] for i in range(n))
        new[j] = mean[j] + (alpha / (n * sigma)) * g
    delta = math.sqrt(sum((new[j] - mean[j]) ** 2 for j in range(len(mean))))
    return new, delta


def fitness(completion: str, expected: str, cost_norm: float = COST_LAMBDA) -> float:
    """Fitness = task success minus normalized cost. Success is the same crude
    ground-truth check the self-play orchestrator uses (number match, else
    substring). The cost term stays 0 until the settlement RFC lands: the
    fleet lane computes nothing owed (fleet spec section 6)."""
    c = str(completion).strip()
    hit = False
    try:
        hit = abs(float(c) - float(expected)) < 0.01
    except (ValueError, TypeError):
        hit = str(expected) in c
    return (1.0 if hit else 0.0) - float(cost_norm)


# -- the byte-cost model (what a 3-node ES round costs in bytes) -----------

def cue_chars_expected() -> int:
    """Expected rendered-cue chars at mean 0: half the fragments included
    (integer floor), separator space each."""
    total = sum(len(f) + 1 for f in CUE_FRAGMENTS.values())
    return total // 2


def round_cost_bytes(*, pop: int = POP_PER_GEN, nodes: int = 3,
                     task_chars: int = 120, completion_chars: int = 276,
                     status_polls: int = 3) -> dict:
    """Application-layer JSON byte budget of one ES generation across the
    mesh. Defaults: pop 6 (3 antithetic pairs), 3 nodes, the fleet spec's
    example completion of 276 chars (docs/ref/GSTD_FLEET_LANE_SPEC.md section
    5, chars: 276), 3 status polls per task (the mesh's own node cadence is
    5s; the lane polls patiently). Counts JSON payload bytes only: the mesh
    settles credits per task, not per byte, and TCP/TLS add fixed per-request
    overhead no one bills for. The gradient-free shape is the point: the
    outbound payload is a task prompt with a rendered cue, the inbound payload
    is a completion; there is no third thing."""
    prompt_chars = task_chars + 1 + cue_chars_expected()
    submit_body = json.dumps(
        {"id": "gstd-es-g000-e00", "kind": TASK_SHAPE,
         "prompt": "x" * prompt_chars, "device_hint": "desktop"})
    submit_bytes = len(submit_body.encode("utf-8"))
    poll_body = json.dumps(
        {"task_id": "t" * 24, "status": "complete",
         "result": "x" * completion_chars, "model": "gemma:2b"})
    poll_bytes = len(poll_body.encode("utf-8"))
    status_bytes = status_polls * (24 + 10 + 40)  # url tail + running body + envelope
    per_task = submit_bytes + poll_bytes + status_bytes
    return {
        "pop": pop,
        "nodes": nodes,
        "tasks": pop,
        "submit_bytes_per_task": submit_bytes,
        "poll_bytes_per_task": poll_bytes,
        "status_bytes_per_task": status_bytes,
        "per_task_bytes": per_task,
        "round_total_bytes": per_task * pop,
        "bytes_per_node": (per_task * pop) // max(1, nodes),
        "model": "es-generation across %d nodes, %d tasks (%d antithetic pairs)"
                 % (nodes, pop, pop // 2),
    }


# -- state + ledger ---------------------------------------------------------

def fresh_state() -> dict:
    return {"schema": "es_state.v1", "gen": 0, "seed_base": int(time.time()),
            "mean": [0.0] * len(GENOME), "sigma": SIGMA, "alpha": ALPHA,
            "ts": _now()}


def load_state() -> dict:
    try:
        st = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        # Unreadable or absent state reseeds BY DESIGN; the reason is logged,
        # never swallowed silently (violation ratchet: no except-pass).
        _LOG.info("es trainer state unreadable, reseeding fresh: %s", exc)
        return fresh_state()
    if st.get("schema") == "es_state.v1" and len(st.get("mean", [])) == len(GENOME):
        return st
    return fresh_state()


def save_state(state: dict) -> None:
    ES_RUNS.mkdir(parents=True, exist_ok=True)
    state = dict(state)
    state["ts"] = _now()
    STATE_PATH.write_text(json.dumps(state, indent=1), encoding="utf-8")


def bank_round(row: dict) -> None:
    """Append one es_round_row.v1. Rows carry scores, seeds, and evidence
    hashes; never completions, never eps floats (re-derivable from seeds)."""
    ES_RUNS.mkdir(parents=True, exist_ok=True)
    row = dict(row)
    if "why" in row:
        row["why"] = gfp._scrub(str(row["why"]))
    with ROUNDS_LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# -- the gated round ---------------------------------------------------------

def es_round(task_prompt: str, expected: str, *, pop: int = POP_PER_GEN) -> dict:
    """One ES generation over the mesh. Gate first, always: a closed gate is a
    blocked verdict with zero network attempts (retry never: one submit and
    one poll window per perturbation, failures bank)."""
    ok, why = gfp.wallet_gate("es round")
    if not ok:
        return {"ok": False, "blocked": True, "why": why}
    state = load_state()
    gen = int(state.get("gen", 0))
    seed = int(state.get("seed_base", 0)) + gen
    eps_list = sample_perturbations(seed, len(GENOME), pop)
    devices = sorted(gfp.wallets()) or ["desktop"]
    scores: list[dict] = []
    fired = 0
    for i, eps in enumerate(eps_list):
        vec = [m + float(state["sigma"]) * e for m, e in zip(state["mean"], eps)]
        wid = "es-g%03d-e%02d" % (gen, i)
        prompt = render_prompt(task_prompt, vec)
        dev = devices[i % len(devices)]
        fired += 1
        sub = gfp.submit_task(work_id=wid, prompt=prompt,
                              task_shape=TASK_SHAPE, device=dev)
        if not sub.get("ok"):
            bank_round({"schema": "es_round_row.v1", "class": "eval",
                        "gen": gen, "genome_id": wid, "node": dev,
                        "stage": "submit", "ok": False,
                        "why": sub.get("why", ""), "ts": _now()})
            continue
        done = gfp.poll_task(sub["task_id"], device=dev,
                             task_shape=TASK_SHAPE, work_id=wid)
        if not done.get("ok"):
            bank_round({"schema": "es_round_row.v1", "class": "eval",
                        "gen": gen, "genome_id": wid, "node": dev,
                        "stage": "poll", "task_id": done.get("task_id", ""),
                        "ok": False, "why": done.get("why", ""), "ts": _now()})
            continue
        fit = fitness(done.get("completion", ""), expected)
        mesh_row = gfp.gps_mesh_row(
            node_device=dev, task_shape=TASK_SHAPE,
            evidence_hash=done["evidence_hash"], work_id=wid,
            task_id=done["task_id"], ok=True,
            chars=len(done.get("completion", "")),
            model=done.get("model", ""), detail=done.get("completion", ""))
        gfp.bank_mesh(mesh_row)
        scores.append({"genome_id": wid, "seed": seed, "eps_index": i,
                       "node": dev, "fitness": round(fit, 4),
                       "evidence_hash": done["evidence_hash"]})
    # The update consumes ONLY the returned scores (and the locally
    # re-derived eps of scored evals): the no-gradient clause.
    scored_eps = [eps_list[s["eps_index"]] for s in scores]
    new_mean, delta = update_mean(
        state["mean"], scored_eps, [s["fitness"] for s in scores],
        float(state.get("alpha", ALPHA)), float(state.get("sigma", SIGMA)))
    round_row: dict = {
        "schema": "es_round_row.v1", "class": "generation", "gen": gen,
        "seed": seed, "task_shape": TASK_SHAPE, "n_fired": fired,
        "n_scored": len(scores), "scores": scores,
        "mean_delta_l2": round(delta, 6), "ts": _now()}
    if scores:
        round_row["mean_after"] = [round(x, 6) for x in new_mean]
        state["mean"] = new_mean
    state["gen"] = gen + 1
    save_state(state)
    bank_round(round_row)
    return {"ok": True, "gen": gen, "n_fired": fired,
            "n_scored": len(scores), "mean_delta_l2": round(delta, 6),
            "devices": devices}


# -- CLI ---------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--cost", action="store_true")
    ap.add_argument("--round", action="store_true", dest="do_round")
    ap.add_argument("--task", default="")
    ap.add_argument("--answer", default="")
    a = ap.parse_args(argv)
    if a.status:
        ws = gfp.wallets()
        print("WALLET GATE:", "OPEN" if ws else "BLOCKED",
              "(devices with wallets: " + (", ".join(sorted(ws)) or "none") + ")")
        st = load_state()
        print("trainer state: gen=%s dim=%d sigma=%s alpha=%s"
              % (st.get("gen"), len(st["mean"]), st["sigma"], st["alpha"]))
        print("genome:", ", ".join(GENOME))
        print("state:", STATE_PATH)
        print("rounds ledger:", ROUNDS_LEDGER)
        print("wire: fitness scores only; no gradient, no weight delta travels")
        return 0
    if a.cost:
        print(json.dumps(round_cost_bytes(), indent=1))
        return 0
    if a.do_round:
        if not a.task or not a.answer:
            print("--round needs --task and --answer")
            return 2
        out = es_round(a.task, a.answer)
        print(json.dumps(out, ensure_ascii=False))
        return GATE_EXIT if out.get("blocked") else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
