---
name: burn-wave-engineering-patterns-20260927
description: 9/26-27 flash-lane burn invented four reusable engineering patterns
  under pressure — schema registry with both-side gates, guard-pin maintenance
  law, dormant flag gate, sort-totality key for mixed-precision event logs;
  plus the receipt-ghost and checkbox-desync diseases
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

The 9/26-27 flash-lane burn (422 briefs, 12-lane swarm + dispatcher, ~1.2B tokens) invented three engineering patterns under pressure that generalize beyond this session:

1. **Schema registry with both-side gates** (B2-342): pin writer keys with census count, first-seen seq (decimal string past 2^53), and owning writer; arm a validate-side ERROR for new keys and a fold-side WARN for unknown keys. Born when 30 event writer keys were found unowned.

2. **Guard-pin maintenance law** (B2-259): when a generator lane lands and a pin check (check7) fails, the lane must re-audit every differing row against source bytes and re-derive pin constants from that audit — never delete pins to get green. Born when B2-242's restores legitimately moved pinned rows.

3. **Dormant flag gate** (B2-133): one reader of a `dormant: true` flag in config gates all consumers; operator GO flips the flag and every gate restores with zero code edit. Applied to cerebras across seven mag/ files in one lane.

4. **Sort-totality key for mixed-precision event logs** (B2-279/B2-280): when an event log mixes exact decimal-string seqs, past-2^53 numeric doubles, and null-seq events, a naive Array.sort is non-transitive and last-register-wins becomes sort-luck refold to refold. Fix: three-tier total-order key (tier 0 null-seq by (ts, file order), tier 1 inexact doubles demoted below all exact seqs with counted warning, tier 2 exact decimal strings by BigInt) plus a migration that re-pins every band-winner at a fresh exact seq. Proven live: 561 band events censused, 231 re-pinned, 35 stranded items rescued, refold-stability test 5x clean.

Two diseases named and countered:
- **Receipt ghosts**: lanes complete but receipts get erased by concurrent whole-file restores (B2-328 disease class); fix = verify-only resolution (file exists, sha matches) before reconstruct-or-retire.
- **Checkbox-receipt desync**: rows flip [x]→[ ] or [ ]→[x] by racing processes with no receipt; fix = B2-238 law (landing earns check) + B2-251 audit sweep.

5. **Git-smudge CRLF diagnostic** (B2-243): when a ledger's bytes change but only in line endings (LF→CRLF), and the LF content exists as a dangling blob in the object store while no blob holds the CRLF form, it's `core.autocrlf=true` smudging on checkout/stash-pop — not a rogue writer. Prove by normalizing the old content (strip CR) and sha-comparing to the new bytes; if identical, exonerate all writers. Fix: add bytes-level LF-only assertion to the verifier (check8 pattern) and `.gitattributes` binary/-text for sha-cited files.

**How to apply**: these patterns generalize to any fleet or agent system that needs coordinated state management under concurrent writes. The schema registry works for any append-only log; the guard-pin law works for any assertion-bytes system; the dormant gate works for any feature-flag consumer network; the sort-totality key works for any event-sourcing log that mixes seq precision or carries null-seq events; the git-smudge diagnostic works for any byte-cited file on a repo with autocrlf enabled.
