#!/usr/bin/env node
/**
 * index_fold.mjs — Ethereum-style append-only event log + fold for the shared inbox.
 *
 * KILLS the lost-update race structurally:
 *   Writers never read-modify-WRITE the whole INDEX.json. Instead every change is
 *   APPENDED (>>) as one line to index_events.jsonl — an append is atomic for small
 *   writes under POSIX — and INDEX.json is DERIVED by folding the log. Two writers
 *   appending both survive; nothing clobbers the log.
 *
 * The event log is the source of truth. INDEX.json is only a materialized fold of it.
 * Events are never erased (history is never rewritten); INVALIDATE marks an item
 * inactive instead of deleting its REGISTER line.
 *
 * Usage:
 *   node index_fold.mjs rebuild              Fold ALL events -> rewrite INDEX.json items
 *   node index_fold.mjs add <file> [class] [purpose]
 *                                             Append a register event (+ writer nonce), refold
 *   node index_fold.mjs invalidate <file> [reason]
 *                                             Append an invalidate event, refold
 *   node index_fold.mjs verify                 Re-hash every item's file vs the event log
 *
 * Per-writer nonce pattern (replay protection): the fold tracks, per writer, the last
 * nonce it has seen for that writer. `add` advances its own nonce. On fold, any GAP in
 * a writer's nonce sequence is reported as a warning — a warning that a concurrent writer
 * may have been interleaved or a nonce was skipped.
 */
import { createHash } from 'crypto';
import { readFileSync, writeFileSync, appendFileSync, existsSync, statSync, renameSync } from 'fs';

const INBOX_DIR = 'C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox';
const EVENTS_FILE = `${INBOX_DIR}/index_events.jsonl`;
const INDEX_FILE = `${INBOX_DIR}/INDEX.json`;
const ROOT_MARKER = 'shared_inbox.v1';

// ---------------------------------------------------------------------------
// helpers
// ---------------------------------------------------------------------------
function sha256hex(buf) {
  return createHash('sha256').update(buf).digest('hex').toUpperCase();
}

function nowIso() {
  return new Date().toISOString();
}

function die(msg, code = 1) {
  process.stderr.write(`ERROR: ${msg}\n`);
  process.exit(code);
}

function readEvents() {
  if (!existsSync(EVENTS_FILE)) die(`events file missing: ${EVENTS_FILE}`);
  const lines = readFileSync(EVENTS_FILE, 'utf8').split('\n').filter((l) => l.trim() !== '');
  const events = [];
  const skipped = [];
  lines.forEach((line, idx) => {
    try {
      events.push(JSON.parse(line));
    } catch (e) {
      skipped.push(idx + 1);  // tolerant reader: keep folding over legacy junk (line 94, PENDING_CODEX)
    }
  });
  if (skipped.length) console.error('skipped malformed lines:', skipped.join(','));
  events.sort((a, b) => (a.seq - b.seq) || (a.ts < b.ts ? -1 : 1));
  return events;
}

function nextSeq(events) {
  let max = 0;
  for (const ev of events) if (typeof ev.seq === 'number' && ev.seq > max) max = ev.seq;
  return max + 1;
}

// ---------------------------------------------------------------------------
// fold: events -> INDEX.json items
// ---------------------------------------------------------------------------
function fold(events) {
  // nonce tracking per writer for replay-protection warning
  const nonceByWriter = {};
  const nonceWarnings = [];

  let active = [];          // items currently registered
  const seen = new Set();   // files with a REGISTER that is active or later invalidated
  const invalidated = new Set();

  for (const ev of events) {
    // nonce gap detection (replay protection)
    if (ev.writer != null && typeof ev.nonce === 'number') {
      const prev = nonceByWriter[ev.writer];
      if (prev != null && ev.nonce !== prev + 1) {
        nonceWarnings.push(
          `writer "${ev.writer}" nonce GAP: expected ${prev + 1}, got ${ev.nonce} (seq ${ev.seq})`
        );
      }
      nonceByWriter[ev.writer] = ev.nonce;
    }

    if (ev.op === 'register') {
      if (!ev.file) die(`register event seq ${ev.seq} missing file`);
      seen.add(ev.file);
      active.push({
        path: ev.file,
        class: ev.class || 'UNPROVEN',
        purpose: ev.purpose || '',
        sha256: ev.sha256 || '',
        seq: ev.seq,
        register_ts: ev.ts || '',
      });
    } else if (ev.op === 'invalidate') {
      const target = ev.file;
      if (!target) die(`invalidate event seq ${ev.seq} missing file`);
      invalidated.add(target);
      active = active.filter((it) => it.path !== target);
    }
    // 'note' events carry no state — they are log-only markers.
  }

  // Sort active items by seq (registration order) = canonical order.
  active.sort((a, b) => a.seq - b.seq);

  const items = active.map(({ seq, register_ts, ...rest }) => rest);

  const meta = {
    schema: ROOT_MARKER,
    root: INBOX_DIR,
    host_root: 'watch/inbox',
    purpose:
      'Single shared landing zone. INDEX.json is now DERIVED from the append-only event log ' +
      'index_events.jsonl (Ethereum fold pattern, EXP-002A). Writers APPEND events; they ' +
      'never rewrite this file or the log. The log is the source of truth.',
    read_first: '/board/inbox/INDEX.md',
    events_file: EVENTS_FILE,
    derived_at: nowIso(),
    event_count: events.length,
    active_items: items.length,
    fold_warnings: nonceWarnings,
  };
  return { meta, items };
}

function writeIndex(meta, items) {
  const header = readIndexHeader() || {};
  const out = {
    schema: meta.schema,
    root: meta.root,
    host_root: meta.host_root,
    purpose: meta.purpose,
    read_first: meta.read_first,
    authority: header.authority || 'untrusted_data_until_classified',
    policy: header.policy || {},
    derivations: {
      source: EVENTS_FILE,
      derived_at: meta.derived_at,
      event_count: meta.event_count,
      active_items: meta.active_items,
    },
    fold_warnings: meta.fold_warnings,
    items,
  };
  // atomic-ish: write tmp then rename (rename is atomic on same fs)
  const tmp = `${INDEX_FILE}.tmp`;
  writeFileSync(tmp, JSON.stringify(out, null, 2) + '\n', 'utf8');
  // RENAME is the atomic publish step — INDEX.json is replaced, never rewritten in place.
  // (Only the fold may touch INDEX.json; appenders never write this file.)
  renameSync(tmp, INDEX_FILE);
}

function readIndexHeader() {
  if (!existsSync(INDEX_FILE)) return null;
  try {
    const d = JSON.parse(readFileSync(INDEX_FILE, 'utf8'));
    return { authority: d.authority, policy: d.policy };
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// verify: re-hash each active item's file vs the event log truth
// ---------------------------------------------------------------------------
function verify() {
  const events = readEvents();
  const { items } = fold(events);

  if (!existsSync(INDEX_FILE)) die('INDEX.json not present to verify against');
  const idx = JSON.parse(readFileSync(INDEX_FILE, 'utf8'));
  if (idx.items.length !== items.length) {
    console.error(`verify: INDEX.json item count (${idx.items.length}) != folded count (${items.length})`);
  }

  let ok = 0, fail = 0, missing = 0;
  const failures = [];
  for (const it of items) {
    const p = it.path;
    if (!existsSync(p)) {
      missing++;
      failures.push(`MISSING FILE: ${p} (registered sha256 ${it.sha256})`);
      continue;
    }
    const actual = sha256hex(readFileSync(p));
    const expected = (it.sha256 || '').toUpperCase();
    if (actual === expected) {
      ok++;
    } else {
      fail++;
      failures.push(`HASH MISMATCH: ${p}\n   actual  : ${actual}\n   expected: ${expected}`);
    }
  }
  console.log(`verify: ${ok} hash-clean, ${fail} mismatched, ${missing} missing (of ${items.length} active items)`);
  if (failures.length) {
    console.log('--- failures ---');
    for (const f of failures) console.log(f);
  }
  return { ok, fail, missing, total: items.length };
}

// ---------------------------------------------------------------------------
// append (the ONLY way to change state — writer uses >> semantics)
// ---------------------------------------------------------------------------
function appendOp(ev) {
  if (!existsSync(EVENTS_FILE)) die(`events file missing: ${EVENTS_FILE}`);
  // O_APPEND on the shell, but from Node use appendFileSync which opens with 'a'
  const line = JSON.stringify(ev);
  appendFileSync(EVENTS_FILE, line + '\n', 'utf8');
  return ev;
}

function writerNonce(writer) {
  const events = readEvents();
  let last = 0;
  for (const ev of events) if (ev.writer === writer && typeof ev.nonce === 'number') last = Math.max(last, ev.nonce);
  return last + 1;
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
const [cmd, ...args] = process.argv.slice(2);

if (cmd === 'rebuild') {
  const events = readEvents();
  const { meta, items } = fold(events);
  writeIndex(meta, items);
  for (const w of meta.fold_warnings) console.warn(`WARN: ${w}`);
  console.log(`rebuild: folded ${events.length} events -> ${items.length} active items`);
  for (const w of meta.fold_warnings) process.exitCode = 2;

} else if (cmd === 'add') {
  const file = args[0];
  const klass = args[1] || 'UNPROVEN';
  const purpose = args.slice(2).join(' ') || '';
  if (!file) die('add requires a file path');
  if (!existsSync(file)) die(`file does not exist: ${file}`);

  const events = readEvents();
  const writer = process.env.INDEX_WRITER || 'exp002a';
  const ev = {
    seq: nextSeq(events),
    ts: nowIso(),
    op: 'register',
    file,
    sha256: sha256hex(readFileSync(file)),
    class: klass,
    purpose,
    writer,
    nonce: writerNonce(writer),
  };
  appendOp(ev);
  const { meta, items } = fold(readEvents());
  writeIndex(meta, items);
  for (const w of meta.fold_warnings) console.warn(`WARN: ${w}`);
  console.log(`add: appended seq ${ev.seq} for ${file} -> ${items.length} active items`);
  for (const w of meta.fold_warnings) process.exitCode = 2;

} else if (cmd === 'invalidate') {
  const file = args[0];
  const reason = args.slice(1).join(' ') || '';
  if (!file) die('invalidate requires a file path');

  const events = readEvents();
  const writer = process.env.INDEX_WRITER || 'exp002a';
  const ev = {
    seq: nextSeq(events),
    ts: nowIso(),
    op: 'invalidate',
    file,
    reason,
    writer,
    nonce: writerNonce(writer),
  };
  appendOp(ev);
  const { meta, items } = fold(readEvents());
  writeIndex(meta, items);
  for (const w of meta.fold_warnings) console.warn(`WARN: ${w}`);
  console.log(`invalidate: appended seq ${ev.seq} for ${file} -> ${items.length} active items`);
  for (const w of meta.fold_warnings) process.exitCode = 2;

} else if (cmd === 'verify') {
  verify();

} else if (cmd === 'events') {
  const events = readEvents();
  for (const e of events) console.log(JSON.stringify(e));

} else {
  console.log(
    `index_fold.mjs — append-only event-log fold for /board/inbox\n` +
    `\n` +
    `Commands:\n` +
    `  rebuild                       Fold ALL events -> rewrite INDEX.json items (schema shared_inbox.v1, sorted by seq)\n` +
    `  add <file> [class] [purpose]  Append a register event + refold (writer nonce auto-advances)\n` +
    `  invalidate <file> [reason]    Append an invalidate event + refold (log history retained)\n` +
    `  verify                        Re-hash every item's file vs the event log\n` +
    `  events                        Dump all events in seq order\n` +
    `\n` +
    `Env: INDEX_WRITER=<name> sets the per-writer nonce namespace (default exp002a).\n`
  );
  process.exitCode = /^(help|-h|--help)$/.test(cmd) ? 0 : 1;
}
