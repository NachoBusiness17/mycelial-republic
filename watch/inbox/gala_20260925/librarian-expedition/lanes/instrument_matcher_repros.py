"""instrument_matcher_repros.py - instrument-audit lane (gala 2026-10-01, division B).

PART A: defect-aware matching of the newest holdings tranche (7 persona_priorart
        papers landed 2026-09-30T22:55Z, after the last holdings-audit run 18:28Z)
        across every channel the three instruments expose.
PART B: repro of suspected NEW defects, all inside temp dirs (no repo writes):
        R1: librarian_catalog.verify_canon crashes on a missing canon file
            (the `missing` counter at mag/librarian_catalog.py:145 is dead code)
        R2: librarian_catalog.verify_canon passes destroyed content with a valid
            hash (no magic-byte or readability check anywhere in it)
        R3a: holdings_audit dup detector sensitivity: planted duplicate IS caught
        R3b: holdings_audit dup detector self-report: overlapping shelves produce
             phantom groups (the 09-30 "149 duplicate groups" mechanism)
        R4: holdings_audit PDF magic check reads only 8 bytes: destroyed body passes
Run: .venv/Scripts/python.exe instrument_matcher_repros.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
sys.path.insert(0, str(ROOT))
from mag import holdings_audit, librarian_catalog  # noqa: E402
from mag.librarian import ARXIV, receipt_state  # noqa: E402

STOP = set("a an the of for and or in on to by with at as from is are be".split())


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())


def salient(title: str, n: int = 8) -> str:
    toks = [t for t in norm(title).split() if t and t not in STOP]
    return " ".join(toks[:n])


def ledgers() -> list:
    out = []
    for l in sorted(ROOT.glob("memory/runs/**/*LANDING*.json")):
        d = json.loads(l.read_text(encoding="utf-8"))
        for r in (d.get("rows") or []):
            out.append((str(l), r))
    return out


def part_a() -> dict:
    rows = ledgers()
    claimed = {}
    for l, r in rows:
        if str(r.get("status", "")).startswith("LANDED") and r.get("landed"):
            claimed[r["landed"]] = {"ledger": Path(l).name, "row": r}
    pulled, hashed, _pdf_tokens = receipt_state()
    rec_dir = ROOT / "docs/report_v1/sources/receipts"
    recs = sorted(rec_dir.glob("*.md"))

    seen_stems = [p for p in recs if ARXIV.search(p.stem)]
    blind = [p for p in recs if not ARXIV.search(p.stem)]

    # semantic-title channel: does a LANDED ledger title appear (normalized,
    # first 8 salient words) inside the receipt text?
    rec_text = {}
    for p in recs:
        rec_text[p] = norm(p.read_text(encoding="utf-8", errors="replace")[:20000])
    title_recovered = 0
    for p in blind:
        land = claimed.get("corpus/papers_reference_nonredistributable/" + p.stem + ".pdf")
        if not land:
            for _l, r in rows:
                if str(r.get("receipt", "")).endswith(p.name) and r.get("title"):
                    land = {"row": r}
                    break
        if land and land["row"].get("title"):
            if salient(land["row"]["title"]) in rec_text[p]:
                title_recovered += 1

    # the newest tranche, per file, across every channel
    persona = [p for p in recs if p.stem.startswith("persona_priorart_")]
    matrix = []
    for p in persona:
        stem = p.stem
        text = p.read_text(encoding="utf-8", errors="replace")[:20000]
        arxiv_in_stem = bool(ARXIV.search(stem))
        m_text = ARXIV.search(text)
        land = next(({"ledger": Path(l).name, "row": r} for l, r in rows
                     if str(r.get("landed", "")).endswith(stem + ".pdf")), None)
        disk = ROOT / "corpus/papers_reference_nonredistributable" / (stem + ".pdf")
        disk_ok = False
        magic = False
        if disk.exists():
            data = disk.read_bytes()
            row_sha = (land or {}).get("row", {}).get("sha256")
            disk_ok = (not row_sha) or hashlib.sha256(data).hexdigest() == row_sha
            magic = data[:8].startswith(b"%PDF-")
        matrix.append({
            "receipt": stem + ".md",
            "arxiv_id_in_stem": arxiv_in_stem,
            "receipt_state_sees": arxiv_in_stem,
            "arxiv_id_in_receipt_text": bool(m_text),
            "in_UNREGISTERED_report": bool(m_text) and ("arxiv:" + m_text.group(1) in
                                                        (ROOT / "watch/LIBRARIAN_REPORT.md").read_text(encoding="utf-8", errors="replace")),
            "ledger_claim": land["ledger"] if land else None,
            "on_disk": disk.exists(),
            "sha_matches_ledger": disk_ok,
            "pdf_magic_ok": magic,
            "in_fts_catalog": False,
            "in_librarian_catalog_shelves": False,
        })

    return {
        "receipts_on_disk": len(recs),
        "receipt_state_sees": len(seen_stems),
        "receipt_state_blind": len(blind),
        "blind_recovered_by_semantic_title": title_recovered,
        "newest_tranche_matrix": matrix,
    }


def part_b() -> dict:
    out = {}

    # ==== R1 + R2: librarian_catalog.verify_canon in temp ====
    tmp = Path(tempfile.mkdtemp(prefix="inst_audit_"))
    try:
        canon = tmp / "canon"
        canon.mkdir()
        good = canon / "good.txt"
        good.write_bytes(b"clean readable content")
        destroyed = canon / "destroyed.txt"
        destroyed.write_bytes(b"\x00" * 4096)
        mf = canon / "MANIFEST.sha256"
        mf.write_text(
            hashlib.sha256(good.read_bytes()).hexdigest() + "  good.txt\n"
            + hashlib.sha256(destroyed.read_bytes()).hexdigest() + "  destroyed.txt\n",
            encoding="utf-8")
        old = librarian_catalog.CANON
        librarian_catalog.CANON = canon
        try:
            r2 = librarian_catalog.verify_canon()
            out["R2_destroyed_content_valid_hash"] = {
                "verdict": r2,
                "passes": bool(r2.get("ok")),
            }
            # R1: unlink a claimed file; the manifest still names it
            (canon / "good.txt").unlink()
            try:
                r1 = librarian_catalog.verify_canon()
                out["R1_missing_file"] = {"crashed": False, "verdict": r1}
            except FileNotFoundError as e:
                out["R1_missing_file"] = {"crashed": True, "exception": type(e).__name__,
                                          "detail": str(e)[:120]}
        finally:
            librarian_catalog.CANON = old
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ==== R3a/R3b: holdings_audit dup detector in temp ====
    tmp2 = Path(tempfile.mkdtemp(prefix="inst_audit_dup_"))
    try:
        (tmp2 / "shelves/a").mkdir(parents=True)
        (tmp2 / "shelves/a/sub").mkdir(parents=True)
        (tmp2 / "shelves/b").mkdir(parents=True)
        body = b"unique holding bytes " * 100
        (tmp2 / "shelves/a/holding1.txt").write_bytes(body)
        (tmp2 / "shelves/a/sub/holding1_copy.txt").write_bytes(body)
        (tmp2 / "shelves/a/holding2.txt").write_bytes(b"other bytes " * 100)
        (tmp2 / "shelves/b/holding3.txt").write_bytes(b"shelf b bytes " * 100)
        old_root, old_shelves, old_rec = holdings_audit.ROOT, holdings_audit.SHELVES, holdings_audit.RECEIPTS
        holdings_audit.ROOT = tmp2
        holdings_audit.RECEIPTS = tmp2 / "receipts"
        try:
            holdings_audit.SHELVES = ["shelves/a", "shelves/b"]
            r3a = holdings_audit.audit()
            out["R3a_planted_duplicate"] = {
                "duplicate_groups": r3a["direction_2_disk_to_claims"]["duplicate_groups"],
                "findings": [f for f in r3a["findings"] if f.startswith("DUPLICATE-GROUP")],
                "sensitivity_ok": r3a["direction_2_disk_to_claims"]["duplicate_groups"] == 1,
            }
            holdings_audit.SHELVES = ["shelves/a", "shelves/a/sub", "shelves/b"]
            r3b = holdings_audit.audit()
            child_files = sum(1 for _ in (tmp2 / "shelves/a/sub").rglob("*") if _.is_file())
            out["R3b_overlap_phantoms"] = {
                "duplicate_groups": r3b["direction_2_disk_to_claims"]["duplicate_groups"],
                "child_files": child_files,
                "self_report_reproduced": r3b["direction_2_disk_to_claims"]["duplicate_groups"] == child_files,
            }
        finally:
            holdings_audit.ROOT, holdings_audit.SHELVES, holdings_audit.RECEIPTS = old_root, old_shelves, old_rec
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)

    # ==== R4: PDF magic check reads 8 bytes; destroyed body passes ====
    tmp3 = Path(tempfile.mkdtemp(prefix="inst_audit_pdf_"))
    try:
        sh = tmp3 / "shelves/ref"
        sh.mkdir(parents=True)
        destroyed_pdf = b"%PDF-1.7" + b"\x00" * 100000
        (sh / "destroyed.pdf").write_bytes(destroyed_pdf)
        (tmp3 / "memory/runs/x").mkdir(parents=True)
        (tmp3 / "memory/runs/x/X_LANDING.json").write_text(json.dumps({
            "rows": [{"status": "LANDED", "landed": "shelves/ref/destroyed.pdf",
                      "sha256": hashlib.sha256(destroyed_pdf).hexdigest(),
                      "bytes": len(destroyed_pdf)}]}), encoding="utf-8")
        old_root, old_shelves, old_rec, old_globs = (
            holdings_audit.ROOT, holdings_audit.SHELVES, holdings_audit.RECEIPTS, holdings_audit.LEDGER_GLOBS)
        holdings_audit.ROOT = tmp3
        holdings_audit.SHELVES = ["shelves/ref"]
        holdings_audit.RECEIPTS = tmp3 / "receipts"
        holdings_audit.LEDGER_GLOBS = ["memory/runs/**/*LANDING*.json"]
        try:
            r4 = holdings_audit.audit()
            out["R4_pdf_magic_8bytes"] = {
                "unreadable": r4["content_checks"]["unreadable"],
                "clean": r4["clean"],
                "hash_ok": r4["direction_1_claims_to_disk"]["ok"],
                "destroyed_body_passed": r4["clean"] is True,
            }
        finally:
            (holdings_audit.ROOT, holdings_audit.SHELVES, holdings_audit.RECEIPTS,
             holdings_audit.LEDGER_GLOBS) = (old_root, old_shelves, old_rec, old_globs)
    finally:
        shutil.rmtree(tmp3, ignore_errors=True)

    return out


if __name__ == "__main__":
    a = part_a()
    b = part_b()
    print(json.dumps({"PART_A_matcher": a, "PART_B_repros": b}, indent=1, ensure_ascii=False))
