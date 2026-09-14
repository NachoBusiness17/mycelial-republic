"""Reproduce the scoped recount without dispatching tools or importing fleet code.

Run with Python 3. The default input is the adjacent frozen snapshot. An optional
first argument can name the live ledger; only the registered byte prefix is read,
and its hash must match before any counts are accepted. No ledger text is printed.
"""
import hashlib
import json
from pathlib import Path
import sys

PREFIX_BYTES = 27_934_077
EXPECTED_SHA256 = '9ab1b9dff8b2001c2a82a7c092d2c63613daa744507df6ea2b551bbad1957b74'
source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('failure-ledger-frozen-prefix.jsonl')
with source.open('rb') as stream:
    raw = stream.read(PREFIX_BYTES)
actual_digest = hashlib.sha256(raw).hexdigest()
if len(raw) != PREFIX_BYTES or actual_digest != EXPECTED_SHA256:
    raise SystemExit('UNPROVEN: input bytes do not match the registered frozen prefix')

signature = 'run_shell:c73866f2f1b5'
exact = literal = elsewhere = valid = 0
invalid = []
sessions = set()
row_hashes = set()
identity_fields = set()
for line_number, line in enumerate(raw.splitlines(), 1):
    if not line.strip():
        continue
    has_literal = signature.encode('ascii') in line
    literal += int(has_literal)
    try:
        row = json.loads(line)
    except (ValueError, UnicodeDecodeError):
        invalid.append(line_number)
        continue
    if not isinstance(row, dict):
        raise SystemExit('UNPROVEN: unexpected non-object JSON row')
    valid += 1
    if row.get('sig') == signature:
        exact += 1
        row_hashes.add(hashlib.sha256(line).hexdigest())
        if row.get('session_id'):
            sessions.add(str(row['session_id']))
        identity_fields.update(k for k in ('attempt_id', 'operation_id', 'request_id', 'call_id') if row.get(k) is not None)
    elif has_literal:
        elsewhere += 1

print(json.dumps({'snapshot_sha256': actual_digest, 'captured_bytes': len(raw),
                  'valid_json_rows': valid, 'invalid_line_numbers': invalid,
                  'exact_signature_records': exact, 'literal_matching_lines': literal,
                  'literal_mentions_elsewhere': elsewhere, 'distinct_row_hashes': len(row_hashes),
                  'distinct_sessions': len(sessions), 'explicit_identity_fields': sorted(identity_fields),
                  'verified_unique_dispatch_attempts': None}, indent=2))
