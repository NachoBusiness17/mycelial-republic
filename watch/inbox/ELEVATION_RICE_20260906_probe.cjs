// Reproduce the distance-field counterexample using the prototype's own geometry.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const path = require('node:path');

const root = path.resolve(__dirname, '../..');
const source = path.join(root, 'dashboard/static/doorbench.html');
const bytes = fs.readFileSync(source);
const html = bytes.toString('utf8');
const start = html.indexOf('function cb(');
const end = html.indexOf('// ------------------------------------------------------- field + textures');
assert(start >= 0 && end > start, 'Expected geometry section must exist');
assert(html.includes('const DR = { x0:62, y0:2, z0:28, w:1, h:6, d:8 };'),
  'Dirty-region definition changed; review this probe');
const values = vm.runInNewContext(
  'const N=64,W=2/N;\n' + html.slice(start, end) +
  '\n[evalAt(61,4,31,false), evalAt(61,4,31,true)]', {}, {timeout: 1000});
assert.equal(values[0], 0.046875);
assert.equal(values[1], 0.015625);
assert.notEqual(values[0], values[1]);
console.log(JSON.stringify({
  claim: 'Changing field value outside declared dirty set',
  status: 'COUNTEREXAMPLE_CONFIRMED',
  source: 'dashboard/static/doorbench.html',
  source_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  cell: [61,4,31], inside_dirty_set: false,
  open: values[0], closed: values[1],
  limitation: 'Geometry-value test only; no rendered failure or speedup measured'
}, null, 2));
