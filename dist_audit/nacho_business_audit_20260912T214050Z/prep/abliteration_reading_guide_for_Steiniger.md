ENTRY FILES
- Code: mag/cache_identity.py
- Schema / guide: audit_prep/identity_schema.md

READING GUIDE (outsider):
1) Identity serialization portability
   - Check: audit_prep/identity_schema.md
   - Test: mag/tests/test_identity_schema_portability.py
   - Why: ensures exported persona tokens map across tokenizers and formats

2) Transfer surfaces and gates
   - Check: mag/transfer_gate.py, mag/canon_gate.py, mag/cache_identity.py
   - Test: mag/tests/verify_identity_coupling.py
   - Why: these are the runtime paths that move cached persona material between organs

3) Pack-driven induction and seed control
   - Check: packs/gen_matthew_480.py and packs/p320_matthew_20260913.json
   - Check hermes_personas: mag/hermes_personas/*.md
   - Why: persona construction uses packs; verify the seed, prompt scaffolding, and whether pack metadata is sufficient to reproduce identity

ONE TRAP (what fools the auditor):
- Superficial schema passing: tests and identity_schema.md may assert a JSON schema and unit-roundtrip but do NOT exercise cross-substrate/tokenizer variations (see audit_prep_verkle/migration_manifest_ATTACK_CELL_20260913.md and HANDOFF/MIGRATION_MAC_STUDIO_QUAD_20260825.md). If reviewer trusts schema-only checks, cross-model drift or substrate-specific tokenization will be missed.

QUICK ACTIONABLES (starter):
- Run mag/tests/test_identity_schema_portability.py and mag/tests/verify_identity_coupling.py under the two tokenizers used in packs (local Ollama vs host tokenizer).
- Attempt an export/import using packs/p320_matthew_20260913.json via mag/cache_identity.py and validate textual equivalence plus model-response parity.

RECIPIENT: Matthew Steiniger reading lane; file created as dist_audit/nacho_business_audit_20260912T214050Z/prep/abliteration_reading_guide_for_Steiniger.md
