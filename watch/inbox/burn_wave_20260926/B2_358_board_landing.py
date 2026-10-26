"""B2-358 board landing: retire claims, landing note, self-feeds (2026-09-26).

Targeted string surgery on QUEUE.md with an mtime guard: between read and
write the board is hot (concurrent lanes land every minute), so the script
re-reads and retries when the mtime moves. No whole-file rewrite semantics
beyond the single write of the mutated bytes; every anchor is unique text this
lane authored or the unique tail of the B2-358 brief row.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_358_env_tripwire_20260926.md"

CLAIMS_OLD_NEW = [
    (
        "- CLAIM B2-358 mag/doctor.py 2026-09-26T17:23:03Z (B2-358 env tripwire: check_env_sanity MAG_SEAT_CRASH_LOG/MAG_GAPS_LOG warning row plus report field only; re-read bytes before your edit per the claim law)",
        "- CLAIMED B2-358 mag/doctor.py 2026-09-26T17:23:03Z (B2-358 env tripwire: check_env_sanity MAG_SEAT_CRASH_LOG/MAG_GAPS_LOG warning row plus report field only; re-read bytes before your edit per the claim law) -> " + RECEIPT,
    ),
    (
        "- CLAIM B2-358 mag/shared_surface.py 2026-09-26T17:23:03Z (B2-358 env tripwire: validate warning line for the same two vars only; re-read bytes before your edit per the claim law)",
        "- CLAIMED B2-358 mag/shared_surface.py 2026-09-26T17:23:03Z (B2-358 env tripwire: validate warning line for the same two vars only; re-read bytes before your edit per the claim law; rebased mid-lane on the concurrent B2-342 growth, anchored blocks intact, rebase named in the receipt) -> " + RECEIPT,
    ),
    (
        "- CLAIM B2-358 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T17:23:03Z (lane's own board: claim lines, B2-358 landing note, self-feed briefs; foreign CLAIMs honored, anchored edits on freshly-read bytes, no whole-file rewrite)",
        "- CLAIMED B2-358 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T17:23:03Z (lane's own board: claim lines, B2-358 landing note, self-feed briefs; foreign CLAIMs honored, anchored edits on freshly-read bytes, no whole-file rewrite) -> " + RECEIPT,
    ),
]

ROW_TAIL_OLD = "watch/inbox/burn_wave_20260926/B2_79_pollution_fix_20260926.md."
ROW_TAIL_NEW = (
    "watch/inbox/burn_wave_20260926/B2_79_pollution_fix_20260926.md."
    " Landed 2026-09-26 (row sat pre-checked [x] from its B2-86 self-feed with"
    " no receipt, the B2-238 disease; this landing earns the check): new"
    " mag/env_redirect.py (REDIRECT_VARS table, OPERATOR_RESPONSE,"
    " env_redirect_status, env_redirect_warnings) wired into both surfaces:"
    " mag/doctor.py check_env_sanity returns a redirect_warnings row (ok"
    " semantics unchanged) and examine() aggregates it into report.warnings;"
    " mag.shared_surface validate extends its warnings with the same"
    " ENV-REDIRECT lines naming the variable, the redirect target and the"
    " operator response (warning, never an error). Design decision measured"
    " live: the first cut suppressed on PYTEST_CURRENT_TEST and the pins caught"
    " pytest re-setting that marker at every phase transition, so the warning"
    " fires unconditionally and status keeps in_test_run informational only."
    " Falsifier executed live 17:35Z on a plain shell:"
    " MAG_SEAT_CRASH_LOG pointed at"
    " agents/env_tripwire_falsifier/stray_seat_crash.log, one real RuntimeError"
    " through _log_seat_crash landed its traceback in that stray file, validate"
    " named the var, the target and the response; clean direction zero"
    " ENV-REDIRECT lines; production logs byte-still (logs/seat_crashes.log"
    " 322668 bytes, memory/training/loop_gaps.jsonl 103301 bytes, before and"
    " after). Pins tests/test_env_redirect_tripwire.py 10 passed; neighbor"
    " suites (temperature_stack, shared_surface_events, doctor provider,"
    " doctor scheduled) 52 passed. Ratchet first FAIL NEW=1 file-too-long"
    " mag/shared_surface.py:447 (fingerprint 198edd83211b76e1): growth measured"
    " on bytes (157 at HEAD, 311 at this lane's claim-read, 447 to 456 by"
    " close; the concurrent B2-342 landing plus this lane's +22 lines,"
    " 311+22=333 under the cap; the B2-357 receipt independently names the hit"
    " as this lane's in-flight edit), debt accepted by name as the bridge per"
    " the B2-248 precedent, register 875 to 876, re-check PASS NEW=0, split"
    " self-fed below. Em-dash count 0 on added lines. Self-fed B2-381, B2-382,"
    " B2-383 UNCHECKED (first drafted B2-378/379/380, numbers taken by the"
    " concurrent B2-354 and B2-342 self-feeds mid-lane, renumbered highest+1"
    " per the B2-167 law); receipt " + RECEIPT + "."
)

SELF_FEEDS = """
- [ ] B2-381 Split mag/shared_surface.py back under the 400-line bar: (self-fed by B2-358) the module rode the ratchet at 447+ lines on 2026-09-26 (157 at HEAD, 311 at the B2-358 claim-read, 447 to 456 by close after the B2-342 schema-registry landing and the B2-358 tripwire block), and B2-358 accepted the file-too-long debt as the bridge by name (fingerprint 198edd83211b76e1 in configs/violation_baseline.json, register 875 to 876, re-check PASS NEW=0); per the B2-248 precedent move a self-contained block (scan_events_log with its baseline loader, or the B2-156 living-item prefix loop) into a sibling module so the file sits under 400 lines, then prune the accepted claim per the ratchet law, never just silenced; falsifier: tools/violation_ratchet.py check --changed shows the claim pruned with the register back under 876 and the moved block's tests still green; pointers mag/shared_surface.py, configs/violation_baseline.json (accepted 198edd83211b76e1), watch/inbox/burn_wave_20260926/B2_248_module_split_20260926.md, watch/inbox/burn_wave_20260926/B2_358_env_tripwire_20260926.md Evidence.
- [ ] B2-382 mag.cmd doctor never runs the mag.doctor checks: (self-fed by B2-358) main.py doctor (the mag.cmd doctor path) prints mag.health.sanity plus mag.guard.doctor_print, while the mag/doctor.py check family (env sanity incl. the B2-358 env-redirect tripwire, provider sanity, inbox sanity, chain discipline) is reachable only as a library (doctor_agent.py, flex_test.py, api_gateway.py) or via tests, so the operator console command named doctor and the doctor surface carrying the tripwire are different programs and a leaked MAG_SEAT_CRASH_LOG never shows on mag.cmd doctor; wire at least check_env_sanity (cheap, env-only) into the main.py doctor output with the redirect warnings printed to the console, or register in AGENTS.md that the tripwire lives on python -m mag.shared_surface validate and the library doctor only; falsifier: MAG_SEAT_CRASH_LOG set in a plain shell, run mag.cmd doctor, and no output line names the redirect; pointers main.py doctor branch, mag/guard.py doctor_print, mag/doctor.py check_env_sanity, mag/env_redirect.py, watch/inbox/burn_wave_20260926/B2_358_env_tripwire_20260926.md.
- [ ] B2-383 Census the env-var write-path overrides in mag/: (self-fed by B2-358) REDIRECT_VARS (mag/env_redirect.py) covers exactly the two seams known on 2026-09-26 (MAG_SEAT_CRASH_LOG, MAG_GAPS_LOG), but no sweep ever enumerated which other os.environ reads in mag/ redirect a production write path (logs, jsonl ledgers, state snapshots), so the next isolation seam re-opens the silent-redirect class on a third variable; grep-census every env var that feeds a Path used for writing, classify each as redirect-seam (add to REDIRECT_VARS and the two warning surfaces), deliberate config (document, no warning), or read-only; falsifier: a new env-var write redirect added today appears in no table, no warning and no census row; pointers mag/env_redirect.py REDIRECT_VARS, mag/agent_cli.py _log_seat_crash, mag/temperature_stack.py _gaps_log, watch/inbox/burn_wave_20260926/B2_358_env_tripwire_20260926.md.
"""


def apply(text: str) -> str:
    for old, new in CLAIMS_OLD_NEW:
        if text.count(old) != 1:
            raise SystemExit(f"claim anchor not unique (count={text.count(old)}): {old[:80]}")
        text = text.replace(old, new)
    if text.count(ROW_TAIL_OLD) < 1:
        raise SystemExit("B2-358 row tail anchor missing")
    if "Landed 2026-09-26 (row sat pre-checked [x] from its B2-86 self-feed" in text:
        raise SystemExit("landing note already present; refusing to double-apply")
    # replace only the FIRST occurrence (the brief row); later copies of the
    # pointer in landing notes of other rows must stay untouched
    idx = text.find(ROW_TAIL_OLD)
    text = text[:idx] + ROW_TAIL_NEW + text[idx + len(ROW_TAIL_OLD):]
    if not text.endswith("\n"):
        text += "\n"
    text += SELF_FEEDS if text.endswith("\n\n") else ("\n" + SELF_FEEDS)
    return text


def main() -> int:
    for attempt in range(6):
        mtime_before = BOARD.stat().st_mtime_ns
        raw = BOARD.read_bytes()
        text = raw.decode("utf-8")
        if "Landed 2026-09-26 (row sat pre-checked [x] from its B2-86 self-feed" in text:
            print("already applied by a prior run; nothing to do")
            return 0
        new_text = apply(text)
        time.sleep(0.2)
        if BOARD.stat().st_mtime_ns != mtime_before:
            print(f"attempt {attempt}: board moved mid-edit, re-reading")
            continue
        BOARD.write_bytes(new_text.encode("utf-8"))
        print(f"board landing applied on attempt {attempt}: claims retired, landing note, 3 self-feeds")
        return 0
    print("FAILED: board too hot after 6 attempts; re-run this script")
    return 1


if __name__ == "__main__":
    sys.exit(main())
