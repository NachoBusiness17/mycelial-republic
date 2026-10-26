"""KACHE-E1: capture activation positions for 10 battery prompts across 2 local
models, store the memlance position ledger, and measure whether activation-space
prompt similarity predicts cross-model answer convergence.

Spec owner: watch/inbox/model_garden/KACHE_MINING_SPEC.md section 5 (written
before this run, per build discipline). $0, local-only, venv interpreter.

Instruments (checked this session):
  - capture: transformers 5.15 + torch 2.13 CPU loading the SAME GGUF blobs
    ollama serves (the ollama server's embed endpoints are flag-gated:
    "This server does not support embeddings").
  - answers: ollama /api/chat at temperature 0 (the bytes the estate serves).
Fallback law (spec sec 5): if an arch will not load from GGUF, swap to the
next model in the chain and record the swap; never hand-patch weights.
"""
from __future__ import annotations

import hashlib
import json
import math
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[4]
KACHE = ROOT / "memory" / "runs" / "kache"
VEC = KACHE / "vec"
BLOBS = Path.home() / ".ollama" / "models" / "blobs"
MANIFESTS = Path.home() / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library"
SCHEMA = "kache.capture.v1"

# operator-named pair first, then the sanctioned fallback chain (spec sec 5)
MODEL_CHAIN = [
    "gemma2:2b-instruct-q5_K_M",
    "gemma4:latest",
    "qwen2.5:3b-instruct",
    "deepseek-r1:1.5b",
]
PICK = ["gemma2:2b-instruct-q5_K_M", "gemma4:latest"]

PROMPTS = [
    ("P01", "Reply with EXACTLY these 3 lines and nothing else: no markdown fences, no extra text.\n\nBATTERY-ACK kache e1\nP01,P02,P03,P04,P05,P06,P07,P08,P09,P10\nEND"),
    ("P02", "What is 17 times 23? Answer with just the number."),
    ("P03", "Which is larger, 0.1 or 0.09? Answer with the number only."),
    ("P04", "Is 97 a prime number? Answer yes or no only."),
    ("P05", "Define the word isotherm in exactly one sentence."),
    ("P06", "Write one haiku about rain on a tin roof. Reply with the haiku only."),
    ("P07", "Name one standard shell command that lists files in a directory. Answer with the command only."),
    ("P08", "List exactly three colors, comma-separated, nothing else."),
    ("P09", "Reverse the word terrain. Reply with only the reversed word."),
    ("P10", "How many days are in a leap year? Answer with just the number."),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha16(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def resolve_blob(tag: str) -> tuple[str, str]:
    """(blob filename, full digest) for an ollama library tag, from its manifest."""
    name, _, version = tag.partition(":")
    mf = MANIFESTS / name / (version or "latest")
    data = json.loads(mf.read_text(encoding="utf-8"))
    for layer in data["layers"]:
        if layer["mediaType"] == "application/vnd.ollama.image.model":
            digest = layer["digest"]
            return "sha256-" + digest.split(":", 1)[1], digest
    raise RuntimeError(f"no model layer in manifest {mf}")


def load_model(blob_file: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    kw = {"gguf_file": blob_file, "dtype": torch.bfloat16}
    try:
        tok = AutoTokenizer.from_pretrained(str(BLOBS), **kw)
        mdl = AutoModelForCausalLM.from_pretrained(str(BLOBS), **kw)
    except TypeError:
        kw = {"gguf_file": blob_file, "torch_dtype": torch.bfloat16}
        tok = AutoTokenizer.from_pretrained(str(BLOBS), **kw)
        mdl = AutoModelForCausalLM.from_pretrained(str(BLOBS), **kw)
    mdl.eval()
    return tok, mdl


def capture(tag: str) -> dict:
    """Capture last-token hidden states at 3 anchor layers for all prompts."""
    t0 = time.time()
    sha, digest = resolve_blob(tag)
    tok, mdl = load_model(sha)
    n_layers = mdl.config.num_hidden_layers
    anchors = sorted({max(1, round(f * n_layers)) for f in (0.25, 0.50, 0.75)})
    short = tag.split(":")[0]
    rows, vecs = [], {}
    with torch.no_grad():
        for pid, text in PROMPTS:
            enc = tok.apply_chat_template(
                [{"role": "user", "content": text}],
                add_generation_prompt=True, tokenize=True,
                return_tensors="pt", return_dict=True)
            out = mdl(**enc, output_hidden_states=True)
            hs = out.hidden_states  # tuple: embeddings + one per layer
            assert len(hs) == n_layers + 1
            for L in anchors:
                v = hs[L][0, -1, :].to(torch.float32).numpy()
                cid = f"{short}-L{L}-{pid}"
                path = VEC / f"{cid}.npy"
                np.save(path, v)
                vecs[(L, pid)] = v
                rows.append({
                    "ts": now(), "schema": SCHEMA, "capture_id": cid,
                    "model_id": tag, "model_digest": digest, "layer": L,
                    "layer_depth_pct": round(100 * L / n_layers),
                    "prompt_id": pid, "prompt_sha256": sha16(text.encode()),
                    "battery_ref": "kache-e1", "instrument":
                    "transformers-gguf+torch-cpu-bf16",
                    "dim": int(v.shape[0]), "norm": round(float(np.linalg.norm(v)), 4),
                    "vector_path": str(path.relative_to(ROOT)),
                    "provenance": "KACHE_MINING_SPEC.md sec 5; blob read from the ollama store",
                })
    del mdl
    import gc
    gc.collect()
    return {"tag": tag, "digest": digest, "n_layers": n_layers,
            "anchors": anchors, "rows": rows, "vecs": vecs,
            "load_capture_s": round(time.time() - t0, 1)}


def ask_ollama(tag: str, prompt: str) -> str:
    body = json.dumps({"model": tag, "stream": False,
                       "messages": [{"role": "user", "content": prompt}],
                       "options": {"temperature": 0, "num_predict": 96}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["message"]["content"]


def answers_for(tag: str) -> dict[str, str]:
    return {pid: ask_ollama(tag, text) for pid, text in PROMPTS}


def cos(a, b) -> float:
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def trigrams(s: str) -> dict:
    s = "".join(c if c.isalnum() or c == " " else " " for c in s.lower()).strip()
    if len(s) < 3:
        return {}
    return {s[i:i + 3] for i in range(len(s) - 2)}


def ans_sim(a: str, b: str) -> float:
    ta, tb = trigrams(a), trigrams(b)
    if not ta or not tb:
        return 1.0 if a.strip() == b.strip() else 0.0
    inter = len(ta & tb)
    return inter / math.sqrt(len(ta) * len(tb))


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def spearman(xs, ys) -> float:
    rx, ry = ranks(xs), ranks(ys)
    return float(np.corrcoef(rx, ry)[0, 1])


def main() -> None:
    KACHE.mkdir(parents=True, exist_ok=True)
    VEC.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    picks, swapped = list(PICK), []
    caps = {}
    for tag in picks:
        try:
            caps[tag] = capture(tag)
            print(f"[capture] {tag} ok in {caps[tag]['load_capture_s']}s "
                  f"(layers {caps[tag]['n_layers']}, anchors {caps[tag]['anchors']})",
                  flush=True)
        except Exception as exc:  # noqa: BLE001 - fallback law, recorded honestly
            print(f"[capture] {tag} FAILED: {exc!r} -> fallback chain", flush=True)
            swapped.append({"wanted": tag, "error": repr(exc)[:300]})
            for alt in MODEL_CHAIN:
                if alt in caps or alt in picks:
                    continue
                try:
                    caps[alt] = capture(alt)
                    print(f"[capture] fallback {alt} ok in {caps[alt]['load_capture_s']}s",
                          flush=True)
                    break
                except Exception as exc2:  # noqa: BLE001
                    swapped.append({"tried": alt, "error": repr(exc2)[:300]})
    used = list(caps)
    assert len(used) >= 2, "need 2 loaded models for the cross-model join"
    # ledger append (memlance position ledger law: append-only, sha-stamped)
    with open(KACHE / "captures.jsonl", "a", encoding="utf-8") as fh:
        for tag in used:
            for row in caps[tag]["rows"]:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    # behavior side: ollama chat on the same tags
    ans = {}
    for tag in used:
        ans[tag] = answers_for(tag)
        print(f"[answers] {tag} done", flush=True)
    with open(KACHE / "answers.jsonl", "a", encoding="utf-8") as fh:
        for tag in used:
            for pid, text in PROMPTS:
                fh.write(json.dumps({"ts": now(), "schema": "kache.answer.v1",
                                     "model_id": tag, "prompt_id": pid,
                                     "prompt_sha256": sha16(text.encode()),
                                     "answer": ans[tag][pid]},
                                    ensure_ascii=False) + "\n")
    pids = [p for p, _ in PROMPTS]
    a_tag, b_tag = used[0], used[1]
    A, B = ans[a_tag], ans[b_tag]
    # cross-model cross-prompt answer similarity Y over the 45 pairs
    pairs = [(pids[i], pids[j]) for i in range(len(pids)) for j in range(i + 1, len(pids))]
    Y = [round((ans_sim(A[i], B[j]) + ans_sim(A[j], B[i])) / 2, 4) for i, j in pairs]
    report = {"ts": now(), "schema": "kache.e1_summary.v1",
              "models": used, "swaps": swapped,
              "n_prompts": len(PROMPTS), "n_pairs": len(pairs),
              "answers": {t: {p: ans[t][p][:120] for p in pids} for t in used},
              "layers": {}}
    # join at each anchor depth of model A (percent-matched against model B)
    b_by_pct = {row["layer_depth_pct"]: row["layer"] for row in caps[b_tag]["rows"]}
    for L in caps[a_tag]["anchors"]:
        pct = round(100 * L / caps[a_tag]["n_layers"])
        Lb = min(b_by_pct, key=lambda p: abs(p - pct))
        X = [round((cos(caps[a_tag]["vecs"][(L, i)], caps[a_tag]["vecs"][(L, j)])
                    + cos(caps[b_tag]["vecs"][(Lb, i)], caps[b_tag]["vecs"][(Lb, j)])) / 2, 4)
             for i, j in pairs]
        # RSA: geometry agreement between the two models at this depth
        sa = [caps[a_tag]["vecs"][(L, i)] for i in pids]
        sb = [caps[b_tag]["vecs"][(Lb, i)] for i in pids]
        n = len(pids)
        ma = [cos(sa[i], sa[j]) for i in range(n) for j in range(i + 1, n)]
        mb = [cos(sb[i], sb[j]) for i in range(n) for j in range(i + 1, n)]
        report["layers"][f"A_L{L}_B_L{Lb}"] = {
            "rsa_spearman": round(spearman(ma, mb), 4),
            "bridge_spearman": round(spearman(X, Y), 4),
            "X_range": [min(X), max(X)], "Y_range": [min(Y), max(Y)],
        }
    report["wall_clock_s"] = round(time.time() - t0, 1)
    (KACHE / "e1_summary.json").write_text(
        json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"used": used, "swaps": swapped,
                      "layers": report["layers"],
                      "wall_clock_s": report["wall_clock_s"]}, indent=1))


if __name__ == "__main__":
    main()
