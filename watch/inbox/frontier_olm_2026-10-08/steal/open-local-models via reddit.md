# STEAL CARD: open-local-models via reddit (frontier OLM 2026-10-08) - REV 3

Rev 2 of the round-1 draft. Lands the critique's fixes 1-4 and folds non-blocking 5-6.
Claims unchanged from rev 1 carry rev 1 receipts and were reproduced byte-for-byte by
the round-2 critique (its WHAT I VERIFIED block, part of the ask material); new claims
below carry fresh instruments run this sitting. Card law: banks the PORT, not the find
(precedent at watch/inbox/frontier_olm_2026-10-08/steal/open-local-models.md:6-8).

## The find (headline corrected per fix 3)

Ollama v0.40.1 (flagged Latest) and v0.40.2-rc0 (flagged Pre-release) landed
2026-10-08; v0.40.1 carries a Windows-only clef decision-head correctness fix. Rev 1's
headline asserted "v0.40.1 and v0.40.2 landed"; corrected here to the pre-release
naming because the headline is the sentence the next reader hand-copies.

- Releases list page, fetched this sitting: v0.40.2 is flagged Pre-release (08 Oct
  16:53, changelog range v0.40.1...v0.40.2-rc0, two changes: README community entry +
  "server: hide duplicate and downgrade guards from list"); v0.40.1 is flagged Latest
  (07 Oct 23:22, changelog v0.40.0...v0.40.1-rc0, seven changes incl. the clef and
  manifest bullets). https://github.com/ollama/ollama/releases
- Atom bytes (local byte-parse, no summarizer):
  watch/inbox/frontier_olm_2026-10-08/sweep/_raw/ollama_releases.atom: v0.40.1 entry
  :29-38 with "llama: fix clef head reads past 2GiB on windows by @Gigrise in #18777"
  (:36) and "manifest: avoid symlinks on Windows by @dhiltgen in #18852" (:38);
  v0.40.2-rc0 entry :8-27, atom title "v0.40.2" (:12), server bullet (:16).
- Mechanism (fetch-tier, WebFetch of https://github.com/ollama/ollama/pull/18777,
  re-fetched this sitting; carries the summarizer discount per the sweep's OWED 6
  discipline at sweep/open-local-models-reddit.md:256-258): verbatim, "The Windows
  llama-server ships with libc++ 18.1.8 (libc++.dll in the 0.35.1 release), where that
  seek truncates the offset to 32 bits"; clef.cpp head-weight loads past 2GiB land
  inside backbone weights, clef-flash (~10.0 GB blob, head tensors ~9.53 GB) feeds Q8_0
  backbone bytes to the head as float32, every /v1/systemone request on Windows fails
  "Clef: non-finite logit" on all backends (head always CPU); clef:27b unaffected
  (head below 2 GB); fix reads via ggml_fopen with an explicit 64-bit seek.

## Estate map: sovereign mirror + P3 digest gate + quantizer pin contract

Organ 1, SOVEREIGN MIRROR, and the held percolator row (fix 2, the reconciliation).

- Measured ground (rev 1 receipts, reproduced by the critique): daemon 0.34.3
  (`ollama --version`; `curl -s http://localhost:11434/api/version`), 15 models in
  `ollama list`, none clef-class. The clef-head bug is NOT live on this box today;
  exposure is CONTINGENCY, not active.
- The held row: memory/percolator/candidates.jsonl, ts 2026-10-02T04:17:43.293033Z,
  probe field verbatim (extracted by python filter on the ts this sitting): "Quiet-
  window Ollama 0.34.3 to 0.35 upgrade on the shared janitor host (rollback surface is
  the daemon binary; 15 model blobs persist), then step 0: one POST /v1/systemone
  batch of three named questions (one CHOICE, one SCORE, one NOUL) against tev1:0.8b".
  The same row's claim grounds the landing version: "Typed decision models landed
  natively in Ollama 0.35 (/v1/systemone; nimble 9B Bespoke Labs, tev1 4B and
  tev1:0.8b Together AI)".
- The conflict: PR #18777's own text names libc++.dll in the 0.35.1 release as the
  broken carrier. An operator firing the held row verbatim lands 0.35/0.35.x, whose
  Windows llama-server carries the broken libc++ for clef head reads past 2 GiB, and
  the new routing floor would then forbid exactly the Jev-class traffic that row
  routes.
- Reconciliation (the port): the held row's upgrade target moves from 0.35 to
  >= v0.40.1, superseded by reference to this card. >= v0.40.1 satisfies both the
  typed-decision door (the row's purpose) and the clef floor. The row's step-0 POST
  batch (tev1:0.8b, CHOICE/SCORE/NOUL) is unaffected and rides the upgraded daemon.
- Law row text, with the fix-6 scoping sentence inside it: "Any Jev-style decision-
  model serving on this Windows host requires daemon >= v0.40.1." Scope: PRECAUTION,
  not measured exposure: only head tensors past 2 GiB break (clef:27b unaffected per
  the PR), the estate's 0.5B-8B band makes that sub-class unlikely in-band, and the
  measured box state is 0.34.3 with zero clef-class models installed.

Organ 2, P3 DIGEST GATE (fix 1, honest re-attribution; fix 4, persistence + ritual).

- Re-attribution: arming is NOT a new port. It is the estate's own open OWED:
  watch/inbox/port_wave_20261007/p3_tag_digest.md:85-86 states "No digest is pinned
  yet on the fleet (the live run above is the proof); the operator pins via
  MAG_PIN_DIGESTS=\"gemma:2b=<hex>,...\" using the digests /api/tags reports", and
  :52-58 already ran the identical live verify rev 1 reported as its LIVE MEASUREMENT
  (exit 0, all three pins unpinned, warn printed once). Rev 1 reproduced a known
  state; it did not discover it. This card's NEW value is scoped to exactly two
  things: the urgency trigger below, and the both-direction falsifier probe below.
- Urgency trigger: v0.40.1 #18852 (manifest: avoid symlinks on Windows) and
  v0.40.2-rc0 #18874 (hide duplicate and downgrade guards from list) make the
  manifest layer the gate reads hot. The arming OWED and the daemon upgrade should
  land in the same window, because the post-upgrade GET /api/tags digest set is the
  correct pin source (pin before the upgrade and the upgrade itself manufactures the
  first refusal).
- Persistence (fix 4a): `rg -l "MAG_PIN_DIGESTS"` over the repo (frontier 10-08 banks
  and nul paths excluded) returns only mag/ollama_policy.py (reads it),
  tests/test_pin_digest_thinking.py (mocks it), and p3_tag_digest.md (instructs it).
  No repo file SETS it: a shell-scoped set is a probe, not an armed gate. Persistence
  is an operator call (owner framing per p3_tag_digest.md:86) between a user/machine
  environment variable and warm-boot injection; the gate is already wired to re-read
  on every --verify warm boot (mag/hermes_warm_boot.py:213-218 stamps
  state["pin_verify"] = verify_pins(), read this sitting), so a persisted variable is
  re-checked every boot with no further code. Plain non-verify boots do not gate, by
  design (p3_tag_digest.md:91-92).
- Refuse ritual (fix 4b): when verify_pins REFUSES (digest mismatch, or a pinned tag
  missing, mag/ollama_policy.py:132-140; refusal shape per p3_tag_digest.md:26-29),
  the rung stays refused; the operator re-pins ONLY from a fresh GET /api/tags digest
  after confirming WHY the digest moved (re-pull, re-tag, or upstream re-point), and
  files the re-pin receipt beside p3_tag_digest.md. Never auto-repin from the
  daemon's own answer: auto-repin would defeat the gate, whose founding case is the
  silent tag re-point (qwen3:4b aliasing qwen3:4b-thinking byte-identical manifests,
  mag/ollama_policy.py:21-25). Coverage for the refusal, sha256-prefix,
  not-installed, daemon-down fail-closed, and warn-once paths rides
  tests/test_pin_digest_thinking.py (17 tests, described at p3_tag_digest.md:62-66;
  file existence confirmed by the rg receipt this sitting).
- Live digests for probe step 1 (GET /api/tags, read this sitting): gemma:2b
  b50d6c999e592ae4f79acae23b4feaefbdfceaa7cd366df2610e3072c052a160; gemma4-desk
  8b8796e7d24b31599bf928c5e98ee9edf8085c00762b97922952aadcdb7a4a27; qwen-desk
  01b6981310d958ebc35a78ccfc35688346509c828c9e1189660b3e6b1d412d2a.

Organ 3, QUANTIZER PIN CONTRACT (non-blocking 5, slimmed to the new clause only). The
instrument amendment is the sibling card's find 1 port: owner
watch/inbox/frontier_olm_2026-10-08/steal/open-local-models.md:25-42, seven-pin
contract at watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md:91-96 (ollama
version is a pin), difficulty-hardened re-run OWED at :100-104 as its trigger. This
card adds one clause to that instrument: any daemon upgrade (0.34.3 -> >= v0.40.1) is
a serving-context move that re-opens the fired qwen2.5:7b tie, so the version pin must
move WITH the upgrade window, not before it.

## Probe (one, falsifiable, cheap; executes the P3 OWED rather than double-banking it)

1. (2 minutes, no daemon mutation) Set MAG_PIN_DIGESTS persistently (fix 4a
   mechanism, operator's choice of channel) using the three digests read from
   GET /api/tags this sitting, then re-run `.venv\Scripts\python.exe -m
   mag.ollama_policy --verify`. Expect ok true, matched == the three pins, exit 0.
   This executes p3_tag_digest.md:85-86; if it cannot pass, the gate's read path is
   broken and the OWED was underspecified (falsified in the boring direction).
2. (upgrade window) Re-run --verify BEFORE re-pinning, after the 0.34.3 -> >= v0.40.1
   upgrade. Falsifier runs both directions: a REFUSAL proves the gate catches the
   #18852 manifest-change class live (first true positive lands as the fix-4b ritual,
   not an incident); verify staying matched across a major daemon upgrade falsifies
   the manifest-layer bearing for this box and downgrades the port to the
   version-floor law alone.

## Overlap receipts (rev 1 instruments, reproduced byte-for-byte by the critique)

- `rg -i -c "0[.]40[.]1"` catalog/catalog.jsonl -> zero; control "0[.]40[.]0" -> zero;
  control "ollama" -> 1299. memory/ `rg -l -i "v0[.]40[.]1"` -> zero. watch/inbox hits
  only the two 10-08 sweep files. The find's named noise files
  (memory/cost/vast_charges.jsonl, memory/derived/derived_dag_index.json) -> zero. The
  sweep's 612 figure (sweep/open-local-models-reddit.md:222) is now contradicted by
  two independent greps (rev 1's and the critique's); correction belongs to the
  sweep's owner, carried here as unreproduced.
- New this sitting: `rg -l -i "0[.]40[.]1|version floor" memory/rib/` -> no output.
  No prior version-floor law exists; port 1 is not re-banked (checked per critique
  reject 1's standard).

## OWED (never asserted as fact)

1. PR #18777 mechanism is fetch-tier (WebFetch summarizer, discount per
   sweep/open-local-models-reddit.md:256-258); byte diff of llama/clef/clef.cpp before
   any of it routes a decision.
2. The clef/typed-decision landing version rides the held percolator row's own claim
   ("landed natively in Ollama 0.35") and the sweep's day-6 register rows
   (sweep/open-local-models-reddit.md:53-55); not independently verified by this seat.
3. No upgrade executed, no env var set (both operator-gated); the pin-arm probe is
   specified with step-1 receipts banked, not fired.
4. A clef-flash-class blob (~10 GB per the fetch-tier PR read) lands against the
   disk-floor tripwire (disk_free_floor_gb 15, commit 0b9980351); any clef pull is a
   disk-relief-cadence decision.
5. The 612 overlap figure is unreproduced by two independent greps; sweep-owner fix.
6. The persistence channel (user vs machine env var vs boot-script injection) and the
   held row's step-0 amendment are operator/owner calls; this card names the
   mechanism and the reconciliation, sets nothing, edits no held row.

## Receipt index (run this sitting)

- WebFetch: https://github.com/ollama/ollama/releases (Pre-release vs Latest flags);
  https://github.com/ollama/ollama/pull/18777 (libc++.dll-in-0.35.1 verbatim).
- Read: watch/inbox/port_wave_20261007/p3_tag_digest.md (full, 93 lines);
  mag/hermes_warm_boot.py:200-229 (pin_verify stamp at :213-218).
- Commands: python filter over memory/percolator/candidates.jsonl by ts 293033Z
  (1 row, probe + claim verbatim above); `rg -l "MAG_PIN_DIGESTS"` repo-wide (3
  files); `rg -l -i "0[.]40[.]1|version floor" memory/rib/` (zero);
  `curl -s http://localhost:11434/api/tags` (full digests above).
- Rev 1 instruments (version reads, --verify JSON, ollama list, catalog/memory
  greps) were re-run by the critique this round and matched byte-for-byte; not
  re-run here, cited as reproduced.

## REV 3 addendum (round 3, this sitting)

No claim changed from rev 2. The round-3 critique carries the same four rejects, all
already landed in the rev 2 body above: fix 1 = Organ 2 re-attribution (arming is the
P3 OWED at watch/inbox/port_wave_20261007/p3_tag_digest.md:85-86, prior identical live
run at :52-58); fix 2 = Organ 1 reconciliation (held row's 0.35 target moves to
>= v0.40.1, superseded by reference; PR's libc++.dll-in-0.35.1 carrier line quoted);
fix 3 = headline reads v0.40.2-rc0 (Pre-release); fix 4 = persistence mechanism +
refuse ritual in Organ 2.

New this round, from the critique's Note: the StealCard JSON returned in round 2 was
never persisted as this card's own file. The JSON beside this md,
open-local-models.json, is the SIBLING card's (read this sitting: area
"open-local-models", card_path names open-local-models.md, its own four-find content
intact; NO overwrite occurred). The whole steal/ directory is untracked
(`git status --porcelain` -> "?? watch/inbox/frontier_olm_2026-10-08/steal/"), so
nothing was committed or lost either way. This card's JSON is now banked as its own
file at watch/inbox/frontier_olm_2026-10-08/steal/open-local-models via reddit.json,
fields mirroring the sibling's shape (area, rev, banked, card_path, steal,
source_url, estate_map, probe, chars).
