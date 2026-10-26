# coldhot-cold-glm-flash-mag__training_events (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: read_events slurps the entire events.jsonl into memory before slicing, unbounded on an append-only file | EVIDENCE: mag/training_events.py:106-120 | FIX: tail-read the file (seek from end) or stream-parse lines and keep only the last `limit` rows.
DEFECT 2: export_jsonl's tier_max argument is never enforced; only each row's own tier_max is checked, so callers can claim a gate that does not exist | EVIDENCE: mag/training_events.py:130-133,150-152 | FIX: filter `eligible` to rows whose tier_max is at or below the `tier_max` argument, or drop the parameter and manifest field.
DEFECT 3: emit silently rewrites unknown patterns to "route_decision" (line 77), corrupting labels for every typo'd caller | EVIDENCE: mag/training_events.py:75-77 | FIX: log a fkb_failure-style side event or raise ValueError instead of coercing.
DEAD-CODE: the `tier_max` parameter of export_jsonl is accepted but never read | EVIDENCE: mag/training_events.py:130-133,143
ONE-SITTING FIX: replace read_text-split with a bounded tail read in read_events so emit/stats/export cannot balloon memory as events.jsonl grows | EVIDENCE: mag/training_events.py:106-108
