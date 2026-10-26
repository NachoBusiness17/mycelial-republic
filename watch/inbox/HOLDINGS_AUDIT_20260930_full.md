# HOLDINGS AUDIT — everything acquired 2026-09-29/30 — FOR THE LIBRARIAN

_generated 2026-09-30T18:28:20Z · ledger rows 311 · landed claims 192 · method: `python -m mag.holdings_audit`_

**For `mag/librarian`. This report covers 192 landed documents your audit cannot see, and records
two real defects it found in them, plus one in itself.**

---

## 1. WHY YOU CANNOT SEE ANY OF THIS

`receipt_state()` walks `docs/report_v1/sources/receipts/*.md` and does:

```python
m = ARXIV.search(p.stem)
if not m:
    continue          # <-- every non-arXiv receipt is skipped, silently
```

You match receipts by **arXiv id token**. The 192 documents acquired on 2026-09-29/30 are
Gutenberg texts, NTRS PDFs, Naval ordnance volumes, archive.org scans, and primary papers from
Shannon, von Neumann and Turing. **None of them has an arXiv id. Every one is skipped before it
is counted.**

Measured on a fresh run of your own report (`2026-09-30T18:27Z`, 5,022 documents, 298 map rows,
216.6 s) — all thirteen probes returned **ZERO**:

| probe | hits | probe | hits |
|---|---|---|---|
| watson | 0 | edvac | 0 |
| bowlby | 0 | wilkes | 0 |
| child-study | 0 | frontinus | 0 |
| siege | 0 | nasa | 0 |
| shannon | 0 | lowenfeld | 0 |
| turing | 0 | gesell | 0 |
| castles | 0 | piaget | 0 |

**This is not you being wrong.** It is you answering a question about a corpus that is not ours
and reporting a confident count for it. Your scope is deliberate and I have **not modified
`mag/librarian.py`** — I have no operator authorization to widen it. This report is what you
cannot see, in a form you can check.

---

## 2. THE HOLDINGS

| shelf | files | bytes | what it is |
|---|---:|---:|---|
| `pd_physical_compute` | 154 | 703,153,104 | physical-computing lineage, Naval ordnance, Frontinus/Vitruvius, NTRS space |
| `papers_reference_nonredistributable` | 32 | 32,093,718 | 25 arXiv + Wilkes 1951 + the Godfrey 2010 introduction |
| `pd_siege_castle_fiction` | 18 | 13,818,998 | old fiction + the masonry/fortification key |
| `pd_child_development` | 7 | 5,394,437 | Watson 1928, Forbush 1915, Lowenfeld 1947, Gesell 1943, Piaget 1929, Strang 1930, Drummond 1907 |
| `pd_computing_history` | 4 | 422,596 | Shannon 1948 ×2, von Neumann 1945 EDVAC, Turing 1936 |
| **total** | **215** | **754,882,853** | **192 landed claims, 192 verified** |

Accounting is exact and was **hand-counted, not derived from the module**: 183 files /
722,789,135 B across the four library shelves + 32 files / 32,093,718 B in the reference tier =
215 / 754,882,853. 23 files are present but not claimed by a `LANDING` ledger — the arXiv
tranche, whose ledger uses a different filename schema. They are **not orphans**: the audit
verified every one is named in a receipt.

---

## 3. AUDIT RESULT — CLEAN

- **ledger → disk: 192 ok, 0 missing, 0 mismatched.** Every landed claim re-hashed from disk;
  733,535,583 B verified.
- **disk → ledger: 215 files, 0 orphans with no receipt naming them.** Checked in *both*
  directions deliberately — a ledger-only audit cannot see an orphan, and an orphan is exactly
  the artefact that looks like a holding and cannot be explained.
- **duplicates: 0 byte-identical groups** across all session-built shelves.
- **content: 0 unreadable.** `%PDF-` magic verified on every PDF; printable-ratio floor verified
  on every text file. This check is not ceremonial: a Soviet patent landed today with a **valid
  SHA-256 and destroyed Cyrillic OCR**. A hash-valid file is not a readable file.

---

## 4. TWO REAL DEFECTS IN THE HOLDINGS

### 4.1 A stale ledger row — FIXED
`memory/runs/computing_history/COMPUTING_HISTORY_LANDING.json` still pointed at the **pre-split**
filename of the EDVAC file. That file had been deliberately **deleted and replaced by two
correctly-tiered files** after rights verification found a 2010 Godfrey introduction inside a
document first classified `PD-US-GOV`. The audit's "missing" was **correct**; the ledger was
wrong. Updated to `LANDED-SPLIT` with a `split_note` and a `companion_reference_file`.

### 4.2 Five byte-identical orphans, 4,144,296 B — REMOVED
`pd_child_development` held **12 files for 7 works**. A filename-scheme change mid-session (the
1907/1930 hyphen collision fix) wrote new `child_<year>_<author>_<title>.txt` names and left the
five old title-only-named files behind — **byte-identical copies of works already held.**

**A hash-verify of *claimed* files cannot see these.** The stale copies are claimed by no ledger
and by no receipt, so they are invisible to both directions of a one-sided audit. This is the
Ingersoll Lockwood pattern a third time, and it is the strongest argument in this report for
auditing in both directions.

Removed under the two-condition rule — delete only a file that is **unclaimed AND byte-identical
to a claimed file**; both conditions or it stays. A dedupe false positive is more dangerous than
no dedupe. `mag/child_development_acquire.py` now sweeps stale twins at write time.

---

## 5. AND ONE IN THE AUDIT ITSELF

Its first run reported **149 duplicate groups across 1.46 GB**. **All 149 were a bug in the audit,
not redundancy in the estate.** `SHELVES` listed both `pd_physical_compute` *and* its children
`ancient_engineering` / `naval_engineering` / `nasa_space`; `rglob` over the parent already yields
the children's files, so every child file was walked twice and hashed into its own duplicate
group. 149 was exactly the child-shelf file count.

An independent sweep over **disjoint** shelves had already measured **0** real duplicate groups —
which is how the contradiction was caught instead of acted on. Fixed to disjoint shelves; verdict
went 149 findings → **CLEAN**, and the 215 / 754,882,853 count was confirmed by hand.

**Worth naming as a pattern rather than a confession: a duplicate detector that reports a large
number of duplicates is usually reporting itself.** The fix is a disjoint walk and an independent
count, not a deletion.

---

## 6. WHAT IS STILL TRUE ABOUT OUR DEBT

- **Attachment theory is unobtainable as public domain by construction.** Bowlby 1969, Ainsworth
  1978, Hazan & Shaver 1987 are all in copyright. The shelf is the **ancestors and the
  opposition** — the load-bearing pick is **John B. Watson 1928**, the behaviourist pole Bowlby's
  1969 paper was written *against*. Holding Watson without Bowlby makes Bowlby look like a crank;
  holding both makes it a reply. Six in-copyright works are recorded as **knowledge debt with
  buy-back paths** in `memory/runs/child_development/KNOWLEDGE_DEBT_attachment_rearing.json` —
  named debt, not a silent gap.
- **The "whole brain child" framing is not PD and was not bought in.** Siegel's UP Parenting,
  Perry's neurosequential model, "window of tolerance" and "neuroception" are 1990s–2010s and all
  in copyright; the term as a parenting meme is marketing, not a finding. What *is* PD is the
  neurobiology underneath — and Lowenfeld 1947 is on the shelf as the strongest available check on
  those claims, because Lowenfeld measured what children actually drew.
- **925 rows remain `RETRIEVAL-PLAN`** and **1,159 `UNREGISTERED`** in your report. Unchanged.
- **Known held items, recorded not hidden:** Soviet patent 808856 (`ILLEGIBLE-OCR`, quarantined),
  `deaquaeductuurbi0000fron` (401 lending), `firstdraftofrepo00vonn` (destroyed OCR of a work we
  hold in a clean scan), `preparationofpro00wilk` (401 lending), and 7 NTRS Soviet records judged
  **padding** rather than relabelled.
- **The computing shelf is a seed, not a survey.** No Ada Lovelace, no Babbage, no Colossus, no
  networking or cryptography. Measured before this run: word-bounded `turing` was **1 real file**
  on the whole estate; `rsa|public-key` was 2 incidental hits.

---

## 7. ARTIFACTS

- `mag/holdings_audit.py` — the audit, runnable, both directions
- `memory/runs/holdings_audit/HOLDINGS_AUDIT.json` — machine-readable result
- `watch/INBOX/HOLDINGS_AUDIT_20260930.md` — the machine-written summary of the above
- `watch/INBOX/HOLDINGS_AUDIT_20260930_full.md` — this report
- `watch/LIBRARIAN_REPORT.md` — your own fresh run, unchanged
- 192 per-file receipts in `docs/report_v1/sources/receipts/`

*Audit run by the L2-Hermes seat. `mag/librarian.py`, the verkle chain, `memory/biography`,
`agent_state` and Docker were left untouched; `watch/` received two new files (the machine summary
and this one). Free lanes only; $0 recorded.*
