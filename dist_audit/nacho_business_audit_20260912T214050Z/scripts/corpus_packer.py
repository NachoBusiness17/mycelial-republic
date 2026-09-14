#!/usr/bin/env python3
"""EXP-BRAIN-01 corpus-enhancement packer (gopher grok-1).

Read-only on docs/ and memory/. Writes only under state/vast/.
No network, no API keys. Stdlib only — safe on a secretless GPU box.

Run: .venv\\Scripts\\python.exe scripts\\corpus_packer.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "state" / "vast"
PACKS_DIR = OUT_DIR / "corpus_packs"
INVENTORY_PATH = OUT_DIR / "corpus_inventory.json"
QUESTIONS_PATH = OUT_DIR / "corpus_questions.json"

# 4000-token packs for an 8192-ctx serve, leaving room for the question.
MAX_PACK_TOKENS = 4000
HEADER_RESERVE_TOKENS = 160
BODY_TOKEN_BUDGET = MAX_PACK_TOKENS - HEADER_RESERVE_TOKENS
CHARS_PER_TOKEN = 4
NEAR_DUP_HAMMING = 3
TOP_PACKS_PER_THEME = 20
QUESTIONS_PER_THEME = 10
STALE_DAYS = 30

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".csv",
    ".html",
    ".htm",
    ".rst",
    ".xml",
    ".prompt",
}

THEMES: list[dict[str, Any]] = [
    {
        "id": 0,
        "name": "contradictions between documents",
        "keywords": (
            "contradict", "contradiction", "conflict", "conflicts", "disagree",
            "disagreement", "contrary", "versus", " vs ", "instead", "supersede",
            "superseded", "retract", "retracted", "reverse", "reversed", "obsolete",
            "however", "on the other hand", "but actually", "not the case",
            "dispute", "disputed", "unproven", "supported", "disagrees",
            "in tension", "mutually exclusive", "can't both", "cannot both",
            "was wrong", "corrects", "correction", "override", "overridden",
            "no longer", "deprecated", "replaced by", "replaces",
        ),
    },
    {
        "id": 1,
        "name": "stale claims with dates older than 30 days",
        "keywords": (
            "as of", "as-of", "dated", "stale", "outdated", "out of date",
            "formerly", "previously", "old claim", "last updated", "snapshot",
            "at the time", "was current", "no longer current", "expired",
            "2025-", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05",
            "2026-06", "2026-07", "yesterday", "last month", "last week",
        ),
    },
    {
        "id": 2,
        "name": "unfalsifiable or missing receipts",
        "keywords": (
            "unproven", "unfalsifiable", "no receipt", "missing receipt",
            "without receipt", "no evidence", "no test", "no measure",
            "not measured", "tbd", "todo", "someday", "we will", "we should",
            "believe", "obviously", "clearly", "always", "never", "must be",
            "hypothesis", "hypothes", "vision", "inevitably", "certainly",
            "no cite", "citation needed", "ungrounded", "faith", "vibes",
            "assert", "assumes", "assumed", "no bytes", "not verified",
            "unverified", "anecdote", "anecdotal", "handwave",
        ),
    },
    {
        "id": 3,
        "name": "overlapping scope / duplicate work",
        "keywords": (
            "duplicate", "duplicat", "overlap", "overlapping", "same as",
            "already", "reuse", "reuses", "parallel", "also covers",
            "same goal", "same work", "copy of", "mirror of", "similar to",
            "another pass", "v2", "v3", "v4", "v5", "reimplementation",
            "rewrite", "fork", "steal", "ilap", "same protocol", "twice",
            "redundant", "near-identical", "repeat", "repeated",
        ),
    },
]

ISO_DATE_RE = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")
COMPACT_DATE_RE = re.compile(r"\b(20\d{2})(\d{2})(\d{2})T")
YEAR_MONTH_RE = re.compile(r"\b(20\d{2})-(\d{2})\b")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"“(\[])")
WORD_RE = re.compile(r"[a-z0-9]{3,}")
HEADING_OR_BLANK_RE = re.compile(r"(?m)(?=^#{1,6}\s)|\n{2,}")

KEY_PATTERNS = [
    re.compile(r"xai-[A-Za-z0-9]{16,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"gsk_[A-Za-z0-9]{16,}"),
    re.compile(r"AIza[A-Za-z0-9_-]{16,}"),
    re.compile(r"hf_[A-Za-z0-9]{16,}"),
    re.compile(r"ghp_[A-Za-z0-9]{16,}"),
    re.compile(r"gho_[A-Za-z0-9]{16,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{16,}"),
    re.compile(r"glpat-[A-Za-z0-9_-]{12,}"),
    re.compile(r"dop_v1_[a-f0-9]{32,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    re.compile(r"VAST_API_KEY\s*=\s*\S+"),
    re.compile(r"OPENROUTER_API_KEY\s*=\s*\S+"),
]

JSON_TEXT_KEYS = {
    "title",
    "ask",
    "answer",
    "prompt",
    "excerpt",
    "text",
    "summary",
    "hypothesis",
    "content",
    "body",
    "markdown",
    "criterion",
    "note",
    "goal",
    "question",
    "claim",
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def estimate_tokens(text: str) -> int:
    """House heuristic: ~4 chars/token (mag.token_economy)."""
    if not text:
        return 0
    return max(0, (len(text) + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN)


def redact_secrets(text: str) -> str:
    out = text
    for pat in KEY_PATTERNS:
        out = pat.sub("[REDACTED-KEY]", out)
    return out


def rel_posix(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def iter_corpus_files() -> list[Path]:
    """docs/ref/*.md + docs/concepts/*.md + memory/research_packs/* (recursive)."""
    files: list[Path] = []
    seen: set[Path] = set()

    def add(path: Path) -> None:
        try:
            resolved = path.resolve()
        except OSError:
            return
        if resolved in seen or not resolved.is_file():
            return
        seen.add(resolved)
        files.append(resolved)

    ref = ROOT / "docs" / "ref"
    if ref.is_dir():
        for p in sorted(ref.rglob("*.md")):
            add(p)

    concepts = ROOT / "docs" / "concepts"
    if concepts.is_dir():
        for p in sorted(concepts.rglob("*.md")):
            add(p)

    packs = ROOT / "memory" / "research_packs"
    if packs.is_dir():
        for p in sorted(packs.rglob("*")):
            if p.is_file() and p.name != ".gitkeep":
                add(p)

    return files


def source_rank(rel: str) -> int:
    if rel.startswith("docs/ref/"):
        return 0
    if rel.startswith("docs/concepts/"):
        return 1
    return 2


def build_inventory(files: list[Path]) -> dict[str, Any]:
    by_root: dict[str, dict[str, int]] = defaultdict(lambda: {"files": 0, "bytes": 0})
    by_ext: dict[str, dict[str, int]] = defaultdict(lambda: {"files": 0, "bytes": 0})
    records: list[dict[str, Any]] = []
    total_bytes = 0
    for path in files:
        try:
            st = path.stat()
        except OSError:
            continue
        rel = rel_posix(path)
        if rel.startswith("docs/ref/"):
            root_name = "docs/ref"
        elif rel.startswith("docs/concepts/"):
            root_name = "docs/concepts"
        elif rel.startswith("memory/research_packs/"):
            root_name = "memory/research_packs"
        else:
            root_name = "other"
        ext = path.suffix.lower() or "(none)"
        n = int(st.st_size)
        total_bytes += n
        by_root[root_name]["files"] += 1
        by_root[root_name]["bytes"] += n
        by_ext[ext]["files"] += 1
        by_ext[ext]["bytes"] += n
        mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
        records.append(
            {
                "path": rel,
                "bytes": n,
                "mtime": iso_z(mtime),
                "ext": ext,
                "root": root_name,
            }
        )
    return {
        "experiment": "EXP-BRAIN-01",
        "generated_at": iso_z(now_utc()),
        "roots": ["docs/ref/**/*.md", "docs/concepts/**/*.md", "memory/research_packs/**"],
        "file_count": len(records),
        "total_bytes": total_bytes,
        "by_root": dict(by_root),
        "by_ext": dict(by_ext),
        "files": records,
    }


def is_probably_binary(sample: bytes) -> bool:
    if not sample:
        return False
    if b"\x00" in sample:
        return True
    # high ratio of non-text bytes
    textish = sum(1 for b in sample if b in (9, 10, 13) or 32 <= b < 127)
    return textish / max(1, len(sample)) < 0.75


def load_text(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix not in TEXT_SUFFIXES:
        return None
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if is_probably_binary(raw[:8192]):
        return None
    text = raw.decode("utf-8", errors="replace")
    if suffix in {".json", ".jsonl"}:
        extracted = extract_json_text(text, suffix)
        if extracted.strip():
            text = extracted
    return redact_secrets(text)


def extract_json_text(raw: str, suffix: str) -> str:
    blobs: list[str] = []
    if suffix == ".jsonl":
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                blobs.append(line)
                continue
            blobs.extend(_walk_json_strings(obj))
        return "\n\n".join(blobs)
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    blobs.extend(_walk_json_strings(obj))
    return "\n\n".join(blobs) if blobs else raw


def _walk_json_strings(obj: Any, key: str | None = None) -> list[str]:
    out: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(_walk_json_strings(v, str(k)))
    elif isinstance(obj, list):
        for item in obj:
            out.extend(_walk_json_strings(item, key))
    elif isinstance(obj, str):
        s = obj.strip()
        if not s:
            return out
        k = (key or "").lower()
        if k in JSON_TEXT_KEYS or len(s) >= 80:
            if k:
                out.append(f"{k}: {s}")
            else:
                out.append(s)
    return out


def split_units(text: str) -> list[str]:
    parts = [p.strip() for p in HEADING_OR_BLANK_RE.split(text) if p and p.strip()]
    return parts or ([text.strip()] if text.strip() else [])


def hard_wrap(unit: str, budget_tokens: int) -> list[str]:
    budget_chars = max(64, budget_tokens * CHARS_PER_TOKEN)
    if estimate_tokens(unit) <= budget_tokens:
        return [unit]
    sentences = [s.strip() for s in SENTENCE_RE.split(unit) if s.strip()]
    if not sentences:
        sentences = [unit]
    chunks: list[str] = []
    buf: list[str] = []
    size = 0
    for sent in sentences:
        extra = len(sent) + (1 if buf else 0)
        if buf and size + extra > budget_chars:
            chunks.append(" ".join(buf))
            buf = [sent]
            size = len(sent)
        else:
            buf.append(sent)
            size += extra
    if buf:
        chunks.append(" ".join(buf))
    # still oversize (one huge sentence) — slice by chars
    final: list[str] = []
    for ch in chunks:
        if estimate_tokens(ch) <= budget_tokens:
            final.append(ch)
            continue
        step = budget_chars
        for i in range(0, len(ch), step):
            piece = ch[i : i + step].strip()
            if piece:
                final.append(piece)
    return final


def chunk_text(text: str) -> list[str]:
    units = split_units(text)
    chunks: list[str] = []
    buf: list[str] = []
    buf_text = ""

    def flush() -> None:
        nonlocal buf, buf_text
        if buf:
            chunks.append(buf_text)
            buf = []
            buf_text = ""

    for unit in units:
        if estimate_tokens(unit) > BODY_TOKEN_BUDGET:
            flush()
            chunks.extend(hard_wrap(unit, BODY_TOKEN_BUDGET))
            continue
        candidate = unit if not buf else buf_text + "\n\n" + unit
        if buf and estimate_tokens(candidate) > BODY_TOKEN_BUDGET:
            flush()
            buf = [unit]
            buf_text = unit
        else:
            buf.append(unit)
            buf_text = candidate
    flush()
    return [c for c in chunks if c.strip()]


def normalize_text(text: str) -> str:
    t = text.lower()
    t = re.sub(r"```[\s\S]*?```", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _fnv64(data: str) -> int:
    h = 14695981039346656037
    for b in data.encode("utf-8"):
        h ^= b
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h


def simhash64(text: str) -> int:
    tokens = WORD_RE.findall(text.lower())
    if not tokens:
        return 0
    acc = [0] * 64
    n = len(tokens)
    for i in range(n):
        if i + 2 < n:
            shingle = tokens[i] + " " + tokens[i + 1] + " " + tokens[i + 2]
        else:
            shingle = tokens[i]
        h = _fnv64(shingle)
        for bit in range(64):
            acc[bit] += 1 if (h >> bit) & 1 else -1
    out = 0
    for bit in range(64):
        if acc[bit] > 0:
            out |= 1 << bit
    return out


def hamming64(a: int, b: int) -> int:
    return (a ^ b).bit_count()


class Chunk:
    __slots__ = (
        "source",
        "chunk_index",
        "chunk_count",
        "text",
        "tokens",
        "sha256",
        "simhash",
        "mtime",
        "dates",
        "dup_of",
    )

    def __init__(
        self,
        source: str,
        chunk_index: int,
        chunk_count: int,
        text: str,
        mtime: datetime,
    ) -> None:
        self.source = source
        self.chunk_index = chunk_index
        self.chunk_count = chunk_count
        self.text = text
        self.tokens = estimate_tokens(text)
        norm = normalize_text(text)
        self.sha256 = sha256_hex(norm or text)
        self.simhash = simhash64(norm) if len(norm) >= 40 else 0
        self.mtime = mtime
        self.dates = extract_dates(text, source, mtime)
        self.dup_of: str | None = None


def extract_dates(text: str, source: str, mtime: datetime) -> list[datetime]:
    found: list[datetime] = []
    seen: set[str] = set()

    def add(dt: datetime) -> None:
        key = dt.date().isoformat()
        if key in seen:
            return
        seen.add(key)
        found.append(dt)

    for m in ISO_DATE_RE.finditer(text):
        try:
            add(datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc))
        except ValueError:
            continue
    for m in COMPACT_DATE_RE.finditer(text + " " + source):
        try:
            add(datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc))
        except ValueError:
            continue
    for m in YEAR_MONTH_RE.finditer(text):
        try:
            add(datetime(int(m.group(1)), int(m.group(2)), 1, tzinfo=timezone.utc))
        except ValueError:
            continue
    add(mtime)
    return found


def chunk_files(files: list[Path], inventory_index: dict[str, dict[str, Any]]) -> list[Chunk]:
    ordered = sorted(files, key=lambda p: (source_rank(rel_posix(p)), rel_posix(p)))
    out: list[Chunk] = []
    for path in ordered:
        rel = rel_posix(path)
        text = load_text(path)
        if not text or not text.strip():
            continue
        pieces = chunk_text(text)
        if not pieces:
            continue
        rec = inventory_index.get(rel, {})
        mtime_s = rec.get("mtime")
        try:
            mtime = (
                datetime.strptime(mtime_s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if mtime_s
                else datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            )
        except (OSError, TypeError, ValueError):
            mtime = now_utc()
        n = len(pieces)
        for i, piece in enumerate(pieces, start=1):
            out.append(Chunk(rel, i, n, piece, mtime))
    return out


def dedupe(chunks: list[Chunk]) -> tuple[list[Chunk], int, int]:
    """Keep first occurrence (docs/ref first). Exact sha256, then simhash near-dup."""
    kept: list[Chunk] = []
    seen_sha: dict[str, str] = {}
    sim_index: list[tuple[int, str]] = []
    exact = 0
    near = 0
    for ch in chunks:
        prev = seen_sha.get(ch.sha256)
        if prev is not None:
            ch.dup_of = prev
            exact += 1
            continue
        if ch.simhash:
            dup = False
            for other_sh, other_src in sim_index:
                if hamming64(ch.simhash, other_sh) <= NEAR_DUP_HAMMING:
                    ch.dup_of = other_src
                    near += 1
                    dup = True
                    break
            if dup:
                continue
            sim_index.append((ch.simhash, ch.source))
        seen_sha[ch.sha256] = ch.source
        kept.append(ch)
    return kept, exact, near


def filename_overlap_keys(source: str) -> list[str]:
    name = Path(source).name.lower()
    keys: list[str] = []
    m = re.search(r"(deep-c-[a-f0-9]{8,})", name)
    if m:
        keys.append(m.group(1))
    m = re.search(r"(lattice-[a-z0-9-]+)", name)
    if m:
        keys.append(m.group(1))
    stem = Path(source).stem.lower()
    stem = re.sub(r"^\d{8}t\d{6}z_", "", stem)
    stem = re.sub(r"\.(answer|prompt|json|pdf).*", "", stem)
    if len(stem) >= 12:
        keys.append(stem[:24])
    return keys


def keyword_hits(text: str, keywords: Iterable[str]) -> tuple[int, list[str]]:
    low = text.lower()
    n = 0
    hit: list[str] = []
    for kw in keywords:
        c = low.count(kw)
        if c:
            n += c
            hit.append(kw)
    return n, hit


def score_chunk(
    ch: Chunk,
    theme: dict[str, Any],
    overlap_freq: Counter[str],
    stale_cutoff: datetime,
) -> tuple[int, list[str]]:
    hits, matched = keyword_hits(ch.text, theme["keywords"])
    score = hits * 3
    tid = theme["id"]
    reasons = list(matched[:8])

    if tid == 0:
        # contrastive structure bonus
        if "however" in ch.text.lower() and ("claim" in ch.text.lower() or "instead" in ch.text.lower()):
            score += 4
            reasons.append("contrast-structure")
        if re.search(r"\bv[0-9]\b.*\bv[0-9]\b", ch.text.lower()):
            score += 3
            reasons.append("multi-version")
    elif tid == 1:
        stale_dates = [d for d in ch.dates if d < stale_cutoff]
        if stale_dates:
            oldest = min(stale_dates)
            age = (stale_cutoff - oldest).days
            score += 4 + min(20, age // 7)
            reasons.append(f"stale-date:{oldest.date().isoformat()}")
        if ch.mtime < stale_cutoff:
            score += 3
            reasons.append("stale-mtime")
        if ISO_DATE_RE.search(ch.text):
            score += 2
    elif tid == 2:
        if re.search(r"\b(unproven|tbd|todo|no receipt|missing receipt)\b", ch.text, re.I):
            score += 8
            reasons.append("explicit-gap")
        if re.search(r"\b(we will|we should|must|always|never|obviously|clearly)\b", ch.text, re.I):
            score += 3
            reasons.append("modal-claim")
        if "receipt" not in ch.text.lower() and re.search(r"\b(claim|assert|true|works)\b", ch.text, re.I):
            score += 2
            reasons.append("claim-without-receipt-word")
    elif tid == 3:
        keys = filename_overlap_keys(ch.source)
        bonus = 0
        for k in keys:
            freq = overlap_freq.get(k, 0)
            if freq >= 2:
                bonus = max(bonus, min(24, freq * 2))
                reasons.append(f"name-overlap:{k}x{freq}")
        score += bonus
        if re.search(r"\b(v[2-9]|rewrite|fork|duplicate|already)\b", ch.text, re.I):
            score += 3

    # tiny files still rank if they hit; zero-hit packs can still fill the top-20
    score += min(2, ch.tokens // 2000)  # slight preference for substance
    return score, reasons


def rank_for_theme(
    chunks: list[Chunk],
    theme: dict[str, Any],
    overlap_freq: Counter[str],
    stale_cutoff: datetime,
) -> list[tuple[Chunk, int, list[str]]]:
    scored: list[tuple[Chunk, int, list[str]]] = []
    for ch in chunks:
        s, reasons = score_chunk(ch, theme, overlap_freq, stale_cutoff)
        scored.append((ch, s, reasons))
    scored.sort(key=lambda row: (-row[1], row[0].source, row[0].chunk_index))
    return scored


def pack_header(ch: Chunk, pack_n: int, score: int, reasons: list[str]) -> str:
    reason_s = ",".join(reasons[:6]) if reasons else "none"
    return (
        f"PACK {pack_n:02d}  score={score}  tokens={ch.tokens}  "
        f"sha256={ch.sha256[:16]}  simhash=0x{ch.simhash:016x}\n"
        f"SOURCE: {ch.source}  chunk {ch.chunk_index}/{ch.chunk_count}\n"
        f"REASONS: {reason_s}"
    )


def write_theme_file(
    theme: dict[str, Any],
    ranked: list[tuple[Chunk, int, list[str]]],
    generated_at: str,
) -> tuple[Path, int]:
    PACKS_DIR.mkdir(parents=True, exist_ok=True)
    path = PACKS_DIR / f"theme_{theme['id']}.txt"
    top = ranked[:TOP_PACKS_PER_THEME]
    lines: list[str] = [
        f"# EXP-BRAIN-01 corpus pack — theme {theme['id']}: {theme['name']}",
        f"# packs: {len(top)}  generated: {generated_at}",
        f"# ranked by keyword relevance; body <= {BODY_TOKEN_BUDGET} tokens "
        f"(pack budget {MAX_PACK_TOKENS}, chars/{CHARS_PER_TOKEN})",
        "",
    ]
    for i, (ch, score, reasons) in enumerate(top, start=1):
        hdr = pack_header(ch, i, score, reasons)
        lines.append("=" * 80)
        lines.append(hdr)
        lines.append("=" * 80)
        lines.append(ch.text.rstrip())
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path, len(top)


def snippet_around(text: str, needle: str, width: int = 180) -> str:
    low = text.lower()
    idx = low.find(needle.lower())
    if idx < 0:
        s = " ".join(text.split())
        return s[:width].rstrip()
    start = max(0, idx - width // 3)
    end = min(len(text), idx + len(needle) + width * 2 // 3)
    s = " ".join(text[start:end].split())
    if start > 0:
        s = "…" + s
    if end < len(text):
        s = s + "…"
    return s


def first_sentences(text: str, n: int = 2) -> str:
    parts = [p.strip() for p in SENTENCE_RE.split(text) if p.strip()]
    if not parts:
        return " ".join(text.split())[:220]
    return " ".join(parts[:n])[:280]


def make_questions(
    theme: dict[str, Any],
    ranked: list[tuple[Chunk, int, list[str]]],
) -> list[dict[str, Any]]:
    """Ground 10 cross-exam questions in the ranked packs (no model calls)."""
    top = ranked[: max(12, TOP_PACKS_PER_THEME)]
    questions: list[dict[str, Any]] = []
    used: set[str] = set()
    tid = theme["id"]
    kws = list(theme["keywords"])

    def add(q: str, sources: list[str], packs: list[int]) -> None:
        key = re.sub(r"\s+", " ", q.lower())[:180]
        if key in used or not q.strip():
            return
        used.add(key)
        questions.append(
            {
                "n": len(questions) + 1,
                "q": q,
                "source_files": sources[:4],
                "source_packs": packs[:4],
            }
        )

    # Pair nearby packs for contrast / overlap questions.
    for i, (ch, score, reasons) in enumerate(top):
        if len(questions) >= QUESTIONS_PER_THEME:
            break
        pack_n = i + 1
        hit_kw = next((k for k in kws if k.strip() and k.lower() in ch.text.lower()), None)
        snip = snippet_around(ch.text, hit_kw, 160) if hit_kw else first_sentences(ch.text)
        snip = snip.replace("\n", " ").strip()
        if len(snip) < 24:
            continue
        other = top[(i + 1) % len(top)][0] if len(top) > 1 else None
        other_src = other.source if other else None

        if tid == 0:
            if other_src and other_src != ch.source:
                add(
                    f"Does {ch.source} contradict {other_src}? Pack {pack_n:02d} says: "
                    f"\"{snip}\". Which claim is current? Cite bytes or mark Unproven.",
                    [ch.source, other_src],
                    [pack_n, (i + 1) % len(top) + 1],
                )
            else:
                add(
                    f"In {ch.source} (pack {pack_n:02d}): \"{snip}\". "
                    f"What other corpus file disputes this, and what receipt would settle it?",
                    [ch.source],
                    [pack_n],
                )
        elif tid == 1:
            stale = [d for d in ch.dates if d]
            oldest = min(stale).date().isoformat() if stale else "unknown-date"
            add(
                f"{ch.source} carries date {oldest} (pack {pack_n:02d}) and claims: \"{snip}\". "
                f"Is this still true as of {now_utc().date().isoformat()} "
                f"(stale if older than {STALE_DAYS} days)? Name the superseding file or mark stale.",
                [ch.source],
                [pack_n],
            )
        elif tid == 2:
            add(
                f"{ch.source} (pack {pack_n:02d}) states: \"{snip}\". "
                f"What observation would falsify this, and which file should hold the receipt? "
                f"If none exists, mark Unproven.",
                [ch.source],
                [pack_n],
            )
        else:
            if other_src and other_src != ch.source:
                add(
                    f"{ch.source} and {other_src} appear to cover overlapping scope "
                    f"(pack {pack_n:02d}: \"{snip}\"). Which is canonical? What work is duplicated?",
                    [ch.source, other_src],
                    [pack_n],
                )
            else:
                add(
                    f"{ch.source} (pack {pack_n:02d}) may duplicate other work: \"{snip}\". "
                    f"List the overlapping files and the single canonical owner.",
                    [ch.source],
                    [pack_n],
                )

    # Fallback templates grounded in remaining pack sources (still no model).
    fallbacks = [
        (
            0,
            "Where do MAG version docs (v2/v3/v4/v5) disagree on the current phase gate? "
            "Cite two files from this theme pack and pick one as current.",
        ),
        (
            0,
            "Is FIND · FILE · LOAD in OPERATOR_CARD still consistent with the compass and DNA docs? "
            "Quote both sides.",
        ),
        (
            1,
            "Which dated 'as of' / 'as-of' claims in this theme are older than 30 days and still "
            "written in present tense? List three with dates.",
        ),
        (
            1,
            "Research-pack scrapes from July 2026 — which of their factual claims about models, "
            "prices, or APIs are stale as of today? Cite pack + original URL field if present.",
        ),
        (
            2,
            "Which vision/proposal sentences in this theme have no measure, test, or receipt path? "
            "Mark each Supported / Disputed / Unproven.",
        ),
        (
            2,
            "Find claims that use always/never/obviously/clearly with no cited bytes. "
            "Rewrite each as a falsifiable check.",
        ),
        (
            3,
            "Multiple research packs share the same deep-c-* paper id. Are they independent work "
            "or scrape duplicates? Name the canonical pack id.",
        ),
        (
            3,
            "ILAP / steal / v3–v5 pipes: which documents restate the same protocol under a new name? "
            "Collapse to one owner file.",
        ),
    ]
    for ft, q in fallbacks:
        if len(questions) >= QUESTIONS_PER_THEME:
            break
        if ft != tid:
            continue
        srcs = [ch.source for ch, _, _ in top[:3]]
        add(q, srcs, list(range(1, min(4, len(top) + 1))))

    # Last-resort unique questions from leftover sources.
    for i, (ch, _, _) in enumerate(top):
        if len(questions) >= QUESTIONS_PER_THEME:
            break
        add(
            f"Cross-examine {ch.source} chunk {ch.chunk_index}/{ch.chunk_count} under theme "
            f"'{theme['name']}'. What must be true for the claims to hold, and what file "
            f"would prove them false?",
            [ch.source],
            [i + 1],
        )

    return questions[:QUESTIONS_PER_THEME]


def build_overlap_freq(chunks: list[Chunk]) -> Counter[str]:
    freq: Counter[str] = Counter()
    for ch in chunks:
        for k in filename_overlap_keys(ch.source):
            freq[k] += 1
    return freq


def run(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="EXP-BRAIN-01 corpus packer")
    p.add_argument("--inventory-only", action="store_true")
    args = p.parse_args(argv)

    files = iter_corpus_files()
    inventory = build_inventory(files)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INVENTORY_PATH.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"INVENTORY files={inventory['file_count']} bytes={inventory['total_bytes']} "
        f"-> {rel_posix(INVENTORY_PATH)}",
        flush=True,
    )
    if args.inventory_only:
        return 0

    index = {rec["path"]: rec for rec in inventory["files"]}
    raw_chunks = chunk_files(files, index)
    kept, n_exact, n_near = dedupe(raw_chunks)
    print(
        f"CHUNKS raw={len(raw_chunks)} kept={len(kept)} exact_dup={n_exact} near_dup={n_near}",
        flush=True,
    )
    if len(kept) < 10:
        print("WARN: fewer than 10 unique chunks after dedupe", flush=True)

    overlap_freq = build_overlap_freq(kept)
    stale_cutoff = now_utc() - timedelta(days=STALE_DAYS)
    generated_at = inventory["generated_at"]

    theme_stats: list[dict[str, Any]] = []
    all_questions: list[dict[str, Any]] = []
    PACKS_DIR.mkdir(parents=True, exist_ok=True)

    for theme in THEMES:
        ranked = rank_for_theme(kept, theme, overlap_freq, stale_cutoff)
        path, n_written = write_theme_file(theme, ranked, generated_at)
        qs = make_questions(theme, ranked)
        all_questions.append(
            {
                "id": theme["id"],
                "name": theme["name"],
                "questions": qs,
            }
        )
        top_score = ranked[0][1] if ranked else 0
        theme_stats.append(
            {
                "id": theme["id"],
                "name": theme["name"],
                "packs_written": n_written,
                "path": rel_posix(path),
                "top_score": top_score,
                "questions": len(qs),
            }
        )
        print(
            f"THEME {theme['id']} packs={n_written} top_score={top_score} -> {rel_posix(path)}",
            flush=True,
        )

    questions_doc = {
        "experiment": "EXP-BRAIN-01",
        "generated_at": generated_at,
        "stale_cutoff": stale_cutoff.date().isoformat(),
        "themes": all_questions,
    }
    QUESTIONS_PATH.write_text(
        json.dumps(questions_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"QUESTIONS -> {rel_posix(QUESTIONS_PATH)}", flush=True)

    inventory["packer"] = {
        "chunks_raw": len(raw_chunks),
        "chunks_kept": len(kept),
        "exact_dups": n_exact,
        "near_dups": n_near,
        "max_pack_tokens": MAX_PACK_TOKENS,
        "body_token_budget": BODY_TOKEN_BUDGET,
        "themes": theme_stats,
        "questions_path": rel_posix(QUESTIONS_PATH),
    }
    INVENTORY_PATH.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
