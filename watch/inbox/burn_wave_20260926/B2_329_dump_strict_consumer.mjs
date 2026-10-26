#!/usr/bin/env node
/**
 * B2_329_dump_strict_consumer.mjs: the B2-329 falsifier's strict JSON consumer.
 *
 * Reads `node scripts/index_fold_host.mjs events` from stdin and validates every
 * dumped line against the event key schema, rejecting UNKNOWN keys. The schema is
 * the census of every key any real writer ever appended to
 * watch/inbox/index_events.jsonl, taken at lane start over log sha256
 * cfd3b2dde83b7dadf32e9b21cd54ef64a0fe6a4ab3e354a524c314b57953cec4 (3443 lines,
 * 3 legacy malformed lines the fold skips and this consumer therefore never sees).
 * Fold plumbing fields (_outside, _unresolved) are attached in memory by
 * readEvents and were written by NO writer, so they are unknown keys here: a
 * downstream consumer with this schema parses them as event content, which is
 * exactly the B2-329 defect.
 *
 * Usage:
 *   node scripts/index_fold_host.mjs events | node B2_329_dump_strict_consumer.mjs [out.json]
 *
 * Prints a one-line verdict and, given a path argument, writes the full result
 * JSON (status, lines checked, unknown keys with line numbers and counts).
 * Exit 0 on PASS, 1 on FAIL.
 */
import { readFileSync, writeFileSync } from 'fs';

// Census-derived writer schema at log sha cfd3b2dd... (counts in comments are
// occurrences across the 3439 parseable lines at lane start).
const SCHEMA = new Set([
  'seq',        // 3019: appendOp + legacy numeric seqs
  'ts',         // 3439
  'op',         // 3359
  'file',       // 3354
  'sha256',     // 3219
  'class',      // 2934
  'purpose',    // 3270
  'writer',     // 1252
  'nonce',      // 1055
  'living',     // 16 (B2-156 living law)
  'size',       // 14 (living prefix seal)
  'seal',       // 2 (living open)
  'reason',     // 142 (invalidate)
  'bytes',      // 327 (legacy writer extras below, census at lane start)
  'files',      // 61
  'source',     // 61
  'kind',       // 21
  'item',       // 21
  'card',       // 21
  'url',        // 16
  'prev_sha256', // 12
  'note',       // 5
  'cls',        // 4
  'repaired',   // 2
  'repair_note', // 2
  'cls_key_disclosed', // 2
  'text',       // 1
  't',          // 1
  'path',       // 1
  'commit',     // 1
]);

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const lines = Buffer.concat(chunks).toString('utf8').split('\n').filter((l) => l.trim() !== '');

const unknown = new Map(); // key -> { count, firstLine }
let checked = 0;
lines.forEach((line, idx) => {
  let ev;
  try {
    ev = JSON.parse(line);
  } catch (e) {
    const rec = unknown.get('<unparseable line>') || { count: 0, firstLine: idx + 1 };
    rec.count++;
    unknown.set('<unparseable line>', rec);
    return;
  }
  checked++;
  for (const k of Object.keys(ev)) {
    if (!SCHEMA.has(k)) {
      const rec = unknown.get(k) || { count: 0, firstLine: idx + 1 };
      rec.count++;
      unknown.set(k, rec);
    }
  }
});

const unknownList = [...unknown.entries()]
  .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
  .map(([k, rec]) => ({ key: k, count: rec.count, firstLine: rec.firstLine }));
const result = {
  probe: 'B2_329_dump_strict_consumer.mjs',
  schema: 'census of writer keys at index_events.jsonl sha cfd3b2dde83b7dadf32e9b21cd54ef64a0fe6a4ab3e354a524c314b57953cec4',
  status: unknownList.length === 0 ? 'PASS' : 'FAIL',
  lines_checked: checked,
  unknown_keys: unknownList,
};

const outPath = process.argv[2];
if (outPath) writeFileSync(outPath, JSON.stringify(result, null, 2) + '\n', 'utf8');
process.stdout.write(`${result.status}: ${checked} lines checked, ${unknownList.length} unknown key(s)` +
  (unknownList.length ? ` (${unknownList.map((u) => `${u.key} x${u.count}`).join(', ')})` : '') + '\n');
process.exit(unknownList.length === 0 ? 0 : 1);
