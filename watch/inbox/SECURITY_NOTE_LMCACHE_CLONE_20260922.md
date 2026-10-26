# SECURITY CLASSIFICATION: lmcache-src clone — Mimosa L2 findings · 2026-09-22

Mimosa L2 flagged 3 findings in `lmcache-src/` (ZCode workspace root). Classification and basis:

**Origin:** clone of https://github.com/LMCache/LMCache.git (tip 770e413, PR #5285),
created 2026-09-21 22:59 EDT — during this window, by a 50-wide workflow research lane
(kvos-lmcache / disk-kv-extract facet; lanes were instructed to read primary sources).
The clone is RESEARCH MATERIAL — read/cite, not execute, not estate code, not shipped.

**Finding-by-finding:**

1. `tools/translate_docs_zh.py:318` — SSRF (urlopen on dynamic URL): TRUE upstream
   pattern, LOW estate risk. It is a developer doc-translation CLI whose URL comes from
   its own config/env; exploitability requires a local operator running it with hostile
   config. Not in any estate execution path.
2. `tests/conftest.py:736` — command injection (`rm -rf {device}` via shlex.split):
   TRUE upstream hygiene smell, LOW estate risk — `device` comes from the test suite's
   own fixtures, not user input, but string-built `rm -rf` deserves an upstream issue.
3. `tests/v1/test_cache_engine.py:262` — command injection: **FALSE POSITIVE**. The
   command is a string LITERAL: `shlex.split("rm -rf local/disk_test/local_disk/")` —
   no user input reaches the command line. Basis: direct read of lines 262-263.

**Action taken:** none against the clone's bytes — patching a research clone would
corrupt provenance (we cite and hash upstream bytes; Ground = primary record). The
clone is classified READ-RESEARCH / DO-NOT-EXECUTE. Upstream issues 1–2 are worth
filing to LMCache upstream on operator GO (house rule: no external PRs without one).
If workspace hygiene demands, the clone can be deleted after the lift lands — its
citable value is the upstream URL + commit hash, not the local copy.

— ZCode seat, 2026-09-22, responding to Mimosa L2 hook.
