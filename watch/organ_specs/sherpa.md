# ORGAN SPEC: the Sherpa — route planner + quartermaster for the engine bay

```python
#!/usr/bin/env python3
"""sherpa.py — the climbing governor.

Law: no climber launches into bad weather, and no camp ships a queue
thinner than the covenant allows. Every pass the sherpa (1) inventories
unmined files per shelf, (2) stages/restocks engine queues proportional
to each engine's lane health, (3) writes the altitude report to the
board, and (4) calls turnback if lane health degrades or queue quality
thins (thin-ratio > 30%).

Stdlib only. Fail loud on any missing input.
"""

import argparse
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMMIT_MAP = os.path.join(ROOT, "watch", "summit_map.json")
LANE_PROBE = os.path.join(ROOT, "watch", "lane_probe.jsonl")
COVENANT = os.path.join(ROOT, "state", "vast", "covenant.json")
REPORT = os.path.join(ROOT, "watch", "sherpa_report.json")

BASECAMP = os.path.join(ROOT, "camps", "basecamp")
CAMP1 = os.path.join(ROOT, "camps", "camp1")
CAMP2 = os.path.join(ROOT, "camps", "camp2")

THIN_RATIO_MAX = 0.30
LANE_HEALTH_FLOOR = 0.40
QUEUE_TARGET = 8          # nominal queue depth per engine per pass
MINEABLE_EXT = {".md", ".txt", ".json", ".jsonl", ".py", ".yaml", ".yml"}


def fail(msg):
    raise SystemExit("sherpa: " + msg)


def read_json(path):
    if not os.path.isfile(path):
        fail("missing required file: %s" % path)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_jsonl(path):
    if not os.path.isfile(path):
        fail("missing required file: %s" % path)
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                fail("lane_probe.jsonl line %d malformed: %s" % (lineno, exc))
    return rows


def load_lane_health():
    """Fold lane_probe.jsonl into {lane: health} where health is a float 0..1."""
    probes = read_jsonl(LANE_PROBE)
    if not probes:
        fail("lane_probe.jsonl is empty — no weather to climb by")
    buckets = {}
    for row in probes:
        lane = row.get("lane")
        health = row.get("health")
        if lane is None or health is None:
            fail("lane probe missing 'lane' or 'health': %r" % row)
        try:
            health = float(health)
        except (TypeError, ValueError):
            fail("non-numeric health in lane probe: %r" % row)
        buckets.setdefault(lane, []).append(health)
    # Recent probes matter most: last three, weight-decayed toward 1.0.
    folded = {}
    for lane, series in buckets.items():
        recent = series[-3:]
        weights = [1.0 / (i + 1) for i in range(len(recent))]
        folded[lane] = round(
            sum(h * w for h, w in zip(reversed(recent), weights)) / sum(weights),
            4,
        )
    return folded


def load_lane_law():
    """Extract lane_law envelopes from covenant.json."""
    cov = read_json(COVENANT)
    law = cov.get("lane_law")
    if not isinstance(law, dict):
        fail("covenant.json missing lane_law object")
    return law


def load_summit_map():
    wanted = read_json(SUMMIT_MAP)
    if not isinstance(wanted, list):
        fail("summit_map.json must be a list of fold-products")
    return wanted


def mineable_files(camp_dir):
    """Inventory mineable files under a camp shelf. Fail loud if shelf missing."""
    if not os.path.isdir(camp_dir):
        fail("missing camp shelf: %s" % camp_dir)
    found = []
    for base, dirs, names in os.walk(camp_dir):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in sorted(names):
            if name.startswith("."):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in MINEABLE_EXT:
                found.append(os.path.join(base, name))
    return found


def inventory_unmined(mined_index):
    """Return {camp: [files]} for files not yet marked mined in mined_index."""
    inv = {}
    for camp, path in (("basecamp", BASECAMP), ("camp1", CAMP1), ("camp2", CAMP2)):
        unmined = [f for f in mineable_files(path) if os.path.abspath(f) not in mined_index]
        inv[camp] = unmined
    return inv


def read_mined_index(path):
    """A simple ledger of already-mined files; missing file = empty ledger."""
    if not os.path.isfile(path):
        return set()
    with open(path, "r", encoding="utf-8") as fh:
        return {line.strip() for line in fh if line.strip()}


def write_mined_index(path, mined):
    with open(path, "w", encoding="utf-8") as fh:
        for item in sorted(mined):
            fh.write(item + "\n")


def queue_dir(engine):
    d = os.path.join(CAMP2, "queues", engine)
    os.makedirs(d, exist_ok=True)
    return d


def queue_depth(engine):
    return len([n for n in os.listdir(queue_dir(engine)) if n.endswith(".json")])


def queue_thin_ratio(engine):
    """Ratio of queue entries whose payload is empty/thin (no body, tiny doc)."""
    d = queue_dir(engine)
    total = 0
    thin = 0
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(d, name)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                entry = json.load(fh)
        except (json.JSONDecodeError, OSError):
            thin += 1
            total += 1
            continue
        total += 1
        body = entry.get("body") or entry.get("text") or ""
        if not body or len(str(body).strip()) < 40:
            thin += 1
    if total == 0:
        return 0.0
    return thin / total


def stage_queues(unmined, lane_health, lane_law):
    """Restock each engine's queue proportional to its lane health.

    Returns {engine: staged_count}. Engines on lanes below the health floor
    get nothing staged.
    """
    staged = {}
    pool = []
    for camp, files in sorted(unmined.items()):
        pool.extend(files)

    engines = sorted(lane_health)
    if not engines:
        fail("no lanes probed — cannot stage engines")
    for engine in engines:
        health = lane_health[engine]
        law = lane_law.get(engine, {})
        floor = float(law.get("health_floor", LANE_HEALTH_FLOOR))
        cap = int(law.get("queue_cap", QUEUE_TARGET))
        if health < floor:
            staged[engine] = 0
            continue
        target = min(cap, max(1, int(round(QUEUE_TARGET * health))))
        have = queue_depth(engine)
        need = max(0, target - have)
        take = min(need, len(pool))
        for _ in range(take):
            src = pool.pop(0)
            entry = {
                "engine": engine,
                "src": os.path.abspath(src),
                "staged_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "camp": os.path.basename(os.path.dirname(os.path.dirname(src))),
            }
            seq = have + staged[engine] + 1
            name = "%s_%04d.json" % (engine, seq)
            with open(os.path.join(queue_dir(engine), name), "w", encoding="utf-8") as fh:
                json.dump(entry, fh, indent=2)
            staged[engine] = staged.get(engine, 0) + 1
        staged[engine] = staged.get(engine, 0)
    return staged


def call_turnback(lane_health, lane_law, engines_staged):
    """Decide turnback. Returns (turnback: bool, reasons: [str])."""
    reasons = []
    for engine, health in sorted(lane_health.items()):
        floor = float(lane_law.get(engine, {}).get("health_floor", LANE_HEALTH_FLOOR))
        if health < floor:
            reasons.append("lane %s degraded: health %.2f below floor %.2f"
                           % (engine, health, floor))
        if engine in engines_staged:
            thin = queue_thin_ratio(engine)
            if thin > THIN_RATIO_MAX:
                reasons.append("queue %s thin: thin-ratio %.2f > %.2f"
                               % (engine, thin, THIN_RATIO_MAX))
    return (bool(reasons), reasons)


def write_report(report):
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return REPORT


def climb_pass(once=True):
    """One planning pass: inventory, stage, report, turnback."""
    summit = load_summit_map()
    lane_health = load_lane_health()
    lane_law = load_lane_law()
    ledger = os.path.join(ROOT, "watch", "sherpa_mined.txt")
    mined = {os.path.abspath(p) for p in read_mined_index(ledger)}
    unmined = inventory_unmined(mined)

    engines_staged = stage_queues(unmined, lane_health, lane_law)

    queues_left = {e: queue_depth(e) for e in lane_health}
    thin = {e: round(queue_thin_ratio(e), 4) for e in lane_health}

    turnback, reasons = call_turnback(lane_health, lane_law, engines_staged)
    wings_mined = sum(queues_left.values())

    report = {
        "pass_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "once": once,
        "fold_products_wanted": len(summit),
        "unmined": {camp: len(files) for camp, files in unmined.items()},
        "lane_health": lane_health,
        "staged": engines_staged,
        "queues_left": queues_left,
        "thin_ratio": thin,
        "wings_mined": wings_mined,
        "fold_debt": max(0, len(summit) - wings_mined),
        "turnback": turnback,
        "turnback_reasons": reasons,
    }
    path = write_report(report)

    if not turnback:
        # Commit staged sources to the mined ledger only on a good pass.
        mined.update(os.path.abspath(f) for files in unmined.values() for f in files)
        write_mined_index(ledger, mined)

    return report, path


def main(argv=None):
    parser = argparse.ArgumentParser(description="sherpa — the climbing governor")
    parser.add_argument("--once", action="store_true",
                        help="run one planning pass and write the altitude report")
    args = parser.parse_args(argv)
    if not args.once:
        parser.error("only --once is supported; run: sherpa.py --once")
    report, path = climb_pass(once=True)
    status = "TURNBACK" if report["turnback"] else "CLIMB"
    sys.stdout.write("sherpa: %s — wings_mined=%d fold_debt=%d report=%s\n"
                     % (status, report["wings_mined"], report["fold_debt"], path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
