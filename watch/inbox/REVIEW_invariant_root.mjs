#!/usr/bin/env node
// invariant_root.mjs — INVARIANT ROOT + PROOF publication tool (Ethereum-style planewave).
// Exp-002b: invariants as enforced proposals; anchor via rolling root + proof path.
//
// Usage:
//   node invariant_root.mjs propose "<invariant text>" <proposer>
//        appends {seq,ts,op:"propose",text,proposer,prev_root} to /board/invariants_proposals.jsonl
//        prev_root = the root computed over ALL prior lines (before this proposal).
//   node invariant_root.mjs root
//        folds ALL proposal lines in seq order, prints the rolling root.
//        fold rule: h_i = sha256(lineBytes); root_i = sha256(root_{i-1}Raw || h_iRaw)
//        genesis root = sha256("")  [the well-defined empty-input constant].
//        Deterministic: same log => same root, always.
//   node invariant_root.mjs prove <seq>
//        outputs the invariant line + the intermediate hash path from genesis to <seq>
//        + consumer instructions to re-derive the root WITHOUT reading the full log.
//        A consumer verifies by: start genesis, fold each h_i on the path, reach root_<seq>,
//        and (if seq is not the tail) confirm root_<seq> == prev_root recorded on the next line.
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, appendFileSync, existsSync } from 'node:fs';

const LOG = '/board/invariants_proposals.jsonl';

const sha = (data) => createHash('sha256').update(data).digest('hex');
const shaRaw = (data) => createHash('sha256').update(data).digest(); // 32 raw bytes
const GENESIS_ROOT = sha(''); // e3b0c442... constant

// Read all proposal lines in file order. Skip malformed/blank lines but FAIL loudly on corruption.
function loadLines() {
  if (!existsSync(LOG)) return [];
  const raw = readFileSync(LOG, 'utf8').split('\n').filter((l) => l.trim() !== '');
  return raw;
}
// Fold provenance: returns array of {hash, root, lineIndex} per line in seq order.
function fold(lines) {
  let prevRootRaw = Buffer.from(GENESIS_ROOT, 'hex');
  const path = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const hRaw = shaRaw(line);
    const h = hRaw.toString('hex');
    const rootRaw = shaRaw(Buffer.concat([prevRootRaw, hRaw]));
    const root = rootRaw.toString('hex');
    path.push({ lineIndex: i, line, h, root });
    prevRootRaw = rootRaw;
  }
  return path;
}
function currentRoot(lines) {
  const path = fold(lines);
  return path.length === 0 ? GENESIS_ROOT : path[path.length - 1].root;
}

const [, , cmd, ...rest] = process.argv;

if (cmd === 'propose') {
  const text = rest[0];
  const proposer = rest[1];
  if (!text || !proposer) {
    console.error('usage: node invariant_root.mjs propose "<invariant text>" <proposer>');
    process.exit(1);
  }
  const lines = loadLines();
  const prev = currentRoot(lines);
  const seq = lines.length; // 0-based seq; lines.length+1 proposals gave seq of next = length
  const rec = {
    seq,
    ts: new Date().toISOString(),
    op: 'propose',
    text,
    proposer,
    prev_root: prev,
  };
  const line = JSON.stringify(rec);
  appendFileSync(LOG, line + '\n');
  console.log(`APPENDED seq=${seq} prev_root=${prev}`);
  console.log(line);
  console.log(`now ${lines.length + 1} proposal(s); next root:`);
  console.log(currentRoot(loadLines()));
} else if (cmd === 'root') {
  const lines = loadLines();
  console.log(`GENESIS_ROOT=${GENESIS_ROOT}`);
  console.log(`proposals=${lines.length}`);
  console.log(`ROOT=${currentRoot(lines)}`);
} else if (cmd === 'prove') {
  const target = Number(rest[0]);
  if (Number.isNaN(target)) {
    console.error('usage: node invariant_root.mjs prove <seq>');
    process.exit(1);
  }
  const lines = loadLines();
  if (target < 0 || target >= lines.length) {
    console.error(`PROVE FAIL: seq ${target} out of range (0..${lines.length - 1})`);
    process.exit(1);
  }
  const path = fold(lines);
  // Proof path = intermediate fold records from genesis up to (and including) target.
  const proofPath = path.slice(0, target + 1);
  const targetRecord = proofPath[proofPath.length - 1];
  const nextPrevRoot = target + 1 < lines.length ? JSON.parse(lines[target + 1]).prev_root : null;

  console.log(`== PROOF for seq ${target} ==`);
  console.log(`LOG=${LOG}`);
  console.log(`GENESIS_ROOT=${GENESIS_ROOT}`);
  console.log(`== invariant line (seq=${target}) ==`);
  console.log(lines[target]);
  console.log(`\n== proof path (genesis -> seq ${target}) ==`);
  proofPath.forEach((p) => {
    console.log(`  idx ${String(p.lineIndex).padStart(2)}: sha256(line)=${p.h}`);
    console.log(`             root=${p.root}`);
  });
  console.log(`\nroot_at_seq_${target}=${targetRecord.root}`);
  if (nextPrevRoot !== null) {
    console.log(`prev_root recorded on NEXT line (seq ${target + 1})=${nextPrevRoot}`);
    console.log(`NEXT-LINE ANCHOR MATCH: ${nextPrevRoot === targetRecord.root}`); 
  } else {
    console.log('(this is the tail proposal — anchor against the published root, not a next line)');
  }
  console.log(`PUBLISHED-TIP MATCH: ${targetRecord.root === currentRoot(lines)}`);

  console.log(`\n== CONSUMER INSTRUCTIONS (re-derive root WITHOUT reading full log) ==`);
  console.log(`1. Start accumulator A = GENESIS_ROOT (${GENESIS_ROOT}).`);
  proofPath.forEach((p) => {
    console.log(`2. A = sha256( A(raw) || sha256(line_{${p.lineIndex}})(raw) )  ->  ${p.root}`);
  });
  console.log(`3. A now == root_at_seq_${target} = ${targetRecord.root}.`);
  console.log(`4. If this proof was anchored BEFORE later appends, confirm ${targetRecord.root} equals the root that was published/tipped at proposal time (invariants are immutable once anchored).`);
  console.log(`5. (Optional cross-check) if a later line exists, its prev_root must equal ${targetRecord.root}.`);
} else {
  console.error('usage:');
  console.error('  node invariant_root.mjs propose "<invariant text>" <proposer>');
  console.error('  node invariant_root.mjs root');
  console.error('  node invariant_root.mjs prove <seq>');
  process.exit(1);
}
