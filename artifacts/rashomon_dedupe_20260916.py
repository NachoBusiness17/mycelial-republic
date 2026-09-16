"""rashomon_dedupe_20260916 — B12 audit: Rashomon witness URL dedupe measurement.

Read-only. Extracts every URL from the fixed Rashomon corpus, canonicalizes each
with mag.link_library.canonicalize, and reports:
  - total raw URL occurrences and distinct raw URL strings
  - unique canonical count
  - duplicate clusters (same canonical reachable from N different raw spellings)
  - cross-record restatements (same raw URL filed in more than one corpus file)
  - any localhost/private/reserved hosts found (reported, never raised)

No file is modified. Ledger rows are filtered to the Rashomon drop writers so the
audit stays on the witness set (the wider ledger belongs to other lanes).

Run:  .venv/Scripts/python.exe artifacts/rashomon_dedupe_20260916.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.link_library import canonicalize, canonical_sha256, validate_host_safety  # noqa: E402

# --- fixed corpus (mission: fixed paths) -------------------------------------
LEDGER = ROOT / "watch" / "inbox" / "LINKS.jsonl"
LEDGER_WRITERS = {"zcode-rashomon-20260914", "dedupe-test"}

CORPUS_TEXT_FILES = [
    ROOT / "watch/inbox/RASHOMON_SURFACE_ELEPHANT_20260914.md",
    ROOT / "queue/handoff/ractors/BAUDRILLARD_rashomon_20260904.md",
    ROOT / "queue/handoff/ractors/FOUCAULT_rashomon_20260904.md",
    ROOT / "queue/handoff/ractors/MCLUHAN_rashomon_20260904.md",
    ROOT / "queue/handoff/ractors/PLATO_KIRK_rashomon_20260904.md",
    ROOT / "memory/research/ghost-rashomon-proposal-20260809.md",
    ROOT / "memory/narrative_corpus/rashomon/tavern_bar_fight_party.v1.md",
    ROOT / "watch/inbox/SESSION_RECOVERY_FORGE_DAEMON_20260914.md",
    ROOT / "watch/inbox/PARABLE_ARC_SYNTHESIS_20260916.md",
    ROOT / "watch/inbox/wave_20260916/receipts/B13_CODETAUR_KAN.md",
    ROOT / "queue/lanes/research/inbox.jsonl",
]

URL_RE = re.compile(r"https?://[^\s'\"<>()\[\]{}\\]+")
TRIM = ".,;:!?'\"`*"  # markdown / prose trailing punctuation


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def clean_hit(hit: str) -> str:
    return hit.rstrip(TRIM).rstrip(")").rstrip(TRIM)


def main() -> int:
    # url_string -> { canonical, sha, occurrences: [(file, field)] }
    records: dict[str, dict] = {}
    corpus_url_files = 0

    for path in CORPUS_TEXT_FILES:
        if not path.is_file():
            print(f"MISSING corpus file: {rel(path)}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = {clean_hit(m) for m in URL_RE.findall(text)}
        if hits:
            corpus_url_files += 1
        for url in hits:
            rec = records.setdefault(url, {"canonical": None, "sha": "", "where": []})
            rec["where"].append(f"{rel(path)}")

    # ledger rows: Rashomon drop writers only, url + canonical fields
    ledger_rows = 0
    if LEDGER.is_file():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("writer") not in LEDGER_WRITERS:
                continue
            ledger_rows += 1
            for field in ("url", "canonical"):
                value = (row.get(field) or "").strip()
                if not value:
                    continue
                rec = records.setdefault(value, {"canonical": None, "sha": "", "where": []})
                rec["where"].append(f"{rel(LEDGER)}#{field}·{row.get('writer')}·seq{row.get('seq')}")

    # canonicalize everything
    canonical_of: dict[str, str] = {}
    unsafe: list[tuple[str, str]] = []
    errors: list[tuple[str, str]] = []
    for url, rec in records.items():
        try:
            validate_host_safety(url)
        except ValueError as exc:
            unsafe.append((url, str(exc)))
        try:
            canon = canonicalize(url)
        except ValueError as exc:
            errors.append((url, str(exc)))
            continue
        canonical_of[url] = canon
        rec["canonical"] = canon
        rec["sha"] = canonical_sha256(canon)

    # clusters: canonical -> distinct raw spellings
    clusters: dict[str, list[str]] = defaultdict(list)
    for url, canon in canonical_of.items():
        clusters[canon].append(url)

    dup_clusters = {c: urls for c, urls in clusters.items() if len(urls) > 1}
    restatements = {u: r for u, r in records.items() if len(r["where"]) > 1}

    # --- report -------------------------------------------------------------
    print("=" * 72)
    print("B12 RASHOMON WITNESS URL DEDUPE AUDIT — 2026-09-16")
    print("=" * 72)
    print(f"corpus text files scanned : {len(CORPUS_TEXT_FILES)} (with >=1 URL: {corpus_url_files})")
    print(f"ledger rows in scope      : {ledger_rows} (writers: {', '.join(sorted(LEDGER_WRITERS))})")
    print(f"total URL occurrences     : {sum(len(r['where']) for r in records.values())}")
    print(f"distinct raw URL strings  : {len(records)}")
    print(f"unique canonicals         : {len(clusters)}")
    print(f"canonicalize errors       : {len(errors)}")
    print(f"localhost/private hits    : {len(unsafe)}")
    if unsafe:
        for url, why in unsafe:
            print(f"  UNSAFE {url}  ->  {why}")
    if errors:
        for url, why in errors:
            print(f"  ERROR  {url}  ->  {why}")

    print("\n--- per-canonical breakdown ---")
    for canon in sorted(clusters):
        urls = sorted(clusters[canon])
        occ = sum(len(records[u]["where"]) for u in urls)
        tag = f"CLUSTER x{len(urls)} spellings" if len(urls) > 1 else "singleton"
        print(f"{canon}")
        print(f"    sha256={records[urls[0]]['sha'][:16]}…  raw_strings={len(urls)}  occurrences={occ}  [{tag}]")
        for u in urls:
            for where in records[u]["where"]:
                print(f"      - {u}")
                print(f"        source: {where}")
                break  # one source line per spelling; full detail in restatements

    print("\n--- DUPLICATE CLUSTERS (same canonical, different raw spellings) ---")
    if not dup_clusters:
        print("(none)")
    for i, (canon, urls) in enumerate(sorted(dup_clusters.items()), 1):
        print(f"cluster {i}: {canon}")
        for u in sorted(urls):
            print(f"    raw: {u}")
            for where in records[u]["where"]:
                print(f"         found in: {where}")

    print("\n--- CROSS-RECORD RESTATEMENTS (same raw URL in >1 corpus source) ---")
    if not restatements:
        print("(none)")
    for u, rec in sorted(restatements.items()):
        print(f"{u}")
        for where in rec["where"]:
            print(f"    - {where}")

    print("\n--- SURFACE FILE NOTE ---")
    surface = ROOT / "watch/inbox/RASHOMON_SURFACE_ELEPHANT_20260914.md"
    surface_urls = sorted({clean_hit(m) for m in URL_RE.findall(surface.read_text(encoding="utf-8"))}) if surface.is_file() else []
    print(f"literal http(s) URLs in RASHOMON_SURFACE_ELEPHANT_20260914.md: {len(surface_urls)}")
    print("(witness sources appear there as prose refs, e.g. 'slashreboot.com, Zenodo 17811909')")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
