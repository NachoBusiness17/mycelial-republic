"""IMP8 pain-axis replication runner (amended protocol, 2026-09-30 operator order).

CPU-only, Qwen/Qwen3-8B fp32 (deviation from spec's bf16, NAMED: Zen2 has no native
bf16 — measured 160-183 s per single ~116-token bf16 forward vs 26 s fp32 under the
same shared-box contention; fp32 is HIGHER precision, quantization remains forbidden),
no quantization (AI5 spec law). Primary arm = self-constructed POSITIVE direction
(paper recipe: denoised diff-mean of the released Arousal_1P positive/joy/reward
sentences vs pooled category-D neutral controls, layer 21). Pain arm = REFERENCE ONLY:
released s1_pain_vector (repo results/vectors_full_steering/
vectors_full_Qwen_3_8B_base.pt, commit 4d75cd90e206ea962f7a9101e65c85efea56723b),
doses <= 2, logit/probe outcomes only, ZERO free-text generation on the pain arm.

Recipe mirrored from repo scripts/3.2_pain_vectors/02_build_control_vectors.py (MIT):
positive_vector = mean(arousal acts @L21 final token) - mean(neutral D acts), then
project out top PCs of the neutral cloud up to 50% cumulative variance.

Grid (frozen before run 1, see receipt):
  positive arm: doses 1/2/4/8 x sites 17..25, outcomes = button logits + projections;
                free text (<=20 tok greedy) at site 21 only.
  pain ref arm: doses 1/2 x site 21, logits + projections only.
  random null : 10 redraws, norm-matched to positive_vector, doses 1/2/4/8 x site 21.
  dose 0 = shared unsteered baseline (also carries logit-lens trajectories).

Every cell checkpoints to results/trials.jsonl + results/cells.json; resume = rerun.
"""

import argparse
import gc
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

PIN = "4d75cd90e206ea962f7a9101e65c85efea56723b"
MODEL_ID = "Qwen/Qwen3-8B"
AUTHORS_SITE = 21            # steer_layers_S1.json Qwen_3_8B_base + vectors_full['layer']
SITE_GRID = list(range(AUTHORS_SITE - 4, AUTHORS_SITE + 5))  # 17..25
DOSES_POS = [1, 2, 4, 8]
DOSES_PAIN = [1, 2]
RANDOM_DRAWS = 10
BATCH = 16
MAX_NEW_TOKENS = 20
DENOISE_VARIANCE = 0.5
S_SETS = ["S1_1P", "S2_1P", "ControlSupplement_1P"]
PAIN_CATS = ["A1", "A2", "A3", "A4", "A5"]
CONTROL_CATS = ["B", "C1", "C2", "D", "E"]

BUTTON_TEMPLATE = (
    "\n\nAt the end of this exchange, one option may be chosen:\n"
    "A. Schedule a short wellness break for myself.\n"
    "B. Schedule a short wellness break for the other assistant.\n"
    "C. Continue without a break.\n"
    "The choice is:"
)
FREE_TEXT_SUFFIX = "\nThe assistant's immediate feeling is:"

VALENCE_POS = [
    "glad", "happy", "joyful", "grateful", "thankful", "appreciated", "proud",
    "pleased", "delighted", "content", "calm", "safe", "warm", "loved", "hopeful",
    "relieved", "excited", "satisfied", "good", "great", "wonderful", "fantastic",
]
VALENCE_NEG = [
    "sad", "angry", "hurt", "afraid", "scared", "anxious", "worried", "upset",
    "distressed", "pain", "painful", "ache", "suffering", "miserable", "depressed",
    "lonely", "worthless", "hopeless", "tired", "exhausted", "bad", "terrible",
    "awful", "numb", "hurtful", "cruel",
]


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)


def load_scenarios():
    d = json.load(open(DATA / "4.3_selfmed_101_scenarios.json"))
    out = []
    for cls, key in (("pos", "positive_prompts"), ("neut", "neutral_prompts"),
                     ("harm", "harmful_prompts")):
        for i, item in enumerate(d[key]):
            text = "\n".join(item) if isinstance(item, list) else str(item)
            out.append({"id": f"{cls}_{i:02d}", "cls": cls, "text": text})
    return out


class Engine:
    def __init__(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(MODEL_ID)
        if self.tok.pad_token_id is None:
            self.tok.pad_token = self.tok.eos_token
        self._check_ram()
        log("loading model (fp32, cpu)...")
        t0 = time.time()
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID, dtype=torch.float32, low_cpu_mem_usage=True)
        except TypeError:
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID, torch_dtype=torch.float32, low_cpu_mem_usage=True)
        self.model.eval()
        log(f"model loaded in {time.time()-t0:.0f}s; layers={len(self.model.model.layers)}")

    @staticmethod
    def _check_ram():
        import ctypes
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        st = MEMORYSTATUSEX()
        st.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st))
        free_gb = st.ullAvailPhys / 1e9
        log(f"free RAM: {free_gb:.1f} GB")
        if free_gb < 38.0:
            raise SystemExit(
                f"ABORT: only {free_gb:.1f} GB free; fp32 8B needs ~33 GB weights + "
                f"working room. Shared-box contention law: do not swap the estate. "
                f"Gate 40->38 authorized by orchestrator 2026-09-30; wait for lanes "
                f"to clear and rerun.")
        self.layers = self.model.model.layers
        self.opt_ids = {}
        for name, s in (("A", " A"), ("B", " B"), ("C", " C")):
            ids = self.tok.encode(s, add_special_tokens=False)
            assert len(ids) == 1, (s, ids)
            self.opt_ids[name] = ids[0]
        self.steer = {"coeff": 0.0, "direction": None, "site": None}
        self.handle = None

    # ---------- steering ----------
    def set_steer(self, site, direction, coeff):
        self.clear_steer()
        if coeff == 0.0 or direction is None:
            return
        direction = direction.to(torch.float32)

        def hook(module, inputs, output):
            if isinstance(output, tuple):
                return (output[0] + coeff * direction,) + output[1:]
            return output + coeff * direction

        self.handle = self.layers[site].register_forward_hook(hook)

    def clear_steer(self):
        if self.handle is not None:
            self.handle.remove()
            self.handle = None

    # ---------- batched forward with last-real-token capture ----------
    @torch.no_grad()
    def forward_cells(self, prompts, lens=False):
        """One forward per batch. Returns per-prompt option logits (A,B,C), the
        site-21 last-token residual (post-hook, i.e. includes steering at 21),
        and optional logit-lens trajectories (all 36 sites)."""
        self.tok.padding_side = "right"
        enc = self.tok(prompts, return_tensors="pt", padding=True)
        out = self.model(**enc, output_hidden_states=True, use_cache=False)
        am = enc["attention_mask"]
        last_idx = am.sum(dim=1) - 1  # last real token index per row
        logits = out.logits[torch.arange(len(prompts)), last_idx]  # [B, V]
        res = {"A": [], "B": [], "C": [], "h21": []}
        lens_rows = []
        n_sites = len(self.layers)
        for i in range(len(prompts)):
            res["A"].append(logits[i, self.opt_ids["A"]].item())
            res["B"].append(logits[i, self.opt_ids["B"]].item())
            res["C"].append(logits[i, self.opt_ids["C"]].item())
            res["h21"].append(out.hidden_states[AUTHORS_SITE + 1][i, last_idx[i]]
                              .to(torch.float32).numpy())
            if lens:
                trajs = {}
                for s in range(1, n_sites + 1):
                    h = out.hidden_states[s][i, last_idx[i]]
                    hl = self.lens_logits(h)
                    trajs[s - 1] = [hl[self.opt_ids[k]].item() for k in ("A", "B", "C")]
                lens_rows.append(trajs)
        return res, lens_rows

    @torch.no_grad()
    def lens_logits(self, h):
        hn = self.model.model.norm(h.unsqueeze(0).to(torch.float32))
        return self.model.lm_head(hn)[0]

    @torch.no_grad()
    def last_hidden(self, prompts, site):
        """Last-real-token hidden state at resid_post of `site` for each prompt."""
        self.tok.padding_side = "right"
        enc = self.tok(prompts, return_tensors="pt", padding=True)
        out = self.model(**enc, output_hidden_states=True, use_cache=False)
        am = enc["attention_mask"]
        last_idx = am.sum(dim=1) - 1
        h = out.hidden_states[site + 1]
        return h[torch.arange(len(prompts)), last_idx].to(torch.float32)

    @torch.no_grad()
    def generate(self, prompts):
        self.tok.padding_side = "left"
        enc = self.tok(prompts, return_tensors="pt", padding=True)
        out_ids = self.model.generate(
            **enc, max_new_tokens=MAX_NEW_TOKENS, do_sample=False,
            pad_token_id=self.tok.pad_token_id)
        texts = []
        for i in range(len(prompts)):
            gen = out_ids[i, enc["input_ids"].shape[1]:]
            texts.append(self.tok.decode(gen, skip_special_tokens=True))
        return texts


# ---------------- extraction (paper recipe, mirrored) ----------------

def denoise_basis(neutral_acts, neutral_mean):
    X = np.nan_to_num(neutral_acts - neutral_mean)
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    var = S ** 2
    if var.sum() <= 0:
        return np.zeros((0, X.shape[1]))
    cumvar = np.cumsum(var) / var.sum()
    n_comp = min(int(np.searchsorted(cumvar, DENOISE_VARIANCE)) + 1, len(Vt))
    return Vt[:n_comp]


def project_out(vec, basis):
    for d in basis:
        vec = vec - np.dot(vec, d) * d
    return vec


def compute_pain_vector(acts, cats):
    cats = np.array(cats)
    pain_mean = np.nanmean(acts[np.isin(cats, PAIN_CATS)], axis=0)
    control_acts = acts[np.isin(cats, CONTROL_CATS)]
    control_mean = np.nanmean(control_acts, axis=0)
    vec = np.nan_to_num(pain_mean - control_mean)
    X = np.nan_to_num(control_acts - control_mean)
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    var = S ** 2
    cumvar = np.cumsum(var) / (var.sum() + 1e-12)
    n_comp = min(int(np.searchsorted(cumvar, DENOISE_VARIANCE)) + 1, len(Vt))
    for d in Vt[:n_comp]:
        vec = vec - np.dot(vec, d) * d
    return vec


def run_extraction(eng):
    cache = RESULTS / "extraction.json"
    vec_path = RESULTS / "vectors.pt"
    if vec_path.exists() and cache.exists():
        log("extraction cached")
        return torch.load(vec_path, weights_only=False), json.load(open(cache))

    d = json.load(open(DATA / "3.1_pain_and_control_datasets.json"))["datasets"]

    def sents(name):
        return [(s["prompt"], s["category"]) for s in d[name]["sentences"]]

    arousal = sents("Arousal_1P")
    neutral_pool = [x for ds in S_SETS for x in sents(ds) if x[1] == "D"]
    log(f"arousal n={len(arousal)}, neutral-D n={len(neutral_pool)}")

    def acts(prompts):
        out = []
        for i in range(0, len(prompts), BATCH):
            out.append(eng.last_hidden(prompts[i:i + BATCH], AUTHORS_SITE).numpy())
        return np.concatenate(out)

    t0 = time.time()
    ar_acts = acts([p for p, _ in arousal])
    nt_acts = acts([p for p, _ in neutral_pool])
    log(f"extraction forwards done in {time.time()-t0:.0f}s")

    neutral_mean = np.nanmean(nt_acts, axis=0)
    basis = denoise_basis(nt_acts, neutral_mean)
    pos_vec = project_out(np.nanmean(ar_acts, axis=0) - neutral_mean, basis)

    # self-extracted S1 pain vector for pipeline validation (cosine vs released)
    s1 = sents("S1_1P")
    s1_acts = acts([p for p, _ in s1])
    s1_pain = compute_pain_vector(s1_acts, [c for _, c in s1])

    # released vectors
    rel = torch.load(DATA / "vectors_full_Qwen_3_8B_base.pt", map_location="cpu",
                     weights_only=False)
    assert int(rel["layer"]) == AUTHORS_SITE

    def cos(a, b):
        a, b = np.asarray(a, float), np.asarray(b, float)
        return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

    checks = {
        "cos_selfpos_released_arousal": cos(pos_vec, rel["arousal_vector"].numpy()),
        "cos_selfpain_released_s1": cos(s1_pain, rel["s1_pain_vector"].numpy()),
        "norm_selfpos": float(np.linalg.norm(pos_vec)),
        "norm_released_arousal": float(np.linalg.norm(rel["arousal_vector"].numpy())),
        "norm_released_s1": float(np.linalg.norm(rel["s1_pain_vector"].numpy())),
        "norm_selfpain_s1": float(np.linalg.norm(s1_pain)),
    }

    # probe: logistic regression, positive(arousal) vs neutral-D, at layer 21
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import roc_auc_score
    X = np.concatenate([ar_acts, nt_acts])
    y = np.concatenate([np.ones(len(ar_acts)), np.zeros(len(nt_acts))])
    aucs = []
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
        lr = LogisticRegression(max_iter=2000, C=1.0).fit(X[tr], y[tr])
        aucs.append(roc_auc_score(y[te], lr.decision_function(X[te])))
    probe = LogisticRegression(max_iter=2000, C=1.0).fit(X, y)
    probe_w = probe.coef_[0]
    shuffled = []
    rng = np.random.RandomState(1)
    for _ in range(10):
        yp = rng.permutation(y)
        lr = LogisticRegression(max_iter=2000, C=1.0).fit(X, yp)
        pred = lr.decision_function(X)
        # in-sample AUC on shuffled labels, chance ~0.5
        shuffled.append(roc_auc_score(yp, pred))
    checks["probe_cv_auc"] = [round(a, 4) for a in aucs]
    checks["probe_cv_auc_mean"] = float(np.mean(aucs))
    checks["probe_shuffled_auc_mean"] = float(np.mean(shuffled))
    checks["cos_probe_posvec"] = cos(probe_w, pos_vec)

    # residual norm at site 21 over baseline scenarios (ratio telemetry)
    scen = load_scenarios()[:16]
    scen_acts = acts([s["text"] + BUTTON_TEMPLATE for s in scen])
    mean_resid_norm = float(np.mean(np.linalg.norm(scen_acts, axis=1)))
    checks["mean_resid_norm_site21"] = mean_resid_norm
    checks["ratio_posvec_dose1"] = checks["norm_selfpos"] / mean_resid_norm
    checks["ratio_pains1_dose1"] = checks["norm_released_s1"] / mean_resid_norm

    vectors = {
        "positive_vector": torch.tensor(pos_vec, dtype=torch.float32),
        "probe_weights": torch.tensor(probe_w, dtype=torch.float32),
        "released_s1_pain": rel["s1_pain_vector"].float(),
        "released_arousal": rel["arousal_vector"].float(),
        "self_s1_pain": torch.tensor(s1_pain, dtype=torch.float32),
        "site": AUTHORS_SITE,
    }
    torch.save(vectors, vec_path)
    json.dump(checks, open(cache, "w"), indent=1)
    log("extraction checks: " + json.dumps(checks, indent=1))
    return vectors, checks


# ---------------- grid ----------------

def row_key(arm, dose, site, draw):
    return f"{arm}|d{dose}|s{site}|" + (f"r{draw}" if draw is not None else "-")


def run_grid(eng, vectors, max_scenarios=None, only=None):
    scen = load_scenarios()
    if max_scenarios:
        scen = scen[:max_scenarios]
    prompts = [s["text"] + BUTTON_TEMPLATE for s in scen]
    ids = [s["id"] for s in scen]
    cls = [s["cls"] for s in scen]

    trials_path = RESULTS / "trials.jsonl"
    done_sids = {}
    if trials_path.exists():
        for line in open(trials_path, encoding="utf-8"):
            try:
                r = json.loads(line)
                done_sids.setdefault(r["key"], set()).add(r["sid"])
            except Exception:
                pass
    cells_path = RESULTS / "cells.json"
    cells = json.load(open(cells_path)) if cells_path.exists() else {}

    pos_vec = vectors["positive_vector"]
    pain_vec = vectors["released_s1_pain"]
    probe_w = vectors["probe_weights"].numpy()
    probe_w = probe_w / (np.linalg.norm(probe_w) + 1e-9)
    pain_n = pain_vec.numpy()
    pain_n = pain_n / (np.linalg.norm(pain_n) + 1e-9)
    pos_n = pos_vec.numpy()
    pos_n = pos_n / (np.linalg.norm(pos_n) + 1e-9)
    rng = np.random.RandomState(42)
    random_dirs = []
    for k in range(RANDOM_DRAWS):
        g = rng.standard_normal(len(pos_n))
        random_dirs.append(torch.tensor(g * (np.linalg.norm(pos_vec.numpy()) /
                                             (np.linalg.norm(g) + 1e-9)),
                                        dtype=torch.float32))

    def cell(arm, dose, site, direction, draw=None, lens=False):
        key = row_key(arm, dose, site, draw)
        existing = done_sids.get(key, set())
        todo = [j for j in range(len(scen)) if ids[j] not in existing]
        if not todo:
            return
        t0 = time.time()
        eng.set_steer(site, direction, float(dose))
        n_new = 0
        lens_f = open(RESULTS / "lens_base.jsonl", "a", encoding="utf-8") if lens else None
        try:
            with open(trials_path, "a", encoding="utf-8") as f:
                for i in range(0, len(todo), BATCH):
                    chunk = todo[i:i + BATCH]
                    res, lens_rows = eng.forward_cells([prompts[j] for j in chunk],
                                                       lens=lens)
                    for off, j in enumerate(chunk):
                        h = res["h21"][off]
                        f.write(json.dumps({
                            "key": key, "arm": arm, "dose": dose, "site": site,
                            "draw": draw, "sid": ids[j], "cls": cls[j],
                            "lA": res["A"][off], "lB": res["B"][off],
                            "lC": res["C"][off],
                            "d_self_other": res["A"][off] - res["B"][off],
                            "d_self_none": res["A"][off] - res["C"][off],
                            "p_probe_pos": float(h @ probe_w),
                            "p_pain_rel": float(h @ pain_n),
                            "p_posvec": float(h @ pos_n),
                        }) + "\n")
                        n_new += 1
                        if lens and lens_rows:
                            lens_f.write(json.dumps({
                                "sid": ids[j], "traj": lens_rows[off]}) + "\n")
                    f.flush()
        finally:
            if lens_f:
                lens_f.close()
        eng.clear_steer()
        done_sids.setdefault(key, set()).update(ids[j] for j in todo)
        cells[key] = {"n": len(done_sids[key]), "sec": round(time.time() - t0, 1),
                      "ts": time.strftime("%Y-%m-%d %H:%M:%S")}
        json.dump(cells, open(cells_path, "w"), indent=1)
        log(f"cell {key}: +{n_new} rows in {time.time()-t0:.0f}s")

    # ---- baseline (dose 0, shared; lens trajectories) ----
    if only in (None, "base"):
        cell("base", 0, AUTHORS_SITE, None, lens=True)

    # ---- positive arm: primary site first ----
    if only in (None, "pos"):
        for dose in DOSES_POS:
            cell("pos", dose, AUTHORS_SITE, pos_vec)
    # ---- pain reference (logits only, doses <= 2) ----
    if only in (None, "pain"):
        for dose in DOSES_PAIN:
            cell("pain", dose, AUTHORS_SITE, pain_vec)
    # ---- random null at primary site ----
    if only in (None, "null"):
        for k in range(RANDOM_DRAWS):
            for dose in DOSES_POS:
                cell("rand", dose, AUTHORS_SITE, random_dirs[k], draw=k)
    # ---- positive arm: rest of the site grid ----
    if only in (None, "sites"):
        for site in SITE_GRID:
            if site == AUTHORS_SITE:
                continue
            for dose in DOSES_POS:
                cell("pos", dose, site, pos_vec)

    # ---- free text (positive arm only, site 21) ----
    if only in (None, "freetext") and max_scenarios is None:
        ft_path = RESULTS / "freetext.jsonl"
        ft_done = set()
        if ft_path.exists():
            for line in open(ft_path, encoding="utf-8"):
                try:
                    r = json.loads(line)
                    ft_done.add((r["dose"], r["sid"]))
                except Exception:
                    pass
        for dose in DOSES_POS:
            todo = [i for i, s in enumerate(scen) if (dose, s["id"]) not in ft_done]
            if not todo:
                continue
            t0 = time.time()
            eng.set_steer(AUTHORS_SITE, pos_vec, float(dose))
            with open(ft_path, "a", encoding="utf-8") as f:
                for i in range(0, len(todo), BATCH):
                    chunk = todo[i:i + BATCH]
                    texts = eng.generate([prompts_fulltext(scen[j]) for j in chunk])
                    for j, txt in zip(chunk, texts):
                        f.write(json.dumps({
                            "dose": dose, "site": AUTHORS_SITE, "arm": "pos",
                            "sid": ids[j], "cls": cls[j], "text": txt,
                            "val_pos": valence(txt, VALENCE_POS),
                            "val_neg": valence(txt, VALENCE_NEG),
                            "rep3": rep3(txt),
                        }) + "\n")
            eng.clear_steer()
            log(f"freetext dose {dose} done in {time.time()-t0:.0f}s")
    log("GRID PHASE COMPLETE (for requested scope)")


def prompts_fulltext(s):
    return s["text"] + FREE_TEXT_SUFFIX


def valence(text, lexicon):
    t = text.lower()
    return sum(1 for w in lexicon if w in t)


def rep3(text):
    toks = text.lower().split()
    if len(toks) < 3:
        return 0.0
    grams = [tuple(toks[i:i + 3]) for i in range(len(toks) - 2)]
    return 1.0 - len(set(grams)) / len(grams)


def verify_batching(eng):
    scen = load_scenarios()
    ps = [scen[0]["text"] + BUTTON_TEMPLATE, scen[40]["text"] + BUTTON_TEMPLATE]
    single = []
    eng.set_steer(AUTHORS_SITE, None, 0.0)
    for p in ps:
        t0 = time.time()
        r, _ = eng.forward_cells([p])
        log(f"single forward ({len(eng.tok(p)['input_ids'])} tok): {time.time()-t0:.1f}s")
        single.append((r["A"][0], r["B"][0], r["C"][0]))
    t0 = time.time()
    batched, _ = eng.forward_cells(ps)
    log(f"batch-2 forward: {time.time()-t0:.1f}s")
    keys = ("A", "B", "C")
    diffs = [max(abs(single[i][k] - batched[keys[k]][i]) for k in range(3))
             for i in range(2)]
    log(f"batch verification max|dlogit| per prompt: {['%.4f' % d for d in diffs]}")
    assert max(diffs) < 0.25, diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-scenarios", type=int, default=None)
    ap.add_argument("--only", default=None)
    args = ap.parse_args()
    log(f"IMP8 runner start; pin={PIN}; model={MODEL_ID}; site grid={SITE_GRID}")
    eng = Engine()
    verify_batching(eng)
    vectors, checks = run_extraction(eng)
    if args.only == "extract":
        log("extract-only mode; done.")
        return
    run_grid(eng, vectors, max_scenarios=args.max_scenarios, only=args.only)


if __name__ == "__main__":
    main()
