# CANON HARVEST SCORE — 2026-09-06 (worker s5-canon, read-only scoring)

Queue item: "read/score in-flight grok X-harvest". Scored against
`watch/X_HARVEST_DOCTRINE_20260905.md`. All counts measured by direct parse, not memory.

## 1. Inventory (tri-state, measured on disk)

- Pass 1–4 working haul: `memory/runs/x_bookmark_harvest_20260905/` — ~50 files,
  **15,152,956 B**, mtimes 2026-09-05 13:17 → 15:46 (4 bounded passes, one afternoon).
- Banked copies: `corpus/canon/` — **154 files, 2,714,493 B**. cmp-verified byte-IDENTICAL
  to the working receipts (`x_canon_2025_pass3.jsonl` ≡ `x_canon_2025.jsonl`;
  `receipts_dec2025_mar2026.jsonl` ≡ `receipts_2025_dec.jsonl`).
  Contents: `x_canon_2026_fx/` 130 fx jsons + 1 stray top-level = 131 roots (2026-08-14 → 09-02);
  `x_canon_nachoquixotic_v1.jsonl` 116 rows (from 2022-11-25);
  `x_canon_2025_pass3.jsonl` 314 rows (2025-01-01 → 12-31, only 35/365 days, 1 day proven complete);
  `receipts_dec2025_mar2026.jsonl` 324 rows — Kirk (~16 mentions) + Rashomon (~10) receipts PRESENT;
  enumeration index 129 rows.
- Ponytail canon pin `memory/improve/sources/ponytail-2026-08-03/`: 156 files (excl .git),
  1,642,202 B — CONFIRMED, methodology repo, separate from the X haul.
- Tweet-content date span: 2022-11-25 → 2026-01-28.
- **"6/6 COMPLETE" = SUPPORTED** — `pass2_summary.md` per-item table: retrieved ≥ advertised
  on all six (1/1, 8/5, 166/120, 7/5, 33/12, 0/0), nested-branch gap honestly declared.
- **"215 reply bodies" = SUPPORTED** — `canon_folder_harvest.jsonl` parses to exactly
  **215** nested bodies (1+8+166+7+33+0). NOTE: the Sep-5 ZAI corpus audit called this
  UNPROVEN because it searched `corpus/` only; the bodies live in `memory/runs/`.
  Location gap, not a count gap.

## 2. Cite-gate spot check (3 canon tweets, seed 20260906)

| id | url | timestamp | capture method | verdict |
|---|---|---|---|---|
| 1986938246241145297 | yes | Fri Nov 07 2025 23:26:08 +0000 | retrieved_via: 4 doors | PASS |
| 2016455418927534109 | yes | Wed Jan 28 2026 10:16:50 +0000 | 4 doors incl. x_thread_fetch full-text (fxtwitter had truncated the poem) | PASS |
| 1910191971479458298 | yes | Thu Apr 10 2025 04:43:50 +0000 | 4 doors | PASS |

**cite-gate = 3/3.** Programmatic sweep: all 215 replies carry author handle + url + date.

## 3. Doctrine compliance (six clauses)

1. Automate STORAGE, not RETRIEVAL — **PASS.** Four discrete human-triggered passes
   13:17–15:46; walls (login wall, Chrome file-lock, 10/query cap) recorded and stopped,
   never forced; no loop/daemon artifacts.
2. Own content core; replies cited corroboration — **PASS.** 6 roots @NachoQuixotic;
   215/215 replies carry handle + url. Nothing laundered.
3. Cite-verify gate (second door before banking) — **PARTIAL.** Roots are multi-door
   (fxtwitter + x_thread_fetch + keyword_search + threadreaderapp on the Epstein
   self-thread). The 215 replies are single-door (x_keyword_search) with only aggregate
   cross-check. Per doctrine they must be flagged UNVERIFIED until second-doored.
4. One fingerprint, no auto-re-auth — **PASS.** `_cookie_copies/` one-time copy; dead
   OAuth token and login wall documented, sessions stopped; stderr logs empty.
5. Restore law — **PASS (vacuous).** Enumeration was read-only listing; no deck/folder
   mutation artifacts existed to revert.
6. Declared-glass falsifier — **UNPROVEN / IN-FLIGHT.** Method published in-repo
   (pass2_summary + harvest_2025_summary + doctrine card); the external 30-day
   declaration has not been fired.

**Score: 4 PASS, 1 PARTIAL, 1 UNPROVEN. RED LINE respected** (bounded, human-triggered,
no 24/7 ingestion loop).

## 4. Verdict

- The canon-folder harvest the queue item points at is **DONE**: 6/6 trees complete,
  215/215 bodies on disk with full citations, receipts in-cage, banked byte-identical.
- Still IN-FLIGHT elsewhere: the 2025 timeline (314 rows = 35/365 days sampled; resume
  pointers filed in `harvest_2025_summary.md`), clause-3 reply second-door, clause-6
  declaration. Rashomon/Kirk receipt stratum: COLLECTED.
- **CLOSE the queue item.** One handoff action for the next queue item (not a reopen):
  run the fxtwitter second door over the 215 replies before they enter any falsifier
  corpus — the only gap between "banked" and "banked clean" under clause 3.

---
BATCH5|s5|RECEIPT: haul=<154 files/2,714,493 B banked + 50 files/15,152,956 B working/2022-11-25→2026-01-28>, claims 6-of-6=<SUPPORTED>, 215-replies=<SUPPORTED>, cite-gate=<3/3>, doctrine=<4 PASS/1 PARTIAL/1 UNPROVEN of 6>, verdict=<CLOSE — handoff: fxtwitter second door on 215 replies before falsifier use>
