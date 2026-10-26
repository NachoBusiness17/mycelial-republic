"""ESTATE SMITH CHART — health as |Gamma| coordinates, not prose.

Law (self-steal, 2026-09-21, from the pseudospectrum/Smith-chart wave):
  A system whose eigenvalues look healthy but whose response to a unit
  perturbation is enormous is NON-NORMAL and sick. Prose status answers are
  reflections: |Gamma| -> 1 means all power bounced, none delivered.
  Bar: |Gamma| > 0.5 => the organ may NOT be answered with prose; it gets a fix.

Gamma = 1 - delivered/claimed per organ, computed from bytes on disk.
Every organ names its source file. An organ with no machine-readable source
is DARK (listed, unmetered) — a dark meter is itself a finding.

Usage (from repo root): .venv/Scripts/python.exe tools/estate_smith_chart.py [--no-plot]
Outputs: watch/inbox/ESTATE_SMITH_CHART_<date>.json (+ .png unless --no-plot)
"""

import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y%m%d")
BAR = 0.5  # the prose/fix bar, pre-stated

ROOT = Path.cwd().resolve()
OUT_DIR = (ROOT / "watch" / "inbox").resolve()
LOG_DIR = (ROOT / "logs").resolve()
sys.path.insert(0, str(ROOT))  # allow `from mag...` imports when run from tools/


def inbox_path(suffix):
    """Output path, resolved and confined to watch/inbox."""
    p = (OUT_DIR / ("ESTATE_SMITH_CHART_" + STAMP + suffix)).resolve()
    if not p.is_relative_to(OUT_DIR):
        raise ValueError("output path escapes watch/inbox")
    return p


def read_jsonl_tail(path, n):
    rows = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(line)
    except FileNotFoundError:
        return []
    return rows[-n:]


def organ_lanes():
    """Provider lanes from logs/provider_usage.jsonl: last 30 calls each."""
    src = "logs/provider_usage.jsonl"
    rows = read_jsonl_tail(LOG_DIR / "provider_usage.jsonl", 3000)
    by_prov = defaultdict(list)
    for r in rows:
        try:
            e = json.loads(r)
            by_prov[e.get("provider")].append(e)
        except Exception:
            continue
    out = {}
    for prov in ("z_ai3", "deepseek", "ollama"):
        recent = by_prov.get(prov, [])[-30:]
        if not recent:
            out[prov] = {"gamma": None, "status": "DARK", "n": 0, "src": src}
            continue
        oks = sum(1 for e in recent if e.get("ok"))
        last = recent[-1]
        gamma = round(1.0 - oks / len(recent), 3)
        entry = {"gamma": gamma, "ok_ratio": round(oks / len(recent), 3),
                 "n": len(recent), "last_ts": last.get("ts", ""),
                 "last_ok": last.get("ok"), "src": src}
        if prov == "ollama" and gamma == 1.0:
            entry["status"] = "EXEMPT"  # family-box law: local inference is
            # night-window only; day-dark by law is not sickness.
        else:
            entry["status"] = "REFLECTING" if gamma > BAR else "DELIVERING"
        out[prov] = entry
    return out


def organ_supervisor():
    """Fraction of recent supervisor events that are errors (2h window).

    Time-boxed 2026-09-22: a count-based tail let an ended error storm
    (container-era reaper spam) hold Gamma at 1.00 for hours after the
    last real error. Health is now, not history.
    """
    src = "logs/supervisor.jsonl (last 120 min)"
    rows = read_jsonl_tail(LOG_DIR / "supervisor.jsonl", 400)
    if not rows:
        return {"gamma": None, "status": "DARK", "src": src}
    cutoff = NOW.timestamp() - 120 * 60
    err = ok = 0
    old = 0
    errs = defaultdict(int)
    for r in rows:
        try:
            e = json.loads(r)
        except Exception:
            continue
        try:
            ts = datetime.fromisoformat(str(e.get("ts", "")).replace("Z", "+00:00")).timestamp()
        except Exception:
            ts = None
        if ts is not None and ts < cutoff:
            old += 1
            continue
        if "error" in str(e.get("event", "")) or "error" in e:
            err += 1
            errs[str(e.get("event", "?"))] += 1
        else:
            ok += 1
    if err + ok == 0:
        return {"gamma": 0.0, "status": "DELIVERING", "ok": 0, "err": 0,
                "note": f"no supervisor events in window ({old} rows older)", "src": src}
    gamma = round(err / max(1, err + ok), 3)
    return {"gamma": gamma, "err": err, "ok": ok, "top_errors": dict(errs),
            "status": "REFLECTING" if gamma > BAR else "DELIVERING", "src": src}


def organ_queue():
    """The running slot: stale log while status=running => zombie => Gamma 1."""
    src = "mag.orchestrator.queue_status + logs/orchestrator/<id>.out.log"
    try:
        from mag.orchestrator import queue_status
        qs = queue_status()
    except Exception as e:
        return {"gamma": None, "status": "DARK", "src": src, "error": str(e)[:120]}
    counts = qs.get("counts", {})
    rid = qs.get("running_task_id")
    zombie = None
    if rid:
        log = LOG_DIR / "orchestrator" / (str(rid) + ".out.log")
        if log.exists():
            age_min = (NOW.timestamp() - log.stat().st_mtime) / 60.0
            zombie = {"task": rid, "log_age_min": round(age_min, 1),
                      "zombie": age_min > 30}
        else:
            zombie = {"task": rid, "log_age_min": None, "zombie": True}
    g = 0.0
    if zombie and zombie.get("zombie"):
        g = 1.0
    return {"gamma": g, "counts": counts, "running": zombie,
            "failed": counts.get("failed", 0),
            "status": "REFLECTING" if g > BAR else "DELIVERING", "src": src}


def organ_day_work():
    """Stalled share in the last day_work mirror line."""
    src = "logs/lane_scheduler.log"
    rows = read_jsonl_tail(LOG_DIR / "lane_scheduler.log", 200)
    line = None
    for r in reversed(rows):
        if "lane=day_work" in r:
            line = r.strip()
            break
    if not line:
        return {"gamma": None, "status": "DARK", "src": src}
    stalled = 0
    for tok in line.split():
        if tok.startswith("stalled="):
            try:
                stalled = int(tok.split("=")[1])
            except ValueError:
                stalled = 0
    gamma = round(stalled / (stalled + 1), 3)  # +1: the mirror pass itself
    return {"gamma": gamma, "stalled": stalled, "line": line,
            "status": "REFLECTING" if gamma > BAR else "DELIVERING", "src": src}


def organ_handoffs():
    """Pending peer handoffs. Bar pre-stated: >10 pending = queue rot."""
    src = "mag.peer_handoff.list_peer_handoffs"
    try:
        from mag.peer_handoff import list_peer_handoffs
        ph = list_peer_handoffs(limit=50)
        pending = [h for h in ph if h.get("status") != "done"]
        n = len(pending)
    except Exception as e:
        return {"gamma": None, "status": "DARK", "src": src, "error": str(e)[:120]}
    gamma = round(min(1.0, n / 10.0), 3)
    return {"gamma": gamma, "pending_n": n,
            "status": "REFLECTING" if gamma > BAR else "DELIVERING", "src": src}


def organ_checkpoints():
    """Deliberate-ask plumbing: tasks looping on 'checkpoint (apply)'.

    Law 4: a meter with no evidence is DARK, never DELIVERING — gamma=0 on
    zero logs was the meter lying about organs it had never seen (seed
    audit 09-25). DELIVERING requires logs in-window showing no loops.
    """
    src = "logs/orchestrator/*.out.log (last 24h)"
    odir = LOG_DIR / "orchestrator"
    logs = []
    if odir.is_dir():
        for fn in odir.iterdir():
            if fn.suffix != ".log" or not fn.name.endswith(".out.log"):
                continue
            if not fn.is_relative_to(LOG_DIR):
                continue
            logs.append(fn)
    loop = []
    in_window = 0
    for fn in logs:
        age_h = (NOW.timestamp() - fn.stat().st_mtime) / 3600.0
        if age_h > 24:
            continue
        in_window += 1
        try:
            txt = fn.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        n = txt.count("checkpoint (apply)")
        if n >= 10:
            loop.append({"task": fn.name.replace(".out.log", ""),
                         "checkpoint_lines": n, "age_h": round(age_h, 1)})
    if in_window == 0:
        return {"gamma": None, "looping": [], "status": "DARK", "src": src}
    gamma = 1.0 if loop else 0.0
    return {"gamma": gamma, "looping": loop,
            "status": "REFLECTING" if gamma > BAR else "DELIVERING", "src": src}


def main():
    lanes = organ_lanes()
    organs = {
        "supervisor": organ_supervisor(),
        "flash_lane_zai3": lanes["z_ai3"],
        "deepseek_lane": lanes["deepseek"],
        "ollama_lane": lanes["ollama"],
        "queue": organ_queue(),
        "day_work": organ_day_work(),
        "handoffs": organ_handoffs(),
        "checkpoint_apply": organ_checkpoints(),
    }
    dark = [k for k, v in organs.items() if v.get("gamma") is None]
    exempt = [k for k, v in organs.items() if v.get("status") == "EXEMPT"]
    prose_bar_violations = [k for k, v in organs.items()
                            if v.get("gamma") is not None
                            and v["gamma"] > BAR and v.get("status") != "EXEMPT"]

    result = {
        "schema": "estate.smith_chart.v1",
        "ts": NOW.isoformat(),
        "bar": BAR,
        "law": "gamma = 1 - delivered/claimed from bytes; |gamma| > 0.5 => "
               "no prose answers, fixes only",
        "organs": organs,
        "dark": dark,
        "exempt": exempt,
        "prose_bar_violations": prose_bar_violations,
        "non_normality_note": "eigenvalue view (config/enabled/armed) is in "
                              "each organ's own status field; the transient "
                              "view is gamma — a non-normal system reads "
                              "healthy by spectrum and dies by transient",
    }
    out_json = inbox_path(".json")
    out_json.write_text(json.dumps(result, indent=2), encoding="utf-8")

    if "--no-plot" not in sys.argv:
        plot(inbox_path(".png"), organs, dark, exempt, prose_bar_violations)

    # console = the meter reading, not prose
    print("ESTATE SMITH CHART " + NOW.isoformat() + "  bar=" + str(BAR))
    for k, v in organs.items():
        g = v.get("gamma")
        gs = "DARK" if g is None else "Gamma=%.2f" % g
        print("  %-18s %-12s %s" % (k, gs, v.get("status", "")))
    print("  DARK unmetered: " + str(dark or "none"))
    print("  EXEMPT by law:  " + str(exempt or "none"))
    print("  NO-PROSE LIST:  " + str(prose_bar_violations or "none"))
    print("  wrote " + str(out_json))


SECTORS = {
    "supervisor": 90,
    "flash_lane_zai3": 150,
    "deepseek_lane": 30,
    "ollama_lane": 180,
    "queue": 270,
    "day_work": 240,
    "handoffs": 300,
    "checkpoint_apply": 0,
}


def plot(png, organs, dark, exempt, violations):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 8))
    ax.set_aspect("equal")
    ax.axis("off")
    for r, lbl, style in ((1.0, "|Gamma|=1 total reflection", "-"),
                          (0.75, "0.75", ":"),
                          (0.5, "0.5 PROSE/FIX BAR", "--"),
                          (0.25, "0.25", ":")):
        ring = plt.Circle((0, 0), r, fill=False, ls=style,
                          color="#c0392b" if r == 0.5 else "#888",
                          lw=2.2 if r == 0.5 else 1.0)
        ax.add_patch(ring)
        ax.text(0.02, r + 0.02, lbl, fontsize=7.5,
                color="#c0392b" if r == 0.5 else "#666")
    ax.add_patch(plt.Circle((0, 0), 0.015, color="green"))
    ax.text(0.02, -0.06, "center: matched, delivering", fontsize=7.5,
            color="green")

    for name, ang in SECTORS.items():
        v = organs.get(name, {})
        g = v.get("gamma")
        a = math.radians(ang)
        if g is None:  # dark: plotted on the rim in gray-X, unmetered
            x, y = math.cos(a), math.sin(a)
            ax.plot([x], [y], "x", color="#555", ms=9, mew=2)
            ax.text(x * 1.12, y * 1.12, name + "\nDARK", fontsize=8,
                    ha="center", va="center", color="#555")
            continue
        x, y = g * math.cos(a), g * math.sin(a)
        if v.get("status") == "EXEMPT":
            ax.plot([x], [y], "o", mfc="white", mec="#2980b9", ms=8, mew=1.6)
            lbl = name + "\nEXEMPT (night law)"
        else:
            bad = g > BAR
            ax.plot([x], [y], "o", color="#c0392b" if bad else "#27ae60", ms=8)
            lbl = name + "\n|G|=%.2f" % g
        ax.annotate(lbl, (x, y), xytext=(x * 1.25, y * 1.25), fontsize=8,
                    ha="center", va="center",
                    color="#c0392b" if (g > BAR and v.get("status") != "EXEMPT")
                    else "#333")

    lines = ["UNMETERED (dark = sickness):"]
    lines += ["  - " + d for d in dark] or ["  - none"]
    lines += ["", "EXEMPT by law:"]
    lines += ["  - " + e for e in exempt] or ["  - none"]
    lines += ["", "NO-PROSE LIST (fixes only):"]
    lines += ["  - " + v for v in violations] or ["  - none"]
    fig.text(0.02, 0.02, "\n".join(lines), fontsize=8, family="monospace",
             va="bottom", bbox=dict(boxstyle="round", fc="#f7f7f7", ec="#bbb"))
    fig.suptitle("ESTATE SMITH CHART — health as |Gamma|, not prose",
                 fontsize=13, y=0.98)
    fig.text(0.5, 0.935, NOW.isoformat() + "  ·  sources: logs/*.jsonl, "
             "logs/*.log, mag.orchestrator, mag.peer_handoff",
             ha="center", fontsize=8, color="#666")
    fig.subplots_adjust(left=0.0, right=0.72, top=0.9, bottom=0.02)
    fig.savefig(png, dpi=140)
    print("  wrote " + str(png))


if __name__ == "__main__":
    main()
