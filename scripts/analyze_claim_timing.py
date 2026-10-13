#!/usr/bin/env python3
"""
Timing analysis for the "one hour to first true claim" metric.
Processes verkle chain data to establish baseline timing distribution.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def load_chain_data(chain_file):
    """Load verkle chain data and return first N entries."""
    knots = []
    with open(chain_file, 'r') as f:
        for i, line in enumerate(f):
            if i >= 100:  # Process first 100 knots
                break
            knots.append(json.loads(line))
    return knots

def is_true_claim(knot):
    """
    Determine if a chain knot represents a "true claim".
    Criteria based on observable patterns in the chain:
    1. Has a dominant_theme (not null)
    2. Has a tension_index > 0.5 (shows engagement/conflict)
    3. Contains operational language (e.g., "build", "launch", "verify")
    """
    
    # Criterion 1: Has dominant theme
    if not knot.get('dominant_theme'):
        return False
    
    # Criterion 2: Has tension (engagement level)
    tension = knot.get('tension_index', 0)
    try:
        tension_float = float(tension) if tension else 0.0
    except (ValueError, TypeError):
        tension_float = 0.0
    
    if tension_float <= 0.5:
        return False
    
    # Criterion 3: Operational language in filename or theme
    operational_terms = ['build', 'launch', 'verify', 'audit', 'deploy', 'check', 'gate']
    filename = knot.get('filename', '').lower()
    theme = knot.get('dominant_theme', '').lower()
    
    for term in operational_terms:
        if term in filename or term in theme:
            return True
    
    return False

def calculate_timing(knots):
    """Calculate timing distribution for true claims."""
    true_claims = []
    
    for knot in knots:
        if is_true_claim(knot):
            ts = knot['ts']
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                true_claims.append({
                    'ts': ts,
                    'filename': knot['filename'],
                    'theme': knot['dominant_theme'],
                    'tension': knot.get('tension_index', 0),
                    'session_id': knot['session_id']
                })
            except ValueError:
                continue
    
    return true_claims

def main():
    chain_file = Path('memory/biography/verkle_chain.jsonl')
    if not chain_file.exists():
        print(f"ERROR: Chain file not found: {chain_file}")
        sys.exit(1)
    
    print("Analyzing verkle chain for 'true claim' timing...")
    knots = load_chain_data(chain_file)
    true_claims = calculate_timing(knots)
    
    print(f"\nProcessed {len(knots)} chain knots")
    print(f"Found {len(true_claims)} 'true claims'")
    
    if true_claims:
        print("\nTrue claims found:")
        for claim in true_claims:
            print(f"  {claim['ts']} | {claim['theme']} | {claim['filename']}")
        
        # Calculate timing from first knot to first true claim
        first_knot_ts = knots[0]['ts']
        first_true_ts = true_claims[0]['ts']
        
        try:
            start_dt = datetime.fromisoformat(first_knot_ts.replace('Z', '+00:00'))
            true_dt = datetime.fromisoformat(first_true_ts.replace('Z', '+00:00'))
            time_diff = (true_dt - start_dt).total_seconds() / 3600  # Convert to hours
            
            print(f"\nTime to first true claim: {time_diff:.2f} hours")
            
            if time_diff <= 1.0:
                print("✅ CONFIRMED: One-hour metric achieved")
            else:
                print("❌ DISPUTED: One-hour metric NOT achieved")
                
        except ValueError as e:
            print(f"ERROR: Invalid timestamp format: {e}")
    else:
        print("❌ NO TRUE CLAIMS FOUND in first 100 knots")
        print("The 'one hour to first true claim' metric is UNVERIFIABLE")

if __name__ == "__main__":
    main()