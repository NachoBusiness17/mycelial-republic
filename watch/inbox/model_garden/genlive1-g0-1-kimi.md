# genlive1-g0-1-kimi (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Uncontrolled temp file creation with predictable name allows symlink attack on replace | EVIDENCE: tools/corpus_fts_rebuild.py:48-50 | FIX: Use tempfile.mkstemp(dir=db_path.parent) or os.O_EXCL|O_NOFOLLOW for atomic temp creation
DEAD-CODE: malformed counter incremented but never returned or logged in final output | EVIDENCE: tools/corpus_fts_rebuild.py:65
ONE-SITTING FIX: Replace tmp_path.exists()/unlink() race with tempfile.mkstemp in same directory | EVIDENCE: tools/corpus_fts_rebuild.py:48
