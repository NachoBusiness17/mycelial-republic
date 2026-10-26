## Verdict

steal

## Evidence

Reader chain for bond rows, byte-read 2026-09-28:

1. Display render (write side): mag/bonds.py:384 `_format_md(pack)` writes the Related runs section into bonds_active.md at lines 438-453; row template line 449 carries the seat label verbatim: ``f"- **{r.get('run_id')}** seat=`{r.get('seat')}` · "``. Rows come from `list_related_runs(last_n=6)` at bonds.py:294, unfiltered by seat at ingest.
2. Loaders: mag/bonds.py:473 `load_bonds_text` returns BONDS_MD verbatim (476); mag/bonds.py:479 `load_bonds_json` loads bonds_active.json.
3. Pack assembly: mag/context_pack.py:601-603 reads both; the landed seat filter sits at 603. Grep of every `bj` use in the file: 595, 602, 603, 605-607, 630. `bonds_meta` (604-609) emits session_id, n_loops, n_bonds only; line 630 consumes open_loops only. `bj["related_runs"]` after the filter has NO consumer: the filter is a no-op on emitted output today.
4. Emitted surface: mag/context_pack.py:865 return dict `"bonds": bonds_text or ...` (string truncated, source continues with a fallback literal) is the de facto related_runs reader surface, and it is UNFILTERED, sourced from the ingest-time md.
5. Minor readers: mag/story.py:55-58 (load_bonds_json, open_loops only), mag/modules.py:216 (doctor file check), mag/tapestry.py:74 (reads memory/runs/related_runs.jsonl directly, lab surface, not the bonds file).

Recommendation: (a), the existing reader plus the pack's new filter. `_format_md` / `load_bonds_text` / return field `bonds` already carry seat-labeled rows to every pack reader; a new tiny production reader (b) would duplicate `load_bonds_json` as a third surface, which is fallback-branch creep. Honest caveat: (a) is complete only once the filtered rows gain an emitter; the natural site is `bonds_meta` (context_pack.py:604-609), one line.

## Steal or Vacuous

Named reader surface (fleet canon): the pack's `bonds` field is the reader surface. Chain: seat argument -> context_pack.py:603 filter (in-memory, no emitter yet, owed) -> return dict 865 -> bonds_active.md via bonds.py:438-453, seat label at 449. NPC=SEAT identity persistence is readable today through this existing seat path; the only owed build is the one-line `bonds_meta` emitter that makes the 603 filter observable instead of in-memory only. No new reader surface is built.

## Falsifier

After one research trail close seeds a seat=research row: a cold reader runs `build_context_pack(seat="research")` and reads the return `bonds` field: the Related runs section must hold at least one row and every row must read seat=`research`. A second independent reader applies the 603 predicate (row seat equals research) to `bonds.load_bonds_json()` on bonds_active.json and must match name/state/purpose/last_result anchors with the text rows. `queue/lanes/research/runner_state.json` must carry seat=research. Falsified on anchor divergence, any foreign-seat row in the pack section, or any seatless cited registry artifact. Owed before run: the bonds_meta emitter line, so the pack clause is byte-checkable rather than text-grepped.

## Bibliography

- watch/inbox/BURN_world-models-multi-agent_20260927_g.md (read 2026-09-28)
- watch/inbox/BURN_world-models-multi-agent_20260927_e.md (read 2026-09-28)
- mag/bonds.py lines 290-296, 384, 438-453, 473-484 (read 2026-09-28)
- mag/context_pack.py lines 590-611, 865, plus full-file `bj` grep (read 2026-09-28)
- mag/story.py lines 52-60 (read 2026-09-28)
- mag/modules.py:216, mag/tapestry.py:74 grep trace (read 2026-09-28)
- WebSearch "bond file reader surface design multi-agent shared state 2026", 2026-09-28, thin: chemistry/concrete noise, closest snippet hits [File systems for agents](https://www.amplifypartners.com) and [Designing multi-agent pipelines with shared state](https://discuss.huggingface.co), snippet-level only, nothing read in full
