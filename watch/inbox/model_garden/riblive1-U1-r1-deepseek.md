# riblive1-U1-r1-deepseek (deepseek-chat @ deepseek, turn 1, channel: content)

L1: Strictly-after-day means same-day commits never count
CLAIM: Growth from git is counted only from commits whose committer-local date is strictly greater than the census date, so test files landed on the census day itself never trigger STALE. Same-day activity is deliberately treated as ambiguous, not as growth.
STEAL: Add a same-day test vector to tools/census_patrol_selftest.py asserting that a file added at 23:59 on census day yields added_since == 0, pinning the ambiguity rule before someone "fixes" it to >=.
FALSIFIER: A patched patrol() that treats same-day commits as growth and survives every frozen vector in census_patrol_selftest.py and tests/test_census_drift_patrol.py, proving the rule was never pinned.
SOURCE: tools/census_drift_patrol.py: "if commit_day is not None and commit_day > census_date and line.startswith(\"tests/\")"
LEVERAGE: high

L2: Disk shrink is the only provable file-count drift
CLAIM: Because item-bearing files are a subset of pytest-named candidates, disk count can only ever exceed the carrier claim; therefore only disk_files < carrier_files is read as drift, and every over-direction gap is labeled instrument lag and printed as evidence, never as a violation. The asymmetry is the load-bearing choice.
STEAL: Add a unit test to tests/test_census_drift_patrol.py with disk_files = carrier_files + 50 asserting verdict OK, so the evidence-only treatment of the gap cannot silently become a failure mode.
FALSIFIER: A real tests/ tree where pytest-name candidates are fewer than item-bearing files, which would falsify the subset premise and make the shrink-only rule unsound.
SOURCE: tools/census_drift_patrol.py: "only shrink is provable drift"
LEVERAGE: high

L3: Exit 2 is the fail-closed arm for every unverifiable byte
CLAIM: Missing carrier, unparseable **Tests:** line, unparseable date, future-dated census, and git failure all map to exit 2 via PatrolError or an explicit pre-check, so the gate never guesses a pass on missing or malformed evidence. Exit 2 is reserved for cannot-verify, exit 1 for verified-stale.
STEAL: Write a table-driven pytest case that feeds run() a root with each of the five fault shapes and asserts exit 2, forcing new fault types to declare their code.
FALSIFIER: Any code path in run() that returns 0 or 1 after a parse or subprocess failure, which would collapse the cannot-verify arm into a verdict.
SOURCE: tools/census_drift_patrol.py: "a git failure is exit 2, never a guess and never a pass"
LEVERAGE: high

L4: The census claim parses only from the parenthesized clause
CLAIM: CENSUS_CLAIM_RE reads counts and date only from the "N tests [collected] / M files (YYYY-MM-DD census" clause, so prose numbers elsewhere on the bullet cannot poison the parse; a non-canonical bullet returns None and exits 2 rather than guessing. The retired first-match regexes are named as the bug this closes.
STEAL: Add an adversarial vector to census_patrol_selftest.py that prepends "31 files grown" prose to the real bullet and asserts the parse still reads the clause counts, since that probe already exists on disk to copy.
FALSIFIER: A bullet where a prose number forms a full census clause ahead of the real claim and parses first, which would falsify the clause-anchoring premise.
SOURCE: tools/census_drift_patrol.py: "prose numbers elsewhere on the bullet cannot poison the parse"
LEVERAGE: high

L5: Deep check runs only behind --collect, never in the default path
CLAIM: The default gate measures growth by git commits and disk bytes alone and never invokes pytest, keeping pre-push fast and venv-free; the collected-count comparison requires explicit --collect and takes COLLECT_DRIFT_TOLERANCE (20) as a symmetric bar. Because the file-growth signal is blind to items added inside existing files, an unrun deep check leaves real collected drift invisible to the default gate.
STEAL: Add a scheduling note or CI job that runs tools/census_drift_patrol.py --collect on a timer with the venv present, since the default gate structurally cannot catch intra-file parametrize growth.
FALSIFIER: A pre-push run without --collect that nonetheless exits 1 due to collected drift, which would falsify the claim that the deep check stays outside the default path.
SOURCE: tools/census_drift_patrol.py: "growth is measured by git and disk bytes only, which keeps pre-push fast and dependency-free"
LEVERAGE: medium
