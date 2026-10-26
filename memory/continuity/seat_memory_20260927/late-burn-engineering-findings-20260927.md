---
name: late-burn-engineering-findings-20260927
description: Late-burn engineering findings 9/27 — PYTEST_CURRENT_TEST can't be
  a suppression key (pytest re-sets it at every phase transition), restore guard
  two-arm pattern, stanza-based crash census replacing substring math
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Three engineering findings from the late width-24 swarm (9/27 early AM) that are generalizable beyond this fleet:

## PYTEST_CURRENT_TEST is not a suppression key (B2-358)

The first cut of the env-redirect tripwire suppressed on `PYTEST_CURRENT_TEST`, but the pins caught pytest re-setting that marker at every phase transition — it can never serve as a suppression key for env-var-based test isolation. The correct pattern: check for a test-specific VALUE in the env var, not just the presence of the env var itself. Warning fires unconditionally; `in_test_run` stays informational.

## Restore guard two-arm pattern (B2-343)

Pre-write `check` arm (fails exit 1 naming every claim filed after the snapshot ts, including retired CLAIMED lines which is the exact blind spot the 16:35 restore slipped through) + post-hoc `audit` arm riding the refold gate's `--changed` shape. No-op restores (bytes already equal snapshot sha) pass. The retired-CLAIMED counting is the load-bearing insight.

## Stanza-based crash census (B2-357)

Replaces `count("Traceback") - count("INJECTED-")` substring math with structural stanza counting: split on `stage=` header lines, entries = stanzas holding a Traceback header, test = stanza with a body line starting with INJECTED-. This makes chained exceptions count once and quoted markers never misclassify. The census imports `_CRASH_STANZA_RE` from the reader so writer and reader cannot drift.

## Width-24 verdict consolidated

The ceiling is a function of window depth, not a constant:
- Fresh window width 24: clean, 109M tok/h
- Deep window width 24: 8 surfaced 1302s in 1 hour
- Width 10-12 at any depth: 1,741 silently absorbed (invisible to surfaced counts)
- 287 absorbed in three "clean" waves (129+35+123)
- The absorbed-retry blind spot is now closed by tools/provider_error_tally.py
