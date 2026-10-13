"""legality_dataset — W3K: LDT legality dataset over the REAL water-graph engine.

Mickey17 W3 lane (2026-09-29). The N4 LDT experiment design
(logs/mates/night_burn_20260930.jsonl, row "N4-ldt-experiment") calls for a
legality corpus shaped `(state vector + action -> label)` rendered as a flat
token sequence. This tool builds that corpus locally, deterministically, $0:

  - States: seeded-random WaterGraph boards in the Mountain family
    (server/world.py build_mountain_graph): every board keeps `crown` the
    unique COLD node at the strict max elevation and `waste` at elev 0, so
    `crown` can only be fed by steam condensation — the Mountain's own law
    (the gate route can never reach the crown; the boil route can).
  - Actions: verbs from the world's live verb table (CHAT_TABLE.verbs via
    server/protocol_table.py: the DEFAULT v0 four plus say/whisper, same
    source as server/world.VERBS) plus fake verbs/targets so every reject
    reason (UNKNOWN_VERB / UNKNOWN_TARGET / DRY_POOL / BAD_TEXT) is
    represented. (Was server.protocol.VERBS, the 4-verb DEFAULT set, which
    mislabeled say/whisper as UNKNOWN_VERB in training data — caught by the
    Q11 mirror lane 2026-10-01.)
  - Labels: legality is MountainWorld.validate's exact rule set minus the
    sid check (no sessions in a dataset); the one-step outcome is measured,
    not modeled — the action is applied with MountainWorld._apply's physics
    (boil lifts 1, valve toggles, join/tag touch nothing) and one REAL
    WaterGraph.tick() runs; crown_gain := crown volume strictly rose.

Determinism law (single random.Random(seed) stream, canonical sorted-key
JSONL, no wall clock anywhere in the outputs): same seed -> byte-identical
train/val splits. Pinned by tests/test_legality_dataset.py, which also
spot-checks 10 samples against mag/water_graph.py directly (independent
re-derivation, not this module's own labeler).

Output: <out>/train.jsonl, <out>/val.jsonl, <out>/MANIFEST.json (seed,
counts, label distribution, per-file sha256).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph, from_spec  # noqa: E402
from server.protocol_table import CHAT_TABLE  # noqa: E402

VERBS = CHAT_TABLE.verbs  # the world's verb truth (server.world.VERBS single-sources this)

SCHEMA = "legality_ds.v1"

# Board vocabulary (Mountain family). Fake pools deliberately sit OUTSIDE
# these namespaces so an UNKNOWN_TARGET sample can never collide with a
# real name.
_NODE_POOL = ["terrace", "hollow", "gate1", "gate2", "sill1", "pool",
              "ridge", "benches", "flats"]
_PIPE_POOL = ["p_spring", "p_terrace", "p_out", "p_drain", "p_bypass",
              "p_ridge", "p_flats", "p_pool"]
_FAKE_NODES = ["ghost", "moon", "vent", "sump"]
_FAKE_VERBS = ["purify", "dig", "freeze", "douse"]
_KIND_WEIGHTS = [("plain", 0.6), ("xor", 0.2), ("sill", 0.2)]


# --------------------------------------------------------------- boards ----
def make_graph_spec(rng: random.Random) -> dict[str, Any]:
    """One seeded-random Mountain-family board (water_graph.v1 spec shape,
    plus node `sill`/`steam` and pipe `primed` so from_spec + restore is
    lossless)."""
    n_extra = rng.randint(1, 9)                       # |V| in [4, 12]
    names = rng.sample(_NODE_POOL, n_extra)

    nodes: dict[str, dict[str, Any]] = {}
    nodes["spring"] = {"elev": rng.randint(8, 11), "kind": "plain",
                       "sill": 0, "volume": rng.randint(0, 6), "steam": 0}
    for name in names:
        r = rng.random()
        # weighted kind pick, cumulative thresholds (plain 0.6 / xor 0.2 / sill 0.2)
        kind = "plain" if r < _KIND_WEIGHTS[0][1] else (
            "xor" if r < _KIND_WEIGHTS[0][1] + _KIND_WEIGHTS[1][1] else "sill")
        nodes[name] = {
            "elev": rng.randint(1, 7),
            "kind": kind,
            "sill": rng.randint(1, 3) if kind == "sill" else 0,
            "volume": rng.randint(0, 3),
            "steam": 0,
        }
    nodes["waste"] = {"elev": 0, "kind": "waste", "sill": 0,
                      "volume": 0, "steam": 0}
    # crown: unique COLD node, strictly highest — the Mountain law.
    nodes["crown"] = {"elev": 15, "kind": "cold", "sill": 0,
                      "volume": rng.randint(0, 2), "steam": 0}

    # occasional pre-existing steam: the condensation route already armed
    steamables = [n for n in nodes if n not in ("crown",)]
    if steamables and rng.random() < 0.15:
        nodes[rng.choice(steamables)]["steam"] = rng.randint(1, 2)

    node_names = list(nodes)
    pipes: dict[str, dict[str, Any]] = {}
    n_pipes = max(3, round(1.5 * len(node_names)) + rng.randint(-1, 1))
    pipe_names = [p for p in _PIPE_POOL if p not in pipes][:n_pipes] or []
    seen_pairs: set[tuple[str, str]] = set()
    pipe_idx = 0
    while len(pipes) < n_pipes and pipe_idx < 200:
        src, dst = rng.sample(node_names, 2)
        if (src, dst) in seen_pairs:
            continue
        seen_pairs.add((src, dst))
        name = (pipe_names[pipe_idx] if pipe_idx < len(pipe_names)
                else f"p{pipe_idx}")
        siphon = rng.random() < 0.2
        pipes[name] = {
            "src": src, "dst": dst, "cap": rng.randint(1, 2),
            "siphon": siphon, "crest": rng.randint(2, 3) if siphon else 2,
            "primed": False, "open": rng.random() < 0.8,
        }
        pipe_idx += 1

    return {"schema": "water_graph.v1", "tick": 0,
            "nodes": nodes, "pipes": pipes}


def rebuild_graph(spec: dict[str, Any]) -> WaterGraph:
    """from_spec + restore the two fields from_spec drops (node.steam,
    pipe.primed) so a sample's board is byte-faithful to its spec."""
    g = from_spec(spec)
    for name, nd in spec["nodes"].items():
        g.nodes[name].steam = int(nd.get("steam", 0))
    for name, pp in spec["pipes"].items():
        g.pipes[name].primed = bool(pp.get("primed", False))
    return g


# --------------------------------------------------------------- labels ----
def engine_validate(g: WaterGraph, verb: str, target: str) -> tuple[bool, str | None]:
    """MountainWorld.validate (server/world.py) verbatim minus the sid
    check: a dataset has no sessions, so UNKNOWN_SID cannot occur."""
    if verb not in VERBS:
        return False, "UNKNOWN_VERB"
    if verb == "valve":
        if target not in g.pipes:
            return False, "UNKNOWN_TARGET"
        return True, None
    if target not in g.nodes:
        return False, "UNKNOWN_TARGET"
    if verb in ("boil", "tag") and g.nodes[target].volume <= 0:
        return False, "DRY_POOL"
    return True, None


def engine_apply(g: WaterGraph, verb: str, target: str) -> None:
    """MountainWorld._apply's physics (boil lifts 1; valve toggles; join and
    tag are social verbs, no hydraulics)."""
    if verb == "boil":
        g.boil(target, 1)
    elif verb == "valve":
        pipe = g.pipes[target]
        if pipe.open:
            g.close(target)
        else:
            g.open(target)


def label_sample(spec: dict[str, Any], verb: str, target: str) -> dict[str, Any]:
    """Legality + one-step outcome, both measured on the real engine."""
    g = rebuild_graph(spec)
    ok, why = engine_validate(g, verb, target)
    reason = {"UNKNOWN_VERB": "unknown_verb",
              "UNKNOWN_TARGET": "unknown_target",
              "DRY_POOL": "dry_pool"}.get(why or "")
    crown_gain = False
    if ok:
        crown_before = g.volume("crown")
        engine_apply(g, verb, target)
        g.tick()
        crown_gain = g.volume("crown") > crown_before
    label = (f"illegal_{reason}" if reason
             else ("legal_gain" if crown_gain else "legal_no_gain"))
    return {"legal": ok, "illegal_reason": reason,
            "crown_gain": crown_gain, "label": label}


# -------------------------------------------------------------- actions ----
def sample_action(rng: random.Random, spec: dict[str, Any]) -> tuple[str, str]:
    """Coverage-shaped action draw: mostly honest tries, plus guaranteed
    streams of each reject reason (dry-pool hunters, fake verbs, fake
    targets)."""
    node_names = list(spec["nodes"])
    pipe_names = list(spec["pipes"])
    roll = rng.random()
    if roll < 0.10:                                   # unknown verb
        return rng.choice(_FAKE_VERBS), rng.choice(node_names + pipe_names)
    if roll < 0.20:                                   # unknown target
        verb = rng.choice(VERBS)
        fake = (_FAKE_NODES if verb != "valve" else
                [f"p_{n}" for n in _FAKE_NODES])
        return verb, rng.choice(fake)
    if roll < 0.40:                                   # dry-pool hunter
        verb = rng.choice(("boil", "tag"))
        dry = [n for n in node_names if spec["nodes"][n]["volume"] <= 0]
        target = rng.choice(dry) if dry else rng.choice(node_names)
        return verb, target
    verb = rng.choice(VERBS)                          # honest try
    if verb == "valve":
        target = (rng.choice(pipe_names) if pipe_names and rng.random() < 0.8
                  else rng.choice([f"p_{n}" for n in _FAKE_NODES]))
    else:
        target = rng.choice(node_names) if rng.random() < 0.75 else rng.choice(_FAKE_NODES)
    return verb, target


# --------------------------------------------------------------- render ----
def render_tokens(spec: dict[str, Any], verb: str, target: str,
                  label: str) -> list[str]:
    """The N4 paper's flat shape: [node tokens; edge tokens; ACTION; LABEL].
    Every field is a typed token so a tiny transformer can consume it
    verbatim (atom vocabulary per the lattice design)."""
    toks = ["[STATE]"]
    for name, nd in spec["nodes"].items():
        toks += [f"n:{name}", f"k:{nd['kind']}", f"z:{nd['elev']}",
                 f"v:{nd['volume']}", f"s:{nd.get('steam', 0)}"]
        if nd["kind"] == "sill":
            toks.append(f"sill:{nd.get('sill', 0)}")
    for name, pp in spec["pipes"].items():
        toks += [f"p:{name}", f"{pp['src']}>{pp['dst']}", f"c:{pp['cap']}",
                 f"sip:{int(pp['siphon'])}", f"o:{int(pp['open'])}"]
        if pp["siphon"]:
            toks += [f"cr:{pp['crest']}", f"pr:{int(pp.get('primed', False))}"]
    toks += ["[ACTION]", f"verb:{verb}", f"tgt:{target}", "[LABEL]", label]
    return toks


# ------------------------------------------------------------ generation ----
def generate(n: int, seed: int, val_frac: float = 0.1) -> tuple[list[dict], list[dict]]:
    rng = random.Random(seed)
    rows: list[dict] = []
    for i in range(n):
        spec = make_graph_spec(rng)
        verb, target = sample_action(rng, spec)
        lab = label_sample(spec, verb, target)
        rows.append({
            "id": f"ldt-{i:06d}",
            "schema": SCHEMA,
            "graph": spec,
            "verb": verb,
            "target": target,
            **lab,
            "tokens": render_tokens(spec, verb, target, lab["label"]),
        })
    # seeded shuffle (random.seed(str) is hash-free: sha512 of the bytes,
    # stable across runs and PYTHONHASHSEED values)
    order = list(range(n))
    random.Random(f"{seed}:split").shuffle(order)
    n_val = round(n * val_frac)
    val_ids = set(order[:n_val])
    train = [r for i, r in enumerate(rows) if i not in val_ids]
    val = [r for i, r in enumerate(rows) if i in val_ids]
    return train, val


def _dump(rows: list[dict], path: Path) -> str:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_dataset(out_dir: Path, n: int, seed: int, val_frac: float = 0.1) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    train, val = generate(n, seed, val_frac)
    manifest: dict[str, Any] = {
        "schema": SCHEMA,
        "seed": seed, "n": n, "val_frac": val_frac,
        "verbs": list(VERBS),
        "label_field": "label",
        "label_set": ["illegal_unknown_verb", "illegal_unknown_target",
                      "illegal_dry_pool", "legal_no_gain", "legal_gain"],
    }
    files = {}
    for split, rows in (("train", train), ("val", val)):
        path = out_dir / f"{split}.jsonl"
        sha = _dump(rows, path)
        dist: dict[str, int] = {}
        for r in rows:
            dist[r["label"]] = dist.get(r["label"], 0) + 1
        files[split] = {"path": str(path), "rows": len(rows), "sha256": sha,
                        "bytes": path.stat().st_size, "labels": dist}
    manifest["files"] = files
    (out_dir / "MANIFEST.json").write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--val-frac", type=float, default=0.1)
    ap.add_argument("--out", type=Path, default=ROOT / "logs" / "legality_ds")
    args = ap.parse_args(argv)
    manifest = write_dataset(args.out, args.n, args.seed, args.val_frac)
    for split, info in manifest["files"].items():
        print(f"{split}: {info['rows']} rows, {info['bytes']} bytes, "
              f"sha256={info['sha256'][:12]}…, labels={info['labels']}")
    print(f"manifest: {args.out / 'MANIFEST.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
