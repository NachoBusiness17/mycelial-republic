# B2-309 QUEUE.md registration re-seal after the B2-255 rename sweep (2026-09-26)

## Verdict

LANDED. The QUEUE.md registration chain is confirmed unbroken across the
B2-255 rename sweep and extended to current bytes: the pre-sweep seal was
sha 392929B8A53D4795... (index seq 1789823567015749437, 2026-09-26T15:25:15Z),
the sweep landed 15:44:15Z, the first post-sweep register is seq
1789823567015749479 at 16:00:19Z, and 27 QUEUE.md-targeted registers exist
post-sweep (latest before this lane: 3E9ED4663398C272 at 20:05:46.662Z). This
lane appended a fresh whole-file re-seal register (seq 1790454146070911747)
sealing the current post-sweep bytes, naming the sweep as the semantic change
per LIVING_HASH_LAW section 5. The brief's falsifier is already void in the
best way: index_events holds 27 QUEUE.md registers after the sweep ts.

## Evidence file:line quotes

- watch/inbox/index_events.jsonl, pre-sweep: seq "1789823567015749437",
  ts "2026-09-26T15:25:15.247Z", op register, file
  burn_wave_20260926/QUEUE.md, sha256 392929B8A53D4795...; sweep ts from
  memory/burns/LEDGER.jsonl row "B2-255-queue-double-spend-sweep" ts
  "2026-09-26T15:44:15Z"; first post-sweep register seq "1789823567015749479"
  ts "2026-09-26T16:00:19.000Z"; count of post-sweep QUEUE.md registers
  between 16:00:19Z and lane start: 27; latest pre-lane register seq
  "1790452960608924164" ts "2026-09-26T20:05:46.662Z" sha 3E9ED4663398C272...
- This lane's re-seal: seq "1790454146070911747", file
  burn_wave_20260926/QUEUE.md, sha256 C224254E8EE9D284... (full 64-hex in
  the event), class BOARD, purpose naming pre-sweep sha, sweep ts, and the
  post-sweep chain. Note: QUEUE.md moved again between the lane's first
  measurement (A6F4056790CF905F...) and the append (concurrent lanes), and
  the seal captured bytes at its own append moment - which is the living
  law's expected behavior for a hot board, and the chain is what proves it.
- The semantic change being sealed: B2_255_double_spend_20260926.md line 44
  "Each renamed line, quoted verbatim (post-edit bytes...)" - 24 row ids
  rewritten in place.
- mag.shared_surface validate at close: ok false with hash-mismatch errors
  against INDEX.json on files this wave's lanes edited or others own
  (REFEREE_VERDICT_20260926.md, B2_12 files, FLEET_IMPRINT, INDEX.json
  itself...). This is the pre-existing B2-191 INDEX-staleness class
  (register-vs-append race across a 24-lane wave), not caused by the
  index_events append; QUEUE.md is NOT in the mismatch list.

## Work done

1. Enumerated all QUEUE.md registration events (36 total) from
   index_events.jsonl; located the last pre-sweep seal, the sweep ts, and
   the post-sweep chain; measured current sha.
2. Confirmed the brief's falsifier condition (no post-sweep register) is
   already void: 27 post-sweep registers, chain unbroken since 16:00:19Z.
3. Appended the whole-file re-seal register at current bytes with the full
   pre/post chain named in the purpose field (the add door in practice:
   the index_events append convention, validated shape per my other
   registrations).
4. Ran mag.shared_surface validate; reported its pre-existing red honestly
   (B2-191 class, QUEUE.md not among the mismatches).
5. Filed this receipt; LEDGER row; QUEUE row pointer; INDEX registration of
   the receipt.

## Falsifier

This receipt is inverted if any of the following holds: (a) index_events
shows a gap in QUEUE.md registers spanning the sweep ts (15:25:15Z to
16:00:19Z is the only 39-minute window; if a register emerges inside it with
a post-sweep sha, the chain reading changes); (b) the pre-sweep sha
392929B8A53D4795... is proven to differ from bytes that existed at 15:44:15Z
(a register between 15:25 and 15:44 would break my pre-sweep anchor);
(c) my re-seal event's sha stops matching any historical byte state AND no
newer seal exists (an unregistered rewrite happened after it).

## Bibliography closed

watch/inbox/index_events.jsonl (36 QUEUE.md events parsed; seqs and shas
quoted); memory/burns/LEDGER.jsonl B2-255 row (sweep ts);
watch/inbox/burn_wave_20260926/B2_255_double_spend_20260926.md (line 44, the
semantic-change description); watch/inbox/LIVING_HASH_LAW_20260926.md
section 5 (accepted from the brief as the governing rule);
mag.shared_surface validate output (quoted honestly). No network calls.
