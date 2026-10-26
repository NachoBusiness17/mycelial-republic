"""concept_predictor tests — AF1 smoke laws + AH16 grouped-split laws
(2026-09-30).

1. extraction: jsonl -> events (ts sort, canonical-less rows dropped,
   source normalization, hour buckets, lane-bearing subsequence).
2. window construction: count formula, contents, target strictly after
   context (no peeking).
3. baseline sanity: bigram train accuracy >= max unigram frequency on its
   own training set (mathematically guaranteed: per-key max share dominates
   the global argmax share when averaged over the keys' own rows),
   == 1.0 on deterministic transitions, top-3 pads from the unigram
   ranking without duplicates, candidate filtering holds.
4. end-to-end small slice (chrono): featurize + tiny numpy MLP on a
   learnable 3-cycle, loss falls, holdout top-1 well above chance.
5. AH16 grouped split: chrono mask reproduces the AF1 event-index cut;
   grouped mask holds a seeded round(15%) of recurring key-groups across
   their FULL timeline (scattered indices, not a tail), is deterministic,
   and rejects a held_override naming non-recurring groups.
6. no-peeking featurizer fit: fit_event_mask covers exactly context+target
   events of train windows (chrono reduces to events[:cut]; an event seen
   only inside holdout windows is never fitted on).
7. end-to-end grouped cell: recurring canons nameable on BOTH sides
   (train vocab + in-vocab holdout truths), unseen-key baseline falls to
   unigram (exactly 0.0 in the built chain), verdict wiring decided by
   the reported numbers. NOT asserted: a winning MLP — key-side grouping
   leaves the held canon's last-slot column untrained by construction, so
   transfer across the held key is the experiment, not a test law.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.concept_predictor import (FrequencyPredictor,  # noqa: E402
                                     SequenceFeaturizer, chrono_train_mask,
                                     fit_event_mask, grouped_train_mask,
                                     hour_bucket, lane_bearing, load_events,
                                     make_windows, mlp_topk_accuracy,
                                     normalize_source, run_cell, train_mlp)


def _ts(hours: float) -> str:
    base = datetime(2026, 9, 30, tzinfo=timezone.utc)
    return (base + timedelta(hours=hours)).isoformat().replace("+00:00", "Z")


def _row(ts_hours: float, canonical: str, source: str, lane: str | None,
         domain: str = "d1") -> dict:
    return {"ts": _ts(ts_hours), "source": source, "domain": domain,
            "canonical": canonical, "lane": lane}


def _ev(i: int, n_cycle: int = 3) -> dict:
    return {"ts": _ts(i * 2.0), "source": "s1", "domain": "d1",
            "canonical": f"c{'ABC'[i % n_cycle]}",
            "lane": ["groq", "nvidia"][i % 2], "hour": hour_bucket(_ts(i * 2.0))}


# ------------------------------------------------------------ extraction ----
def test_load_events_sorts_drops_and_normalizes(tmp_path: Path) -> None:
    p = tmp_path / "mini.jsonl"
    lines = [
        _row(6.0, "c1", "ox:t0042", "ox", domain="ox_artifact"),
        _row(1.0, "c2", "fuel:abcd1234", None, domain="fuel_feed"),
        {"ts": _ts(3.0), "source": "x", "domain": "ops"},  # no canonical
    ]
    p.write_text("\n".join(json.dumps(r) for r in lines), encoding="utf-8")
    events = load_events(p)
    assert [e["canonical"] for e in events] == ["c2", "c1"]  # ts sort
    assert [e["source"] for e in events] == ["fuel", "ox"]
    assert events[0]["lane"] == ""            # null lane -> empty string
    assert [e["hour"] for e in events] == [0, 2]  # 1h->0, 6h->2 of 8 buckets
    assert [e["canonical"] for e in lane_bearing(events)] == ["c1"]

    assert normalize_source("fuel:deadbeef") == "fuel"
    assert normalize_source("OX_RESIDENT_res-1-x") == "ox_resident"
    assert normalize_source("moderation:zai") == "moderation"
    assert normalize_source("") == "unknown"
    assert normalize_source(None) == "unknown"


# -------------------------------------------------------------- windows ------
def test_make_windows_shape_and_no_peeking() -> None:
    events = [_ev(i) for i in range(6)]
    k = 2
    wins = make_windows(events, k)
    assert len(wins) == len(events) - k
    ctx, tgt = wins[0]
    assert [e["canonical"] for e in ctx] == ["cA", "cB"]
    assert tgt["canonical"] == "cC"
    for ctx, tgt in wins:  # target never inside its own context
        assert all(c["ts"] < tgt["ts"] for c in ctx)


# ------------------------------------------------------------- baseline -----
def test_baseline_deterministic_transitions_score_1() -> None:
    pairs = [("a", "x")] * 10 + [("b", "y")] * 10
    base = FrequencyPredictor().fit(pairs)
    assert base.accuracy(pairs, 1) == 1.0
    assert base.topk("a", 1) == ["x"]


def test_baseline_at_least_max_unigram_frequency() -> None:
    # mixed transitions: bigram must tie-or-beat the unigram floor on the
    # very data it was fit on (mission's baseline sanity law).
    pairs = ([("a", "x")] * 6 + [("a", "y")] * 4
             + [("b", "y")] * 5 + [("b", "x")] * 1)
    uni_floor = max(Counter(t for _k, t in pairs).values()) / len(pairs)
    base = FrequencyPredictor().fit(pairs)
    assert base.accuracy(pairs, 1) >= uni_floor - 1e-9
    # a seeded random reshuffle must obey the same law
    rng = np.random.default_rng(7)
    keys = [f"k{i % 5}" for i in range(400)]
    tgts = [f"t{rng.integers(0, 4)}" for _ in range(400)]
    pairs2 = list(zip(keys, tgts))
    floor2 = max(Counter(t for _k, t in pairs2).values()) / len(pairs2)
    base2 = FrequencyPredictor().fit(pairs2)
    assert base2.accuracy(pairs2, 1) >= floor2 - 1e-9


def test_baseline_topk_padding_and_candidates() -> None:
    pairs = ([("a", "x")] * 3 + [("b", "y")] * 2 + [("b", "z")] * 1)
    base = FrequencyPredictor().fit(pairs)
    assert base.topk("a", 3) == ["x", "y", "z"]  # bigram x, unigram pad y,z
    assert len(set(base.topk("a", 3))) == 3
    assert base.topk("never-seen", 2) == ["x", "y"]  # unigram backoff
    assert base.topk("a", 3, candidates={"y", "z"}) == ["y", "z"]


# ------------------------------------------------------------ end to end ----
def test_model_end_to_end_on_small_slice() -> None:
    events = [_ev(i) for i in range(72)]
    k, split = 4, int(72 * 0.85)
    fe = SequenceFeaturizer(src_top=8, canon_top=8).fit(events[:split])
    wins = make_windows(events, k)
    X = fe.transform(wins, k)
    assert X.shape == (len(events) - k, k * fe.slot + 8)
    # each event slot lights exactly 4 one-hots (src|domain|canonical|lane)
    # plus exactly 1 hour bucket per window
    np.testing.assert_allclose(X.sum(axis=1), 4 * k + 1)

    vocab = ["cA", "cB", "cC"]
    y_idx = {t: i for i, t in enumerate(vocab)}
    train_rows = list(range(split - k))
    Xtr = X[train_rows]
    ytr = np.array([y_idx[wins[i][1]["canonical"]] for i in train_rows],
                   dtype=np.int64)
    params, losses = train_mlp(Xtr, ytr, len(vocab), hidden=[16, 8],
                               epochs=60, lr=2e-3, batch=16, seed=13)
    assert losses[-1] < losses[0] and np.isfinite(losses[-1])
    assert mlp_topk_accuracy(params, Xtr, ytr, 1) >= 0.9  # cycle is easy

    ho = list(range(split - k, len(wins)))
    yho = np.array([y_idx[wins[i][1]["canonical"]] for i in ho],
                   dtype=np.int64)
    top1 = mlp_topk_accuracy(params, X[ho], yho, 1)
    top3 = mlp_topk_accuracy(params, X[ho], yho, 3)
    assert top1 >= 0.7          # chance is 1/3
    assert top3 >= top1


# ------------------------------------------------------- AH16 split laws ----
def _ns(**over) -> argparse.Namespace:
    base = dict(k=4, holdout=0.15, seed=13, group_min_count=2, src_top=8,
                canon_feat_top=8, hidden="32,16", epochs=60, lr=2e-3,
                batch=16, l2=1e-4, canon_min_count=2)
    base.update(over)
    return argparse.Namespace(**base)


def _chain_events(states: list[str], domain_of: dict[str, str],
                  ) -> list[dict]:
    return [{"ts": _ts(i * 2.0), "source": "s1",
             "domain": domain_of[s], "canonical": s, "lane": "groq",
             "hour": hour_bucket(_ts(i * 2.0))}
            for i, s in enumerate(states)]


def test_chrono_mask_reproduces_af1_cut() -> None:
    events = [_ev(i) for i in range(40)]
    k, holdout = 4, 0.15
    mask, meta = chrono_train_mask(events, len(events) - k, k, holdout)
    cut = int(len(events) * (1 - holdout))
    assert meta["cut_event_index"] == cut
    assert mask == [(k + i) < cut for i in range(len(events) - k)]
    assert not mask[-1] and mask[0]              # tail held out
    covered = fit_event_mask(len(events),
                             [i for i, m in enumerate(mask) if m], k)
    assert covered.tolist() == [True] * cut + [False] * (len(events) - cut)


def test_grouped_split_membership_and_determinism() -> None:
    # rec x3, rec2 x2, singletons x1: recurring keys are {rec, rec2}
    states = (["rec"] * 3 + ["rec2"] * 2 + ["s1", "s2", "rec", "s3",
                                            "rec2", "rec"])
    events = _chain_events(states, {s: "d" for s in set(states)})
    k = 2
    wins = make_windows(events, k)
    keys = [c[-1]["canonical"] for c, _t in wins]

    mask, meta = grouped_train_mask(wins, "canonical", 0.5, seed=13,
                                    group_min=2, held_override=None)
    # 50% of 2 recurring groups, round -> 1 held (>=1 floor)
    assert meta["n_recurring_groups"] == 2
    assert len(meta["held_groups"]) == 1
    held = meta["held_groups"][0]
    assert mask == [kk != held for kk in keys]   # full timeline, scattered
    assert sum(mask) == len([kk for kk in keys if kk != held])

    mask2, meta2 = grouped_train_mask(wins, "canonical", 0.5, seed=13,
                                      group_min=2, held_override=None)
    assert (mask2, meta2) == (mask, meta)        # seeded determinism

    # held_override naming non-recurring (or unknown) groups must fail
    # loud, never silently hold nothing and report UNSCORABLE
    for bad in ({"s1"}, {"rec", "nope"}):
        try:
            grouped_train_mask(wins, "canonical", 0.15, seed=13,
                               group_min=2, held_override=bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"held_override {bad} must raise")


def test_fit_event_mask_no_peeking_grouped() -> None:
    # n0 H1 X H2 n4 n5 with H1, X, H2 held: windows touching X are all
    # holdout, so X is never a fitted event; H2 reappears inside a train
    # window's context (w3 covers events 3..5), so H2 IS covered.
    states = ["n0", "H1", "X", "H2", "n4", "n5"]
    events = _chain_events(states, {s: "d" for s in states})
    k = 2
    wins = make_windows(events, k)
    mask, _ = grouped_train_mask(wins, "canonical", 0.9, seed=13,
                                 group_min=1,
                                 held_override={"H1", "X", "H2"})
    train_idx = [i for i, m in enumerate(mask) if m]
    assert train_idx == [3]                     # only w3 (key n4) is train
    covered = fit_event_mask(len(events), train_idx, k)
    # window i covers event indices i..k+i: w3 covers 3,4,5
    assert covered.tolist() == [False, False, False, True, True, True]
    canon_seen = {events[j]["canonical"] for j in range(len(events))
                  if covered[j]}
    assert "X" not in canon_seen                # no peeking at held X
    assert "H2" in canon_seen                   # ctx of a train window


def test_grouped_cell_answerable_and_transfers() -> None:
    # alpha-domain chain: A->B, A2->B, B->{D,A2}, D->{D,A}. D self-loops to
    # dominance so the unigram top (D) is never a holdout truth — the
    # baseline, falling back to unigram on the unseen key A, scores 0.0
    # exactly. Holding A's windows keeps every recurring canon nameable on
    # BOTH sides (B stays a train class via A2->B; A stays one via D->A).
    # The test asserts the AH16 protocol contract — answerability, parity
    # numbers, verdict wiring — NOT a winning outcome: key-side grouping
    # leaves the held canon's last-slot column untrained by construction,
    # so whether the MLP transfers across it is the experiment, not a law.
    rng = np.random.default_rng(5)
    trans = {"A": [("B", 1.0)], "A2": [("B", 1.0)],
             "B": [("D", 0.5), ("A2", 0.5)],
             "D": [("D", 0.85), ("A", 0.15)]}
    states, cur = [], "A"
    for _ in range(400):
        states.append(cur)
        r, acc = rng.random(), 0.0
        for nxt, p in trans[cur]:
            acc += p
            if r <= acc:
                cur = nxt
                break
    domain = {"A": "alpha", "A2": "alpha", "B": "beta", "D": "beta"}
    events = _chain_events(states, domain)

    args = _ns(k=4, epochs=80, hidden="48,24", lr=2e-3, batch=16)
    res = run_cell("next-canonical-grouped", events, "canonical", 2,
                   "grouped", args, held_override={"A"})
    assert res["held_groups"] == ["A"]
    # answerability: recurring canons nameable on BOTH sides
    assert {"A", "A2", "B", "D"} <= set(res["vocab"])
    assert res["n_scored"] > 0 and res["n_in_vocab"] == res["n_scored"]
    # unseen-key baseline falls to unigram whose top (D) is never the
    # holdout truth (always B after A): exactly zero
    assert res["base_top1"] == 0.0
    assert res["mlp_top1"] == res["mlp_top1"] and res["mlp_top1"] >= 0.0
    # verdict wiring: the reported numbers decide the reported verdict
    m1, b1 = res["mlp_top1"], res["base_top1"]
    expected = ("MLP BEATS baseline" if m1 > b1 else
                "FALSIFIER FIRES: MLP loses to baseline" if m1 < b1 else
                "TIE")
    assert res["verdict"] == expected
