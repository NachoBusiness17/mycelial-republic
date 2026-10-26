# INSTRUMENT AUDIT - the librarian's matching vs the newest holdings

_gala librarian-expedition, division B, lane instrument-audit, 2026-10-01. Raw outputs:
`watch/inbox/gala_20260925/librarian-expedition/lanes/instrument-audit.check.txt` (263 lines).
Method note: every command run with `.venv/Scripts/python.exe` on the repo root, this session._

## 0. WHAT "TODAY'S ADDITIONS" ACTUALLY ARE (measured, not assumed)

- Files in the 5 holdings shelves with mtime >= 2026-10-01T00:00Z: **0** (222 shelf files total,
  222 pre-date today). The holdings shelves received nothing strictly today.
- The newest tranche the instruments have never verified: **7 persona_priorart papers**, landed
  2026-09-30T22:55-22:56Z (file mtimes + `memory/runs/persona_priorart/PERSONA_PRIORART_LANDING.json`
  `ts: 2026-09-30T22:56:03Z`), i.e. ~4.5h AFTER the last holdings-audit run (18:28:20Z). The 09-30
  audit never saw them; shelf count went 215 -> 222, exactly these 7.
- Today's corpus additions outside the holdings shelves: `corpus/steal/DESCENT_DAY1_STEAL_20261001.md`
  and the Ghidra tool drop (`corpus/tools/`, ~6,000+ files, mtime 2026-10-01T10:47-11:00Z).
- Ledger rows: 321 real rows across the 12 `*LANDING*.json` ledgers (577 was a double count: the
  `NTRS_LANDING*.json` glob re-matches 3 ledgers the `*LANDING*` glob already caught, 256 rows
  counted twice). 314/321 rows carry NO date string, so "what landed today" is NOT answerable
  from the ledgers; only file mtimes (this is defect N5 below).

Test set used: the 7 persona papers (the effective "new holdings" since the last audit), plus the
whole-receipts visibility census (257 receipts).

## 1. THE THREE INSTRUMENTS, RUN TODAY

| instrument | command | result |
|---|---|---|
| mag.librarian v1 | `python -m mag.librarian` | 5,608 docs, 299 rows; UNREGISTERED 1,512; DUST 12; exit 1. Fresh `watch/LIBRARIAN_REPORT.md` rewritten by the run. |
| mag.holdings_audit | `holdings_audit.audit()` called directly (main() NOT called: `OUT_MD` is hardcoded to the dated 09-30 receipt, `mag/holdings_audit.py:63`, and running it would clobber that receipt) | 321 rows, 201 landed claims, 201 ok / 0 missing / 0 mismatch, 752,370,614 B re-hashed, 222 shelf files, 0 dup groups, 0 unreadable, verdict CLEAN. |
| mag.librarian_catalog | `python -m mag.librarian_catalog --verify` and `--once` | canon manifest: **DRIFT, 4 of 205 hash rows drifted**; 11 curated shelves, 89,831 files / 14.93 GB counted. |

## 2. THE THREE KNOWN DISEASES, RE-TESTED

### D1 arXiv-id-only matching: PRESENT, live, and BROADER than documented
- The 09-30 audit framed it as "none has an arXiv id". The persona tranche **has** arXiv ids in its
  stems and is still invisible: `ARXIV = \b(\d{4}\.\d{4,5})\b` (`mag/librarian.py:34`) does not fire
  on `persona_priorart_2405.07248` because `_` is a word character, so there is no `\b` before the
  id (probe 1 in the check file: NO MATCH on all persona stems; MATCH on bare `0706.1347`).
- `receipt_state()` (`mag/librarian.py:107-111`) sees **28 of 257 receipts**; **229 are blind**.
  The 7 persona receipts: 0 seen.
- The same ids DO match inside the receipts' text (space/colon-delimited there), so all 7 appear in
  the fresh report only under UNREGISTERED ("map behind the desk"): lines 506-842 of
  `watch/LIBRARIAN_REPORT.md`, e.g. `arxiv:2405.07248 <- docs\report_v1\sources\receipts\persona_priorart_2405.07248.md +1`.
  The instrument reports its own holdings as citation debt.
- The 13 classic probes (watson, bowlby, child-study, siege, shannon, turing, edvac, wilkes,
  frontinus, nasa, lowenfeld, gesell, piaget) are STILL ALL ZERO in the 2026-10-01 fresh report.
- **Miss count for the newest tranche: 7/7 to D1.** Whole-census blind count: 229/257 receipts.

### D2 duplicate detector reporting itself: bug ABSENT in today's run, mechanism CONFIRMED reproducible, guard is a comment not a check
- Today's run over the disjoint shelves: 0 duplicate groups (correct; the persona PDFs are 7
  distinct papers, and the 09-30 five-orphan removal held).
- Sensitivity (temp repro R3a): a planted byte-identical twin IS caught exactly once
  (`DUPLICATE-GROUP 8d26a8a0c64a`).
- Self-report mechanism (temp repro R3b): listing a parent shelf and its child reproduces the
  09-30 disease exactly - phantom groups == child file count. Nothing in the code enforces
  disjointness; `mag/holdings_audit.py:66-79` is a comment claiming "DISJOINT BY CONSTRUCTION".
  The detector still cannot see its own overlap. Verdict: contained, not cured.

### D3 valid hash, destroyed content: PRESENT in librarian_catalog, PARTIAL in holdings_audit
- `verify_canon()` (`mag/librarian_catalog.py:123-146`) is hash-only: repro R2 returns
  `ok: true, drifted: 0` for a 4,096-null-byte file whose hash is in the manifest. No magic-byte
  or readability check exists anywhere in the catalog instrument.
- `holdings_audit`'s PDF check reads only 8 bytes of magic (`mag/holdings_audit.py:155-158`):
  repro R4 passes a `%PDF-1.7` header followed by 100,000 null bytes as CLEAN (hash matches, 0
  unreadable). The `.txt` printable-ratio floor is real (it caught the Soviet patent on 09-30);
  the PDF-side floor is magic-only.
- Today's live canon drift (4 files: `_retired/x_canon_nachoquixotic_v1.jsonl`,
  `x_canon_2026_fx/fx_2094770591702098071.json`, `x_canon_2026_fx/fx_2096341325960417585.json`,
  `x_canon_enumeration_index.jsonl`) is genuine drift the catalog instrument correctly flags
  (manifest sealed 2026-09-22; heads are readable `{"url":`/`{"code":` JSON, so NOT D3 cases, but
  unexplained byte changes on canon paths - resolve before the expedition trusts canon).

## 3. NEW DISEASES (all with repro in the check file)

- **N1: `verify_canon()` crashes on a missing canon file.** The `missing` counter
  (`mag/librarian_catalog.py:145`) is dead code: `fp.read_bytes()` at :141 is uncaught, so a
  manifest row naming a deleted file raises FileNotFoundError out of `--verify`/`--once` instead
  of reporting `missing: 1`. Repro R1: `crashed: true, FileNotFoundError`.
- **N3: hardcoded-scope blindness; the three instruments' shelf lists disagree and none covers
  today's additions.** `papers_reference_nonredistributable` is in `holdings_audit.SHELVES`
  (`mag/holdings_audit.py:73-79`) but NOT in `librarian_catalog.CURATED`
  (`mag/librarian_catalog.py:35-47`): the catalog instrument cannot see the 39-file reference
  tier at all, per-file or as a count. `corpus/tools/` (today's ~6k-file Ghidra drop) is in
  neither, and the corpus FTS catalog has **0 rows** for it (752,984 rows scanned, probe 4) and
  **0 rows** for the persona papers. Today's largest acquisition is invisible to every record
  instrument simultaneously.
- **N4: the holdings audit's output path is a dated hardcode.** `OUT_MD = watch/INBOX/HOLDINGS_AUDIT_20260930.md`
  (`mag/holdings_audit.py:63`): every future run silently overwrites the 09-30 dated receipt with
  new data. I avoided running main() for exactly this reason.
- **N5: landing ledgers carry no per-row date** (314/321 rows contain no date string): "what
  landed today" is not answerable from the ledger; only mtime inference works. (Minor, but it is
  why the tranche boundary had to be derived from mtimes in section 0.)

## 4. TRUE CATALOG STATUS OF THE NEWEST TRANCHE, AFTER DEFECT-AWARE MATCHING

Per-file matrix (matcher output, check file section 4), 7/7 persona papers:

| channel | result |
|---|---|
| on disk + sha matches PERSONA_PRIORART_LANDING.json | 7/7 |
| PDF magic `%PDF-` | 7/7 |
| receipt on disk naming it | 7/7 |
| ledger claim | 7/7 |
| receipt_state() (librarian v1 holdings channel) | **0/7** |
| visible to librarian v1 at all (as UNREGISTERED citation) | 7/7 (false-positive channel) |
| librarian_catalog shelves | **0/7** |
| corpus FTS catalog rows | **0/7** |
| semantic-title channel (ledger title, first 8 salient words, in receipt text) | 7/7 |

Semantic-title recovery over the whole blind census: **38 of the 229** blind receipts carry a
LANDED ledger title match in their first 20,000 chars (channel bounded to ledger-row titles;
receipts with no titled LANDED row are unrecoverable by this channel and stay counted blind).

**Verdict: the holdings are clean and byte-true; the catalog as a record of the record is blind
to them.** The gathering expedition can trust the bytes (holdings_audit both-direction, CLEAN
today) but must not trust `mag.librarian` counts or `mag.librarian_catalog` shelf coverage as
visibility claims: use ledger-title semantic matching + both-direction audit as the matching
organ, never the id-token regex alone.

## 5. ARTIFACTS

- `watch/inbox/gala_20260925/librarian-expedition/lanes/instrument-audit.check.txt` - raw outputs, all commands
- `watch/inbox/gala_20260925/librarian-expedition/lanes/instrument_matcher_repros.py` - the matcher + repro script (R1-R4)
- `watch/inbox/gala_20260925/librarian-expedition/lanes/matcher_repros_out.json` - its JSON output
- `watch/inbox/gala_20260925/librarian-expedition/lanes/holdings_audit_today.json` - today's both-direction audit result
- `watch/LIBRARIAN_REPORT.md` - fresh 2026-10-01 librarian run (rewritten by the instrument itself)
- `CORPUS_CATALOG.md`, `state/library/catalog.jsonl`, `catalog_runs.jsonl` - rewritten/appended by `librarian_catalog --once` (its designed output)

## 6. HONESTY NOTES

- I did NOT modify `mag/librarian.py`, `mag/holdings_audit.py`, or `mag/librarian_catalog.py`.
  The 09-30 auditor declined to widen `mag/librarian.py` without operator authorization; same
  restraint here. All repros run in temp dirs with module constants monkeypatched in-process.
- `tools/violation_ratchet.py check --changed` exit 1 (2 NEW rows: `tools/hermes_burn.py:393`,
  `tools/model_garden.py:446`). This lane authored no byte under `mag/` or `tools/` - those files
  carry concurrent edits from other lanes on this shared working tree (mtimes 23:02/23:16Z inside
  this lane's window; my writes are only the watch/inbox paths listed above). The debt is real and
  named, and it is not this lane's.
- Not run: `mag/holdings_audit` main() (would clobber the dated 09-30 receipt, N4); the 200k-file
  `max_files` cap in `shelf_row` (`mag/librarian_catalog.py:65-91`) was code-read as a latent
  truncation defect but no current shelf approaches 200k files (max curated shelf 89,831), so it
  was not exercised on live data.

*Free-lane work, $0. No code under mag/ or tools/ touched by this lane.*
