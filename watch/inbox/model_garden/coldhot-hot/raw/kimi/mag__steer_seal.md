# coldhot-hot-kimi-mag__steer_seal (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: LOG is unconditionally used in _log_event before None check, but LOG is defined as a Path that may not exist, causing mkdir to fail on permission errors without proper handling | EVIDENCE: mag/steer_seal.py:66 | FIX: Move LOG.parent.mkdir inside the try block or handle OSError explicitly for mkdir

DEFECT 2: write_keyfile force=True path uses os.replace which is atomic but non-force path uses os.open/os.fdopen without fsync, risking partial writes on crash | EVIDENCE: mag/steer_seal.py:157-163 | FIX: Add os.fsync(fd) before os.fdopen closes in non-force write_keyfile path

DEFECT 3: _gate passes keyfile=None to verify and load_keys when keyfile param is None, but default_keyfile() may not exist causing VerifyError that returns False from verify, yet _gate treats this as verify failure rather than distinguishing missing keyfile from bad MAC | EVIDENCE: mag/steer_seal.py:328-330 | FIX: Pass explicit keyfile=default_keyfile() when keyfile is None to ensure consistent path resolution and clearer error propagation

DEAD-CODE: _PUNCT_TO_SPACE translation table is created but only used in classify which normalizes to NFC then uppercases; the punctuation stripping is correct but the table construction could be lazy | EVIDENCE: mag/steer_seal.py:48 | FIX: None - not clearly dead, but consider lazy initialization if import-time cost matters

ONE-SITTING FIX: Add atomic tmp+replace to _log_event for the known jsonl surface violation | EVIDENCE: mag/steer_seal.py:75-85 | FIX: Write to LOG.with_suffix('.tmp') then os.replace to LOG inside the try block
