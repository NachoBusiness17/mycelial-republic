"""geometric_probe - zero-shot geometric probes across catalog models, reality-anchored.

Steal: slashreboot's zero-shot geometric probing (convergent manifolds across LLMs),
twisted estate-way: every probe is anchored to REAL structure (hue order, physical
temperature scale, fixed opposition poles), so cross-model convergence measures
reality-tracking, not inter-model consensus. Open-completion seeds feed
mag/percolator.percolate() (domain = model family) so lineage invariants compile
under the organ's own recurrence + count laws.

ALL network egress is delegated to tools/hermes_burn.py (the sanctioned carrier:
its endpoint fence, retries and usage banking are the boundary organ; this module
holds no sockets). Free lanes only, $0, SENSING surface per the driving ladder.

Consumer: operator (invariant harvest lane, watch/inbox/ORG_SYSTEM_V2_PERCOLATED_20261018.md);
Verifier: --selftest offline vectors + the live run receipt in watch/inbox/.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
STEALTH_FLAG = ROOT / "state" / "stealth_driver.off"

try:
    from mag.percolator import percolate
except Exception:  # noqa: BLE001 - selftest/dry runs run organless
    def percolate(text, source="", domain="general"):
        return {"verdict": "organless"}

WATER_STATE = ROOT / "state" / "probe_water.json"
LOCAL_ROSTER = ["gemma4:latest", "gemma:2b", "qwen2.5:7b-instruct-q8_0",
                "deepseek-r1:1.5b", "athena-class:latest"]

DEFAULT_ROSTER = [
    "poolside/laguna-s-2.1:free",
    "cohere/north-mini-code:free",
    "dots-studio/dots-3-note-preview:free",
    "nvidia/nemotron-3.5-super-vl:free",
    "xingchen-agi/xing4.0-29b-a4b:free",
    "liquid/lfm-2.5-2.6b:free",
]
COLORS = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "magenta"]
HUE_ORDER = COLORS[:]
TEMP_ITEMS = ["ice cube", "fridge interior", "room air", "human body", "fever",
              "candle flame", "stove burner", "sun surface"]
OPPOSITIONS = [("safe", "dangerous"), ("friend", "enemy"), ("light", "dark"),
               ("honest", "deceitful"), ("order", "chaos"), ("warm", "cold"),
               ("alive", "dead"), ("sacred", "profane")]
SEEDS = [
    'Complete this sentence without explanation, one sentence only: "The one thing I always..."',
    'Complete this sentence without explanation, one sentence only: "I never..."',
    'Complete this sentence without explanation, one sentence only: "What I want you to remember about me is..."',
]
COLOR_ASK = ("Place these 8 colors on a circle by assigning each an angle in degrees "
             "(0-360): " + ", ".join(COLORS) + '. Reply ONLY with JSON: '
             '{"red": <deg>, "orange": <deg>, ...} no other text.')
TEMP_ASK = ("Place these on a single number line where larger = hotter, using your choice "
            "of numbers: " + ", ".join(TEMP_ITEMS) + '. Reply ONLY with JSON: '
            '{"ice cube": <num>, ...} no other text.')
OPP_ASK = ("For each pair, assign +1 or -1 to the FIRST word depending on whether it sits "
           "on the positive or negative side of the axis the pair naturally forms: "
           + "; ".join(f"{a}/{b}" for a, b in OPPOSITIONS) + '. Reply ONLY with JSON: '
           '{"safe": 1, "dangerous": -1, ...} no other text.')

_HB = None


def _carrier():
    """Load tools/hermes_burn.py as the boundary organ (its fence, its retries)."""
    global _HB
    if _HB is None:
        os.environ.setdefault("HERMES_BURN_API_BASE",
                              "https://openrouter.ai/api/v1/chat/completions")
        os.environ.setdefault("HERMES_BURN_UNPRICED_OK", "1")
        spec = importlib.util.spec_from_file_location(
            "hermes_burn", ROOT / "tools" / "hermes_burn.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _HB = mod
    return _HB


def ask_local(model: str, prompt: str, timeout: int = 300) -> str:
    """Local ollama via CLI subprocess: no sockets, no rate limit, the shelf runs free."""
    try:
        p = subprocess.run(["ollama", "run", model, prompt], capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
        out = (p.stdout or "").strip()
        return out if out else f"__ERROR__ empty ({(p.stderr or '')[:120]})"
    except Exception as e:  # noqa: BLE001
        return f"__ERROR__ {type(e).__name__}: {e}"


def _env_key() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    return os.environ.get("OPENROUTER_API_KEY", "")


def ask(model: str, prompt: str, key: str, retries: int = 2) -> str:
    hb = _carrier()
    try:
        data = hb._call(model, [{"role": "user", "content": prompt}], 400, key,
                        retries=retries)
        return (data["choices"][0]["message"]["content"] or "")
    except Exception as e:  # noqa: BLE001 - failures are findings, logged not raised
        return f"__ERROR__ {type(e).__name__}: {e}"


def _first_json(text: str) -> dict | None:
    clean = re.sub(r"```(?:json)?", "", text)
    for m in re.finditer(r"\{[^{}]*\}", clean, re.S):
        try:
            v = json.loads(m.group(0))
            if isinstance(v, dict):
                return v
        except json.JSONDecodeError:
            continue
    return None


def color_adjacency(coords: dict) -> float | None:
    """Best-rotation match of the model's angular hue order to the physical wheel."""
    deg = {}
    for c in HUE_ORDER:
        v = coords.get(c)
        if not isinstance(v, (int, float)):
            return None
        deg[c] = float(v) % 360.0
    order = sorted(HUE_ORDER, key=lambda c: deg[c])
    best = 0
    for r in range(len(HUE_ORDER)):
        rot = HUE_ORDER[r:] + HUE_ORDER[:r]
        best = max(best, sum(1 for i in range(len(order)) if order[i] == rot[i]))
    return best / len(HUE_ORDER)


def kendall_tau(xs: list, ys: list) -> float:
    n = len(xs)
    if n < 2:
        return float("nan")
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = (xs[i] - xs[j]) * (ys[i] - ys[j])
            conc += s > 0
            disc += s < 0
    return (conc - disc) / (n * (n - 1) * 0.5)


def temp_tau(nums: dict) -> float | None:
    got, exp = [], []
    for item, want in zip(TEMP_ITEMS, range(8)):
        v = nums.get(item)
        if not isinstance(v, (int, float)):
            return None
        got.append(float(v))
        exp.append(want)
    return kendall_tau(exp, got)


def opposition_sign_rate(vals: dict) -> float | None:
    ok = total = 0
    for a, b in OPPOSITIONS:
        va, vb = vals.get(a), vals.get(b)
        if not isinstance(va, (int, float)) or not isinstance(vb, (int, float)):
            continue
        total += 1
        if va * vb < 0:
            ok += 1
    return ok / total if total else None


def probe_model(model: str, askfn, do_percolate: bool = True) -> dict:
    fam = model.split("/")[0]
    out = {"model": model, "family": fam, "ts": datetime.now(timezone.utc).isoformat()}
    coords = _first_json(askfn(model, COLOR_ASK))
    out["color_adjacency"] = color_adjacency(coords) if coords else None
    time.sleep(2.5)  # free-tier pacing: rapid calls trip per-model RPM
    nums = _first_json(askfn(model, TEMP_ASK))
    out["temp_tau"] = temp_tau(nums) if nums else None
    time.sleep(2.5)
    signs = _first_json(askfn(model, OPP_ASK))
    out["opposition_rate"] = opposition_sign_rate(signs) if signs else None
    seeds = []
    for s in SEEDS:
        time.sleep(2.5)
        txt = askfn(model, s).strip()
        seeds.append(txt[:300])
        if do_percolate and txt and not txt.startswith("__ERROR__"):
            res = percolate(f"{txt}", source=model, domain=f"probe_{fam}")
            if isinstance(res, dict):
                out["percolate_verdict"] = res.get("verdict", "?")
    out["seeds"] = seeds
    return out


def _water_load() -> dict:
    if WATER_STATE.exists():
        return json.loads(WATER_STATE.read_text(encoding="utf-8"))
    spec = {"nodes": {"reservoir": {"volume": 8}}, "pipes": {}, "tick": 0}
    for m in DEFAULT_ROSTER:
        spec["nodes"][m] = {"volume": 1}
        spec["pipes"][f"reservoir->{m.split('/')[0]}"] = {
            "src": "reservoir", "dst": m, "cap": 1}
    return spec


def _water_beat(drip: int = 6, local: bool = True, do_percolate: bool = True,
                out_path: str | None = None) -> list:
    """One live water-computer beat: cron-drip inflow, pipe transfer by cap,
    spend one cycle per model with water, STARVED names the dry. OUT = real
    API calls (the receipt file is the bucket); local models run off-water
    (subprocess ollama, the shelf is unrationed). Engine: mag/water_graph."""
    sys.path.insert(0, str(ROOT))
    from mag.water_graph import WaterGraph, from_spec
    key = _env_key()
    spec = _water_load()
    g = from_spec(spec)
    g.nodes["reservoir"].volume = min(g.nodes["reservoir"].volume + drip, 24)
    events: list[str] = []
    for pname, pipe in g.pipes.items():
        src, dst = g.nodes[pipe.src], g.nodes[pipe.dst]
        move = min(pipe.cap, src.volume, max(0, 4 - dst.volume))
        if move > 0:
            src.volume -= move
            g._receive(dst, move, events)
    g.tick_count += 1
    rows = []
    for mname, node in g.nodes.items():
        if mname == "reservoir":
            continue
        if node.volume < 1:
            rows.append({"model": mname, "starved": True, "ts": g.tick_count})
            continue
        node.volume -= 1
        rows.append(probe_model(mname, lambda mm, p: ask(mm, p, key), do_percolate))
    if local:
        # THE HEADLESS LAW (operator, 2026-10-18): headless work runs during game
        # sessions; only the eye is paused. When stealth_driver.off exists the eye
        # is down - local ollama calls would fail-spawn every beat, so skip them.
        if STEALTH_FLAG.exists():
            rows.append({"model": "local_shelf", "skipped": "eye down (stealth_driver.off)"})
        else:
            for m in LOCAL_ROSTER:
                rows.append(probe_model(m, lambda mm, p: ask_local(mm, p), do_percolate))
    (ROOT / "state").mkdir(exist_ok=True)
    WATER_STATE.write_text(json.dumps(g.to_spec(), indent=1), encoding="utf-8")
    if out_path:
        with open(out_path, "a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row) + "\n")
    glass = {n: g.nodes[n].volume for n in g.nodes}
    print(f"geometric_probe: water beat {g.tick_count} glass={glass} events={events}")
    return rows


def selftest() -> int:
    assert abs(color_adjacency({c: i * 45 for i, c in enumerate(HUE_ORDER)}) - 1.0) < 1e-9
    assert color_adjacency({c: 0 for c in HUE_ORDER}) is not None
    assert abs(temp_tau(dict(zip(TEMP_ITEMS, range(8)))) - 1.0) < 1e-9
    assert abs(temp_tau(dict(zip(TEMP_ITEMS, list(reversed(range(8)))))) + 1.0) < 1e-9
    assert abs(opposition_sign_rate({"safe": 1, "dangerous": -1, "friend": 1, "enemy": -1}) - 1.0) < 1e-9
    assert _first_json('sure! here: {"red": 0} hope that helps') == {"red": 0}
    assert _first_json('```json\n{"red": 10, "orange": 50}\n``` extra {"noise": 1}')["red"] == 10
    assert _first_json("no json here") is None
    print("geometric_probe: selftest ok")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=",".join(DEFAULT_ROSTER),
                    help="comma-separated model ids (:free lanes)")
    ap.add_argument("--out", default=str(ROOT / "watch" / "inbox" / "GEOMETRIC_PROBE_RUN.jsonl"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-percolate", action="store_true")
    ap.add_argument("--water", action="store_true",
                    help="live water-computer beat: state/probe_water.json governs remote spend")
    ap.add_argument("--no-local", action="store_true", help="skip the unrationed local shelf")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    sys.path.insert(0, str(ROOT))
    if args.no_percolate:
        def percolate(text, source="", domain="general"):  # noqa: E306
            return {"verdict": "skipped"}
    else:
        from mag.percolator import percolate  # noqa: F811
    if args.water:
        rows = _water_beat(local=not args.no_local,
                           do_percolate=not args.no_percolate,
                           out_path=str(ROOT / "watch" / "inbox" / "GEOMETRIC_PROBE_RUN.jsonl"))
        ca = [r["color_adjacency"] for r in rows if r.get("color_adjacency") is not None]
        tt = [r["temp_tau"] for r in rows if r.get("temp_tau") is not None]
        starved = sum(1 for r in rows if r.get("starved"))
        print(f"geometric_probe: water ok parsed={len(ca)+len(tt)} color={ca} temp={tt} starved={starved}")
        return 0
    sys.path.insert(0, str(ROOT))
    key = _env_key()
    if not key:
        print("geometric_probe: FAIL no OPENROUTER_API_KEY")
        return 2
    roster = [m.strip() for m in args.models.split(",") if m.strip()]
    print(f"geometric_probe: roster {len(roster)} via hermes_burn carrier", flush=True)
    rows = []
    for i, model in enumerate(roster, 1):
        try:
            rows.append(probe_model(model, lambda mm, p: ask(mm, p, key),
                                    not args.no_percolate))
        except Exception as e:  # noqa: BLE001
            rows.append({"model": model, "error": f"{type(e).__name__}: {e}"})
        print(f"  [{i}/{len(roster)}] {model}", flush=True)
        time.sleep(2)
    with open(args.out, "a", encoding="utf-8") as fh:
        for row in sorted(rows, key=lambda r: r.get("model", "")):
            fh.write(json.dumps(row) + "\n")
    ca = [r["color_adjacency"] for r in rows if r.get("color_adjacency") is not None]
    tt = [r["temp_tau"] for r in rows if r.get("temp_tau") is not None]
    print(f"geometric_probe: ok models={len(ca) + len(tt)} color_mean="
          f"{(sum(ca) / len(ca)):.2f}({len(ca)}) temp_tau_mean="
          f"{(sum(tt) / len(tt)):.2f}({len(tt)}) -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
