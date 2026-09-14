"""phase_lift_real — the moment of truth: phase-lift on REAL model logits.

Synthetic proved the mechanism is sound (aligned_greedy, alpha~0.25 -> steer 1.0,
KL ~0.02 nats). The open question: do REAL model logits contain any usable,
meaningful phase direction worth steering with?

This adapter:
  1. Loads a small real model (transformers). Full V-dim logits come from a forward
     pass — the ONLY honest source (chat APIs / Ollama give top-N only).
  2. Constructs a candidate phase signal phi. First real trial starts with the
     simplest meaningful candidates:
       - constant phase (baseline: proves the collapse path works on real logits)
       - accumulated phase: running phase from previous accepted tokens
         (encourages coherence, the operator's candidate #3)
  3. Runs the winning collapse (aligned_greedy, low alpha) and reports:
       - KL(phase-implied-dist || original softmax)  -- must stay low
       - token log-prob under the original model (coherence proxy)
       - determinism / repetition vs greedy
  4. Post the numbers even if ugly. That is the next decision point.

Schema: phase_lift_real.v1 · reuse: phase_lift (complex_lift, phase_collapse, metrics)
"""
from __future__ import annotations

import json
import math
import random
from typing import Any

import numpy as np

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

from mag import phase_lift as pl

SCHEMA = "phase_lift_real.v1"
DEFAULT_MODEL = "gpt2"          # 124M, tiny, CPU-friendly, gives full logits


def _tokens_phases_from_ids(ids: np.ndarray, groups: int = 8) -> np.ndarray:
    """Naive but real phase candidate: assign each token a phase by its id bucket.

    This is a PROXY for a meaningful steering direction (lexical cluster by token-id
    bucket). It tests whether the collapse even operates coherently on real logits.
    Honest: this is not yet a learned semantic direction; it's the first real probe.
    """
    return (ids % groups).astype(np.float64) * (2.0 * math.pi / groups)


def _constant_phase(vocab: int, angle: float) -> np.ndarray:
    return np.full(vocab, angle)


class RealLogits:
    """Small real model giving full V-dim logits via a single forward pass."""

    def __init__(self, model_name: str = DEFAULT_MODEL):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, dtype=torch.float32)
        self.model.eval()

    def vocab(self) -> int:
        return self.model.config.vocab_size

    def encode(self, text: str) -> np.ndarray:
        return np.asarray(self.tokenizer.encode(text), dtype=np.int64)

    def decode(self, ids) -> str:
        return self.tokenizer.decode(ids)

    def logits_for(self, input_ids: np.ndarray) -> np.ndarray:
        """Full logits for the LAST position given input_ids. Returns (V,) float64."""
        import torch
        inp = torch.from_numpy(input_ids).unsqueeze(0)
        with torch.no_grad():
            out = self.model(inp)
        return out.logits[0, -1].cpu().numpy().astype(np.float64)

    def embed_phases(self, seed: int = 0) -> np.ndarray:
        """PER-TOKEN phase from the token embedding projected onto a fixed 2-D plane.

        We pick two fixed random D-dim basis vectors (u, v) and project each token's
        embedding onto them:
            phi_i = atan2(W[i] . v, W[i] . u)   in [-pi, pi]

        This gives a NON-constant phase that varies across the vocab by each token's
        embedding direction. target_phase then selects a direction in this plane. The
        plane is arbitrary (a fixed probe), but it is a real, token-varying signal —
        which is what the degenerate constant-phase result proved was necessary.
        """
        rng = np.random.default_rng(seed)
        emb = self.model.get_input_embeddings()
        W = emb.weight.detach().cpu().numpy().astype(np.float64)  # (V, D)
        D = W.shape[1]
        u = rng.normal(size=D); u /= np.linalg.norm(u)
        v = rng.normal(size=D); v -= (v @ u) * u; v /= np.linalg.norm(v)  # orthonormal
        x = W @ u  # (V,)
        y = W @ v  # (V,)
        return np.arctan2(y, x)  # (V,) in [-pi, pi]


def real_trial(*, model_name: str = DEFAULT_MODEL, prompt: str = "",
               n_tokens: int = 40, alpha: float = 0.25, temperature: float = 0.8,
               steer_angle: float = 0.0, seed: int = 0) -> dict[str, Any]:
    """Autoregressive real-model trial: greedy vs phase-controlled.

    phi = PER-TOKEN phase from the token embedding projected onto a 2-D steering
    vector at `steer_angle`. target_phase = steer_angle (pull tokens whose embedding
    direction is near the steer). Measures:
      - KL per step (phase-dist vs softmax) -> must stay low
      - steer_delta: |logp(controlled) - logp(greedy)| under original softmax
        (>0 means the channel actually moved the token; 0 = no-op)
      - repetition (diversity) greedy vs controlled
    """
    # per-token phase from the embedding projected onto a fixed 2-D probe plane;
    # target_phase = steer_angle selects a direction in that plane (pull tokens
    # whose embedding direction is near the steer).
    rl = RealLogits(model_name)
    V = rl.vocab()
    rng = random.Random(seed)
    rl.torch.manual_seed(seed)

    phi = rl.embed_phases(seed=seed)      # (V,) per-token phase, non-constant
    target = steer_angle

    prompt = (prompt or "Once upon a time, the queen of the hidden city").strip()
    ids = rl.encode(prompt).tolist()

    greedy_text, controlled_text = [], []
    kl_s, logprob_controlled, steer_delta = [], [], []
    n_moved = 0

    for _ in range(n_tokens):
        arr = np.asarray(ids, dtype=np.int64)
        logits = rl.logits_for(arr)                 # (V,)
        p = pl.softmax(logits, temperature)
        g = int(np.argmax(logits))

        z = pl.complex_lift(logits, temperature, phi)
        c = pl.phase_collapse(z, mode="aligned_greedy", target_phase=target,
                              alpha=alpha, rng=rng)

        d_phase = pl._distribution(z, "aligned_greedy", target, alpha)
        kl_s.append(pl.kl(d_phase, p))
        lp_c = float(np.log(p[c] + 1e-12)); lp_g = float(np.log(p[g] + 1e-12))
        logprob_controlled.append(lp_c)
        steer_delta.append(abs(lp_c - lp_g))
        if c != g:
            n_moved += 1

        greedy_text.append(rl.decode([g]))
        controlled_text.append(rl.decode([c]))
        ids.append(c)

    greedy_str = "".join(greedy_text); controlled_str = "".join(controlled_text)

    def _repetition(s: str) -> float:
        toks = s.split()
        return 0.0 if not toks else 1.0 - len(set(toks)) / len(toks)

    return {
        "schema": SCHEMA,
        "model": model_name, "prompt": prompt, "n_tokens": n_tokens,
        "alpha": alpha, "temperature": temperature, "steer_angle": round(steer_angle, 3),
        "results": {
            "mean_kl_phase_vs_softmax_nats": round(float(np.mean(kl_s)), 4),
            "mean_logprob_controlled": round(float(np.mean(logprob_controlled)), 4),
            "mean_steer_delta_logprob": round(float(np.mean(steer_delta)), 4),
            "frac_tokens_moved": round(n_moved / n_tokens, 3),
            "repetition_greedy": round(_repetition(greedy_str), 3),
            "repetition_controlled": round(_repetition(controlled_str), 3),
        },
        "greedy_text": greedy_str,
        "controlled_text": controlled_str,
        "note": "Real logits. phi = per-token embedding direction projected onto a "
                "2-D steer vector. frac_tokens_moved > 0 proves the channel operates "
                "on real logits; mean_kl low proves it doesn't destroy the "
                "distribution. steer_delta measures how far it actually moved the "
                "chosen token's log-prob.",
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="phase_lift_real")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--prompt", default="")
    ap.add_argument("--tokens", type=int, default=40)
    ap.add_argument("--alpha", type=float, default=0.25)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--steer", type=float, default=0.0, help="steer angle (radians)")
    a = ap.parse_args(argv)
    print(json.dumps(real_trial(model_name=a.model, prompt=a.prompt,
                                n_tokens=a.tokens, alpha=a.alpha,
                                temperature=a.temperature, steer_angle=a.steer), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
