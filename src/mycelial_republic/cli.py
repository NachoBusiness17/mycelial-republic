"""CLI entrypoint: mycelia."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mycelia",
        description="Mycelial Republic — Phase 0 Seed Mirror tools",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prep = sub.add_parser("prep", help="Extract and clean posts from X archive")
    p_prep.add_argument("--raw", required=True, help="Path to zip or extracted archive dir")
    p_prep.add_argument("--out", required=True, help="Output JSONL path")
    p_prep.add_argument("--min-chars", type=int, default=40, help="Drop posts shorter than this")

    p_xp = sub.add_parser("x-pull", help="Fetch public posts by status ID into JSONL")
    p_xp.add_argument("--out", required=True)
    p_xp.add_argument("--ids", default="", help="Comma-separated status IDs")
    p_xp.add_argument("--ids-file", default="", help="File with one ID per line")
    p_xp.add_argument("--seed", default="", help="Merge existing JSONL")

    p_bm = sub.add_parser(
        "bookmarks",
        help="Ingest URL lists / browser exports (use for X Bookmarks pasted as links)",
    )
    p_bm.add_argument("--path", required=True, help="File or data/bookmarks drop folder")
    p_bm.add_argument("--out", required=True)
    p_bm.add_argument("--seed", default="")
    p_bm.add_argument("--folder", default="", help="Filter by folder name substring")
    p_bm.add_argument("--no-fetch", action="store_true", help="Do not fetch URL bodies")

    p_xbm = sub.add_parser(
        "x-bookmarks",
        help="Fetch X Bookmarks via official API (needs X_USER_ID + OAuth token)",
    )
    p_xbm.add_argument("--out", required=True)

    p_th = sub.add_parser(
        "thread-pull",
        help="Pull full threads + media metadata for status IDs (subposts via unroll)",
    )
    p_th.add_argument("--ids-file", required=True)
    p_th.add_argument("--out", required=True)
    p_th.add_argument("--seed", default="")
    p_th.add_argument("--sleep", type=float, default=0.4)

    p_ann = sub.add_parser("annotate", help="Annotate posts with rope/knot metadata")
    p_ann.add_argument("--in", dest="inp", required=True, help="Input posts JSONL")
    p_ann.add_argument("--out", required=True, help="Output training JSONL")
    p_ann.add_argument(
        "--auto-heuristics",
        action="store_true",
        help="Apply keyword heuristics for chord/refusal tags (review still required)",
    )

    p_val = sub.add_parser("validate", help="Validate annotated training set")
    p_val.add_argument("--in", dest="inp", required=True)
    p_val.add_argument("--min", type=int, default=800, help="Minimum example count")

    p_la = sub.add_parser(
        "lattice-adapt",
        help="Convert Mag lattice digs into honest training rows + eval fixtures",
    )
    p_la.add_argument("--digs", required=True, help="Path to lattice digs dir")
    p_la.add_argument("--train-out", required=True)
    p_la.add_argument("--fixture-out", required=True)

    p_strike = sub.add_parser("strike", help="Log a chord strike on an artifact")
    p_strike.add_argument("--target", required=True, help="What was struck (path or name)")
    p_strike.add_argument("--rope", default="", help="Named rope / tension source")
    p_strike.add_argument("--loops", default="", help="Loops found")
    p_strike.add_argument("--moves", default="", help="Disentangled moves")
    p_strike.add_argument("--out", default="", help="Optional output markdown path")

    p_sc = sub.add_parser("scaffolds", help="List or show Steiniger/hybrid scaffolds")
    p_sc.add_argument("action", choices=["list", "show"], nargs="?", default="list")
    p_sc.add_argument("path", nargs="?", default="", help="Relative path for show")
    p_sc.add_argument("--max-chars", type=int, default=0)

    p_st = sub.add_parser(
        "selftest",
        help="Run built-in checklist self-tests; score vector map + influences",
    )
    p_st.add_argument("--checklist", default="", help="Path to selftest_checklist.yaml")
    p_st.add_argument("--map", dest="map_path", default="", help="Path to vector_map_*.yaml")
    p_st.add_argument("--out", default="", help="Report output directory")
    p_st.add_argument(
        "--responses",
        default="",
        help="Optional dir of live response .txt overrides (named like fixtures)",
    )

    p_vm = sub.add_parser("vector-map", help="Print or export current vector map snapshot")
    p_vm.add_argument("--map", dest="map_path", default="", help="Path to vector_map yaml")
    p_vm.add_argument(
        "--from-latest-selftest",
        action="store_true",
        help="Use logs/selftest/latest.json measured map if present",
    )
    p_vm.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")

    p_infer = sub.add_parser(
        "infer",
        help="Run the local seed-mirror model via ollama (chat)",
    )
    p_infer.add_argument("prompt", help="Prompt to send to the seed-mirror model")
    p_infer.add_argument(
        "--model", default="seed-mirror", help="Ollama model name (default seed-mirror)"
    )
    p_infer.add_argument(
        "--fixture",
        default="",
        help="Optional eval fixture JSONL to score responses against",
    )

    from mycelial_republic.scrum import add_scrum_parser

    add_scrum_parser(sub)

    args = parser.parse_args(argv)

    if args.cmd == "prep":
        from mycelial_republic.data.prep import run_prep

        return run_prep(args.raw, args.out, min_chars=args.min_chars)
    if args.cmd == "x-pull":
        from mycelial_republic.data.x_pull import run_pull_ids

        ids: list[str] = []
        if args.ids:
            ids.extend(args.ids.split(","))
        if args.ids_file:
            from pathlib import Path

            p = Path(args.ids_file)
            if p.is_file():
                ids.extend(p.read_text(encoding="utf-8").splitlines())
        return run_pull_ids(ids, args.out, seed_jsonl=args.seed or None)
    if args.cmd == "bookmarks":
        from mycelial_republic.data.bookmarks_ingest import run_bookmarks_ingest

        return run_bookmarks_ingest(
            args.path,
            args.out,
            seed=args.seed or None,
            fetch=not args.no_fetch,
            folder_filter=args.folder,
        )
    if args.cmd == "x-bookmarks":
        from mycelial_republic.data.x_bookmarks_api import run_x_bookmarks_api

        return run_x_bookmarks_api(args.out)
    if args.cmd == "thread-pull":
        from mycelial_republic.data.thread_pull import run_thread_pull
        from pathlib import Path

        ids = [
            ln.strip()
            for ln in Path(args.ids_file).read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")
        ]
        return run_thread_pull(
            ids, args.out, seed=args.seed or None, sleep_s=args.sleep
        )
    if args.cmd == "annotate":
        from mycelial_republic.data.annotate import run_annotate

        return run_annotate(args.inp, args.out, auto_heuristics=args.auto_heuristics)
    if args.cmd == "validate":
        from mycelial_republic.data.validate import run_validate

        return run_validate(args.inp, min_examples=args.min)
    if args.cmd == "lattice-adapt":
        from mycelial_republic.data.lattice_adapter import run_adapt

        return run_adapt(args.digs, args.train_out, args.fixture_out)
    if args.cmd == "strike":
        from mycelial_republic.audit.chord_strike import run_strike

        return run_strike(
            target=args.target,
            rope=args.rope,
            loops=args.loops,
            moves=args.moves,
            out_path=args.out or None,
        )
    if args.cmd == "scaffolds":
        from mycelial_republic.scaffolds.catalog import list_scaffolds, read_scaffold, scaffolds_root

        if args.action == "list" or not args.path:
            root = scaffolds_root()
            print(f"root: {root}")
            for p in list_scaffolds():
                rel = p.relative_to(root)
                print(f"{p.stat().st_size:8d}  {rel.as_posix()}")
            return 0
        text = read_scaffold(args.path)
        if args.max_chars and len(text) > args.max_chars:
            print(text[: args.max_chars])
            print(f"\n... [{len(text) - args.max_chars} more chars]")
        else:
            print(text)
        return 0
    if args.cmd == "selftest":
        from mycelial_republic.selftest.runner import run_selftest

        report = run_selftest(
            checklist_path=args.checklist or None,
            map_path=args.map_path or None,
            responses_dir=args.responses or None,
            out_dir=args.out or None,
        )
        print(
            f"selftest: {report.passed}/{report.total} passed | overall={report.overall:.3f} | "
            f"E={report.dirichlet_energy:.4f} | ok={report.ok}"
        )
        for p in report.probes:
            flag = "PASS" if p.passed else "FAIL"
            print(f"  [{flag}] {p.id:28s} {p.aggregate:.3f}  {p.session}")
            if p.error:
                print(f"         error: {p.error}")
        print("reports → logs/selftest/ (latest.json, vector_map_latest.md)")
        return 0 if report.ok else 1
    if args.cmd == "vector-map":
        import json
        from pathlib import Path

        from mycelial_republic.vector_map.model import load_vector_map

        root = Path(__file__).resolve().parents[2]
        latest = root / "logs" / "selftest" / "latest.json"
        if args.from_latest_selftest and latest.is_file():
            data = json.loads(latest.read_text(encoding="utf-8"))
            snap = data.get("vector_map") or {}
            if args.json:
                print(json.dumps(snap, indent=2))
            else:
                # Prefer written markdown if present
                md = root / "logs" / "selftest" / "vector_map_latest.md"
                if md.is_file() and not args.json:
                    print(md.read_text(encoding="utf-8"))
                else:
                    print(json.dumps(snap, indent=2))
            return 0
        map_path = args.map_path or str(root / "configs" / "vector_map_hybrid.yaml")
        vmap = load_vector_map(map_path)
        if args.json:
            print(json.dumps(vmap.snapshot(), indent=2))
        else:
            print(vmap.to_markdown())
        return 0
    if args.cmd == "infer":
        from mycelial_republic.train.infer import run_infer

        return run_infer(args.prompt, model=args.model, fixture=args.fixture or None)
    if args.cmd == "scrum":
        from mycelial_republic.scrum import run_scrum

        return run_scrum(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
