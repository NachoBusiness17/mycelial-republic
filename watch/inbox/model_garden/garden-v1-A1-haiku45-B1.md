# garden-v1-A1-haiku45-B1 (anthropic/claude-haiku-4.5 @ nous, turn 1, channel: content)

IMPROVEMENT 1: Evidence preflight check only probes first 400 chars of file; truncated evidence files pass validation but fail silently when rendered, defeating CARRIER-PATCH 3 intent | EVIDENCE: tools/hermes_burn.py:175-182 | FIX: Read full file in preflight and check that probe appears verbatim in body (not just first 400 chars).

IMPROVEMENT 2: _hermes_key() opens .env file once per key name search without seeking; file handle leaks if exception raised before loop completes | EVIDENCE: tools/hermes_burn.py:75-82 | FIX: Wrap loop in `with open(...) as f: for line in f:` or call readlines() once before iteration.

IMPROVEMENT 3: run_ask() appends turn 2 output to out_path without checking file still exists; concurrent asks with same id or external deletion cause silent data loss on revision turns | EVIDENCE: tools/hermes_burn.py:316-317 | FIX: Assert out_path.exists() before append on turn 2, raise RuntimeError if missing.

DIFFERENT-BUILD: I would move _assert_evidence_in_body() call to _landed_skip() return point, not inside the turn loop. Evidence validity is a precondition of the ask itself, not a per-turn gate; validating twice (turn 1 and turn 2 rebuild) wastes cycles and masks the true dependency: an ask with invalid evidence should be refused at entry, before any output file is written.
