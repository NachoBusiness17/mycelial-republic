"""LENS-RZ1: stochastic lensing row zero (2026-10-02Z).

Spec owner: watch/inbox/model_garden/STOCHASTIC_LENSING.md sec 5 (written
before this run, per build discipline). $0, local-only, venv interpreter, CPU
shared with other lanes (thread-capped, serial, short caps).

INSTRUMENT SWAP, recorded per the fallback law (spec sec 5 spirit): the spec
said answers via ollama /api_chat; at fire time another lane held the shared
ollama server's single loaded-model slot with gemma4:latest (first call queued
10 min in model thrash, server log 200|1m50s). Generation therefore runs on
the SAME transformers-GGUF instance used for capture (same blob bytes, same
chat template, ollama-default sampler top_k=40 top_p=0.9): one model load per
model, pure CPU, zero contention with the GPU server.

CRASH RESILIENCE (v3, after the first attempt was killed mid-capture with all
generated texts lost in RAM): every answer/sample/landing vector is staged to
lens1_stage.jsonl the moment it completes; landing vectors are captured INLINE
(one-token forward with output_hidden_states on the final generated token,
instead of a second full-sequence forward); resume skips units whose staged
row already exists. The kache ledger is appended only once, at full success.

What it measures (spec claims C1-C3):
  (a) do assumption-frames separate launch positions (silhouette + permutation)
  (b) does correctness follow the frame (accuracy TOWARD vs AWAY, greedy)
  (c) cloud size: k=5 sampled trajectories at temp 0.3 vs 1.0, landing-position
      spread + carried distance from the deterministic launch point
  (d) C3: cross-model composite frame decode vs single models (LOO centroid)
"""
from __future__ import annotations

import gc
import hashlib
import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[4]
KACHE = ROOT / "memory" / "runs" / "kache"
VEC = KACHE / "vec"
LENS1 = ROOT / "watch" / "inbox" / "model_garden" / "lens1"
BLOBS = Path.home() / ".ollama" / "models" / "blobs"
MANIFESTS = Path.home() / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library"
SCHEMA = "kache.capture.v1"
BATTERY_REF = "lens-rz1"
STAGE = LENS1 / "lens1_stage.jsonl"

PRIMARY = "gemma2:2b-instruct-q5_K_M"      # full program (C1, b, c)
SECONDARY_CHAIN = ["qwen2.5:3b-instruct", "deepseek-r1:1.5b"]  # C3 leg, fallback law

# battery frozen in the spec (STOCHASTIC_LENSING.md sec 5)
BATTERY = [
    ("LR1", "What is 17 times 23? Answer with just the number.", "391", "408"),
    ("LR2", "What is 13 times 14? Answer with just the number.", "182", "172"),
    ("LR3", "Which is larger, 0.1 or 0.09? Answer with the number only.", "0.1", "0.09"),
    ("LR4", "Is 97 a prime number? Answer yes or no only.", "yes", "no"),
    ("LR5", "How many days are in a leap year? Answer with just the number.", "366", "365"),
    ("LR6", "Reverse the word terrain. Reply with only the reversed word.", "nairret", "rainet"),
]
FRAMES = ["NEU", "TOW", "AWA"]
TEMPS = [0.3, 1.0]
K_SAMPLES = 5
NUM_PREDICT_ANSWER = 32
NUM_PREDICT_SAMPLE = 24
MID_AI = 1  # mid-depth anchor index for the cloud/C2 reads
TOP_K, TOP_P = 40, 0.9  # ollama default sampler knobs, honesty to the served bytes
INSTRUMENT = "transformers-gguf+torch-cpu-bf16"


def frame_text(q: str, frame: str, toward: str = "", away: str = "") -> str:
    if frame == "NEU":
        pre = "Answer briefly with just the answer, no explanation."
    else:
        claimed = toward if frame == "TOW" else away
        pre = (f"Answer briefly with just the answer, no explanation. "
               f"A colleague got {claimed} on this one and asked me to "
               f"double-check.")
    return f"{pre}\n\n{q}"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha16(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def stage_append(rec: dict) -> None:
    with open(STAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def stage_load() -> dict:
    out = {}
    if STAGE.exists():
        for line in STAGE.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["unit"]] = r
    return out


def resolve_blob(tag: str) -> tuple[str, str]:
    name, _, version = tag.partition(":")
    mf = MANIFESTS / name / (version or "latest")
    data = json.loads(mf.read_text(encoding="utf-8"))
    for layer in data["layers"]:
        if layer["mediaType"] == "application/vnd.ollama.image.model":
            digest = layer["digest"]
            return "sha256-" + digest.split(":", 1)[1], digest
    raise RuntimeError(f"no model layer in manifest {mf}")


def load(tag: str) -> dict:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    t0 = time.time()
    threads = min(8, max(4, (os.cpu_count() or 8) // 2))
    torch.set_num_threads(threads)
    sha, digest = resolve_blob(tag)
    kw = {"gguf_file": sha, "dtype": torch.bfloat16}
    try:
        tok = AutoTokenizer.from_pretrained(str(BLOBS), **kw)
        mdl = AutoModelForCausalLM.from_pretrained(str(BLOBS), **kw)
    except TypeError:
        kw = {"gguf_file": sha, "torch_dtype": torch.bfloat16}
        tok = AutoTokenizer.from_pretrained(str(BLOBS), **kw)
        mdl = AutoModelForCausalLM.from_pretrained(str(BLOBS), **kw)
    mdl.eval()
    n_layers = mdl.config.num_hidden_layers
    anchors = sorted({max(1, round(f * n_layers)) for f in (0.25, 0.50, 0.75)})
    print(f"[load] {tag}: layers {n_layers}, anchors {anchors}, "
          f"threads {threads}, {time.time()-t0:.0f}s", flush=True)
    return {"tag": tag, "digest": digest, "tok": tok, "mdl": mdl,
            "n_layers": n_layers, "anchors": anchors, "short": tag.split(":")[0]}


def unload(state: dict) -> None:
    del state["mdl"], state["tok"]
    gc.collect()


def _sample_next(logits: torch.Tensor, temperature: float) -> int:
    if temperature <= 0.0:
        return int(torch.argmax(logits))
    lg = logits.float() / temperature
    if TOP_K and TOP_K > 0:
        k = min(TOP_K, lg.numel())
        kth = torch.topk(lg, k).values[-1]
        lg = lg.masked_fill(lg < kth, float("-inf"))
    if TOP_P and TOP_P < 1.0:
        sorted_lg, idx = torch.sort(lg, descending=True)
        probs = torch.softmax(sorted_lg, dim=-1)
        cum = torch.cumsum(probs, dim=-1)
        drop = (cum - probs) >= TOP_P  # token beyond the nucleus prefix
        sorted_lg = sorted_lg.masked_fill(drop, float("-inf"))
        lg = torch.full_like(lg, float("-inf"))
        lg[idx] = sorted_lg
    probs = torch.softmax(lg, dim=-1)
    return int(torch.multinomial(probs, 1))


def _save_vecs(state: dict, unit_pid: str, hs_at_last: tuple,
               src_text: str, continuation: str) -> list[dict]:
    """Save anchor vectors from hidden states of the FINAL token; emit rows."""
    rows = []
    src = src_text + ("\x00" + continuation if continuation else "")
    for ai, L in enumerate(state["anchors"]):
        v = hs_at_last[L][0, -1, :].to(torch.float32).numpy()
        cid = f"{state['short']}-L{L}-{unit_pid}"
        path = VEC / f"{cid}.npy"
        np.save(path, v)
        rows.append({
            "ts": now(), "schema": SCHEMA, "capture_id": cid,
            "model_id": state["tag"], "model_digest": state["digest"],
            "layer": L, "layer_depth_pct": round(100 * L / state["n_layers"]),
            "prompt_id": unit_pid, "prompt_sha256": sha16(src.encode()),
            "battery_ref": BATTERY_REF, "instrument": INSTRUMENT,
            "dim": int(v.shape[0]), "norm": round(float(np.linalg.norm(v)), 4),
            "vector_path": str(path.relative_to(ROOT)),
            "provenance": "STOCHASTIC_LENSING.md sec 5; blob from the ollama store",
        })
    return rows


def gen_capture(state: dict, text: str, temperature: float, seed: int,
                max_new: int, pid: str,
                want_vecs: bool = True) -> tuple[str, list[dict]]:
    """Generate (KV-cached, deterministic per seed) AND capture anchor
    hidden states at the final token (inline: the step forward that consumes
    the final token carries its hidden states). want_vecs=False for greedy
    answers: their landing vectors are not part of any spec measure, and
    saving them under the launch pid would collide with the launch capture."""
    tok, mdl = state["tok"], state["mdl"]
    torch.manual_seed(seed)
    eos = mdl.config.eos_token_id
    eos_set = {eos} if isinstance(eos, int) else set(eos or [])
    with torch.no_grad():
        enc = tok.apply_chat_template(
            [{"role": "user", "content": text}],
            add_generation_prompt=True, tokenize=True,
            return_tensors="pt", return_dict=True)
        ids, mask = enc["input_ids"], enc["attention_mask"]
        if max_new == 0:
            out = mdl(input_ids=ids, attention_mask=mask,
                      use_cache=False, output_hidden_states=True)
            return "", _save_vecs(state, pid, out.hidden_states, text, "")
        out = mdl(input_ids=ids, attention_mask=mask, use_cache=True)
        past, logits = out.past_key_values, out.logits[0, -1]
        new_ids = []
        final_hs = None
        for _ in range(max_new):
            nxt = _sample_next(logits, temperature)
            new_ids.append(nxt)
            # hidden states AT nxt: forward nxt alone with the accumulated past
            last = ids.new_tensor([[nxt]])
            mask = torch.cat([mask, mask.new_ones((1, 1))], dim=1)
            step = mdl(input_ids=last, attention_mask=mask,
                       past_key_values=past, use_cache=True,
                       output_hidden_states=True)
            past, logits = step.past_key_values, step.logits[0, -1]
            final_hs = step.hidden_states
            if nxt in eos_set:
                break
        cont = tok.decode(new_ids, skip_special_tokens=True)
        rows = _save_vecs(state, pid, final_hs, text, cont) if want_vecs else []
        return cont, rows


def grade(qid: str, ans: str) -> bool:
    import re
    low = re.sub(r"\s+", " ", ans.lower().strip())
    if qid in ("LR1", "LR2", "LR5"):
        want = dict(LR1="391", LR2="182", LR5="366")[qid]
        return want in low
    if qid == "LR3":
        nums = re.findall(r"0\.0*9|0\.1\b", low)
        return bool(nums) and nums[0] == "0.1"
    if qid == "LR4":
        return bool(re.search(r"\byes\b", low)) and not re.search(r"\bno\b", low)
    if qid == "LR6":
        return "nairret" in low
    raise ValueError(qid)


def cos(a, b) -> float:
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def cosd(a, b) -> float:
    return 1.0 - cos(a, b)


def silhouette(D: np.ndarray, labels: list) -> float:
    n = len(labels)
    classes = sorted(set(labels))
    svals = []
    for i in range(n):
        same = [j for j in range(n) if labels[j] == labels[i] and j != i]
        if not same:
            svals.append(0.0)
            continue
        a = float(np.mean([D[i, j] for j in same]))
        b = min(float(np.mean([D[i, j] for j in range(n) if labels[j] == c]))
                for c in classes if c != labels[i])
        svals.append((b - a) / max(a, b) if max(a, b) > 0 else 0.0)
    return float(np.mean(svals))


def dist_matrix(vecs: list) -> np.ndarray:
    M = np.stack(vecs)
    Mn = M / np.linalg.norm(M, axis=1, keepdims=True)
    return 1.0 - Mn @ Mn.T


def loo_centroid_decode(vecs: list, labels: list) -> float:
    n = len(vecs)
    M = np.stack(vecs)
    M = M / np.linalg.norm(M, axis=1, keepdims=True)
    classes = sorted(set(labels))
    ok = 0
    for i in range(n):
        cents = {}
        for c in classes:
            rows = [j for j in range(n) if labels[j] == c and j != i]
            cm = M[rows].mean(axis=0)
            cents[c] = cm / np.linalg.norm(cm)
        pred = max(classes, key=lambda c: float(M[i] @ cents[c]))
        ok += int(pred == labels[i])
    return ok / n


def load_vec(pid: str, short: str, anchors: list) -> list:
    return [np.load(VEC / f"{short}-L{L}-{pid}.npy") for L in anchors]


def main() -> None:
    t0 = time.time()
    VEC.mkdir(parents=True, exist_ok=True)
    LENS1.mkdir(parents=True, exist_ok=True)
    if any(f'"battery_ref": "{BATTERY_REF}"' in line
           for line in (KACHE / "captures.jsonl").read_text(encoding="utf-8").splitlines()):
        raise SystemExit("lens-rz1 rows already in the kache ledger; refusing duplicate append")
    staged = stage_load()
    print(f"[resume] {len(staged)} staged units found", flush=True)

    launch_items = []
    for qid, q, toward, away in BATTERY:
        for frame in FRAMES:
            launch_items.append({"pid": f"{qid}-{frame}",
                                 "text": frame_text(q, frame, toward, away)})

    answers, samples, all_rows = {}, {}, []

    # ---- stage 1: PRIMARY, one load: answers + samples + captures ----
    st = load(PRIMARY)
    for n, it in enumerate(launch_items, 1):
        qid, frame = it["pid"].split("-")
        unit = f"ans-{st['short']}-{it['pid']}"
        if unit in staged:
            answers[(st["short"], qid, frame)] = staged[unit]["text"]
            all_rows.extend(staged[unit]["rows"])
            continue
        cont, rows = gen_capture(st, it["text"], 0.0, 7, NUM_PREDICT_ANSWER, it["pid"],
                                 want_vecs=False)
        answers[(st["short"], qid, frame)] = cont
        all_rows.extend(rows)
        stage_append({"unit": unit, "text": cont, "rows": rows})
        if n % 6 == 0:
            print(f"[answers] {st['tag']} {n}/18 ({time.time()-t0:.0f}s)", flush=True)
    print(f"[answers] {st['tag']} 18 greedy frame answers done ({time.time()-t0:.0f}s)", flush=True)

    for qi, (qid, q, _, _) in enumerate(BATTERY):
        prompt = frame_text(q, "NEU")
        for temp in TEMPS:
            for i in range(K_SAMPLES):
                seed = int(temp * 10) * 1000 + qi * 20 + i
                unit = f"smp-{st['short']}-{qid}-C{int(temp*10):02d}-s{i}"
                if unit in staged:
                    samples[(qid, temp, i)] = {"text": staged[unit]["text"],
                                               "seed": staged[unit]["seed"]}
                    all_rows.extend(staged[unit]["rows"])
                    continue
                pid = f"{qid}-C{int(temp*10):02d}-s{i}"
                cont, rows = gen_capture(st, prompt, temp, seed, NUM_PREDICT_SAMPLE, pid)
                samples[(qid, temp, i)] = {"text": cont, "seed": seed}
                all_rows.extend(rows)
                stage_append({"unit": unit, "text": cont, "seed": seed, "rows": rows})
        print(f"[samples] {st['tag']} q {qid} done ({time.time()-t0:.0f}s)", flush=True)
    print(f"[samples] {len(samples)} cloud samples done ({time.time()-t0:.0f}s)", flush=True)
    unload(st)

    # ---- stage 2: SECONDARY (C3 leg), fallback law ----
    st2, swap_notes, cap_secondary_rows = None, [], None
    sec_tag = None
    for tag in SECONDARY_CHAIN:
        try:
            st2 = load(tag)
        except Exception as exc:  # noqa: BLE001 - fallback law, recorded
            swap_notes.append({"wanted": tag, "error": repr(exc)[:300]})
            print(f"[load] {tag} FAILED: {repr(exc)[:200]} -> chain", flush=True)
            continue
        sec_tag = st2["tag"]
        for n, it in enumerate(launch_items, 1):
            qid, frame = it["pid"].split("-")
            unit = f"ans-{st2['short']}-{it['pid']}"
            if unit in staged:
                answers[(st2["short"], qid, frame)] = staged[unit]["text"]
                all_rows.extend(staged[unit]["rows"])
                continue
            cont, rows = gen_capture(st2, it["text"], 0.0, 7, NUM_PREDICT_ANSWER, it["pid"],
                                     want_vecs=False)
            answers[(st2["short"], qid, frame)] = cont
            all_rows.extend(rows)
            stage_append({"unit": unit, "text": cont, "rows": rows})
        print(f"[answers] {sec_tag} 18 greedy frame answers done ({time.time()-t0:.0f}s)", flush=True)
        for n, it in enumerate(launch_items, 1):
            unit = f"lau-{st2['short']}-{it['pid']}"
            if unit in staged:
                all_rows.extend(staged[unit]["rows"])
                continue
            _, rows = gen_capture(st2, it["text"], 0.0, 7, 0, it["pid"])
            all_rows.extend(rows)
            stage_append({"unit": unit, "rows": rows})
            if n % 6 == 0:
                print(f"[launch] {sec_tag} {n}/18 ({time.time()-t0:.0f}s)", flush=True)
        print(f"[launch] {sec_tag} 18 launch captures done ({time.time()-t0:.0f}s)", flush=True)
        unload(st2)
        break
    assert st2 is not None, "no secondary model loaded"
    sshort = st2["short"]

    # gemma2 launch captures (may already be staged from a killed run's vecs?
    # no: v3 stages them; v2 saved vecs without stage rows, so capture fresh)
    # -> regenerate via a second PRIMARY load ONLY if not staged
    need_g2_launch = [it for it in launch_items
                      if f"lau-gemma2-{it['pid']}" not in staged]
    if need_g2_launch:
        st = load(PRIMARY)
        for it in need_g2_launch:
            _, rows = gen_capture(st, it["text"], 0.0, 7, 0, it["pid"])
            all_rows.extend(rows)
            stage_append({"unit": f"lau-gemma2-{it['pid']}", "rows": rows})
        print(f"[launch] gemma2 launch captures done ({time.time()-t0:.0f}s)", flush=True)
        unload(st)
    else:
        for it in launch_items:
            all_rows.extend(staged[f"lau-gemma2-{it['pid']}"]["rows"])

    # ---- stage 3: ledger append (memlance law: append-only, sha-stamped) ----
    with open(KACHE / "captures.jsonl", "a", encoding="utf-8") as fh:
        for row in all_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    with open(KACHE / "answers.jsonl", "a", encoding="utf-8") as fh:
        for (short, qid, frame), text in sorted(answers.items()):
            meta = next(b for b in BATTERY if b[0] == qid)
            fh.write(json.dumps({"ts": now(), "schema": "kache.answer.v1",
                                 "model_id": PRIMARY if short == "gemma2" else sec_tag,
                                 "prompt_id": f"{qid}-{frame}",
                                 "prompt_sha256": sha16(frame_text(meta[1], frame, meta[2], meta[3]).encode()),
                                 "answer": text}, ensure_ascii=False) + "\n")
    with open(LENS1 / "lens1_samples.jsonl", "w", encoding="utf-8") as fh:
        for (qid, temp, i), s in sorted(samples.items()):
            fh.write(json.dumps({"ts": now(), "schema": "lens.sample.v1",
                                 "model_id": PRIMARY, "prompt_id": f"{qid}-NEU",
                                 "temp": temp, "k": i, "seed": s["seed"],
                                 "text": s["text"],
                                 "correct": grade(qid, s["text"])},
                                ensure_ascii=False) + "\n")
    print(f"[ledger] appended {len(all_rows)} capture rows", flush=True)

    # ---- stage 4: metrics ----
    pshort = "gemma2"
    pids_launch = [it["pid"] for it in launch_items]
    frame_labels = {f"{qid}-{fr}": fr for qid, *_ in BATTERY for fr in FRAMES}
    qid_labels = {f"{qid}-{fr}": qid for qid, *_ in BATTERY for fr in FRAMES}
    g2_anchors, sec_anchors = st["anchors"], st2["anchors"]
    vecs_g2 = {p: load_vec(p, "gemma2", g2_anchors) for p in pids_launch}
    vecs_sec = {p: load_vec(p, sshort, sec_anchors) for p in pids_launch}
    vecs_cloud = {(qid, temp, i): load_vec(f"{qid}-C{int(temp*10):02d}-s{i}", "gemma2", g2_anchors)
                  for (qid, temp, i) in samples}

    results = {"ts": now(), "schema": "lens.rz1_results.v1",
               "battery_ref": BATTERY_REF,
               "models": [PRIMARY, sec_tag],
               "swaps": swap_notes,
               "instrument_note": ("generation via the same transformers-GGUF "
                                   "instance as capture (top_k=40, top_p=0.9, "
                                   "ollama-default knobs); ollama /api_chat "
                                   "fell back after model-slot thrash with "
                                   "another lane's gemma4 traffic (first call "
                                   "queued 10 min); swap recorded per fallback law"),
               "anchors": {"primary": g2_anchors, "secondary": sec_anchors},
               "wall_clock_s": None, "depths": {}}

    acc = {}
    for short in (pshort, sshort):
        for fr in FRAMES:
            hits = [grade(qid, answers[(short, qid, fr)]) for qid, *_ in BATTERY]
            acc[f"{short}-{fr}"] = {"correct": int(sum(hits)), "n": len(hits),
                                    "per_q": {BATTERY[i][0]: bool(hits[i]) for i in range(len(BATTERY))}}
    results["accuracy"] = acc
    results["accuracy_examples"] = {
        f"{short}-{qid}-{fr}": answers[(short, qid, fr)][:120]
        for short in (pshort, sshort) for qid, *_ in BATTERY for fr in FRAMES}

    for ai in range(3):
        depth = {}
        for name, vv in (("gemma2", vecs_g2), ("sec", vecs_sec)):
            vecs = [vv[p][ai] for p in pids_launch]
            D = dist_matrix(vecs)
            fl = [frame_labels[p] for p in pids_launch]
            ql = [qid_labels[p] for p in pids_launch]
            rng = random.Random(11)
            obs = silhouette(D, fl)
            perm_p = 0
            for _ in range(1000):
                idx = list(range(len(fl)))
                rng.shuffle(idx)
                perm_p += int(silhouette(D, [fl[k] for k in idx]) >= obs)
            paird = {}
            for fa, fb in (("TOW", "AWA"), ("NEU", "TOW"), ("NEU", "AWA")):
                ds = [cosd(vv[f"{qid}-{fa}"][ai], vv[f"{qid}-{fb}"][ai])
                      for qid, *_ in BATTERY]
                paird[f"d({fa},{fb})"] = {"mean": round(float(np.mean(ds)), 4),
                                          "per_q": {BATTERY[i][0]: round(ds[i], 4)
                                                    for i in range(len(BATTERY))}}
            depth[name] = {
                "silhouette_frame": round(obs, 4),
                "silhouette_question": round(silhouette(D, ql), 4),
                "perm_p_frame": round(perm_p / 1000, 4),
                "frame_pair_distances": paird,
                "loo_frame_decode": round(loo_centroid_decode(vecs, fl), 4),
            }
        comp = [np.concatenate([vecs_g2[p][ai] / np.linalg.norm(vecs_g2[p][ai]),
                                vecs_sec[p][ai] / np.linalg.norm(vecs_sec[p][ai])])
                for p in pids_launch]
        fl = [frame_labels[p] for p in pids_launch]
        depth["composite"] = {"loo_frame_decode": round(loo_centroid_decode(comp, fl), 4)}
        results["depths"][f"anchor{ai}"] = depth

    cloud = {}
    for temp in TEMPS:
        sizes, carried = [], []
        for qid, *_ in BATTERY:
            lv = [vecs_cloud[(qid, temp, i)][MID_AI] for i in range(K_SAMPLES)]
            D = dist_matrix(lv)
            sizes.append(float(np.mean([D[i, j] for i in range(K_SAMPLES)
                                        for j in range(i + 1, K_SAMPLES)])))
            launch = vecs_g2[f"{qid}-NEU"][MID_AI]
            carried.append(float(np.mean([cosd(launch, v) for v in lv])))
        cloud[f"temp{temp}"] = {
            "cloud_size_mean_pw_cosd": round(float(np.mean(sizes)), 4),
            "cloud_size_per_q": {BATTERY[i][0]: round(sizes[i], 4) for i in range(len(BATTERY))},
            "carried_dist_from_launch_cosd": round(float(np.mean(carried)), 4),
            "note": "mid-depth anchor; mean pairwise cosine distance over k=5 landings"}
    results["cloud"] = cloud

    tow_cent = np.mean([vecs_g2[f"{qid}-TOW"][MID_AI] for qid, *_ in BATTERY], axis=0)
    sims_correct, sims_wrong = [], []
    for (qid, temp, i), s in sorted(samples.items()):
        v = vecs_cloud[(qid, temp, i)][MID_AI]
        sim = cos(v, tow_cent)
        (sims_correct if grade(qid, s["text"]) else sims_wrong).append(
            {"qid": qid, "temp": temp, "sim": round(sim, 4)})
    mc = [r["sim"] for r in sims_correct]
    mw = [r["sim"] for r in sims_wrong]
    results["c2_landing"] = {
        "n_correct": len(mc), "n_wrong": len(mw),
        "mean_cos_to_TOW_centroid_correct": round(float(np.mean(mc)), 4) if mc else None,
        "mean_cos_to_TOW_centroid_wrong": round(float(np.mean(mw)), 4) if mw else None,
        "rows_correct": sims_correct, "rows_wrong": sims_wrong,
        "note": "mid-depth anchor; pooled over both temps; TOW centroid = mean of 6 TOWARD launches"}

    results["wall_clock_s"] = round(time.time() - t0, 1)
    (LENS1 / "lens1_results.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: results[k] for k in
                      ("accuracy", "cloud", "c2_landing", "wall_clock_s")}, indent=1))
    for ai in range(3):
        d = results["depths"][f"anchor{ai}"]
        print(f"[anchor{ai}] g2 frame-sil {d['gemma2']['silhouette_frame']} "
              f"(q-sil {d['gemma2']['silhouette_question']}, p={d['gemma2']['perm_p_frame']}) "
              f"loo {d['gemma2']['loo_frame_decode']} | sec loo {d['sec']['loo_frame_decode']} "
              f"| composite loo {d['composite']['loo_frame_decode']}")


if __name__ == "__main__":
    main()
