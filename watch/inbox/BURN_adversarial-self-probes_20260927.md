# BURN adversarial-self-probes 2026-09-27

## Verdict

steal

## Evidence

- Tool landed: tools/ledger_append_gate.py (stdlib only, never appends). Contract: (a) JSON object; (b) six typed fields: ts ISO-8601 UTC, slug nonempty, verdict nonempty, fresh_failure_mode strict bool, landing exists-on-disk or owed-marker (owed|missing), one_line string; (c) byte-identical one_line banked refuses; (d) exit 0 + VALID on pass, exit 2 + reason on refuse.
- Live battery, actual outputs (temp ledger, 2 seed rows):
  1. valid new row: VALID, exit 0
  2. valid variant (+00:00 ts, tool-path landing): VALID, exit 0
  3. the _d forged row verbatim (prose ffm): REFUSE "(b) fresh_failure_mode must be boolean true/false (strict type), got str", exit 2
  4. boolean-ffm duplicate one_line: REFUSE "(c) duplicate one_line already in ledger (row 1...)", exit 2
  5. missing ts: REFUSE "(b) required field(s) missing: ts", exit 2
  6. byte-copy of real row 557 vs real ledger: REFUSE "(c) duplicate one_line already in ledger (row 557...)", exit 2
  Ledger bytes verified unchanged after every run.
- Read-only history audit (self-match excluded), 557 rows: 434 non-conforming on ffm (431 key-missing, 3 prose); row 265 stores one_line as a JSON list; row 554 landing watch/inbox/ORGAN_CENSUS_20260927.md does not exist on disk: a live false landing in tonight's tail, hours old, undetected until this gate; 3 byte-identical prior duplicates (pairs 106=107, 368=372, 419=422; first two never counted anywhere); 0 ts violations.
- Web search snippet-level again; the one fetch resolved to a blog homepage, not the cited post. Nothing adopted, none owed.

## Steal or Vacuous

Steal: the PROBE-C pre-registered build EXECUTED and is byte-tested. The forged row that landed clean in the miss now refuses exit 2 before any append. The gate earned beyond its brief: the landing branch caught a live false landing (554) the freshness checker never covered, the duplicate branch surfaced two never-counted pairs, the type branch found the list-typed one_line. Boundary honesty: unwired by contract (adoption is cross-window; tools/ledger_lock.py cmd_append is the natural caller and currently calls only json.loads). By the _d falsifier's own rule the MISSED stands until a live writer routes through the gate; this pass closes the build half only. Inherited blindness, named: paraphrase duplicates pass (byte-identical check only); verdict is pinned nonempty here, the _d enum and per-line sha pin stay owed.

## Falsifier (or none proposed)

Adoption falsifier, pre-registered: wire validate_line into ledger_lock.py cmd_append before lock acquisition, cross-window. The gate is real only if a forged row entering via the normal write path exits nonzero and is refused pre-lock. If any live writer still lands rows without calling the gate after adoption, the gate is theater and a fresh miss books. Owed decision at adoption: the 434 banked non-conforming rows get either a backfill sweep or an explicit conformance frontier (ledger row number where the gate went live); silent grandfathering is the vacuous outcome.

## Bibliography (closed)

- watch/inbox/PROWL_STEAL_20260925.md (read)
- watch/inbox/BURN_adversarial-self-probes_20260925.md through _20260926_d.md, seven receipts (read; _d is the direct predecessor)
- memory/burns/LEDGER.jsonl (read-only, bytes unchanged)
- tools/ledger_lock.py, tools/ledger_close_check.py (read)
- tools/ledger_append_gate.py (BUILT this pass)
- Web search 2026-09-27, "write-time schema validation gate append JSONL ledger September 2026" (snippet-level); fetch redreamality.com (homepage, not the post; nothing adopted, none owed)
