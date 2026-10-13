"""Knot tonight's three artifacts into the verkle chain (2026-09-12).

D6 divergence-lane finding: the parable, the 25k loop fix, and the trailer
telemetry existed only as watch cards — one knot-session from being history.
This session sediments them. Backup-first per the surgery law; the chain's
own integrity gate refuses an unverified chain regardless.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import verkle_knot as vk  # noqa: E402

BIO = ROOT / "memory" / "biography"
STAMP = "2026-09-12T02:5xZ"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dossier(session_id: str, dominant: str, files: list[Path], note: str) -> dict:
    now = datetime.now(timezone.utc)
    manifest = {str(f.relative_to(ROOT)): _sha(f) for f in files if f.is_file()}
    commit_hex = hashlib.sha256(
        json.dumps(manifest, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "session_id": session_id,
        "time": {
            "created_at": {
                "iso_minute": now.strftime("%Y-%m-%dT%H:%M") + "Z",
                "unix_minute": int(now.timestamp()) // 60,
                "date": now.strftime("%Y-%m-%d"),
            },
            "updated_at": {
                "iso_minute": now.strftime("%Y-%m-%dT%H:%M") + "Z",
                "unix_minute": int(now.timestamp()) // 60,
            },
        },
        "scalar_knot": {
            "theme_vector": {
                "dominant": dominant,
                "basis": vk.THEME_BASIS,
                "raw": [0.0] * len(vk.THEME_BASIS),
                "normalized": [0.0] * len(vk.THEME_BASIS),
            },
            "duration_minutes": 0,
            "tension_index": None,
            "residual_weight": None,
            "Q_proxy": None,
            "gap_proxy": None,
            "lambda2_proxy": None,
            "dirichlet_energy_proxy": None,
        },
        "content_commit": {"hex": commit_hex},
        "chord": {"commitment_hash": None, "framework_root": None, "note": note},
        "_manifest": manifest,
    }


def main() -> int:
    chain = BIO / "verkle_chain.jsonl"
    tip = BIO / "verkle_tip.json"
    for target in (chain, tip):
        if target.is_file():
            bak = target.with_suffix(target.suffix + ".bak-knotnight-20260912")
            shutil.copy2(target, bak)
            print(f"backup: {bak.name}")

    artifacts = [
        dossier(
            "artifact-parable-20260911",
            "parable_testament",
            [
                ROOT / "corpus" / "canon" / "THE_PARABLE_OF_THE_FIELD_AND_THE_STONES.md",
                ROOT / "watch" / "inbox" / "COLD_READ_TEST_20260912.md",
                ROOT / "corpus" / "canon" / "THE_FIRST_LAW_20260912.md",
            ],
            "The First Law and the parable: 7 blind readers across 2 waves "
            "rebuilt the same house from the story alone. Story-as-installer "
            "SUPPORTED at grammar level.",
        ),
        dossier(
            "artifact-25k-loop-fix-20260911",
            "loop_fix_receipt",
            [
                ROOT / "watch" / "MOONSHOT_THE_LOOP_20260911.md",
                ROOT / "tests" / "test_tool_dispatch_shape.py",
                ROOT / "scripts" / "alert_reader.py",
            ],
            "The 25k silent-loss class closed: result.error surfaced "
            "(agent_cli.py), cmd->command alias (tools/__init__.py), "
            "signature-pressure alarm caught its second loop (powershell "
            "x1545) on its first night. Corrected count: 24,854 records + "
            "153 mentions = LINES.",
        ),
        dossier(
            "artifact-trailer-20260911",
            "trailer_telemetry",
            [
                ROOT / "watch" / "inbox" / "TRAILER_MECHANISM_20260911.md",
                ROOT / "dashboard" / "static" / "trailer_telemetry.json",
            ],
            "Attachment under relative motion: severity-3 trailer telemetry "
            "live — falls achieved, dynamic range real, the falsifier has "
            "its first data.",
        ),
    ]

    results = []
    for d in artifacts:
        res = vk.append_verkle_knot(d)
        results.append((d["session_id"], res))
        ok = res.get("ok")
        print(f"{d['session_id']}: ok={ok} "
              f"{'skipped' if res.get('skipped') else ''} "
              f"leaf={str(res.get('leaf_hash'))[:12]} "
              f"file={res.get('filename')}")
        if not ok:
            print(f"  ERROR: {res.get('error') or res}")
            return 1

    # post-write verification
    ver = vk._verify_chain_consistent()
    print(f"chain consistent after writes: {ver}")
    tipdoc = json.loads(tip.read_text(encoding="utf-8"))
    print(f"tip: root={str(tipdoc.get('root'))[:16]} leaves={tipdoc.get('n_leaves')}")
    return 0 if ver[0] else 1


if __name__ == "__main__":
    raise SystemExit(main())
