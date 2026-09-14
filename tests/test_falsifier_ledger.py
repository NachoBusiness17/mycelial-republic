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


def test_grounding_jsonl_chain_and_schema():
    rows = parse_jsonl(GROUND_JSONL)
    prev = None
    for i, r in enumerate(rows):
        # required fields mapping: accept both 'state' or 'verdict', and 'ts' or 'timestamp'
        assert 'claim' in r, f"row {i} missing claim"
        assert 'evidence' in r, f"row {i} missing evidence"
        state_val = r.get('state') or r.get('verdict')
        assert state_val is not None, f"row {i} missing state/verdict"
        assert state_val in ('SUPPORTED', 'DISPUTED', 'UNPROVEN', 'UNVERIFIED', 'REJECTED'), f"row {i} state invalid: {state_val}"
        assert 'hash' in r, f"row {i} missing hash"
        # verify prev linkage
        if prev is None:
            # first row prev may be None or missing
            pass
        else:
            assert r.get('prev') == prev, f"row {i} prev mismatch: expected {prev} got {r.get('prev')}"
        # verify hash shape: 64-hex string and prev linkage
        h = r['hash']
        assert isinstance(h, str) and len(h) in (64, 128), f"row {i} hash looks wrong: {h[:16]}..."
        # prev linkage must point to previous row's hash
        if prev is None:
            # first row may have prev == '0'*64 or missing
            pass
        else:
            assert r.get('prev') == prev, f"row {i} prev mismatch: expected {prev} got {r.get('prev')}"
        prev = r['hash']


def test_evidence_local_pointers_resolve():
    rows = parse_jsonl(GROUND_JSONL)
    for i, r in enumerate(rows):
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
