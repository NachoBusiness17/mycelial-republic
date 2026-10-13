"""Census for the XiaomiMiMo/MiMo-V2.6-RL-oss dataset (HF, Apache 2.0).

AC3 (last_mile_20260930): download the 5 parquet shards via
huggingface_hub.snapshot_download (datasets lib absent from the venv; the
mission brief sanctions the hub route), count rows, and census the fields
the estate wants for the water-graph legality comparison: shard sizes,
data_source / ability / agent_name / reward_model.style, project-type
heuristics on the code shard (instance ids are opaque format-code-task-NNNNNN
so the only project signal is the problem_statement text), category/tag
spread on the general shard, music metadata, docker image + test command +
timeout shapes inside extra_info.instance_json, and a seeded 5-prompt sample
with the environment triple (docker image, test command, timeouts).

Output: prints a markdown census and writes JSON next to the receipt
(watch/inbox/last_mile_20260930/ac3_mimo_census.json). Deterministic:
sampled indices come from random.Random(seed), never from wall clock.
Receipt: watch/inbox/last_mile_20260930/AC3_MIMO.md (2026-09-29 run:
7,780 rows across 5 shards, ~21.4 MB parquet).
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import re
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data" / "mimo_v26"
OUT_JSON = REPO / "watch" / "inbox" / "last_mile_20260930" / "ac3_mimo_census.json"
REPO_ID = "XiaomiMiMo/MiMo-V2.6-RL-oss"
SHARDS = ["code.parquet", "cyber.parquet", "general/train.parquet",
          "music.parquet", "webdev.parquet"]
SAMPLE_SEED = 20260930
SAMPLE_N = 5

# Multi-label heuristic over problem_statement text; the code shard's
# instance_json carries no repo/language field (only cwd, which is a constant
# /testbed or /workspace/repo), so text is the only project-type signal.
PROJECT_PATTERNS: dict[str, str] = {
    "Python": r"\bpython\b|pypi|pip install",
    "JS/TS/Node": r"typescript|javascript|\bnpm\b|\byarn\b|\bnode\.js\b|react|vue|webpack",
    "Django": r"\bdjango\b",
    "Java/JVM": r"\bjava\b|\bmaven\b|\bgradle\b|\bkotlin\b",
    "C/C++": r"\bc\+\+\b|\bgcc\b|\bclang\b|\bcmake\b",
    "Go": r"\bgolang\b|\bgo module\b|\bgo\b \w+\.go",
    "Rust": r"\brust\b|cargo\.toml|\bcrate\b",
    "GitHub Actions": r"github actions|\bactions/\b|action\.ya?ml|workflow file",
    "Flutter/Dart": r"\bflutter\b|\bdart\b",
    "Gazebo/ROS": r"\bgazebo\b|\bros2?\b|\brviz\b",
}


def ensure_data() -> Path:
    """Download shards on first use; keep the 925-file general/envs tree out
    (41,285 files) — the parquet rows already embed the env manifests."""
    missing = [s for s in SHARDS if not (DATA_DIR / s).exists()]
    if missing:
        from huggingface_hub import snapshot_download
        snapshot_download(REPO_ID, repo_type="dataset",
                          allow_patterns=SHARDS + ["README.md", "image-mapping.jsonl"],
                          local_dir=str(DATA_DIR))
    return DATA_DIR


def load_rows() -> dict[str, list[dict[str, Any]]]:
    import pyarrow.parquet as pq
    return {s: pq.read_table(DATA_DIR / s).to_pylist() for s in SHARDS}


def ctr(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(collections.Counter(str(r.get(key)) for r in rows).most_common())


def instance_jsons(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for r in rows:
        raw = r.get("extra_info", {}).get("instance_json")
        out.append(json.loads(raw) if raw else {})
    return out


def census(rows_by_shard: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    result: dict[str, Any] = {"repo_id": REPO_ID, "shards": {}}
    for shard, rows in rows_by_shard.items():
        entry: dict[str, Any] = {
            "rows": len(rows),
            "data_source": ctr(rows, "data_source"),
            "ability": ctr(rows, "ability"),
            "agent_name": ctr(rows, "agent_name"),
            "reward_style": dict(collections.Counter(
                r["reward_model"]["style"] for r in rows).most_common()),
            "reward_ground_truth_nonempty": sum(
                1 for r in rows if (r["reward_model"].get("ground_truth") or "").strip()),
            "prompt_turns": dict(collections.Counter(
                len(r["prompt"]) for r in rows).most_common()),
            "prompt_roles": dict(collections.Counter(
                m["role"] for r in rows for m in r["prompt"]).most_common()),
        }
        ijs = instance_jsons(rows)
        if shard == "code.parquet":
            proj = collections.Counter()
            for r, ij in zip(rows, ijs):
                ps = (ij.get("problem_statement") or "").lower()
                hit = False
                for label, pat in PROJECT_PATTERNS.items():
                    if re.search(pat, ps):
                        proj[label] += 1
                        hit = True
                if not hit:
                    proj["(unmatched: no project keyword)"] += 1
            entry["project_type_heuristic_multilabel"] = dict(proj.most_common())
            entry["docker_images_distinct"] = len({ij.get("docker_image") for ij in ijs})
            entry["test_command_shapes"] = dict(collections.Counter(
                ij.get("test_command") for ij in ijs).most_common(5))
            entry["verifier_timeout_sec"] = dict(collections.Counter(
                ij.get("verifier_timeout_sec") for ij in ijs).most_common())
            entry["has_test_patch"] = sum(1 for ij in ijs if ij.get("test_patch"))
        if shard == "cyber.parquet":
            entry["docker_images"] = dict(collections.Counter(
                ij.get("docker_image") for ij in ijs).most_common(5))
        if shard == "general/train.parquet":
            entry["categories"] = dict(collections.Counter(
                str(ij.get("category")) for ij in ijs).most_common(15))
            tags = collections.Counter(
                t for ij in ijs for t in (ij.get("tags") or [])[:3])
            entry["tags_top"] = dict(tags.most_common(20))
            entry["difficulty"] = dict(collections.Counter(
                str(ij.get("difficulty")) for ij in ijs).most_common())
            res = collections.Counter()
            for ij in ijs:
                res[f"agent={ij.get('agent_timeout_sec')}/verifier={ij.get('verifier_timeout_sec')}"] += 1
            entry["timeouts_agent_verifier"] = dict(res.most_common(8))
            entry["resource_limits_memory_mb_top"] = dict(collections.Counter(
                str(ij.get("memory_mb")) for ij in ijs).most_common(5))
            entry["allow_internet"] = dict(collections.Counter(
                str(ij.get("allow_internet")) for ij in ijs).most_common())
            entry["docker_images"] = dict(collections.Counter(
                (ij.get("docker_image") or "").split("/")[-1] for ij in ijs
            ).most_common(5))
        if shard == "webdev.parquet":
            entry["categories"] = dict(collections.Counter(
                str(ij.get("category")) for ij in ijs).most_common())
            entry["docker_images"] = dict(collections.Counter(
                ij.get("docker_image") for ij in ijs).most_common(5))
        if shard == "music.parquet":
            ei = [r["extra_info"] for r in rows]
            entry["lang"] = dict(collections.Counter(e.get("lang") for e in ei).most_common())
            entry["tags_top"] = dict(collections.Counter(
                e.get("tag") for e in ei).most_common(10))
            entry["length"] = dict(collections.Counter(e.get("length") for e in ei).most_common())
        result["shards"][shard] = entry
    result["total_rows"] = sum(len(r) for r in rows_by_shard.values())
    return result


def sample_prompts(rows_by_shard: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Seeded stratified sample: one row per shard, keyed by instance id."""
    rng = random.Random(SAMPLE_SEED)
    picked = []
    for shard in SHARDS:
        rows = rows_by_shard[shard]
        r = rows[rng.randrange(len(rows))]
        ij = instance_jsons([r])[0]
        picked.append({
            "shard": shard,
            "instance_id": r["extra_info"].get("instance_id")
                           or r["extra_info"].get("src_id"),
            "prompt_head": r["prompt"][0]["content"][:400],
            "reward": {k: (v[:200] if isinstance(v, str) else v)
                       for k, v in r["reward_model"].items()},
            "extra_info_env": {k: ij.get(k) for k in
                               ("docker_image", "test_command", "verifier_timeout_sec",
                                "agent_timeout_sec", "cwd", "category", "difficulty")
                               if k in ij},
            "extra_info_other_keys": sorted(set(ij) - {
                "docker_image", "test_command", "verifier_timeout_sec",
                "agent_timeout_sec", "cwd", "category", "difficulty"}),
        })
    return picked


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-write", action="store_true",
                    help="print only; skip the JSON receipt sidecar")
    args = ap.parse_args(argv)

    ensure_data()
    rows_by_shard = load_rows()
    result = census(rows_by_shard)
    result["samples"] = sample_prompts(rows_by_shard)

    print("# MiMo-V2.6-RL-oss census\n")
    print(f"total rows: {result['total_rows']}\n")
    print("| shard | rows | data_source | ability | reward | notes |")
    print("|---|---|---|---|---|---|")
    notes = {
        "code.parquet": "1 docker image + test_command per task; timeout 1800s",
        "cyber.parquet": "arvo vuln repro, rule checks, no test cmd",
        "general/train.parquet": "925 general_agent + 64 terminal_bench; rubric verify",
        "music.parquet": "zh music prompts, rule checks",
        "webdev.parquet": "visual grading, single shared image",
    }
    for shard in SHARDS:
        e = result["shards"][shard]
        print(f"| {shard} | {e['rows']} | {next(iter(e['data_source']), '')} "
              f"| {next(iter(e['ability']), '')} | {next(iter(e['reward_style']), '')} "
              f"| {notes[shard]} |")

    if not args.no_write:
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\njson: {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
