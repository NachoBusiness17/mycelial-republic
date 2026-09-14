#!/usr/bin/env python3
"""Runtime test for 480-wide wave temperature rigidity."""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, '.')

from mag.temperature_stack import registry, stack_for_goal


def simulate_480_wide_wave_improve():
    """Simulate 480-wide wave with [improve] tag and verify stack application."""
    reg = registry()
    
    print("Testing 480-wide wave with [improve] tag...")
    print("=" * 60)
    
    # Resolve improve stack for the wave
    improve_stack = reg.resolve(goal="[improve]", tag="improve")
    print(f"Resolved improve stack: timeout={improve_stack.timeout_s}s, tokens={improve_stack.max_tokens}, temp={improve_stack.temperature}")
    
    # Simulate 480 lanes with improve goals
    lanes = []
    for i in range(480):
        lane_id = f"lane_{i:03d}"
        goal = f"[improve] self-improve task {i}"
        
        # Each lane should resolve to the improve stack
        lane_stack = reg.resolve(goal=goal, tag="improve")
        lane_data = {
            'lane_id': lane_id,
            'goal': goal,
            'resolved_stack': lane_stack.id,
            'timeout_s': lane_stack.timeout_s,
            'max_tokens': lane_stack.max_tokens,
            'temperature': lane_stack.temperature,
            'expected_timeout': improve_stack.timeout_s,
            'expected_tokens': improve_stack.max_tokens,
            'expected_temp': improve_stack.temperature,
            'matches_expected': (
                lane_stack.timeout_s == improve_stack.timeout_s and
                lane_stack.max_tokens == improve_stack.max_tokens and
                lane_stack.temperature == improve_stack.temperature
            )
        }
        lanes.append(lane_data)
    
    # Analyze results
    all_match = all(lane['matches_expected'] for lane in lanes)
    mismatched_lanes = [lane for lane in lanes if not lane['matches_expected']]
    
    # Simulate runtime enforcement check
    runtime_check_pass = True
    for lane in lanes:
        if lane['timeout_s'] > improve_stack.timeout_s:
            print(f"❌ Lane {lane['lane_id']} exceeded timeout: {lane['timeout_s']}s > {improve_stack.timeout_s}s")
            runtime_check_pass = False
        if lane['max_tokens'] > improve_stack.max_tokens:
            print(f"❌ Lane {lane['lane_id']} exceeded tokens: {lane['max_tokens']} > {improve_stack.max_tokens}")
            runtime_check_pass = False
    
    # Generate report
    report = {
        'schema': 'mag_480_wave_temperature_test.v1',
        'ts': datetime.now(timezone.utc).isoformat(),
        'test_type': '480_wide_wave_improve_tag',
        'wave_width': 480,
        'goal_tag': '[improve]',
        'resolved_improve_stack': {
            'id': improve_stack.id,
            'timeout_s': improve_stack.timeout_s,
            'max_tokens': improve_stack.max_tokens,
            'temperature': improve_stack.temperature
        },
        'lanes_tested': len(lanes),
        'all_lanes_match_expected': all_match,
        'mismatched_lanes': len(mismatched_lanes),
        'runtime_enforcement_pass': runtime_check_pass,
        'verifier_pass': all_match and runtime_check_pass,
        'lanes': lanes[:10],  # Sample first 10 lanes in report
        'sample_mismatches': mismatched_lanes[:5] if mismatched_lanes else []
    }
    
    # Save to state directory
    state_dir = Path('state')
    state_dir.mkdir(exist_ok=True)
    report_path = state_dir / 'temperature_rigidity_480_wave_test.json'
    report_path.write_text(json.dumps(report, indent=2))
    
    # Print summary
    print(f"✓ All lanes match expected stack: {all_match}")
    print(f"✓ Runtime enforcement pass: {runtime_check_pass}")
    print(f"✓ Overall test pass: {report['verifier_pass']}")
    print(f"Mismatched lanes: {len(mismatched_lanes)}")
    
    if mismatched_lanes:
        print("Sample mismatches:")
        for lane in mismatched_lanes[:3]:
            print(f"  {lane['lane_id']}: {lane['resolved_stack']} (expected improve)")
    
    print(f"Full report saved to: {report_path}")
    
    return report


if __name__ == "__main__":
    result = simulate_480_wide_wave_improve()
    sys.exit(0 if result['verifier_pass'] else 1)