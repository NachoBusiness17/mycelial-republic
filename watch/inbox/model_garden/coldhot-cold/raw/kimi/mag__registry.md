# coldhot-cold-kimi-mag__registry (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: write_residual writes to path without atomic tmp+replace, risking corruption on crash | EVIDENCE: mag/registry.py:235-239 | FIX: use tempfile.NamedTemporaryFile + os.replace pattern as in upsert_registry
DEFECT 2: set_latest_session writes LATEST_SESSION and latest.dossier.json without atomic tmp+replace | EVIDENCE: mag/registry.py:138-150 | FIX: use tempfile.NamedTemporaryFile + os.replace for both files
DEFECT 3: write_derived_md writes directly to BIO/latest.md without atomic tmp+replace | EVIDENCE: mag/registry.py:256-260 | FIX: use tempfile.NamedTemporaryFile + os.replace for latest.md
DEAD-CODE: legacy_dossier_path function only used in migration path and find_residual fallback | EVIDENCE: mag/registry.py:35-36
ONE-SITTING FIX: Add atomic tmp+replace wrapper and apply to all direct write_text/write_bytes calls | EVIDENCE: mag/registry.py:138-150,235-239,256-260,268-275,284-291
