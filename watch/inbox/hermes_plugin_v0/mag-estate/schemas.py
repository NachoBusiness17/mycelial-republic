"""Tool schemas (what the model reads). Read-only v0."""
_EMPTY = {"type": "object", "properties": {}, "required": []}

CHAIN_VERIFY = {
    "name": "mag_chain_verify",
    "description": ("Verify the Mag hash-chain memory (memory/biography/verkle_chain.jsonl) is internally "
                    "consistent: recompute the merkle root over all leaves and compare with the tip. "
                    "Read-only. Returns ok + reason. Note: internal consistency only; it proves nothing "
                    "against a writer who also rewrote the tip (needs an external witness)."),
    "parameters": _EMPTY,
}
RECEIPT_VALIDATE = {
    "name": "mag_receipt_validate",
    "description": ("Validate a fleet_report.v1 JSON report (SPOTREP/SITREP/NOTICE/RELIEF/ACK) against "
                    "Mag's schema, including the secret-shaped-value refusal. Pure check, writes nothing. "
                    "Use before filing a report."),
    "parameters": {"type": "object",
                   "properties": {"report": {"type": "string",
                                             "description": "The report as a JSON object string"}},
                   "required": ["report"]},
}
NOTICES = {
    "name": "mag_notices",
    "description": "List Mag fleet NOTICEs currently in force with their ACKs (read-only).",
    "parameters": _EMPTY,
}
LEASES = {
    "name": "mag_leases",
    "description": ("List Mag restricted-resource leases (who holds what until when). Read-only; "
                    "acquire/release stay with Mag's own CLI (scripts/lease.py) in v0."),
    "parameters": _EMPTY,
}
