#!/usr/bin/env python3
"""Temperature rigidity verification script for audit prep."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, '.')

from mag.temperature_stack import registry, stack_for_goal


def verify_temperature_rigidity():
    """Verify temperature rigidity bands and improve tag resolution."""
    reg = registry()
    
    # Define expected band values from temperature_stacks.yaml
    bands = {
        'cold': {'timeout_s': 120, 'max_tokens': 512, 'temperature': 0.1},
        'warm': {'timeout_s': 600, 'max_tokens': 4096, 'temperature': 0.2},
        'hot': {'timeout_s': 900, 'max_tokens': 8192, 'temperature': 0.35},
        'scarce': {'timeout_s': 1200, 'max_tokens': 8192, 'temperature': 0.5},
        'improve': {'timeout_s': 420, 'max_tokens': 2048, 'temperature': 0.25}
    }
    
    results = {}
    all_bands_match = True
    
    # Verify each band
    for band_name, expected in bands.items():
        stack = reg.get(band_name)
        actual = {
            'timeout_s': stack.timeout_s,
            'max_tokens': stack.max_tokens,
            'temperature': stack.temperature
        }
        
        matches = (
            actual['timeout_s'] == expected['timeout_s'] and
            actual['max_tokens'] == expected['max_tokens'] and
            actual['temperature'] == expected['temperature']
        )
        
        if not matches:
            all_bands_match = False
            
        results[band_name] = {
            'expected': expected,
            'actual': actual,
            'matches': matches
        }
    
    # Verify improve tag resolution for [improve] goal
    improve_stack = reg.resolve(goal="[improve]", tag="improve")
    improve_expected = {'timeout_s': 420, 'max_tokens': 2048, 'temperature': 0.25}
    improve_actual = {
        'timeout_s': improve_stack.timeout_s,
        'max_tokens': improve_stack.max_tokens,
        'temperature': improve_stack.temperature
    }
    improve_matches = (
        improve_actual['timeout_s'] == improve_expected['timeout_s'] and
        improve_actual['max_tokens'] == improve_expected['max_tokens'] and
        improve_actual['temperature'] == improve_expected['temperature']
    )
    
    if not improve_matches:
        all_bands_match = False
        
    results['improve_tag_resolution'] = {
        'expected': improve_expected,
        'actual': improve_actual,
        'matches': improve_matches
    }
    
    # Generate verification report
    report = {
        'schema': 'mag_temperature_rigidity_verification.v1',
        'ts': datetime.now(timezone.utc).isoformat(),
        'verifier': 'temperature_rigidity',
        'bands': results,
        'all_bands_match': all_bands_match,
        'improve_tag_matches': improve_matches,
        'verifier_pass': all_bands_match and improve_matches,
        'note': '480-wide wave temperature gating verification'
    }
    
    # Save to state directory
    state_dir = Path('state')
    state_dir.mkdir(exist_ok=True)
    report_path = state_dir / 'temperature_rigidity_verifier_latest.json'
    report_path.write_text(json.dumps(report, indent=2))
    
    return report


if __name__ == "__main__":
    result = verify_temperature_rigidity()
    
    # Print summary for immediate feedback
    print("Temperature Rigidity Verification Report:")
    print("=" * 50)
    print(f"Overall Pass: {result['verifier_pass']}")
    print(f"All Bands Match: {result['all_bands_match']}")
    print(f"Improve Tag Matches: {result['improve_tag_matches']}")
    print()
    
    for band_name, band_result in result['bands'].items():
        status = "✓" if band_result['matches'] else "✗"
        print(f"{status} {band_name}: {band_result['actual']}")
    
    print()
    print(f"Report saved to: state/temperature_rigidity_verifier_latest.json")
    
    # Exit with appropriate code
    sys.exit(0 if result['verifier_pass'] else 1)