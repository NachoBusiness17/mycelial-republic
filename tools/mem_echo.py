#!/usr/bin/env python3
"""mem_echo.py - the semantic echo lane (MagMemEcho).

Steal card: watch/inbox/link_drops_20261014/VAULT_MEMORY_LOOP_STEAL.md
(2026-10-14). The estate had organs without the loop: no sweep read its own
prose for the same idea written differently, months apart. This tool is that
loop, first pass:

1. walk watch/inbox/ for .md files, cap to the N most recent by mtime
   (default 3000 for the first pass)
2. embed the first 2000 chars of each via local ollama (/api/embeddings)
3. cache relpath -> {sha256, embedding, mtime} in an incremental state JSON
   (watch/inbox/mem_echo_state.json); re-embed only new or changed files
4. greedy cosine clustering at threshold 0.92, oldest file roots the cluster;
   keep clusters with >= 2 members whose mtimes span >= 14 days (cross-time
   echoes only; same-day near-copies are byte-dedupe's job, not ours)
5. write watch/inbox/mem_echo_report.md; clusters with >= 3 members are
   EMPHASIS per the operator's duplication-is-emphasis law (2026-09-14):
   "duplication is emphasis - find the nuance and put them all together."

Local and free: ollama embeddings, no paid calls. Falsifier (steal card): if
the first pass finds only byte-noise, the lane is dedupe by another name and
gets cut; genuine cross-month convergences earn its cadence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
PREFERRED_MODELS = ("nomic-embed-text", "mxbai-embed-large", "all-minilm")

_TL = threading.local()


def _session(base_url: str) -> requests.Session:
    sess = getattr(_TL, "session", None)
    if sess is None:
        sess = requests.Session()
        sess.mount(base_url, requests.adapters.HTTPAdapter(pool_maxsize=8))
        _TL.session = sess
    return sess


def embed_one(base_url: str, model: str, text: str, retries: int = 3) -> list[float]:
    sess = _session(base_url)
    payload = {"model": model, "prompt": text}
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            resp = sess.post(base_url + "/api/embeddings", json=payload, timeout=120)
            if resp.status_code == 200:
                emb = resp.json().get("embedding")
                if emb:
                    return emb
                raise RuntimeError("ollama returned an empty embedding")
            last_exc = RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        except Exception as exc:  # retried below, surfaced after the loop
            last_exc = exc
        time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"embed failed after {retries} attempts: {last_exc}")


def detect_model(base_url: str) -> str:
    resp = requests.get(base_url + "/api/tags", timeout=15)
    resp.raise_for_status()
    names = [m.get("name", "") for m in resp.json().get("models", [])]
    for want in PREFERRED_MODELS:
        for name in names:
            if name == want or name.split(":")[0] == want:
                return name
    for name in names:
        if "embed" in name.lower():
            return name
    raise SystemExit(
        "no embedding model in ollama; run: ollama pull nomic-embed-text (274MB, local, free)"
    )


def scan_md(root: Path, exclude: set[Path]) -> list[tuple[Path, float]]:
    found: list[tuple[Path, float]] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            path = Path(dirpath) / fn
            if path in exclude:
                continue
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            found.append((path, mtime))
    return found


def chunk_text(path: Path, chunk_chars: int) -> str:
    with path.open("rb") as handle:
        raw = handle.read(chunk_chars * 4)
    return raw.decode("utf-8", errors="replace")[:chunk_chars]


def first_line_snippet(text: str, width: int = 140) -> str:
    for line in text.splitlines():
        stripped = " ".join(line.split())
        if stripped:
            return stripped[:width]
    return "(empty file)"


def cluster_vectors(vectors: list[list[float]], order: list[int], threshold: float) -> list[list[int]]:
    """Greedy centroid clustering; each item joins the first cluster whose
    normalized centroid is within the cosine threshold, else opens a new one.
    `order` lists vector indices in insertion order (oldest mtime first) so
    the oldest echo roots each cluster."""
    mat = np.asarray(vectors, dtype=np.float32)
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    unit = mat / norms
    n = len(order)
    cents = np.zeros((n, unit.shape[1]), dtype=np.float32)
    sums: list[np.ndarray] = []
    assign = [-1] * n
    k = 0
    for i in order:
        if k:
            sims = cents[:k] @ unit[i]
            j = int(np.argmax(sims))
            if float(sims[j]) >= threshold:
                sums[j] = sums[j] + mat[i]
                denom = float(np.linalg.norm(sums[j]))
                cents[j] = sums[j] / (denom if denom else 1.0)
                assign[i] = j
                continue
        cents[k] = unit[i]
        sums.append(mat[i].copy())
        assign[i] = k
        k += 1
    groups: dict[int, list[int]] = {}
    for idx, cluster_id in enumerate(assign):
        groups.setdefault(cluster_id, []).append(idx)
    return list(groups.values())


def build_report(
    report_path: Path,
    args,
    model: str,
    dims: int,
    scanned: int,
    batch_n: int,
    embedded_now: int,
    cached: int,
    kept: list[dict],
) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    convergence = [c for c in kept if len(c["members"]) >= 3]
    echoes = [c for c in kept if len(c["members"]) == 2]
    lines: list[str] = []
    lines.append(f"# mem_echo report ({now})")
    lines.append("")
    lines.append(f"Semantic echo lane over {root} .md surfaces (steal card: ")
    lines.append("link_drops_20261014/VAULT_MEMORY_LOOP_STEAL.md). Same idea, different")
    lines.append("words, months apart. Cosine threshold "
                 f"{args.threshold}, cross-time gap >= {args.min_gap_days} days.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- scanned: {scanned} .md files under {root}/")
    lines.append(f"- batch: {batch_n} most recent by mtime")
    lines.append(f"- embedded this run: {embedded_now} (cached from state: {cached})")
    lines.append(f"- embedding model: {model} ({dims} dims, local ollama at {args.base_url})")
    lines.append(f"- chunk: first {args.chunk_chars} chars per file")
    lines.append(f"- cross-time echo clusters (>= 2 members, >= {args.min_gap_days}d span): {len(kept)}")
    lines.append(f"- convergence clusters (>= 3 members): {len(convergence)}")
    lines.append("")

    def render_cluster(out: list[str], cluster: dict, label: str) -> None:
        members = cluster["members"]
        out.append(f"### {label}: {len(members)} members, span {cluster['span_days']:.0f} days")
        out.append("")
        for member in members:
            mtime = datetime.fromtimestamp(member["mtime"]).strftime("%Y-%m-%d %H:%M")
            out.append(f"- `{member['rel']}` (mtime {mtime})")
        out.append("")
        out.append("First lines:")
        out.append("")
        for member in members:
            snippet = member["snippet"].replace("`", "'")
            out.append(f"- > {snippet}")
        out.append("")

    if convergence:
        lines.append("## EMPHASIS: convergence clusters (>= 3 members)")
        lines.append("")
        lines.append("Operator law (2026-09-14): duplication is emphasis - find the")
        lines.append("nuance and put them all together. An idea written three times")
        lines.append("independently is load-bearing and deserves one banked card.")
        lines.append("")
        for rank, cluster in enumerate(
            sorted(convergence, key=lambda c: (-len(c["members"]), -c["span_days"])), start=1
        ):
            render_cluster(lines, cluster, f"convergence {rank}")
    else:
        lines.append("## EMPHASIS: convergence clusters (>= 3 members)")
        lines.append("")
        lines.append("None found this pass.")
        lines.append("")

    lines.append(f"## Cross-time echoes (2 members, span >= {args.min_gap_days}d)")
    lines.append("")
    if echoes:
        for cluster in sorted(echoes, key=lambda c: -c["span_days"]):
            render_cluster(lines, cluster, "echo")
    else:
        lines.append("None found this pass.")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="semantic echo lane over watch/inbox prose")
    ap.add_argument("--root", default="watch/inbox")
    ap.add_argument("--state", default="watch/inbox/mem_echo_state.json")
    ap.add_argument("--report", default="watch/inbox/mem_echo_report.md")
    ap.add_argument("--base-url", default="http://localhost:11434")
    ap.add_argument("--model", default=None, help="embedding model (default: autodetect)")
    ap.add_argument("--cap", type=int, default=3000, help="max files this pass (most recent)")
    ap.add_argument("--chunk-chars", type=int, default=2000)
    ap.add_argument("--threshold", type=float, default=0.92)
    ap.add_argument("--min-gap-days", type=float, default=14.0)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args(argv)

    root = Path(args.root)
    if not root.is_absolute():
        root = REPO_ROOT / root
    state_path = Path(args.state)
    if not state_path.is_absolute():
        state_path = REPO_ROOT / state_path
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = REPO_ROOT / report_path

    model = args.model or detect_model(args.base_url)
    print(f"[mem_echo] model: {model}", flush=True)

    t0 = time.time()
    all_files = scan_md(root, exclude={state_path, report_path})
    scanned = len(all_files)
    print(f"[mem_echo] scanned {scanned} .md files in {time.time() - t0:.1f}s", flush=True)
    if not all_files:
        print("[mem_echo] nothing to do", flush=True)
        return 1

    all_files.sort(key=lambda t: t[1], reverse=True)
    batch = all_files[: args.cap]

    state: dict = {"version": 1, "model": model, "entries": {}}
    if state_path.exists():
        try:
            loaded = json.loads(state_path.read_text(encoding="utf-8"))
            if loaded.get("model") == model:
                state["entries"] = loaded.get("entries", {})
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[mem_echo] state unreadable ({exc}); rebuilding", flush=True)

    entries = state["entries"]
    chunk_of = lambda p: chunk_text(p, args.chunk_chars)  # noqa: E731 - small local helper

    to_embed: list[tuple[int, str, str]] = []  # (batch idx, relpath, sha)
    texts: dict[int, str] = {}
    batch_meta: list[tuple[str, float]] = []  # (relpath, mtime)
    vectors: list[list[float] | None] = [None] * len(batch)
    cached = 0

    for idx, (path, mtime) in enumerate(batch):
        rel = path.relative_to(REPO_ROOT).as_posix()
        batch_meta.append((rel, mtime))
        text = chunk_of(path)
        texts[idx] = text
        if len(text.strip()) < 20:
            continue  # stub or empty file; nothing to echo
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        entry = entries.get(rel)
        if entry and entry.get("sha256") == sha and entry.get("embedding"):
            vectors[idx] = entry["embedding"]
            cached += 1
        else:
            to_embed.append((idx, rel, sha))

    print(
        f"[mem_echo] batch {len(batch)}: {cached} cached, {len(to_embed)} to embed",
        flush=True,
    )

    embedded_now = 0
    t1 = time.time()

    def work(job: tuple[int, str, str]) -> tuple[int, list[float]]:
        idx, _rel, _sha = job
        raw = embed_one(args.base_url, model, texts[idx])
        return idx, [round(float(x), 5) for x in raw]

    if to_embed:
        dims = 0
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for done, (idx, vec) in enumerate(pool.map(work, to_embed), start=1):
                vectors[idx] = vec
                embedded_now += 1
                if not dims:
                    dims = len(vec)
                if done % 250 == 0 or done == len(to_embed):
                    rate = done / max(time.time() - t1, 0.001)
                    print(
                        f"[mem_echo] embedded {done}/{len(to_embed)} ({rate:.0f}/s)",
                        flush=True,
                    )

    # Persist state before clustering so embed spend survives a crash later.
    for job_idx, rel, sha in to_embed:
        vec = vectors[job_idx]
        if vec is None:
            continue
        entries[rel] = {"sha256": sha, "mtime": batch_meta[job_idx][1], "embedding": vec}
    state_path.write_text(json.dumps(state), encoding="utf-8")
    print(f"[mem_echo] state saved: {state_path}", flush=True)

    usable = [i for i, v in enumerate(vectors) if v is not None]
    if len(usable) < 2:
        print("[mem_echo] fewer than 2 embeddable files; no clusters possible", flush=True)
        return 1

    usable_vectors = [vectors[i] for i in usable]
    dims = len(usable_vectors[0])
    order = sorted(usable, key=lambda i: batch_meta[i][1])  # oldest roots the cluster
    pos_of = {batch_i: pos for pos, batch_i in enumerate(usable)}

    groups = cluster_vectors(usable_vectors, [pos_of[i] for i in order], args.threshold)

    min_gap = args.min_gap_days * 86400.0
    kept: list[dict] = []
    for members_pos in groups:
        if len(members_pos) < 2:
            continue
        members = []
        for pos in members_pos:
            batch_i = usable[pos]
            rel, mtime = batch_meta[batch_i]
            members.append(
                {
                    "rel": rel,
                    "mtime": mtime,
                    "snippet": first_line_snippet(texts[batch_i]),
                }
            )
        mtimes = [m["mtime"] for m in members]
        span = max(mtimes) - min(mtimes)
        if span < min_gap:
            continue  # same-window near-copies are boring
        kept.append({"members": members, "span_days": span / 86400.0})

    convergence_n = sum(1 for c in kept if len(c["members"]) >= 3)
    build_report(
        report_path, args, model, dims, scanned, len(batch), embedded_now, cached, kept
    )

    print("", flush=True)
    print("[mem_echo] summary", flush=True)
    print(f"  scanned .md files : {scanned}", flush=True)
    print(f"  batch (recent cap): {len(batch)}", flush=True)
    print(f"  embedded this run : {embedded_now}", flush=True)
    print(f"  cached            : {cached}", flush=True)
    print(f"  model             : {model} ({dims} dims)", flush=True)
    print(f"  echo clusters     : {len(kept)} (>= 2 members, >= {args.min_gap_days:.0f}d span)", flush=True)
    print(f"  convergence       : {convergence_n} (>= 3 members)", flush=True)
    print(f"  report            : {report_path}", flush=True)
    for cluster in sorted(kept, key=lambda c: (-len(c["members"]), -c["span_days"]))[:5]:
        heads = ", ".join(Path(m["rel"]).name for m in cluster["members"][:3])
        print(
            f"  cluster({len(cluster['members'])}, {cluster['span_days']:.0f}d): {heads}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
