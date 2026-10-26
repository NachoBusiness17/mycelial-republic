import json
import os
from pathlib import Path
import pytest
import hashlib

REPO_ROOT = Path(__file__).resolve().parents[1]
GROUND_MD = REPO_ROOT / 'dashboard' / 'static' / 'grounding_wave.md'
GROUND_JSONL = REPO_ROOT / 'watch' / 'GROUNDING_WAVE.jsonl'

ALLOWED_LOCAL_PREFIXES = ['dashboard/', 'watch/', 'memory/', 'scripts/', 'docs/']


def sha_short(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:12]


def parse_jsonl(path: Path):
    if not path.exists():
        pytest.skip(f"{path} missing; skip ledger machine check")
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                pytest.fail(f"invalid jsonl line: {line[:160]}")
            rows.append(obj)
    return rows


def test_grounding_md_exists():
    assert GROUND_MD.exists(), f"Expected {GROUND_MD} in repo"


def _live_rows(rows):
    """v4 admission filter (2026-09-27): rows buried by a cross-signed void
    are effectively dead — the ledger keeps their bytes (delete-as-append)
    but schema/pointer checks walk only LIVE rows. The voids for #122/#123
    (MALFORMED, the frozen truncated row) and #104 (EVIDENCE_DEAD, the
    misnamed art pointer) were posted + operator-witnessed 2026-09-27."""
    from mag.grounding_wave import _admission, _live_claim
    adm = _admission(rows)
    return [(i, r) for i, r in enumerate(rows)
            if _live_claim(rows, i + 1, adm["voided_keys"])]


def test_grounding_jsonl_chain_and_schema():
    rows = parse_jsonl(GROUND_JSONL)
    prev = None
    for i, r in _live_rows(rows):
        # required fields mapping: accept both 'state' or 'verdict', and 'ts' or 'timestamp'
        assert 'claim' in r, f"row {i} missing claim"
        assert 'evidence' in r, f"row {i} missing evidence"
        state_val = r.get('state') or r.get('verdict')
        assert state_val is not None, f"row {i} missing state/verdict"
        assert state_val in ('SUPPORTED', 'DISPUTED', 'UNPROVEN', 'UNVERIFIED', 'REJECTED'), f"row {i} state invalid: {state_val}"
        assert 'hash' in r, f"row {i} missing hash"
        # v4 re-anchor rule: prev may point past a fully-buried stretch
        from mag.grounding_wave import _admission, _reanchor_ok
        if prev is None:
            # first live row prev may be None or missing
            pass
        else:
            adm = _admission(rows)
            assert r.get('prev') == prev or _reanchor_ok(rows, i + 1, r.get('prev'), adm), (
                f"row {i} prev mismatch: expected {prev} got {r.get('prev')} (and not a valid re-anchor)")
        h = r['hash']
        assert isinstance(h, str) and len(h) in (64, 128), f"row {i} hash looks wrong: {h[:16]}..."
        prev = r['hash']


def test_evidence_local_pointers_resolve():
    rows = parse_jsonl(GROUND_JSONL)
    for i, r in _live_rows(rows):
        evidence = r['evidence']
        if isinstance(evidence, str):
            evs = [evidence]
        else:
            evs = list(evidence)
        for e in evs:
            e = e.strip()
            # split combined pointers like 'a + b' or comma lists
            parts = [p.strip() for part in e.replace(')', '').split('+') for p in part.split(',')]
            import re
            for ptxt in parts:
                # remove parenthetical notes, e.g. 'path (MEMORY_TRIM_PROPOSAL.md' or 'path (file)'
                # also strip stray trailing punctuation
                pclean = re.sub(r"\s*\(.*$", "", ptxt).strip().rstrip('.,;')
                if not pclean:
                    continue
                if any(pclean.startswith(pfx) for pfx in ALLOWED_LOCAL_PREFIXES):
                    # if trailing '(' remains, drop it
                    pclean = pclean.replace(' (', '')
                    # if pclean ends with a space then a filename, split and keep the path
                    # e.g. 'memory/runs/batch5_20260906/ (MEMORY_TRIM_PROPOSAL.md' -> 'memory/runs/batch5_20260906/'
                    pclean = pclean.split(' ')[0]
                    p = REPO_ROOT / pclean
                    # allow globs like *.md to match at least one file
                    if any(x in pclean for x in ['*', '?']):
                        import glob
                        matches = list(glob.glob(str(p)))
                        assert matches, f"row {i} evidence glob pointer missing: {pclean} (glob {p})"
                    else:
                        assert p.exists(), f"row {i} evidence pointer missing: {pclean} (resolved {p})"
                else:
                    # external URLs are allowed; no assertion
                    pass
