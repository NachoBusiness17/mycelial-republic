"""THE 50 - W5 T23: Mr Pool reaction signatures.

Called-shot posts vs faded posts, reaction deltas, honest n per bucket.

Buckets (message level, from watch/inbox/mrpool_export/):
  called   : msg carries at least one dated call row in
             called_shot_ledger_captions.jsonl (v2) or called_shot_ledger.jsonl (v1).
  faded    : every other msg in ledger_full.jsonl (no filed call on this day).
  matched  : faded msgs within +/-45 days of a called msg (controls audience drift).

Metrics per bucket: n, views, forwards, reactions (total/organic/paid),
reactions per 1K views (rpv), emoji rates per 1K views, media mix.
Deltas: raw called-faded, time-matched pooled, and paired (called msg vs
median of its own 45-day faded controls). Permutation p-values, seed 50.

Run: .venv/Scripts/python.exe scripts/the50_t23_reaction_sigs.py
Out: memory/runs/the50/w5_t23_reaction_sigs.json
Stdlib only, deterministic.
"""
import json
import os
import random
import re
import statistics
from collections import defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(ROOT, "watch", "inbox", "mrpool_export")
OUT = os.path.join(ROOT, "memory", "runs", "the50", "w5_t23_reaction_sigs.json")
AS_OF = date(2026, 9, 19)          # T12 used the same as-of date for expiry
MATCH_DAYS = 45
PERMS = 20000
SEED = 50
R4 = lambda x: round(x, 4) if isinstance(x, float) else x


def load(name):
    with open(os.path.join(EXP, name), encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def d(s):
    y, m, dd = s[:10].split("-")
    return date(int(y), int(m), int(dd))


def reactions_of(row):
    out = {"total": 0, "paid": 0, "organic": 0, "mix": defaultdict(int)}
    for x in row.get("reactions") or []:
        n = x["n"]
        out["total"] += n
        if x["e"] == "ReactionPaid()":
            out["paid"] += n
        else:
            out["organic"] += n
            out["mix"][x["e"]] += n
    return out


def med(xs):
    return statistics.median(xs) if xs else None


def bucket_stats(rows, label):
    views = [r["_views"] for r in rows if r["_views"] is not None]
    vw = [v for v in views if v > 0]
    fwd = [r["_fwd"] for r in rows]
    tot = [r["_react"]["total"] for r in rows]
    org = [r["_react"]["organic"] for r in rows]
    paid = [r["_react"]["paid"] for r in rows]
    rpv = [r["_rpv"] for r in rows if r["_rpv"] is not None]
    orpv = [r["_orpv"] for r in rows if r["_orpv"] is not None]
    view_sum = sum(views)
    mix = defaultdict(int)
    for r in rows:
        for e, n in r["_react"]["mix"].items():
            mix[e] += n
    media = defaultdict(int)
    for r in rows:
        media[r.get("media_type") or "none"] += 1
    return {
        "bucket": label,
        "n_msgs": len(rows),
        "n_with_views_field": len(views),
        "n_views_gt0": len(vw),
        "n_no_views": len(rows) - len(views),
        "views_median": med(views),
        "views_mean": R4(statistics.fmean(views)) if views else None,
        "views_sum": view_sum,
        "forwards_median": med(fwd),
        "forwards_sum": sum(fwd),
        "reactions_total_median": med(tot),
        "reactions_total_sum": sum(tot),
        "reactions_organic_median": med(org),
        "reactions_organic_sum": sum(org),
        "reactions_paid_sum": sum(paid),
        "n_msgs_with_paid": sum(1 for p in paid if p > 0),
        "rpv_per_1k_median": R4(med(rpv)) if rpv else None,
        "rpv_per_1k_mean": R4(statistics.fmean(rpv)) if rpv else None,
        "organic_rpv_per_1k_median": R4(med(orpv)) if orpv else None,
        "replies_median": med([r.get("replies_count") or 0 for r in rows]),
        "n_replies_gt0": sum(1 for r in rows if (r.get("replies_count") or 0) > 0),
        "media_mix": dict(sorted(media.items(), key=lambda kv: -kv[1])),
        "emoji_share_of_organic": {
            e: R4(n / sum(mix.values())) for e, n in
            sorted(mix.items(), key=lambda kv: -kv[1])[:10]
        } if mix else {},
    }


def perm_diff_median(a, b, perms=PERMS, seed=SEED):
    """Two-sided permutation p for diff of medians, pooled labels."""
    rng = random.Random(seed)
    pool = list(a) + list(b)
    na = len(a)
    obs = statistics.median(a) - statistics.median(b)
    hits = 0
    for _ in range(perms):
        rng.shuffle(pool)
        da = statistics.median(pool[:na])
        db = statistics.median(pool[na:])
        if abs(da - db) >= abs(obs) - 1e-12:
            hits += 1
    return obs, hits / perms


def main():
    full = load("ledger_full.jsonl")
    cap = load("called_shot_ledger_captions.jsonl")
    v1 = load("called_shot_ledger.jsonl")

    # called set: union of v2 caption msg_ids and v1 msg_file ids
    call_ids = {r["msg_id"] for r in cap}
    for r in v1:
        m = re.match(r"msg_(\d+)", r.get("msg_file") or "")
        if m:
            call_ids.add(int(m.group(1)))
    targets = defaultdict(set)
    for r in cap:
        targets[r["msg_id"]].add(r["target_date"])
    for r in v1:
        m = re.match(r"msg_(\d+)", r.get("msg_file") or "")
        if m and r.get("target_date"):
            targets[int(m.group(1))].add(r["target_date"])

    for r in full:
        r["_views"] = r.get("views")
        r["_fwd"] = r.get("forwards") or 0
        r["_react"] = reactions_of(r)
        v = r["_views"]
        t = r["_react"]["total"]
        r["_rpv"] = (t / v * 1000.0) if v else None
        o = r["_react"]["organic"]
        r["_orpv"] = (o / v * 1000.0) if v else None

    called = [r for r in full if r["msg_id"] in call_ids]
    faded = [r for r in full if r["msg_id"] not in call_ids]

    called_exp, called_open = [], []
    for r in called:
        tgts = targets[r["msg_id"]]
        (called_open if any(d(t) >= AS_OF for t in tgts) else called_exp).append(r)

    # time-matched controls: faded msgs within +/-MATCH_DAYS of some called msg
    call_dates = [d(r["date"]) for r in called]
    matched, pairs = [], []
    for r in faded:
        dd = d(r["date"])
        if any(abs((dd - c).days) <= MATCH_DAYS for c in call_dates):
            matched.append(r)
    by_day = defaultdict(list)
    for r in faded:
        by_day[d(r["date"])].append(r)
    for r in called:
        dd = d(r["date"])
        ctrl = []
        for off in range(-MATCH_DAYS, MATCH_DAYS + 1):
            ctrl.extend(by_day.get(dd.fromordinal(dd.toordinal() + off), []))
        ctrl = [c for c in ctrl if c["_rpv"] is not None]
        if ctrl and r["_rpv"] is not None:
            pairs.append(r["_rpv"] - statistics.median([c["_rpv"] for c in ctrl]))

    obs_raw, p_raw = perm_diff_median(
        [r["_rpv"] for r in called if r["_rpv"] is not None],
        [r["_rpv"] for r in faded if r["_rpv"] is not None])
    obs_pair, p_pair = None, None
    if pairs:
        rng = random.Random(SEED)
        obs_pair = statistics.median(pairs)
        hits = 0
        for _ in range(PERMS):
            flips = [x if rng.random() < 0.5 else -x for x in pairs]
            if abs(statistics.median(flips)) >= abs(obs_pair) - 1e-12:
                hits += 1
        p_pair = hits / PERMS

    # emoji signature: organic reactions per 1K views, called vs matched faded
    top = defaultdict(int)
    for r in full:
        for e, n in r["_react"]["mix"].items():
            top[e] += n
    top_emojis = [e for e, _ in sorted(top.items(), key=lambda kv: -kv[1])[:12]]

    def emoji_rates(rows):
        vs = sum(r["_views"] or 0 for r in rows)
        agg = defaultdict(int)
        for r in rows:
            for e, n in r["_react"]["mix"].items():
                agg[e] += n
        return {e: R4(agg.get(e, 0) / vs * 1000.0) if vs else None for e in top_emojis}

    er_called = emoji_rates(called)
    er_matched = emoji_rates(matched)
    signature = []
    for e in top_emojis:
        c, m = er_called[e], er_matched[e]
        signature.append({
            "emoji": e,
            "called_per_1k_views": c,
            "faded_matched_per_1k_views": m,
            "ratio_called_over_matched": R4(c / m) if (c is not None and m) else None,
        })
    signature.sort(key=lambda s: -(s["ratio_called_over_matched"] or 0))

    art = {
        "task": "THE 50 W5 T23 Mr Pool reaction signatures",
        "as_of": AS_OF.isoformat(),
        "question": "do called-shot posts pull a different audience reaction than posts with no call on file (faded posts)?",
        "inputs": {
            "ledger_full.jsonl": {"rows": len(full), "span": [min(r["date"] for r in full)[:10], max(r["date"] for r in full)[:10]]},
            "called_shot_ledger_captions.jsonl": {"rows": len(cap), "uniq_msg_ids": len({r["msg_id"] for r in cap})},
            "called_shot_ledger.jsonl (v1)": {"rows": len(v1), "adds_msg_ids": sorted(call_ids - {r["msg_id"] for r in cap})},
        },
        "definitions": {
            "called": "msg carries at least one dated call row (v2 captions ledger, plus v1 msg 3091); n=%d msgs" % len(called),
            "faded": "no filed call row for that msg; 'faded' = no call on file, not proof no call was made; n=%d msgs" % len(faded),
            "expired_open": "msg-level: OPEN if any of its call targets is >= as-of date, else EXPIRED; expiry is not a verdict, only v1 Med Bed rows carry filed verdicts (ALL BROKEN per CALLED_SHOT_VERDICT.json)",
            "matched": "faded msgs within +/-45 days of some called msg (audience-size control)",
            "rpv": "reactions per 1,000 views (organic_rpv excludes ReactionPaid tips)",
        },
        "buckets": {
            "called": bucket_stats(called, "called"),
            "called_expired_targets": bucket_stats(called_exp, "called_expired_targets"),
            "called_open_targets": bucket_stats(called_open, "called_open_targets"),
            "faded": bucket_stats(faded, "faded"),
            "faded_time_matched": bucket_stats(matched, "faded_time_matched"),
        },
        "deltas": {
            "raw_called_vs_faded": {
                "rpv_median_called": R4(med([r["_rpv"] for r in called if r["_rpv"] is not None])),
                "rpv_median_faded": R4(med([r["_rpv"] for r in faded if r["_rpv"] is not None])),
                "diff": R4(obs_raw),
                "perm_p_two_sided": p_raw,
                "perms": PERMS,
                "confound": "called posts cluster in 2024-2026 when the channel was bigger; raw delta is age-confounded",
            },
            "matched_called_vs_faded": {
                "n_matched_faded": len(matched),
                "rpv_median_matched_faded": R4(med([r["_rpv"] for r in matched if r["_rpv"] is not None])),
                "paired_msgs": len(pairs),
                "paired_median_delta_rpv": R4(obs_pair) if obs_pair is not None else None,
                "paired_below_zero_frac": R4(sum(1 for x in pairs if x < 0) / len(pairs)) if pairs else None,
                "signflip_perm_p_two_sided": p_pair,
            },
        },
        "emoji_signature": {
            "note": "organic reactions per 1K views; ratio >1 means the emoji is more characteristic of called posts",
            "rates_vs_time_matched_faded": signature,
        },
        "honest_n": {
            "called_msgs": len(called),
            "called_expired_target_msgs": len(called_exp),
            "called_open_target_msgs": len(called_open),
            "faded_msgs": len(faded),
            "faded_time_matched_msgs": len(matched),
            "paired_msgs": len(pairs),
            "msgs_without_views_field": [r["msg_id"] for r in full if r["_views"] is None],
            "msgs_with_reactions": sum(1 for r in full if r["_react"]["total"] > 0),
            "album_member_msgs_grouped_true": sum(1 for r in full if r.get("grouped")),
            "msgs_with_any_reply": sum(1 for r in full if (r.get("replies_count") or 0) > 0),
        },
        "caveats": [
            "'faded' is operationalized as no filed call row; the caption ledger was built by caption/date scans and may miss implicit calls",
            "reaction and view counts are Telegram display values at scrape time (2026-09-18); recent posts have not finished accruing",
            "expiry of a target date is not an adjudicated BROKEN verdict for v2 rows; only the v1 Med Bed campaign carries filed verdicts (ALL BROKEN)",
            "album members (grouped=true) share one album; views/reactions are per-message as scraped, so albums weigh more than once",
            "media mix differs by bucket (see media_mix); photo-vs-video reaction behavior is a known confound not adjusted here",
            "permutation p-values are Monte Carlo (seed %d, %d draws); with n_called=%d the smallest two-sided p is coarse" % (SEED, PERMS, len(called)),
        ],
        "provenance": {
            "script": "scripts/the50_t23_reaction_sigs.py",
            "run": ".venv/Scripts/python.exe scripts/the50_t23_reaction_sigs.py",
            "stdlib_only": True,
            "seed": SEED,
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(art, f, indent=1, ensure_ascii=False)
    print("wrote", OUT)
    for k in ("called", "faded", "faded_time_matched"):
        b = art["buckets"][k]
        print(k, "n=%d rpv_med=%s fwd_med=%s react_med=%s" % (
            b["n_msgs"], b["rpv_per_1k_median"], b["forwards_median"], b["reactions_total_median"]))
    print("paired delta", art["deltas"]["matched_called_vs_faded"])
    print("top signature:", signature[:3])


if __name__ == "__main__":
    main()
