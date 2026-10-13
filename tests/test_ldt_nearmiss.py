"""ldt_nearmiss tests — IMP9 laws (Mickey17 W3K lane, 2026-09-30).

1. Flip law: every generated pair's original verdict is legal_gain and its
   twin verdict is the family's illegal_* — verified with the PROPAGATOR
   (the generator itself already refuses unflipped pairs; the test re-derives
   from the raw graphs so a broken verifier cannot self-certify).
2. Engine agreement: label_sample (the REAL engine) agrees with the
   propagator on both sides of every sampled pair — the generator cannot
   drift from the engine it is adversarial FOR.
3. Render-diff minimality: the dry twin's token render differs from the
   original's in exactly one atom (v:k -> v:0 at the target position); the
   pipe-rename twin touches only p: identity atoms; the node-rename twin
   only n: identity and edge-endpoint atoms. Every non-identity field
   (k:/z:/v:/s:/sill:/c:/sip:/o:/cr:/pr:) survives the renames untouched —
   the near-miss is a hole, not a different board.
4. Graph shape: renames preserve node/pipe insertion order and every
   non-renamed field byte-for-byte; no twin name collides with an existing
   node/pipe.
5. Determinism: same seed -> byte-identical pair list; families all filled.
6. Featurizer OOV law: after fitting on the standard train split, no *_twin
   atom is in the state vocabulary — the twin's hole is dropped, exactly the
   flat-render baseline's honest behavior.
7. Projection pin: on twin rows the feasible set is the family's illegal
   singleton, so evaluate_lattice (renorm) answers the twin correctly at
   confidence exactly 1.0 — the by-construction cure the experiment names a
   proof, not a measurement.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.ldt_lattice import LABELS, evaluate_lattice, feasible_set  # noqa: E402
from tools.ldt_nearmiss import (FAMILIES, TWIN_SUFFIX, build_twin,  # noqa: E402
                                generate_pairs, make_pair)
from tools.ldt_train import load_jsonl  # noqa: E402
from tools.legality_dataset import label_sample, render_tokens  # noqa: E402
from tools.legality_propagator import propagate  # noqa: E402

_WANT = {"dry_pool": "illegal_dry_pool",
         "unknown_target_node": "illegal_unknown_target",
         "unknown_target_pipe": "illegal_unknown_target"}


def _pairs(per_family: int = 12, seed: int = 99) -> list[dict]:
    return generate_pairs(per_family, seed)


_ID_PREFIXES = ("n:", "p:")


def _identity_atom(tok: str) -> bool:
    return tok.startswith(_ID_PREFIXES)


def test_flip_law_and_engine_agreement() -> None:
    pairs = _pairs()
    assert len(pairs) == 12 * len(FAMILIES)
    for p in pairs:
        fam = p["family"]
        # original: propagator re-derived from raw graph == legal_gain
        o = propagate(p["orig"]["graph"], p["verb"], p["target"])
        assert o["label"] == "legal_gain", (p["id"], o)
        # twin: propagator == the family's illegal label == the stored label
        t = propagate(p["twin"]["graph"], p["verb"], p["target"])
        assert t["label"] == _WANT[fam] == p["twin"]["label"], (p["id"], t)
        # engine agrees on BOTH sides (the agreement law)
        oe = label_sample(p["orig"]["graph"], p["verb"], p["target"])
        te = label_sample(p["twin"]["graph"], p["verb"], p["target"])
        assert oe["label"] == "legal_gain" and te["label"] == _WANT[fam]


def _state_atoms(tokens: list[str]) -> list[str]:
    """Markers, action atoms and the label token dropped: the diff test
    compares the STATE render only (action atoms are identical by
    construction; the label is the target, not an input)."""
    drop = {"[STATE]", "[ACTION]", "[LABEL]", "legal_gain",
            "legal_no_gain"} | {f"illegal_{r}" for r in
                                ("unknown_verb", "unknown_target", "dry_pool")}
    return [t for t in tokens if t not in drop]


def test_render_diff_minimality() -> None:
    for p in _pairs():
        fam, tgt = p["family"], p["target"]
        o = _state_atoms(p["orig"]["tokens"])
        t = _state_atoms(p["twin"]["tokens"])
        assert len(o) == len(t)
        if fam == "dry_pool":
            # exactly one atom changed: the target's v:k -> v:0 … except the
            # label token pair (dropped above) nothing else may differ
            diff = [(a, b) for a, b in zip(o, t) if a != b]
            assert diff == [(f"v:{p['orig']['graph']['nodes'][tgt]['volume']}",
                             "v:0")], diff
        elif fam == "unknown_target_pipe":
            for a, b in zip(o, t):
                if a != b:
                    assert a.startswith("p:") and b.startswith("p:"), (a, b)
                    assert b == f"p:{tgt}{TWIN_SUFFIX}"
        else:  # node rename: only n: atoms and src>dst edge atoms change
            for a, b in zip(o, t):
                if a != b:
                    assert a.startswith("n:") or ">" in a, (a, b)
                    assert tgt in a and f"{tgt}{TWIN_SUFFIX}" in b


def test_rename_preserves_shape_and_order() -> None:
    for p in _pairs():
        if p["family"] == "dry_pool":
            continue
        og, tg = p["orig"]["graph"], p["twin"]["graph"]
        tgt = p["target"]
        if p["family"] == "unknown_target_pipe":
            assert list(tg["pipes"]) == [n + TWIN_SUFFIX if n == tgt else n
                                         for n in og["pipes"]]
            for n in og["pipes"]:
                n2 = n + TWIN_SUFFIX if n == tgt else n
                assert tg["pipes"][n2] == og["pipes"][n]
        else:
            assert list(tg["nodes"]) == [n + TWIN_SUFFIX if n == tgt else n
                                         for n in og["nodes"]]
            for n in og["nodes"]:
                n2 = n + TWIN_SUFFIX if n == tgt else n
                assert tg["nodes"][n2] == og["nodes"][n]
            for n, pp in og["pipes"].items():
                expected = dict(pp)
                if pp["src"] == tgt:
                    expected["src"] += TWIN_SUFFIX
                if pp["dst"] == tgt:
                    expected["dst"] += TWIN_SUFFIX
                assert tg["pipes"][n] == expected
        # no collision: the twin name is new
        assert f"{tgt}{TWIN_SUFFIX}" not in og["pipes"]
        if p["family"] == "unknown_target_pipe":
            assert tgt not in tg["pipes"]


def test_determinism_and_families() -> None:
    a, b = generate_pairs(4, seed=7), generate_pairs(4, seed=7)
    assert a == b
    fams = {p["family"] for p in a}
    assert fams == set(FAMILIES)


def test_featurizer_oov_law() -> None:
    ds = ROOT / "logs" / "legality_ds" / "train.jsonl"
    if not ds.exists():
        return  # dataset not built in this checkout — generator laws above
                # still pin the contract; skip rather than fabricate a fit
    from tools.ldt_train import Featurizer
    fe = Featurizer().fit(load_jsonl(ds))
    for p in _pairs(4):
        if p["family"] == "dry_pool":
            continue
        tgt = p["target"]
        assert f"n:{tgt}{TWIN_SUFFIX}" not in fe.state_vocab
        assert f"p:{tgt}{TWIN_SUFFIX}" not in fe.state_vocab


def test_projection_pin_on_twins() -> None:
    """Twin feasible set is the illegal singleton: renorm answers correctly
    at confidence exactly 1.0 (the proof-by-construction arm), strict never
    answers outside F."""
    pairs = _pairs(8)
    twin_rows = [p["twin"] for p in pairs]
    feas = [feasible_set(r["graph"], r["verb"], r["target"])
            for r in twin_rows]
    y = np.array([LABELS.index(r["label"]) for r in twin_rows])
    for f in feas:
        assert len(f) == 1 and "illegal_" in next(iter(f))
    # synthetic probs: the model votes overwhelmingly WRONG (legal_gain)
    probs = np.full((len(y), len(LABELS)), 0.05)
    for i in range(len(y)):
        probs[i, LABELS.index("legal_gain")] = 0.80
    ren = evaluate_lattice(probs, feas, y, threshold=0.7, mode="renorm")
    strict = evaluate_lattice(probs, feas, y, threshold=0.7, mode="strict")
    assert ren["answered"] == len(y) and ren["answered_wrong"] == 0
    assert ren["soundness"] == 1.0
    assert strict["answered_infeasible"] == 0
    # strict pays the coverage cost: 0.15 masked mass < tau -> abstain
    assert strict["answered"] == 0


def test_build_twin_roundtrip_labels() -> None:
    import random
    rng = random.Random(5)
    made = 0
    while made < 6:
        p = make_pair(rng, FAMILIES[made % len(FAMILIES)])
        if p is None:
            continue
        # rebuild the twin from the ORIGINAL graph via build_twin -> the
        # same stored twin graph (builder is a pure function of spec+target)
        twin_spec, want = build_twin(p["orig"]["graph"], p["target"],
                                     p["family"])
        assert twin_spec == p["twin"]["graph"]
        assert propagate(twin_spec, p["verb"], p["target"])["label"] == want
        made += 1
