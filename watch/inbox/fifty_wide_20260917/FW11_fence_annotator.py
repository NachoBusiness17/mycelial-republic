"""FW-11 fence annotator (2026-09-28, fifty_wide_20260917).

Assigns owner or SUPERSEDED markers to the 30 launcher-shaped fences the
2026-09-17 prose census flagged (watch/PROSE_CENSUS_20260917.md, "Launcher-shaped
fences" section). Idempotence: NOT idempotent — markers are inserted after the
opening fence line; running twice would double them. Already run once; kept for
reproducibility of the exact transform.

Marker kinds:
- owner: `# fence-owner: <who> — <why>` inside the fence. Recognized by
  mag/prose_census.py _FENCE_OWNER_RE (added same day) so owned standing
  launchers clear the census flag, per the module's documented "SUPERSEDED/owner
  marker" contract.
- super: `# SUPERSEDED (FW-11 ...)` for one-shot receipt commands already
  executed; do not re-run from prose.

Receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
"""

from collections import defaultdict
from pathlib import Path

OWNER = "watch/inbox/fifty_wide_20260917/FW11_fence_owners.md"

# (file, fence_index_1based, kind, owner_or_reason, orig_date)
TARGETS = [
    ("RUNNING.md", 1, "owner", "operator - standing container daemon start (mag-sovereign lane runner)", None),
    ("AGENTS.md", 2, "owner", "operator - harness command card (AGENTS.md Commands section)", None),
    ("README.md", 1, "owner", "operator - README quickstart card", None),
    ("README.md", 2, "owner", "operator - README quickstart card", None),
    ("README.md", 3, "owner", "operator - README goal-run card", None),
    ("README.md", 4, "owner", "operator - README command card", None),
    ("README.md", 5, "owner", "operator - README models card", None),
    ("README.md", 6, "owner", "operator - README research-pack card", None),
    ("README.md", 7, "owner", "operator - README dispatch card", None),
    ("README.md", 8, "owner", "operator - README scaffold card", None),
    ("HANDOFF_MAG_AGENT_TODOS.md", 1, "owner", "implementing agent - handoff boot card", None),
    ("HANDOFF_MAG_AGENT_TODOS.md", 2, "owner", "implementing agent - improve cycle card", None),
    ("HANDOFF_MAG_AGENT_TODOS.md", 3, "owner", "implementing agent - test suite card", None),
    ("HANDOFF_MAG_AGENT_TODOS.md", 4, "owner", "implementing agent - context-pack card", None),
    ("HANDOFF_MAG_AGENT_TODOS.md", 5, "owner", "implementing agent - context-pack numbered card", None),
    ("watch/AUDIT_B_ELDER_20260901.md", 1, "super", "one-shot elder-audit staging, executed 2026-09-01, receipt filed", "2026-09-01"),
    ("watch/AUDIT_C_VERKLE_20260901.md", 1, "super", "one-shot verkle health check, executed 2026-09-01", "2026-09-01"),
    ("watch/CLAIM_REPAIR_V0_20260905.md", 1, "super", "v0 proof commands, executed 2026-09-05 (FINDING 2 closed at v0)", "2026-09-05"),
    ("watch/FALSIFIER_LEDGER_AUDIT_GUIDE_20260912.md", 1, "owner", "falsifier-lane auditor - guide command, meant to be re-run per the guide", None),
    ("watch/FLEET_AUDIT_20260901.md", 1, "super", "mag.openclaw_patches apply, executed 2026-09-01", "2026-09-01"),
    ("watch/KNOT_BRIDGE_20260906.md", 1, "super", "one-shot 2026-09-06 backfill; mag/zcode_export.py since deleted - do not re-run", "2026-09-06"),
    ("watch/LANE_AUTOMATION_SPECS_20260904.md", 2, "owner", "builder-lane spec - lane prompt card (spec text, not a shell launcher)", None),
    ("watch/MAIN_CHANNEL_CONTRACT_20260901.md", 2, "owner", "supervisor - main-channel contract ops card", None),
    ("watch/STEERING_SYNTHESIS_20260901.md", 3, "super", "one-shot verkle_lance link example, 2026-09-01", "2026-09-01"),
    ("watch/inbox/GAP1_SPAWN_MANIFEST_20260906.md", 1, "owner", "spawn-manifest tool users - live CLI usage card (mag/spawn_manifest.py exists)", None),
    ("watch/inbox/REVEAL_FIVE_REHEARSALS_20260906.md", 1, "owner", "operator - power-loss restore runbook, kept deliberately", None),
    ("watch/inbox/REVEAL_FIVE_REHEARSALS_20260906.md", 2, "owner", "operator - documented how-to-run-again pattern, kept deliberately", None),
    ("watch/inbox/SEAT_SPORes_AUDIT_CELL_20260912.md", 1, "super", "one-shot verkle_audit cell check, executed 2026-09-12", "2026-09-12"),
    ("watch/inbox/SELF_STEAL_REBUILD_RETEST_SALON_20260831.md", 4, "super", "one-shot salon step (cartridge read), 2026-08-31", "2026-08-31"),
    ("watch/inbox/SELF_STEAL_REBUILD_RETEST_SALON_20260831.md", 8, "super", "one-shot orphan_audit batch, 2026-08-31", "2026-08-31"),
]


def main() -> None:
    byfile: dict[str, list] = defaultdict(list)
    for f, i, kind, why, od in TARGETS:
        byfile[f].append((i, kind, why, od))

    for f, items in byfile.items():
        p = Path(f)
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        fence = 0
        open_at: dict[int, int] = {}
        inside = False
        for pos, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                if not inside:
                    fence += 1
                    open_at[fence] = pos
                    inside = True
                else:
                    inside = False
        for idx, kind, why, od in items:
            if idx not in open_at:
                print(f"!! {f}#fence{idx}: no such fence opening (total {fence})")
                continue
            pos = open_at[idx]
            if kind == "owner":
                marker = f"# fence-owner: {why}. FW-11 2026-09-28; receipt: {OWNER}\n"
            else:
                marker = f"# SUPERSEDED (FW-11 2026-09-28): {why}. Do not re-run from prose. Receipt: {OWNER}\n"
            lines[pos] = lines[pos] + marker
        p.write_text("".join(lines), encoding="utf-8")
        print(f"annotated {f}: {len(items)} fences")


if __name__ == "__main__":
    main()
