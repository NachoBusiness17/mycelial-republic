"""The GPS embedding trial: string keys vs kNN over EmbeddingGemma 2.

Operator order (2026-10-06 GPS-embedding lane): hold out 30% of
verdict_log rows; for each held-out ask (task_shape) route two ways -
(A) string-key exact match as the ledger routes today (task_shape_
has_history -> shape_table[0] winner; no history -> the exploration
model, router.py's rule) and (B) kNN over the embedded space (cosine,
k=3, majority vote of the neighbors' shape winners) - and measure
routing accuracy against the full-ledger oracle winner plus ms/ask
local. Filed falsifier: if embedding-NN does not beat string keys on
held-out accuracy OR costs > 5 ms/ask, the substrate dies (bank the
kill with numbers); a win banks the win and the flip-to-default still
needs the operator GO.

Oracle: the production capability table's own winner rule,
shape_table[0] (pass_rate desc, momentum badge, sample size, model_id)
- exactly the ranking tools/gps_mcp/router.py's duel router uses.
Ground truth per held-out ask = that rule computed on the FULL ledger
(the quantity routing is trying to predict); a route is correct iff it
names the same model.

Timing defect fixed at landing (trust bytes, not reports): the first
run's per-ask timings measured cache hits on both arms (route_b reused
a precomputed query vector; route_a read a precomputed winners dict),
reporting 0.1 ms/ask for an embed that costs tens of ms. The landed
instruments embed the query text fresh on every B ask (train-side
neighbor vectors stay precomputed, mirroring the sidecar in
deployment) and re-run shape_table on every A ask. The falsifier's
cost verdict follows the fixed instrument; the buggy 0.1 ms reading is
struck and preserved here as the defect record.

A leave-one-shape-out cold-start arm is included because it is the
regime where string keys cannot help (no exact match exists) and the
vector thesis must pay for itself: train = the other 9 shapes, asks =
the held shape's rows. Model-free arithmetic lives in
gps_embed_stats.py; the pull + sidecar in gps_embed.py.
"""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any, Optional

from .gps_embed import (
    DEFAULT_CONFIG,
    DEFAULT_LEDGER,
    DEFAULT_MODEL_DIR,
    EMBEDDER_ID,
    FP32_ONNX,
    Q4_ONNX,
    RUN_DIR,
    EmbeddingGemma2ONNX,
    sha256_file,
)
from .gps_embed_stats import (
    HOLDOUT_FRACTION,
    KNN_K,
    TRIAL_SEED,
    knn_vote,
    mcnemar_exact_p,
    read_verdict_rows,
    stratified_holdout,
    wilson_ci,
)
from .ledger import CapabilityLedger
from .router import shape_table

MS_PER_ASK_BUDGET = 5.0  # the filed falsifier's cost bar


def build_scratch_ledger(rows: list[dict[str, Any]], db_path: Path) -> CapabilityLedger:
    """A scratch CapabilityLedger fed exactly these rows (rowid order
    preserved so momentum windows read time honestly). Evidence hashes
    are omitted: each row is one distinct observation and the a04
    dedupe gate must not collapse trial rows."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    ledger = CapabilityLedger(db_path)
    for r in rows:
        ledger.record_verdict(r["model_id"], r["task_shape"], int(r["verdict"]))
    return ledger


def exploration_model(config_path: Path | str = DEFAULT_CONFIG) -> str:
    return str(json.loads(Path(config_path).read_text(encoding="utf-8"))["exploration_model"])


def winner_of(ledger: CapabilityLedger, task_shape: str) -> Optional[str]:
    """The ledger's own winner rule (shape_table[0]: pass_rate desc,
    momentum, sample size, model_id) - the exact ranking the duel
    router uses today."""
    table = shape_table(ledger, task_shape)
    return None if not table else str(table[0]["model_id"])


def run_trial(
    ledger_db: Path | str = DEFAULT_LEDGER,
    run_dir: Path | str = RUN_DIR,
    model_dir: Path | str = DEFAULT_MODEL_DIR,
    seed: int = TRIAL_SEED,
    time_q4: bool = True,
) -> dict[str, Any]:
    """30% verdict-row holdout; route A (string key, ledger semantics)
    vs route B (kNN over EmbeddingGemma 2 space); accuracy vs the
    full-ledger oracle winner, Wilson CIs, exact McNemar, warm ms/ask,
    q4 timing arm, and the leave-one-shape-out cold-start arm."""
    ledger_db = Path(ledger_db)
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    # Byte-copy production before opening it through CapabilityLedger
    # (init_schema writes); production bytes are never touched.
    prod_copy = run_dir / "production_copy.db3"
    shutil.copy2(ledger_db, prod_copy)
    prod_ledger = CapabilityLedger(prod_copy)

    rows = read_verdict_rows(ledger_db)
    train_rows, held_rows = stratified_holdout(rows, HOLDOUT_FRACTION, seed)
    train_ledger = build_scratch_ledger(train_rows, run_dir / "train_seed.db3")

    embedder = EmbeddingGemma2ONNX(model_dir, FP32_ONNX)
    all_shapes = sorted({r["task_shape"] for r in rows})
    train_shapes = sorted({r["task_shape"] for r in train_rows})
    # Train-side vectors precomputed once (the sidecar's deployment
    # shape); the per-ask QUERY embed is always fresh (see docstring).
    shape_vecs = {s: embedder.embed([s])[0] for s in all_shapes}

    oracle = {s: winner_of(prod_ledger, s) for s in all_shapes}
    explore = exploration_model()
    train_winners = {s: winner_of(train_ledger, s) for s in train_shapes}

    def route_a(shape: str) -> Optional[str]:
        if train_ledger.task_shape_has_history(shape):
            return winner_of(train_ledger, shape)
        return explore  # no ledger history -> exploration model (router.py rule)

    def route_b(shape: str) -> tuple[Optional[str], list[dict[str, Any]]]:
        query = embedder.embed([shape])[0]  # per-ask query embed
        return knn_vote(query, {s: shape_vecs[s] for s in train_shapes}, train_winners)

    # -- accuracy pass ------------------------------------------------
    a_hits = b_hits = 0
    discordant = [0, 0]  # [A right B wrong, A wrong B right]
    b_misses: list[dict[str, Any]] = []
    for r in held_rows:
        shape = r["task_shape"]
        truth = oracle.get(shape)
        ra = route_a(shape)
        rb, detail = route_b(shape)
        a_ok = ra is not None and ra == truth
        b_ok = rb is not None and rb == truth
        a_hits += int(a_ok)
        b_hits += int(b_ok)
        if a_ok and not b_ok:
            discordant[0] += 1
        if b_ok and not a_ok:
            discordant[1] += 1
        if not b_ok:
            b_misses.append(
                {"held_shape": shape, "oracle": truth, "route_b": rb, "neighbors": detail}
            )
    n_held = len(held_rows)
    a_ci = wilson_ci(a_hits, n_held)
    b_ci = wilson_ci(b_hits, n_held)

    # -- warm timing pass (ms/ask, batch=1: the routing ask is single) --
    def timed(fn) -> tuple[float, float, float]:
        for shape in train_shapes:  # warm every path first
            fn(shape)
        per_call: list[float] = []
        for r in held_rows:
            t0 = time.perf_counter_ns()
            fn(r["task_shape"])
            per_call.append((time.perf_counter_ns() - t0) / 1e6)
        per_call.sort()
        return (
            sum(per_call) / len(per_call),
            per_call[len(per_call) // 2],
            per_call[int(0.95 * (len(per_call) - 1))],
        )

    a_mean, a_p50, a_p95 = timed(route_a)
    b_mean, b_p50, b_p95 = timed(lambda s: route_b(s)[0])

    # Decomposition: the kNN arithmetic alone (query embed + neighbors
    # all precomputed) - the floor cost if queries were cached.
    def knn_only(shape: str) -> Optional[str]:
        m, _ = knn_vote(shape_vecs[shape], {s: shape_vecs[s] for s in train_shapes}, train_winners)
        return m

    knn_mean, knn_p50, knn_p95 = timed(knn_only)

    # -- q4 timing arm (same asks; quantization moves latency, and the
    #    falsifier's cost bar deserves the cheapest official arm too) --
    q4: dict[str, Any] = {"available": False}
    if time_q4 and (Path(model_dir) / Q4_ONNX).exists():
        q4_embedder = EmbeddingGemma2ONNX(model_dir, Q4_ONNX)
        q4_vecs = {s: q4_embedder.embed([s])[0] for s in all_shapes}

        def q4_ask(shape: str) -> Optional[str]:
            query = q4_embedder.embed([shape])[0]  # per-ask query embed
            m, _ = knn_vote(query, {s: q4_vecs[s] for s in train_shapes}, train_winners)
            return m

        q4_mean, q4_p50, q4_p95 = timed(q4_ask)
        q4_hits = sum(
            1 for r in held_rows if q4_ask(r["task_shape"]) == oracle.get(r["task_shape"])
        )
        # Leave-one-out over train shapes: does quantization move the
        # k=3 neighbor choice at all versus fp32?
        agree = sum(
            1
            for s in train_shapes
            if knn_vote(q4_vecs[s], {t: q4_vecs[t] for t in train_shapes if t != s}, train_winners)[0]
            == knn_vote(shape_vecs[s], {t: shape_vecs[t] for t in train_shapes if t != s}, train_winners)[0]
        )
        q4 = {
            "available": True,
            "ms_per_ask_mean": round(q4_mean, 2),
            "ms_per_ask_p50": round(q4_p50, 2),
            "ms_per_ask_p95": round(q4_p95, 2),
            "accuracy": round(q4_hits / n_held, 4),
            "loso_neighbor_agreement_fp32": f"{agree}/{len(train_shapes)}",
        }

    # -- leave-one-shape-out cold-start arm ----------------------------
    loso_per_shape: dict[str, dict[str, Any]] = {}
    loso_b_hits = loso_rows = loso_a_hits = 0
    for held_shape in all_shapes:
        others = [r for r in rows if r["task_shape"] != held_shape]
        fold_db = run_dir / f"loso_{held_shape.replace('/', '_')}.db3"
        fold_ledger = build_scratch_ledger(others, fold_db)
        fold_shapes = sorted({r["task_shape"] for r in others})
        fold_winners = {s: winner_of(fold_ledger, s) for s in fold_shapes}
        # Method A on an unseen shape is always the exploration route
        # (router.py: no ledger history -> exploration model).
        rb, detail = knn_vote(
            shape_vecs[held_shape], {s: shape_vecs[s] for s in fold_shapes}, fold_winners
        )
        truth = oracle[held_shape]
        n_shape_rows = sum(1 for r in rows if r["task_shape"] == held_shape)
        loso_a_hits += n_shape_rows * int(explore == truth)
        loso_b_hits += n_shape_rows * int(rb == truth)
        loso_rows += n_shape_rows
        loso_per_shape[held_shape] = {
            "oracle_winner": truth,
            "route_a": explore,
            "route_b": rb,
            "b_neighbors": detail,
            "rows": n_shape_rows,
        }
        fold_ledger.close()
        fold_db.unlink(missing_ok=True)

    result = {
        "instrument": {
            "ledger": str(ledger_db),
            "ledger_sha256": sha256_file(ledger_db),
            "rows_total": len(rows),
            "split": {
                "seed": seed,
                "holdout_fraction": HOLDOUT_FRACTION,
                "train_rows": len(train_rows),
                "held_rows": n_held,
                "per_shape_held": {
                    s: sum(1 for r in held_rows if r["task_shape"] == s)
                    for s in all_shapes
                },
            },
            "oracle": "production capability shape_table[0] (pass_rate desc, momentum, n, model_id)",
            "embedder": EMBEDDER_ID,
            "knn_k": KNN_K,
            "exploration_model": explore,
            "cpu_ms_budget_per_ask": MS_PER_ASK_BUDGET,
        },
        "method_a_string_key": {
            "accuracy": round(a_hits / n_held, 4),
            "hits": a_hits,
            "wilson95": [round(x, 4) for x in a_ci],
            "ms_per_ask_mean": round(a_mean, 3),
            "ms_per_ask_p50": round(a_p50, 3),
            "ms_per_ask_p95": round(a_p95, 3),
        },
        "method_b_knn_embed": {
            "accuracy": round(b_hits / n_held, 4),
            "hits": b_hits,
            "wilson95": [round(x, 4) for x in b_ci],
            "ms_per_ask_mean": round(b_mean, 2),
            "ms_per_ask_p50": round(b_p50, 2),
            "ms_per_ask_p95": round(b_p95, 2),
            "knn_only_ms_mean": round(knn_mean, 3),
            "knn_only_ms_p50": round(knn_p50, 3),
            "knn_only_ms_p95": round(knn_p95, 3),
            "misses": b_misses,
        },
        "q4_arm": q4,
        "paired_test": {
            "a_right_b_wrong": discordant[0],
            "b_right_a_wrong": discordant[1],
            "mcnemar_exact_p": round(mcnemar_exact_p(*discordant), 6),
        },
        "loso_cold_start": {
            "note": "train = other 9 shapes, asks = held shape rows; method A has no string key to match (exploration route)",
            "a_accuracy_rowweighted": round(loso_a_hits / loso_rows, 4),
            "b_accuracy_rowweighted": round(loso_b_hits / loso_rows, 4),
            "per_shape": loso_per_shape,
        },
        "train_winners": train_winners,
        "oracle_winners": oracle,
    }

    # -- falsifier verdict --------------------------------------------
    beats = b_hits > a_hits
    ties = b_hits == a_hits and result["paired_test"]["mcnemar_exact_p"] > 0.05
    under_budget = b_mean <= MS_PER_ASK_BUDGET
    q4_under = bool(q4.get("available")) and q4["ms_per_ask_mean"] <= MS_PER_ASK_BUDGET
    if beats and under_budget:
        verdict = "WIN: embedding-NN beats string keys within the 5 ms/ask budget; flip-to-default needs the operator GO"
    elif beats and q4_under:
        verdict = (
            "WIN with caveat: fp32 exceeds 5 ms/ask but the q4 arm stays within"
            " budget with equal-or-better accuracy; operator picks the arm on GO"
        )
    elif ties and (under_budget or q4_under):
        verdict = (
            "NO DIFFERENCE: accuracies tie within noise and cost is within"
            " budget; no flip justified, no kill on accuracy either"
        )
    else:
        reasons = []
        if not beats:
            reasons.append(
                "held-out accuracy does not beat string keys"
                f" (A {a_hits}/{n_held} vs B {b_hits}/{n_held},"
                f" McNemar exact p={result['paired_test']['mcnemar_exact_p']})"
            )
        if not under_budget and not q4_under:
            reasons.append(
                f"cost exceeds {MS_PER_ASK_BUDGET} ms/ask"
                f" (fp32 {b_mean:.1f} ms mean; q4 {q4.get('ms_per_ask_mean')} ms)"
            )
        verdict = "KILL: " + "; ".join(reasons)
    result["verdict"] = verdict

    out_path = run_dir / "trial_results.json"
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    prod_ledger.close()
    train_ledger.close()
    result["results_path"] = str(out_path)
    return result


if __name__ == "__main__":  # pragma: no cover - CLI shell entry
    import sys

    result = run_trial()
    slim = {k: v for k, v in result.items() if k != "loso_cold_start"}
    print(json.dumps(slim, indent=2, sort_keys=True))
    print("verdict:", result["verdict"])
    sys.exit(0)
