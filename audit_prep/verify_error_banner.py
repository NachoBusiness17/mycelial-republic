#!/usr/bin/env python3
"""
Error Banner Audit Verification Script
Automated verification of the error_banner doctrine across all game files.
"""

import os
import re
import json
from pathlib import Path

def check_error_banner_in_file(filepath):
    """Check if a file contains the error banner fixture."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for error banner div
        banner_div = 'id="errbanner"' in content
        # Check for error event listener
        error_listener = 'window.addEventListener(\'error\'' in content
        # Check for unhandled rejection listener
        rejection_listener = 'window.addEventListener(\'unhandledrejection\'' in content
        
        return {
            'file': filepath.name,
            'has_banner_div': banner_div,
            'has_error_listener': error_listener,
            'has_rejection_listener': rejection_listener,
            'complete_fixture': banner_div and error_listener and rejection_listener
        }
    except Exception as e:
        return {
            'file': filepath.name,
            'error': str(e),
            'has_banner_div': False,
            'has_error_listener': False,
            'has_rejection_listener': False,
            'complete_fixture': False
        }

def main():
    """Main audit function."""
    dashboard_dir = Path("dashboard/static")
    
    if not dashboard_dir.exists():
        print(f"❌ Dashboard directory not found: {dashboard_dir}")
        return False
    
    html_files = list(dashboard_dir.glob("*.html"))
    print(f"🔍 Found {len(html_files)} HTML files in dashboard/static/")
    
    results = []
    missing_fixture = []
    incomplete_fixture = []
    
    for html_file in html_files:
        result = check_error_banner_in_file(html_file)
        results.append(result)
        
        if not result['complete_fixture']:
            if not result['has_banner_div']:
                missing_fixture.append(result['file'])
            else:
                incomplete_fixture.append(result['file'])
    
    # Print summary
    print(f"\n📊 AUDIT RESULTS:")
    print(f"✅ Complete fixture: {len([r for r in results if r['complete_fixture']])}/{len(html_files)}")
    print(f"❌ Missing fixture: {len(missing_fixture)}")
    print(f"⚠️  Incomplete fixture: {len(incomplete_fixture)}")
    
    if missing_fixture:
        print(f"\n🚨 FILES MISSING ERROR BANNER:")
        for file in missing_fixture:
            print(f"  - {file}")
    
    if incomplete_fixture:
        print(f"\n⚠️  FILES WITH INCOMPLETE FIXTURE:")
        for file in incomplete_fixture:
            result = next(r for r in results if r['file'] == file)
            missing_parts = []
            if not result['has_banner_div']: missing_parts.append("banner_div")
            if not result['has_error_listener']: missing_parts.append("error_listener")
            if not result['has_rejection_listener']: missing_parts.append("rejection_listener")
            print(f"  - {file} (missing: {', '.join(missing_parts)})")
    
    # Generate audit report
    audit_data = {
        'total_files': len(html_files),
        'complete_fixture': len([r for r in results if r['complete_fixture']]),
        'missing_fixture': len(missing_fixture),
        'incomplete_fixture': len(incomplete_fixture),
        'missing_fixture_files': missing_fixture,
        'incomplete_fixture_files': incomplete_fixture,
        'results': results
    }
    
    with open('audit_prep/error_banner_audit.json', 'w') as f:
        json.dump(audit_data, f, indent=2)
    
    print(f"\n📄 Audit report saved to: audit_prep/error_banner_audit.json")
    
    return len(missing_fixture) == 0 and len(incomplete_fixture) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)