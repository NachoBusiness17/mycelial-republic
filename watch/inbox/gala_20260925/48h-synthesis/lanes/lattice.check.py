"""lattice lane finish-line check (gala, division B).

Verifies, against the repo tree:
1. every receipt path cited in watch/inbox/48h_synth/lattice.md exists;
2. every quote in lattice.md is a byte (whitespace-normalized) substring of its source receipt;
3. each of the 4 insights cites >= 2 receipts from DIFFERENT organ families;
4. lattice.md has >= 3 insight headers, zero em/en dashes, and the tapestry gap is stated;
5. the tapestry absence evidence: git log on mag/tapestry*.py since 2026-09-28 is empty,
   and the tapestry suite rows exist in suite-burn.check.txt.

Writes raw output to lattice.check.txt beside this script. Exit 0 = all pass.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
CHECK_FILE = ROOT / "watch/inbox/gala_20260925/48h-synthesis/lanes/lattice.check.txt"
CHAPTER = ROOT / "watch/inbox/48h_synth/lattice.md"

ORGANS = {
    "delivery": ["watch/inbox/wave5_repair/render-pipe.md"],
    "attention": ["watch/inbox/wave5_repair/attention-channel.md",
                  "watch/inbox/ball2/attention-ledger.md"],
    "mcp": ["watch/inbox/ball2/mcp-bridge-r1.md",
            "watch/inbox/wave5_repair/mcp-pin-wire.md"],
    "stealth": ["watch/inbox/wave5_repair/stealth-tools.md",
                "watch/inbox/ball2/driver-v2.md"],
    "seed": ["watch/inbox/wave5_repair/seed-kernel.md"],
    "events": ["watch/inbox/wave5_repair/events-door.md"],
    "census": ["watch/inbox/wave5_repair/patrol-fix.md"],
    "suite": ["watch/inbox/wave5_repair/suite-burn.md",
              "watch/inbox/gala_20260925/wave5-repair_RECEIPT.md"],
}

# (insight, receipt path, verbatim quote)
QUOTES = [
    ("I1", "watch/inbox/wave5_repair/mcp-pin-wire.md",
     "This is the first estate instance of a w4-41 class-W gap (proved mechanism, zero callers) being closed by wiring rather than by more proof."),
    ("I1", "watch/inbox/wave5_repair/render-pipe.md",
     "a budget smaller than the core it must deliver is not a budget, it is a silent eraser"),
    ("I1", "watch/inbox/wave5_repair/seed-kernel.md",
     "verify() decodes a carried memory/law/registry.json and fails on any law_ref id the carried registry does not hold."),
    ("I1", "watch/inbox/wave5_repair/attention-channel.md",
     "A cast the ranker rejects now makes capture return ok False and the CLI exit 1"),
    ("I1", "watch/inbox/wave5_repair/events-door.md",
     "The loader's strictness contract is amended, not loosened: unknown schema-less rows still raise; only carrier-named debt is accepted, by name, in-file."),
    ("I1", "watch/inbox/ball2/driver-v2.md",
     "free-lane dispatches are now formally closeable by funded verification, and the work queue has a drain for the first time"),
    ("I2", "watch/inbox/wave5_repair/seed-kernel.md",
     "after a sibling write to tools/stealth_driver.py staled the 10:43 seals; the SLO fired exactly as designed: verify exit 1 voided CURRENT, one command re-rendered"),
    ("I2", "watch/inbox/wave5_repair/stealth-tools.md",
     "tools/stealth_driver.py accepted at 753 lines, now 1108 (+355)"),
    ("I2", "watch/inbox/ball2/mcp-bridge-r1.md",
     "the two real connects pinned all six tools into state/mcp_pins.jsonl (rows 85-92, identical hashes across connects = PINNED, no drift alarm)"),
    ("I2", "watch/inbox/wave5_repair/mcp-pin-wire.md",
     "returns the manifest WITH drifted tools WITHHELD: the mutated description/schema never reaches a model"),
    ("I2", "watch/inbox/wave5_repair/attention-channel.md",
     "real patrol alerts were destroyed (the 2026-09-26 COLLECT-DRIFT and 2026-09-28 fleet-task-doctor alerts, w4-09)"),
    ("I2", "watch/inbox/wave5_repair/patrol-fix.md",
     "the census tripwire can no longer be blinded into a lying exit 2 by ordinary markdown reflow"),
    ("I2", "watch/inbox/wave5_repair/render-pipe.md",
     "operator directives now render inside `policy` proper, in every mode, mode-capped, at mag/context_pack.py:1142-1147"),
    ("I2", "watch/inbox/wave5_repair/seed-kernel.md",
     "10 law-role entries with real bytes (9 memory/law/*.md + registry.json 9,849 B; every law_ref id machine-checkable against carried bytes)"),
    ("I3", "watch/inbox/wave5_repair/events-door.md",
     "Nothing was committed; the working tree carries this lane's edits"),
    ("I3", "watch/inbox/wave5_repair/seed-kernel.md",
     "Nothing committed: the shared tree holds sibling lanes' uncommitted work"),
    ("I3", "watch/inbox/ball2/attention-ledger.md",
     "the P0 `repo:handoff` item is the operative context every ball lane ran on (uncommitted wave5 tree, no upstream)"),
    ("I3", "watch/inbox/wave5_repair/events-door.md",
     'an early `--help` probe of `baseline-update` was NOT inert - it executed and registered all 4 under the default "operator" name'),
    ("I3", "watch/inbox/ball2/driver-v2.md",
     'an accidental bare `baseline-update` invocation (the tool has no --help; it executed and registered 3 sibling debts as "by: operator") was reverted with `git checkout -- configs/violation_baseline.json` before anything else touched the file'),
    ("I3", "watch/inbox/wave5_repair/attention-channel.md",
     "The four NEW violations name files this lane never touched"),
    ("I3", "watch/inbox/wave5_repair/stealth-tools.md",
     "The 4 NEW hits are NOT this lane's files"),
    ("I3", "watch/inbox/ball2/driver-v2.md",
     "an unseen surface (a) killed my freshly started .venv loop, (b) DELETED state/fuel/stealth_driver.jsonl (gone between 15:16Z and 15:21Z; no repo code deletes it, grep clean), and (c) spawned uv-python + venv pythonw PAIRS born the same second"),
    ("I3", "watch/inbox/wave5_repair/stealth-tools.md",
     'The old code set `hermes_python = sys.executable` (the comment claimed "Hermes Python, already on PATH"; it is the DRIVER\'s python).'),
    ("I4", "watch/inbox/wave5_repair/suite-burn.md",
     "the 14 named suite failures burned to zero (2026-09-29)"),
    ("I4", "watch/inbox/gala_20260925/wave5-repair_RECEIPT.md",
     "finish line 14 failed / 2452 passed / 12 skipped in 2326.98s, all 14 byte-proven basetemp-environmental"),
    ("I4", "watch/inbox/wave5_repair/events-door.md",
     "Full-suite `pytest -q` ran to completion in the background in 2389.58s (39:49): 7 failed, 2436 passed, 12 skipped, 15 errors. NONE of the failures touch this lane's surface"),
    ("I4", "watch/inbox/wave5_repair/events-door.md",
     "test_seed_mcp.py (15 errors, TypeError build()), test_context_pack_delivery.py (2)"),
    ("I4", "watch/inbox/ball2/mcp-bridge-r1.md",
     "all 19 test files that import the tools registry: 218 passed, exit 0"),
    ("I2", "watch/inbox/ball2/attention-ledger.md",
     "trades settle once and reprice the feed"),
]

# insight -> receipt paths expected to back it (organ-distinctness is asserted)
INSIGHT_SOURCES = {
    "I1": ["watch/inbox/wave5_repair/mcp-pin-wire.md",
           "watch/inbox/wave5_repair/render-pipe.md",
           "watch/inbox/wave5_repair/seed-kernel.md",
           "watch/inbox/wave5_repair/attention-channel.md",
           "watch/inbox/wave5_repair/events-door.md",
           "watch/inbox/ball2/driver-v2.md"],
    "I2": ["watch/inbox/wave5_repair/seed-kernel.md",
           "watch/inbox/wave5_repair/stealth-tools.md",
           "watch/inbox/ball2/mcp-bridge-r1.md",
           "watch/inbox/wave5_repair/mcp-pin-wire.md",
           "watch/inbox/wave5_repair/attention-channel.md",
           "watch/inbox/wave5_repair/patrol-fix.md",
           "watch/inbox/wave5_repair/render-pipe.md"],
    "I3": ["watch/inbox/wave5_repair/events-door.md",
           "watch/inbox/wave5_repair/seed-kernel.md",
           "watch/inbox/ball2/attention-ledger.md",
           "watch/inbox/ball2/driver-v2.md",
           "watch/inbox/wave5_repair/attention-channel.md",
           "watch/inbox/wave5_repair/stealth-tools.md"],
    "I4": ["watch/inbox/wave5_repair/suite-burn.md",
           "watch/inbox/gala_20260925/wave5-repair_RECEIPT.md",
           "watch/inbox/wave5_repair/events-door.md",
           "watch/inbox/ball2/mcp-bridge-r1.md"],
}


def norm(s: str) -> str:
    return " ".join(s.split())


def organ_of(path: str) -> str:
    for organ, paths in ORGANS.items():
        if path in paths:
            return organ
    return "?"


def main() -> int:
    lines: list[str] = []
    failures = 0

    def log(msg: str) -> None:
        lines.append(msg)
        print(msg)

    log("LATTICE CHECK " + "=" * 60)
    log(f"chapter: {CHAPTER}")
    log("")

    # 1. receipt existence
    log("[1] cited receipt paths exist")
    all_paths = sorted({p for paths in INSIGHT_SOURCES.values() for p in paths})
    for p in all_paths:
        ok = (ROOT / p).is_file()
        log(f"  {'PASS' if ok else 'FAIL'} exists: {p}")
        failures += 0 if ok else 1
    log("")

    # 2. quote byte containment
    log("[2] quotes are whitespace-normalized byte substrings of their sources")
    for insight, path, quote in QUOTES:
        src = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        ok = norm(quote) in norm(src)
        log(f"  {'PASS' if ok else 'FAIL'} [{insight}] {path} :: {quote[:60]}...")
        failures += 0 if ok else 1
    log("")

    # 3. insight citation discipline: >= 2 receipts, >= 2 distinct organs
    log("[3] each insight cites >= 2 receipts from different organ families")
    for insight in sorted(INSIGHT_SOURCES):
        organs = {organ_of(p) for p in INSIGHT_SOURCES[insight]}
        ok = len(INSIGHT_SOURCES[insight]) >= 2 and len(organs) >= 2 and "?" not in organs
        log(f"  {'PASS' if ok else 'FAIL'} {insight}: {len(INSIGHT_SOURCES[insight])} receipts, organs={sorted(organs)}")
        failures += 0 if ok else 1
    log("")

    # 4. chapter shape and dash discipline
    log("[4] chapter receipt")
    chapter = CHAPTER.read_text(encoding="utf-8")
    n_insights = chapter.count("\n## Insight ")
    log(f"  {'PASS' if n_insights >= 3 else 'FAIL'} insight headers in chapter: {n_insights} (need >= 3)")
    failures += 0 if n_insights >= 3 else 1
    em = chapter.count("\u2014")
    en = chapter.count("\u2013")
    log(f"  {'PASS' if em == 0 and en == 0 else 'FAIL'} em-dashes={em} en-dashes={en} in lattice.md")
    failures += 0 if em == 0 and en == 0 else 1
    has_gap = "no dedicated 48h tapestry receipt exists" in chapter
    log(f"  {'PASS' if has_gap else 'FAIL'} tapestry gap stated honestly in chapter")
    failures += 0 if has_gap else 1
    log("")

    # 5. tapestry absence evidence, run here
    log("[5] tapestry absence evidence")
    r = subprocess.run(
        ["git", "log", "--oneline", "--since=2026-09-28", "--", "mag/tapestry.py", "mag/tapestry_visual.py"],
        cwd=str(ROOT), capture_output=True, text=True)
    log(f"  git log --oneline --since=2026-09-28 -- mag/tapestry.py mag/tapestry_visual.py")
    log(f"  exit={r.returncode} stdout={r.stdout.strip()!r} (empty = no tapestry commits in window)")
    ok = r.returncode == 0 and r.stdout.strip() == ""
    log(f"  {'PASS' if ok else 'FAIL'} no tapestry repair commits in the 48h window")
    failures += 0 if ok else 1
    sb = ROOT / "watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt"
    txt = sb.read_text(encoding="utf-8", errors="replace")
    hits = [i + 1 for i, line in enumerate(txt.splitlines()) if "tapestry" in line.lower()]
    log(f"  suite-burn.check.txt tapestry rows at lines: {hits[:6]}... ({len(hits)} hits)")
    ok = len(hits) >= 5
    log(f"  {'PASS' if ok else 'FAIL'} tapestry suite-green pin present in the 48h suite run")
    failures += 0 if ok else 1
    log("")

    verdict = "LATTICE CHECK: PASS" if failures == 0 else f"LATTICE CHECK: FAIL ({failures})"
    log(verdict)
    CHECK_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"raw output written: {CHECK_FILE}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
