# swarm1-glm-flash-mag__scale_salon (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: --retry refires the architect and redteam gopher lanes unconditionally, duplicating spend on every retry run against the operator's dollar cap | EVIDENCE: mag/scale_salon.py:228-229 | FIX: change the filter to `jobs = [j for j in jobs if j[0]["id"] not in prev]` so gopher lanes dedupe like writers
DEFECT 2: after --retry, each OK gopher appears twice in raw.jsonl once via the refired row and once via prev, so the digest and pack double-count lanes | EVIDENCE: mag/scale_salon.py:244-245 | FIX: dedupe by lane id before writing: `seen = {}; rows = [seen.setdefault(r["lane"], r) for r in rows + list(prev.values())]`
DEFECT 3: _guard's resolved-IP check is TOCTOU: urlopen re-resolves DNS independently, so an attacker-controlled allowlisted host can pass the guard then resolve to a private address at request time | EVIDENCE: mag/scale_salon.py:166,184 | FIX: pin the validated IP (custom HTTPSConnection to the checked address with SNI/server_hostname set) instead of letting urlopen resolve again
DEAD-CODE: the https scheme check in _guard can never raise since every ALLOWED_BASES entry is an https literal | EVIDENCE: mag/scale_salon.py:63-64
ONE-SITTING FIX: make the retry filter lane-agnostic so gophers dedupe and raw.jsonl stays single-row-per-lane | EVIDENCE: mag/scale_salon.py:228-229

Falsifier for DEFECT 1: run `python mag/scale_salon.py --retry` against an existing raw.jsonl containing OK gopher rows and observe a second paid chat/completions call per gopher lane in provider logs.
