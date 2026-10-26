"""Radix-leaf LRU prefix-cache simulator + estate tape loaders (library half).

This is the measurement engine of the G1 gap law null arm; the CLI that drives
it over the trail tapes is tools/lru_null_arm.py (split 2026-10-03 to keep both
files under the ratchet's 400-line bar - the first ratchet run on the merged
file read NEW file-too-long at :602, check log
watch/inbox/gala_20260925/build-it-all/lanes/m3-lru-null-arm.check.txt).

Law: memory/research_polished/kv_cache_compaction.md:13 - gap-fold G1: any
eviction/compaction claim must beat LRU/ARC/PBKV/Belady-MIN arms or it is
decoration. Semantics (vLLM/SGLang RadixAttention lineage):
  - the cache is a radix tree of full blocks; lookup walks block-by-block from
    the root and stops at the first absent block (a deeper block cannot exist
    above a missing ancestor);
  - every visited/created node is touched (request-granularity LRU clock);
  - eviction removes the least-recently-used LEAF only; when the evicted
    leaf's parent loses its last child, the parent remains cached as the
    shorter prefix and becomes evictable in turn;
  - the partial trailing block of a prompt is never inserted; its chars always
    count as miss (conservative, fixed).

All builders are deterministic: no RNG, no clock reads in the hot path - same
rows, same numbers, byte for byte.
"""
from __future__ import annotations

import glob
import hashlib
import heapq
import itertools
import json
from datetime import datetime
from pathlib import Path

SCHEMA = "lru_null_arm.v1"
CLIP_SUFFIX = "\n…(pack clipped)"  # estate clip shape, mag/context_pack.py:1416


# --------------------------------------------------------------------------
# Tape loading
# --------------------------------------------------------------------------

def load_rows(trails_dir: Path) -> tuple[list[dict], dict]:
    """Load every *.jsonl row under trails_dir. Returns (rows, inventory)."""
    rows: list[dict] = []
    files = sorted(glob.glob(str(trails_dir / "*.jsonl")))
    per_file: dict[str, int] = {}
    skipped_bad_ts = 0
    skipped_bad_json = 0
    for fp in files:
        lane = Path(fp).stem
        per_file[lane] = 0
        with open(fp, encoding="utf-8", errors="replace") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    raw = json.loads(line)
                except ValueError:
                    skipped_bad_json += 1
                    continue
                ts = str(raw.get("ts") or "")
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except ValueError:
                    skipped_bad_ts += 1
                    continue
                per_file[lane] += 1
                rows.append({
                    "dt": dt,
                    "ts": ts,
                    "lane": lane,
                    "line_no": line_no,
                    "actor": str(raw.get("actor") or "(none)"),
                    "event": str(raw.get("event") or "(none)"),
                    "detail": str(raw.get("detail") or "").replace("\n", " "),
                })
    inventory = {
        "trails_dir": str(trails_dir),
        "files": files,
        "rows_total": sum(per_file.values()),
        "rows_per_file": per_file,
        "skipped_bad_json": skipped_bad_json,
        "skipped_bad_ts": skipped_bad_ts,
    }
    return rows, inventory


def most_recent_chronological(rows: list[dict], limit: int) -> list[dict]:
    """Most recent `limit` rows by ts, returned oldest-first (serving order)."""
    ordered = sorted(rows, key=lambda r: (r["dt"], r["lane"], r["line_no"]))
    if limit and len(ordered) > limit:
        ordered = ordered[-limit:]
    return ordered


# --------------------------------------------------------------------------
# Sessions + prompt building
# --------------------------------------------------------------------------

def assign_sessions(rows: list[dict], gap_min: float) -> tuple[list[dict], int]:
    """Tag each row with session_n (per lane+actor, gap-broken). One pass."""
    gap_s = gap_min * 60.0
    last_dt: dict[tuple[str, str], datetime] = {}
    sess_n: dict[tuple[str, str], int] = {}
    n_sessions = 0
    for r in rows:
        key = (r["lane"], r["actor"])
        prev = last_dt.get(key)
        if prev is None or (r["dt"] - prev).total_seconds() > gap_s:
            sess_n[key] = sess_n.get(key, 0) + 1
            n_sessions += 1
        r["session"] = sess_n[key]
        last_dt[key] = r["dt"]
    return rows, n_sessions


def _frozen_prefix(lane: str, actor: str, budget: int, frozen_chars: int) -> str:
    """Deterministic frozen prefix per (lane, actor), realistic-sized.

    Synthetic by design (see tools/lru_null_arm.py docstring): bytes derive
    ONLY from (lane, actor, budget, frozen_chars) - never from row data - so
    the prefix is byte-identical across sessions exactly like the A2 frozen
    prompt is.
    """
    head = (f"[FROZEN-PREFIX mode=janitor lane={lane} actor={actor} "
            f"pack_budget={budget} law=context_pack_A2]")
    seed = hashlib.sha256(f"{lane}|{actor}|{budget}".encode("utf-8")).hexdigest()
    filler_line = f"law-line {seed[:16]}: the context prefix is the unit of economics; "
    body = filler_line * (max(0, frozen_chars) // max(1, len(filler_line)) + 1)
    return (head + "\n" + body)[:max(0, frozen_chars)]


def _event_line(r: dict) -> str:
    return f"[{r['ts']}] {r['actor']} {r['event']}: {r['detail']}"


def _clip_keep_head(text: str, budget: int) -> str:
    """Estate hard clip, mag/context_pack.py:1414-1416 shape."""
    if len(text) <= budget:
        return text
    return text[: max(0, budget - len(CLIP_SUFFIX))] + CLIP_SUFFIX


def build_prompt_sets(rows: list[dict], *, budget: int, frozen_chars: int,
                      arms: list[str]) -> tuple[dict[str, list[str]], dict]:
    """One prompt per row per arm, in replay order. Returns (prompts, meta)."""
    transcripts: dict[tuple[str, str, int], list[str]] = {}
    prompts: dict[str, list[str]] = {a: [] for a in arms}
    frozen_cache: dict[tuple[str, str], str] = {}
    frozen_hashes: dict[str, str] = {}
    for r in rows:
        key2 = (r["lane"], r["actor"])
        key3 = (r["lane"], r["actor"], r["session"])
        tlist = transcripts.setdefault(key3, [])
        tlist.append(_event_line(r))
        frozen = frozen_cache.get(key2)
        if frozen is None:
            frozen = _frozen_prefix(r["lane"], r["actor"], budget, frozen_chars)
            frozen_cache[key2] = frozen
            frozen_hashes[f"{r['lane']}/{r['actor']}"] = hashlib.sha256(
                frozen.encode("utf-8")).hexdigest()
        if "frozen_append" in prompts:
            prompts["frozen_append"].append(
                _clip_keep_head(frozen + "\n" + "\n".join(tlist), budget))
        if "frozen_window" in prompts:
            window = max(0, budget - len(frozen) - len(CLIP_SUFFIX))
            tail = ("\n".join(tlist))[-window:] if window else ""
            prompts["frozen_window"].append(
                _clip_keep_head(frozen + tail, budget))
        if "volatile" in prompts:
            vol = (f"[PACK ts={r['ts']} lane={r['lane']} actor={r['actor']} "
                   f"pack_budget={budget}]")
            window = max(0, budget - len(vol) - len(CLIP_SUFFIX))
            tail = ("\n".join(tlist))[-window:] if window else ""
            prompts["volatile"].append(_clip_keep_head(vol + tail, budget))
    meta = {
        "frozen_chars": frozen_chars,
        "frozen_prefix_sha256_by_lane_actor": frozen_hashes,
        "clip_suffix": CLIP_SUFFIX,
    }
    return prompts, meta


# --------------------------------------------------------------------------
# Radix-leaf LRU prefix cache simulator
# --------------------------------------------------------------------------

class _Node:
    __slots__ = ("block", "parent", "children", "last_used")

    def __init__(self, block: str, parent: "_Node | None"):
        self.block = block
        self.parent = parent
        self.children: dict[str, "_Node"] = {}
        self.last_used = -1


class RadixLeafLRU:
    """Radix tree over full blocks, leaf-only LRU eviction (see module doc)."""

    def __init__(self, capacity_blocks: int | None, block_chars: int):
        if capacity_blocks is not None and capacity_blocks < 1:
            raise ValueError("capacity_blocks must be >= 1 or None")
        self.capacity = capacity_blocks
        self.block_chars = block_chars
        self.root = _Node("", None)
        self._heap: list[tuple[int, int, _Node]] = []
        self._seq = itertools.count()
        self._clock = 0
        self.n_cached = 0
        self.evictions = 0

    # -- internals ---------------------------------------------------------

    def _touch(self, node: _Node) -> None:
        node.last_used = self._clock
        if not node.children:  # a leaf is evictable at its new recency
            heapq.heappush(self._heap, (node.last_used, next(self._seq), node))

    def _pop_lru_leaf(self) -> _Node:
        while self._heap:
            last_used, _seq, node = heapq.heappop(self._heap)
            if (node.parent is not None and not node.children
                    and node.last_used == last_used):
                return node
            # stale entry (touched, became internal, or already evicted): skip
        raise RuntimeError("eviction with no cached leaf: impossible state")

    def _evict_until_under(self) -> None:
        while self.capacity is not None and self.n_cached > self.capacity:
            node = self._pop_lru_leaf()
            parent = node.parent
            assert parent is not None and node.block in parent.children
            del parent.children[node.block]
            node.parent = None
            self.n_cached -= 1
            self.evictions += 1
            if parent is not self.root and not parent.children:
                # parent just became a leaf; it stays cached (shorter prefix)
                heapq.heappush(self._heap,
                               (parent.last_used, next(self._seq), parent))

    # -- API ---------------------------------------------------------------

    def request(self, prompt: str) -> tuple[int, int, bool]:
        """Serve one prompt. Returns (hit_chars, total_chars, full_hit)."""
        self._clock += 1
        n_full = len(prompt) // self.block_chars
        node = self.root
        hit_blocks = 0
        for i in range(n_full):
            block = prompt[i * self.block_chars:(i + 1) * self.block_chars]
            child = node.children.get(block)
            if child is None:
                break
            node = child
            self._touch(node)
            hit_blocks += 1
        for i in range(hit_blocks, n_full):
            block = prompt[i * self.block_chars:(i + 1) * self.block_chars]
            child = _Node(block, node)
            node.children[block] = child
            node = child
            self._touch(node)
            self.n_cached += 1
        self._evict_until_under()
        hit_chars = hit_blocks * self.block_chars
        total = len(prompt)
        return hit_chars, total, hit_chars == total


def replay(prompts: list[str], *, capacity_blocks: int | None,
           block_chars: int) -> dict:
    """Fresh-cache replay of a prompt sequence. Returns the stats dict."""
    sim = RadixLeafLRU(capacity_blocks, block_chars)
    total_chars = 0
    hit_chars = 0
    full_hits = 0
    for p in prompts:
        h, t, full = sim.request(p)
        total_chars += t
        hit_chars += h
        full_hits += 1 if full else 0
    return {
        "capacity_blocks": capacity_blocks,
        "capacity_chars": (None if capacity_blocks is None
                           else capacity_blocks * block_chars),
        "requests": len(prompts),
        "total_chars": total_chars,
        "hit_chars": hit_chars,
        "hit_rate": round(hit_chars / total_chars, 6) if total_chars else 0.0,
        "full_hit_rate": round(full_hits / len(prompts), 6) if prompts else 0.0,
        "evictions": sim.evictions,
        "final_cached_blocks": sim.n_cached,
    }


# --------------------------------------------------------------------------
# Self-test (synthetic, deterministic)
# --------------------------------------------------------------------------

def self_test() -> tuple[list[str], int]:
    """Unit battery for the simulator + clip shape. Returns (failures, n)."""
    failures: list[str] = []
    n_checks = 0

    def check(name: str, cond: bool, detail: str = "") -> None:
        nonlocal n_checks
        n_checks += 1
        if not cond:
            failures.append(f"{name}: {detail}")

    # 1. block-granular prefix sharing
    sim = RadixLeafLRU(None, 4)
    sim.request("AAAA")
    h, t, _ = sim.request("AAAAB")  # second block "AAAAB"[4:] = "B" partial
    check("prefix_share", h == 4 and t == 5, f"hit={h} total={t}")

    # 2. LRU evicts the least recently used leaf
    sim = RadixLeafLRU(2, 4)
    sim.request("AAAA")   # cached A
    sim.request("BBBB")   # cached B
    sim.request("CCCC")   # evicts A (oldest), caches C
    h, _, _ = sim.request("BBBB")  # full hit; a hit inserts nothing
    check("lru_keeps_recent", h == 4, f"hit={h}")
    h, _, _ = sim.request("AAAA")  # miss; this insert evicts C (LRU leaf:
    check("lru_evicts_oldest", h == 0, f"hit={h}")  # untouched since req3)
    h, _, _ = sim.request("BBBB")  # B survived: touched at req4, more recent
    check("lru_evict_cascade", h == 4, f"hit={h}")  # than C

    # 3. leaf-only eviction: internal (prefix) block survives
    sim = RadixLeafLRU(1, 4)
    sim.request("AAAABBBB")   # 2 blocks; evicts leaf BBBB, keeps AAAA
    h, t, _ = sim.request("AAAACCCC")  # AAAA cached, CCCC new
    check("internal_survives", h == 4 and t == 8, f"hit={h} total={t}")
    h, _, _ = sim.request("BBBBDDDD")
    check("evicted_leaf_gone", h == 0, f"hit={h}")

    # 4. append-only growth: second turn mostly hits
    sim = RadixLeafLRU(None, 64)
    p1 = "X" * 256
    p2 = p1 + "Y" * 192
    sim.request(p1)
    h2, t2, _ = sim.request(p2)
    check("append_only_hits", h2 == 256 and t2 == 448, f"hit={h2} total={t2}")

    # 5. estate clip shape
    clipped = _clip_keep_head("Z" * 6000, 4800)
    check("clip_shape", len(clipped) == 4800 and clipped.endswith("(pack clipped)"),
          f"len={len(clipped)} tail={clipped[-20:]!r}")
    unclipped = _clip_keep_head("Z" * 100, 4800)
    check("clip_noop", unclipped == "Z" * 100, "short text must pass through")

    # 6. capacity floor and determinism
    sim = RadixLeafLRU(1, 4)
    sim.request("AAAA")
    sim.request("BBBB")
    check("capacity_honored", sim.n_cached <= 1, f"cached={sim.n_cached}")
    a = replay(["AAAA", "BBBB", "AAAA"], capacity_blocks=2, block_chars=4)
    b = replay(["AAAA", "BBBB", "AAAA"], capacity_blocks=2, block_chars=4)
    check("determinism", a == b, "same input must give identical stats")

    return failures, n_checks
