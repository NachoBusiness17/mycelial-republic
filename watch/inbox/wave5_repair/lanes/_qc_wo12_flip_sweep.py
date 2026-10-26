"""queue-closes lane instrument: WO-12 bookkeeping flip sweep over queue/todo.md.

Spec: watch/inbox/burn_reset_20260927/flash50/sess-02.md WO-12. Safety model:
(1) pre-edit recount must read UNCHECKED 63; (2) every flip is keyed on line
number AND an expected content snippet, so any live-tree drift aborts the
sweep instead of flipping the wrong row; (3) insertions run after flips,
bottom-up, so line numbers stay stable through the edit; (4) post-edit
recount is printed with the surviving unchecked lines. The file stays
untracked (gitignored) per WO-12 criterion 6.

Deviations from the bare "51 flips, 12 untouched" shape, both documented in
watch/inbox/wave5_repair/queue-closes.md:
- line 232 flips because WO-10 completed in this lane (its own criteria:
  flip once the rebuild verb lands and validate is green on its axes);
- lines 235 + 237 flip as MERGED into the WO-12(3) re-seeded Stone 5 line
  (leaving both open next to the merged line would triplicate the item).

Run: .venv/Scripts/python.exe _qc_wo12_flip_sweep.py apply
     (no arg = dry: recounts + asserts only, no writes)
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
TODO = REPO / "queue" / "todo.md"

CLOSE = ">> CLOSED 2026-09-29 queue-closes WO-12: "

# line_no -> (expected snippet somewhere in the line, pointer appended)
FLIPS: dict[int, tuple[str, str]] = {
    5: ("Cerebras lane", "DECIDED PARKED inline 2026-09-26 (header + this line); sess-02 sB MINE (configs/providers.yaml cerebras dormant block 694-704)"),
    32: ("Auto-promote gate", "Q-002 (watch/inbox/burn_reset_20260927/queue/Q-002.md); tools/auto_promote.py + tests/test_auto_promote.py on disk (sess-02 sB MINE)"),
    33: ("Session cards", "Q-003 (queue/Q-003.md); memory/biography/cards/ holds 15 .card.json (sess-02 sB MINE)"),
    98: ("Review memory/attention.md when Mag pings", "Q-005 (queue/Q-005.md) 127 pings triaged 2026-09-28; writer mag/biography.py:509-515; habit line NOT re-seeded (operator ruling on the ritual not given)"),
    104: ("hand-annotate more chord/refusal/rope rows", "Q-007 (queue/Q-007.md) 11 rows banked (RECEIPT-SIDE)"),
    126: ("Spider is blind but FKB has clear failure patterns", "Q-008 (queue/Q-008.md) thresholds fixed, suite green (QREAD)"),
    127: ("eat comms_trail consumption into routing", "carried since checkpoint d575bc168; mag/comms_trail.py:223 comms_consumption.v1 (sess-02 sB MINE)"),
    129: ("derived DAG index over existing hashes", "Q-010 (queue/Q-010.md); tools/derived_dag.py 16,221B + memory/derived/derived_dag_index.json 30,772,308B (sess-02 sB MINE)"),
    130: ("Huang gate", "Q-011 (queue/Q-011.md); mag/frontier_salon.py:180 roundtable(why, baseline) (sess-02 sB MINE)"),
    135: ("Astra bundle", "SUPERSEDED inline by line 133 (FW-37..49 re-seed) + Q-021 dead-path verify"),
    136: ("Retro-knotter", "SUPERSEDED inline by line 133 + Q-021"),
    137: ("Small fixes: janitor phantom", "SUPERSEDED inline by line 133 + Q-021"),
    138: ("Game: run mud51 gate", "SUPERSEDED inline by line 133 + Q-021"),
    139: ("Estate: vislab health", "SUPERSEDED inline by line 133 + Q-021"),
    140: ("Memory/doctrine: 632 unindexed triage memo", "SUPERSEDED inline by line 133 + Q-021"),
    141: ("Research: recursion crosswalk", "SUPERSEDED inline by line 133 + Q-021"),
    142: ("Ops: drift check, providers re-probe", "SUPERSEDED inline by line 133 + Q-021"),
    146: ("A. Morning verification wave", "Q-020 (queue/Q-020.md) + FW01..05 per-item receipts dir-listed"),
    147: ("B. Census debt", "Q-021 (queue/Q-021.md)"),
    148: ("C. Tide machinery", "Q-022 (queue/Q-022.md) + Q-022_tide_prompt_v1_baseline.txt dir-listed"),
    149: ("D. Patrol debt", "Q-023 (queue/Q-023.md)"),
    151: ("F. Operator gate packets", "Q-025 (queue/Q-025.md)"),
    152: ("G. Wave stones", "Q-026 (queue/Q-026.md)"),
    153: ("H. Game estate", "Q-027 (queue/Q-027.md) + FW38..42 per-item files dir-listed"),
    160: ("Land scanner v3", "LANDED: mag/catalog_rebuild.py:1 idempotent catalog rebuild v3 (sess-02 sB MINE)"),
    161: ("Catalog freshness budget", "LANDED: mag/catalog_rescan.py + mag/catalog_freshness.py + catalog/catalog_fts.sqlite 161,345,536B (sess-02 sB MINE)"),
    162: ("Tags v2 owner column", "Q-031 (queue/Q-031.md); mag/catalog_tags.py:27-31 owner field (sess-02 sB MINE)"),
    194: ("Swarm", "games wave + Q-037 input wiring; roblox/src/server/SwarmZone.luau 14,782B (sess-02 sB MINE)"),
    195: ("Comparative audit", "Q-033 (queue/Q-033.md) (QREAD)"),
    196: ("First video-input burn", "Q-034 (queue/Q-034.md) bison.mp4 through stealth/space-bunny-alpha (QREAD)"),
    197: ("mirrors.json", "configs/mirrors.json 468B + tools/stealth_driver.py:67 MIRRORS, :605-607 per-host diff (sess-02 sB MINE)"),
    198: ("Reasoning-effort dial policy", "Q-036 (queue/Q-036.md) (RECEIPT-SIDE)"),
    203: ("Client pass: chat remotes", "Q-037 (queue/Q-037.md) (RECEIPT-SIDE)"),
    218: ("Public gateway host", "Q-039 (queue/Q-039.md) non-localhost bind + shared-secret + proof (RECEIPT-SIDE)"),
    223: ("v1.1 client polish", "Q-040 (queue/Q-040.md) (RECEIPT-SIDE)"),
    224: ("Leaderstats page", "Q-041 (queue/Q-041.md) (RECEIPT-SIDE)"),
    225: ("Pet orb model + trail", "Q-042 (queue/Q-042.md) (RECEIPT-SIDE)"),
    232: ("shared_surface INDEX fold rebuild still OWED", "WO-10 CLOSED THIS LANE 2026-09-29: rebuild verb mag/surface_rebuild.py (python -m mag.shared_surface rebuild [--dry] and mag.cmd surface-rebuild) + tests/test_surface_rebuild.py 3 passed; production passes 1-4, truly-invisible 93 -> 0, stale 28 -> 0, missing 5 -> 0 at census; validate residual = sibling live-append races only; receipt watch/inbox/wave5_repair/queue-closes.md"),
    244: ("Polish backlog from wave zones", "Q-043 (queue/Q-043.md) all three landed (RECEIPT-SIDE)"),
    249: ("Fold owed: sphere kinship graph", "FOLDED 2026-09-25 inline (SphereKinship/DfValue/Temptation/ProceduralBody .luau on disk, sess-02 sB MINE); residuals re-seeded as own line below"),
    254: ("play-as-work v4.0 citation layer", "RESOLVED by v6 master inline UPDATE (line 257); watch/inbox/play_as_work_20260926/VERIFICATION_v6_20260926.md (sess-02 sB MINE)"),
    255: ("factorioctl lane go/no-go", "SUPERSEDED into U1 substrate decision (line 257 UPDATE; substrate line 261 checked inline)"),
    262: ("SESSION_HANDOFF_20260926_noir_u1_gates", "CONSUMED: ../fle_u1/.fle/inspect_logs/2026-09-27T11-56-56 iron-plate-throughput eval postdates handoff (sess-02 sB MINE)"),
    266: ("Thought Quantizer v0.3", "memory/corpus/quantized_thought/compile_report.json v0.3 compiled 2026-09-28T16:19:05Z with the two-pass over-refuse fix (sess-02 sB MINE)"),
    267: ("Gene-pool audit regenerator, or tombstone", "TOMBSTONED: GENE_POOL_TOMBSTONE_20260927.md + mag/gene_pool_feeder.py:3-4 (sess-02 sB MINE)"),
    268: ("FOSSIL-IN-FEED law teeth", "tools/fossil_check.py WARN-only freshness arm + configs/fossil_registry.json, wired into the 08:30 census patrol (sess-02 sB MINE)"),
    272: ("Loop 3 verkle_knot", "dirac closure class: watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl exactly 6 rows + sess-02 rerun 2026-09-28T23:43:14Z closed_solved=6 open_gaps=0"),
    273: ("Loop 1 context_pack", "dirac closed: BANKED_INVARIANTS 6 rows + sess-02 rerun closed_solved=6 open_gaps=0"),
    274: ("Loop 2 context_checkpoint", "dirac closed: BANKED_INVARIANTS 6 rows + sess-02 rerun closed_solved=6 open_gaps=0"),
    275: ("Loops 4+5 context_admission", "dirac closed: BANKED_INVARIANTS 6 rows + sess-02 rerun closed_solved=6 open_gaps=0"),
    276: ("Loop 6 water_computer", "dirac closed: BANKED_INVARIANTS 6 rows + sess-02 rerun closed_solved=6 open_gaps=0"),
    277: ("Structural: scan() can never report", "dirac structural complaint answered in behavior: BANKED_INVARIANTS 6 rows + sess-02 rerun closed_solved=6 open_gaps=0"),
    # merge flips (deviation documented in the receipt)
    235: ("Stone 5 (Grok, pre-Sunday): packet FILED", "MERGED 2026-09-29 WO-12 into the re-seeded Stone 5 line below per WO-8 (same item twice; execution still OWED)"),
    237: ("Stone 5 (Grok, pre-Sunday): adversarial pass", "MERGED 2026-09-29 WO-12 into the re-seeded Stone 5 line below per WO-8 (same item twice; execution still OWED)"),
}

# (anchor_line, snippet, new_line_text) - applied bottom-up after flips
INSERTS = [
    (249, "Fold owed: sphere kinship graph",
     "- [ ] [mag] DF fold residuals (re-seeded 2026-09-29 WO-12 from the line above): "
     "supernatural villain plots, per-class attack triggers beyond scorpion-force, "
     "Ages of Powers branch (bundle already landed: SphereKinship/DfValue/Temptation/"
     "ProceduralBody .luau)."),
    (237, "Stone 5 (Grok, pre-Sunday): adversarial pass",
     "- [ ] [mag] Stone 5 Grok asks, MERGED single line (re-seeded 2026-09-29 WO-12 per WO-8; "
     "kills the lines-235+237 duplicate): 4 asks (prereg adversarial falsifier pass, W4 rerun "
     "design review, October reading list, BURN_* filings audit); lane ruling OWED per "
     "DRIVING LADDER (asks 1-3 to FUNDED, ask 4 repo-byte audit gopher LOCAL); packets "
     "watch/inbox/GROK_LANE_PACKET_20260925.md + watch/inbox/GROK_ASK4_SCOPE_FREEZE_20260926.md."),
]


def unchecked(lines: list[str]) -> list[tuple[int, str]]:
    return [(i + 1, l) for i, l in enumerate(lines) if l.startswith("- [ ]")]


def main() -> int:
    apply = "apply" in sys.argv
    raw = io.open(TODO, "rb").read().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(eol)
    if lines and lines[-1] == "":
        lines = lines[:-1]  # trailing newline handled at write
    pre = unchecked(lines)
    print(f"PRE-EDIT UNCHECKED {len(pre)} (eol={'CRLF' if eol == chr(13) + chr(10) else 'LF'})")
    if len(pre) != 63:
        print("ABORT: expected 63 unchecked (drift law); no edits made")
        return 2
    pre_lines = {n for n, _ in pre}
    missing = sorted(set(FLIPS) - pre_lines)
    if missing:
        print(f"ABORT: flip lines not unchecked at recount: {missing}")
        return 2
    for n, (snippet, _) in sorted(FLIPS.items()):
        if snippet not in lines[n - 1]:
            print(f"ABORT: line {n} snippet mismatch: expected {snippet!r} in {lines[n - 1][:90]!r}")
            return 2
    for anchor, snippet, _ in INSERTS:
        if snippet not in lines[anchor - 1]:
            print(f"ABORT: insert anchor {anchor} snippet mismatch")
            return 2
    print(f"asserts ok: {len(FLIPS)} flips + {len(INSERTS)} inserts keyed on live bytes")
    if not apply:
        print("DRY: no writes")
        return 0
    for n, (_, pointer) in sorted(FLIPS.items()):
        line = lines[n - 1]
        lines[n - 1] = "- [x]" + line[5:] + " " + CLOSE + pointer
    for anchor, _, new_line in sorted(INSERTS, key=lambda t: -t[0]):
        lines.insert(anchor, new_line)  # after the anchor line (0-based index == anchor)
    io.open(TODO, "w", encoding="utf-8", newline="").write(eol.join(lines) + eol)
    post = unchecked(io.open(TODO, encoding="utf-8").read().splitlines())
    print(f"POST-EDIT UNCHECKED {len(post)}")
    for n, l in post:
        print(f"  {n} {l[:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
