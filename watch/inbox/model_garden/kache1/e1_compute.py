"""KACHE-E1 compute-only finish: read the banked position ledger + answers,
compute the RSA geometry agreement and the activation-proximity vs
cross-model-answer-convergence bridge. No model reload (the capture run
banked everything before its layer-lookup crash; bug: min() over the
pct->layer dict returned the pct key, not the layer value).

Swap record from the capture run (its stdout log): gemma4:latest LOADED as
Gemma4ForCausalLM but its GGUF tokenizer carries no chat_template, so the
capture failed at prompt 1 and the spec sec 5 fallback fired: qwen2.5:3b-
instruct. Cross-family pair (stronger claim than same-family, spec sec 5).
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
KACHE = ROOT / "memory" / "runs" / "kache"
PROMPT_IDS = [f"P{i:02d}" for i in range(1, 11)]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_ledger():
    rows = [json.loads(l) for l in open(KACHE / "captures.jsonl",
                                        encoding="utf-8") if l.strip()]
    models = {}
    for r in rows:
        m = models.setdefault(r["model_id"], {"rows": [], "vecs": {},
                                              "pct_layer": {}})
        m["rows"].append(r)
        m["pct_layer"][r["layer_depth_pct"]] = r["layer"]
        v = np.load(ROOT / r["vector_path"])
        m["vecs"][(r["layer"], r["prompt_id"])] = v
    return models


def load_answers():
    ans = {}
    for l in open(KACHE / "answers.jsonl", encoding="utf-8"):
        r = json.loads(l)
        ans.setdefault(r["model_id"], {})[r["prompt_id"]] = r["answer"]
    return ans


def cos(a, b) -> float:
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def trigrams(s: str) -> set:
    s = "".join(c if c.isalnum() or c == " " else " " for c in s.lower()).strip()
    if len(s) < 3:
        return set()
    return {s[i:i + 3] for i in range(len(s) - 2)}


def ans_sim(a: str, b: str) -> float:
    ta, tb = trigrams(a), trigrams(b)
    if not ta or not tb:
        return 1.0 if a.strip() == b.strip() else 0.0
    return len(ta & tb) / math.sqrt(len(ta) * len(tb))


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(xs, ys) -> float:
    return float(np.corrcoef(ranks(xs), ranks(ys))[0, 1])


def main() -> None:
    models = load_ledger()
    ans = load_answers()
    used = sorted(models)
    a_tag, b_tag = used[0], used[1]
    A, B = ans[a_tag], ans[b_tag]
    pairs = [(i, j) for x, i in enumerate(PROMPT_IDS)
             for j in PROMPT_IDS[x + 1:]]
    Y = [round((ans_sim(A[i], B[j]) + ans_sim(A[j], B[i])) / 2, 4)
         for i, j in pairs]
    report = {"ts": now(), "schema": "kache.e1_summary.v1", "models": used,
              "swap_note": ("gemma4:latest loaded (Gemma4ForCausalLM) but its "
                            "GGUF tokenizer has no chat_template; capture "
                            "failed at prompt 1; spec sec 5 fallback fired -> "
                            "qwen2.5:3b-instruct (cross-family pair)"),
              "n_prompts": 10, "n_pairs": len(pairs),
              "answers": {t: {p: ans[t][p][:160] for p in PROMPT_IDS}
                          for t in used},
              "layers": {}, "Y_values": Y}
    for L in sorted(models[a_tag]["pct_layer"].values()):
        pct = round(100 * L / 26) if "gemma2" in a_tag else None
        # recover pct from the ledger rows instead of hardcoding depth
        pct = next(r["layer_depth_pct"] for r in models[a_tag]["rows"]
                   if r["layer"] == L)
        Lb = models[b_tag]["pct_layer"][
            min(models[b_tag]["pct_layer"], key=lambda p: abs(p - pct))]
        X = [round((cos(models[a_tag]["vecs"][(L, i)],
                        models[a_tag]["vecs"][(L, j)])
                    + cos(models[b_tag]["vecs"][(Lb, i)],
                          models[b_tag]["vecs"][(Lb, j)])) / 2, 4)
             for i, j in pairs]
        sa = [models[a_tag]["vecs"][(L, p)] for p in PROMPT_IDS]
        sb = [models[b_tag]["vecs"][(Lb, p)] for p in PROMPT_IDS]
        ma = [cos(sa[i], sa[j]) for i in range(10) for j in range(i + 1, 10)]
        mb = [cos(sb[i], sb[j]) for i in range(10) for j in range(i + 1, 10)]
        report["layers"][f"A_L{L}_B_L{Lb}"] = {
            "rsa_spearman": round(spearman(ma, mb), 4),
            "bridge_spearman": round(spearman(X, Y), 4),
            "X_range": [min(X), max(X)], "Y_range": [min(Y), max(Y)],
        }
    # SALVAGE LEG (metric lesson): the pre-registered pair-Y (cross-model
    # cross-prompt similarity) is structurally ~0 on a divergent-answer
    # battery - different prompts have different answers by design, so the
    # bridge Spearman above is a FAILED-TO-MEASURE, not a finding. The
    # salvage: per-prompt convergence conv_i = sim(A_i, B_i) vs per-prompt
    # activation typicality X_i = mean_j cos(h_i, h_j), both from banked bytes.
    conv = [ans_sim(A[p], B[p]) for p in PROMPT_IDS]
    report["per_prompt"] = {"conv_i": [round(c, 4) for c in conv]}
    for L in sorted(models[a_tag]["pct_layer"].values()):
        pct = next(r["layer_depth_pct"] for r in models[a_tag]["rows"]
                   if r["layer"] == L)
        Lb = models[b_tag]["pct_layer"][
            min(models[b_tag]["pct_layer"], key=lambda p: abs(p - pct))]
        def typ(vecs, LL):
            return [round(sum(cos(vecs[(LL, i)], vecs[(LL, j)])
                             for j in PROMPT_IDS if j != i) / 9, 4)
                    for i in PROMPT_IDS]
        xa = typ(models[a_tag]["vecs"], L)
        xb = typ(models[b_tag]["vecs"], Lb)
        xm = [round((u + v) / 2, 4) for u, v in zip(xa, xb)]
        # numeric-cluster sanity: intra {P02,P03,P04,P10} vs all-cross cosine
        num = {"P02", "P03", "P04", "P10"}
        intra = [cos(models[a_tag]["vecs"][(L, i)], models[a_tag]["vecs"][(L, j)])
                 for i in num for j in num if i < j]
        allc = [cos(models[a_tag]["vecs"][(L, i)], models[a_tag]["vecs"][(L, j)])
                for x, i in enumerate(PROMPT_IDS) for j in PROMPT_IDS[x + 1:]]
        report["per_prompt"][f"A_L{L}_B_L{Lb}"] = {
            "typicality_spearman_A": round(spearman(xa, conv), 4),
            "typicality_spearman_B": round(spearman(xb, conv), 4),
            "typicality_spearman_mean": round(spearman(xm, conv), 4),
            "numeric_cluster_intra_vs_all_A": [
                round(sum(intra) / len(intra), 4), round(sum(allc) / len(allc), 4)],
        }
    (KACHE / "e1_summary.json").write_text(
        json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    slim = {k: v for k, v in report.items()
            if k not in ("answers", "Y_values")}
    print(json.dumps(slim, indent=1))


if __name__ == "__main__":
    main()
