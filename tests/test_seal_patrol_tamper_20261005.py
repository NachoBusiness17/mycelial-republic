"""R3 trust landing tests: forged seal shapes + the append/rewrite taxonomy
(2026-10-05). Fold row 3 (watch/inbox/ractor_engine/2026-10-05-ouroboros-
r3-trust/SYNTHESIS.md) proved three fooling shapes on the old patrol, each
pinned here against the upgraded organ:

(a) a forged appended row erased drift (a lens probe took 12 drifted files
    to 0) - now the witness rule holds it: a hand-typed row (no writer, no
    register partner) cannot clear a file whose witnessed seals are
    prefix-broken.
(b) a backdated row masked the true latest seal (last-row-wins returned
    CLEAN on a violated newest seal) - now max-TS selection ignores ledger
    order and takes the newest ts per file.
(c) whole-bytes compare could not split living append boards (permanently
    red) from true rewrites - now the stamped byte length plus the
    incremental prefix hash classifies append (quiet) vs rewrite (alarm).

Chain verify: per-writer backward nonce/seq and prev-digest mismatches are
exit 2 (cannot verify); batch seals sharing a nonce and forward gaps are
legitimate writer history and never fatal.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import tools.prepush_seal_patrol as psp

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "prepush_seal_patrol.py"
PY = sys.executable

T1 = "2026-10-05T12:00:00+00:00"
T2 = "2026-10-05T13:00:00+00:00"
T3 = "2026-10-05T14:00:00+00:00"
T0 = "2026-10-05T11:00:00+00:00"  # backdated


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _board(root: Path, rel: str, data: bytes) -> Path:
    path = root / "watch/inbox" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _abs(root: Path, rel: str) -> str:
    return str(root / "watch/inbox" / rel).replace("\\", "/")


def _seal(root: Path, rel: str, data: bytes, ts: str, nonce: int = 100) -> list[dict]:
    """A real writer's seal: register (writer + nonce + seq, relative path)
    then its autoseal pair (absolute path, stamped byte length, sha)."""
    return [
        {"ts": ts, "op": "register", "file": rel, "sha256": _sha(data),
         "class": "receipt", "purpose": "autoseal register", "writer": "md-record-seal",
         "nonce": nonce, "seq": 1790900000000000000 + nonce},
        {"ts": ts, "op": "autoseal", "file": _abs(root, rel), "bytes": len(data),
         "sha256": _sha(data), "purpose": "autoseal (rib.md.record.v1)"},
    ]


def _ledger(root: Path, rows: list[dict], extra: str = "") -> Path:
    led = root / "watch/inbox/index_events.jsonl"
    led.parent.mkdir(parents=True, exist_ok=True)
    led.write_text("".join(json.dumps(r) + "\n" for r in rows) + extra,
                   encoding="utf-8")
    return led


def _cli(root: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, str(TOOL), "--root", str(root),
         "--ledger", "watch/inbox/index_events.jsonl", *extra],
        capture_output=True, text=True, timeout=60)


# shape (a): the forged fresh row erasing drift


def test_forged_fresh_row_cannot_erase_drift(tmp_path):
    """The fold's eraser: file rewritten after a real seal, then a hand-typed
    row appended claiming the drifted bytes with a fresh ts. Last-row-wins
    returned CLEAN; now the unwitnessed row cannot clear a prefix-broken
    witnessed seal and the file alarms."""
    v1 = b"sealed content line one\n"
    f = _board(tmp_path, "board/x.md", v1)
    rows = _seal(tmp_path, "board/x.md", v1, T1)
    v2 = b"rewritten sealed content\n"          # in-place rewrite, no re-seal
    f.write_bytes(v2)
    rows.append({"ts": T3, "op": "autoseal", "file": _abs(tmp_path, "board/x.md"),
                 "bytes": len(v2), "sha256": _sha(v2),
                 "purpose": "hand-typed, no writer, no register pair"})
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "board/x.md" in r.stdout
    assert "without writer identity" in r.stdout


# shape (b): the backdated row masking the newest seal


def test_backdated_row_cannot_mask_newest_seal(tmp_path):
    """The fold's mask: file sealed at T1 (v1) then T2 (v2, the true newest),
    later edited to v3, then a backdated row (ts T0 < T1) claiming v3 appended
    last. Last-row-wins picked the forged row and returned CLEAN; max-TS
    selects the T2 seal and the violation alarms as a rewrite."""
    v1, v2, v3 = b"first sealed body\n", b"second sealed body, longer\n", b"tampered body\n"
    _board(tmp_path, "board/y.md", v1)
    rows = _seal(tmp_path, "board/y.md", v1, T1, nonce=100)
    rows += _seal(tmp_path, "board/y.md", v2, T2, nonce=101)
    _board(tmp_path, "board/y.md", v3)          # violates the T2 seal
    rows.append({"ts": T0, "op": "autoseal", "file": _abs(tmp_path, "board/y.md"),
                 "bytes": len(v3), "sha256": _sha(v3), "purpose": "backdated forgery"})
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "board/y.md" in r.stdout
    assert "rewrote sealed content" in r.stdout


# shape (c): the append/rewrite taxonomy


def test_prefix_pure_append_is_quiet(tmp_path):
    """A living append board: sealed v1, then bytes appended with no re-seal.
    The old whole-bytes compare cried DRIFT forever; the prefix hash proves
    the sealed bytes survived verbatim and the file counts append-quiet."""
    v1 = b"board header\nrow one\n"
    f = _board(tmp_path, "board/live.md", v1)
    rows = _seal(tmp_path, "board/live.md", v1, T1)
    f.write_bytes(v1 + b"row two appended later\nrow three\n")
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("SEAL-PATROL: ok")
    assert "1 append-quiet" in r.stdout


def test_rewrite_of_sealed_content_alarms_with_evidence(tmp_path):
    """An in-place rewrite of the same length: nothing appended, sealed bytes
    gone. The rewrite class names the file, both sha heads, and the prefix
    evidence (ledger line + stamped sealed length)."""
    v1 = b"AAAA sealed payload BBBB\n"
    f = _board(tmp_path, "board/z.md", v1)
    rows = _seal(tmp_path, "board/z.md", v1, T1)
    f.write_bytes(b"AAAA tampered payload BBBB\n")   # same length, rewritten
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "rewrote sealed content: watch/inbox/board/z.md" in r.stdout
    assert "is no longer a prefix of the file" in r.stdout
    assert f"({len(v1)} sealed bytes)" in r.stdout
    assert _sha(v1)[:12] in r.stdout


def test_shrunken_file_is_a_rewrite(tmp_path):
    """A file that shrank below its stamped sealed length cannot pass any
    prefix test: rewrite class, not quiet."""
    v1 = b"0123456789abcdef" * 8
    f = _board(tmp_path, "board/shrink.md", v1)
    rows = _seal(tmp_path, "board/shrink.md", v1, T1)
    f.write_bytes(b"short")
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 1
    assert "board/shrink.md" in r.stdout


def test_resealed_rewrite_is_quiet(tmp_path):
    """The legit writer path: content rewritten THEN re-sealed through the
    writer. The newest seal exact-matches, so the earlier broken prefix is
    expected history, never a finding."""
    v1, v2 = b"first body\n", b"second body after a proper re-seal\n"
    _board(tmp_path, "board/r.md", v1)
    rows = _seal(tmp_path, "board/r.md", v1, T1, nonce=100)
    _board(tmp_path, "board/r.md", v2)
    rows += _seal(tmp_path, "board/r.md", v2, T2, nonce=101)
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "board/r.md" not in r.stdout


def test_register_row_inherits_bytes_from_autoseal_pair(tmp_path):
    """The register row (writer + nonce, no bytes of its own) inherits the
    stamped length of its same-file same-sha autoseal pair, so a
    register-selected seal still classifies. Selected by the lineno tiebreak
    on equal ts: the later line (the register placed after its autoseal)."""
    v1 = b"pair sealed body\n"
    f = _board(tmp_path, "board/pair.md", v1)
    auto = {"ts": T1, "op": "autoseal", "file": _abs(tmp_path, "board/pair.md"),
            "bytes": len(v1), "sha256": _sha(v1), "purpose": "autoseal"}
    reg = {"ts": T1, "op": "register", "file": "board/pair.md", "sha256": _sha(v1),
           "writer": "md-record-seal", "nonce": 100, "seq": 1790900000000000100}
    _ledger(tmp_path, [auto, reg])
    f.write_bytes(v1 + b"appended after the pair\n")   # append past the seal
    result = psp.patrol(tmp_path, [auto, reg], 150)
    assert result["appended"] and not result["drifted"]


# chain verify: exit 2 on breaks, quiet on legitimate writer history


def test_backward_nonce_breaks_chain_exit_2(tmp_path):
    """A forged or reordered register row: the writer's nonce goes backward
    in ledger order. The ledger itself is untrustworthy: cannot-verify 2."""
    v1 = b"chain body\n"
    _board(tmp_path, "board/c1.md", v1)
    rows = _seal(tmp_path, "board/c1.md", v1, T1, nonce=101)
    rows.append({"ts": T2, "op": "register", "file": "board/c1.md",
                 "sha256": _sha(v1), "writer": "md-record-seal",
                 "nonce": 100, "seq": 1790900000000000100,
                 "purpose": "forged reused nonce"})
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "seal chain broken" in r.stdout
    assert "goes backward" in r.stdout


def test_backward_seq_breaks_chain_exit_2(tmp_path):
    """Same law on the seq clock: ns-stamp going backward under a forward
    nonce is still an order break."""
    v1 = b"chain body two\n"
    _board(tmp_path, "board/c2.md", v1)
    rows = _seal(tmp_path, "board/c2.md", v1, T1, nonce=101)
    rows.append({"ts": T2, "op": "register", "file": "board/c2.md",
                 "sha256": _sha(v1), "writer": "md-record-seal",
                 "nonce": 102, "seq": 1790900000000000050,
                 "purpose": "forged backdated seq"})
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 2
    assert "seq" in r.stdout and "goes backward" in r.stdout


def test_batch_nonce_and_forward_gap_never_fatal(tmp_path):
    """Writer history the chain must NOT flag: batch seals sharing one nonce
    (measured 10 duplicate steps in the live window's md-record-seal rows)
    and a forward gap (multi-surface writers, measured across the corpus)."""
    v1, v2, v3 = b"b1\n", b"b2\n", b"b3\n"
    _board(tmp_path, "board/b1.md", v1)
    _board(tmp_path, "board/b2.md", v2)
    _board(tmp_path, "board/b3.md", v3)
    rows = _seal(tmp_path, "board/b1.md", v1, T1, nonce=200)
    rows += _seal(tmp_path, "board/b2.md", v2, T1, nonce=200)   # batch share
    rows += _seal(tmp_path, "board/b3.md", v3, T2, nonce=205)   # forward gap
    _ledger(tmp_path, rows)
    r = _cli(tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr


def test_prev_digest_chain_verifies_and_breaks(tmp_path):
    """Rows stamped prev = digest of the previous sha row: a correct chain is
    quiet; one wrong link is a cannot-verify break."""
    v1, v2 = b"d1\n", b"d2\n"
    _board(tmp_path, "board/d1.md", v1)
    _board(tmp_path, "board/d2.md", v2)
    r1 = {"ts": T1, "op": "register", "file": "board/d1.md", "sha256": _sha(v1),
          "writer": "md-record-seal", "nonce": 300, "seq": 1790900000000000300}
    r2 = {"ts": T2, "op": "register", "file": "board/d2.md", "sha256": _sha(v2),
          "writer": "md-record-seal", "nonce": 301, "seq": 1790900000000000301}
    r2["prev"] = psp._row_digest(r1)
    _ledger(tmp_path, [r1, r2])
    good = _cli(tmp_path)
    assert good.returncode == 0, good.stdout + good.stderr
    r2_bad = dict(r2, prev="f" * 64)
    _ledger(tmp_path, [r1, r2_bad])
    bad = _cli(tmp_path)
    assert bad.returncode == 2
    assert "prev-digest break" in bad.stdout


def test_max_ts_selects_newest_seal_not_last_row(tmp_path):
    """Unit pin on the selection order itself: three seals for one file, the
    NEWEST ts sits in the middle of the ledger; the verdict follows the
    newest ts (v3), not the last row (v1)."""
    v1, v2, v3 = b"one\n", b"two\n", b"three\n"
    f = _board(tmp_path, "board/s.md", v3)
    rows = [
        {"file": "board/s.md", "sha256": _sha(v1), "op": "register", "ts": T1},
        {"file": "board/s.md", "sha256": _sha(v3), "op": "register", "ts": T3},
        {"file": "board/s.md", "sha256": _sha(v2), "op": "register", "ts": T2},
    ]
    result = psp.patrol(tmp_path, rows, 150)
    assert len(result["matched"]) == 1        # the T3 seal (v3) is operative
    assert result["drifted"] == []
    f.write_bytes(b"drifted\n")
    result2 = psp.patrol(tmp_path, rows, 150)
    assert len(result2["drifted"]) == 1       # against the T3 seal's sha
