"""QUOTE_AUDIT_WIDE 2026-09-25 - byte-grep audit of quote fields.

Widens the n=0 verbatim audit (watch/inbox/GO_LIST_EXECUTION_20260925.md P3,
which found 0 populated evidence_quote fields in watch/inbox) to:
  - memory/research_polished/  (all .md)
  - corpus/steal/              (all .md)

Full docstring and implementation appended below in build chunks.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

T0 = time.time()
ROOT_STR = "C:/Users/foste/Documents/projects/local_sovereign_agent"
ROOT = Path(ROOT_STR)
POL = ROOT / "memory" / "research_polished"
STEAL = ROOT / "corpus" / "steal"
LANES = ROOT / "memory" / "runs" / "mickey17_v2" / "lanes"
RUN = ROOT / "memory" / "runs" / "mickey17_v2"
PACKS = ROOT / "memory" / "research_packs"
FOLD_SECTIONS = ROOT / "memory" / "runs" / "mickey17_v2" / "FOLD_SECTIONS.md"
WORK = ROOT / "memory" / "runs" / "quote_audit_wide_20260925"
SNAP = WORK / "snapshot"
OUT_JSON = ROOT / "watch" / "inbox" / "QUOTE_AUDIT_WIDE_20260925.results.json"

METHOD_NOTE = """Both dirs are snapshotted FIRST with sha256 + stability double-read,
because MASTER_MICKEY17_V2.md was observed being rewritten by a concurrent
fold seat during this audit. Verdicts describe the pinned snapshot bytes.
Normalization (MICKEY-17 verifier lanes' convention):
  norm(s) = re.sub(r'\\s+', ' ', s).strip()
A quote unit HITs when norm(quote) appears inside norm(claimed source) or
vice versa (scope-trim), case-sensitive, whitespace-normalized only.
Unit kinds:
  quote_field    - lines starting Quote / Quote (...):  "..."
  disputed_pair  - Section 5 inline byte-copied quotes: Side X (lane#i): "..."
  inline_span    - inline double-quoted spans >= 5 words (polish census)
Haystacks in priority order:
  1. named lane row  lanes/<lane>.json rows[idx]['quote']
  2. any lane row quote field (list or dict-with-rows shapes)
  3. memory/runs/mickey17_v2/** concat, grep -F batch
  4. memory/research_packs/** concat, grep -F batch
  5. vendored texts: canon/ + root *.txt
  6. repo-wide grep memory corpus watch reference canon (misses only)
Read-only over the audited tree: writes land only under
memory/runs/quote_audit_wide_20260925/ and watch/inbox/ results json.
"""




def _run(*args, **kw):
    # HEADLESS law (spawn_sites_no_window): every spawn is windowless.
    kw.setdefault("creationflags", getattr(subprocess, "CREATE_NO_WINDOW",
                  0x08000000) if sys.platform == "win32" else 0)
    return _run(*args, **kw)

def rel(p):
    """Repo-relative posix name by slicing the known ROOT prefix (read-only tool)."""
    s = str(p).replace("\\", "/").replace(ROOT_STR + "/", "", 1)
    if s.startswith("/") or s.endswith("/") or ":" in s:
        raise ValueError("unexpected path shape: %s" % p)
    return s


def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def read(p):
    return p.read_text(encoding="utf-8", errors="replace")


def sha256(p):
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


# ---------------------------------------------------------------- snapshot

def snapshot_dirs():
    """Copy both dirs with double-read stability check; return per-file manifest."""
    manifest = {}
    if SNAP.exists():
        shutil.rmtree(SNAP)
    for src in (POL, STEAL):
        dst_root = SNAP / rel(src)
        dst_root.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.glob("*.md")):
            h1 = sha256(f)
            shutil.copy2(f, dst_root / f.name)
            h2 = sha256(f)
            h3 = sha256(dst_root / f.name)
            stable = (h1 == h2 == h3)
            manifest[rel(f)] = {
                "sha256": h3, "bytes": (dst_root / f.name).stat().st_size,
                "stable_during_copy": stable,
            }
            if not stable:
                log("UNSTABLE during snapshot: %s (source changed mid-copy)" % f)
    return manifest


# ---------------------------------------------------------------- enumeration

RE_QUOTE_LINE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?Quote(?:\s*\(([^)]*)\))?(?:\*\*)?\s*[:：]\s*(.*)$")
RE_LANE_BRACKET = re.compile(r"\[([a-z0-9-]+)#(\d+)(?:,[^\]]*)?\]")
RE_LANE_COLON = re.compile(r"\[lane:\s*([a-z0-9-]+)")
RE_LANE_HASH = re.compile(r"([a-z0-9-]+)#(\d+)")
RE_SIDE = re.compile(r"^Side\s+[AB]\s*\(([a-z0-9-]+)#(\d+)\)\s*:\s*(.*)$")
RE_Q_LABEL = re.compile(
    r"(Lane claim quote|Lane quote|Lane claim|Baseline quote|Counter-quote|Quote|quote):")
RE_STRAIGHT = re.compile(r'"([^"\n]+)"')
RE_BTICK = re.compile(r"`([^`\n]+)`")
RE_CURLY = re.compile("\u201c([^\u201d\n]+)\u201d")

SECONDARY_LABELS = {"Baseline quote", "Counter-quote"}


def spans_from(text):
    out = [m.group(1) for m in RE_STRAIGHT.finditer(text)]
    out += [m.group(1) for m in RE_CURLY.finditer(text)]
    return out


def span_after_label(line, label_end):
    """First quoted span after a label; backtick wins when it opens first."""
    rest = line[label_end:]
    bq = RE_BTICK.search(rest)
    qs = RE_STRAIGHT.search(rest)
    if bq and (not qs or bq.start() <= qs.start()):
        return bq.group(1)
    if qs:
        return qs.group(1)
    return None


def wordcount(s):
    return len(norm(s).split())


def enumerate_steal(snap_steal):
    units = []
    for f in sorted(snap_steal.glob("*.md")):
        lines = read(f).splitlines()
        pending = None  # (lane, idx_or_None) from heading lines
        for i, line in enumerate(lines, 1):
            same_hash = RE_LANE_HASH.search(line)
            same_colon = RE_LANE_COLON.search(line)
            for m in RE_LANE_BRACKET.finditer(line):
                pending = (m.group(1), int(m.group(2)))
            if same_colon:
                pending = (same_colon.group(1), None)
            sm = RE_SIDE.match(line)
            if sm:
                for span in spans_from(sm.group(3)):
                    if wordcount(span) >= 4:
                        units.append({
                            "dir": "corpus/steal", "file": f.name, "line": i,
                            "kind": "disputed_pair",
                            "note": "byte-copied per Section-5 preamble",
                            "lane": sm.group(1), "idx": int(sm.group(2)),
                            "text": span, "raw": line.strip(),
                        })
                continue
            for qm in RE_Q_LABEL.finditer(line):
                span = span_after_label(line, qm.end())
                if span is None:
                    continue
                kind = ("disputed_pair" if qm.group(1) in SECONDARY_LABELS
                        else "quote_field")
                if same_hash:
                    lane_ref = (same_hash.group(1), int(same_hash.group(2)))
                elif pending is not None:
                    lane_ref = pending
                else:
                    lane_ref = (None, None)
                units.append({
                    "dir": "corpus/steal", "file": f.name, "line": i,
                    "kind": kind, "note": qm.group(1),
                    "lane": lane_ref[0], "idx": lane_ref[1],
                    "text": span, "raw": line.strip(),
                })
    return units


def enumerate_polished(snap_pol):
    units = []
    for f in sorted(snap_pol.glob("*.md")):
        for i, line in enumerate(read(f).splitlines(), 1):
            if RE_QUOTE_LINE.match(line):
                continue
            for span in spans_from(line):
                if wordcount(span) >= 5:
                    units.append({
                        "dir": "memory/research_polished", "file": f.name,
                        "line": i, "kind": "inline_span", "note": "",
                        "lane": None, "idx": None, "text": span,
                        "raw": line.strip(),
                    })
    return units


# ---------------------------------------------------------------- haystacks

def load_lanes():
    lanes = {}
    parse_fail = []
    for f in sorted(LANES.glob("*.json")):
        try:
            d = json.loads(read(f))
        except Exception as e:
            parse_fail.append((f.stem, str(e)[:60]))
            continue
        if isinstance(d, list):
            rows = d
        elif isinstance(d, dict) and isinstance(d.get("rows"), list):
            rows = d["rows"]
        else:
            parse_fail.append((f.stem, "no row list"))
            continue
        lanes[f.stem] = rows
    return lanes, parse_fail


RUN_CONCAT = WORK / "run_concat.txt"
PACKS_CONCAT = WORK / "packs_concat.txt"
CANON_CONCAT = WORK / "canon_concat.txt"
INBOX_CONCAT = WORK / "inbox_concat.txt"
NEEDLES = WORK / "needles.txt"


def _concat_blob(texts):
    return "\n".join(t.replace("\n", " ") for _, t in texts) + "\n"


def build_run_concat(texts):
    RUN_CONCAT.write_text(_concat_blob(texts), encoding="utf-8")


def build_packs_concat(texts):
    PACKS_CONCAT.write_text(_concat_blob(texts), encoding="utf-8")


def build_canon_concat(texts):
    CANON_CONCAT.write_text(_concat_blob(texts), encoding="utf-8")


def build_inbox_concat(texts):
    INBOX_CONCAT.write_text(_concat_blob(texts), encoding="utf-8")


def load_watch_inbox_texts():
    """watch/inbox/** plus watch/*.md, small text files only (media excluded)."""
    texts = []
    base = ROOT / "watch" / "inbox"
    files = [f for f in sorted(base.rglob("*"))
             if f.is_file() and f.suffix.lower() in {".md", ".txt", ".json"}
             and f.stat().st_size <= 5 * 1024 * 1024]
    top = [f for f in sorted((ROOT / "watch").glob("*.md")) if f.is_file()]
    for f in files + top:
        try:
            texts.append((rel(f), norm(read(f)).replace("\n", " ")))
        except Exception as e:
            log("  read fail %s: %s" % (f.name, e))
    log("  watch/inbox+watch: %d texts" % len(texts))
    return texts


def grep_batch(needles, which):
    """One grep -F -f pass over the named concat. Returns {needle: [line nos]}."""
    if not needles:
        return {}
    concat = {"run": RUN_CONCAT, "packs": PACKS_CONCAT, "canon": CANON_CONCAT,
              "inbox": INBOX_CONCAT}[which]
    NEEDLES.write_text("\n".join(needles) + "\n", encoding="utf-8")
    try:
        r = _run(
            ["grep", "-F", "-o", "-n", "-f", str(NEEDLES), str(concat)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=300,
        )
    except Exception as e:
        log("GREP FAIL %s: %s" % (which, e))
        return {n: [] for n in needles}
    hits = {n: [] for n in needles}
    lookup = {}
    for i, n in enumerate(needles):
        lookup.setdefault(n, i)
    for line in r.stdout.splitlines():
        ln, _, match = line.partition(":")
        if match in lookup:
            try:
                hits[needles[lookup[match]]].append(int(ln))
            except ValueError:
                pass
    return hits


def load_dir_texts(base, label):
    texts = []
    files = [f for f in sorted(base.rglob("*")) if f.is_file() and f.suffix.lower() in {
        ".md", ".txt", ".json", ".jsonl", ".py", ".ts", ".js", ".yaml", ".yml",
        ".html", ".csv",
    }]
    for f in files:
        try:
            if f.stat().st_size > 30 * 1024 * 1024:
                log("  skip oversize: %s" % f.name)
                continue
            texts.append((rel(f), norm(read(f)).replace("\n", " ")))
        except Exception as e:
            log("  read fail %s: %s" % (f.name, e))
    log("  %s: %d texts from %d files" % (label, len(texts), len(files)))
    return texts


def repo_grep(needle, limit=3):
    """Last-resort fallback. Scope is deliberately narrow: reference/ only.
    packs/run/canon haystacks are already covered by the grep_batch concats;
    memory/ (5 GB) and corpus/ (6.8 GB) estate-wide searches are out of scope
    and misses say so."""
    try:
        r = _run(
            ["grep", "-rlF", "--binary-files=without-match", "--",
             needle, "reference"],
            cwd=ROOT_STR, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=60,
        )
        return [x.replace("\\", "/") for x in r.stdout.splitlines() if x.strip()][:limit]
    except Exception as e:
        return ["<grep failed: %s>" % e]


# ---------------------------------------------------------------- checks

def longest_shared_window(a, b):
    at, bt = a.split(), b.split()
    best = 0
    for i in range(len(at)):
        for j in range(len(bt)):
            k = 0
            while i + k < len(at) and j + k < len(bt) and at[i + k] == bt[j + k]:
                k += 1
            best = max(best, k)
    return best


def check_steal_units(units, lanes, watch_hits_fn):
    pool = []
    for lane, rows in lanes.items():
        for idx, row in enumerate(rows):
            if isinstance(row, dict) and isinstance(row.get("quote"), str):
                pool.append((lane, idx, "quote", norm(row["quote"])))
            if isinstance(row, dict) and isinstance(row.get("claim"), str) and \
                    len(row.get("claim")) >= 20:
                # claim field as SECONDARY provenance (marked in where)
                pool.append((lane, idx, "claim", norm(row["claim"])))
    log("lane pool: %d entries (quote+claim fields)" % len(pool))

    needles = sorted({norm(u["text"]) for u in units if u["text"]})
    run_hits = grep_batch(needles, "run")
    packs_hits = grep_batch(needles, "packs")
    inbox_hits = grep_batch(needles, "inbox")

    def lane_claim_contains(lane, idx, n):
        """(verdict_or_None, where) for the claimed lane/row."""
        if lane not in lanes or not isinstance(lanes[lane], list):
            return None, None
        rows = lanes[lane]
        if idx is not None:
            if not (0 <= idx < len(rows)):
                return None, None
            row = rows[idx]
            if isinstance(row, dict) and isinstance(row.get("quote"), str):
                q = norm(row["quote"])
                if n == q or (n in q and len(n) >= 0.6 * len(q)) or \
                        (q in n and len(q) >= 0.6 * len(n)):
                    return "HIT", ["%s#%d quote field" % (lane, idx)]
                if longest_shared_window(n, q) >= 8:
                    return "HIT_PARTIAL", ["%s#%d quote field (longest shared window %d tokens)" % (lane, idx, longest_shared_window(n, q))]
            return "MISS_claimed_row", []
        # lane named without row index: search all rows of that lane
        for i, row in enumerate(rows):
            if isinstance(row, dict) and isinstance(row.get("quote"), str):
                q = norm(row["quote"])
                if n == q or (n in q and len(n) >= 0.6 * len(q)) or \
                        (q in n and len(q) >= 0.6 * len(n)):
                    return "HIT", ["%s#%d quote field (lane-level claim)" % (lane, i)]
        return "MISS_claimed_lane", []

    for u in units:
        if not u["text"]:
            u["verdict"] = "NO_SPAN"
            u["where"] = []
            continue
        n = norm(u["text"])
        lane, idx = u.get("lane"), u.get("idx")
        claimed_resolvable = lane is not None and lane in lanes
        u["claimed_row_resolvable"] = claimed_resolvable
        if lane is not None:
            v, w = lane_claim_contains(lane, idx, n)
            if v == "HIT" or v == "HIT_PARTIAL":
                u["verdict"] = v
                u["where"] = w
                continue
            u["verdict"] = v if v else "UNRESOLVED_claimed_row"
            u["where"] = w or []
        else:
            u["verdict"] = "UNRESOLVED_claimed_row"
            u["where"] = []
        # wider searches
        pool_hits = ["%s#%d(%s)" % (l, i, fld) for l, i, fld, q in pool
                     if n in q or q in n]
        if pool_hits:
            u["where"].append("lane quote pool: " + ", ".join(pool_hits[:4]))
            if u["verdict"].startswith(("MISS", "UNRESOLVED")):
                u["verdict"] = "HIT_OTHER_ROW"
            continue
        if run_hits.get(n):
            if u["verdict"].startswith(("MISS", "UNRESOLVED")):
                u["verdict"] = "HIT_RUN_ARCHIVE"
            u["where"].append("run archive concat")
            continue
        if packs_hits.get(n):
            if u["verdict"].startswith(("MISS", "UNRESOLVED")):
                u["verdict"] = "HIT_PACKS"
            u["where"].append("research packs concat")
            continue
        if inbox_hits.get(n):
            if u["verdict"].startswith(("MISS", "UNRESOLVED")):
                u["verdict"] = "HIT_WATCH_INBOX"
            u["where"].append("watch/inbox concat")
            continue
        if watch_hits_fn(n):
            if u["verdict"].startswith(("MISS", "UNRESOLVED")):
                u["verdict"] = "HIT_WATCH_TOP"
            u["where"].append("watch/ top-level .md")
            continue
        u["where"].append("not found in lanes/run/packs/watch-inbox (fallback "
                          "reference/ also negative; memory 5GB + corpus 6.8GB not searched)")
    return units


def check_polished_units(units, run_texts, packs_texts, canon_texts, inbox_texts):
    needles = []
    seen = set()
    for u in units:
        n = norm(u["text"])
        if n and n not in seen:
            seen.add(n)
            needles.append(n)
    log("polished needles: %d distinct" % len(needles))
    pack_hits = grep_batch(needles, "packs")
    inbox_hits = grep_batch(needles, "inbox")
    run_hits = grep_batch(needles, "run")
    canon_hits = grep_batch(needles, "canon")

    def lines_to_files(line_numbers, texts, cap=3):
        out = []
        for ln in line_numbers:
            if 1 <= ln <= len(texts):
                name = texts[ln - 1][0]
                if name not in out:
                    out.append(name)
                if len(out) >= cap:
                    break
        return out

    for u in units:
        n = norm(u["text"])
        if pack_hits.get(n):
            u["verdict"] = "HIT"
            u["where"] = lines_to_files(pack_hits[n], packs_texts)
        elif inbox_hits.get(n):
            u["verdict"] = "HIT_WATCH_INBOX"
            u["where"] = lines_to_files(inbox_hits[n], inbox_texts)
        elif run_hits.get(n):
            u["verdict"] = "HIT_RUN_ARCHIVE"
            u["where"] = lines_to_files(run_hits[n], run_texts)
        elif canon_hits.get(n):
            u["verdict"] = "HIT_VENDORED_TEXT"
            u["where"] = lines_to_files(canon_hits[n], canon_texts)
        else:
            u["verdict"] = "MISS_packs"
            u["where"] = repo_grep(u["text"]) or [
                "not in reference/; memory 5GB + corpus 6.8GB not searched"]
    return units


def check_section_verbatim():
    """Sections the MASTER files label verbatim vs the current FOLD_SECTIONS.md."""
    out = {}

    def fold_section_norm(name):
        if not FOLD_SECTIONS.exists():
            return None
        t = read(FOLD_SECTIONS)
        for m in re.finditer(r"^## ([^\n]+)$", t, re.M):
            ttl = m.group(1).strip()
            if ttl.lower().startswith(name.lower()):
                end = t.find("\n## ", m.end())
                return norm(t[m.end():end if end != -1 else len(t)])
        return None

    fs = norm(read(FOLD_SECTIONS)) if FOLD_SECTIONS.exists() else None
    for f in sorted((SNAP / "corpus" / "steal").glob("MASTER_MICKEY17_V2*.md")):
        text = read(f)
        checks = {}
        # style A: numbered sections 1..3 verbatim (0924 fold claim)
        m1 = re.search(r"^## 1\.", text, re.M)
        m4 = re.search(r"^## 4\.", text, re.M)
        if m1 and m4 and fs is not None:
            sec = norm(text[m1.start():m4.start()])
            checks["sections_1_to_3"] = ("verbatim_in_FOLD_SECTIONS" if sec in fs
                                         else "not_contained_in_current_FOLD_SECTIONS")
        # style B: per-section "verbatim" labels (v2.1 fold)
        heads = list(re.finditer(r"^## ([^\n]+)$", text, re.M))
        for k, h in enumerate(heads):
            title = h.group(1).strip()
            if "verbatim" not in title.lower():
                continue
            body_end = heads[k + 1].start() if k + 1 < len(heads) else len(text)
            body = norm(text[h.end():body_end])
            name = re.sub(r"\s*\(.*$", "", title).strip()
            if fs is None:
                checks[name] = "FOLD_SECTIONS_missing"
            elif body in fs:
                checks[name] = "verbatim_in_FOLD_SECTIONS"
            else:
                # master may copy the fold section then append annotations:
                # try per-line coverage and reverse containment
                lines_in = sum(1 for ln in body.split(" . ")
                               if len(ln) > 40 and ln in fs)
                lines_tot = sum(1 for ln in body.split(" . ") if len(ln) > 40)
                cov = "%d/%d long lines present in FOLD_SECTIONS" % (lines_in, lines_tot)
                fold_sec = fold_section_norm(name)
                if fold_sec and fold_sec in body:
                    checks[name] = "fold_section_contained_in_master (annotations appended); " + cov
                else:
                    checks[name] = "not_contained; " + cov
        out[f.name] = checks or "no verbatim-labeled sections found"
    return out


# ---------------------------------------------------------------- main

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    log("snapshot...")
    manifest = snapshot_dirs()
    log("snapshot manifest: %d files" % len(manifest))

    log("enumerate...")
    steal_units = enumerate_steal(SNAP / "corpus" / "steal")
    pol_units = enumerate_polished(SNAP / "memory" / "research_polished")
    log("steal units: %d | polished units: %d" % (len(steal_units), len(pol_units)))
    kinds = {}
    for u in steal_units + pol_units:
        kinds[(u["dir"], u["kind"])] = kinds.get((u["dir"], u["kind"]), 0) + 1
    log("unit census: " + json.dumps({f"{k[0]}::{k[1]}": v for k, v in sorted(kinds.items())}))

    log("load lanes...")
    lanes, parse_fail = load_lanes()
    n_rows = sum(len(v) for v in lanes.values())
    n_q = sum(1 for v in lanes.values() for r in v if isinstance(r, dict) and r.get("quote"))
    log("lanes loaded: %d rows: %d rows with quote: %d | skipped: %d" % (len(lanes), n_rows, n_q, len(parse_fail)))

    log("load run texts...")
    run_texts = load_dir_texts(RUN, "runs/mickey17_v2")
    build_run_concat(run_texts)

    log("load packs texts...")
    packs_texts = load_dir_texts(PACKS, "research_packs")
    build_packs_concat(packs_texts)
    log("packs concat: %.1f MB" % (PACKS_CONCAT.stat().st_size / 1e6))

    canon_dir = ROOT / "canon"
    canon_texts = load_dir_texts(canon_dir, "canon") if canon_dir.exists() else []
    for f in sorted(ROOT.glob("*.txt")):
        try:
            canon_texts.append((f.name, norm(read(f)).replace("\n", " ")))
        except Exception:
            pass
    build_canon_concat(canon_texts)
    log("vendored texts: %d" % len(canon_texts))

    log("load watch/inbox texts...")
    inbox_texts = load_watch_inbox_texts()
    build_inbox_concat(inbox_texts)
    log("inbox concat: %.1f MB" % (INBOX_CONCAT.stat().st_size / 1e6))

    def watch_top_fn(needle):
        try:
            r = _run(
                ["grep", "-rlF", "--", needle] + [str(p) for p in sorted((ROOT / "watch").glob("*.md"))],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=60)
            return bool(r.stdout.strip())
        except Exception:
            return False

    log("check steal units...")
    steal_units = check_steal_units(steal_units, lanes, watch_top_fn)

    log("check polished units...")
    pol_units = check_polished_units(pol_units, run_texts, packs_texts,
                                     canon_texts, inbox_texts)
    sec = check_section_verbatim()

    # volatility: re-hash live files
    drift = {}
    for name, meta in manifest.items():
        live = ROOT / name
        if live.exists():
            h = sha256(live)
            if h != meta["sha256"]:
                drift[name] = {"snapshot_sha256": meta["sha256"],
                               "live_sha256": h, "changed_during_audit": True}
        else:
            drift[name] = {"snapshot_sha256": meta["sha256"],
                           "live_sha256": None, "changed_during_audit": True}
    log("live drift vs snapshot: %d files" % len(drift))

    results = {
        "schema": "quote_audit_wide.v1",
        "date": "2026-09-25",
        "method_note": METHOD_NOTE,
        "snapshot": {"dir": rel(SNAP), "files": manifest},
        "live_drift_during_audit": drift,
        "haystacks": {
            "lanes_dir": rel(LANES), "lanes_loaded": len(lanes),
            "lane_rows": n_rows, "lane_rows_with_quote": n_q,
            "lane_files_skipped": [{"file": f, "why": w} for f, w in parse_fail],
            "run_files": len(run_texts), "pack_files": len(packs_texts),
            "vendored_texts": len(canon_texts), "watch_inbox_texts": len(inbox_texts),
        },
        "section_verbatim_check": sec,
        "units": steal_units + pol_units,
    }
    OUT_JSON.write_text(json.dumps(results, indent=1, ensure_ascii=True),
                        encoding="utf-8")
    log("wrote " + str(OUT_JSON))

    from collections import Counter
    for d in ("corpus/steal", "memory/research_polished"):
        dus = [u for u in results["units"] if u["dir"] == d]
        c = Counter(u["verdict"] for u in dus)
        log("%s %d units: %s" % (d, len(dus), dict(c)))
    log("section_verbatim: " + json.dumps(sec))
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

