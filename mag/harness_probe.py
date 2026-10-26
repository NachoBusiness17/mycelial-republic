"""harness_probe: the Harness2 loop on the leave-protocol mates (2026-10-17).

A minimal, stdlib-only port of Google Research Harness2 (propose -> probe ->
compose -> blinded select -> reflect -> library; report
watch/LIBRARY/STEAL_HARNESS2_20261017.md) onto organs Mag already has. No new
engine: the dispatcher still runs ONE constant argv per mission file
(tools/leave_dispatcher.py); everything below only writes more mission FILES
and, host-side, reads receipts and files Ed25519-signed proposals
(mag/proposals.py). No model is called from here.

OPT-IN: configs/mates.yaml `harness_probe.enabled: true` (default false).

Daily round, staggered across days so one wave needs no intra-wave order:

  day D    editor_inv / editor_dom read yesterday's receipts and each write
           candidate_<D>_<role>.md (a HARNESS DELTA + receipt:line EVIDENCE,
           or KEEP_BASE) under watch/inbox/mates_leave_protocol/harness_probe/
           candidates/.
  day D+1  probe pair: the SAME mate mission twice, base and base+delta, under
           blinded pack ids (mission_<D+1>_<nn>_probe-xxxxxx.md). The label
           map lives host-side in logs/mates/harness_probe/rounds/.
  day D+2  composer reads both blinded receipts and writes a verdict
           (ROUND / CHOICE / ACTION / DIFF / EXPERIENCE with receipt:line
           evidence). At the next dispatch the host unblinds, and only when the
           composer chose the candidate run and cited real receipt lines does
           it file a proposal SIGNED WITH THE COMPOSER'S OWN KEY (mate:composer,
           ~/.mag_seat/mates/mate__composer.key, loaded in process, never shown
           to any model). Mates review by writing `REVIEW: <proposal_id>
           approve|reject <reason>` lines in their receipts; the host signs
           each with THAT mate's own key.
  adoption proposals.tally: quorum 2 distinct seats (author excluded) AND, by
           quorum.require_non_glm_approval (default true), one approval from a
           non-mate, non-GLM seat. Once ready, the host files the promotion and
           appends the lesson to the law rib as a dated
           `## AMENDMENT (YYYY-MM-DD, harness2 lesson <id>)` block, append-only,
           verified byte-prefix-unchanged (rib_boot mounts AMENDMENT sections,
           served at mag://warm/laws).

At k=1 a full day is 8 mates + 2 editors + 2 probes + 1 composer = 13 packs;
the dispatcher keeps its 16 ceiling. Limit (stated, not hidden): blinding is by
label only. Pack B carries the delta text, and the map sits on the same disk.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:  # `python mag/harness_probe.py` as well as -m
    sys.path.insert(0, str(ROOT))

from mag import proposals as P  # noqa: E402
from mag import seat_handshake as sh  # noqa: E402

STATE_DIR = ROOT / "logs" / "mates" / "harness_probe"
WORK_DIR = ROOT / "watch" / "inbox" / "mates_leave_protocol" / "harness_probe"
RECEIPTS_DIR = ROOT / "watch" / "inbox" / "mates_leave_protocol" / "receipts"
RIB_DIR = ROOT / "memory" / "rib"
CONFIG_PATH = ROOT / "configs" / "mates.yaml"
DEFAULT_RIB = "RIB_LIGHT_MAZE_20261012.md"
SCHEMA = "harness_probe.v1"
DELTA_CAP = 3000
BLIND_RE = re.compile(r"^probe-[0-9a-f]{6}$")
CITE_RE = re.compile(r"(receipt_\d{8}_[A-Za-z0-9_.-]+?\.md):(\d+)")
CAND_RE = re.compile(r"^candidate_(\d{8})_([A-Za-z0-9_-]+)\.md$")
VERDICT_RE = re.compile(r"^verdict_(\d{8})_composer\.md$")
RECEIPT_RE = re.compile(r"^receipt_(\d{8})_([A-Za-z0-9_-]+)\.md$")
REVIEW_RE = re.compile(r"(?m)^\s*REVIEW:\s*(p_[0-9]{8}T[0-9]{6}Z_[0-9a-f]{12})\s+(approve|reject)\b[ \t:-]*(.*)$")
EXPERIENCE_KEYS = ("cue", "lesson", "evidence", "confidence")
HARVEST_DAYS = 3

PROBE_NOTE = """
## Probe (harness2)
This is a paired probe run. Work the mission exactly as written above and file
your receipt under THIS pack's id. Do not look for or open any other probe pack.
"""

DELTA_BLOCK = """
## HARNESS DELTA (candidate change under probe)
{delta}
"""

EDITOR_CONTRACT = """
## Harness2 editor contract ({scope})
Read yesterday's receipts (watch/inbox/mates_leave_protocol/receipts/receipt_{prev}_*.md).
{focus}
Write exactly one file:
  watch/inbox/mates_leave_protocol/harness_probe/candidates/candidate_{date}_{role}.md
Format (plain text, no em-dashes):
  SCOPE: {scope}
  TARGET_MATE: <one mate id from configs/mates.yaml, or any>
  DECISION: DELTA | KEEP_BASE
  ## HARNESS DELTA
  <at most {cap} characters of instructions to add to that mate's mission pack>
  ## EVIDENCE
  - receipt_<date>_<mate>.md:<line> <why this line shows the gap>
No receipt:line evidence, no candidate: KEEP_BASE is a full, honest answer.
{reviews}"""

REVIEW_ASK = """
## Pending harness2 proposals (review them)
For each proposal, read watch/receipts/proposals/<id>/proposal.json and add one
line to your receipt FINDINGS, exactly:
  REVIEW: <proposal_id> approve|reject <one-sentence reason citing receipt:line>
The host signs that line with your own seat key. Pending:
{rows}
"""

COMPOSER_CONTRACT = """
## Harness2 composer contract
Judge each probe round below. Each round ran ONE mission twice under two pack
ids; one run had a candidate HARNESS DELTA added. Compare the two receipts on
the mission itself (findings that hold up, honest counts, dead ends named).
Write exactly one file:
  watch/inbox/mates_leave_protocol/harness_probe/verdicts/verdict_{date}_composer.md
with one block per round:
  ROUND: <round id>
  CHOICE: <the better pack id>
  ACTION: adopt | keep_base
  TARGET: <repo-relative file the change belongs in, default configs/mates.yaml>
  ## DIFF
  <optional unified diff that makes the delta permanent>
  ## EXPERIENCE
  cue: <when this applies>
  lesson: <what to do>
  evidence: <receipt_<date>_<id>.md:<line>; at least one line from this round's receipts>
  confidence: low | medium | high
No receipt:line evidence, no lesson. Nothing is adopted without the quorum.
Rounds:
{rounds}"""


# ------------------------------------------------------------------ helpers

def mate_seat(mate_id: str) -> str:
    return f"{sh.MATE_PREFIX}{mate_id}"


def mate_key_path(mate_id: str) -> Path:
    return sh.default_key_path(mate_seat(mate_id))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_new_json(path: Path, obj: dict[str, Any]) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "x", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
        return True
    except FileExistsError:
        return False


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return p.name


def _prev_day(today: str) -> str:
    d = datetime.strptime(today, "%Y%m%d").date()
    return date.fromordinal(d.toordinal() - 1).strftime("%Y%m%d")


def _sections(text: str) -> tuple[dict[str, str], dict[str, str]]:
    """(header KEY: value fields before the first '## ', {SECTION: body})."""
    fields: dict[str, str] = {}
    secs: dict[str, list[str]] = {}
    cur: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip().upper()
            secs.setdefault(cur, [])
        elif cur is None:
            m = re.match(r"^\s*([A-Za-z_]+)\s*:\s*(.*?)\s*$", line)
            if m:
                fields[m.group(1).upper()] = m.group(2)
        else:
            secs[cur].append(line)
    return fields, {k: "\n".join(v).strip() for k, v in secs.items()}


def citations(text: str) -> list[tuple[str, int]]:
    return [(m.group(1), int(m.group(2))) for m in CITE_RE.finditer(text or "")]


def check_citations(cites: list[tuple[str, int]], receipts_dir: Path) -> list[str]:
    """Problems with receipt:line citations (missing file / line past the end)."""
    bad = []
    for name, line in cites:
        p = receipts_dir / name
        if not p.is_file():
            bad.append(f"{name}:{line} (no such receipt)")
            continue
        n = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        if not 1 <= line <= n:
            bad.append(f"{name}:{line} (receipt has {n} lines)")
    return bad


def _paths(state_dir: Path | None, work_dir: Path | None) -> dict[str, Path]:
    s, w = Path(state_dir or STATE_DIR), Path(work_dir or WORK_DIR)
    return {"rounds": s / "rounds", "verdicts": s / "verdicts", "lessons": s / "lessons",
            "reviews": s / "reviews", "cand": w / "candidates", "vfiles": w / "verdicts"}


# ------------------------------------------------------------------ propose

def parse_candidate(text: str, receipts_dir: Path | None = None) -> dict[str, Any]:
    fields, secs = _sections(text)
    decision = fields.get("DECISION", "").strip().upper().replace(" ", "_")
    out: dict[str, Any] = {"scope": fields.get("SCOPE", "").strip().upper(),
                           "target_mate": fields.get("TARGET_MATE", "").strip(),
                           "delta": secs.get("HARNESS DELTA", ""),
                           "evidence": citations(secs.get("EVIDENCE", ""))}
    if decision == "KEEP_BASE":
        return {**out, "status": "keep_base", "reason": "editor kept the base"}
    if decision != "DELTA":
        return {**out, "status": "invalid", "reason": "DECISION must be DELTA or KEEP_BASE"}
    if not out["delta"] or len(out["delta"]) > DELTA_CAP:
        return {**out, "status": "invalid", "reason": f"HARNESS DELTA empty or over {DELTA_CAP} chars"}
    if not out["evidence"]:
        return {**out, "status": "invalid", "reason": "no receipt:line evidence"}
    if P._secret_hits(out["delta"]):
        return {**out, "status": "invalid", "reason": "delta trips the secret scanner"}
    if receipts_dir is not None:
        bad = check_citations(out["evidence"], Path(receipts_dir))
        if bad:
            return {**out, "status": "invalid", "reason": "bad evidence: " + "; ".join(bad)}
    return {**out, "status": "delta", "reason": "ok"}


# ------------------------------------------------------------------ probe

def assign_blind(seed: Any = None) -> dict[str, str]:
    """{pack_id: "base"|"cand"} with two distinct random ids and a shuffled
    label order (harness2 assign_ids shape). seed=None uses the OS RNG."""
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    ids: set[str] = set()
    while len(ids) < 2:
        ids.add("probe-%06x" % rng.getrandbits(24))
    labels = ["base", "cand"]
    rng.shuffle(labels)
    return dict(zip(sorted(ids), labels))


def render_pack(template: str, *, pack_id: str, today: str, persona: str,
                hunting_ground: str, seed_thread: str, laws: str, steer: str,
                extra: str = "") -> str:
    return template.format(mate_id=pack_id, date=today, persona=persona.strip(),
                           hunting_ground=hunting_ground.strip(),
                           seed_thread=seed_thread.strip(), laws=(laws or "").strip(),
                           steer_block=steer) + extra


def build_pair(template: str, today: str, mate: dict[str, Any], laws: str, steer: str,
               delta: str, blind: dict[str, str]) -> dict[str, str]:
    """Two packs for ONE mission. They differ only by pack id and by the
    HARNESS DELTA block, which only the "cand" side carries."""
    out = {}
    for pid in sorted(blind):
        extra = PROBE_NOTE + (DELTA_BLOCK.format(delta=delta.strip()) if blind[pid] == "cand" else "")
        out[pid] = render_pack(template, pack_id=pid, today=today, persona=mate["persona"],
                               hunting_ground=mate["hunting_ground"],
                               seed_thread=mate["seed_thread"], laws=laws, steer=steer,
                               extra=extra)
    return out


def _rounds(paths: dict[str, Path]) -> list[dict[str, Any]]:
    d = paths["rounds"]
    out = [r for r in (_read_json(p) for p in sorted(d.glob("r_*.json"))) if r] if d.is_dir() else []
    return sorted(out, key=lambda r: r["round_id"])


def pending_candidates(today: str, paths: dict[str, Path], receipts_dir: Path,
                       log: Callable[[str], Any] = print) -> list[tuple[Path, dict[str, Any]]]:
    used = {r["candidate"] for r in _rounds(paths)}
    out = []
    d = paths["cand"]
    for p in sorted(d.glob("candidate_*.md")) if d.is_dir() else []:
        m = CAND_RE.match(p.name)
        if not m or m.group(1) >= today or p.name in used:
            continue
        c = parse_candidate(p.read_text(encoding="utf-8", errors="replace"), receipts_dir)
        if c["status"] == "delta":
            out.append((p, c))
        else:
            log(f"harness_probe: candidate {p.name} not probed ({c['status']}: {c['reason']})")
    return out


def _target_mate(c: dict[str, Any], mates: list[dict[str, Any]], today: str) -> dict[str, Any]:
    by_id = {m["id"]: m for m in mates}
    if c.get("target_mate") in by_id:
        return by_id[c["target_mate"]]
    d = datetime.strptime(today, "%Y%m%d").date()
    return mates[d.toordinal() % len(mates)]


# ------------------------------------------------------------------ compose / select

def parse_verdicts(text: str) -> list[dict[str, Any]]:
    blocks, cur = [], None
    for line in text.splitlines():
        if re.match(r"^\s*ROUND\s*:", line):
            cur = [line]
            blocks.append(cur)
        elif cur is not None:
            cur.append(line)
    out = []
    for b in blocks:
        fields, secs = _sections("\n".join(b))
        exp: dict[str, str] = {}
        for line in secs.get("EXPERIENCE", "").splitlines():
            m = re.match(r"^\s*-?\s*(cue|lesson|evidence|confidence)\s*:\s*(.+?)\s*$", line, re.I)
            if m:
                exp[m.group(1).lower()] = m.group(2)
        diff = secs.get("DIFF", "")
        if diff.startswith("```"):
            diff = "\n".join(ln for ln in diff.splitlines() if not ln.startswith("```"))
        out.append({"round": fields.get("ROUND", "").strip(), "choice": fields.get("CHOICE", "").strip(),
                    "action": fields.get("ACTION", "").strip().lower().replace(" ", "_"),
                    "target": fields.get("TARGET", "").strip() or "configs/mates.yaml",
                    "diff": diff.strip() + ("\n" if diff.strip() else ""), "experience": exp})
    return out


def experience_complete(exp: dict[str, str]) -> bool:
    return all(str(exp.get(k) or "").strip() for k in EXPERIENCE_KEYS) and bool(citations(exp.get("evidence", "")))


def judge(v: dict[str, Any], rnd: dict[str, Any], receipts_dir: Path) -> dict[str, Any]:
    """Unblind one composer verdict. outcome: propose | keep_base | invalid."""
    blind = rnd["blind"]
    base = {"round_id": rnd["round_id"], "choice": v["choice"], "action": v["action"]}
    if v["choice"] not in blind:
        return {**base, "outcome": "invalid", "reason": "CHOICE is not one of this round's pack ids"}
    if v["action"] not in ("adopt", "keep_base"):
        return {**base, "outcome": "invalid", "reason": "ACTION must be adopt or keep_base"}
    exp = v["experience"]
    if not experience_complete(exp):
        return {**base, "outcome": "invalid", "reason": "EXPERIENCE needs cue, lesson, evidence (receipt:line), confidence"}
    mine = {f"receipt_{rnd['date']}_{pid}.md" for pid in blind}
    cites = citations(exp["evidence"])
    if not any(name in mine for name, _ in cites):
        return {**base, "outcome": "invalid", "reason": "evidence cites no line of this round's receipts"}
    bad = check_citations(cites, receipts_dir)
    if bad:
        return {**base, "outcome": "invalid", "reason": "bad evidence: " + "; ".join(bad)}
    label = blind[v["choice"]]
    if v["action"] == "adopt" and label == "cand":
        return {**base, "label": label, "outcome": "propose", "reason": "composer chose the candidate run"}
    why = "composer chose the base run" if label == "base" else "composer kept the base"
    return {**base, "label": label, "outcome": "keep_base", "reason": why}


def proposal_payload(v: dict[str, Any], rnd: dict[str, Any]) -> dict[str, Any]:
    exp = v["experience"]
    other = next(p for p in rnd["blind"] if p != v["choice"])
    rat = (f"Harness2 round {rnd['round_id']} on mate {rnd['target_mate']}'s mission: composer "
           f"chose {v['choice']} (unblinded: candidate run) over {other} (base).\n"
           + "".join(f"{k}: {exp[k]}\n" for k in EXPERIENCE_KEYS)
           + f"candidate: {rnd['candidate']} sha256 {rnd['candidate_sha256'][:16]}\n")
    payload: dict[str, Any] = {"title": f"harness2 {rnd['round_id']}: adopt {rnd['candidate']}"[:P.TITLE_CAP],
                               "targets": [v["target"]], "rationale": rat[:P.TEXT_CAP]}
    if v["diff"].strip():
        payload["diff"] = v["diff"]
    else:
        payload["patch_path"] = rnd["candidate_rel"]
    return payload


def file_verdict_proposal(v: dict[str, Any], rnd: dict[str, Any], *, proposals_root=None,
                          allowlist=None, key_path=None) -> dict[str, Any]:
    """Sign with the COMPOSER'S OWN key (mate:composer) and file it."""
    msg = P.sign_message("proposal", proposal_payload(v, rnd),
                         key_path=key_path or mate_key_path("composer"))
    if msg["payload"]["seat"] != mate_seat("composer"):
        raise ValueError("composer key does not belong to mate:composer")
    return P.submit(msg, root=proposals_root, allowlist=allowlist)


def file_review(mate_id: str, proposal_id: str, verdict: str, reason: str, *,
                proposals_root=None, allowlist=None, key_path=None) -> dict[str, Any]:
    """One mate's review, signed with THAT mate's own key."""
    msg = P.sign_message("review", {"proposal_id": proposal_id, "verdict": verdict,
                                    "reason": reason[:P.TEXT_CAP]},
                         key_path=key_path or mate_key_path(mate_id))
    if msg["payload"]["seat"] != mate_seat(mate_id):
        raise ValueError(f"key does not belong to {mate_seat(mate_id)}")
    return P.submit(msg, root=proposals_root, allowlist=allowlist)


# ------------------------------------------------------------------ reflect / library

def lesson_block(pid: str, exp: dict[str, str], tally: dict[str, Any], round_id: str,
                 day: str) -> str:
    one = lambda s: " ".join(str(s).split())  # noqa: E731
    return (f"\n## AMENDMENT ({day}, harness2 lesson {pid}): {one(exp['cue'])}\n"
            f"- lesson: {one(exp['lesson'])}\n"
            f"- evidence: {one(exp['evidence'])} (round {round_id})\n"
            f"- confidence: {one(exp['confidence'])}\n"
            f"- adopted: author {tally['author']}; approvals {', '.join(tally['approvers'])}; "
            f"non-GLM {', '.join(tally.get('non_glm_approvers') or []) or 'operator'}\n")


def append_lesson(pid: str, exp: dict[str, str], rib: Path, tally: dict[str, Any],
                  round_id: str, day: str | None = None) -> dict[str, Any]:
    """Append-only: refuses unless promoted AND ready with a complete,
    evidence-tied experience; idempotent by proposal id; verifies the old
    bytes are an unchanged prefix after the write."""
    if not (tally.get("promoted") and tally.get("ready")):
        return {"ok": False, "reason": "not adopted (needs ready + promotion)"}
    if not experience_complete(exp):
        return {"ok": False, "reason": "experience incomplete or without receipt:line evidence"}
    old = rib.read_bytes()
    if f"harness2 lesson {pid}".encode() in old:
        return {"ok": True, "reason": "already amended", "appended": 0}
    day = day or date.today().isoformat()
    sep = b"" if old.endswith(b"\n") or not old else b"\n"
    add = sep + lesson_block(pid, exp, tally, round_id, day).encode("utf-8")
    if P._secret_hits(add.decode("utf-8")):
        return {"ok": False, "reason": "lesson trips the secret scanner"}
    with open(rib, "ab") as fh:
        fh.write(add)
    new = rib.read_bytes()
    if not new.startswith(old):
        raise RuntimeError(f"append-only violated on {rib}")
    return {"ok": True, "reason": "amended", "appended": len(add)}


# ------------------------------------------------------------------ host steps

def harvest_reviews(today: str, mates_ids: list[str], receipts_dir: Path, paths: dict[str, Path],
                    *, proposals_root=None, allowlist=None, log: Callable[[str], Any] = print) -> int:
    """Sign each REVIEW line in recent mate receipts with that mate's own key."""
    n = 0
    lo = today
    for _ in range(HARVEST_DAYS):
        lo = _prev_day(lo)
    for p in sorted(receipts_dir.glob("receipt_*.md")) if receipts_dir.is_dir() else []:
        m = RECEIPT_RE.match(p.name)
        if not m or not (lo <= m.group(1) < today) or m.group(2) not in mates_ids:
            continue
        mid = m.group(2)
        for rm in REVIEW_RE.finditer(p.read_text(encoding="utf-8", errors="replace")):
            pid, verdict, reason = rm.group(1), rm.group(2), rm.group(3).strip()
            mark = paths["reviews"] / f"{p.stem}__{pid}.json"
            if mark.exists() or not mate_key_path(mid).is_file():
                continue
            try:
                res = file_review(mid, pid, verdict, reason or f"via {p.name}",
                                  proposals_root=proposals_root, allowlist=allowlist)
            except ValueError as exc:
                log(f"harness_probe: review {mid} -> {pid} refused: {exc}")
                continue
            _write_new_json(mark, {"receipt": p.name, "proposal_id": pid, "seat": res["seat"],
                                   "verdict": verdict, "filed": _now_iso()})
            n += 1
    return n


def file_verdicts(today: str, receipts_dir: Path, paths: dict[str, Path], *, proposals_root=None,
                  allowlist=None, log: Callable[[str], Any] = print) -> list[dict[str, Any]]:
    rounds = {r["round_id"]: r for r in _rounds(paths)}
    done = []
    d = paths["vfiles"]
    for vf in sorted(d.glob("verdict_*_composer.md")) if d.is_dir() else []:
        m = VERDICT_RE.match(vf.name)
        if not m or m.group(1) >= today:
            continue
        for v in parse_verdicts(vf.read_text(encoding="utf-8", errors="replace")):
            rnd = rounds.get(v["round"])
            rec_path = paths["verdicts"] / f"{v['round']}.json"
            if rnd is None or rec_path.exists() or rnd["date"] >= m.group(1):
                continue
            res = judge(v, rnd, receipts_dir)
            res.update({"verdict_file": vf.name, "experience": v["experience"],
                        "target_mate": rnd["target_mate"], "judged": _now_iso()})
            if res["outcome"] == "propose":
                try:
                    filed = file_verdict_proposal(v, rnd, proposals_root=proposals_root,
                                                  allowlist=allowlist)
                    res["proposal_id"] = filed["proposal_id"]
                except (ValueError, OSError) as exc:
                    res.update({"outcome": "invalid", "reason": f"proposal refused: {exc}"})
            _write_new_json(rec_path, res)
            log(f"harness_probe: {v['round']} -> {res['outcome']} ({res['reason']})")
            done.append(res)
    return done


def learn(paths: dict[str, Path], rib: Path, *, proposals_root=None, allowlist=None,
          log: Callable[[str], Any] = print) -> list[dict[str, Any]]:
    out = []
    d = paths["verdicts"]
    for rec in (_read_json(p) for p in sorted(d.glob("r_*.json"))) if d.is_dir() else []:
        pid = (rec or {}).get("proposal_id")
        if not pid or (paths["lessons"] / f"{pid}.json").exists():
            continue
        t = P.tally(pid, root=proposals_root, allowlist=allowlist)
        if t["ready"] and not t["promoted"] and mate_key_path("composer").is_file():
            try:
                P.submit(P.sign_message("promotion", {"proposal_id": pid, "state": "ready"},
                                        key_path=mate_key_path("composer")),
                         root=proposals_root, allowlist=allowlist)
                t = P.tally(pid, root=proposals_root, allowlist=allowlist)
            except ValueError as exc:
                log(f"harness_probe: promotion {pid} refused: {exc}")
        res = append_lesson(pid, rec["experience"], rib, t, rec["round_id"])
        if res["ok"]:
            _write_new_json(paths["lessons"] / f"{pid}.json",
                            {"proposal_id": pid, "rib": rib.name, "round_id": rec["round_id"],
                             "result": res["reason"], "at": _now_iso()})
            log(f"harness_probe: lesson {pid} -> {rib.name} ({res['reason']})")
        out.append({"proposal_id": pid, **res})
    return out


def advance(today: str, config: dict[str, Any], *, receipts_dir=None, state_dir=None,
            work_dir=None, proposals_root=None, allowlist=None, rib_dir=None,
            log: Callable[[str], Any] = print) -> dict[str, Any]:
    """Host-side half of a round (no model calls): harvest reviews, unblind
    and file verdicts, adopt + learn."""
    hp = config.get("harness_probe") or {}
    paths = _paths(state_dir, work_dir)
    rdir = Path(receipts_dir or RECEIPTS_DIR)
    ids = [m["id"] for m in config.get("mates") or []] + [r["id"] for r in hp.get("roles") or []]
    rib = Path(rib_dir or RIB_DIR) / str(hp.get("lesson_rib") or DEFAULT_RIB)
    out: dict[str, Any] = {}
    for name, fn in (("reviews", lambda: harvest_reviews(today, ids, rdir, paths, proposals_root=proposals_root,
                                                         allowlist=allowlist, log=log)),
                     ("verdicts", lambda: file_verdicts(today, rdir, paths, proposals_root=proposals_root,
                                                        allowlist=allowlist, log=log)),
                     ("lessons", lambda: learn(paths, rib, proposals_root=proposals_root,
                                               allowlist=allowlist, log=log))):
        try:
            out[name] = fn()
        except Exception as exc:  # noqa: BLE001 - one broken step never blocks the others
            log(f"harness_probe: {name} step failed: {type(exc).__name__}: {exc}")
            out[name] = f"error: {exc}"
    return out


def _pending_proposal_rows(paths: dict[str, Path]) -> list[str]:
    rows = []
    d = paths["verdicts"]
    for rec in (_read_json(p) for p in sorted(d.glob("r_*.json"))) if d.is_dir() else []:
        if rec and rec.get("proposal_id") and not (paths["lessons"] / f"{rec['proposal_id']}.json").exists():
            rows.append(f"- {rec['proposal_id']} (round {rec['round_id']}, mate {rec['target_mate']})")
    return rows


def write_round_packs(today: str, config: dict[str, Any], *, start_index: int, missions_dir: Path,
                      receipts_dir: Path, template: str, steer_block: Callable[[str], str] = lambda _m: "-",
                      log: Callable[[str], Any] = print, cap: int = 8, state_dir=None, work_dir=None,
                      proposals_root=None, allowlist=None, rib_dir=None, seed: Any = None,
                      run_host_steps: bool = True) -> list[Path]:
    """Called by tools/leave_dispatcher.write_missions when harness_probe.enabled.
    Idempotent: existing packs are never rewritten; today's rounds are reused."""
    hp = config.get("harness_probe") or {}
    paths = _paths(state_dir, work_dir)
    for key in ("rounds", "cand", "vfiles"):
        paths[key].mkdir(parents=True, exist_ok=True)
    if run_host_steps:
        advance(today, config, receipts_dir=receipts_dir, state_dir=state_dir, work_dir=work_dir,
                proposals_root=proposals_root, allowlist=allowlist, rib_dir=rib_dir, log=log)
    k = max(0, int(hp.get("k", 1)))
    roles = {r["id"]: r for r in hp.get("roles") or []}
    mates = config.get("mates") or []
    laws = config.get("laws", "")
    planned: list[tuple[str, str]] = []

    review_rows = _pending_proposal_rows(paths)
    reviews = REVIEW_ASK.format(rows="\n".join(review_rows)) if review_rows else ""
    for rid, scope, focus in (("editor_inv", "INV", "Hunt one GENERAL harness gap that recurs across mates "
                               "(same failure in 2+ receipts)."),
                              ("editor_dom", "DOM", "Hunt one gap SPECIFIC to a single mate's ground "
                               "(one mate, one mission).")):
        r = roles.get(rid)
        if not r:
            continue
        extra = EDITOR_CONTRACT.format(scope=scope, prev=_prev_day(today), focus=focus, date=today,
                                       role=rid, cap=DELTA_CAP, reviews=reviews)
        planned.append((rid, render_pack(template, pack_id=rid, today=today, persona=r["persona"],
                                         hunting_ground=r["hunting_ground"], seed_thread=r["seed_thread"],
                                         laws=laws, steer=steer_block(rid), extra=extra)))

    todays = [r for r in _rounds(paths) if r["date"] == today]
    if mates:
        for i, (cpath, c) in enumerate(pending_candidates(today, paths, receipts_dir, log)[:max(0, k - len(todays))]):
            mate = _target_mate(c, mates, today)
            rnd = {"schema": SCHEMA, "round_id": f"r_{today}_{len(todays) + 1:02d}", "date": today,
                   "candidate": cpath.name, "candidate_rel": _rel(cpath),
                   "candidate_sha256": _sha(cpath.read_text(encoding="utf-8", errors="replace")),
                   "scope": c["scope"], "target_mate": mate["id"], "delta": c["delta"],
                   "blind": assign_blind(None if seed is None else f"{seed}|{today}|{cpath.name}"),
                   "created": _now_iso()}
            if _write_new_json(paths["rounds"] / f"{rnd['round_id']}.json", rnd):
                todays.append(rnd)
    by_id = {m["id"]: m for m in mates}
    for rnd in todays:
        mate = by_id.get(rnd["target_mate"])
        if not mate:
            continue
        pair = build_pair(template, today, mate, laws, steer_block(mate["id"]), rnd["delta"], rnd["blind"])
        planned.extend(sorted(pair.items()))

    due = [r for r in _rounds(paths) if r["date"] < today
           and not (paths["verdicts"] / f"{r['round_id']}.json").exists()
           and all((Path(receipts_dir) / f"receipt_{r['date']}_{pid}.md").is_file() for pid in r["blind"])]
    comp = roles.get("composer")
    if comp and due:
        rows = []
        for r in due:
            recs = ", ".join(f"watch/inbox/mates_leave_protocol/receipts/receipt_{r['date']}_{pid}.md"
                             for pid in sorted(r["blind"]))
            rows.append(f"- ROUND {r['round_id']} (mission of mate {r['target_mate']}): {recs}\n"
                        f"  candidate delta under test:\n    " + r["delta"].replace("\n", "\n    "))
        extra = COMPOSER_CONTRACT.format(date=today, rounds="\n".join(rows))
        planned.append(("composer", render_pack(template, pack_id="composer", today=today,
                                                persona=comp["persona"], hunting_ground=comp["hunting_ground"],
                                                seed_thread=comp["seed_thread"], laws=laws,
                                                steer=steer_block("composer"), extra=extra)))

    if len(planned) > cap:
        log(f"harness_probe: {len(planned)} packs planned, ceiling leaves room for {cap}; extra dropped")
        planned = planned[:cap]
    missions_dir.mkdir(parents=True, exist_ok=True)
    out = []
    for n, (pack_id, text) in enumerate(planned, start=start_index):
        path = missions_dir / f"mission_{today}_{n:02d}_{pack_id}.md"
        if not path.exists():
            path.write_text(text, encoding="utf-8")
            log(f"mission written {path.name} (harness2)")
        out.append(path)
    return out


# ------------------------------------------------------------------ CLI

def _load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dry_pair(mate_id: str, delta: str, out_dir: Path, today: str, seed: Any = None) -> dict[str, Any]:
    """Pair ONE sample mission into out_dir. No dispatcher, no runner, no model."""
    sys.path.insert(0, str(ROOT / "tools"))
    from leave_dispatcher import MISSION_TEMPLATE  # noqa: E402  (module import runs nothing)

    cfg = _load_config()
    mate = next(m for m in cfg["mates"] if m["id"] == mate_id)
    blind = assign_blind(seed)
    steer = "- (dry run: steer row not read)"
    pair = build_pair(MISSION_TEMPLATE, today, mate, cfg.get("laws", ""), steer, delta, blind)
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {}
    for i, (pid, text) in enumerate(sorted(pair.items()), start=1):
        p = out_dir / f"mission_{today}_{i:02d}_{pid}.md"
        p.write_text(text, encoding="utf-8")
        files[pid] = p
    (out_dir / "blind_map.json").write_text(json.dumps({"mate": mate_id, "blind": blind}, indent=1) + "\n",
                                            encoding="utf-8")
    a, b = sorted(pair)
    norm = {pid: pair[pid].replace(pid, "<ID>") for pid in pair}
    cand = next(p for p in blind if blind[p] == "cand")
    basep = next(p for p in blind if blind[p] == "base")
    only_delta = norm[cand] == norm[basep] + DELTA_BLOCK.format(delta=delta.strip())
    return {"mate": mate_id, "packs": {pid: str(files[pid]) for pid in files},
            "bytes": {pid: len(pair[pid].encode()) for pid in pair}, "blind": blind,
            "differ_only_by_delta": only_delta, "model_calls": 0}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="harness_probe", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status")
    s = sub.add_parser("dry-pair", help="pair one sample mission into --out (no model calls)")
    s.add_argument("--mate", required=True)
    s.add_argument("--delta-file", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--seed")
    s = sub.add_parser("review", help="file one mate's review, signed with that mate's key")
    s.add_argument("--mate", required=True)
    s.add_argument("--proposal", required=True)
    s.add_argument("--verdict", choices=("approve", "reject"), required=True)
    s.add_argument("--reason", default="")
    s = sub.add_parser("advance", help="host steps only: harvest reviews, file verdicts, learn")
    s.add_argument("--date", default=datetime.now().strftime("%Y%m%d"))
    a = ap.parse_args(argv)
    if a.cmd == "status":
        paths = _paths(None, None)
        cfg = _load_config()
        print(json.dumps({"enabled": (cfg.get("harness_probe") or {}).get("enabled") is True,
                          "rounds": [r["round_id"] for r in _rounds(paths)],
                          "pending_proposals": _pending_proposal_rows(paths)}, indent=1))
    elif a.cmd == "dry-pair":
        today = datetime.now().strftime("%Y%m%d")
        delta = Path(a.delta_file).read_text(encoding="utf-8")
        print(json.dumps(dry_pair(a.mate, delta, Path(a.out), today, a.seed), indent=1))
    elif a.cmd == "review":
        print(json.dumps(file_review(a.mate, a.proposal, a.verdict, a.reason), indent=1))
    elif a.cmd == "advance":
        print(json.dumps(advance(a.date, _load_config()), indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
