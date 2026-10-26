"""THE CROWN COURT: AGENTS.md load-order row 0a as a gate, not a suggestion.

G1 lane i04-canon-build; gene: memory/runs/genetic_burn/20261018/G0/lanes/
g02-crown-court.md (+ G0/GENOME.md F2). Built per that design; this pour does
NOT wire into mag/rib_boot.py main() and does NOT touch any state/*.md file
(retrofit stamps are a later pour).

THE LIVE BUG THIS CATCHES (F2, live true at gene time 2026-10-18): row 0a says
the crown is the newest state/*.md by mtime with machinery pages excluded, but
the exclusion list was PROSE enforced socially. On 2026-10-06 LIVE_REPORT.md
(a machine-regenerated page) outranked the authored window doc by mtime and was
crowned by naive mtime reading; the adjudication that fixed it lives only in
AGENTS.md prose. Same moment: the crowned doc (state/SOAK_BEACON_20261016.md,
10-16) is older than the newest law rib (memory/rib/RIB_BOB_PRIMARY_20261017.md,
10-17) and the two contradict on hermes tiering. No gate existed to notice.
This module makes the row-0a adjudication mechanical:

- FRONTMATTER: every state doc may declare itself in a canon block (the first
  lines of the file, `canon-key: value` per line, ended by the first blank line
  or the first non-canon line). No YAML dependency; the parser is small and
  frozen under selftest vectors.
- CROWN RULE: the crown is the newest state/*.md by mtime whose resolved class
  is authored. Machinery pages can never crown, mechanically.
- MISSING BLOCK: a doc without a canon block defaults per the row-0a prose
  rule: the three pages AGENTS.md names as automation-regenerated
  (LIVE_REPORT.md, REDBOARD.md, START_BRIEF.md) resolve machinery; everything
  else resolves authored WITH A PRINTED ASSUMPTION WITNESS (migration debt,
  reported every election until stamped; grandfather clause per the gene).
- E-CHECKS (SystemExit, fail-loud class of mag/rib_boot.py:205-211):
    E1  no state/canon_beacon.json on a non-init run (a boot without an
        election record is a blind boot; mint with --init once).
    E2  zero authored state docs (row 0a cannot crown; the estate has no
        position).
    E3  the elected crown's live-read class is machinery (defensive invariant;
        also the guard a future selection bug hits first).
    E4  the crowned doc is older than the newest memory/rib/*.md law rib and
        carries no ADDENDUM ack naming that rib (amend-never-rewrite cure:
        append an ADDENDUM section naming the rib read, or crown a fresher
        doc), OR the crown asserts a canon-claims id that is contradicted or
        dangling in the claims ledger (watch/claims.jsonl, falling back to the
        dormant logs/claims.jsonl; an absent ledger leaves the contradiction
        leg unchecked with a printed witness, never a fake pass).
- E5 (WARN ONLY this pour): crown age over the freshness bound, min(global
  72h default, the doc's canon-fresh-until). Warn-then-flip is the t40
  precedent; flipping to enforce is an operator call.
- E7 (never an exit): drift witness. The on-disk beacon is the PREVIOUS vote;
  boot always re-elects live and prints any movement.

BEACON (state/canon_beacon.json, schema cano... "canon_beacon.v1"): a RECORD
of the election, not the election. --check writes it only after E1-E4 pass.
--init MINTS it even when E4 fires (writes first, then exits nonzero): the
first election on a diseased tree must still leave its record, and today's
live tree IS diseased (E4 true) - one --init run therefore both produces the
beacon and proves the gate. crown.why and writer are MANDATORY free text from
the caller (never auto-generated boilerplate; the beacon is a loud vote, not
another unattributable machine page).

GRAMMAR-FREEZE LAW (tools/census_drift_patrol.py:97-119 ownership pattern):
the frontmatter grammar is owned by CANON_KEY_RE plus this docstring; the
frozen regression vectors live in selftest() below and are NEVER auto-synced
to live state pages, because a frozen vector is the only witness that catches
a rule reword. Update a vector only with a named receipt.

USAGE
    python -m mag.canon_boot --selftest
    python -m mag.canon_boot --init --writer <seat-id> --why "<one line>"
    python -m mag.canon_boot --check --writer <seat-id> --why "<one line>"
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import tempfile
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
BEACON = STATE / "canon_beacon.json"
VAULT = ROOT / "memory" / "rib"
CLAIMS_PRIMARY_REL = "watch/claims.jsonl"          # Organ 1 primary (i01 pour)
CLAIMS_FALLBACK_REL = "logs/claims.jsonl"          # dormant work_register ledger
SCHEMA = "canon_beacon.v1"
DEFAULT_BOUND_HOURS = 72

# The row-0a prose machinery set: the pages AGENTS.md row 0a (2026-10-06
# ADJUDICATION) names as automation-regenerated and never-crown. Carried as
# basenames so a rename fails loud here instead of silently re-crowning a
# machine page. Extending this list is a spec change with a receipt, never a
# quiet tolerance.
PROSE_MACHINERY = ("LIVE_REPORT.md", "REDBOARD.md", "START_BRIEF.md")

# Ledger row statuses that count as a contradicted registered claim (E4 leg 2).
# The dormant logs/claims.jsonl rows carry claim.status like "Unproven";
# only an explicit negative verdict contradicts - absence of proof is not
# contradiction, the same asymmetry the census patrol draws between STALE
# and CANNOT-VERIFY.
CONTRADICTED_STATUSES = {"contradicted", "contradicts", "falsified", "refuted",
                         "dead", "invalid", "false"}

CANON_KEY_RE = re.compile(r"^canon-([a-z][a-z0-9-]*)\s*:\s*(.*?)\s*$")
ADDENDUM_RE = re.compile(r"(?im)^(?:#{1,6}\s*)?ADDENDUM\b")
INLINE_COMMENT_RE = re.compile(r"\s+#.*$")


def parse_canon_frontmatter(text: str) -> dict:
    """Parse the canon block: the first lines of the file, `canon-key: value`
    per line, ended by the first blank line or the first non-canon line.
    Unknown canon- keys are ignored; key order is free. A block that never
    starts (first line is prose) returns present=False - the caller applies
    the row-0a prose default and prints the assumption witness."""
    meta = {"present": False, "class": None, "writer": None, "claims": [],
            "supersedes": [], "fresh_until": None}
    for line in text.splitlines():
        if not line.strip():
            if meta["present"]:
                break          # first blank line ends the block
            return meta        # block never started
        m = CANON_KEY_RE.match(line)
        if not m:
            if meta["present"]:
                break          # a non-canon line ends the block
            return meta        # prose-first doc: no canon block
        meta["present"] = True
        key, val = m.group(1), INLINE_COMMENT_RE.sub("", m.group(2)).strip()
        if key == "class":
            meta["class"] = val or None
        elif key == "writer":
            meta["writer"] = val or None
        elif key == "claims":
            meta["claims"] = [c.strip() for c in val.split(",") if c.strip()]
        elif key == "supersedes":
            meta["supersedes"] = [s.strip() for s in val.split(",") if s.strip()]
        elif key == "fresh-until":
            meta["fresh_until"] = val or None
        # unknown canon- keys ignored by design (forward compatibility)
    return meta


def resolve_doc_class(name: str, meta: dict) -> tuple[str, str | None]:
    """The row-0a prose default for unstamped docs, with its witness.
    Returns (doc_class, witness); witness is None for a stamped doc."""
    if meta["class"]:
        return meta["class"], None
    if name in PROSE_MACHINERY:
        return "machinery", ("unstamped: excluded by the row-0a prose rule "
                             "(AGENTS.md 2026-10-06 adjudication); retrofit "
                             "canon-class: machinery stamp owed")
    return "authored", ("unstamped: defaulted authored per the row-0a prose "
                        "rule (not in the named-machinery set); retrofit "
                        "canon block owed - an unstamped machinery page that "
                        "wins an election is the LIVE_REPORT 2026-10-06 bug "
                        "class")


def _entry(p: Path, state_dir: Path) -> dict:
    st = p.stat()
    mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
    meta = parse_canon_frontmatter(p.read_text(encoding="utf-8-sig",
                                               errors="replace"))
    cls, witness = resolve_doc_class(p.name, meta)
    return {"path": p.relative_to(state_dir.parent).as_posix(),
            "mtime_utc": mtime, "mtime_dt": mtime, "doc_class": cls,
            "excluded": cls != "authored",
            "excluded_by": (f"frontmatter canon-class: {cls}"
                            if meta["class"] and cls != "authored" else
                            ("row-0a prose rule" if cls != "authored" else None)),
            "witness": witness, "meta": meta, "_p": p}


def elect(state_dir: Path) -> dict:
    """Re-elect the crown LIVE from state_dir. Returns crown entry + full
    trace (every doc, excluded + why). The trace is the row-0a adjudication
    made replayable: any later auditor can re-run the rule against it."""
    entries = [_entry(p, state_dir) for p in sorted(state_dir.glob("*.md"))]
    authored = [e for e in entries if not e["excluded"]]
    crown = max(authored, key=lambda e: e["mtime_dt"]) if authored else None
    return {"crown": crown, "trace": entries, "authored_count": len(authored)}


def _clean_trace(trace: list[dict]) -> list[dict]:
    out = []
    for e in trace:
        row = {"path": e["path"],
               "mtime_utc": e["mtime_utc"].isoformat(),
               "doc_class": e["doc_class"],
               "excluded": e["excluded"]}
        if e["excluded_by"]:
            row["excluded_by"] = e["excluded_by"]
        if e["witness"]:
            row["witness"] = e["witness"]
        out.append(row)
    return out


def has_ack_after(crown_text: str, rib_stem: str) -> bool:
    """The amend-never-rewrite cure for an older-than-law crown: an ADDENDUM
    section appended to the crown naming the newer rib it has read. The ack
    is content, not mtime - touching mtime alone cannot fake having read
    law (gene design section 3, anti-gaming)."""
    starts = [m.start() for m in ADDENDUM_RE.finditer(crown_text)]
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(crown_text)
        if rib_stem in crown_text[start:end]:
            return True
    return False


def _load_claims_ledger(root: Path) -> tuple[dict, str | None]:
    """id -> row, from watch/claims.jsonl (Organ 1 primary) falling back to
    the dormant logs/claims.jsonl. Row id = the row's id / claim_id / label
    field, whichever it carries. Paths resolve under the INJECTED root, never
    the module constants, so a selftest tree is hermetic even after the real
    ledger lands. Returns (map, ledger_rel_path_or_None)."""
    for rel in (CLAIMS_PRIMARY_REL, CLAIMS_FALLBACK_REL):
        p = root / rel
        if not p.is_file():
            continue
        rows: dict[str, dict] = {}
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            rid = row.get("id") or row.get("claim_id") or row.get("label")
            if rid:
                rows[str(rid)] = row
        return rows, rel
    return {}, None


def _row_status(row: dict) -> str:
    c = row.get("claim") if isinstance(row.get("claim"), dict) else {}
    return str(row.get("status") or c.get("status") or "").strip().lower()


def check_claims(root: Path, claim_ids: list[str]) -> tuple[list[dict], list[str], list[str]]:
    """E4 leg 2: re-verify every canon-claims id the crown asserts against the
    claims ledger. Returns (claims_checked rows, violation messages, witness
    notes). An absent LEDGER is a witness note (UNCHECKED, printed loud, never
    a fake pass and never a boot-killer on a sibling organ's not-yet-landed
    file); a dangling id or a contradicted status is a violation."""
    checked: list[dict] = []
    violations: list[str] = []
    notes: list[str] = []
    if not claim_ids:
        return checked, violations, notes
    rows, ledger = _load_claims_ledger(root)
    if ledger is None:
        for cid in claim_ids:
            checked.append({"id": cid, "status": "unchecked_ledger_absent",
                            "ledger": None})
        notes.append(
            "E4-WITNESS: crown asserts claims "
            f"({', '.join(claim_ids)}) but no claims ledger exists "
            f"({CLAIMS_PRIMARY_REL} primary, {CLAIMS_FALLBACK_REL} fallback) "
            "- contradiction leg UNCHECKED, not passed")
        return checked, violations, notes
    for cid in claim_ids:
        row = rows.get(cid)
        if row is None:
            violations.append(
                f"CROWN-COURT E4: crown asserts claim id '{cid}' and no such "
                f"row is registered in {ledger} - a dangling claim is a blind "
                "claim; register it or drop it from the crown's canon-claims")
            checked.append({"id": cid, "status": "dangling", "ledger": ledger})
            continue
        status = _row_status(row)
        checked.append({"id": cid, "status": status or "unknown",
                        "ledger": ledger})
        if status in CONTRADICTED_STATUSES:
            violations.append(
                f"CROWN-COURT E4: crown asserts claim id '{cid}' whose "
                f"registered status is '{status}' in {ledger} - the crown "
                "contradicts a registered claim; refresh the crown or the "
                "claim")
    return checked, violations, notes


def _freshness(crown_meta: dict, crown_mtime: datetime, now: datetime) -> tuple[dict, str | None]:
    """E5 inputs: bound = min(global default, the doc's canon-fresh-until)."""
    bound = float(DEFAULT_BOUND_HOURS)
    note = None
    if crown_meta.get("fresh_until"):
        try:
            fu = datetime.fromisoformat(crown_meta["fresh_until"]).replace(tzinfo=timezone.utc)
            doc_bound = max(0.0, (fu - crown_mtime).total_seconds() / 3600.0)
            bound = min(bound, doc_bound)
        except ValueError:
            note = (f"canon-fresh-until '{crown_meta['fresh_until']}' "
                    "unparseable - global bound applies")
    age = max(0.0, (now - crown_mtime).total_seconds() / 3600.0)
    return {"bound_hours": round(bound, 2),
            "doc_bound_utc": (crown_mtime + timedelta(hours=bound)).isoformat(),
            "age_hours_at_write": round(age, 2)}, note


def guard_e3(crown: dict) -> None:
    """E3 defensive invariant: the elected crown's live-read class must be
    authored. Unreachable through elect() by construction; kept as a named
    guard so a future selection change hits a loud wall, not a silent crown."""
    if crown["doc_class"] != "authored":
        raise SystemExit(f"CROWN-COURT E3: machinery page crowned: "
                         f"{crown['path']} - a regenerated page either never "
                         "stamped itself or the stamp lied (the LIVE_REPORT "
                         "2026-10-06 bug class)")


def run_check(root: Path = ROOT, *, writer: str | None, why: str | None,
              init: bool = False, now: datetime | None = None) -> dict:
    """The full boot check: re-elect live, apply E1-E4 (SystemExit), warn on
    E5, print the E7 drift witness, write the beacon. --init records the
    beacon even when E4 fires (then still exits loud); --check writes only
    after every structural check passes."""
    now = now or datetime.now(timezone.utc)
    if not writer or not writer.strip() or not why or not why.strip():
        raise SystemExit("CROWN-COURT INPUT: --writer and --why are mandatory "
                         "(the beacon is a loud vote; an unattributable or "
                         "boilerplate why is another machine page)")
    state_dir = root / "state"
    beacon_path = state_dir / "canon_beacon.json"

    # E1. The beacon must exist: a never-elected estate is the 10-06 bug class.
    if not init and not beacon_path.is_file():
        raise SystemExit("CROWN-COURT E1: no state/canon_beacon.json - mint "
                         "with python -m mag.canon_boot --init (a boot "
                         "without an election record is a blind boot)")

    el = elect(state_dir)
    for e in el["trace"]:
        if e["witness"]:
            print(f"CROWN-COURT ASSUMPTION: {e['path']}: {e['witness']}")
    crown = el["crown"]
    if crown is None:
        raise SystemExit("CROWN-COURT E2: zero authored state docs - row 0a "
                         "cannot crown; the estate has no position")
    guard_e3(crown)

    # law anchor: newest memory/rib/*.md
    vault = root / "memory" / "rib"
    ribs = sorted(vault.glob("*.md")) if vault.is_dir() else []
    if not ribs:
        raise SystemExit("CROWN-COURT E4: cannot verify - law vault "
                         "memory/rib carries no *.md ribs; an election "
                         "without law to anchor against is unverifiable")
    newest_rib = max(ribs, key=lambda p: datetime.fromtimestamp(
        p.stat().st_mtime, tz=timezone.utc))
    rib_mtime = datetime.fromtimestamp(newest_rib.stat().st_mtime,
                                       tz=timezone.utc)
    rib_stem = newest_rib.stem
    crown_newer = crown["mtime_dt"] >= rib_mtime
    ack = False
    violations: list[str] = []
    if not crown_newer:
        crown_text = crown["_p"].read_text(encoding="utf-8-sig",
                                           errors="replace")
        ack = has_ack_after(crown_text, rib_stem)
        if not ack:
            violations.append(
                f"CROWN-COURT E4: crown {crown['path']} "
                f"({crown['mtime_utc'].isoformat()}) is older than newest law "
                f"rib memory/rib/{newest_rib.name} ({rib_mtime.isoformat()}) "
                "- a crown older than law is a crown blind to law; append an "
                "ADDENDUM naming the rib read, or crown a fresher doc "
                "(amend-never-rewrite)")

    claims_checked, claim_violations, claim_notes = check_claims(
        root, crown["meta"]["claims"])
    for note in claim_notes:
        print(f"CROWN-COURT {note}")
    violations.extend(claim_violations)

    fresh, fresh_note = _freshness(crown["meta"], crown["mtime_dt"], now)
    sha = hashlib.sha256(crown["_p"].read_bytes()).hexdigest()
    beacon = {
        "schema": SCHEMA,
        "moment_utc": now.isoformat(),
        "writer": writer.strip(),
        "crown": {
            "path": crown["path"],
            "sha256": sha,
            "mtime_utc": crown["mtime_utc"].isoformat(),
            "doc_class": crown["doc_class"],
            "elected_by": "newest-authored-after-frontmatter-and-row0a-prose-exclusions",
            "why": why.strip(),
        },
        "election_trace": _clean_trace(el["trace"]),
        "freshness": fresh,
        "law_anchor": {
            "newest_rib": f"memory/rib/{newest_rib.name}",
            "newest_rib_mtime_utc": rib_mtime.isoformat(),
            "crown_newer_than_law": bool(crown_newer),
            "ack_found": bool(ack),
        },
        "claims_checked": claims_checked,
    }

    # E7 drift witness: the on-disk beacon is the previous vote.
    if beacon_path.is_file():
        try:
            prior = json.loads(beacon_path.read_text(encoding="utf-8"))
            prior_path = (prior.get("crown") or {}).get("path")
            if prior_path and prior_path != crown["path"]:
                print(f"CROWN-COURT E7-WARN: election moved "
                      f"{prior_path} -> {crown['path']}")
        except (ValueError, AttributeError):
            print("CROWN-COURT E7-WARN: existing beacon unreadable; "
                  "rewriting from the live election")

    if violations:
        if init:
            beacon_path.write_text(
                json.dumps(beacon, indent=1, ensure_ascii=False) + "\n",
                encoding="utf-8")
            print("CROWN-COURT: --init recorded the failed election in the "
                  "beacon before exiting (the beacon is a record, not a "
                  "verdict)")
        raise SystemExit("\n".join(violations))

    # E5: WARN ONLY this pour (t40 precedent; flip-to-enforce is an operator
    # call). Recorded in the beacon either way.
    if fresh_note:
        print(f"CROWN-COURT E5-NOTE: {fresh_note}")
    if fresh["age_hours_at_write"] > fresh["bound_hours"]:
        print(f"CROWN-COURT E5-WARN: crown "
              f"{fresh['age_hours_at_write']:.0f}h old, bound "
              f"{fresh['bound_hours']:.0f}h (warn-only this pour)")

    beacon_path.write_text(
        json.dumps(beacon, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    excluded = sum(1 for e in el["trace"] if e["excluded"])
    print(f"CROWN-COURT: crown={crown['path']} "
          f"sha256={sha[:16]}... authored={el['authored_count']} "
          f"excluded={excluded} law=memory/rib/{newest_rib.name} "
          f"crown_newer_than_law={crown_newer}")
    print(f"CROWN-COURT: why={beacon['crown']['why']}")
    print(f"CROWN-COURT: beacon -> {beacon_path.relative_to(root).as_posix()}")
    return beacon


# ---------------------------------------------------------------- selftest --
# FROZEN VECTORS (grammar-freeze law): these strings are the pinned grammar,
# never auto-synced to live state pages. Update only with a named receipt.

V_AUTHORED = (
    "canon-class: authored\n"
    "canon-writer: zcode-seat-vector\n"
    "canon-claims: hermes.tiering, soak.position\n"
    "canon-supersedes: state/NIGHT_LOOP_20261005.md\n"
    "canon-fresh-until: 2026-10-19\n"
    "\n"
    "# SOAK BEACON-style authored doc\n"
    "\nbody\n"
)
V_MACHINERY = ("canon-class: machinery\ncanon-writer: governor_autorun\n"
               "\n# regenerated page\n\nbody\n")
V_PROSE_ONLY = "# a plain legacy doc\n\nprose body, no canon block\n"
V_UNKNOWN_KEYS = ("canon-class: authored\ncanon-unknown-future-key: x\n"
                  "canon-writer: w\n\nbody\n")
V_COMMENT = ("canon-class: authored  # stamped by hand\n"
             "canon-fresh-until: 2026-10-19\n\nbody\n")
V_AFTER_BLANK = ("canon-class: authored\n\nsome prose\ncanon-class: machinery\n")
V_MALFORMED_DATE = ("canon-class: authored\ncanon-fresh-until: not-a-date\n"
                    "\nbody\n")
V_ACK = ("canon-class: authored\n\n# crown\n\n## ADDENDUM 2026-10-17\n\n"
         "Read memory/rib/RIB_BOB_PRIMARY_20261017.md; position stands.\n")
V_CLAIMS_CROWN = ("canon-class: authored\ncanon-claims: hermes.tiering\n"
                  "\nbody\n")


class _Tree:
    """A throwaway estate: temp root with state/ and memory/rib/, files with
    pinned mtimes. Selftest only; never touches the live tree."""

    def __init__(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="canon_boot_selftest_"))
        (self.root / "state").mkdir()
        (self.root / "memory" / "rib").mkdir(parents=True)

    def doc(self, name: str, text: str, mtime: datetime) -> Path:
        p = self.root / "state" / name
        p.write_text(text, encoding="utf-8")
        os.utime(p, (mtime.timestamp(), mtime.timestamp()))
        return p

    def rib(self, name: str, mtime: datetime) -> Path:
        p = self.root / "memory" / "rib" / name
        p.write_text("# law rib\n", encoding="utf-8")
        os.utime(p, (mtime.timestamp(), mtime.timestamp()))
        return p

    def ledger(self, rel: str, rows: list[dict]) -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(json.dumps(r) + "\n" for r in rows),
                     encoding="utf-8")

    def cleanup(self) -> None:
        import shutil
        shutil.rmtree(self.root, ignore_errors=True)


def _expect_exit(fn, *needle: str) -> str:
    try:
        fn()
    except SystemExit as e:
        msg = str(e)
        for n in needle:
            if n not in msg:
                raise AssertionError(f"exit message missing {n!r}: {msg}")
        return msg
    raise AssertionError(f"expected SystemExit mentioning {needle}, got none")


def selftest() -> int:
    """Frozen vectors: parser grammar, election rule, E1-E4, beacon schema.
    Exit 0 only if every vector passes."""
    vectors: list[tuple[str, callable]] = []
    vec = vectors.append

    # ---- parser grammar (frozen) ----
    def p_authored():
        m = parse_canon_frontmatter(V_AUTHORED)
        assert m["present"] and m["class"] == "authored"
        assert m["writer"] == "zcode-seat-vector"
        assert m["claims"] == ["hermes.tiering", "soak.position"]
        assert m["supersedes"] == ["state/NIGHT_LOOP_20261005.md"]
        assert m["fresh_until"] == "2026-10-19"
    vec(("parser: authored block, all five keys", p_authored))

    def p_machinery():
        m = parse_canon_frontmatter(V_MACHINERY)
        assert m["present"] and m["class"] == "machinery"
    vec(("parser: machinery block", p_machinery))

    def p_missing():
        m = parse_canon_frontmatter(V_PROSE_ONLY)
        assert not m["present"] and m["class"] is None
    vec(("parser: missing block (prose-first doc)", p_missing))

    def p_unknown():
        m = parse_canon_frontmatter(V_UNKNOWN_KEYS)
        assert m["present"] and m["class"] == "authored"
    vec(("parser: unknown canon- keys ignored", p_unknown))

    def p_comment():
        m = parse_canon_frontmatter(V_COMMENT)
        assert m["class"] == "authored" and m["fresh_until"] == "2026-10-19"
    vec(("parser: inline comment stripped", p_comment))

    def p_after_blank():
        m = parse_canon_frontmatter(V_AFTER_BLANK)
        assert m["present"] and m["class"] == "authored"
    vec(("parser: post-blank poison ignored (block ends at blank)", p_after_blank))

    def p_prose_default():
        cls, w = resolve_doc_class("SOME_WINDOW.md",
                                   parse_canon_frontmatter(V_PROSE_ONLY))
        assert cls == "authored" and w and "defaulted authored" in w
        cls2, w2 = resolve_doc_class("LIVE_REPORT.md",
                                     parse_canon_frontmatter(V_PROSE_ONLY))
        assert cls2 == "machinery" and w2 and "prose rule" in w2
    vec(("default: unstamped doc -> authored witness; LIVE_REPORT -> machinery",
         p_prose_default))

    # ---- election rule ----
    def election():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("a_machinery.md", V_MACHINERY, base + timedelta(hours=3))
            t.doc("b_authored.md", V_AUTHORED, base + timedelta(hours=1))
            t.doc("c_plain.md", V_PROSE_ONLY, base)
            t.doc("LIVE_REPORT.md", V_PROSE_ONLY, base + timedelta(hours=2))
            el = elect(t.root / "state")
            assert el["crown"]["path"].endswith("b_authored.md"), el["crown"]
            assert el["authored_count"] == 2
            assert len(el["trace"]) == 4
            by = {e["path"].split("/")[-1]: e for e in el["trace"]}
            assert by["a_machinery.md"]["excluded"] is True
            assert "frontmatter" in by["a_machinery.md"]["excluded_by"]
            assert by["LIVE_REPORT.md"]["excluded"] is True
            assert "prose rule" in by["LIVE_REPORT.md"]["excluded_by"]
            assert by["c_plain.md"]["excluded"] is False
            assert by["c_plain.md"]["witness"]
        finally:
            t.cleanup()
    vec(("election: machinery newest excluded, authored middle crowns, "
         "trace covers all four", election))

    def election_default_authored_wins():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("REDBOARD.md", V_PROSE_ONLY, base + timedelta(hours=5))
            t.doc("plain_window.md", V_PROSE_ONLY, base + timedelta(hours=1))
            el = elect(t.root / "state")
            assert el["crown"]["path"].endswith("plain_window.md")
            assert el["authored_count"] == 1
        finally:
            t.cleanup()
    vec(("election: unstamped REDBOARD excluded by prose rule while unstamped "
         "plain doc defaults authored and crowns", election_default_authored_wins))

    # ---- E2 ----
    def e2():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("a.md", V_MACHINERY, base)
            t.doc("REDBOARD.md", V_PROSE_ONLY, base + timedelta(hours=1))
            t.rib("RIB_X.md", base)
            msg = _expect_exit(lambda: run_check(
                t.root, writer="vec", why="vec", init=True, now=base))
            assert "E2" in msg
        finally:
            t.cleanup()
    vec(("E2: zero authored docs exits", e2))

    # ---- E3 guard ----
    def e3():
        base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
        bad = {"path": "state/a.md", "doc_class": "machinery",
               "mtime_dt": base, "mtime_utc": base}
        msg = _expect_exit(lambda: guard_e3(bad), "E3")
        assert "machinery" in msg
    vec(("E3: machinery-crown guard exits", e3))

    # ---- E1 + init mint ----
    def e1():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_AUTHORED, base)
            t.rib("RIB_X.md", base - timedelta(hours=1))
            msg = _expect_exit(lambda: run_check(
                t.root, writer="vec", why="vec", init=False, now=base), "E1")
            assert "canon_beacon.json" in msg
            b = run_check(t.root, writer="vec", why="first vote",
                          init=True, now=base)
            assert (t.root / "state" / "canon_beacon.json").is_file()
            assert b["schema"] == SCHEMA
        finally:
            t.cleanup()
    vec(("E1: absent beacon exits on --check; --init mints it", e1))

    # ---- E4 leg 1: crown older than newest law rib ----
    def e4_older():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_AUTHORED, base - timedelta(hours=30))
            t.rib("RIB_BOB_PRIMARY_20261017.md", base - timedelta(hours=1))
            msg = _expect_exit(lambda: run_check(
                t.root, writer="vec", why="vec", init=True, now=base), "E4",
                "older than newest law rib")
            beacon = json.loads((t.root / "state" / "canon_beacon.json")
                                .read_text(encoding="utf-8"))
            assert beacon["law_anchor"]["crown_newer_than_law"] is False
        finally:
            t.cleanup()
    vec(("E4: crown older than newest rib exits; --init still records the "
         "beacon with crown_newer_than_law false", e4_older))

    def e4_ack_cures():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_ACK, base - timedelta(hours=30))
            t.rib("RIB_BOB_PRIMARY_20261017.md", base - timedelta(hours=1))
            b = run_check(t.root, writer="vec", why="vec", init=True, now=base)
            assert b["law_anchor"]["ack_found"] is True
            assert b["law_anchor"]["crown_newer_than_law"] is False
        finally:
            t.cleanup()
    vec(("E4: an ADDENDUM naming the rib is the honest cure and passes",
         e4_ack_cures))

    def e4_crown_newer():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_AUTHORED, base)
            t.rib("RIB_X.md", base - timedelta(hours=2))
            b = run_check(t.root, writer="vec", why="vec", init=True, now=base)
            assert b["law_anchor"]["crown_newer_than_law"] is True
        finally:
            t.cleanup()
    vec(("E4: crown at least as new as law passes", e4_crown_newer))

    # ---- E4 leg 2: registered-claim contradiction / dangling / no ledger ----
    def e4_contradicted():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_CLAIMS_CROWN, base)
            t.rib("RIB_X.md", base - timedelta(hours=2))
            t.ledger("watch/claims.jsonl", [
                {"id": "hermes.tiering", "status": "CONTRADICTED"}])
            msg = _expect_exit(lambda: run_check(
                t.root, writer="vec", why="vec", init=True, now=base), "E4",
                "contradicts a registered claim")
        finally:
            t.cleanup()
    vec(("E4: crown claim contradicted in the ledger exits", e4_contradicted))

    def e4_dangling():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_CLAIMS_CROWN, base)
            t.rib("RIB_X.md", base - timedelta(hours=2))
            t.ledger("watch/claims.jsonl", [{"id": "other.claim"}])
            msg = _expect_exit(lambda: run_check(
                t.root, writer="vec", why="vec", init=True, now=base), "E4",
                "dangling")
        finally:
            t.cleanup()
    vec(("E4: dangling claim id exits", e4_dangling))

    def e4_ledger_absent_witness():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_CLAIMS_CROWN, base)
            t.rib("RIB_X.md", base - timedelta(hours=2))
            out = io.StringIO()
            with redirect_stdout(out):
                b = run_check(t.root, writer="vec", why="vec", init=True,
                              now=base)
            assert "UNCHECKED" in out.getvalue()
            assert b["claims_checked"][0]["status"] == "unchecked_ledger_absent"
        finally:
            t.cleanup()
    vec(("E4: absent ledger leaves the contradiction leg UNCHECKED with a "
         "witness, never a fake pass", e4_ledger_absent_witness))

    def e4_ledger_verified_passes():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_CLAIMS_CROWN, base)
            t.rib("RIB_X.md", base - timedelta(hours=2))
            t.ledger("logs/claims.jsonl", [
                {"ts": "2026-09-06T00:00:00Z", "kind": "panel",
                 "label": "hermes.tiering",
                 "claim": {"statement": "s", "status": "Unproven"}}])
            out = io.StringIO()
            with redirect_stdout(out):
                b = run_check(t.root, writer="vec", why="vec", init=True,
                              now=base)
            assert b["claims_checked"][0]["status"] == "unproven"
        finally:
            t.cleanup()
    vec(("E4: fallback ledger logs/claims.jsonl row verifies clean "
         "(Unproven is not contradiction)", e4_ledger_verified_passes))

    # ---- beacon schema ----
    def beacon_schema():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            p = t.doc("win.md", V_AUTHORED, base)
            t.rib("RIB_X.md", base - timedelta(hours=2))
            b = run_check(t.root, writer="vec:lane", why="the founding vote",
                          init=True, now=base)
            for key in ("schema", "moment_utc", "writer", "crown",
                        "election_trace", "freshness", "law_anchor",
                        "claims_checked"):
                assert key in b, key
            c = b["crown"]
            assert c["path"] == "state/win.md" and c["doc_class"] == "authored"
            assert c["why"] == "the founding vote"
            assert b["writer"] == "vec:lane"
            assert c["sha256"] == hashlib.sha256(p.read_bytes()).hexdigest()
            assert b["election_trace"][0]["path"].startswith("state/")
            assert b["freshness"]["bound_hours"] <= DEFAULT_BOUND_HOURS
        finally:
            t.cleanup()
    vec(("beacon: schema v1 fields, sha256 binds the crowned bytes, why "
         "rides verbatim", beacon_schema))

    # ---- E5 warn-only + malformed fresh-until ----
    def e5_warn_only():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_AUTHORED, base - timedelta(hours=100))
            t.rib("RIB_X.md", base - timedelta(hours=101))
            out = io.StringIO()
            with redirect_stdout(out):
                b = run_check(t.root, writer="vec", why="vec", init=True,
                              now=base)
            assert "E5-WARN" in out.getvalue()
            assert b["freshness"]["age_hours_at_write"] > 72.0
        finally:
            t.cleanup()
    vec(("E5: over-bound age warns and still writes (warn-only pour)", e5_warn_only))

    def e5_malformed_date():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_MALFORMED_DATE, base)
            t.rib("RIB_X.md", base - timedelta(hours=2))
            out = io.StringIO()
            with redirect_stdout(out):
                b = run_check(t.root, writer="vec", why="vec", init=True,
                              now=base)
            assert "E5-NOTE" in out.getvalue()
            assert b["freshness"]["bound_hours"] == float(DEFAULT_BOUND_HOURS)
        finally:
            t.cleanup()
    vec(("E5: unparseable canon-fresh-until degrades to the global bound with "
         "a note", e5_malformed_date))

    # ---- input contract ----
    def input_contract():
        t = _Tree()
        try:
            base = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
            t.doc("win.md", V_AUTHORED, base)
            t.rib("RIB_X.md", base - timedelta(hours=2))
            _expect_exit(lambda: run_check(t.root, writer=None, why="x",
                                           init=True, now=base), "INPUT")
            _expect_exit(lambda: run_check(t.root, writer="x", why=None,
                                           init=True, now=base), "INPUT")
        finally:
            t.cleanup()
    vec(("input: writer and why are mandatory free text", input_contract))

    failed = []
    for name, fn in vectors:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            failed.append(name)
            print(f"  FAIL  {name}: {e}")
        except Exception as e:  # noqa: BLE001 - the selftest reports, not hides
            failed.append(name)
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
    print(f"  SELFTEST: {len(vectors) - len(failed)}/{len(vectors)} vectors "
          "pass (frozen grammar; never auto-synced to live pages)")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m mag.canon_boot",
        description="THE CROWN COURT: load-order row 0a as a gate "
                    "(see module docstring; gene g02-crown-court)")
    ap.add_argument("--check", action="store_true",
                    help="re-elect live, apply E1-E4, write the beacon on pass")
    ap.add_argument("--init", action="store_true",
                    help="first election: mint the beacon even if E4 fires, "
                         "then still exit loud")
    ap.add_argument("--selftest", action="store_true",
                    help="run the frozen grammar + check vectors")
    ap.add_argument("--writer", default=None,
                    help="seat/lane id of this vote (mandatory with "
                         "--check/--init)")
    ap.add_argument("--why", default=None,
                    help="one human-auditable line for this vote (mandatory "
                         "with --check/--init)")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.init or a.check:
        run_check(ROOT, writer=a.writer, why=a.why, init=a.init)
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
