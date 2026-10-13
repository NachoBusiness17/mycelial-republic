"""Radix-leaf LRU null arm over the estate trail tapes (G1 gap law, M3 steal).

Law: memory/research_polished/kv_cache_compaction.md:13 - gap-fold G1: any
eviction/compaction claim must beat LRU/ARC/PBKV/Belady-MIN arms or it is
decoration. This tool mints the LRU null arm that law demands: it replays the
most recent N estate tape rows (dashboard/static/trails/*.jsonl) through a
block-level prefix-cache simulator at the real janitor pack budget
(mag/context_pack.py:67, "max_chars": 4800, char-denominated) and sweeps cache
capacity to produce the hit-rate curve.

Source ask: watch/inbox/gala_20260925/fillball-1001/lanes/work/48h.src.md:60
(M3) - falsifiable claim: radix-leaf LRU at the estate's real budget achieves
80%+ hit (external reference: 83.48% at 8k blocks on the AgentX subset,
github.com/gauravapiscean/agentic-kv-cache via HN item 49643543). HOLDS: the
measured number becomes the G1 null every future eviction/compaction claim
must beat or be rejected as decoration. FAILS: the lever is pack budget and
assembly (freeze + tail, mag/context_pack.py:489), not eviction policy.

Serving model (documented, deterministic, no RNG anywhere):

  - Each trail row is ONE serving request, replayed in chronological order.
    Transcript source pinned at probe start: db.sqlite was NOT found at repo
    root, so the run is trails alone - the M3 card's named contingency.
  - Rows group into sessions by (lane=file stem, actor=row actor); a gap over
    --session-gap-min (default 30, the OpenAI documented reuse window cited
    at kv_cache_compaction.md:15) starts a new session.
  - Every request renders an estate-style pack at the real budget:
      a byte-identical frozen prefix (the A2 session-frozen prompt law,
      mag/context_pack.py:467-526 freeze_system_prompt) + the session's
      append-only transcript tail of real row bytes
      ("[{ts}] {actor} {event}: {detail}"), hard-clipped with the estate's
      own clip shape (mag/context_pack.py:1414-1416: keep head, append
      "...(pack clipped)").
  - The frozen prefix is SYNTHETIC but realistic-sized (--frozen-chars,
    default 1024) and deterministic per (lane, actor); its sha256 is recorded
    in the output. Limitation, named: it models a frozen system prompt, it is
    not the estate's live-rendered one.
  - Three arms isolate assembly from eviction:
      frozen_append  estate A2 doctrine: frozen prefix + append-only
                     transcript, head-kept hard clip. PRIMARY (the null).
      frozen_window  pack-first rolling cores: frozen prefix + last-W-chars
                     window of the transcript ("Trail cores (mid-run
                     continuity - re-inject)" serving shape).
      volatile       the pre-A2 disease: prefix re-rendered with the row
                     timestamp every call (repack rebuilds the pack per
                     turn - the #1 cache killer, kv_cache_compaction.md:23).
  - Blocks are char-denominated (the estate budget is chars, not tokens);
    default 256 chars/block. Hit = chars of full blocks already cached at
    lookup time; the partial trailing block never caches (conservative,
    fixed). At budget 4800 the budget is not block-aligned (18.75 blocks), so
    full_hit_rate is structurally 0 - read hit_rate, not full_hit, at this
    budget/block pairing.

Simulator engine + tape loaders live in tools/prefix_cache_sim.py (split
2026-10-03 to stay under the ratchet's 400-line bar; the merged first draft
read NEW file-too-long at :602). Names are re-exported here so tests and
callers can import either path.

Output: JSON (default memory/runs/lru_null_arm/lru_null_arm_results.json) plus
a human table on stdout. Deterministic for a given tree state.

Receipt: watch/inbox/buildall/lru-null-arm.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.prefix_cache_sim import (  # noqa: E402,F401  (re-exported API)
    SCHEMA,
    RadixLeafLRU,
    _clip_keep_head,
    _frozen_prefix,
    assign_sessions,
    build_prompt_sets,
    load_rows,
    most_recent_chronological,
    replay,
    self_test,
)

DEFAULT_GRID = "2,4,8,16,32,64,128,256,512,1024,2048,4096,8192"
DEFAULT_ARMS = "frozen_append,frozen_window,volatile"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--trails-dir", default=str(ROOT / "dashboard" / "static" / "trails"))
    ap.add_argument("--limit", type=int, default=5000,
                    help="most recent N rows (0 = all)")
    ap.add_argument("--budget", type=int, default=4800,
                    help="janitor pack budget in chars (mag/context_pack.py:67)")
    ap.add_argument("--block-chars", type=int, default=256)
    ap.add_argument("--frozen-chars", type=int, default=1024)
    ap.add_argument("--session-gap-min", type=float, default=30.0)
    ap.add_argument("--grid", default=DEFAULT_GRID,
                    help="capacity sweep in blocks; unbounded always appended")
    ap.add_argument("--anchor-blocks", type=int, default=8192,
                    help="external-parity anchor (agentic-kv-cache 8k blocks)")
    ap.add_argument("--arms", default=DEFAULT_ARMS)
    ap.add_argument("--curve-arm", default="frozen_append")
    ap.add_argument("--claim-threshold", type=float, default=0.80)
    ap.add_argument("--out", default=str(ROOT / "memory" / "runs" / "lru_null_arm"
                                         / "lru_null_arm_results.json"))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        failures, n_checks = self_test()
        if failures:
            print(f"SELF-TEST FAIL ({len(failures)}):")
            for f in failures:
                print(f"  - {f}")
            return 1
        print(f"SELF-TEST PASS: {n_checks} checks green "
              "(prefix_share, lru_keeps_recent, lru_evicts_oldest, "
              "lru_evict_cascade, internal_survives, evicted_leaf_gone, "
              "append_only_hits, clip_shape, clip_noop, capacity_honored, "
              "determinism)")
        return 0

    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    curve_arm = args.curve_arm
    if curve_arm not in arms:
        arms.insert(0, curve_arm)

    rows, inventory = load_rows(Path(args.trails_dir))
    rows = most_recent_chronological(rows, args.limit)
    rows, n_sessions = assign_sessions(rows, args.session_gap_min)
    if not rows:
        print("no replayable rows: nothing to measure", file=sys.stderr)
        return 2
    prompts, prompt_meta = build_prompt_sets(
        rows, budget=args.budget, frozen_chars=args.frozen_chars, arms=arms)

    grid = [int(x) for x in str(args.grid).split(",") if x.strip()]
    curve = [replay(prompts[curve_arm], capacity_blocks=c,
                    block_chars=args.block_chars) for c in grid]
    unbounded = replay(prompts[curve_arm], capacity_blocks=None,
                       block_chars=args.block_chars)
    arms_at_anchor = {a: replay(prompts[a], capacity_blocks=args.anchor_blocks,
                                block_chars=args.block_chars) for a in arms}
    # pack-scale capacities: 1x / 4x / 16x the janitor pack budget
    pack_blocks = -(-args.budget // args.block_chars)  # ceil
    pack_scale = {
        f"{n}x_pack": replay(prompts[curve_arm],
                             capacity_blocks=pack_blocks * n,
                             block_chars=args.block_chars)
        for n in (1, 4, 16)
    }

    anchor = arms_at_anchor[curve_arm]
    holds = anchor["hit_rate"] >= args.claim_threshold
    verdict = {
        "claim": ("radix-leaf LRU at the estate's real 4,800-char pack budget "
                  f"achieves {args.claim_threshold:.0%}+ hit on estate trails"),
        "arm": curve_arm,
        "anchor": (f"{args.anchor_blocks} blocks x {args.block_chars} chars = "
                   f"{args.anchor_blocks * args.block_chars} chars (external "
                   "parity: agentic-kv-cache 8k blocks, 83.48% AgentX subset)"),
        "hit_rate_at_anchor": anchor["hit_rate"],
        "threshold": args.claim_threshold,
        "holds": holds,
        "consequence_holds": ("the measured number becomes the G1 null every "
                              "future eviction/compaction claim must beat or "
                              "be rejected as decoration"),
        "consequence_fails": ("the lever is pack budget and assembly (freeze "
                              "+ tail), not eviction policy"),
        "external_reference": "83.48% at 8k blocks on the AgentX subset",
    }

    result = {
        "schema": SCHEMA,
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "config": {
            "limit": args.limit,
            "budget_chars": args.budget,
            "block_chars": args.block_chars,
            "frozen_chars": args.frozen_chars,
            "session_gap_min": args.session_gap_min,
            "grid_blocks": grid,
            "anchor_blocks": args.anchor_blocks,
            "arms": arms,
            "curve_arm": curve_arm,
            "claim_threshold": args.claim_threshold,
        },
        "inventory": {
            **inventory,
            "rows_used": len(rows),
            "span_first_ts": rows[0]["ts"],
            "span_last_ts": rows[-1]["ts"],
            "n_sessions": n_sessions,
            "mean_prompt_chars": round(sum(len(p) for p in prompts[curve_arm])
                                       / len(prompts[curve_arm]), 1),
            "prompt_source_note": ("db.sqlite pinned out at probe start (not "
                                   "found at repo root); trails alone per the "
                                   "M3 card's contingency"),
        },
        "serving_model": prompt_meta,
        "curve": curve,
        "unbounded_ceiling": unbounded,
        "pack_scale": pack_scale,
        "arms_at_anchor": arms_at_anchor,
        "verdict": verdict,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                        encoding="utf-8")

    # human table
    inv = result["inventory"]
    print(f"LRU NULL ARM - radix-leaf LRU over estate trails ({SCHEMA})")
    print(f"tapes: {inv['rows_used']} rows used "
          f"(of {inv['rows_total']} in {len(inv['files'])} files; "
          f"skipped: {inv['skipped_bad_json']} bad json, "
          f"{inv['skipped_bad_ts']} bad ts), "
          f"span {inv['span_first_ts']} .. {inv['span_last_ts']}, "
          f"{inv['n_sessions']} sessions")
    print(f"model: budget={args.budget} chars, block={args.block_chars} chars, "
          f"frozen={args.frozen_chars} chars, session_gap={args.session_gap_min} min, "
          f"curve_arm={curve_arm}")
    print(f"curve arm prompts: mean {inv['mean_prompt_chars']} chars/request")
    print()
    print(f"{'cap_blocks':>10} {'cap_chars':>12} {'hit_rate':>9} "
          f"{'full_hit':>9} {'evictions':>10}")
    for row in curve:
        print(f"{row['capacity_blocks']:>10} {row['capacity_chars']:>12} "
              f"{row['hit_rate']:>9.4f} {row['full_hit_rate']:>9.4f} "
              f"{row['evictions']:>10}")
    u = unbounded
    print(f"{'UNBOUNDED':>10} {'-':>12} {u['hit_rate']:>9.4f} "
          f"{u['full_hit_rate']:>9.4f} {u['evictions']:>10}")
    print()
    print(f"arms at anchor ({args.anchor_blocks} blocks):")
    for a in arms:
        s = arms_at_anchor[a]
        print(f"  {a:>14}: hit_rate={s['hit_rate']:.4f} "
              f"full_hit={s['full_hit_rate']:.4f}")
    print()
    for name, s in pack_scale.items():
        print(f"pack-scale {name:>8} ({s['capacity_blocks']} blocks): "
              f"hit_rate={s['hit_rate']:.4f}")
    print()
    v = verdict
    gate = "HOLDS" if v["holds"] else "FAILS"
    print(f"CLAIM {gate}: '{v['claim']}'")
    print(f"  hit_rate@anchor = {v['hit_rate_at_anchor']:.4f} vs threshold "
          f"{v['threshold']:.2f}  ({v['anchor']})")
    print(f"  consequence: "
          f"{v['consequence_holds'] if v['holds'] else v['consequence_fails']}")
    print()
    print(f"JSON banked: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
