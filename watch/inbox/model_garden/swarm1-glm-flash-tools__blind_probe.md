# swarm1-glm-flash-tools__blind_probe (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: judge accepts any lane string, including DARK or misspelled lanes, and awards it Elo wins over every OK lane with no validation | EVIDENCE: tools/blind_probe.py:189-202 | FIX: require lane in probe_row["returns"] with status "OK" before pairing, else reject
DEFECT 2: re-judging the same probe_id re-awards Elo each time (no once-per-probe guard), silently inflating ratings | EVIDENCE: tools/blind_probe.py:189-206 | FIX: mark probe_row judged (e.g. probe_row["judged"]=True) and refuse repeat judgment
DEFECT 3: Gemini API key sits in the request URL, so a connection URLError string can embed the keyed URL and gets written truncated into the shared probe md and elo.json | EVIDENCE: tools/blind_probe.py:96-97,167,180 | FIX: pass the key via "x-goog-api-key" header instead of the query string
DEAD-CODE: the empty-resolve check is unreachable because socket.getaddrinfo raises instead of returning an empty list | EVIDENCE: tools/blind_probe.py:56-58
ONE-SITTING FIX: add lane validation plus a judged-once flag in judge(), closing both the fake-winner and double-award holes in one edit | EVIDENCE: tools/blind_probe.py:189-206
