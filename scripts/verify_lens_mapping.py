#!/usr/bin/env python3
"""Verify MATTHEWS_LENS.md mappings against actual repo implementation"""

import os
import json
import re
from pathlib import Path

def check_mapping_implementation(mapping_number, claim, search_terms):
    """Check if mapping claim is implemented in repo"""
    repo_root = Path('.')
    found_implementation = False
    
    for term in search_terms:
        # Focus on key files only
        key_files = [
            'watch/inbox/MATTHEWS_LENS.md',
            'AGENTS.md',
            'HANDOFF/MIGRATION_MAC_STUDIO_QUAD_20260825.md',
            'mag/verkle_knot.py',
            'docs/ref/SPORE_SANCHO.md'
        ]
        
        for file_path in key_files:
            if (repo_root / file_path).exists():
                try:
                    with open(repo_root / file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Look for specific term usage with context
                        if term.lower() in content.lower():
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if term.lower() in line.lower():
                                    # Check for implementation context
                                    context = ' '.join(lines[max(0, i-2):min(len(lines), i+3)])
                                    if any(indicator in context.lower() for indicator in [
                                        'def ', 'class ', 'import ', 'function ', 'implementation', 'code',
                                        'algorithm', 'model', 'system', 'framework', 'schema', 'cold_read',
                                        'parable', 'migration', 'substrate', 'identity', 'weights'
                                    ]):
                                        print(f"✓ Found '{term}' with implementation context in {file_path}")
                                        found_implementation = True
                                        break
                except (UnicodeDecodeError, PermissionError):
                    continue
            if found_implementation:
                break
    
    if not found_implementation:
        print(f"✗ No implementation found for claim: {claim}")
    return found_implementation

def main():
    # Mapping claims to verify (focused on key disagreements)
    mappings = {
        1: {
            "claim": "vector framework for in-context sculpting → Primer parable",
            "search_terms": ["primer", "parable", "cold_read"]
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