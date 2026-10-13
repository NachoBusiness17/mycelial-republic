"""EmbeddingGemma 2 pull + embedder + ledger sidecar (GPS embedding lane).

Operator order (2026-10-06): pull EmbeddingGemma 2 (text tower only,
no vision/audio inference), embed every distinct task_shape in
tools/gps_mcp/gps_ledger.db3 verdict_log into a sidecar. The trial that
races string-key routing against kNN over these vectors lives in
tools/gps_mcp/gps_embed_trial.py (same lane, split at landing so the
violation ratchet's 400-line law stays green; receipt watch/inbox/
gps_embed/GPS_EMBED_TRIAL.md).

Pull provenance (why ONNX): the venv's transformers 5.15.0 predates the
`embedding_gemma2` architecture (verified: no
transformers.models.embedding_gemma2; CONFIG_MAPPING_NAMES lacks both
`embedding_gemma2` and `embedding_gemma2_text`), and the google/
embeddinggemma-2 Hub repo ships no remote-code .py files, so
trust_remote_code=True cannot load it either. The order's sanctioned
fallback is the minimal ONNX path: the official export
onnx-community/embeddinggemma-2-ONNX (fp32 primary; q4 pulled as a
secondary timing arm only) under onnxruntime CPU. Media towers never
execute: the graph declares image/video/audio feature inputs as
required, so they are fed zero-sized tensors (0 tokens), which the
graph accepts, and the exported graph itself emits the already
L2-normalized `sentence_embedding` [batch, 768] (mean pooling + 512
to 768 projection inside the graph; norms verified == 1.0).

Task prefix (model card, symmetric tasks): every embedded text uses
"task: clustering | query: {text}" - the same prefix on every compared
input, the card's prescribed configuration for clustering/kNN use.

Sidecar: memory/runs/gps_embed/vectors.db3, keyed
(task_shape, verdict, model_id) per the order, with the distinct-shape
vector stored once in shape_vectors and referenced by row count in
vectors.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Sequence

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
GPS_DIR = REPO_ROOT / "tools" / "gps_mcp"
DEFAULT_LEDGER = GPS_DIR / "gps_ledger.db3"
DEFAULT_CONFIG = GPS_DIR / "config.json"
DEFAULT_MODEL_DIR = REPO_ROOT / "models" / "embeddinggemma-2-onnx"
FP32_ONNX = "onnx/model.onnx"
Q4_ONNX = "onnx/model_q4.onnx"
RUN_DIR = REPO_ROOT / "memory" / "runs" / "gps_embed"
DEFAULT_SIDECAR = RUN_DIR / "vectors.db3"

# Model card (onnx-community/embeddinggemma-2-ONNX README, "Task
# Instruction Prefixes"): symmetric tasks apply the same prefix to all
# compared inputs; clustering is the task class this lane serves.
TASK_PREFIX = "task: clustering | query: "

EMBEDDER_ID = "google/embeddinggemma-2 via onnx-community/embeddinggemma-2-ONNX (fp32 CPU)"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def prefixed(text: str) -> str:
    return f"{TASK_PREFIX}{text}"


class EmbeddingGemma2ONNX:
    """EmbeddingGemma 2 text embeddings via the official ONNX export.

    Text-only by construction: input_ids + attention_mask are fed real
    values and the three media feature inputs are fed zero-sized
    tensors, so no vision/audio path executes. Output is the graph's
    `sentence_embedding`, already L2-normalized (verified norms == 1.0).
    Determinism (receipt GPS_EMBED_TRIAL.md + tests/test_gps_embed_
    trial.py): same input twice is bit-identical in-session and across
    fresh session loads.
    """

    def __init__(self, model_dir: Path | str = DEFAULT_MODEL_DIR, onnx_rel: str = FP32_ONNX):
        self.model_dir = Path(model_dir)
        self.onnx_path = self.model_dir / onnx_rel
        if not self.onnx_path.exists():
            raise FileNotFoundError(
                f"{self.onnx_path} missing: pull it first "
                "(snapshot_download onnx-community/embeddinggemma-2-ONNX)"
            )
        import onnxruntime as ort
        from transformers import AutoTokenizer

        # The tokenizer-only load prints a benign "model of type
        # embedding_gemma2" notice under transformers 5.15: no model
        # class is instantiated, only the fast tokenizer files.
        self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_dir))
        opts = ort.SessionOptions()
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(
            str(self.onnx_path), opts, providers=["CPUExecutionProvider"]
        )
        self.media_zero = {
            "image_features": np.zeros((0, 512), dtype=np.float32),
            "video_features": np.zeros((0, 512), dtype=np.float32),
            "audio_features": np.zeros((0, 512), dtype=np.float32),
        }

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        """Normalized (len(texts), 768) float32 embeddings."""
        encoded = self.tokenizer(
            [prefixed(t) for t in texts], padding=True, return_tensors="np"
        )
        feed = {
            "input_ids": encoded["input_ids"].astype(np.int64),
            "attention_mask": encoded["attention_mask"].astype(np.int64),
            **self.media_zero,
        }
        out = self.session.run(["sentence_embedding"], feed)[0]
        return np.asarray(out, dtype=np.float32)


SIDECAR_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS shape_vectors (
    task_shape TEXT PRIMARY KEY,
    dim        INTEGER NOT NULL,
    vector     BLOB NOT NULL,
    embedder   TEXT NOT NULL,
    prefix     TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS vectors (
    task_shape TEXT NOT NULL,
    verdict    INTEGER NOT NULL,
    model_id   TEXT NOT NULL,
    n_rows     INTEGER NOT NULL,
    vector     BLOB NOT NULL,
    dim        INTEGER NOT NULL,
    PRIMARY KEY (task_shape, verdict, model_id)
);
"""


def ledger_distinct_groups(ledger_db: Path | str) -> list[dict[str, Any]]:
    """(task_shape, verdict, model_id, n_rows) groups, read-only."""
    con = sqlite3.connect(f"file:{ledger_db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(
            "SELECT task_shape, verdict, model_id, COUNT(*) AS n_rows"
            " FROM verdict_log GROUP BY task_shape, verdict, model_id"
            " ORDER BY task_shape, verdict, model_id"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        con.close()


def ledger_total_rows(ledger_db: Path | str) -> int:
    con = sqlite3.connect(f"file:{ledger_db}?mode=ro", uri=True)
    try:
        return int(con.execute("SELECT COUNT(*) FROM verdict_log").fetchone()[0])
    finally:
        con.close()


def build_sidecar(
    ledger_db: Path | str = DEFAULT_LEDGER,
    sidecar_db: Path | str = DEFAULT_SIDECAR,
    model_dir: Path | str = DEFAULT_MODEL_DIR,
    onnx_rel: str = FP32_ONNX,
    embedder: Optional[EmbeddingGemma2ONNX] = None,
) -> dict[str, Any]:
    """Embed each DISTINCT task_shape once; key vectors by
    (task_shape, verdict, model_id) row groups. Idempotent (INSERT OR
    REPLACE; a re-run re-embeds and overwrites, never grows; proven by
    tests/test_gps_embed_trial.py::test_sidecar_build_idempotence)."""
    if embedder is None:
        embedder = EmbeddingGemma2ONNX(model_dir, onnx_rel)
    ledger_db = Path(ledger_db)
    sidecar_db = Path(sidecar_db)
    sidecar_db.parent.mkdir(parents=True, exist_ok=True)
    groups = ledger_distinct_groups(ledger_db)
    shapes = sorted({g["task_shape"] for g in groups})
    t0 = time.perf_counter()
    vectors = embedder.embed(shapes)
    embed_ms = (time.perf_counter() - t0) * 1000.0
    blob_by_shape = {
        s: np.ascontiguousarray(vectors[i]).tobytes() for i, s in enumerate(shapes)
    }
    con = sqlite3.connect(sidecar_db)
    try:
        with con:
            con.executescript(SIDECAR_SCHEMA)
            ts = utc_now_iso()
            meta = {
                "embedder": EMBEDDER_ID if onnx_rel == FP32_ONNX else f"{EMBEDDER_ID} [{onnx_rel}]",
                "onnx_file": str(Path(model_dir) / onnx_rel),
                "onnx_sha256": sha256_file(Path(model_dir) / onnx_rel),
                "dim": str(vectors.shape[1]),
                "prefix": TASK_PREFIX,
                "source_ledger": str(ledger_db),
                "ledger_total_rows": str(ledger_total_rows(ledger_db)),
                "distinct_shapes": str(len(shapes)),
                "distinct_groups": str(len(groups)),
                "embed_ms_all_shapes": f"{embed_ms:.1f}",
                "built_at": ts,
            }
            for k, v in meta.items():
                con.execute(
                    "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (k, v)
                )
            for s in shapes:
                con.execute(
                    "INSERT OR REPLACE INTO shape_vectors"
                    " (task_shape, dim, vector, embedder, prefix, updated_at)"
                    " VALUES (?, ?, ?, ?, ?, ?)",
                    (s, vectors.shape[1], blob_by_shape[s], meta["embedder"], TASK_PREFIX, ts),
                )
            for g in groups:
                con.execute(
                    "INSERT OR REPLACE INTO vectors"
                    " (task_shape, verdict, model_id, n_rows, vector, dim)"
                    " VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        g["task_shape"],
                        int(g["verdict"]),
                        g["model_id"],
                        int(g["n_rows"]),
                        blob_by_shape[g["task_shape"]],
                        vectors.shape[1],
                    ),
                )
    finally:
        con.close()
    return {
        "sidecar": str(sidecar_db),
        "shapes_embedded": len(shapes),
        "groups_written": len(groups),
        "dim": int(vectors.shape[1]),
        "embed_ms_all_shapes": round(embed_ms, 1),
        "meta": meta,
    }


def load_sidecar_vectors(sidecar_db: Path | str) -> dict[str, np.ndarray]:
    con = sqlite3.connect(f"file:{sidecar_db}?mode=ro", uri=True)
    try:
        rows = con.execute("SELECT task_shape, vector FROM shape_vectors").fetchall()
        return {s: np.frombuffer(b, dtype=np.float32) for s, b in rows}
    finally:
        con.close()


def _cli(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="tools.gps_mcp.gps_embed")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pull-info", help="shas + sizes of the pulled model files")
    sub.add_parser("embed", help="build/refresh the vectors sidecar")
    args = parser.parse_args(argv)

    if args.cmd == "pull-info":
        for rel in (
            FP32_ONNX,
            "onnx/model.onnx_data",
            Q4_ONNX,
            "onnx/model_q4.onnx_data",
            "tokenizer.json",
        ):
            p = DEFAULT_MODEL_DIR / rel
            if p.exists():
                print(f"{rel:28s} {p.stat().st_size:>12d} B  sha256={sha256_file(p)}")
            else:
                print(f"{rel:28s} MISSING")
        return 0
    print(json.dumps(build_sidecar(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_cli())
