#!/usr/bin/env python3
"""cycle_brief - the flywheel's morning composer, v1 = THE STEERING SURFACE.

v0 (SNOWBALL_PLAN C1, 2026-10-01): the handoff register - one file per
cycle assembling what every organ produced overnight into what the next
cycle consumes.

v1 (operator: "steer it and learn", 2026-09-30): the brief stops being a
passive register and becomes the day's steering surface. New sections,
in draw order:
  - ANIMAL PROFILES   tools/animal_profiles.py --distill (the fleet sees
                      its own model knowledge at dawn)
  - DOCTRINE SCORECARD  tools/doctrine_arbiter.py scorecard; EXPIRED
                      doctrine is NAMED FOR RETIREMENT (operator gate,
                      never auto-removed)
  - QUOTA + SHAPE REC  tools/quota_ledger.py HOLD/GO head PLUS a derived
                      "today's shape: X-wide staggered" recommendation
                      from the instrument's own measured envelope bytes
  - CLIMB QUEUE       the next 3 pitches from the execution order (the
                      lensing's PRIORITY ORDERING), status + gates
  - MISSIONS          the SEEDS section is now specific lane MISSIONS -
                      pre-written prompts for the mates' next cycle,
                      drawn from the sections above, never invented

Consumes (all byte-backed, never guessed): the v0 sources (stealth tail,
gate digest, meter anomalies, yesterday's receipts) plus the four above.

Fail-open on missing sources (named HONEST-GAP, never fabricated). Zero
network. Runs on the 08:00 task chain before the dispatcher.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "watch" / "inbox"
STEALTH = OUT_DIR / "STEALTH_MINED_FINDINGS.jsonl"
LENSING = OUT_DIR / "mountain_climb" / "THE_LENSING.md"
GATE_DIGEST_MD = OUT_DIR / "GATE_DIGEST.md"
VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"

# climb-queue receipt probes: pitch id -> (receipt, status probe). Every
# status marker cites bytes on disk; a missing receipt is an honest gap.
CLIMB_RECEIPTS: dict[str, tuple[Path, str]] = {
    "P2": (OUT_DIR / "last_mile_20260930" / "B4_SRP6_PORT.md",
           "SRP6 port LANDED (B4, commit 066ba7ef0); lensing demands transport "
           "integrity + group/hash upgrade-or-retire: OPEN"),
    "P3": (OUT_DIR / "last_mile_20260930" / "B5_BUILD.md",
           "artifact LANDED (mountain-e0ff8cec0.zip 28.9 MB); lensing demands "
           "tagged-commit rebuild + one clean-machine run receipt: OPEN"),
    "P6": (OUT_DIR / "last_mile_20260930" / "LW2_ADAM_INVITE.md",
           "invite drafted NOT SENT (identity discipline: Adam's GitHub "
           "username unconfirmed): BLOCKED ON OPERATOR DOOR"),
}


def _run(module: str, *args: str) -> str:
    """Run a sibling tool as a MODULE (python -m tools.X). Module form is
    the law here: the estate splits tool files into cores mid-flight (the
    doctrine_arbiter split, 2026-09-30, broke script-form calls with
    ModuleNotFoundError while -m kept working)."""
    try:
        r = subprocess.run([str(VENV_PY), "-m", module, *args], cwd=str(ROOT),
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120,
                           creationflags=0x08000000 if sys.platform == "win32" else 0)
        if r.returncode == 0:
            return r.stdout
        # Non-zero is often an ATTENTION exit (quota RED, anomaly rows,
        # doctrine EXPIRED) with the full report still on stdout - keep
        # ALL of it, marker first, so section parsers see the real bytes.
        return f"[exit {r.returncode}]\n{r.stdout}"
    except Exception as exc:  # noqa: BLE001 - fail-open, named
        return f"[cannot-run: {exc}]"


def _strip_markers(lines: list[str]) -> list[str]:
    """Drop the [exit N]/[cannot-run ...] marker lines from display."""
    return [l for l in lines
            if l.strip() and not re.fullmatch(r"\[(exit \d+|cannot-run:.*)\]", l.strip())]


def stealth_tail(n: int = 8) -> list[dict]:
    if not STEALTH.exists():
        return []
    rows = []
    with STEALTH.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows[-n:]


# ------------------------------------------------------- v1 section builders

def _no_emdash(s: str) -> str:
    """House law: this file authors zero em-dashes. Instrument bytes keep
    theirs on disk; embedded excerpts are rendered with plain hyphens."""
    return s.replace("\u2014", "-").replace("\u2013", "-")


def section_animal_profiles() -> list[str]:
    out = _run("tools.animal_profiles", "--distill")
    lines = _strip_markers(out.splitlines())[:14]
    head = ["## ANIMAL PROFILES (the fleet's own model knowledge at dawn -",
            "memory/behavioral/animals/ distilled; a stale rib is a smell)"]
    if not lines or lines[0].startswith(("[", "no observations")):
        return head + [f"HONEST-GAP: {out.strip()[:120] or 'no behavioral observations yet'}", ""]
    return head + lines + ["", "stale-row law: any animal whose newest ts predates the last",
                           "wave gets an observation mission below (ribs stay true).", ""]


def section_arena_gwap() -> list[str]:
    """The arena's gwap line with the banked_at moment column (GO item 6,
    a01#5, 2026-10-04): the a01 audit watched its banking verdict flip NO to
    YES between its 03:04Z and 03:26:51Z reads, so every count this brief
    restates carries its AS-OF stamp from the instrument itself."""
    out = _run("tools.arena_gwap", "--status")
    lines = _strip_markers(out.splitlines())
    head = [l for l in lines if l.startswith(("GWAP LEDGER", "ledger rows"))][:2]
    unbanked = [l for l in lines if "banked_at=UNBANKED" in l]
    newest = [l for l in lines
              if l.startswith("banked_at ") and "UNBANKED" not in l][-6:]
    sec = ["## ARENA GWAP (banked_at moments - the moving-tree law: no count without its AS-OF)"]
    if not head:
        sec += ["HONEST-GAP: tools.arena_gwap --status unrunnable"] + (
            [_no_emdash(out.splitlines()[0])[:120]] if out.strip() else []) + [""]
        return sec
    sec += head
    sec += [f"- unbanked dirs at this read: {len(unbanked)}"]
    sec += [f"- {unbanked[0]}"] if unbanked else ["- no unbanked dirs at this read"]
    sec += [f"- {l}" for l in newest]
    sec.append("")
    return sec


def section_doctrine() -> tuple[list[str], list[str], bool]:
    """Scorecard section + the retire-candidate ids + whether the ledger
    is empty (drives a seeding mission)."""
    out = _run("tools.doctrine_arbiter", "scorecard")
    lines = _strip_markers(out.splitlines())
    head = ["## DOCTRINE SCORECARD (measured, not obeyed - doctrine_arbiter R10)",
            "EXPIRED = named for retirement (operator gate; never auto-removed)"]
    empty = bool(lines) and lines[0].startswith("NO DOCTRINE")
    if not lines:
        return head + ["HONEST-GAP: doctrine_arbiter produced no output "
                       "(cannot-run or crash - investigate, do not guess)"], [], True
    if empty:
        return head + ["HONEST-GAP: " + lines[0] + " - the arbiter landed 09-30 with",
                       "zero registrations; the seeding mission below opens the ledger."], [], True
    # item rows render as "  <id> <status> <kind> ..." (two-space indent);
    # the SUMMARY line also contains the word EXPIRED - match rows only.
    expired = [l for l in lines if re.match(r"^\s{2}\S+\s+EXPIRED\s", l)]
    body = [_no_emdash(l) for l in lines[:16]]
    sec = head + body
    if expired:
        sec += ["", "NAMED FOR RETIREMENT (EXPIRED - operator gate, never auto-removed):"]
        sec += [f"- {l.strip()}" for l in expired]
    return sec, [l.strip().split()[0] for l in expired], False


def quota_recommendation(report: str, verdict: str) -> str:
    """Derive 'today's shape: X-wide staggered' from the instrument's own
    measured-envelope bytes (the hold line carries stagger/clean ranges).
    Never at-once: the 19-at-once RED is the standing measured law."""
    hold = next((l for l in report.splitlines() if l.startswith("HOLD threshold")), "")
    stagger = re.search(r"stagger (\d+)-(\d+) wide", hold)
    clean = re.search(r"clean shape (\d+)-(\d+) sustained", hold)
    if verdict == "GREEN" and clean:
        rng = f"{clean.group(2)}-wide staggered (proven clean envelope {clean.group(1)}-{clean.group(2)})"
    elif verdict == "AMBER" and stagger and clean:
        rng = f"{stagger.group(2)}-wide staggered (recover toward the clean {clean.group(1)}-{clean.group(2)})"
    elif stagger:
        rng = f"{stagger.group(1)}-{stagger.group(2)}-wide staggered (hold-line floor; day verdict RED)"
    else:
        rng = "6-8-wide staggered (fallback: hold-line law, envelope unparseable)"
    return f"today's shape: {rng} - STAGGERED, never at-once"


def section_quota() -> tuple[list[str], str]:
    report = _run("tools.quota_ledger")
    # v1 fix: v0 shelled quota_ledger_report.py (a library module with no
    # __main__) so every brief printed "[quota report empty - HONEST-GAP]"
    # while the real CLI lived in quota_ledger.py. Cause named, CLI fixed.
    verdict_m = re.search(r"Day-shape verdict: \*\*(\w+)\*\*", report)
    shape_m = re.search(r"current shape \*\*(\w+)\*\*", report)
    verdict = verdict_m.group(1) if verdict_m else "?"
    shape = shape_m.group(1) if shape_m else "?"
    head_lines = [_no_emdash(l) for l in _strip_markers(report.splitlines())][:5]
    rec = quota_recommendation(report, verdict)
    sec = ["## QUOTA LEDGER (HOLD/GO - the fleet self-throttles on this)",
           f"day verdict **{verdict}** | live signal **{shape}**", "```"]
    sec += head_lines + ["```", f"**RECOMMENDATION: {rec}**", ""]
    return sec, verdict


def climb_rows() -> list[dict]:
    """Next 3 pitches from the execution order = the lensing's PRIORITY
    ORDERING ranking (THE_LENSING.md section 4), the newest route law."""
    if not LENSING.exists():
        return []
    text = LENSING.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\*\*Ranking:\*\*(.*?)(?:\*\*First divergence|\Z)", text, re.S)
    if not m:
        return []
    rows = []
    for rank, pid, rest, tail_txt in re.findall(
            r"^(\d+)\.\s+\*\*(P\d)\s*([^*]*)\*\*\.?\s*(.+)$", m.group(1), re.M):
        receipt, status = CLIMB_RECEIPTS.get(pid, (None, "no receipt probe: HONEST-GAP"))
        rows.append({"rank": rank, "pid": pid, "title": (pid + " " + rest.strip()).strip(": ."),
                     "gate": _no_emdash(" ".join(tail_txt.split()))[:200],
                     "status": status if (receipt is None or receipt.exists()) else
                     f"HONEST-GAP: expected receipt {receipt.name} absent - pitch not landed",
                     "receipt": receipt.name if receipt else "?"})
        if len(rows) == 3:
            break
    return rows


def section_climb_queue(rows: list[dict]) -> list[str]:
    sec = ["## CLIMB QUEUE (next 3 pitches from the execution order -",
           "source: THE_LENSING section 4 PRIORITY ORDERING, the post-lensing reorder)"]
    if not rows:
        return sec + ["HONEST-GAP: lensing ranking unparseable/absent - read",
                      "watch/inbox/mountain_climb/THE_LENSING.md by hand", ""]
    for r in rows:
        sec += [f"### {r['rank']}. {r['title']}",
                f"- status: {r['status']}",
                f"- gate (lens, verbatim-order): {r['gate']}",
                f"- evidence: {r['receipt']} (watch/inbox/last_mile_20260930/)"]
    return sec + ["", "standing gates: paid asks fire only on operator GO (AA1 law);",
                  "the stranger door is an operator door (one Discord ask).", ""]


def section_missions(rows: list[dict], retired: list[str], ledger_empty: bool,
                     verdict: str, stamp: str, walls: int) -> list[str]:
    """SEEDS v1: pre-written lane MISSIONS drawn from the sections above -
    paste-ready prompts, not suggestions. Every mission names source,
    falsifier and receipt path."""
    sec = ["## MISSIONS (pre-written prompts for the mates' next cycle -",
           "drawn from the sections above; the mates paste, they do not interpret)", ""]
    lm = f"watch/inbox/last_mile_{stamp}"
    climb_mission = {
        "P6": ("STRANGER-PREP", "wire the instrumented first contact so it fires the moment the "
               "operator returns Adam's GitHub username: TLS stream with pinned cert on the "
               "authoritative server, server-side tape capture ARMED before connect, and SSH-key "
               "challenge verification against github.com/<user>.keys",
         "a session tape whose challenge signature verifies against the published key, replaying byte-identically"),
        "P3": ("BUILD-RAIL-REDUCED", "rebuild the artifact from a TAGGED "
               "the-mountain commit (not the roblox_to_godot twin), embed the commit sha in the "
               "artifact and print it at boot, bank ONE clean-machine run receipt (fresh machine, "
               "record SmartScreen/AV), ship via GitHub Release or itch butler",
         "clean-machine run receipt naming the tagged sha; no custom delta rail"),
        "P2": ("TRANSPORT-INTEGRITY", "close the auth debt the lensing named: TLS or K-bound frame "
               "MACs on post-auth frames, upgrade-or-retire the WoW 256-bit group + SHA1, delete "
               "the plaintext hello path in both trees",
         "an on-path injection attempt FAILS and is named in a receipt; grep finds no live plaintext hello"),
    }
    for i, r in enumerate(rows, 1):
        name, work, falsifier = climb_mission.get(
            r["pid"], (r["pid"], r["gate"], "the lens's own falsifier"))
        sec += [f"### MISSION {i} - climb lane ({name})",
                "> PROMPT: \"" + work + ". Sources: THE_LENSING sections 4-5, "
                + r["receipt"] + ".\"",
                f"> FALSIFIER: {falsifier}.",
                f"> RECEIPT: {lm}/{r['pid']}_{name}.md", ""]
    if ledger_empty:
        sec += ["### MISSION DOCTRINE-SEED - doctrine lane",
                "> PROMPT: \"the arbiter's ledger is EMPTY (R10 landed 09-30, zero rows). "
                "Register the first pre-registered doctrine four-tuples from today's own "
                "predictions: e.g. P4-at-1-2-lane-days (gps_ledger), staggered-vs-burst wall "
                "rate (anomaly/quota receipts). Pre-registration law: no checkable "
                "predicted_outcome = VOID at registration.\"",
                "> FALSIFIER: doctrine_arbiter scorecard shows rows PENDING with instruments, exit 0.",
                f"> RECEIPT: {lm}/DOCTRINE_SEED.md", ""]
    elif retired:
        sec += ["### MISSION DOCTRINE-RETIRE - operator gate lane",
                "> PROMPT: \"the scorecard names EXPIRED doctrine: " + ", ".join(retired)
                + ". Draft the retire notes citing each item's last measurement; the operator "
                "runs tools/doctrine_arbiter.py retire --id (never auto-removed).\"",
                "> FALSIFIER: retire drafts cite measured values, not vibes.",
                f"> RECEIPT: {lm}/DOCTRINE_RETIRE_DRAFT.md", ""]
    sec += ["### MISSION ANIMAL-OBSERVE - behavioral lane",
            f"> PROMPT: \"the day recorded {walls} wall moment(s) and day verdict {verdict}: append one "
            "observation row per wall code to memory/behavioral/animals/ via tools/animal_profiles.py "
            "observe (kind=failure/envelope), every row citing its receipt source; contradictions "
            "with the rib go to memory/attention.md.\"",
            "> FALSIFIER: animal_profiles --distill newest ts = today for every animal that hit a wall.",
            f"> RECEIPT: {lm}/ANIMAL_OBSERVE.md", ""]
    return sec


# ------------------------------------------------------------------- main ---

def main() -> int:
    today = datetime.now()
    stamp = today.strftime("%Y%m%d")
    ymd = today.strftime("%Y-%m-%d")
    parts: list[str] = [f"# CYCLE BRIEF {ymd} v1 (the steering surface)", ""]

    # 1. the fleet's own model knowledge at dawn
    parts += section_animal_profiles()

    # 2. doctrine measured, not obeyed
    doctrine_sec, retired, ledger_empty = section_doctrine()
    parts += doctrine_sec

    # 3. fuel state + the day's shape recommendation
    quota_sec, verdict = section_quota()
    parts += quota_sec

    # 3.5 the arena's gwap line, moment-stamped (GO item 6 banked_at column)
    parts += section_arena_gwap()

    # 4. the climb: next 3 pitches, status + gates
    rows = climb_rows()
    parts += section_climb_queue(rows)

    # operator gates: run the digest, fall back to the standing artifact
    gates = _run("tools.gate_digest")
    gate_lines = [l for l in gates.splitlines() if l.strip().startswith(("OPEN", "CLOSED", "|"))][:14]
    if not gate_lines and GATE_DIGEST_MD.exists():
        gate_lines = [_no_emdash(l) for l in GATE_DIGEST_MD.read_text(
            encoding="utf-8", errors="replace").splitlines() if l.strip()][:10]
    parts += ["## OPERATOR GATES (human doors - machine burning does not clear these)"] + \
        (gate_lines or ["HONEST-GAP: gate_digest unrunnable and GATE_DIGEST.md unreadable"]) + [""]

    # stealth tail (C3 staged: the fleet stops being write-only)
    tail = stealth_tail()
    parts += [f"## STEALTH TAIL (last {len(tail)} findings - triage targets)"]
    for r in tail:
        note = str(r.get("note", r.get("ponytail_audit", "")))[:100]
        parts.append(f"- {r.get('ts', '?')[:19]} | {str(r.get('lane', '?'))[:12]} | "
                     f"{str(r.get('model', '?'))[:28]} | finish={r.get('finish', '?')} "
                     f"cached={r.get('cached_tokens', '?')} | {note}")
    parts.append("")

    # anomalies (the instruments' own drift)
    anom = _run("tools.anomaly_flagger", "--max-rows", "20")
    anom_lines = [_no_emdash(l) for l in _strip_markers(anom.splitlines())][:10]
    parts += ["## ANOMALY COUNTS (exit 1 = rows named below)"] + anom_lines + [""]

    # yesterday's synthesis pointer (the loop's memory)
    ysyn = OUT_DIR / f"DAY_SYNTHESIS_{(today - timedelta(days=1)).strftime('%Y%m%d')}.md"
    parts += [f"## YESTERDAY", f"- synthesis: {'PRESENT' if ysyn.exists() else 'HONEST-GAP absent'} ({ysyn.name})",
              "- receipts: see watch/inbox/last_mile_* newest", ""]

    # 5. SEEDS v1: missions, not suggestions
    walls_m = re.search(r"wall moments \*\*(\d+)\*\*", "\n".join(quota_sec))
    parts += section_missions(rows, retired, ledger_empty, verdict, stamp,
                              int(walls_m.group(1)) if walls_m else 0)

    out = OUT_DIR / f"CYCLE_BRIEF_{stamp}.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"cycle brief v1 -> {out} ({out.stat().st_size} bytes, "
          f"verdict {verdict}, {len(rows)} climb pitches, {len(parts)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
