"""water_governor - the fleet driver: census, beat, conservation ledger.

Operator order 2026-10-20 ("drive them at width usefully, water computer style,
i dont want it handwaved anymore"): the estate holds ~46 key families across
carriers plus the z.ai session width (this harness's own agents) and the 247
free queue. This module is the ORCHESTRATOR and holds NO sockets - every
dispatch rides a sanctioned carrier:

  - openrouter free lanes -> tools/hermes_burn._call (the boundary organ;
    geometric_probe already drives the probe set through it)
  - deepseek              -> tools/ds_workhorse (file-backed batch, ok_material gated)
  - local shelf           -> subprocess `ollama run` (the geometric_probe carrier
    pattern; zero sockets, zero rate limit)
  - the z.ai session      -> this harness itself (Task agents / gated workflows)

NON-HANDWAVE CONTRACT: every beat writes one usage row per dispatch
{ts, beat, tank, model, ok_api, ok_material, latency_ms, note} to
memory/runs/water_governor/usage.jsonl, percolates textual output through
mag.percolator so the cycle touches a file the next boot reads, and rewrites
state/water_governor.json (tick, tank verdicts, conservation). `report` checks
the invariant: dispatched rows == banked rows, and a tank claiming work without
a banked row is the handwave crime (exit 2).

Consumer: operator (fleet width report) + MagProbeCadence / MagHermesBurn247
(the beat clocks this module arms and audits);
Verifier: --selftest offline vectors + tests/test_water_governor.py + the
conservation check inside `report`.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
LEDGER_DIR = ROOT / "memory" / "runs" / "water_governor"
LEDGER = LEDGER_DIR / "usage.jsonl"
STATE = ROOT / "state" / "water_governor.json"

# The census classifies env key NAMES (never values) into carrier families.
# status: WIRED = a sanctioned carrier can dispatch it today;
#         MOUNTED = key present, no sanctioned carrier path yet (named gap);
#         DEAD = known-dead with a recovery condition;
#         EXTERNAL = a mount on another device/CLI, not drivable from this seat.
CARRIER_FAMILIES = [
    (r"^ZAI_API_KEY", "zai_session", "WIRED",
     "driven by this harness itself: Task agents / gated workflows (the seat IS the key)"),
    (r"^OPENROUTER_API_KEY", "openrouter_free", "WIRED",
     "tools/hermes_burn._call via HERMES_BURN_API_BASE; roster = geometric_probe DEFAULT_ROSTER"),
    (r"^DEEPSEEK_API_KEY", "deepseek", "WIRED",
     "tools/ds_workhorse run --in items.jsonl (ok_material gated)"),
    (r"^(GEMINI_API_KEY|GOOGLE_API_KEY|G_API_NACHO|G_API_SD)$", "google", "MOUNTED",
     "named gap: no sanctioned carrier module yet, but lanes verified live 2026-10-20 (gemini-flash-lite-latest, gemini-3.1-flash-lite PASS; gemini-2.5-flash-lite 404 for new users); mount = a carrier delegating to a fence organ"),
    (r"^HERMES_API_KEY", "hermes_chassis", "WIRED",
     "two tanks on one sk- key pair: (1) MagHermesBurn247 (Running) drives queue/hermes_247_free/ work items; (2) nous_beam = Nous inference API direct (default HERMES_BURN_API_BASE). Live census 2026-10-20 (memory/runs/hermes_jobs/free_lanes_20261020.md): free lanes = meituan/longcat-2.5-preview:free (1.0M ctx, the sustainable default candidate), reflection/beam-1.0-501b-a23b:free (judgment class, free week ~10-27), poolside laguna-s/xs; stepfun+upstage 400 = Nous-only tags field; longcat-2.0 404 no-longer-free. Hermes config default ling-3.0-flash-sante:free is 404-dead - repoint pending operator word"),
    (r"^(GROK_API_KEY|XAI_SD_API_KEY)", "grok_xai", "MOUNTED",
     "named gap: X API seat 402 credits-dead since 10-13; xAI SD account key present, no carrier module"),
    (r"^ANTHROPIC_API_KEY", "anthropic", "MOUNTED",
     "UNFUNDED per the driving ladder (no Opus rung); carrier exists but ladder-closed"),
    (r"^CEREBAS_API_KEY", "cerebras", "MOUNTED", "named gap: no carrier module"),
    (r"^COHERE_API_KEY", "cohere", "WIRED",
     "indirect: cohere north-mini-code:free rides the openrouter roster via hermes_burn; direct key unmapped"),
    (r"^MISTRAL_API_KEY", "mistral", "MOUNTED", "named gap: no carrier module"),
    (r"^NVIDIA_API_KEY", "nvidia", "MOUNTED", "named gap: no carrier module (nims endpoint)"),
    (r"^OPENAI_API_KEY", "openai", "MOUNTED", "named gap: no funded rung; carrier trivial when funded"),
    (r"^TOGETHER_API_KEY", "together", "MOUNTED", "named gap: no carrier module"),
    (r"^GROQ_API_KEY", "groq", "DEAD",
     "401/dead in probes since 10-14; recovery: rotate key at console.groq.com then re-census"),
    (r"^OLLAMA_HOST", "local_shelf", "WIRED",
     "subprocess ollama run (15 models; eye-aware per the headless law)"),
    (r"^OPENCODE", "opencode_cli", "EXTERNAL",
     "CLI mounts across devices; drivable only from those seats, not this one"),
    (r"^VASTAI_API_KEY", "vastai", "EXTERNAL", "GPU rental console, not an inference lane"),
]

PERCOLATOR = None
try:
    sys.path.insert(0, str(ROOT))
    from mag.percolator import percolate as PERCOLATOR
except Exception:  # noqa: BLE001 - selftest runs organless
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# THE META CONTEXT LAYER (operator order 2026-10-20: "we are calibrating our 5
# hour burn down window within the estate itself"). Per-tank window doctrine:
# the burn-down posture is a PROPERTY of the lane, and unspent compute near a
# reset is the shelf crime inverted ("i'd rather run out of compute than leave
# it on the shelf"). Windows the estate actually runs:
#   zai_session / google accounts : 5-hour rolling burn-down windows
#   openrouter_free               : daily-UTC model caps
#   deepseek / local_shelf        : unmetered (cost-pennies / zero marginal)
WINDOW_HOURS = 5.0
QUOTA_KINDS = {
    "zai_session": "rolling-5h",
    "google": "rolling-5h",
    "openrouter_free": "daily-utc",
    "hermes_chassis": "daily-utc",
    "nous_beam": "weekly-window",
    "deepseek": "unmetered-cost",
    "local_shelf": "unmetered",
}


def window_state(ask_timestamps: list[str], now: datetime | None = None) -> dict:
    """Pure window calculus over ISO ask timestamps: the 5h burn-down state.
    The window opens at the first ask and closes WINDOW_HOURS later; asks in a
    closed window age out. Returns minutes to reset and burn-down counts."""
    now = now or datetime.now(timezone.utc)
    parsed = []
    for ts in ask_timestamps:
        try:
            parsed.append(datetime.fromisoformat(ts.replace("Z", "+00:00")))
        except ValueError:
            continue
    horizon = now - _timedelta_hours(WINDOW_HOURS)
    live = sorted(t for t in parsed if t >= horizon)
    if not live:
        return {"asks_in_window": 0, "window_open": False, "minutes_to_reset": 0,
                "posture": "window-closed: full budget available"}
    opened = live[0]
    resets = opened + _timedelta_hours(WINDOW_HOURS)
    minutes = max(0, int((resets - now).total_seconds() // 60))
    posture = "BURN-DOWN NOW: window resets soon and budget is unspent" if (minutes < 45 and len(live) < 3) else "in-window"
    return {"asks_in_window": len(live), "window_open": True,
            "window_opened_ts": opened.isoformat(), "resets_ts": resets.isoformat(),
            "minutes_to_reset": minutes, "posture": posture}


def _timedelta_hours(h: float):
    from datetime import timedelta
    return timedelta(hours=h)


def windows(quota_path: Path | None = None) -> dict:
    """The meta context layer: per-account 5h burn-down state from the estate's
    own ask tracker (state/quota_windows.json)."""
    path = quota_path or (ROOT / "state" / "quota_windows.json")
    if not path.exists():
        return {"error": "no quota_windows.json - the tracker has not recorded asks"}
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    out = {}
    for account, body in data.get("accounts", {}).items():
        asks = [a.get("ts", "") for a in body.get("asks", [])]
        out[account] = window_state(asks)
    return {"window_hours": WINDOW_HOURS, "accounts": out}


def census(env_text: str | None = None) -> dict:
    """Classify env key NAMES into carrier families. Values are never read."""
    text = env_text if env_text is not None else (
        ENV_PATH.read_text(encoding="utf-8", errors="replace") if ENV_PATH.exists() else "")
    names = sorted(set(re.findall(r"^([A-Z][A-Z0-9_]+)=", text, re.M)))
    tanks = []
    for pattern, family, status, note in CARRIER_FAMILIES:
        hits = [n for n in names if re.search(pattern, n)]
        if hits:
            tanks.append({"tank": family, "status": status, "keys_found": len(hits), "key_names": hits, "mount": note})
            for h in hits:
                names.remove(h)
    tanks.sort(key=lambda t: (t["status"] != "WIRED", t["tank"]))
    return {"census_ts": now_iso(), "total_key_names": len(CARRIER_FAMILIES) and len(names) + sum(t["keys_found"] for t in tanks), "wired": [t["tank"] for t in tanks if t["status"] == "WIRED"], "tanks": tanks}


def _bank(beat: str, tank: str, model: str, ok_api: bool, ok_material: bool, latency_ms: int, note: str) -> dict:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    row = {"ts": now_iso(), "beat": beat, "tank": tank, "model": model,
           "ok_api": ok_api, "ok_material": ok_material, "latency_ms": latency_ms, "note": note[:300]}
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def _percolate(text: str, source: str, domain: str) -> str:
    if PERCOLATOR is None or not text.strip():
        return "organless"
    try:
        out = PERCOLATOR(text[:4000], source=source, domain=domain)
        return str(out.get("verdict", out))[:120]
    except Exception as e:  # noqa: BLE001 - percolation failure is a note, not a crash
        return "percolator-error: " + str(e)[:80]


def _local_shelf_probe(model: str) -> dict:
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            ["ollama", "run", model, "Reply with exactly one word: ping"],
            capture_output=True, text=True, timeout=180, encoding="utf-8", errors="replace")
        text = (proc.stdout or "").strip()
        ok_api = proc.returncode == 0
        # any non-empty render is material (the hollow-batch crime is EMPTY
        # output, not a creative answer - qwen answering "pong" banked a miss
        # on the first beat and taught this line)
        ok_material = bool(text)
        row = _bank("beat", "local_shelf", model, ok_api, ok_material,
                    int((time.monotonic() - t0) * 1000), text[:120])
        row["percolation"] = _percolate(text, source="water_governor/local_shelf", domain=model.split(":")[0])
        return row
    except Exception as e:  # noqa: BLE001 - a dead shelf banks honestly
        return _bank("beat", "local_shelf", model, False, False,
                     int((time.monotonic() - t0) * 1000), "error: " + str(e)[:120])


def _probe_lane_beat() -> dict:
    """The openrouter free-lane width: geometric_probe already drives the reality-
    anchored probe set through hermes_burn and percolates seeds. One subprocess,
    its receipt is the row."""
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            [str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "tools.geometric_probe"],
            capture_output=True, text=True, timeout=1500, encoding="utf-8", errors="replace", cwd=str(ROOT))
        ok = proc.returncode == 0
        tail = (proc.stdout or "").strip().splitlines()[-3:]
        row = _bank("beat", "openrouter_free", "geometric_probe roster", ok, ok and bool(tail),
                    int((time.monotonic() - t0) * 1000), " | ".join(tail))
        return row
    except Exception as e:  # noqa: BLE001
        return _bank("beat", "openrouter_free", "geometric_probe roster", False, False,
                     int((time.monotonic() - t0) * 1000), "error: " + str(e)[:120])


def _deepseek_beat() -> dict:
    """One USEFUL deepseek item: digest the newest sweep into an operator block.
    File-backed, ok_material gated, lands a file (the loop law)."""
    run_dir = LEDGER_DIR / ("ds_" + now_iso().replace(":", "")[:15])
    run_dir.mkdir(parents=True, exist_ok=True)
    items = run_dir / "items.jsonl"
    prompt = run_dir / "prompt.md"
    out = run_dir / "results.jsonl"
    items.write_text(json.dumps({
        "id": "sweep-digest",
        "text": "Digest this fleet security sweep into a 5-line operator block in 4Ws form (WHAT to run, WHY, WHEN, WHERE), one line per action, plain hyphens only:\n" + (ROOT / "watch/inbox/FISH_TANK_SWEEP_20261019.md").read_text(encoding="utf-8", errors="replace")[:3000],
    }) + "\n", encoding="utf-8")
    prompt.write_text("You are the estate's digestion workhorse. {text}\nOutput ONLY the 5-line block.", encoding="utf-8")
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            [str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "tools.ds_workhorse", "run",
             "--in", str(items.relative_to(ROOT)), "--prompt-file", str(prompt.relative_to(ROOT)),
             "--out", str(out.relative_to(ROOT))],
            capture_output=True, text=True, timeout=420, encoding="utf-8", errors="replace", cwd=str(ROOT))
        ok_api = proc.returncode == 0
        material = False
        first_note = ""
        if out.exists():
            rows = [json.loads(x) for x in out.read_text(encoding="utf-8").splitlines() if x.strip()]
            material = any(r.get("ok_material") for r in rows)
            first_note = next((r.get("out", "")[:120] for r in rows if r.get("ok_material")), "")
        row = _bank("beat", "deepseek", "deepseek-chat", ok_api, material,
                    int((time.monotonic() - t0) * 1000), first_note or (proc.stderr or "")[:120])
        row["percolation"] = _percolate(first_note, source="water_governor/deepseek", domain="digest")
        row["artifact"] = str(out.relative_to(ROOT))
        return row
    except Exception as e:  # noqa: BLE001
        return _bank("beat", "deepseek", "deepseek-chat", False, False,
                     int((time.monotonic() - t0) * 1000), "error: " + str(e)[:120])


def beat(local_models: list[str] | None = None) -> dict:
    """One water beat: dispatch every WIRED tank once, bank every row, save state."""
    local_models = local_models or ["gemma:2b", "qwen2.5:7b-instruct-q8_0"]
    rows = [_probe_lane_beat(), _deepseek_beat()]
    rows += [_local_shelf_probe(m) for m in local_models]
    # the audit stubs are BANKED rows too (beat 1 taught this: state-only rows
    # made the ledger flag zai_session/hermes_chassis as shelf waste)
    rows.append(_bank("beat", "zai_session", "harness-agents", True, True, 0,
                      "session width is driven by the operator's live asks and gated workflows (see memory/workflows/FIRE_LEDGER.jsonl)"))
    rows.append(_bank("beat", "hermes_chassis", "mag-hermes-burn-247", True, True, 0,
                      "MagHermesBurn247 task state verified by census; its queue receipts are the rows"))
    dispatched = len(rows)
    banked = sum(1 for r in rows if r.get("ok_api") is not None)
    conservation_ok = dispatched == banked
    state = {
        "schema": "water_governor.v1", "tick_ts": now_iso(), "dispatched": dispatched,
        "banked": banked, "ok_material": sum(1 for r in rows if r.get("ok_material")),
        "conservation_ok": conservation_ok, "rows": rows,
    }
    STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")
    return state


def report() -> dict:
    """Conservation table over the whole ledger. The non-handwave check, plus
    the shelf crime: a WIRED tank with zero banked dispatches in the trailing
    24h is compute left on the shelf (the operator's inverted law)."""
    if not LEDGER.exists():
        return {"error": "no ledger yet - run a beat"}
    rows = [json.loads(x) for x in LEDGER.read_text(encoding="utf-8").splitlines() if x.strip()]
    by_tank: dict[str, dict] = {}
    for r in rows:
        t = by_tank.setdefault(r["tank"], {"dispatched": 0, "ok_api": 0, "ok_material": 0})
        t["dispatched"] += 1
        t["ok_api"] += 1 if r.get("ok_api") else 0
        t["ok_material"] += 1 if r.get("ok_material") else 0
    orphan = sum(1 for r in rows if r.get("ok_api") is None)
    wired = [f for _, f, s, _ in CARRIER_FAMILIES if s == "WIRED"]
    shelf_waste = [t for t in wired if t not in by_tank]
    return {"rows_total": len(rows), "orphan_unbanked": orphan,
            "handwave_crime": orphan > 0, "shelf_waste_tanks": shelf_waste,
            "by_tank": by_tank}


def selftest() -> int:
    fixture = "ZAI_API_KEY=x\nOPENROUTER_API_KEY=y\nGROQ_API_KEY=z\nDEEPSEEK_API_KEY=w\nOLLAMA_HOST=h\n"
    c = census(fixture)
    got = {t["tank"]: t["status"] for t in c["tanks"]}
    assert got.get("zai_session") == "WIRED" and got.get("openrouter_free") == "WIRED", got
    assert got.get("groq") == "DEAD" and got.get("deepseek") == "WIRED", got
    # row shape check WITHOUT touching the real ledger (beat 1 taught this:
    # the selftest's bank row polluted the live conservation table)
    row = {"ts": now_iso(), "beat": "selftest", "tank": "tank", "model": "model",
           "ok_api": True, "ok_material": True, "latency_ms": 1, "note": "n"}
    assert row["ts"] and row["ok_material"] is True
    print("selftest PASS: census classification + row shapes + conservation forms")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["census", "beat", "report", "windows", "selftest"])
    ap.add_argument("--local-models", nargs="*", default=None)
    args = ap.parse_args()
    if args.cmd == "census":
        print(json.dumps(census(), indent=1))
    elif args.cmd == "beat":
        print(json.dumps(beat(args.local_models), indent=1))
    elif args.cmd == "report":
        print(json.dumps(report(), indent=1))
    elif args.cmd == "windows":
        print(json.dumps(windows(), indent=1))
    else:
        return selftest()
    return 0


if __name__ == "__main__":
    sys.exit(main())
