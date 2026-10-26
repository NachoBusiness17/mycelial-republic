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
 *
 * Fold warnings (2026-09-26 B2-40): OUTSIDE_RE drops used to be SILENT. The 09-26 boot
 * lane's bulk registration wrote 235 register events starting watch/ that all vanished
 * from INDEX.json with no signal (B2_02 receipt, defect 1; plus 1 memory/ stray).
 * Dropped register events are now counted per top-level path segment and reported as
 * fold_warnings on the existing WARN + exit-2 channel.
 *
 * Seq scheme (2026-09-26 B2-40): float64 cannot add 1 past 2^53, so the old nextSeq
 * returned one constant forever once the log crossed 2^53: every node append on 09-26
 * emitted seq 1789823567015749400 (559 events in the 1789823567* family of
 * index_events.jsonl; `max + 1 === max` verified in node v22). Arithmetic now runs in
 * BigInt: seq is a plain JSON number while it fits 2^53-1 and a decimal STRING beyond
 * (JSON.parse keeps every digit of a string, none of a past-2^53 number). Events
 * without a usable seq (the md_record_seal.py hook appends none) keep ordering by ts.
 *
 * Sort totality (2026-09-26 B2-279): the B2-40 comparator compared seq-carrying
 * events by BigInt seq and fell through to ts for everything else, which is NOT
 * a total order (counterexample: A seq 2 ts early, B no-seq ts mid, C seq 1 ts
 * late gives C<A<B<C), so within the 2^53 quantization band (raw literal
 * 1789823567015749400 family, gala batch 1789823567015749473-477, all parsing
 * to one double) last-register-wins was decided by sort luck refold to refold:
 * B2-254 measured QUEUE.md and phone_relay_log.jsonl flipping failing to living
 * across four refolds with zero register events in between. Every event now
 * carries one total-order key: null-seq events key on (ts, file order) and sit
 * strictly below every seq event; integer Number seqs past MAX_SAFE_INTEGER
 * (the JSON.parse quantization band, ulp 256 at production magnitude) keep
 * their parsed BigInt but are demoted below every exact seq with a counted
 * fold warning; exact seqs (safe integers and digit-only decimal strings)
 * compare exactly via BigInt. Ties inside a tier fall to ts then file order
 * (stable sort), so the comparator is a lexicographic tuple order: total and
 * transitive. Owning brief: watch/inbox/burn_wave_20260926/QUEUE.md row
 * B2-279; receipt B2_279_sort_totality_20260926.md.
 *
 * Dump purity (2026-09-26 B2-329): readEvents attaches the fold plumbing fields
 * _outside and _unresolved to every parsed event in memory, and the `events`
 * command dumped each event as readEvents left it, so every dumped line since
 * B2-157 carried those fields and a strict downstream consumer rejected them as
 * unknown keys (falsifier: the dump piped through
 * watch/inbox/burn_wave_20260926/B2_329_dump_strict_consumer.mjs failed on
 * _outside x3442 pre-fix). The `events` command now strips every
 * underscore-prefixed field from its output: underscore is the reserved prefix
 * for fold-internal fields (the convention every future readEvents attachment
 * must follow, so one filter keeps the dump closed), and the dump carries only
 * writer-shaped event content. The LOG BYTES are untouched: the fields never
 * existed on disk (census over index_events.jsonl at sha
 * cfd3b2dde83b7dadf32e9b21cd54ef64a0fe6a4ab3e354a524c314b57953cec4: zero
 * underscore keys in 3439 parseable lines) and the dump is read-only. The fold
 * itself keeps using _outside/_unresolved; only the dump sheds them. Rebase
 * note: this block and the events-command filter were landed once at 16:33Z,
 * erased at 16:35:35Z by a concurrent stale-base whole-file write (the
 * B2-250 disease, claimed for this file at 16:06:18Z by B2-280 whose snapshot
 * predated the landing), and re-applied on the post-erase bytes named in the
 * receipt. Owning brief: watch/inbox/burn_wave_20260926/QUEUE.md row B2-329;
 * receipt B2_329_dump_strip_20260926.md.
 *
 * Key schema registry (2026-09-26 B2-342): the writer-key vocabulary of the
 * event log is load-bearing (the B2-329 dump purity law makes a strict
 * downstream consumer of the `events` dump reject any key outside it) and is
 * now owned by configs/events_key_schema.json: every key any writer ever
 * appended, with first-seen line, seq (decimal string per the B2-40 scheme),
 * ts and owning writer, census at a recorded log sha256. The vocabulary is
 * CLOSED, not required-fields: a registered key may always be omitted. Every
 * fold now warns on any event carrying a key outside the registry (one
 * warning per distinct key, with count and an example event) on the existing
 * WARN + exit-2 fold_warnings channel, and mag.shared_surface validate
 * ERRORS on the same keys, so a writer that mints a fresh key is named on
 * its next append+refold and fails the gate until the key is registered by
 * name or the writer is fixed. Underscore-prefixed fields are the reserved
 * fold-internal namespace (B2-329) and are exempt. Owning brief:
 * watch/inbox/burn_wave_20260926/QUEUE.md row B2-342; receipt
 * B2_342_schema_registry_20260926.md.
 *
 * INDEX_INBOX_DIR env (2026-09-26 B2-40): overrides the inbox root so tests can fold a
 * throwaway log; the default stays the host durable inbox (watch/inbox).
 *
 * Living-file law (2026-09-26 B2-156): append-heavy boards (QUEUE.md, LINKS.jsonl)
 * went sha-stale on every concurrent append, so verify cried wolf and writers
 * papered it with hash-refresh re-registers (LINKS.jsonl took 4 in 2 hours on
 * 09-26). Owning spec: watch/inbox/LIVING_HASH_LAW_20260926.md. A register event
 * may carry living:true + size:N where sha256 seals exactly the first N bytes;
 * verify hashes that sealed PREFIX, so append-only growth is LIVING OK (counted,
 * never a failure) while mutation or truncation of the sealed prefix still fails
 * hard. Living is writer-asserted per registration (add --living), never inferred
 * from class.
 *
 * Writer-side poison guard (2026-09-26 B2-147): add/invalidate DIE before appendOp
 * when the argv path, normalized by the fold's own normInboxFile, matches
 * OUTSIDE_RE or has no inbox-relative form, so no new outside event (watch/ or
 * repo-root poison) can be minted; the read side still folds and counts legacy
 * poison on the B2-40 warning channel, unchanged. One source of truth: the guard
 * and the fold share the same hoisted normalizer and regexes.
 *
 * Composed-prefix normalization (2026-09-26 B2-149 + B2-157): writers also mint
 * ABSOLUTE host paths. drift-patrol-cron registered
 * /board/inbox/C:/Users/.../watch/inbox/burn_wave_20260926/QUEUE.md
 * (index_events.jsonl line 3053): the board strip alone left
 * C:/Users/.../watch/inbox/... which OUTSIDE_RE cannot see (it tests
 * repo-relative segments only), so the register folded as a phantom item that
 * only Windows existsSync silently resolved, and verify hash-mismatched it
 * (B2_145_phantom_paths_20260926.md evidence section). Until this fix the
 * production fold stayed phantom-free only by JSON.parse quantization luck:
 * that event's past-2^53 seq literal 1789823567015749474 parses down to
 * ...376, just BELOW the exact string seqs of the B2-145 invalidates
 * (...380-384). The normalizer now strips the absolute host inbox root in the
 * same pass, so composed and bare absolute registers fold to their real
 * inbox-relative path, and any post-normalize residue that still fails the
 * inbox-relative check (drive letter, dot-dot, empty) drops with a fold
 * warning like the B2-40 outside-dropped class instead of landing as an
 * unresolvable item.
 */
import { createHash } from 'crypto';
import { readFileSync, writeFileSync, appendFileSync, existsSync, statSync, renameSync } from 'fs';
import { isAbsolute, join as pathJoin } from 'path';

const INBOX_DIR = process.env.INDEX_INBOX_DIR || 'C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox';
const EVENTS_FILE = `${INBOX_DIR}/index_events.jsonl`;
const INDEX_FILE = `${INBOX_DIR}/INDEX.json`;
const ROOT_MARKER = 'shared_inbox.v1';

// B2-157 2026-09-26: absolute host roots that normalize away. The env root
// (test/container inboxes) AND the compiled host default (so events minted on
// this host still resolve when folded under a different INDEX_INBOX_DIR).
// Forward-slash, no trailing slash, deduped.
const INBOX_ROOTS = [...new Set(
  [
    INBOX_DIR,
    'C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox',
  ].map((r) => String(r).replace(/\\/g, '/').replace(/\/+$/, ''))
)];

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

// B2-342 2026-09-26: the writer-key registry (configs/events_key_schema.json)
// is repo-level, so it resolves relative to THIS SCRIPT, never the (possibly
// env-overridden) inbox root: throwaway test inboxes gate against the same
// vocabulary as the production log. Loaded once per process.
const KEY_SCHEMA_URL = new URL('../configs/events_key_schema.json', import.meta.url);
let keySchemaState;
function loadKeySchema() {
  if (keySchemaState) return keySchemaState;
  try {
    const parsed = JSON.parse(readFileSync(KEY_SCHEMA_URL, 'utf8'));
    const keys = new Set(
      (Array.isArray(parsed.keys) ? parsed.keys : [])
        .map((e) => (e && typeof e.key === 'string' ? e.key : ''))
        .filter(Boolean)
    );
    keySchemaState = { loaded: keys.size > 0, keys };
  } catch (e) {
    keySchemaState = { loaded: false, keys: new Set(), error: String((e && e.message) || e) };
  }
  return keySchemaState;
}

// B2-147 2026-09-26: hoisted to module scope (were readEvents-local) so the
// WRITER side (add/invalidate) shares one source of truth with the fold's
// read side: the writer guard must normalize and classify with the exact
// bytes the fold will use, never a drifting copy.
// path normalizer (2026-09-19): writers mint many path styles; the fold is the one
// place they all get canonicalized — /board/inbox/x, /app/inbox/x, inbox/inbox/x -> x
const normInboxFile = (f) => {
  // B2-157 2026-09-26: canonicalize separators first (md_record_seal.py:51
  // defends its own writer side; the fold is the canonicalization point for
  // every writer). Log bytes were forward-slash-only at fix time (grep over
  // index_events.jsonl: zero backslash hits), so no historical fold changes.
  let p = String(f || '').trim().replace(/\\/g, '/').replace(/^\/+/, '');
  p = p.replace(/^(board|app)\/inbox\//, '');
  while (p.startsWith('inbox/')) p = p.slice(6);
  // B2-149 + B2-157: strip the absolute host inbox root in the SAME pass.
  // drift-patrol-cron minted /board/inbox/C:/Users/.../watch/inbox/
  // burn_wave_20260926/QUEUE.md (index_events.jsonl line 3053); board strip
  // alone left C:/... which OUTSIDE_RE cannot see, folding a phantom item.
  // Case-insensitive: drive letters and path case vary across writers.
  for (const root of INBOX_ROOTS) {
    if (
      p.length > root.length &&
      p.slice(0, root.length + 1).toLowerCase() === root.toLowerCase() + '/'
    ) {
      p = p.slice(root.length + 1);
      break;
    }
  }
  while (p.startsWith('inbox/')) p = p.slice(6);
  return p;
};
const OUTSIDE_RE = /^(mag|memory|queue|scripts|dashboard|docs|site|tests|models|backend|configs?|deploy|state|watch|research|corpus|dist_audit|attic|handoff|tools|bridge|harness|router|experiments|window|agents|.agents)\//;
// B2-157 2026-09-26: post-normalize inbox-relative check. A path that STILL
// carries a drive letter, a dot-dot segment, or nothing after normalization
// can never resolve as an inbox item (verify would report MISSING, or on
// Windows silently hash an absolute the same way the B2-145 phantoms duped
// bare rows). Those registers drop with a fold warning on the B2-40 channel.
const isUnresolved = (p) =>
  p === '' || /^[A-Za-z]:\//.test(p) || /(^|\/)\.\.(\/|$)/.test(p);

function readEvents() {
  if (!existsSync(EVENTS_FILE)) die(`events file missing: ${EVENTS_FILE}`);
  const lines = readFileSync(EVENTS_FILE, 'utf8').split('\n').filter((l) => l.trim() !== '');
  const events = [];
  const skipped = [];
  lines.forEach((line, idx) => {
    try {
      const ev = JSON.parse(line);
      if (typeof ev.file === 'string') ev.file = normInboxFile(ev.file);
      ev._outside = typeof ev.file === 'string' && OUTSIDE_RE.test(ev.file);
      ev._unresolved =
        typeof ev.file === 'string' && isUnresolved(ev.file) && !ev._outside;
      events.push(ev);
    } catch (e) {
      skipped.push(idx + 1);  // tolerant reader: keep folding over legacy junk (line 94, PENDING_CODEX)
    }
  });
  if (skipped.length) console.error('skipped malformed lines:', skipped.join(','));
  events.sort((a, b) => compareBySeqTs(a, b));
  return events;
}

// B2-40 2026-09-26 seq scheme: Number seqs are exact only under 2^53, and the
// scheme emits decimal STRING seqs beyond that (evidence: every 09-26 node
// append carried the same stuck literal 1789823567015749400 because float64
// `max + 1` was a no-op). B2-279 2026-09-26: seqOf is nextSeq's resume-max
// helper only (monotone over every parseable value, exact or quantized); the
// FOLD ORDER no longer uses it: ordering is seqOrderKey + compareBySeqTs
// below, which is a total order over exact strings, quantized doubles, and
// no-seq events (the old mix of BigInt seq compare with ts fallthrough was
// non-transitive; proof counterexample in the B2-279 header block).
// B2-190 2026-09-26 decision (audit + codify): the log held 561 raw
// number-literal seqs past 2^53 (latest line 3084, the B2-42 note,
// raw 1789823567015749478) and 491 decimal-string seqs past 2^53, every
// string above every literal, so the falsifier "a number-literal seq sorts
// after a later decimal-string seq" is FALSE under seqOrderKey (tier 1
// demoted below tier 2) and under raw value compare; the inexactWarnings
// channel (fold) plus this emission law are the pinned answer: WRITERS emit
// decimal strings past 2^53 (nextSeq below) and never raw number literals,
// the fold WARNs per fold on any tier-1 member still un-migrated. Quantize
// correction to the brief: at this magnitude ulp is 256, so EVEN literals
// quantize too (raw ...478 parses to ...376); only multiples of 256 are
// exactly representable.
const MAX_SAFE_SEQ = BigInt(Number.MAX_SAFE_INTEGER); // 2^53 - 1

function seqOf(ev) {
  const s = ev.seq;
  if (typeof s === 'number' && Number.isInteger(s)) return BigInt(s);
  if (typeof s === 'string' && /^\d+$/.test(s)) return BigInt(s);
  return null;
}

// B2-279 2026-09-26: one total-order key per event.
//   tier 0: no usable seq (autoseals, md_record_seal.py registers, legacy
//            nulls): keyed by (ts, file order), strictly below every seq
//            event;
//   tier 1: integer Number seqs past MAX_SAFE_INTEGER: JSON.parse already
//            quantized the raw literal (ulp 256 at production magnitude), so
//            the digits it kept are kept exactly as a BigInt, but the whole
//            band is demoted below every exact seq and counted on the
//            fold-warning channel (a chronologically-later exact-seq register
//            must outrank it for last-register-wins);
//   tier 2: exact seqs: safe integers and digit-only decimal strings,
//            compared exactly via BigInt.
// Never attached to events (BigInt does not JSON.stringify); the `events`
// dump stays clean.
function seqOrderKey(ev) {
  const s = ev.seq;
  if (typeof s === 'number') {
    if (Number.isSafeInteger(s)) return { tier: 2, seq: BigInt(s) };
    if (Number.isInteger(s)) return { tier: 1, seq: BigInt(s) };
    return { tier: 0, seq: null };
  }
  if (typeof s === 'string' && /^\d+$/.test(s)) return { tier: 2, seq: BigInt(s) };
  return { tier: 0, seq: null };
}

function compareBySeqTs(a, b) {
  const ka = seqOrderKey(a);
  const kb = seqOrderKey(b);
  if (ka.tier !== kb.tier) return ka.tier < kb.tier ? -1 : 1;
  if (ka.seq !== null && kb.seq !== null && ka.seq !== kb.seq) return ka.seq < kb.seq ? -1 : 1;
  // inside a tier: ts, then file order (items carry register_ts; events ts).
  // Equal keys resolve through ES2019 stable sort = file order, so the
  // comparator plus stability is a deterministic total order.
  const ta = a.ts || a.register_ts || '';
  const tb = b.ts || b.register_ts || '';
  if (ta < tb) return -1;
  if (ta > tb) return 1;
  const pa = a.path || a.file || '';
  const pb = b.path || b.file || '';
  if (pa < pb) return -1;
  if (pa > pb) return 1;
  return 0;
}

function nextSeq(events) {
  // BigInt end to end: float64 could not increment past 2^53, which is how every
  // node-appended event on 09-26 got the constant seq 1789823567015749400.
  // Emission stays a plain Number while it fits 2^53-1 (exactly representable)
  // and switches to a decimal string beyond, so appends never repeat a seq.
  // Legacy past-2^53 literals were already quantized by JSON.parse (ulp 256 at
  // that magnitude), so the counter resumes from the largest value the parser
  // can distinguish and is monotone from there.
  let max = null;
  for (const ev of events) {
    const s = seqOf(ev);
    if (s !== null && (max === null || s > max)) max = s;
  }
  const next = (max === null ? 0n : max) + 1n;
  return next <= MAX_SAFE_SEQ ? Number(next) : next.toString();
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
  // B2-40 2026-09-26: OUTSIDE_RE drops used to be silent. The fold discarded the
  // boot lane's watch/-prefixed registers (235 on 09-26 alone, B2_02 receipt defect 1)
  // with no trace beyond this dead local array. Dropped registers are now counted
  // per top-level path segment and surfaced as fold_warnings (WARN + exit 2).
  const outsideDropped = new Map(); // segment -> { events, paths }
  // B2-157 2026-09-26: same channel for registers that still fail the
  // inbox-relative check after normalization (drive letter / dot-dot / empty).
  const unresolvedDropped = new Map(); // segment -> { events, paths }

  // B2-279 2026-09-26: count the 2^53 quantization band members. They still
  // fold (they are valid events) but the total order demotes the whole band
  // below every exact seq, so a chronologically-later exact-seq register of
  // the same file now wins last-register-wins by LAW instead of sort luck.
  // Surfaced on the existing counted fold-warning channel like the B2-40
  // outside-dropped class so band members still owed a migration (B2-280)
  // are visible every fold.
  const inexactValues = new Set();
  let inexactEvents = 0;
  for (const ev of events) {
    const k = seqOrderKey(ev);
    if (k.tier === 1) {
      inexactEvents++;
      inexactValues.add(String(k.seq));
    }
  }
  const inexactWarnings =
    inexactEvents === 0
      ? []
      : [
          `inexact double seq events demoted below every exact seq: ${inexactEvents} event(s) ` +
            `across ${inexactValues.size} distinct parsed value(s) (e.g. ${[...inexactValues]
              .sort()
              .slice(0, 3)
              .join(', ')}): past-2^53 number literals quantize on JSON.parse ` +
            `(ulp 256 at this magnitude); re-register any band member that must win last-register-wins`,
        ];

  // B2-342 2026-09-26: warn on any event key outside the closed vocabulary
  // owned by configs/events_key_schema.json (spec + census in the registry;
  // mag.shared_surface validate ERRORS on the same keys). Underscore is the
  // reserved fold-internal prefix (B2-329): readEvents attaches _outside and
  // _unresolved in memory, written by no writer, so those keys are exempt.
  const keySchema = loadKeySchema();
  const unknownKeyWarnings = [];
  if (!keySchema.loaded) {
    unknownKeyWarnings.push(
      `events key schema registry missing or unreadable (${KEY_SCHEMA_URL.href}): ` +
        `${keySchema.error || 'no keys registered'}; unknown-key gate disabled for this fold`
    );
  } else {
    const unknownKeys = new Map(); // key -> { count, example event }
    for (const ev of events) {
      for (const k of Object.keys(ev)) {
        if (k.startsWith('_') || keySchema.keys.has(k)) continue;
        const rec = unknownKeys.get(k) || { count: 0, example: ev };
        rec.count++;
        unknownKeys.set(k, rec);
      }
    }
    for (const [k, rec] of [...unknownKeys.entries()].sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))) {
      unknownKeyWarnings.push(
        `unknown event key not in configs/events_key_schema.json: ${k} x${rec.count} ` +
          `(e.g. seq ${rec.example.seq}, writer ${rec.example.writer}): register the key ` +
          `by name with first-seen evidence or fix the writer; ` +
          `mag.shared_surface validate fails on it`
      );
    }
  }

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
      if (ev._outside) {
        const seg = `${ev.file.split('/')[0]}/`;
        const rec = outsideDropped.get(seg) || { events: 0, paths: new Set() };
        rec.events++;
        rec.paths.add(ev.file);
        outsideDropped.set(seg, rec);
        continue;  // repo files, not inbox items
      }
      if (ev._unresolved) {
        const seg = `${ev.file.split('/')[0]}/`;
        const rec = unresolvedDropped.get(seg) || { events: 0, paths: new Set() };
        rec.events++;
        rec.paths.add(ev.file);
        unresolvedDropped.set(seg, rec);
        continue;  // post-normalize path still fails the inbox-relative check
      }
      active = active.filter((it) => it.path !== ev.file);  // last register wins (hash refreshes)
      seen.add(ev.file);
      const item = {
        path: ev.file,
        class: ev.class || 'UNPROVEN',
        purpose: ev.purpose || '',
        sha256: ev.sha256 || '',
        seq: ev.seq,
        register_ts: ev.ts || '',
      };
      // B2-156 living-file law: sealed living carries (sha256, size) over the
      // file's first size bytes; open living carries seal:'open' with no byte
      // seal. Events without the flag keep the whole-file seal (item stays
      // flag-free so the JSON shape of static rows is unchanged).
      if (ev.living) {
        item.living = true;
        if (ev.seal != null) item.seal = ev.seal;
        if (ev.size != null) item.size = ev.size;
      }
      active.push(item);
    } else if (ev.op === 'invalidate') {
      const target = ev.file;
      if (!target) die(`invalidate event seq ${ev.seq} missing file`);
      invalidated.add(target);
      active = active.filter((it) => it.path !== target);
    }
    // 'note' events carry no state — they are log-only markers.
  }

  // Sort active items by seq (registration order) = canonical order, under the
  // B2-279 total order: exact seqs by BigInt, the 2^53 quantization band kept
  // but demoted below every exact seq, no-seq items (seal-hook registers)
  // keyed (ts, path) strictly below all seq items. Ties resolve through the
  // stable sort, so the canonical order is deterministic refold to refold.
  active.sort(compareBySeqTs);

  const items = active.map(({ seq, register_ts, ...rest }) => rest);

  const outsideWarnings = [...outsideDropped.entries()]
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
    .map(([seg, rec]) =>
      `outside-dropped register events excluded from items: ${seg} x${rec.events} ` +
      `(${rec.paths.size} distinct path(s)): register inbox files with an inbox-relative path`
    );

  const unresolvedWarnings = [...unresolvedDropped.entries()]
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
    .map(([seg, rec]) =>
      `unresolvable register events excluded from items: ${seg} x${rec.events} ` +
      `(e.g. ${[...rec.paths].sort()[0]}): post-normalize path still fails the ` +
      `inbox-relative check; register with an inbox-relative path`
    );

  const meta = {
    schema: ROOT_MARKER,
    root: '/board/inbox',
    host_root: '/board/inbox',
    purpose:
      'Single shared landing zone. INDEX.json is now DERIVED from the append-only event log ' +
      'index_events.jsonl (Ethereum fold pattern, EXP-002A). Writers APPEND events; they ' +
      'never rewrite this file or the log. The log is the source of truth.',
    read_first: '/board/inbox/INDEX.md',
    events_file: EVENTS_FILE,
    derived_at: nowIso(),
    event_count: events.length,
    active_items: items.length,
    fold_warnings: [...nonceWarnings, ...outsideWarnings, ...unresolvedWarnings, ...inexactWarnings, ...unknownKeyWarnings],
  };
  return { meta, items };
}

function writeIndex(meta, items) {
  const header = readIndexHeader() || {};
  const out = {
    schema: meta.schema,
    root: '/board/inbox',
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

  if (!existsSync(INDEX_FILE)) die(`INDEX.json not present to verify against (cwd=${process.cwd()}; INDEX root=${INDEX_FILE}; set INDEX_INBOX_DIR if the inbox root moved)`);
  const idx = JSON.parse(readFileSync(INDEX_FILE, 'utf8'));
  if (idx.items.length !== items.length) {
    console.error(`verify: INDEX.json item count (${idx.items.length}) != folded count (${items.length})`);
  }

  let ok = 0, livingOk = 0, livingOpen = 0, livingUnverified = 0, fail = 0, missing = 0;
  const failures = [];
  for (const it of items) {
    // B2-299 (2026-09-26): item paths are INBOX-RELATIVE (normInboxFile +
    // the B2-147 writer guard guarantee it at write time), but this loop
    // handed the raw string to existsSync, so it resolved against process
    // cwd: from repo root every file reported MISSING (observed 09-26:
    // 8+ MISSING lines from root, 0 from watch/inbox) and any runner would
    // chase phantom truncations. Resolve against INBOX_DIR; the cwd hint on
    // the INDEX die stays for the env-override case where the root itself
    // is wrong.
    const raw = it.path;
    const p = isAbsolute(raw) ? raw : pathJoin(INBOX_DIR, raw);
    // 2026-09-27: failure and info lines report `raw` (the registered
    // inbox-relative path), never the host-absolute resolution `p` — the
    // contract tests and mag.shared_surface validate both speak relative
    // names, and an absolute tmp path in test output hid the failing item
    // behind a wall of prefix (four living-law tests red on shape alone).
    if (!existsSync(p)) {
      missing++;
      failures.push(`MISSING FILE: ${raw} (registered sha256 ${it.sha256})`);
      continue;
    }
    const buf = readFileSync(p);
    const expected = (it.sha256 || '').toUpperCase();
    // B2-156 living-file law (spec: watch/inbox/LIVING_HASH_LAW_20260926.md).
    // Sealed living: the seal is (sha256, size) over the first size bytes.
    // Growth past the seal is the designed state of an append-only ledger;
    // mutation or truncation of the sealed prefix is still a hard failure.
    // Open living: edit-shaped board, no byte seal, counted only.
    if (it.living) {
      if (it.seal === 'open') {
        livingOpen++;
        console.log(`LIVING OPEN (no byte seal, log-carried integrity): ${raw}`);
        continue;
      }
      const size = typeof it.size === 'number' ? it.size : parseInt(it.size, 10);
      if (!Number.isInteger(size) || size <= 0 || !expected) {
        // Legacy living rows registered before the law named a shape; the
        // steady state is empty (re-register with a shape to clear).
        livingUnverified++;
        console.log(`LIVING UNVERIFIED (no size seal): ${raw}`);
        continue;
      }
      if (buf.length < size) {
        fail++;
        failures.push(`LIVING TRUNCATED: ${raw} (sealed ${size} bytes, file now ${buf.length})`);
      } else if (sha256hex(buf.subarray(0, size)) === expected) {
        livingOk++;
      } else {
        fail++;
        failures.push(`LIVING PREFIX MISMATCH: ${raw}\n   sealed prefix (${size} bytes) changed; file now ${buf.length} bytes`);
      }
      continue;
    }
    if (sha256hex(buf) === expected) {
      ok++;
    } else {
      fail++;
      failures.push(`HASH MISMATCH: ${raw}\n   actual  : ${sha256hex(buf)}\n   expected: ${expected}`);
    }
  }
  console.log(
    `verify: ${ok} hash-clean, ${livingOk} living-ok, ${livingOpen} living-open, ` +
    `${fail} mismatched, ${missing} missing, ${livingUnverified} living-unverified ` +
    `(of ${items.length} active items)`
  );
  if (failures.length) {
    console.log('--- failures ---');
    for (const f of failures) console.log(f);
  }
  return { ok, livingOk, livingOpen, livingUnverified, fail, missing, total: items.length };
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

// B2-147 2026-09-26 writer-side poison guard: add/invalidate used to MINT
// outside events verbatim from argv (the read side dropped them with fold
// warnings, but the append-only log still grew watch/ poison). The guard
// normalizes with the SAME normInboxFile/OUTSIDE_RE/isUnresolved bytes the
// fold uses and DIES before appendOp: no new outside event can be minted,
// while legacy poison in the log stays counted (the B2-40 read-side warning
// channel is unchanged). Spec: QUEUE row B2-147; pointer
// watch/inbox/burn_wave_20260926/B2_40_fold_poison_guard_20260926.md.
function writerGuard(file, op) {
  const p = normInboxFile(file);
  if (OUTSIDE_RE.test(p)) {
    die(`${op}: refusing to append an outside event: normalized path ${p} matches OUTSIDE_RE (B2-147 writer guard); inbox files only`);
  }
  if (isUnresolved(p)) {
    die(`${op}: refusing to append an unresolvable event: normalized path ${p} has no inbox-relative form (B2-147 writer guard)`);
  }
  return p;
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
  // B2-156 living-file law (spec: watch/inbox/LIVING_HASH_LAW_20260926.md):
  // --living seals (sha256, size) over the file's first size bytes (append-only
  // originals); --living-open declares an edit-shaped board with no byte seal
  // (its integrity is the event log + receipts). Mutually exclusive: one file
  // cannot be both growth shapes.
  const living = args.includes('--living');
  const livingOpen = args.includes('--living-open');
  if (living && livingOpen) die('--living and --living-open are mutually exclusive');
  const pos = args.filter((a) => a !== '--living' && a !== '--living-open');
  const file = pos[0];
  const klass = pos[1] || 'UNPROVEN';
  const purpose = pos.slice(2).join(' ') || '';
  if (!file) die('add requires a file path');
  if (!existsSync(file)) die(`file does not exist: ${file}`);
  writerGuard(file, 'add');  // B2-147: die before appendOp on outside/unresolved

  const events = readEvents();
  const writer = process.env.INDEX_WRITER || 'exp002a';
  // Read once: sha and size must describe the SAME bytes or the prefix seal is
  // meaningless (a concurrent append between stat() and read() would split them).
  const bytes = readFileSync(file);
  const ev = {
    seq: nextSeq(events),
    ts: nowIso(),
    op: 'register',
    file,
    sha256: sha256hex(bytes),
    class: klass,
    purpose,
    writer,
    nonce: writerNonce(writer),
  };
  if (living) {
    ev.living = true;
    ev.size = bytes.length;
  } else if (livingOpen) {
    ev.living = true;
    ev.seal = 'open';
  }
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
  writerGuard(file, 'invalidate');  // B2-147: die before appendOp on outside/unresolved

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
  // B2-329 2026-09-26 dump purity: readEvents attaches fold plumbing
  // (_outside, _unresolved) in memory; the dump is a downstream surface and
  // must carry writer-shaped event content only. Underscore is the reserved
  // fold-internal prefix, so one filter strips every current and future
  // internal field. Log bytes are untouched (the fields never existed on
  // disk); the fold keeps using them. Landed, erased by the 16:35:35Z
  // stale-base concurrent write, re-applied (header block names the rebase).
  // Pinned by tests/test_index_fold_host.py::test_events_dump_strips_fold_internal_fields
  // and falsified by watch/inbox/burn_wave_20260926/B2_329_dump_strict_consumer.mjs.
  const events = readEvents();
  for (const e of events) {
    const dump = {};
    for (const k of Object.keys(e)) {
      if (!k.startsWith('_')) dump[k] = e[k];
    }
    console.log(JSON.stringify(dump));
  }

} else {
  console.log(
    `index_fold.mjs — append-only event-log fold for /board/inbox\n` +
    `\n` +
    `Commands:\n` +
    `  rebuild                       Fold ALL events -> rewrite INDEX.json items (schema shared_inbox.v1, sorted by seq)\n` +
    `  add <file> [class] [purpose] [--living|--living-open]\n` +
    `                                Append a register event + refold (writer nonce auto-advances;\n` +
    `                                --living seals the first N bytes, --living-open declares an\n` +
    `                                edit-shaped board; LIVING_HASH_LAW_20260926.md)\n` +
    `  invalidate <file> [reason]    Append an invalidate event + refold (log history retained)\n` +
    `  verify                        Re-hash every item's file vs the event log\n` +
    `  events                        Dump all events in seq order\n` +
    `\n` +
    `Env: INDEX_WRITER=<name> sets the per-writer nonce namespace (default exp002a).\n`
  );
  process.exitCode = /^(help|-h|--help)$/.test(cmd) ? 0 : 1;
}
