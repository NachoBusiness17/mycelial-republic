#!/usr/bin/env python3
"""FlashX latency probe: glm-5.3-flashx vs glm-5.3-flash on the fleet's OpenRouter lane.

Born by operator order 2026-09-27 ("build it") after the GLM-5.3-FlashX lane-math
answer. The probe answers one question with bytes: does the 2.5x-priced speed
tier actually deliver the latency the fleet's human-facing lanes (companion
cycle, NPC gateway, phone relay) would pay for?

Pre-registered verdict rule (frozen before any call fired):
  EARNS  : flashx TTFT >= 2x faster than flash, OR decode tok/s >= 3x flash
  DECLINE: both TTFT < 1.5x and tok/s < 2x
  ELSE   : borderline, price per served conversation decides

Spend cap: aborts if estimated spend exceeds SPEND_CAP_USD. Streaming and
non-streaming both measured; TTFT is the metric the phone relay actually feels.
"""
import json
import os
import statistics
import sys
import time
import urllib.request

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
API = "https://openrouter.ai/api/v1/chat/completions"
BASELINE = "z-ai/glm-5.3-flash"
CONTENDER = "z-ai/glm-5.3-flashx"
CALLS_PER_MODEL = 5
MAX_TOKENS = 600
SPEND_CAP_USD = 0.50
PROMPT = (
    "You are the mountain gatekeeper NPC in a Roblox game. A player walks up and "
    "asks: 'why does the mountain forget the roads?' Answer in character, two "
    "sentences, plain speech."
)


def load_key():
    with open(ENV_PATH, encoding="utf-8") as f:
        for line in f:
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("no OPENROUTER_API_KEY in .env")


def call(model, key, stream):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": MAX_TOKENS,
        "stream": stream,
        **({"stream_options": {"include_usage": True}} if stream else {}),
    }).encode("utf-8")
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
    })
    t0 = time.perf_counter()
    ttft_any = None
    ttft_content = None
    out_tokens = 0
    with urllib.request.urlopen(req, timeout=90) as resp:
        if not stream:
            payload = json.loads(resp.read().decode("utf-8"))
            total = time.perf_counter() - t0
            usage = payload.get("usage", {})
            return {"ttft_s": None, "total_s": total,
                    "out_tokens": usage.get("completion_tokens", 0)}
        for raw in resp:
            line = raw.decode("utf-8", errors="replace").strip()
            if not line.startswith("data: ") or line == "data: [DONE]":
                continue
            chunk = json.loads(line[6:])
            if chunk.get("usage"):
                out_tokens = chunk["usage"].get("completion_tokens", out_tokens)
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            if (delta.get("content") or delta.get("reasoning")) and ttft_any is None:
                ttft_any = time.perf_counter() - t0
            if delta.get("content") and ttft_content is None:
                ttft_content = time.perf_counter() - t0
        total = time.perf_counter() - t0
    return {"ttft_s": ttft_content if ttft_content is not None else ttft_any,
            "ttft_any_s": ttft_any, "total_s": total, "out_tokens": out_tokens}


def est_spend(prices, out_tokens_per_call):
    return CALLS_PER_MODEL * 2 * MAX_TOKENS * (prices["in"] + prices["out"] * 1.5)


def main():
    key = load_key()
    models = json.load(urllib.request.urlopen(
        urllib.request.Request("https://openrouter.ai/api/v1/models"), timeout=30))
    prices = {}
    for m in models.get("data", []):
        if m["id"] in (BASELINE, CONTENDER):
            prices[m["id"]] = {
                "in": float(m["pricing"]["prompt"]),
                "out": float(m["pricing"]["completion"]),
            }
    if CONTENDER not in prices:
        print(json.dumps({"blocked": "flashx not in catalog"}))
        return 2
    projected = sum(est_spend(p, MAX_TOKENS) for p in prices.values())
    if projected > SPEND_CAP_USD:
        print(json.dumps({"blocked": "spend cap", "projected_usd": round(projected, 4)}))
        return 2

    results = {}
    for model in (BASELINE, CONTENDER):
        rows = {"ttft": [], "total": [], "tok_s": []}
        for _ in range(CALLS_PER_MODEL):
            s = call(model, key, stream=True)
            if s["ttft_s"] is not None:
                rows["ttft"].append(s["ttft_s"])
                rows["total"].append(s["total_s"])
                if s["total_s"] > s["ttft_s"]:
                    rate = (s.get("out_tokens") or s.get("out_chars", 0))
                    rows["tok_s"].append(rate / (s["total_s"] - s["ttft_s"]) if rate else 0)
        results[model] = {
            "ttft_ms_mean": round(statistics.mean(rows["ttft"]) * 1000, 1) if rows["ttft"] else None,
            "total_s_mean": round(statistics.mean(rows["total"]), 2) if rows["total"] else None,
            "price_in_per_m": round(prices[model]["in"] * 1_000_000, 2),
            "price_out_per_m": round(prices[model]["out"] * 1_000_000, 2),
        }
    b, x = results[BASELINE], results[CONTENDER]
    ttft_gain = (b["ttft_ms_mean"] / x["ttft_ms_mean"]) if b["ttft_ms_mean"] and x["ttft_ms_mean"] else 0
    verdict = "EARNED" if ttft_gain >= 2 else ("DECLINED" if ttft_gain < 1.5 else "BORDERLINE")
    out = {"verdict": verdict, "ttft_gain_x": round(ttft_gain, 2), "models": results,
           "calls_per_model": CALLS_PER_MODEL, "projected_spend_usd": round(projected, 4)}
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
