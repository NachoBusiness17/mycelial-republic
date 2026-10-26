"""B2-51 close: append the LEDGER row (json.dumps, no heredoc) + self-feed QUEUE briefs."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BURN = ROOT / "watch" / "inbox" / "burn_wave_20260926"

row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-51-autorun-autopsy",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_51_autorun_autopsy_20260926.md",
    "one_line": (
        "governor_autorun autopsy (owed 9/19) run from bytes: the 9/19 17:31Z loop was a false "
        "crash-loop, DOCKER_ONLY marker (created 8/30 22:56 -0400, renamed stale 9/22) plus the "
        "9/14 child self-block (d575bc168) made every host spawn print '[autorun] blocked' and "
        "exit while pre-gate reap() classified it a crash: 28 auto_restarts on 9/19 (final four "
        "17:30:39/46, 17:31:02/17Z; the brief's 4x was the tail), 9 on 9/14, 44 on 9/16, 232 "
        "consecutive blocked lines at supervisor_autorun.out.log:5477-5708; the 9/19 21:58Z gate "
        "(96b5f4b4e) landed after self-resolution, never fired (0 policy_blocked rows), and its "
        "fix comment carried two false evidence claims ('5,708 blocked lines' was the streak's "
        "last line number misread as a count, actual 232; 'crashed 20 days' unsupported, 0 "
        "autorun rows 9/1-9/13 with thousands of daily reaper rows proving the reaper ran); "
        "design fix: the triplicated policy consolidated to ONE predicate in new "
        "mag/runtime_policy.py now imported by governor_autorun + ghost + process_supervisor "
        "(the copies had drifted: children gated os.name==nt, the supervisor gate did not), "
        "false-evidence comments replaced with the corrected receipt, alignment test "
        "test_policy_gate_matches_child_predicate added; verified 11+32 pytest passed, ratchet "
        "check --changed PASS NEW=0, live repro shows a 0.00s policy exit and gate/child "
        "agreement flipping with the marker, carrier pid 5240 restarted 13:07:52Z healthy on "
        "the new code with zero import errors; unknowns named not papered: why 37172 survived "
        "13h under a live marker (MAG_ALLOW_HOST_RUNTIME env of a dead process unrecorded), and "
        "the 232-vs-84 spawn-source delta (briefs B2-150/151 filed)"
    ),
}
ledger = ROOT / "memory" / "burns" / "LEDGER.jsonl"
with ledger.open("a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("ledger rows appended")

briefs = [
    "- [ ] B2-150 Reconcile the 232-vs-84 blocked-line delta: supervisor_autorun.out.log:5477-5708 "
    "holds 232 consecutive '[autorun] blocked' lines but supervisor.jsonl logged only 84 autorun "
    "starts across 9/14+9/16+9/19; name the extra spawn sources that share the slot log without "
    "supervisor rows (detached relauncher, mag_launch slot, manual -c runs) from queue/handoff + "
    "orchestrator logs, or file the source map as unknown with evidence; pointers "
    "logs/autorun_detached.log + watch/inbox/burn_wave_20260926/B2_51_autorun_autopsy_20260926.md.",
    "- [ ] B2-151 Close the pid 37172 survivor unknown: the 9/19 17:31:17Z autorun spawn ran ~13h "
    "(stopped 9/20 06:04:36Z) while the DOCKER_ONLY marker existed to the 9/22 rename; find the "
    "survival mechanism (MAG_ALLOW_HOST_RUNTIME in the supervisor's env, brief marker absence, or "
    "another carrier) from orchestrator t*.out.log, mag_launch state, and 9/19 agent_sessions, "
    "falsifiable outcome only, never synthesize; pointer B2_51 receipt Falsifier.",
]
queue = BURN / "QUEUE.md"
text = queue.read_text(encoding="utf-8")
for b in briefs:
    tag = b.split(" ")[2]
    assert f"- [ ] {tag}" not in text, f"number already claimed: {tag}"
with queue.open("a", encoding="utf-8") as f:
    for b in briefs:
        f.write(b + "\n")
print("queue briefs appended:", [b.split(" ")[2] for b in briefs])
