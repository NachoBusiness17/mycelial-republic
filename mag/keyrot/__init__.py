"""mag.keyrot: automated API key rotation pipeline (2026-10-25).

Stages: inventory -> policy -> plan (adapter or manual queue) -> rotate (--apply only)
-> store -> verify consumer -> ledger. Default is DRY-RUN. Secret values live in
process memory only; every output carries type + sha256 prefix, never a value.
Self-steals tools.secret_guard (parse/read/policy paths), mag.doctor
check_tracked_secrets logic (live-value git grep) and the estate audit file.
Never touches the Mag verkle chain, its tip or its ACL.
"""
