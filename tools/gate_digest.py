"""Gate digest: the standing one-glance list of OPEN operator gates.

Why (2026-09-30, lensing floor item 4 + economics F5.5): the estate stalls
silently on operator-only gates and lanes burn quota rediscovering them (the
LW2 pattern). Scans receipts/mtimes/configs, writes watch/inbox/GATE_DIGEST.md.

Close law: a row closes ONLY by (1) a byte probe flipping it, or (2) a .md
under watch/inbox, newer than the gate's birth receipt, containing the line
"GATE-CLOSED: <slug>". Never hand-edit the digest; regenerate it.
No secret VALUE ever crosses a probe boundary (booleans only).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

ESTATE_ROOT = Path(__file__).resolve().parent.parent
INBOX = ESTATE_ROOT / "watch" / "inbox"
DIGEST_PATH = INBOX / "GATE_DIGEST.md"
MAG_YAML = ESTATE_ROOT / "configs" / "mag.yaml"
ENV_PATH = ESTATE_ROOT / ".env"
LEAK_ROWS = ESTATE_ROOT / "memory" / "trajectory" / "steps.jsonl"
ENV_KEY_NAME = "ZAI_API_KEY_Pro"


@dataclass
class Gate:
    slug: str
    name: str
    why: str
    action: str
    receipts: list[str]  # posix paths relative to root; [0] is the birth receipt
    probe: Callable[[], tuple[str, str]] = field(default=None)  # type: ignore[assignment]

    def birth_path(self) -> Path:
        return ESTATE_ROOT / self.receipts[0]


# ---------------------------------------------------------------- byte probes

def _mtime(p: Path) -> datetime:
    return datetime.fromtimestamp(p.stat().st_mtime)


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def receipt_closes(gate: Gate) -> Path | None:
    """Newest-than-birth inbox receipt carrying the formal close line, if any."""
    if not gate.birth_path().is_file():
        return None
    birth = _mtime(gate.birth_path()).timestamp()
    marker = f"GATE-CLOSED: {gate.slug}"
    hits: list[Path] = []
    for md in INBOX.rglob("*.md"):
        try:
            if md.stat().st_mtime <= birth:
                continue
        except OSError:
            continue
        if marker in _read(md):
            hits.append(md)
    return max(hits, key=_mtime) if hits else None


def probe_marker(gate: Gate) -> tuple[str, str]:
    closed_by = receipt_closes(gate)
    if closed_by is not None:
        rel = closed_by.relative_to(ESTATE_ROOT).as_posix()
        return "CLOSED", f"closed by receipt {rel}"
    return "OPEN", "no close receipt found"


def probe_lensing() -> tuple[str, str]:
    """Phase-2 lensing GO: closed by the landed return (the lensing ran)."""
    ret = INBOX / "mountain_climb" / "THE_LENSING.md"
    if ret.is_file():
        rel = ret.relative_to(ESTATE_ROOT).as_posix()
        return "CLOSED", f"lensing returned; receipt {rel} landed"
    return "OPEN", "no lensing return on disk"


def probe_verkle_v2() -> tuple[str, str]:
    """Verkle v2 flip: the flag itself is the truth. v2 means flipped."""
    text = _read(MAG_YAML)
    m = re.search(r"^chain_mode:\s*(\S+)", text, re.MULTILINE)
    if not m:
        return "OPEN", "configs/mag.yaml chain_mode line missing (checked this run)"
    mode = m.group(1)
    if mode == "v2":
        return "CLOSED", "configs/mag.yaml reads chain_mode: v2 (flipped)"
    return "OPEN", f"configs/mag.yaml reads chain_mode: {mode} (checked this run)"


def _live_env_value() -> str | None:
    """Current .env value for ENV_KEY_NAME, or None. Never printed by callers."""
    if not ENV_PATH.is_file():
        return None
    for line in _read(ENV_PATH).splitlines():
        if line.startswith(ENV_KEY_NAME + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _leaked_rows_carry(value: str) -> bool | None:
    """True if the on-disk pre-containment leak copy still carries the value.

    Ground truth 2026-09-30: no reachable commit carries steps.jsonl (the file
    was index/on-disk exposure, audit finding #1), so the disk file IS the
    leak copy. Post-AG1 rows are redacted, so a rotated value can never land
    there: present means the old value is still the live key.
    """
    try:
        blob = LEAK_ROWS.read_bytes()
    except OSError:
        return None
    return value.encode("utf-8") in blob


def probe_key_rotation() -> tuple[str, str]:
    """ZAI_Pro rotation: closed when the live .env value no longer matches the
    leaked history copy (the operator replaced it), or by close receipt."""
    marker_state, marker_note = probe_marker(GATE_BY_SLUG["key-rotation"])
    value = _live_env_value()
    if value is None:
        return marker_state, f"{marker_note}; live .env value unreadable, byte check skipped"
    still_leaked = _leaked_rows_carry(value)
    if still_leaked is True:
        return "OPEN", (
            "live ZAI_API_KEY_Pro value still byte-present in the on-disk "
            "leak copy memory/trajectory/steps.jsonl (unrotated, checked this run)"
        )
    if still_leaked is False:
        return "CLOSED", (
            "live value matches no leaked on-disk row (rotated or scrubbed)"
        )
    return marker_state, f"{marker_note}; leak copy unreadable, byte check skipped"


# ---------------------------------------------------------------- the gates

GATES: list[Gate] = [
    Gate(
        slug="adam-invite",
        name="Adam invite to the-mountain (no GitHub username)",
        why=(
            "No GitHub username for Adam exists in the estate; both handle guesses "
            "(AdamCrigler, ItsCommodore) 404. An invite to a guessed handle would "
            "grant a possible stranger push access. Onboarding lineage since 09-24."
        ),
        action=(
            "Ask Adam on Discord (ItsCommodore) for his GitHub username, verify it "
            "(gh api users/NAME), then: gh api -X PUT repos/NachoBusiness17/"
            "the-mountain/collaborators/NAME -f permission=push"
        ),
        receipts=[
            "watch/inbox/last_mile_20260930/LW2_ADAM_INVITE.md",
            "watch/inbox/ADAM_ONBOARDING_FULL_20260924.md",
        ],
        probe=lambda: probe_marker(GATE_BY_SLUG["adam-invite"]),
    ),
    Gate(
        slug="nous-portal",
        name="Nous portal check (402s vs ~$171 rib arithmetic)",
        why=(
            "Prime models 402 on reservation while ribs say ~$171 of the $180/$220 "
            "pool should remain; the API has no balance endpoint. Only the portal "
            "separates old-account-402 from a genuinely dry pool."
        ),
        action=(
            "Log into portal.nousresearch.com, read credits + top-up history for "
            "BOTH key pairs (repo .env pair, old SDD/NACHO pair) against the "
            "COST_TRUTH section 4 table; top up if dry"
        ),
        receipts=[
            "watch/inbox/last_mile_20260930/AJ9_NOUS_402.md",
            "watch/inbox/COST_TRUTH_20260930.md",
        ],
        probe=lambda: probe_marker(GATE_BY_SLUG["nous-portal"]),
    ),
    Gate(
        slug="key-rotation",
        name="ZAI_Pro key rotation (rides with the other 6 leaked keys)",
        why=(
            "Seven live keys, incl. ZAI_API_KEY_Pro, were exposed in the "
            "steps.jsonl leak (audit finding #1); the on-disk leak copy "
            "persists and the backup repo holds copies. AG1 containment "
            "(untrack, redaction, pre-commit gate) protects future rows only; "
            "provider-side rotation is the operator-only real fix."
        ),
        action=(
            "Rotate ZAI_API_KEY_Pro at the provider console and replace the value "
            "in .env; same for ALIBABA x2, VERCEL_KEY, HERMES x1/2, GROQ "
            "(audit finding #1)"
        ),
        receipts=[
            "watch/inbox/last_mile_20260930/AG1_SECRETS_CONTAINMENT.md",
            "watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md",
        ],
        probe=probe_key_rotation,
    ),
    Gate(
        slug="phase2-lensing-go",
        name="Phase-2 lensing GO",
        why=(
            "Operator GO word for the Phase-2 lensing ask. Satisfied: the lensing "
            "fired and the return landed. Kept visible as the closure record."
        ),
        action="None (closed); read watch/inbox/mountain_climb/THE_LENSING.md",
        receipts=["watch/inbox/mountain_climb/THE_LENSING.md"],
        probe=probe_lensing,
    ),
    Gate(
        slug="verkle-v2-flip",
        name="Verkle v2 flip (chain_mode v1 to v2)",
        why=(
            "GO recommended (471x to 1,800x less write amplification); all three "
            "preconditions landed green (B8: compaction guard, reader dedupe, "
            "AH19 family). Waiting on the operator's quiet window; never mid-day."
        ),
        action=(
            "At the next quiet window run VERKLE_V2_DECISION section 4 recipe: "
            "pre-flip seal, flip configs/mag.yaml chain_mode to v2, one real "
            "save, post-flip seal, addendum filled"
        ),
        receipts=[
            "watch/inbox/VERKLE_V2_DECISION.md",
            "watch/inbox/last_mile_20260930/B8_V2_PRECONDS.md",
        ],
        probe=probe_verkle_v2,
    ),
    Gate(
        slug="offsite-medium",
        name="Offsite backup medium pick",
        why=(
            "Design + script complete (restic, scripts/backup_offsite.ps1), no "
            "medium chosen. One disk holds the estate, its only remote, and the "
            "gitignored truth core; audit row 18 FAIL stands until a restore "
            "passes."
        ),
        action=(
            "Pick ONE medium (B USB SSD ~$70-110 / C laptop over Tailscale, $0, "
            "off-machine today / D Backblaze B2, cents per month; OFFSITE plan "
            "section 4) and run the 3 commands in section 7"
        ),
        receipts=["watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md"],
        probe=lambda: probe_marker(GATE_BY_SLUG["offsite-medium"]),
    ),
]

GATE_BY_SLUG = {g.slug: g for g in GATES}


# ---------------------------------------------------------------- scan + render

def age_str(birth: Path) -> str:
    if not birth.is_file():
        return "?"
    delta = datetime.now() - _mtime(birth)
    return f"{delta.days}d {delta.seconds // 3600}h"


def scan() -> list[dict]:
    rows = []
    for gate in GATES:
        state, note = ("OPEN", "probe unset") if gate.probe is None else gate.probe()
        rows.append({
            "gate": gate,
            "state": state,
            "note": note,
            "age": age_str(gate.birth_path()) if state == "OPEN" else "-",
        })
    rows.sort(key=lambda r: (r["state"] != "OPEN", r["gate"].slug))
    return rows


def render(rows: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    open_rows = [r for r in rows if r["state"] == "OPEN"]
    closed_rows = [r for r in rows if r["state"] == "CLOSED"]
    oldest = min(open_rows, key=lambda r: r["gate"].birth_path().stat().st_mtime) \
        if open_rows else None
    head = (
        f"OPEN {len(open_rows)} / CLOSED {len(closed_rows)}"
        + (f". Oldest open: {oldest['gate'].name} ({oldest['age']})" if oldest else ".")
    )
    out = [
        "# GATE DIGEST: operator gates at one glance",
        "",
        f"Generated {now} by `tools/gate_digest.py` (byte scan of receipts, mtimes,",
        "configs; never hand-edit this file, regenerate it).",
        "",
        f"**{head}**",
        "",
        "## Open gates (each row is ONE operator action)",
        "",
        "| # | Gate | Open for | Why blocked | The ONE action | Birth receipt |",
        "|---|------|----------|-------------|----------------|---------------|",
    ]
    for i, r in enumerate(open_rows, 1):
        g = r["gate"]
        out.append(
            f"| {i} | {g.name} | {r['age']} | {g.why} | {g.action} | `{g.receipts[0]}` |"
        )
    out += [
        "",
        "## Closed (kept visible)",
        "",
        "| Gate | How it closed |",
        "|------|---------------|",
    ]
    for r in closed_rows:
        out.append(f"| {r['gate'].name} | {r['note']} |")
    out += [
        "",
        "## Live byte checks run this pass",
        "",
    ]
    for r in rows:
        out.append(f"- {r['gate'].slug}: {r['state']} ({r['note']})")
    out += [
        "",
        "## How a row closes (the law)",
        "",
        "1. Byte probe flips it (config flag read, leaked-value match, landed",
        "   return file). No human filing needed.",
        "2. A receipt lands: any .md under watch/inbox, NEWER than the gate's",
        "   birth receipt, containing the line `GATE-CLOSED: <slug>` with the",
        f"   slug from this table: {', '.join(g.slug for g in GATES)}.",
        "",
        "Days-open is anchored to each birth receipt's file mtime (named per",
        "row). Counts are snapshots of one scan moment (census denominator law).",
        "",
    ]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--stdout-only", action="store_true",
                    help="print the digest, do not write GATE_DIGEST.md")
    args = ap.parse_args(argv)

    rows = scan()
    text = render(rows)
    if not args.stdout_only:
        DIGEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        DIGEST_PATH.write_text(text, encoding="utf-8", newline="\n")

    open_rows = [r for r in rows if r["state"] == "OPEN"]
    for r in open_rows:
        g = r["gate"]
        print(f"OPEN  {r['age']:>6}  {g.name}  [{g.slug}]")
        print(f"      action: {g.action}")
    for r in rows:
        if r["state"] == "CLOSED":
            print(f"CLOSED       {r['gate'].name}  ({r['note']})")
    if not args.stdout_only:
        print(f"\nwrote {DIGEST_PATH.relative_to(ESTATE_ROOT).as_posix()}")
    print(f"open gates: {len(open_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
