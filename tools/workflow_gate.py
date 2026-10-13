#!/usr/bin/env python3
"""Workflow gate: fleet dogfood enforcement for dynamic-workflow scripts.

Born 2026-09-25 by operator order: "we need to stop pinging me for workflows,
we need to have a gate that makes sure workflows are being improved, enhanced,
dogfooded, and using our systems like Mickey17 gophers, interagent communication
and steering. Self steal."

The gate runs BEFORE CreateWorkflow submission. It self-steals the ratchet
pattern (exit 2 is the only hard block; every submission registers a row so
improvement is a ledger fact, amend-not-rewrite is visible in digests).

Checks enforced on every script:
  G1 multiplicity   Mickey17 gopher fan-out: per-item named actors in a fan-out
  G2 passoff        interagent communication: an earlier actor's output feeds a later ask
  G3 steering       a reviewer/reader verdict is carried back into a revision ask
  G4 salvage        report() fires inside the fan-out so work survives a dead run
  G5 deliverable    published artifact (markdown/file) plus report-shape return
  G6 receipts       durable receipt lands in watch/inbox, dated (missing date = soft WARN)
  G7 laws           no-fabrication and em-dash law carried inside the asks
  G8 width-shape    TETHERED_LINK width law: declared max_concurrency <= 3 unless
                    the script documents a measured envelope receipt
                    (2026-10-05, curiosity-register row 3, MASTER_READ_ESTATE.md
                    r03#1)

Scenario mode (LAW-12 genesis clause, 2026-09-26): the clause in
watch/inbox/BURN_rsi-harness_20260926.md requires one scenario card per
gate G1-G7, each minted from a real memory/workflows/REGISTRY.jsonl FAIL
row, so every future gate change re-proves itself against observed
failures instead of prose. `check --scenarios configs/workflow_gate_scenarios`
validates the card suite READ-ONLY: cards must cite a registry FAIL row
that actually shows their gate failing, each fixture must produce exactly
the card's expected verdict/warns/exit, and the all-pass control must
pass clean. No registry row is written and no file is modified in
scenario mode.

2026-10-05 (curiosity-register row 3): the suite extends to G8-width-shape
with two cards (hard-fail fixture plus measured-envelope exception fixture)
minted from a real fixture-driven FAIL row; the genesis clause's G1-G7
wording is filed history and stays untouched in the original cards.

2026-10-05 (ouroboros R1 rows 6+7,
watch/inbox/ractor_engine/2026-10-05-ouroboros-r1-fleet/SYNTHESIS.md):
two additive check-time teeth, G1-G8 untouched.
Row 6 stop-cert: a script whose registry status is retired or superseded
cannot mint a fresh PASS row. Registry status shape (the registry carried no
status field before this clause, verified by read): a REGISTRY.jsonl row may
now carry "status": "retired" | "superseded" (the operator's fleet-verdict
pen, e.g. the 2026-10-02 minimum-viable-fleet verdict); a stop-cert row keyed
by name, script path or digest stops re-certification of the same script.
The blocked check still appends its row, verdict "BLOCKED-STOPCERT", exit 2,
so the refusal is itself a ledger fact, not silence.
Row 7 fire ledger: every single-script check appends one row
{ts, script, verdict, digest, fired_args, max_concurrency} to
memory/workflows/FIRE_LEDGER.jsonl (create on first append; append-only,
single writer = this script), joining the declared dispatch width to the
script identity so the journal's width-less fire payloads become joinable.
fired_args is the declared arg surface parsed from the saved-workflow header
block {name: default_or_null}; max_concurrency is parsed with the G8 regex
(null when the script declares none). Scenario mode stays READ-ONLY (no
ledger append, unchanged LAW-12 contract) and --no-register skips the ledger
too, same temp-file-row rationale as the registry skip (seat_law_gate,
2026-09-29).

2026-10-05 (ouroboros R3-L1 move 1,
watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/SYNTHESIS.md
blindness row 1, landing receipt watch/inbox/ouroboros_20261005/
r3_land_gate.md): width truth. The R3 fold proved this gate PASSed a file
whose every dispatch shape lived in a // comment (the banked probe g8_
vacuous_envelope.dwf.ts, PASS exit 0 from repo root, FAIL exit 2 from a
foreign CWD on the same digest: the verdict flipped with the invocation
CWD). Five additive teeth, G1-G8/stop-cert/ledger shapes preserved:
(a) full-line // comments no longer satisfy the G1-G7 shape checks
(strip_comment_lines; /* */ header blocks still carry declarations, the
LAW-12 cards pinned that idiom); (b) G8 hard-fails a non-literal
max_concurrency RHS and counts a width-arg default (parse_declared_args)
as a declared width; (c) the envelope-receipt exception now requires the
named file's BYTES to carry a width-bound measured number, resolved from
REPO_ROOT (Path(__file__).parents[1]), so the verdict cannot flip with CWD
and a directory index is not a measured envelope; (d) an unreadable
script exits 2 (hard block), not 1; (e) the fire ledger joins fired_args
width beside the max_concurrency stamp (fired_width + width_discrepancy
per row, so the row-1 shape, stamp 3 beside fired width 50, is visible
without eyeballing the nested args).

2026-10-07 (port wave P6 port 3, G2 PLACEMENT LAW, additive; from the
swarm-orchestration steal card watch/inbox/frontier_olm_2026-10-07/steal/
swarm-orchestration.md steal 1, ArcticSwarm): G2 passoff has always been
silent on WHERE the interagent feed lives. The law, three lines: interagent
findings feed happens at REVIEW; blind sweeps within a pass are legal;
cross-pass pooling only AFTER review. Rationale: premature consensus is a
search-phase disease; peers that read a plausible frame while searching
converge on it, and the measured ladder (isolation+review 82.6 > fed-search
78.8 > no-review 74.5 > 40-run majority vote 63.5, BrowseComp-Plus, mirror-
fetched twice per the card) puts naive width LAST. Reference implementation
is the flagship mine's own live shape: sweep asks carry area + questions +
estate map + recipe with zero sibling findings
(.zcode/workflows/olm-mine.dwf.ts:272-289), confirms re-fetch single URLs
independently (:342-349), and findings pool only at the steal round where the
drafting agent receives the area's confirmed finds beside a steering reviewer
(:396-403). Enforcement is a WARN-level soft row attached to the G2 check
(same soft family as the G6 dated stamp and the G3 judge-model stamp): when a
script's interagent pass-off shape names a cross-pass pool token BEFORE its
first review-step marker, or names one with no review step at all, the G2 row
goes soft-not-ok with the placement reason. The 0/1/2 exit contract and the
hard G1-G8/stop-cert/ledger shapes are untouched; the detector is a grep
approximation by design, never an AST claim, and a false warn is a review
conversation, not a blocked push.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import sys
from pathlib import Path

REGISTRY = os.path.join("memory", "workflows", "REGISTRY.jsonl")
FIRE_LEDGER = os.path.join("memory", "workflows", "FIRE_LEDGER.jsonl")
SCENARIO_DIR_DEFAULT = os.path.join("configs", "workflow_gate_scenarios")

# R3-L1 move 1c (2026-10-05): repo root for CWD-independent envelope-receipt
# resolution. The pre-fix gate ran os.path.isfile(stamped_path), so the same
# script PASSed from the repo root and FAILed from /tmp (fold re-verified both
# verdicts on digest 661e5b317ecb). Anchored to the module file, never CWD.
REPO_ROOT = Path(__file__).resolve().parents[1]


def strip_comment_lines(text: str) -> str:
    """R3-L1 move 1a (2026-10-05): drop full-line // comments before the
    G1-G7 shape checks. Cause: the R3 banked probe (watch/inbox/ractor_
    engine/2026-10-05-ouroboros-r3-trust/probes/g8_vacuous_envelope.dwf.ts,
    14 comment lines + const placeholder = 1;) passed the pre-fix gate with
    every dispatch shape in a comment, evidence that the checks certified
    spelling, not behavior. Boundary, deliberate: /* */ block-comment lines
    still count (the saved-workflow header-block idiom the LAW-12 cards and
    fixtures pinned), and the soft declaration stamps (G6 dated stamp, G3
    judge-model) stay full-text because they are declarations, not dispatch
    shapes. A block-comment-only fooling shape needs its own dated card
    before this gate rejects it (residue in watch/inbox/ouroboros_20261005/
    r3_land_gate.md)."""
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("//")
    )

# R1 row 6 stop-cert (2026-10-05): registry status values that stop a script
# from minting a fresh PASS row. No registry row carried a status field before
# this clause; the operator's fleet-verdict pen mints them (row 9 surface).
STOPCERT_STATUSES = ("retired", "superseded")

CHECKS = [
    ("G1-multiplicity",
     "Mickey17 gopher fan-out: per-item named actors (agent(\"x-\" + item) inside a fan-out)",
     lambda t: bool(re.search(r'agent\(\s*"[^"]*"\s*\+', t)) or bool(re.search(r'agent\(`[^`]*\+', t)),
    ),
    ("G2-passoff",
     "interagent communication: an earlier actor's output (text/json/path) feeds a later ask",
     lambda t: bool(re.search(r'JSON\.stringify\(\s*\w+\)', t))
     or bool(re.search(r'\+\s*\w+\.(text|issues|stdout|path|quotes)\b', t)),
    ),
    ("G3-steering",
     "steering: reviewer/reader feedback carried back into a revision ask",
     lambda t: ("reported these issues" in t)
     or ("cold reader reported" in t)
     or bool(re.search(r'Previous critique', t))
     or bool(re.search(r'\.(issues|feedback|comments|critique)\b[^\n]{0,200}ask<', t, re.S)),
    ),
    ("G4-salvage",
     "incremental report() inside the fan-out (work survives a dead run)",
     lambda t: bool(re.search(r'report\(\s*\w+\s*\)\s*;', t)),
    ),
    ("G5-deliverable",
     "published deliverable (artifact.markdown/file) plus report-shape return (conclusion:)",
     lambda t: ("artifact.markdown(" in t or "artifact.file(" in t) and ("conclusion:" in t),
    ),
    # SPEC t69 (wired from t62 next_steal): a receipt-path mention must also carry a dated stamp (t62 prefilter family, label + YYYY-MM-DD); a missing stamp is a soft-false WARN row with a reason, never a new hard-block exit (0/1/2 contract unchanged).
    ("G6-receipts",
     "durable receipt landing in watch/inbox with a dated stamp",
     lambda t: ("watch/inbox" in t) or ("watch\\inbox" in t),
    ),
    ("G7-laws",
     "no-fabrication and em-dash law carried inside the asks",
     lambda t: ("no em-dashes" in t)
     and ("never fabricate" in t or "no-fabrication" in t or "never synthesize" in t),
    ),
    # G8 (2026-10-05, curiosity-register row 3 r03#1): the TETHERED_LINK width
    # law as a submit-time instrument. HARD fail: workflow children get zero
    # adapter retries, so an over-envelope width is the 429-storm shape that
    # killed dwfrun-15738edf. Exception: a documented measured envelope receipt
    # (the operator max-concurrency standing law of 2026-09-26).
    ("G8-width-shape",
     "dispatch shape is the retry strategy (TETHERED_LINK width law): declared"
     " max_concurrency (literal stamp or width-arg default) <= 3 unless the"
     " script documents a measured envelope receipt whose bytes carry the width",
     lambda t: g8_width_shape_ok(t),
    ),
]

# t69: dated-stamp requirement behind G6, same regex family as the
# githooks/pre-push freshness prefilter (t62): label set + colon + YYYY-MM-DD,
# case-insensitive like freshness_gate.STAMP_RE. A receipt mention without a
# matching line is a soft finding, not a gate failure.
G6_STAMP_RE = re.compile(
    r"(?i)\b(source[-_ ]fetched|fetched|observed[-_]at)\s*:\s*\d{4}-\d{2}-\d{2}"
)


G6_SOFT_REASON = (
    "receipt mention lacks a dated stamp (label + YYYY-MM-DD, t62 prefilter family);"
    " soft-warn, not a hard block"
)

# B2-206 (2026-09-26): judge-independence marker behind G3, same soft-warn
# family as G6. The dwf facade gives subagents the session model only ("no
# per-subagent model choice", dynamic-workflows skill), so independence is a
# FIRING contract, not a script line: a workflow with a fresh-reader judge
# seat must declare the cross-family model the operator fires it with
# (CreateWorkflow/AmendWorkflow subagent_model), as a `judge-model:` stamp.
# G3 steering present but no stamp => soft-warn naming the B2-60 D2 finding;
# exit contract untouched. Falsifier from B2-60: one cross-family reviewer
# fold vs the same-model baseline.
G3_JUDGE_MODEL_RE = re.compile(
    r"(?i)\b(judge[-_ ]?model|subagent[_ ]?model)\s*:\s*[a-z0-9][a-z0-9._/-]+"
)

G3_SOFT_REASON = (
    "judge independence undeclared: the fresh-reader seat runs same-session-model"
    " (B2-60 D2, context freshness is not weight independence); declare"
    " 'judge-model: <provider/model>' naming the cross-family subagent_model to"
    " fire with; soft-warn, not a hard block"
)

# G2 PLACEMENT LAW (2026-10-07, port wave P6 port 3, swarm-orchestration steal
# card steal 1, ArcticSwarm): findings feed belongs at review; blind sweeps
# within a pass are legal; cross-pass pooling only after review. Grep
# approximation on purpose (the docstring clause names it): the detector reads
# comment-stripped code text for a cross-pass pool token and a review-step
# marker, never an AST. WARN-only soft row on G2, exit contract untouched.
# Calibrated this sitting: .zcode/workflows/olm-mine.dwf.ts (the reference
# implementation) carries zero pool tokens, so the live shape stays clean, and
# no scenario fixture carries a pool token, so the LAW-12 suite stays green.
G2_CROSS_POOL_RE = re.compile(
    r"(?i)cross[\s_-]?pass[\s_-]?(?:pool|findings|results|sweep)s?\b"
    r"|\ball[\s_-]?findings\b"
    r"|\bfindings[\s_-]?pool\b"
    r"|\bpooled\b"
)
G2_REVIEW_STEP_RE = re.compile(
    r"(?i)\b(reviewer|review round|review ask|steering|steer|critique|cold reader)\b"
)
G2_PLACEMENT_SOFT_REASON = (
    "G2 placement law (2026-10-07, ArcticSwarm via the swarm-orchestration steal"
    " card): a cross-pass pool is named before the first review step (or with no"
    " review step at all). The law: interagent findings feed happens at review;"
    " blind sweeps within a pass are legal; cross-pass pooling only after review."
    " Reference shape: .zcode/workflows/olm-mine.dwf.ts:272-289 blind sweep asks,"
    " :342-349 independent confirms, :396-403 pooling at the steal round beside"
    " the reviewer. Grep approximation, WARN-only; the 0/1/2 exit contract is"
    " unchanged"
)


def g2_placement_positions(text: str) -> tuple:
    """(first cross-pass pool position, first review-step position) over
    comment-stripped code text; either entry is None when absent."""
    pool = G2_CROSS_POOL_RE.search(text)
    review = G2_REVIEW_STEP_RE.search(text)
    return (
        pool.start() if pool else None,
        review.start() if review else None,
    )


def g2_placement_pool_before_review(text: str) -> bool:
    """True when a cross-pass pool token precedes the first review step (or a
    pool token exists with no review step anywhere). Soft warn only. Reads
    comment-stripped code text (strip_comment_lines, idempotent) so a pool
    token living only in a full-line // comment certifies and warns about
    nothing - the G8 comment-fooling lesson, warn side."""
    stripped = strip_comment_lines(text)
    pool_pos, review_pos = g2_placement_positions(stripped)
    return pool_pos is not None and (
        review_pos is None or pool_pos < review_pos
    )

# G8-width-shape (2026-10-05, curiosity-register row 3 r03#1,
# corpus/steal/MASTER_READ_ESTATE.md): converts the TETHERED_LINK width law
# (corpus/steal/TETHERED_LINK_STEAL_20260925.md, as amended by B2-435 with the
# proven-width table in watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md
# and watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md) from
# 11 days of AGENTS.md prose into a submit-time gate. Workflow children ride
# maxAttempts 0 (zero adapter retries), so the dispatch shape is the retry
# strategy: a 50-wide fan-out on the coding-plan account 429-storms it (code
# 1302) and crashes tethered sessions with fake subscription errors. A script
# that declares max_concurrency above 3 must document a measured envelope
# receipt with an `envelope-receipt: <path>` stamp naming an existing
# watch/inbox file (the operator max-concurrency standing law of 2026-09-26).
G8_MAX_CONCURRENCY_RE = re.compile(r"max_concurrency\s*[:=]\s*(\d+)")
G8_ENVELOPE_STAMP_RE = re.compile(r"(?i)\benvelope[-_ ]receipt\s*:\s*([^\s'\"`,)]+)")

# R3-L1 move 1b (2026-10-05): the whole RHS after max_concurrency[:=], so a
# non-literal shape (a variable, Number(x), ${arg}) is a hard FAIL instead of
# an invisible "undeclared". The width law binds a declared integer literal.
G8_MAX_CONCURRENCY_RHS_RE = re.compile(r"max_concurrency\s*[:=]\s*([^\n]*)")

# R3-L1 move 1b: arg names whose declared default is a fired width (the
# FIRE_LEDGER row-1 shape: fired_args carried width "50" while the comment
# stamp read max_concurrency 3; a width riding an arg must declare like one).
G8_WIDTH_ARG_KEYS = ("width", "max_concurrency")

# R3-L1 move 1c (2026-10-05): the envelope exception verifies BYTES, not
# existence. A receipt counts only when some line carries a number tightly
# bound to a width token (width(s) N / max_concurrency N / N-wide, transition
# values like 50->14 excluded) with a measurement-evidence word in the window
# and no failure word on the line, after date/time tokens are sterilized (a
# bare YYYY or 20260926 is a date, not a width). Calibrated 2026-10-05:
# watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md carries width 10
# ("measured a new rung: Task agents width 10"); watch/inbox/INDEX.json
# carries none at any width (929KB of index purposes, zero width-bound
# measurements), and AFTERPARTY itself carries no clean 50 (the 50-wide row
# is the 1302 storm, and the strike list that quotes "50-wide clean" says
# "do not cite as measured").
G8_RECEIPT_PAIR_RE = re.compile(
    r"(?:\bwidths?\b|\bmax_concurrency\b|\bconcurrenc\w*)[^\S\n]{0,6}[:=]?[^\S\n]{0,6}(?<!->)(\d{1,4})\b(?!->)"
    r"|(?<!->)(\d{1,4})\b(?!->)[^\S\n]{0,2}[-\s][^\S\n]{0,2}wide\b",
    re.I,
)
G8_RECEIPT_MEASURE_WORDS = (
    "measured", "proven", "clean", "ceiling", "ladder", "sustained",
    "tok/h", "absorbed",
)
G8_RECEIPT_FAIL_WORDS = (
    "storm", "1302", "429", "crash", "death", "fail", "untested",
    "do not cite",
)
G8_RECEIPT_DATE_RES = (
    re.compile(r"\b20\d{2}-\d{2}-\d{2}\b"),
    re.compile(r"\b20\d{6}\b"),
    re.compile(r"\b20\d{2}\b"),
    re.compile(r"\b\d{1,2}:\d{2}"),
)


def _receipt_line_numbers(line: str) -> str:
    """Sterilize date/time tokens so a YYYY or compact date is never read
    as a measured width number."""
    s = line
    for rx in G8_RECEIPT_DATE_RES:
        s = rx.sub(" ", s)
    return s


def receipt_carries_measured_width(receipt_text: str, declared: int) -> bool:
    """True when the receipt's bytes carry a width-bound measured number at
    or above the declared width (R3-L1 move 1c calibration above)."""
    for line in receipt_text.splitlines():
        low = line.lower()
        if any(w in low for w in G8_RECEIPT_FAIL_WORDS):
            continue
        sterile = _receipt_line_numbers(line)
        for m in G8_RECEIPT_PAIR_RE.finditer(sterile):
            num = m.group(1) or m.group(2)
            if not num or int(num) < declared:
                continue
            a, b = max(0, m.start() - 45), min(len(sterile), m.end() + 45)
            window = sterile[a:b].lower()
            if any(w in window for w in G8_RECEIPT_MEASURE_WORDS):
                return True
    return False


def declared_arg_widths(text: str) -> list:
    """Numeric defaults of width-arg declarations (parse_declared_args),
    counted as declared widths by G8 (R3-L1 move 1b)."""
    widths = []
    for key, val in parse_declared_args(text).items():
        if key in G8_WIDTH_ARG_KEYS and isinstance(val, str) and val.strip().isdigit():
            widths.append(int(val.strip()))
    return widths


def g8_width_check(text: str) -> tuple:
    """(ok, reason) for the width law. Hard fails: a non-literal
    max_concurrency RHS; a declared width (stamp literal or width-arg
    default) above 3 without an envelope receipt whose bytes carry a
    width-bound measured number for that width, resolved from REPO_ROOT so
    the verdict cannot flip with the invocation CWD (R3-L1 moves 1b/1c)."""
    for m in G8_MAX_CONCURRENCY_RHS_RE.finditer(text):
        rhs = m.group(1).strip()
        token = rhs.split()[0] if rhs else ""
        if not token or not token.isdigit():
            shown = token if token else "(empty)"
            return False, (
                f"non-literal max_concurrency RHS {shown}: declare an integer"
                " literal (the width law binds the declared dispatch shape,"
                " R3-L1 move 1b)"
            )
    widths = [int(w) for w in G8_MAX_CONCURRENCY_RE.findall(text)]
    widths.extend(declared_arg_widths(text))
    if not widths or max(widths) <= 3:
        return True, ""
    declared = max(widths)
    for m in G8_ENVELOPE_STAMP_RE.finditer(text):
        path = m.group(1)
        if ("watch/inbox" not in path) and ("watch\\inbox" not in path):
            continue
        resolved = REPO_ROOT / path.replace("\\", "/")
        if not resolved.is_file():
            continue
        try:
            receipt_text = resolved.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if receipt_carries_measured_width(receipt_text, declared):
            return True, ""
    return False, (
        f"declared width {declared} above 3 with no measured envelope receipt"
        " whose bytes carry it: the envelope-receipt stamp must name a"
        " watch/inbox file carrying a width-bound measured number at or above"
        f" {declared} (R3-L1 move 1c: file existence alone is not a measurement)"
    )


def g8_width_shape_ok(text: str) -> bool:
    """Width law boolean (compat wrapper over g8_width_check)."""
    return g8_width_check(text)[0]


def run_checks(text: str) -> list:
    """Run the G1-G8 gate checks over script text (shared by check paths).

    R3-L1 move 1a (2026-10-05): the G1-G7 shape checks read
    strip_comment_lines(text), so a full-line // comment satisfies nothing
    (the banked comment-only probe must FAIL, not PASS). G8 keeps the full
    text because its declarations (the max_concurrency stamp, the
    envelope-receipt stamp) are documentation stamps by design; its truth
    now comes from g8_width_check. The soft declaration stamps (G6 dated
    stamp, G3 judge-model) also search the full text: they certify
    declarations, not dispatch shapes."""
    code_text = strip_comment_lines(text)
    rows = []
    for cid, desc, fn in CHECKS:
        if cid == "G8-width-shape":
            ok, hard_reason = g8_width_check(text)
        else:
            ok, hard_reason = bool(fn(code_text)), ""
        row = {"id": cid, "ok": ok, "desc": desc}
        # t69: G6 soft-false. Receipt mention present but no dated stamp:
        # mark the row not-ok with a reason, keep it out of the failed set,
        # so the verdict and the 0/1/2 exit contract are untouched.
        if cid == "G6-receipts" and ok and not G6_STAMP_RE.search(text):
            row["ok"] = False
            row["soft"] = True
            row["reason"] = G6_SOFT_REASON
        # B2-206: G3 soft-false. Steering present but no judge-model stamp:
        # the reviewer certifies steering, not weight independence.
        if cid == "G3-steering" and ok and not G3_JUDGE_MODEL_RE.search(text):
            row["ok"] = False
            row["soft"] = True
            row["reason"] = G3_SOFT_REASON
        # G2 placement law (2026-10-07, port wave P6 port 3): pass-off present
        # but a cross-pass pool is named before the first review step (or with
        # no review step). Soft row only; exit contract untouched.
        if cid == "G2-passoff" and ok and g2_placement_pool_before_review(code_text):
            row["ok"] = False
            row["soft"] = True
            row["reason"] = G2_PLACEMENT_SOFT_REASON
        # R3-L1: G8 hard-fail reason (width truth is behavioral, say why).
        if cid == "G8-width-shape" and not ok and hard_reason:
            row["reason"] = hard_reason
        rows.append(row)
    return rows


def split_rows(rows: list) -> tuple:
    """Return (failed_ids, warned_ids) from run_checks rows."""
    failed = [r["id"] for r in rows if not r["ok"] and not r.get("soft")]
    warned = [r["id"] for r in rows if r.get("soft")]
    return failed, warned


def load_registry_index() -> dict:
    """Index registry rows by (ts, digest); tolerant of malformed lines."""
    index = {}
    if not os.path.exists(REGISTRY):
        return index
    with open(REGISTRY, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            index[(row.get("ts"), row.get("digest"))] = row
    return index


def load_stopcert_index() -> dict:
    """R1 row 6 (2026-10-05): latest stop-cert surface from REGISTRY.jsonl,
    keyed by name, script path and digest. Tolerant of malformed lines."""
    stops = {"names": set(), "scripts": set(), "digests": set()}
    if not os.path.exists(REGISTRY):
        return stops
    with open(REGISTRY, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(row.get("status", "")).lower() not in STOPCERT_STATUSES:
                continue
            for key in ("name", "script"):
                val = row.get(key)
                if val:
                    val = str(val)
                    stops["names" if key == "name" else "scripts"].add(val)
                    stops["names" if key == "name" else "scripts"].add(
                        os.path.basename(val.replace("\\", "/")))
            if row.get("digest"):
                stops["digests"].add(str(row["digest"]))
    return stops


def stop_cert_reason(script: str, digest: str, stops: dict) -> str:
    """Non-empty reason string when the script carries a retired/superseded
    registry status, else ""."""
    base = os.path.basename(script.replace("\\", "/"))
    norm_script = script.replace("\\", "/")
    hits = []
    if base in stops["names"]:
        hits.append(f"name {base} carries a {STOPCERT_STATUSES[0]}/{STOPCERT_STATUSES[1]} registry status row")
    if norm_script in stops["scripts"]:
        hits.append(f"script path {script} carries a {STOPCERT_STATUSES[0]}/{STOPCERT_STATUSES[1]} registry status row")
    if digest in stops["digests"]:
        hits.append(f"digest {digest} carries a {STOPCERT_STATUSES[0]}/{STOPCERT_STATUSES[1]} registry status row")
    return "; ".join(hits)


def max_declared_width(text: str):
    """Max declared max_concurrency (G8 instrument), None when undeclared."""
    widths = [int(w) for w in G8_MAX_CONCURRENCY_RE.findall(text)]
    return max(widths) if widths else None


def parse_declared_args(text: str) -> dict:
    """R1 row 7: the declared firing surface from the saved-workflow header
    block, {name: default_or_null}. No args block: {}. Best effort by design;
    the ledger joins fires to width, it does not re-validate declarations."""
    m = re.search(r"(?m)^args:\s*$(.*?)(?=^\S|\Z)", text, re.S)
    if not m:
        return {}
    out = {}
    current = None
    for line in m.group(1).splitlines():
        name = re.match(r"^  ([A-Za-z_][\w-]*):\s*$", line)
        if name:
            current = name.group(1)
            out.setdefault(current, None)
            continue
        if current:
            d = re.match(r"^\s+default:\s*(.+?)\s*$", line)
            if d:
                out[current] = d.group(1).strip().strip('"').strip("'")
    return out


def validate_card(card, label: str, known_ids: set, registry_index: dict) -> str:
    """Structural + citation validation. Returns an error string or ""."""
    required = [
        "gate_id", "cited_fail_row", "scenario_input",
        "expected_verdict", "regression_criterion", "rollback_note",
    ]
    for key in required:
        if key not in card:
            return f"missing required field '{key}'"
    gate_id = card["gate_id"]
    if gate_id not in known_ids:
        return f"unknown gate_id '{gate_id}'"
    cited = card["cited_fail_row"]
    if not isinstance(cited, dict):
        return "cited_fail_row must be an object with ts, digest, name"
    key = (cited.get("ts"), cited.get("digest"))
    row = registry_index.get(key)
    if row is None:
        return (
            f"cited FAIL row (ts={cited.get('ts')}, digest={cited.get('digest')})"
            " not found in " + REGISTRY
        )
    if row.get("verdict") != "FAIL":
        return f"cited row {key} has verdict {row.get('verdict')}, not FAIL"
    check = next((c for c in row.get("checks", []) if c.get("id") == gate_id), None)
    if check is None or check.get("ok") is not False:
        return f"cited row does not show {gate_id} failing"
    if not os.path.isfile(card["scenario_input"]):
        return f"scenario_input not found: {card['scenario_input']}"
    expected = card["expected_verdict"]
    if not isinstance(expected, dict):
        return "expected_verdict must be an object"
    if expected.get("overall") not in ("PASS", "FAIL"):
        return "expected_verdict.overall must be PASS or FAIL"
    for field in ("failed_checks", "warn_checks"):
        val = expected.get(field)
        if not isinstance(val, list) or any(v not in known_ids for v in val):
            return f"expected_verdict.{field} must be a list of known gate ids"
    if expected.get("exit_code") not in (0, 1, 2):
        return "expected_verdict.exit_code must be 0, 1 or 2"
    for field in ("regression_criterion", "rollback_note"):
        if not isinstance(card[field], str) or not card[field].strip():
            return f"{field} must be a non-empty string"
    return ""


def run_scenarios(scen_dir: str) -> int:
    """Validate the scenario card suite. READ-ONLY: never writes a row."""
    card_paths = sorted(glob.glob(os.path.join(scen_dir, "*.card.json")))
    if not card_paths:
        print(f"SCENARIOS ERROR: no *.card.json cards under {scen_dir}")
        return 1
    known_ids = {cid for cid, _, _ in CHECKS}
    registry_index = load_registry_index()
    failures = []
    for card_path in card_paths:
        label = os.path.basename(card_path)
        try:
            with open(card_path, encoding="utf-8") as f:
                card = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"SCENARIOS ERROR {label}: cannot read card: {exc}")
            failures.append(label)
            continue
        err = validate_card(card, label, known_ids, registry_index)
        if err:
            print(f"SCENARIOS ERROR {label}: {err}")
            failures.append(label)
            continue
        with open(card["scenario_input"], encoding="utf-8") as f:
            text = f.read()
        failed, warned = split_rows(run_checks(text))
        expected = card["expected_verdict"]
        verdict = "FAIL" if failed else "PASS"
        problems = []
        if verdict != expected["overall"]:
            problems.append(f"verdict {verdict} != expected {expected['overall']}")
        if failed != expected["failed_checks"]:
            problems.append(f"failed {failed} != expected {expected['failed_checks']}")
        if warned != expected["warn_checks"]:
            problems.append(f"warned {warned} != expected {expected['warn_checks']}")
        exit_code = 2 if failed else 0
        if exit_code != expected["exit_code"]:
            problems.append(f"exit {exit_code} != expected {expected['exit_code']}")
        if problems:
            print(f"SCENARIOS FAIL {label}: " + "; ".join(problems))
            failures.append(label)
        else:
            print(
                f"SCENARIOS ok   {label}: {card['gate_id']} -> {verdict}"
                f" exit {exit_code} fixture={card['scenario_input']}"
            )
    control = os.path.join(scen_dir, "fixtures", "pass_control.dwf.ts")
    if os.path.isfile(control):
        with open(control, encoding="utf-8") as f:
            ctext = f.read()
        cfailed, cwarned = split_rows(run_checks(ctext))
        if cfailed or cwarned:
            print(f"SCENARIOS FAIL pass_control: failed={cfailed} warned={cwarned}")
            failures.append("pass_control")
        else:
            print(f"SCENARIOS ok   pass_control: all {len(CHECKS)} gates clean")
    if failures:
        print(f"SCENARIOS: {len(failures)} of {len(card_paths)} cards red (read-only run, no registry row)")
        return 2
    print(f"SCENARIOS: {len(card_paths)} cards validated read-only (no registry row written)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Fleet workflow dogfood gate")
    ap.add_argument("cmd", choices=["check"], help="check a workflow script against the gate")
    ap.add_argument("--script", default=None, help="path to the .dwf.ts workflow script")
    ap.add_argument("--scenarios", default=None, metavar="DIR",
                    help="validate the scenario card suite under DIR, read-only")
    ap.add_argument("--name", default=None, help="run label for the registry row")
    ap.add_argument("--no-register", action="store_true",
                    help="skip the registry append (for hook payload checks: "
                         "a pre-write gate of in-flight content must not mint "
                         "rows pointing at temp files that die immediately - "
                         "seat_law_gate cause, 2026-09-29)")
    args = ap.parse_args()

    if args.scenarios:
        return run_scenarios(args.scenarios)
    if not args.script:
        ap.error("check requires --script PATH or --scenarios DIR")

    try:
        with open(args.script, encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        # R3-L1 move 1d (2026-10-05): an unreadable script is a hard block
        # (exit 2), not a soft 1. The gate certifies the script's bytes; a
        # script whose bytes cannot be read has no certificate to mint, and
        # exit 1 was a shape no other gate failure uses.
        print(f"GATE ERROR: cannot read script (hard block): {exc}")
        return 2

    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    rows = run_checks(text)
    failed, _ = split_rows(rows)

    # R1 row 6 stop-cert (2026-10-05): a retired/superseded script cannot mint
    # a fresh PASS row. The check still runs and its row still lands; the
    # verdict becomes BLOCKED-STOPCERT and the exit is the hard block.
    stops = load_stopcert_index()
    stopcert = stop_cert_reason(args.script, digest, stops)
    verdict = "PASS" if not failed else "FAIL"
    if stopcert and verdict == "PASS":
        verdict = "BLOCKED-STOPCERT"
    print(f"workflow_gate {verdict} digest={digest} script={args.script}")
    for r in rows:
        if r.get("soft"):
            print("  WARN  " + f"{r['id']}: {r['desc']} [{r['reason']}]")
        else:
            print(("  ok    " if r["ok"] else "  FAIL  ") + f"{r['id']}: {r['desc']}")
    if stopcert:
        print("  STOPCERT  " + stopcert)

    if args.no_register:
        return 2 if (failed or stopcert) else 0

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = {
        "ts": ts,
        "name": args.name or os.path.basename(args.script),
        "digest": digest,
        "script": args.script,
        "verdict": verdict,
        "checks": rows,
    }
    if stopcert:
        row["stopcert"] = stopcert
    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    with open(REGISTRY, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # R1 row 7 fire ledger (2026-10-05): every single-script check appends one
    # row joining script identity to declared width, so the workflow journal's
    # width-less fire payloads become joinable to the gate's own instrument.
    # Append-only, single writer (this script); skipped in scenario mode
    # (read-only LAW-12 contract) and under --no-register (temp-file rows).
    # R3-L1 move 1e (2026-10-05): fired_args.width joins the max_concurrency
    # stamp at row top level (fired_width + width_discrepancy), because the
    # ledger's own row 1 read stamp 3 beside fired_args.width "50" and the
    # contradiction was invisible until the R3 fold eyeballed the nested args.
    # max_concurrency stays the stamp parse; fired_width is the arg surface;
    # the discrepancy flag is the per-row join.
    fired_args = parse_declared_args(text)
    fired_width = None
    for key in G8_WIDTH_ARG_KEYS:
        val = fired_args.get(key)
        if isinstance(val, str) and val.strip().isdigit():
            fired_width = int(val.strip())
            break
    mc_stamp = max_declared_width(text)
    fire_row = {
        "ts": ts,
        "script": args.script,
        "verdict": verdict,
        "digest": digest,
        "fired_args": fired_args,
        "max_concurrency": mc_stamp,
        "fired_width": fired_width,
        "width_discrepancy": (
            fired_width is not None and mc_stamp is not None
            and fired_width != mc_stamp
        ),
    }
    os.makedirs(os.path.dirname(FIRE_LEDGER), exist_ok=True)
    with open(FIRE_LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(fire_row, ensure_ascii=False) + "\n")

    if failed or stopcert:
        if stopcert:
            print("GATE: stop-cert: this script's registry status bars a fresh certificate; retire the pen or restore the status row by named operator action, never a silent re-cert.")
        if failed:
            print("GATE: fix the FAIL items by editing the script file in place (amend-not-rewrite), then re-check.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
