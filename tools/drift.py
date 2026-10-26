"""drift -- the metric-referent drift instrument (2026-09-18).

Born from METRIC_REFERENT_TRIANGULATION_20260918.md: five fleet documents
(fleet, briefing, chronicle, fold, bibliography) share one armature. Each
measures its RATE OF CHANGE (cheap) and calls that measurement orientation,
while the TRUTH INSTRUMENT that would say whether the movement is in the
right direction sits unbuilt (expensive). The missing quantity in all five
is the same number: corr(delta-M, delta-R), the correlation between the
metric's movement and the referent's movement, over a window where the
metric moved and the referent did or didn't.

This organ computes that number. Verdicts:
  VACUOUS      the referent never moved during the window: the metric is
               measuring nothing that matters (yet)
  ALIGNED      metric and referent move together (corr >= +0.5)
  DRIFTING     weak or no correlation: the metric may have decoupled
  INVERTED     metric rises while referent falls (corr <= -0.5): alarm
  INSUFFICIENT too few deltas to say anything (need >= 3 of each)
  FRAGILE-ALIGNED  not emitted by this module: stamped downstream by
               tools/drift_pairs_stamp.py _apply_aging_guard when an ALIGNED
               verdict's referent is immature (aging guard). It is ALIGNED's
               provisional form, never a sixth classifier output here;
               consumers (drift_dashboard _verdict_color, the board) must
               render it amber-green and treat it as ALIGNED-provisional,
               never as blank/unknown (B2-218 vocabulary sweep 2026-09-26).

Pure computation. Reads nothing, writes nothing. Feed it two series and
honesty comes back.
"""


def _deltas(series):
    return [series[i + 1] - series[i] for i in range(len(series) - 1)]


def _pearson(xs, ys):
    n = len(xs)
    if n < 2 or n != len(ys):
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    return cov / ((vx ** 0.5) * (vy ** 0.5))


def drift_check(metric, referent, window=0, label="") -> dict:
    """Correlate a metric's movement with its referent's movement.

    metric, referent: numeric time series (same length, ordered oldest first).
    window: optional tail restriction (last N deltas). label: free tag.
    """
    metric = [float(x) for x in (metric or [])]
    referent = [float(x) for x in (referent or [])]
    if len(metric) != len(referent) or len(metric) < 2:
        return {"ok": False, "error": "series must be same length, >= 2 points"}
    dm = _deltas(metric)
    dr = _deltas(referent)
    if window and window >= 1:
        dm, dr = dm[-int(window):], dr[-int(window):]
    if len(dm) < 3:
        return {"ok": True, "tool": "drift_check", "label": label,
                "verdict": "INSUFFICIENT", "deltas": len(dm),
                "note": "need >= 3 deltas after windowing"}
    corr = _pearson(dm, dr)
    referent_moved = any(d != 0 for d in dr)
    if not referent_moved:
        verdict = "VACUOUS"
        note = ("referent never moved during the window: the metric is "
                "measuring motion with no measured destination")
    elif corr is None:
        verdict = "DEGENERATE"
        note = "zero variance in one series' deltas"
    elif corr >= 0.5:
        verdict = "ALIGNED"
        note = "metric movement tracks referent movement"
    elif corr <= -0.5:
        verdict = "INVERTED"
        note = "metric rises while referent falls: stop trusting the metric"
    else:
        verdict = "DRIFTING"
        note = "weak coupling: the metric may have decoupled from its referent"
    return {"ok": True, "tool": "drift_check", "label": label,
            "verdict": verdict, "corr_dm_dr": round(corr, 4) if corr is not None else None,
            "deltas_used": len(dm), "metric_moved": any(d != 0 for d in dm),
            "referent_moved": referent_moved, "note": note,
            "law": "a rate metric answers 'is it moving'; only corr(delta-M, "
                   "delta-R) answers 'is it moving north'"}


def drift_check_cmd(metric: str = "", referent: str = "", window: int = 0, label: str = "") -> dict:
    """Comma-separated numeric series version for MCP/CLI callers."""
    try:
        m = [float(x) for x in metric.split(",") if x.strip()]
        r = [float(x) for x in referent.split(",") if x.strip()]
    except ValueError as e:
        return {"ok": False, "error": "parse: " + str(e)}
    return drift_check(m, r, window=window, label=label)
