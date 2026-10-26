# swarm1-deepseek-mag__art_forge (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: `_refresh_index` calls `re.sub` but the module never imports `re`, so the index refresh raises NameError | EVIDENCE: mag/art_forge.py:105 (re.sub usage), imports mag/art_forge.py:21-29 | FIX: add `import re` to the import block

DEFECT 2: Losing rows. On partial failure the todo rows that failed to forge are dropped: the rewrite path only preserves `rest` plus forged ids | EVIDENCE: mag/art_forge.py:158-160 | FIX: build remaining from ids not in `done` (i.e. `rest + [r for r in todo if rid not in done]`)

DEFECT 3: `rows = [json.loads(l) for l in ...]` has no per-line guard, so one malformed queue line crashes the whole cycle and blocks all later rows | EVIDENCE: mag/art_forge.py:132 | FIX: wrap each parse in try/except and append the bad line to errors

DEAD-CODE: `_refresh_index` return value is discarded, so the `True`/`False` return has no consumer | EVIDENCE: mag/art_forge.py:103-114, mag/art_forge.py:164

ONE-SITTING FIX: add `import re` so the marker-gated index rebuild stops crashing | EVIDENCE: mag/art_forge.py:21-29, mag/art_forge.py:105
