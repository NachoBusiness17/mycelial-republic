# riblive1-U1-r1-glm-flash (glm-5.3-flash @ zai, turn 1, channel: content)

L1: Prose numbers cannot poison the census parse
CLAIM: The census claim is read only from the parenthesized clause matched by CENSUS_CLAIM_RE, anchored on the "N tests [collected] / M files (YYYY-MM-DD census" shape. Earlier first-match regexes took the first date or count anywhere on the bullet, so tripwire prose like "31 files grown" ahead of the claim silently became the parse (B2-245).
STEAL: If your parser reads a carrier line with multiple number-bearing regexes, re-anchor the match on the claim's clause shape so stray prose numbers cannot satisfy it.
FALSIFIER: Reordering the live AGENTS.md bullet so tripwire prose precedes the claim changes the parsed counts, or self-test vectors show first-match behavior.
SOURCE: tools/census_drift_patrol.py "prose numbers elsewhere on the bullet never parse, the B2-245 order-fragility fix"
LEVERAGE: high

L2: Frozen regression vectors never auto-sync to the live carrier
CLAIM: Parser grammar is owned by CENSUS_CLAIM_RE plus its comment block; frozen fixture vectors in census_patrol_selftest.py and tests/test_census_drift_patrol.py are never updated when the live AGENTS.md count moves, because a frozen number is the only witness that can catch a grammar break. Vectors change only with a named receipt (B2-274).
STEAL: Audit your hand-copied fixtures for live-value sync; if they track the live count, freeze them and require a receipt to move.
FALSIFIER: Rewording the AGENTS.md bullet to a foreign grammar turns self-test or pytest red; or fixtures are found updating themselves from the live bullet.
SOURCE: tools/census_drift_patrol.py "the live count moving (1,837 -> 1,879 -> 1,910 in one day) must not move the fixtures"
LEVERAGE: high

L3: Verdict cores are pure and fail-closed on unverifiable bytes
CLAIM: patrol(), collect_patrol(), and zero_collect_patrol() are pure functions returning verdict dicts; any cannot-verify condition (missing carrier, unparseable claim, future census date, git failure, pytest timeout) exits 2, never a guess and never a pass. The deep check also treats a None collected claim as UNVERIFIABLE exit 2.
STEAL: Extract your gate's verdict logic into pure cores taking only parsed bytes, and route every gather failure to a distinct cannot-verify exit code instead of defaulting to pass.
FALSIFIER: A gather failure (bad git, missing file, unparseable line) produces exit 0 anywhere in the tool.
SOURCE: tools/census_drift_patrol.py "Fail-closed by construction: a missing carrier file, a missing or unparseable"
LEVERAGE: high

L4: Staleness requires age AND world movement, never same-day mismatch
CLAIM: The carrier is STALE only when its census age exceeds CENSUS_STALE_DAYS (default 7) AND tests/ grew since the census day (commits strictly after that day, or disk candidate count shrinking below the claimed file count). A same-day or in-window mismatch is evidence text, never exit 1; same-day commits are excluded as ambiguous.
STEAL: Adopt the two-condition bar (age beyond window plus committed growth or disk shrink) in any freshness gate so daily landing noise cannot fail pushes.
FALSIFIER: A census one day old alongside 50 new test files exits 1, or a 30-day-old census with zero growth exits 1.
SOURCE: tools/census_drift_patrol.py "STALE = age beyond bar AND growth since the census."
LEVERAGE: medium

L5: Zero-collect test files fail by default, tolerance needs a receipt
CLAIM: A pytest-named file on disk contributing zero collected node ids fails the deep check exit 1 unless it is in ZERO_COLLECT_TOLERANT, which is seeded empty on purpose; the one real case (test_selffeed_integration.py) was itself the disease, a __main__ script wearing test naming. Aggregate "N tests / M files" denominators hid it for weeks.
STEAL: Run pytest --collect-only, diff disk candidates against collected files, and name or fail every zero-item file instead of trusting aggregate counts.
FALSIFIER: A file named test_*.py collecting zero items passes the deep check without a ZERO_COLLECT_TOLERANT entry.
SOURCE: tools/census_drift_patrol.py "test files that collect zero items hide inside the aggregate denominators"
LEVERAGE: medium
