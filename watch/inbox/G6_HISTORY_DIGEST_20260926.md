# G6 HISTORY DIGEST 2026-09-26

Gopher t76 (wired from t69 next_steal). Audits every PASS row in
`memory/workflows/REGISTRY.jsonl` against the t69 dated-stamp bar: the gate's own
`G6_STAMP_RE` (`(?i)\b(source[-_ ]fetched|fetched|observed[-_]at)\s*:\s*\d{4}-\d{2}-\d{2}`)
applied to each registered script file on disk, exactly as `tools/workflow_gate.py`
applies it behind G6.

Scope and method:

- Registry rows total: 10. PASS rows audited: 6. FAIL rows (4) are out of scope and listed below.
- Rows skipped because the script file no longer exists: 0. All three registered
  PASS-row scripts are still on disk.
- Read-only audit: the registry was not appended to, no repo file changed, nothing registered.
- Raw output: `watch/inbox/gala_20260925/afterparty/lanes/t76.check.txt` (audit_exit=0).

## Audit table (one line per PASS row)

| script | verdict | dated-stamp |
|---|---|---|
| .zcode/workflow-drafts/Tree-Doctrine-50-wide-dig.dwf.ts (row da62eaa8c17f, 2026-09-25T18:52:43Z) | WARN | no |
| .zcode/workflows/mickey17-v2.dwf.ts (row 9b51b8e2ee05, 2026-09-25T20:47:59Z) | WARN | no |
| .zcode/workflows/the-gala.dwf.ts (row 0ad57dc88296, 2026-09-26T02:32:43Z) | WARN | no |
| .zcode/workflows/the-gala.dwf.ts (row 0ad57dc88296, 2026-09-26T02:33:43Z) | WARN | no |
| .zcode/workflows/the-gala.dwf.ts (row 0ad57dc88296, 2026-09-26T02:51:06Z) | WARN | no |
| .zcode/workflows/the-gala.dwf.ts (row 0ad57dc88296, 2026-09-26T03:27:51Z) | WARN | no |

Verdict key: WARN = receipt-path mention present but no dated stamp; under the
current gate this is the G6 soft-false row (`ok=false, soft=true, reason="receipt
mention lacks a dated stamp (label + YYYY-MM-DD, t62 prefilter family)"`), verdict
stays PASS, exit stays 0.

## Counts

- PASS rows audited: 6
- dated (stamp present): 0
- undated (WARN under current G6): 6
- no receipt mention (would hard-FAIL current G6): 0
- skipped, script file missing: 0
- unique scripts among PASS rows: 3

## Negatives (first-class)

1. The dogfood debt is total: zero of six PASS history rows would pass the current
   G6 dated-stamp bar. Every PASS row predates t69's stamp requirement, so the
   soft WARN covers the whole PASS ledger, not a corner of it.
2. Digest drift on mickey17-v2.dwf.ts: the registered row carries digest
   9b51b8e2ee05 but the file on disk hashes to 5492d9a51eb2 (sha256, first 12 hex,
   gate's own digest formula). The file was edited after the 2026-09-25T20:47:59Z
   PASS row was written; the WARN verdict above is judged on the on-disk text, and
   the registered bytes no longer exist anywhere. The other two scripts match their
   registered digests exactly.
3. Out-of-scope FAIL rows (4, listed for honesty, not audited): tree-doctrine-dig
   25dff0842218, mickey17-v2.dwf.ts f190bf31e2ef, the-gala.dwf.ts 2a9ae3707582, and
   the t69 debug row t69dbg cfcc50823fe1 whose Temp script
   (`C:/Users/foste/AppData/Local/Temp/t69dbg/sample.dwf.ts`) still exists but was
   not audited because FAIL rows are outside this item's scope.
4. This digest is authored text: 0 em-dashes and 0 en-dashes (scan in t76.check.txt).

Bank: `watch/inbox/gala_20260925/afterparty/lanes/t76.json`.
