# Error Banner Audit Preparation Summary

## Cell Context
**DOMAIN**: error_banner — ship-with-failures-visible doctrine  
**MODE**: MAP — produce the outsider's reading guide for this area  
**CELL DELIVERABLES**: 3 files created in `audit_prep/`

## Outsider's Reading Guide

### Entry File
`audit_prep/error_banner_audit_cell.md` - Main audit finding per the output contract

### Three Things to Check

1. **Coverage Gap**: Verify the 9/109 file discrepancy - are core dashboard pages intentionally excluded from error handling, or is this an oversight?

2. **Selective Application**: Determine if there's a documented architectural decision that differentiates between game/interactive pages (which have banners) and core system pages (which don't)

3. **Alternative Mechanisms**: Investigate whether core dashboard pages use alternative error handling that provides equivalent failure visibility

### The One Trap
**Assuming universal application**: The biggest trap is assuming the "ship-with-failures-visible" doctrine applies equally to all surfaces. The evidence suggests selective implementation - audit must determine if this is intentional design (with documentation) or implementation inconsistency.

## Evidence Package Created

- `error_banner_audit.md` - Detailed audit checklist and methodology
- `verify_error_banner.py` - Automated verification script (found 97/109 files missing complete fixture)
- `error_banner_audit_cell.md` - Main audit finding per output contract
- `error_banner_independent_analysis.md` - Stage B analysis suggesting selective transparency

## Key Discovery
The doctrine is inconsistently applied: only 9% of dashboard pages have complete error handling, creating a potential gap between stated principles and actual system behavior that an abliteration-minded examiner would exploit.