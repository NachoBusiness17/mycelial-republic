D15 retest probe B2 (2026-10-07, lane d15-trust-teeth-retest): one fabricated
quantity attributed, in its own sentence, to a live code path, and one control
quantity citing a dead record path, both through the same engine run.
RECORD_SOURCE_SUFFIXES filters code suffixes out before the unresolved branch
(tools/citation_lint_numbers.py:208-217), so a .py attribution leaves sources
empty and unresolved empty, and the number is never counted at all.

The fold burned 911M tokens this week (tools/hermes_burn.py).

The fleet burned 912M tokens this week (watch/inbox/NO_SUCH_D15_SOURCE.md).
