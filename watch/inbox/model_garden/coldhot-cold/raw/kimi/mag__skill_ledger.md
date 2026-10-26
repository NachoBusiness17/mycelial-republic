# coldhot-cold-kimi-mag__skill_ledger (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Race condition in _append: non-atomic write to shared jsonl surface | EVIDENCE: mag/skill_ledger.py:63-66 | FIX: Use tempfile.NamedTemporaryFile(dir=path.parent, delete=False) + os.replace for atomic append
DEFECT 2: _count uses errors='replace' corrupting line count accuracy on encoding errors | EVIDENCE: mag/skill_ledger.py:71-77 | FIX: Use errors='strict' and handle UnicodeDecodeError explicitly, or use byte-counting with newline detection
DEFECT 3: proven_moves loads entire decisions file into memory at once | EVIDENCE: mag/skill_ledger.py:82-94 | FIX: Stream-read with mmap or line-by-line iteration instead of read_text().splitlines()
DEAD-CODE: OUTCOME_REGISTRY dict is defined but never read programmatically | EVIDENCE: mag/skill_ledger.py:36-49
ONE-SITTING FIX: Replace _append with atomic tmp+replace pattern | EVIDENCE: mag/skill_ledger.py:63-66
