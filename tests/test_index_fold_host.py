"""tests for scripts/index_fold_host.mjs (B2-40, 2026-09-26).

Covers the two defects the B2-02 receipt filed as owed:
  1. OUTSIDE_RE dropped register events (file starting watch/ etc.) SILENTLY;
     the fold must now surface them as fold_warnings + WARN + exit 2.
  2. nextSeq was a float64 no-op past 2^53 (every node append on 09-26 wrote
     the constant seq 1789823567015749400); seq must now advance exactly,
     staying a JSON number under 2^53 and becoming a decimal string past it.

B2-156 (2026-09-26) adds the living-file law coverage (spec:
watch/inbox/LIVING_HASH_LAW_20260926.md): add --living seals (sha256, size)
over the file's first size bytes; verify counts append-only growth as
living-ok, keeps prefix mutation and truncation as hard failures, and leaves
the whole-file rule for plain registers untouched.

B2-149 + B2-157 (2026-09-26) add the composed-prefix case: drift-patrol-cron
minted /board/inbox/C:/Users/.../watch/inbox/burn_wave_20260926/QUEUE.md
(index_events.jsonl line 3053), so normInboxFile must strip the board|app/inbox
prefix AND the absolute host inbox root in one pass, and a post-normalize path
that still fails the inbox-relative check must drop with a fold warning.

B2-279 (2026-09-26) pins the sort-totality law: the B2-40 comparator mixed
BigInt seq compare with a ts fallthrough, which is non-transitive, so within
the 2^53 quantization band last-register-wins was decided by sort luck refold
to refold (B2-254 measured QUEUE.md and phone_relay_log.jsonl flipping across
four refolds with zero registers between). Every event now carries one
total-order key: null-seq events key on (ts, file order) strictly below every
seq event, integer Number seqs past MAX_SAFE_INTEGER keep their parsed BigInt
but are demoted below every exact seq with a counted fold warning, and exact
seqs (safe integers and digit-only decimal strings) compare exactly via
BigInt. The refold-stability test below is the pinned falsifier.

B2-329 (2026-09-26) pins the dump purity law: the `events` command strips every
underscore-prefixed field (the reserved fold-internal prefix: _outside,
_unresolved) from its output, so downstream consumers parse writer-shaped
event content only, and the log bytes stay untouched by the dump.

Runs the real script with node against a throwaway inbox via INDEX_INBOX_DIR;
the durable watch/inbox is never touched by these tests.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "index_fold_host.mjs"
NODE = shutil.which("node")

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

pytestmark = pytest.mark.skipif(NODE is None, reason="node not available")


def _run(inbox, *args, writer="b2-40-test"):
    env = dict(
        os.environ,
        INDEX_INBOX_DIR=str(inbox).replace("\\", "/"),
        INDEX_WRITER=writer,
    )
    return subprocess.run(
        [NODE, str(SCRIPT), *args],
        env=env,
        cwd=str(inbox),
        capture_output=True,
        text=True,
        timeout=120,
        creationflags=HEADLESS,
    )


def _mk_inbox(tmp_path, events=()):
    inbox = tmp_path / "inbox"
    inbox.mkdir(exist_ok=True)  # exist_ok: B2-157 tests pre-create dirs to seed real payload bytes
    lines = "".join(json.dumps(e) + "\n" for e in events)
    (inbox / "index_events.jsonl").write_text(lines, encoding="utf-8")
    return inbox


def _events(inbox):
    out = []
    for ln in (inbox / "index_events.jsonl").read_text(encoding="utf-8").splitlines():
        if ln.strip():
            out.append(json.loads(ln))
    return out


def test_outside_dropped_register_warns(tmp_path):
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": 1,
                "ts": "2026-09-26T00:00:00Z",
                "op": "register",
                "file": "watch/inbox/POISON_20260926.md",
                "sha256": "X",
                "writer": "boot-lane",
                "nonce": 1,
            }
        ],
    )
    (inbox / "CLEAN_20260926.md").write_text("clean", encoding="utf-8")
    r = _run(inbox, "add", "CLEAN_20260926.md", "receipt", "b2-40 test")
    assert "add: appended seq" in r.stdout, r.stdout + r.stderr
    assert r.returncode == 2, (r.returncode, r.stderr)  # fold warning channel
    assert "outside-dropped register" in r.stderr
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    warns = " ".join(idx["fold_warnings"])
    assert "outside-dropped register" in warns
    assert "watch/" in warns
    assert "x1" in warns
    paths = [it["path"] for it in idx["items"]]
    assert "CLEAN_20260926.md" in paths
    assert "watch/inbox/POISON_20260926.md" not in paths


def test_seq_stays_number_within_2pow53(tmp_path):
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": 5,
                "ts": "2026-09-26T00:00:00Z",
                "op": "register",
                "file": "SEED.md",
                "sha256": "X",
                "writer": "w",
                "nonce": 1,
            }
        ],
    )
    (inbox / "A.md").write_text("a", encoding="utf-8")
    r = _run(inbox, "add", "A.md")
    assert "add: appended seq 6" in r.stdout, r.stdout + r.stderr
    ev = _events(inbox)[-1]
    assert isinstance(ev["seq"], int) and ev["seq"] == 6


def test_seq_advances_past_2pow53_as_exact_string(tmp_path):
    lim = 2**53 - 1  # Number.MAX_SAFE_INTEGER; the last exactly representable stop
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": lim,
                "ts": "2026-09-26T00:00:00Z",
                "op": "register",
                "file": "SEED.md",
                "sha256": "X",
                "writer": "w",
                "nonce": 1,
            }
        ],
    )
    (inbox / "A.md").write_text("a", encoding="utf-8")
    (inbox / "B.md").write_text("b", encoding="utf-8")
    assert "add: appended seq" in _run(inbox, "add", "A.md").stdout
    assert "add: appended seq" in _run(inbox, "add", "B.md").stdout
    s1 = _events(inbox)[-2]["seq"]
    s2 = _events(inbox)[-1]["seq"]
    assert isinstance(s1, str) and s1 == str(lim + 1)  # 2^53 exactly, no float loss
    assert isinstance(s2, str) and int(s2) == lim + 2 and s2 != s1


def test_seq_never_sticks_at_production_scale(tmp_path):
    stuck = 1789823567015749400  # the constant every 09-26 node append carried
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": stuck,
                "ts": "2026-09-26T00:00:00Z",
                "op": "register",
                "file": "SEED.md",
                "sha256": "X",
                "writer": "w",
                "nonce": 1,
            }
        ],
    )
    (inbox / "A.md").write_text("a", encoding="utf-8")
    (inbox / "B.md").write_text("b", encoding="utf-8")
    assert "add: appended seq" in _run(inbox, "add", "A.md").stdout
    assert "add: appended seq" in _run(inbox, "add", "B.md").stdout
    s1 = _events(inbox)[-2]["seq"]
    s2 = _events(inbox)[-1]["seq"]
    assert s1 != s2, "nextSeq no-op regression: two appends share one seq"
    assert isinstance(s1, str) and int(s2) == int(s1) + 1


def test_fold_orders_string_missing_and_legacy_seq(tmp_path):
    # B2-279 2026-09-26 re-derived this expectation under the sort-totality
    # law: null-seq events key strictly below every seq event (tier 0), the
    # past-2^53 number 1789823567015749400 is an inexact double (tier 1,
    # demoted, counted on the fold-warning channel), and the decimal string
    # is exact (tier 2). The old expectation (LEGACY above STRINGSEQ by
    # BigInt, NOSEQ slotted by ts in the middle) encoded the non-transitive
    # comparator this lane replaced.
    inbox = _mk_inbox(
        tmp_path,
        [
            {  # md_record_seal.py appends registers with NO seq field
                "ts": "2026-09-26T00:00:03Z",
                "op": "register",
                "file": "NOSEQ.md",
                "sha256": "X",
                "writer": "md-record-seal",
                "nonce": 1,
            },
            {
                "seq": 1789823567015749400,
                "ts": "2026-09-26T00:00:01Z",
                "op": "register",
                "file": "LEGACY.md",
                "sha256": "X",
                "writer": "w",
                "nonce": 1,
            },
            {  # the 2026-09-26 scheme: decimal string past 2^53
                "seq": "9007199254740992000",
                "ts": "2026-09-26T00:00:02Z",
                "op": "register",
                "file": "STRINGSEQ.md",
                "sha256": "X",
                "writer": "w",
                "nonce": 2,
            },
        ],
    )
    r = _run(inbox, "rebuild")
    assert r.returncode == 2, r.stderr  # the inexact-double warning channel
    assert "inexact double seq events demoted below every exact seq" in r.stderr
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    # Canonical order under the B2-279 total order: null-seq tier lowest,
    # then the demoted quantized double, then every exact seq above it.
    assert [it["path"] for it in idx["items"]] == [
        "NOSEQ.md",
        "LEGACY.md",
        "STRINGSEQ.md",
    ]
    warns = " ".join(idx["fold_warnings"])
    assert "inexact double seq events demoted below every exact seq: 1 event(s)" in warns


# ---------------------------------------------------------------------------
# B2-279 sort totality (2026-09-26). Defect: the B2-40 comparator mixed
# BigInt seq compare with a ts fallthrough (non-transitive; counterexample
# A seq 2 ts early, B no-seq ts mid, C seq 1 ts late gives C<A<B<C), so the
# 2^53 quantization band decided last-register-wins by sort luck refold to
# refold (B2-254 measured QUEUE.md and phone_relay_log.jsonl flipping across
# four refolds with zero register events between).
# ---------------------------------------------------------------------------

# The production band shapes: a raw past-2^53 literal (python writes the raw
# digits; node's JSON.parse quantizes it, ulp 256 at this magnitude) and an
# exact decimal string whose value sits above the parsed double.
BAND_RAW_LITERAL = 1789823567015749474  # parses to the double ...376 in node
EXACT_ABOVE_BAND = "1789823567015749380"  # B2-145-style exact string seq


def _snapshot_index(inbox):
    d = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    # derived_at moves on every fold by design; stability is about items and
    # warnings.
    return {"items": d["items"], "fold_warnings": d.get("fold_warnings", [])}


def _append_note(inbox, n):
    """Append a state-free note event with an exact decimal-string seq minted
    like the B2-40 scheme (quoted so JSON.parse never quantizes it). Notes
    change the event array shape, which is what exercised the old sort luck."""
    lim = 2**53 - 1
    mx = 0
    for ln in (inbox / "index_events.jsonl").read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        ev = json.loads(ln)
        s = ev.get("seq")
        if isinstance(s, int) and s >= 0:
            mx = max(mx, s)
        elif isinstance(s, str) and s.isdigit():
            mx = max(mx, int(s))
    nxt = mx + n
    ev = {
        "seq": nxt if nxt <= lim else str(nxt),
        "ts": f"2026-09-26T16:{n:02d}:00Z",
        "op": "note",
        "file": "NOTE.md",
        "writer": "b2-279-test",
    }
    with (inbox / "index_events.jsonl").open("a", encoding="utf-8", newline="") as fh:
        fh.write(json.dumps(ev) + "\n")
    return ev


def test_inexact_band_register_loses_to_later_exact_register(tmp_path):
    # The B2-254 disease shape: a whole-file register with a raw past-2^53
    # literal (quantizes into the band double) vs a chronologically-later
    # exact-seq register of the SAME file, with null-seal-style events
    # interleaved between them (the interleave that made the old comparator
    # non-transitive). The exact register must win last-register-wins by law,
    # and the demotion must surface as a counted fold warning.
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": BAND_RAW_LITERAL,
                "ts": "2026-09-26T12:03:24Z",
                "op": "register",
                "file": "VICTIM.md",
                "sha256": "BANDBYTES",
                "purpose": "hash refresh: gala-night writes evolved after registration",
                "writer": "drift-patrol-cron",
            },
            {  # null-seq autoseal-style interleave, exactly the poison class
                "ts": "2026-09-26T12:30:00Z",
                "op": "register",
                "file": "SEALED.md",
                "sha256": "S",
                "writer": "md-record-seal",
            },
            {
                "seq": EXACT_ABOVE_BAND,
                "ts": "2026-09-26T13:12:05Z",
                "op": "register",
                "file": "VICTIM.md",
                "sha256": "EXACTBYTES",
                "writer": "zcode-b2-254",
            },
        ],
    )
    (inbox / "VICTIM.md").write_text("v", encoding="utf-8")
    (inbox / "SEALED.md").write_text("s", encoding="utf-8")
    r = _run(inbox, "rebuild")
    assert r.returncode == 2, (r.returncode, r.stderr)
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    item = next(it for it in idx["items"] if it["path"] == "VICTIM.md")
    assert item["sha256"] == "EXACTBYTES", idx["items"]
    warns = " ".join(idx["fold_warnings"])
    assert "inexact double seq events demoted below every exact seq: 1 event(s)" in warns
    assert "1789823567015749376" in warns  # the parsed double, named in the warning


def test_total_order_breaks_the_old_cycle(tmp_path):
    # The literal non-transitivity counterexample: under the old comparator
    # C(seq 1, late ts) < A(seq 2, early ts) < B(no-seq, mid ts) < C, a cycle.
    # Under the B2-279 law the null-seq event keys strictly below every seq
    # event, so the ascending canonical order is B first, then seq 1, seq 2:
    # every pairwise comparison agrees, no cycle, refold to refold.
    inbox = _mk_inbox(
        tmp_path,
        [
            {"seq": 2, "ts": "2026-09-26T09:00:00Z", "op": "register", "file": "A.md", "sha256": "a", "writer": "w"},
            {"ts": "2026-09-26T10:00:00Z", "op": "register", "file": "B.md", "sha256": "b", "writer": "w"},
            {"seq": 1, "ts": "2026-09-26T11:00:00Z", "op": "register", "file": "C.md", "sha256": "c", "writer": "w"},
        ],
    )
    for n in ("A.md", "B.md", "C.md"):
        (inbox / n).write_text(n.lower(), encoding="utf-8")
    r = _run(inbox, "rebuild")
    assert r.returncode == 0, (r.returncode, r.stderr)
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    assert [it["path"] for it in idx["items"]] == ["B.md", "C.md", "A.md"]


def test_refold_stability_with_dummy_appends_between(tmp_path):
    # The pinned B2-279 falsifier: refold five times with a dummy append
    # between; any active-item or fold-warning change dies. The event mix is
    # the full pathological set: band doubles, exact strings, same-file
    # competing registers, and null-seq interleaves on both sides.
    events = [
        {"seq": 2, "ts": "2026-09-26T09:00:00Z", "op": "register", "file": "EARLYSEQ.md", "sha256": "e1", "writer": "w"},
        {"seq": BAND_RAW_LITERAL, "ts": "2026-09-26T12:03:24Z", "op": "register", "file": "BAND.md", "sha256": "BANDOLD", "writer": "patrol"},
        {"ts": "2026-09-26T12:30:00Z", "op": "register", "file": "SEALA.md", "sha256": "s", "writer": "md-record-seal"},
        {"seq": EXACT_ABOVE_BAND, "ts": "2026-09-26T13:12:05Z", "op": "register", "file": "BAND.md", "sha256": "BANDNEW", "writer": "w"},
        {"seq": 1, "ts": "2026-09-26T13:30:00Z", "op": "register", "file": "SEQONE.md", "sha256": "q", "writer": "w"},
        {"ts": "2026-09-26T13:31:00Z", "op": "register", "file": "SEALB.md", "sha256": "t", "writer": "md-record-seal"},
        {"seq": BAND_RAW_LITERAL, "ts": "2026-09-26T12:03:25Z", "op": "register", "file": "BAND2.md", "sha256": "B2OLD", "writer": "patrol"},
    ]
    inbox = _mk_inbox(tmp_path, events)
    for n, body in (("BAND.md", "b1"), ("SEALA.md", "s1"), ("SEQONE.md", "q"), ("SEALB.md", "t"), ("BAND2.md", "b2")):
        (inbox / n).write_text(body, encoding="utf-8")
    assert "rebuild: folded" in _run(inbox, "rebuild").stdout
    first = _snapshot_index(inbox)
    for i in range(1, 6):
        r = _run(inbox, "rebuild")
        assert "rebuild: folded" in r.stdout, r.stdout + r.stderr
        snap = _snapshot_index(inbox)
        assert snap == first, f"refold {i} moved active items: {_diff_paths(first, snap)}"
        _append_note(inbox, i)  # dummy state-free append between refolds


def _diff_paths(a, b):
    pa = [it["path"] for it in a["items"]]
    pb = [it["path"] for it in b["items"]]
    return {"order_or_set_changed": pa != pb, "before": pa, "after": pb}


# ---------------------------------------------------------------------------
# B2-156 living-file law (spec: watch/inbox/LIVING_HASH_LAW_20260926.md)
# ---------------------------------------------------------------------------

def _register_and_get_item(inbox, name):
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    return next(it for it in idx["items"] if it["path"] == name)


def test_living_add_seals_prefix_and_growth_passes(tmp_path):
    inbox = _mk_inbox(tmp_path)
    board = inbox / "BOARD.md"
    sealed = b"line one\nline two\n"
    board.write_bytes(sealed)
    r = _run(inbox, "add", "BOARD.md", "board", "burn queue", "--living")
    assert "add: appended seq" in r.stdout, r.stdout + r.stderr
    item = _register_and_get_item(inbox, "BOARD.md")
    assert item["living"] is True
    assert item["size"] == len(sealed)
    # a concurrent-writer style append after registration must NOT be a failure
    with board.open("ab") as fh:
        fh.write(b"line three (appended later)\n")
    r = _run(inbox, "verify")
    assert "0 mismatched" in r.stdout, r.stdout
    assert "1 living-ok" in r.stdout, r.stdout
    assert "--- failures ---" not in r.stdout, r.stdout


def test_living_prefix_mutation_is_a_hard_failure(tmp_path):
    inbox = _mk_inbox(tmp_path)
    board = inbox / "BOARD.md"
    board.write_bytes(b"sealed history bytes\n")
    assert "add: appended seq" in _run(inbox, "add", "BOARD.md", "board", "--living").stdout
    board.write_bytes(b"TAMPERED history bytes\nplus an appended line\n")
    r = _run(inbox, "verify")
    assert "LIVING PREFIX MISMATCH: BOARD.md" in r.stdout, r.stdout
    assert "1 mismatched" in r.stdout, r.stdout


def test_living_truncation_is_a_hard_failure(tmp_path):
    inbox = _mk_inbox(tmp_path)
    board = inbox / "BOARD.md"
    board.write_bytes(b"0123456789\n")
    assert "add: appended seq" in _run(inbox, "add", "BOARD.md", "board", "--living").stdout
    board.write_bytes(b"01234")
    r = _run(inbox, "verify")
    assert "LIVING TRUNCATED: BOARD.md" in r.stdout, r.stdout


def test_plain_register_keeps_whole_file_seal(tmp_path):
    inbox = _mk_inbox(tmp_path)
    doc = inbox / "DOC.md"
    doc.write_bytes(b"static doc\n")
    assert "add: appended seq" in _run(inbox, "add", "DOC.md", "receipt").stdout
    item = _register_and_get_item(inbox, "DOC.md")
    assert "living" not in item, "plain add must not grow a living flag"
    with doc.open("ab") as fh:
        fh.write(b"append\n")
    r = _run(inbox, "verify")
    assert "HASH MISMATCH: DOC.md" in r.stdout, r.stdout
    assert "0 living-ok" in r.stdout, r.stdout


def test_readd_without_living_drops_the_flag(tmp_path):
    inbox = _mk_inbox(tmp_path)
    board = inbox / "BOARD.md"
    board.write_bytes(b"v1\n")
    assert "add: appended seq" in _run(inbox, "add", "BOARD.md", "board", "--living").stdout
    board.write_bytes(b"v2 rewritten\n")  # semantic rewrite: re-seal whole file
    assert "add: appended seq" in _run(inbox, "add", "BOARD.md", "board", "rewrite").stdout
    item = _register_and_get_item(inbox, "BOARD.md")
    assert "living" not in item, "last-register-wins: a plain re-add unsets living"
    r = _run(inbox, "verify")
    assert "0 mismatched" in r.stdout, r.stdout


def test_living_without_size_seal_is_counted_not_failed(tmp_path):
    # legacy row shape: living:true but registered before the size seal existed
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": 1,
                "ts": "2026-09-26T00:00:00Z",
                "op": "register",
                "file": "LEGACY_LIVING.md",
                "sha256": "DEADBEEF",
                "living": True,
                "writer": "w",
                "nonce": 1,
            }
        ],
    )
    (inbox / "LEGACY_LIVING.md").write_bytes(b"whatever bytes\n")
    assert "rebuild: folded" in _run(inbox, "rebuild").stdout
    r = _run(inbox, "verify")
    assert "LIVING UNVERIFIED (no size seal): LEGACY_LIVING.md" in r.stdout, r.stdout
    assert "1 living-unverified" in r.stdout, r.stdout
    assert "0 mismatched" in r.stdout, r.stdout


def test_living_open_insertions_are_counted_never_failed(tmp_path):
    # edit-shaped board: growth happens by mid-file insertion (QUEUE.md appends
    # its rows under the ## Open anchor), so no byte prefix stays stable; the
    # open shape declares that and verify only counts it.
    inbox = _mk_inbox(tmp_path)
    board = inbox / "QUEUE.md"
    board.write_bytes(b"# queue\n## Open\n- [ ] old row\n")
    r = _run(inbox, "add", "QUEUE.md", "board", "burn queue", "--living-open")
    assert "add: appended seq" in r.stdout, r.stdout + r.stderr
    item = _register_and_get_item(inbox, "QUEUE.md")
    assert item["living"] is True and item["seal"] == "open"
    assert "size" not in item
    board.write_bytes(b"# queue\n## Open\n- [ ] new row\n- [ ] old row\n")  # insertion
    r = _run(inbox, "verify")
    assert "1 living-open" in r.stdout, r.stdout
    assert "0 mismatched" in r.stdout, r.stdout
    assert "--- failures ---" not in r.stdout, r.stdout


def test_living_flags_are_mutually_exclusive(tmp_path):
    inbox = _mk_inbox(tmp_path)
    (inbox / "A.md").write_bytes(b"a\n")
    r = _run(inbox, "add", "A.md", "--living", "--living-open")
    assert r.returncode == 1, (r.returncode, r.stdout + r.stderr)
    assert "mutually exclusive" in r.stderr, r.stderr


# ---------------------------------------------------------------------------
# B2-149 + B2-157 composed-prefix normalization (2026-09-26). Production
# evidence: index_events.jsonl line 3053, drift-patrol-cron register with
# file "/board/inbox/C:/Users/.../watch/inbox/burn_wave_20260926/QUEUE.md".
# ---------------------------------------------------------------------------

DEFAULT_ROOT = "C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox"


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_composed_board_prefix_and_host_root_strip_in_one_pass(tmp_path):
    # The exact line-3053 mint shape against the test inbox root: one pass of
    # normInboxFile must land the register on the bare inbox-relative path.
    inbox = tmp_path / "inbox"
    root = str(inbox).replace("\\", "/")
    queue = inbox / "burn_wave_20260926" / "QUEUE.md"
    queue.parent.mkdir(parents=True)
    queue.write_text("q", encoding="utf-8")
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": 1,
                "ts": "2026-09-26T12:03:24Z",
                "op": "register",
                "file": f"/board/inbox/{root}/burn_wave_20260926/QUEUE.md",
                "sha256": _sha(queue),
                "class": "receipt",
                "writer": "drift-patrol-cron",
                "nonce": 1,
            }
        ],
    )
    r = _run(inbox, "rebuild")
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    assert [it["path"] for it in idx["items"]] == ["burn_wave_20260926/QUEUE.md"]
    assert idx["fold_warnings"] == []
    r = _run(inbox, "verify")
    assert "1 hash-clean" in r.stdout, r.stdout


def test_production_default_root_composed_shape_folds_from_foreign_inbox(tmp_path):
    # The literal production bytes of line 3053 folded under a FOREIGN
    # INDEX_INBOX_DIR: the compiled host default root must still strip, so a
    # container/test fold resolves host-minted absolute events.
    inbox = tmp_path / "inbox"
    queue = inbox / "burn_wave_20260926" / "QUEUE.md"
    queue.parent.mkdir(parents=True)
    queue.write_text("q", encoding="utf-8")
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": 1,
                "ts": "2026-09-26T12:03:24Z",
                "op": "register",
                "file": f"/board/inbox/{DEFAULT_ROOT}/burn_wave_20260926/QUEUE.md",
                "sha256": _sha(queue),
                "class": "receipt",
                "writer": "drift-patrol-cron",
                "nonce": 1,
            }
        ],
    )
    r = _run(inbox, "rebuild")
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    assert [it["path"] for it in idx["items"]] == ["burn_wave_20260926/QUEUE.md"]
    r = _run(inbox, "verify")
    assert "1 hash-clean" in r.stdout, r.stdout


def test_bare_absolute_host_root_register_lands_bare(tmp_path):
    # the md_record_seal pre-B2-41 mint shape: C:/Users/.../watch/inbox/<name>
    inbox = tmp_path / "inbox"
    recap = inbox / "RECAP_7D_20260926.md"
    recap.parent.mkdir(parents=True)
    recap.write_text("r", encoding="utf-8")
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "ts": "2026-09-26T11:32:35Z",
                "op": "register",
                "file": f"{DEFAULT_ROOT}/RECAP_7D_20260926.md",
                "sha256": _sha(recap),
                "class": "receipt",
                "writer": "md-record-seal",
                "nonce": 4,
            }
        ],
    )
    r = _run(inbox, "rebuild")
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    assert [it["path"] for it in idx["items"]] == ["RECAP_7D_20260926.md"]
    r = _run(inbox, "verify")
    assert "1 hash-clean" in r.stdout, r.stdout


def test_composed_absolute_invalidate_converges_with_bare_register(tmp_path):
    # B2-145 convergence: a register and its invalidate minted as absolute /
    # composed paths must hit the same post-normalize key as a bare register,
    # so an absolute invalidate kills the absolute register and a later bare
    # re-register survives (the historical fold must not resurrect phantoms).
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": 1789823567015749376,  # stuck-literal family, quantizes like line 3053
                "ts": "2026-09-26T12:03:24Z",
                "op": "register",
                "file": f"/board/inbox/{DEFAULT_ROOT}/burn_wave_20260926/QUEUE.md",
                "sha256": "F230CB5D86E17BCCBEDBE18FCAAA5B5C2F08B427C87CC5518003B241242AFC2E",
                "class": "receipt",
                "writer": "drift-patrol-cron",
                "nonce": 1,
            },
            {
                "seq": "1789823567015749384",  # B2-145 invalidate, exact string seq
                "ts": "2026-09-26T13:12:05Z",
                "op": "invalidate",
                "file": f"{DEFAULT_ROOT}/burn_wave_20260926/QUEUE.md",
                "reason": "phantom absolute host path (B2-145)",
                "writer": "zcode-b2-145-burn-20260926",
                "nonce": 6,
            },
            {
                "seq": "1789823567015749389",  # B2-145 bare re-register
                "ts": "2026-09-26T13:15:42Z",
                "op": "register",
                "file": "burn_wave_20260926/QUEUE.md",
                "sha256": "768798D4CD7EF57F4698A6BBF678E731958F39905F688BFBA40DDF18A3021D4A",
                "class": "BOARD",
                "writer": "zcode-b2-145-burn-20260926",
                "nonce": 7,
            },
        ],
    )
    (inbox / "burn_wave_20260926").mkdir()
    (inbox / "burn_wave_20260926" / "QUEUE.md").write_text("q", encoding="utf-8")
    r = _run(inbox, "rebuild")
    # B2-279 2026-09-26 re-derivation: the seeded register literal
    # 1789823567015749376 is a past-2^53 double, i.e. a quantization-band
    # member, so the fold now emits the counted inexact-double warning
    # (exit 2) while the item outcomes are unchanged: the exact-string
    # invalidate ...384 outranks the demoted band register and the later
    # exact re-register ...389 wins last-register-wins.
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert "inexact double seq events demoted below every exact seq: 1 event(s)" in r.stderr
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    items = [it for it in idx["items"] if it["path"] == "burn_wave_20260926/QUEUE.md"]
    assert len(items) == 1, idx["items"]
    assert items[0]["sha256"] == "768798D4CD7EF57F4698A6BBF678E731958F39905F688BFBA40DDF18A3021D4A"


def test_post_normalize_unresolved_register_warns_and_drops(tmp_path):
    # A drive-letter residue that no known root explains (D:/ elsewhere) and a
    # dot-dot escape both fail the inbox-relative check after normalization:
    # they must not land as items and must surface on the fold-warning channel.
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": 1,
                "ts": "2026-09-26T12:00:00Z",
                "op": "register",
                "file": "D:/elsewhere/STALE_DRIVE.md",
                "sha256": "X",
                "writer": "w",
                "nonce": 1,
            },
            {
                "seq": 2,
                "ts": "2026-09-26T12:01:00Z",
                "op": "register",
                "file": "../escape.md",
                "sha256": "X",
                "writer": "w",
                "nonce": 2,
            },
        ],
    )
    (inbox / "REAL.md").write_text("r", encoding="utf-8")
    r = _run(inbox, "add", "REAL.md", "receipt")
    assert "add: appended seq" in r.stdout, r.stdout + r.stderr
    assert r.returncode == 2, (r.returncode, r.stderr)  # fold warning channel
    assert "unresolvable register" in r.stderr, r.stderr
    assert "D:/" in r.stderr, r.stderr
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    paths = [it["path"] for it in idx["items"]]
    assert paths == ["REAL.md"], paths
    warns = " ".join(idx["fold_warnings"])
    assert "unresolvable register" in warns
    assert "D:/" in warns and "../escape.md" in warns


# B2-329 (2026-09-26) pins the dump purity law: readEvents attaches the fold
# plumbing fields _outside and _unresolved in memory, and the `events` command
# must strip every underscore-prefixed field from its output so downstream
# consumers parse writer-shaped event content only. Underscore is the reserved
# fold-internal prefix. Log bytes are untouched: the fields never existed on
# disk, and this test checks the seeded log bytes read back unchanged after the
# dump. Falsifier companion: watch/inbox/burn_wave_20260926/B2_329_dump_strict_consumer.mjs
# over the production dump.
def test_events_dump_strips_fold_internal_fields(tmp_path):
    inbox = _mk_inbox(
        tmp_path,
        [
            {
                "seq": 1,
                "ts": "2026-09-26T12:00:00Z",
                "op": "register",
                "file": "REAL_20260926.md",
                "sha256": "X",
                "class": "receipt",
                "purpose": "b2-329 dump purity",
                "writer": "w",
                "nonce": 1,
            },
            {
                # Outside register: readEvents attaches _outside=True in memory,
                # the exact field the pre-fix dump leaked (brief falsifier).
                "seq": 2,
                "ts": "2026-09-26T12:01:00Z",
                "op": "register",
                "file": "watch/inbox/POISON_20260926.md",
                "sha256": "X",
                "writer": "boot-lane",
                "nonce": 1,
            },
        ],
    )
    before = (inbox / "index_events.jsonl").read_bytes()
    r = _run(inbox, "events")
    assert r.returncode == 0, (r.returncode, r.stderr)
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    assert len(lines) == 2, lines
    dumped = [json.loads(ln) for ln in lines]
    for ev in dumped:
        for k in ev:
            assert not k.startswith("_"), (k, ev)  # no fold plumbing in the dump
    # Writer-shaped content survives intact, exact key set pinned.
    assert dumped[0] == {
        "seq": 1,
        "ts": "2026-09-26T12:00:00Z",
        "op": "register",
        "file": "REAL_20260926.md",
        "sha256": "X",
        "class": "receipt",
        "purpose": "b2-329 dump purity",
        "writer": "w",
        "nonce": 1,
    }
    assert dumped[1]["file"] == "watch/inbox/POISON_20260926.md"  # content, not _outside
    # The dump is read-only: log bytes on disk are exactly what was seeded.
    assert (inbox / "index_events.jsonl").read_bytes() == before


# ---------------------------------------------------------------------------
# B2-342 (2026-09-26) pins the key schema registry warning: the writer-key
# vocabulary is owned by configs/events_key_schema.json (closed vocabulary,
# not required-fields); every fold warns on any event carrying a key outside
# it (WARN + exit-2 fold_warnings channel), and mag.shared_surface validate
# ERRORS on the same keys. Underscore keys are the reserved fold-internal
# prefix (B2-329) and are exempt.
# ---------------------------------------------------------------------------

def _b2_342_events():
    return [
        {"seq": 1, "ts": "2026-09-26T12:00:00Z", "op": "register", "file": "REAL_20260926.md",
         "sha256": "X", "class": "receipt", "purpose": "b2-342 key schema", "writer": "w", "nonce": 1},
        {"seq": 2, "ts": "2026-09-26T12:01:00Z", "op": "note", "file": "REAL_20260926.md",
         "writer": "w", "nonce": 2},
    ]


def test_unknown_event_key_warns_and_sets_exit_2(tmp_path):
    inbox = _mk_inbox(
        tmp_path,
        _b2_342_events()
        + [{"seq": 3, "ts": "2026-09-26T12:02:00Z", "op": "note", "writer": "rogue",
            "fresh_key_not_in_registry": "x"}],
    )
    r = _run(inbox, "rebuild")
    assert r.returncode == 2, (r.returncode, r.stderr)  # the counted WARN channel
    assert "unknown event key not in configs/events_key_schema.json: fresh_key_not_in_registry" in r.stderr
    assert "register the key" in r.stderr
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    assert any("fresh_key_not_in_registry" in w for w in idx["fold_warnings"])


def test_registered_keys_produce_no_unknown_key_warning(tmp_path):
    inbox = _mk_inbox(tmp_path, _b2_342_events())
    r = _run(inbox, "rebuild")
    assert r.returncode == 0, (r.returncode, r.stderr)
    assert "unknown event key" not in r.stderr
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    assert not any("unknown event key" in w for w in idx["fold_warnings"])


def test_underscore_keys_do_not_trip_the_key_warning(tmp_path):
    # readEvents attaches _outside/_unresolved in memory; the registry gate
    # must never warn on the fold's own plumbing fields (B2-329 prefix law).
    ev = _b2_342_events()[0]
    ev["_outside"] = False
    ev["_unresolved"] = False
    inbox = _mk_inbox(tmp_path, [ev])
    r = _run(inbox, "rebuild")
    assert r.returncode == 0, (r.returncode, r.stderr)
    assert "unknown event key" not in r.stderr


# ---------------------------------------------------------------------------
# B2-380 (2026-09-26): pin the fold minters' key sets against the registry.
# The add/invalidate minters must emit ONLY keys registered in
# configs/events_key_schema.json (closed vocabulary); the appendOp
# unknown-key path exists but never fired for them because nothing tested it.
# Falsifier shape: add ev.probe = 1 to the add minter and these pins name it.
# ---------------------------------------------------------------------------

def _schema_keys():
    schema = ROOT / "configs" / "events_key_schema.json"
    return {k["key"] for k in json.loads(schema.read_text(encoding="utf-8"))["keys"]}


def test_add_minter_keys_are_registered(tmp_path):
    inbox = _mk_inbox(tmp_path)
    (inbox / "probe_target.txt").write_text("payload\n", encoding="utf-8")
    r = _run(inbox, "add", "probe_target.txt", "TEST", "b2-380 add minter")
    assert r.returncode == 0, r.stderr
    last = _events(inbox)[-1]
    assert last["op"] == "register"
    unknown = set(last) - _schema_keys()
    assert not unknown, f"add minter emitted unregistered keys: {sorted(unknown)}"


def test_invalidate_minter_keys_are_registered(tmp_path):
    inbox = _mk_inbox(tmp_path)
    (inbox / "probe_target.txt").write_text("payload\n", encoding="utf-8")
    _run(inbox, "add", "probe_target.txt", "TEST", "b2-380 add")
    r = _run(inbox, "invalidate", "probe_target.txt", "b2-380 invalidate minter")
    assert r.returncode == 0, r.stderr
    last = _events(inbox)[-1]
    assert last["op"] == "invalidate"
    unknown = set(last) - _schema_keys()
    assert not unknown, f"invalidate minter emitted unregistered keys: {sorted(unknown)}"
