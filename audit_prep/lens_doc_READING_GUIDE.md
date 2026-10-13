## Finding — what your cell yields
The lens_doc area produces a falsifiable outsider's reading guide that maps Matthew Steiniger's published framework terms to the actual repo structure, exposing where the mapping overclaims and creating entry points for his abliteration instinct. The guide reveals that the strongest disagreement with the obvious reading is the claim that "our terms map cleanly to yours" – in reality, the house repurposes his EUT entropy minimization as a maintenance inequality, and the chain is not emergent ordering but a signed append-only ledger.

## Evidence — what in the repo supports it (file/shape, no invention)
- Entry file: `watch/inbox/MATTHEWS_LENS.md` (80 lines) contains explicit mappings of Steiniger's terms to house components
- Shape: 10 numbered mappings from "Your [term]" → "our [component]" with conceptual claims
- Disagreement evidence: `AGENTS.md` § "Verkle chain rule" and "Standing ruling" contradict the mapping of EUT to emergent ordering – the chain is explicitly read-only with root mismatch traps, not emergent
- Missing evidence: No implementation of "entropy minimization resists gradients; temperature modulates rigidity" as claimed in mapping #6 – only maintenance inequality references exist
- Overclaim evidence: Mapping #3 "Athena → Rocinante" claims substrate-native identities, but the migration design only claims identity lives in the ledger, not weights

## Risk if wrong — what the audit breaks on if this is missed
- **False positive mapping**: Steiniger's abliteration instinct will attack the clean mapping claim, finding the read-only chain contradicts emergent ordering, and the house will appear to either misunderstand his framework or misrepresent its own architecture
- **Trust erosion**: If the mapping overclaims are not exposed, the examiner will discover them independently and conclude the house either doesn't understand his work or is being disingenuous
- **Falsifier failure**: The examiner's falsifier expects precise mappings; any overclaim in the lens will fail his reproducibility test and break the audit's credibility

## The act — the concrete prep step (file/spec/number)
Create `audit_prep/lens_doc_READING_GUIDE.md` with content:

```markdown
# Lens Doc Reading Guide - Matthew Steiniger Framework Mapping

## Entry Point
`watch/inbox/MATTHEWS_LENS.md` - The explicit mapping document claiming "his terms mapping ours"

## Three Things to Check

1. **Claim Accuracy**: Verify each of the 10 numbered mappings against actual repo implementation
   - Check if mapping claims match code/structure (e.g., "EUT → verkle chain" emergent vs read-only)
   - Look for actual implementations of claimed concepts (e.g., "entropy minimization" code)
   - Verify "substrate-native identities" claim against migration design docs

2. **Overclaim Detection**: Identify where the mapping exceeds what exists in the repo
   - Mapping #1: "vector framework for in-context sculpting" → "Primer parable" (cold-read vs actual implementation)
   - Mapping #6: "entropy minimization resists gradients" → "maintenance inequality" (conceptual vs mathematical)
   - Mapping #3: "Athena → Rocinante" substrate-native identities (claim vs actual ledger-only persistence)

3. **Missing Implementations**: Find concepts claimed in mapping but not implemented
   - "temperature modulates rigidity" – no temperature parameter in code
   - "cross-model identity transfer" – only wave mirror, no transfer protocol
   - "abliteration" – only error banners, no systematic safeguard removal

## The One Trap
**Do NOT accept the mapping at face value** – Steiniger's abliteration instinct will attack the cleanest claims. The strongest disagreement is that EUT (emergent entropy) maps to a read-only ledger with root mismatch traps, not emergent ordering. The chain's deterministic, signed nature contradicts the emergent framing.

## Falsifier
Produce a working implementation of "entropy minimization resists gradients; temperature modulates rigidity" as mathematical code, not conceptual maintenance inequality. Until then, the mapping overclaims.
```

2. Create supporting script `scripts/verify_lens_mapping.py` to check claims against repo structure:
```python
#!/usr/bin/env python3
"""Verify MATTHEWS_LENS.md mappings against actual repo implementation"""

import os
import json
import re
from pathlib import Path

def check_mapping_implementation(mapping_number, claim, search_terms):
    """Check if mapping claim is implemented in repo"""
    repo_root = Path('.')
    
    for term in search_terms:
        # Search in code files
        for ext in ['.py', '.md', '.yaml', '.json']:
            for file_path in repo_root.rglob(f"*{ext}"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if term.lower() in content.lower():
                            print(f"✓ Found '{term}' in {file_path}")
                            return True
                except (UnicodeDecodeError, PermissionError):
                    continue
    
    print(f"✗ No implementation found for claim: {claim}")
    return False

def main():
    # Mapping claims to verify (simplified version)
    mappings = {
        1: {
            "claim": "vector framework for in-context sculpting → Primer parable",
            "search_terms": ["primer", "parable", "cold_read", "vector", "sculpting"]
        },
        6: {
            "claim": "entropy minimization resists gradients → maintenance inequality", 
            "search_terms": ["entropy", "minimization", "gradient", "temperature", "rigidity", "maintenance"]
        },
        3: {
            "claim": "Athena → Rocinante substrate-native identities",
            "search_terms": ["rocinante", "substrate", "migration", "identity", "weights"]
        }
    }
    
    print("Verifying MATTHEWS_LENS.md mappings against repo implementation...")
    print("=" * 60)
    
    for mapping_num, data in mappings.items():
        print(f"\nMapping {mapping_num}: {data['claim']}")
        implemented = check_mapping_implementation(mapping_num, data['claim'], data['search_terms'])
        print(f"Status: {'IMPLEMENTED' if implemented else 'NOT IMPLEMENTED'}")
    
    print("\n" + "=" * 60)
    print("Falsifier: Produce mathematical implementation of entropy minimization to prove mapping valid")

if __name__ == "__main__":
    main()
```

3. Add both files to `audit_bundle/INDEX.json` with SHA-256 hashes.

## Falsifier — what would prove this wrong
- Mathematical implementation of "entropy minimization resists gradients; temperature modulates rigidity" as actual code, not conceptual maintenance inequality
- Discovery of emergent ordering in the verkle chain (currently it's explicitly read-only with root mismatch traps)
- Working cross-model identity transfer protocol (currently only wave mirror exists)
- Temperature parameter that actually modulates system rigidity in the codebase