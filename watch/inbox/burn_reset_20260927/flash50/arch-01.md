# arch-01: mag/context_pack.py pipeline map (what enters, what sheds, what reaches the model)

Date: 2026-09-28. Seat: mirror-arch-01 (flash50 burn reset). Source read in full this session via the Read tool: mag/context_pack.py, 1,362 lines / 54,863 bytes (verified: `.venv/Scripts/python.exe` splitlines + stat, probe output `file_lines: 1362`, `file_bytes: 54863`). The ask named "1,277 lines": that count is stale by 85 lines. Last commit touching the file: a23928aca 2026-09-27 22:53:18 -0400 (`git log -1 --format=... -- mag/context_pack.py`), which lands on top of 3eb6dc251 (quantizer delivery) and 0654e7638 (clip-ladder fix). All line numbers below are the current tree on branch mag/run-beta1-factory-build-audi-20260806T231709Z (working tree clean at session start).

Cross-reference: sibling receipt s2-08 (commit d8fa1f2d8) mapped this pipeline on 2026-09-27. This item re-derives independently from the current bytes. Where numbers overlap they corroborate (s2-08 "full mode assembled 27249 -> 4496 rendered"; this run measured 27,218 -> 4,496, consistent within tree drift). Where this run goes further it says so.

## 1. Entry surfaces (live grep this session)

Command: `git grep -n "build_context_pack\|format_context_pack_text\|format_agent_preamble\|infer_pack_mode\|freeze_system_prompt\|evolving_tail" -- mag tools scripts tests` plus a context_pack grep over main.py / mag/agent_cli.py / mag/coordination.py. Result: 17 build_context_pack call sites across 11 live-tree files (s2-08 counted 7 surfaces; the caller set has grown):

- main.py:3486-3505 (mag.cmd context-pack CLI)
- mag/agent_cli.py: 6 sites (965, 2590, 2592, 2820, 3002, 3030); TUI repack at 965-971 wires freeze_system_prompt (995) + evolving_tail (1000), the A2 byte-identical-prefix law (context_pack.py:430-440)
- mag/autorun_common.py:40-56 (autorun fast lane, fast=True, plus worker preamble at :56)
- mag/coordination.py:254-257 (2,400-char fallback pack)
- mag/decision_framework.py:274-277 (2,000-char excerpt)
- mag/dispatch.py:76-77, mag/dashboard_plugin.py:58+77, mag/operator_os.py:96-97, mag/refine_chain.py:181-183, mag/self_drive.py:67-70, mag/voice_handoff.py:184-187

Consumers split into two shapes: full pack text (format_context_pack_text) and the coarse worker preamble (format_agent_preamble, :1282-1362, cap 2,200 :1286).

## 2. Stage A: assembly (build_context_pack, :571-973)

Mode configs :52-146. Budgets: janitor 1,200 (:57), route 1,800 (:72), build 5,500 (:87), audit 7,500 (:104), plan 11,000 (:120), full 4,500 (:135). Note the paradox read straight off the config: "full" includes the most layers (resonance+trail+skills+ijl+heat+coordination+mirror_clue, :137-143) with the second-smallest budget, while "plan" includes nearly the same set (minus trail+mirror) with 2.4x the budget.

Sources read on every build (caps at read time), with render fate determined in Stage B:

| Source | Read at | Cap | Lines |
|---|---|---|---|
| latest_brief_text (mag/lanes) | :618 | max_brief 400-1200 | 592 |
| memory/live_from_grok.md | :619 | max_live (janitor: 0) | 619 |
| memory/attention.md | :620 | 600 | 620 |
| memory/operator_directives.md | :621 | 2,800 | 621 |
| queue/todo.md | :622 | 500 | 622 |
| bonds (ingest+text+json) | :630-647 | max_bonds 500-1600 | 632-637 |
| resonance top_cards n=3 | :649-663 | goal_hint 400 | 655-659 |
| open_loops (bonds, else keyword scan of brief) | :665-673 | 8 items x 160 | 666-673 |
| run_trail excerpt | :675-682 | 12 events / 1,600 | 680 |
| skills_for_job | :684-691 | 600 | 689 |
| ijl skill beads | :693-707 | 500 | 705 |
| verkle tip badge + dig census | :709-730 | cache TTL 3,600s | 528, 726 |
| checkpoint_restore | :733-740 | (per pointer) | 738 |
| agent_state excerpt | :742-759 | 900 | 748 |
| OPERATOR_CONTINUITY.md | :761-767 | 2,200 | 765 |
| nervous pack_excerpt | :769-775 | (dict) | 773 |
| behavioral leaf + decision tips | :777-797, :851-860 | 1,200 + 1,400 merged | 794, 858 |
| compass FRAMEWORK_BLOCK | :795 | 900 | 795 |
| tesuji wins | :799-817 | 900 | 815 |
| coordination activity + tripartite + peer | :819-842 | 900 + 700; 1,600 only in peer branch | 824, 830, 840 |
| mirror voice / clue chain | :863-868 | 600 / 500 | 867-868 |
| zeitgeist | :869 | 800 | 269 |
| build excerpt / scope card | :871-878, :880-882 | 4,000 / 2,500 | 873, 176 |
| RIB doctrine (43 files) | :935 | 2,800 | 305-340 |
| quantized laws (12 rows) | :917 | 1,800 + 7d staleness gate | 343-391 |
| proven moves / solved | :916, :918 | 8 / 10 rows | 394-427 |
| MAG_FULL_CONTEXT subchain mount | :954-972 | 48,000 default, clamp 8k-200k | 283-294 |

Read cost flags: `_clip` (:277-280) reads each whole file before slicing, so janitor's max_live=0 (:56) still pays a full read of live_from_grok.md for zero output; attention (600) and directives (2,800) are read in every mode but render only in plan/full heat and L0c respectively; `_rib_doctrine` (:312-340) opens all 43 memory/rib/*.md files on every build. The s2-08 finding that coordination pulls a 29.7MB shared_activity read is cross-cited from receipt d8fa1f2d8, not re-measured here (I did not open mag/coordination.py:121 this session).

## 3. Stage B: the render ladder (format_context_pack_text, :993-1279)

Render order when nothing clips (:1235): policy_full -> L1 bonds (:1159) -> L1b skills+ijl (:1166) -> L1c mirror/clue (:1179) -> L2b frozen BUILD (:1184) -> L2c scope (:1191) -> L2 trail (:1199) -> L3 task (:1207) -> L4 heat (:1222).

Inside policy_full: L0 header + tip/dirac/health lines (:1049-1060), then the UNCAPPED objective read (:1063-1068: `CURRENT_OBJECTIVE.md` read with `.strip()`, no length cap, no errors="replace"), then compiled laws (:1075-1080), then ctx_a (doctrine/full-subchain/proven/solved, :1091-1118, gate :1092 mode in plan/full/build/audit), then ns lines + agent_state line + models + bonds_meta (:1119-1125), then ctx_b (zeitgeist, agent_state, continuity, directives, behavioral, coordination, resonance, :1126-1157).

The ladder (:1238-1278), each rung appending a designed offload row via _emit_pack_offload (:34-49):

1. Drop L4 heat (:1238-1244).
2. Compact L3: brief to 800, loops to 5 (:1245-1260).
3. Drop the entire ctx tier at once: `policy_bare = policy + policy_mid` (:1269) sheds doctrine, proven, solved, zeitgeist, agent_state text, continuity, directives, behavioral, coordination, resonance together (:1261-1275).
4. Hard clip: `text[:max_chars-20]` (:1276-1278) cuts from the END, so the tail sections (trail, then L3 task) are what dies.

Measured funnel (probe 1, fast=True, six live builds 2026-09-28T23:43Z; total_chars = size entering each rung, from the rows my builds appended to watch/inbox/PACK_OFFLOAD.jsonl lines 832-858):

| mode | budget | assembled (T0) | after r1 | after r2 | after r3 | final | survives |
|---|---|---|---|---|---|---|---|
| janitor | 1,200 | 4,897 | 4,896 | 4,875 | 4,875 | 1,196 | 24.4% |
| route | 1,800 | 10,871 | 10,870 | 10,670 | 6,498 | 1,796 | 16.5% |
| build | 5,500 | 24,217 | 24,216 | 23,917 | 11,145 | 5,496 | 22.7% |
| audit | 7,500 | 20,785 | 20,784 | 20,584 | 8,713 | 7,496 | 36.1% |
| plan | 11,000 | 25,569 | 24,972 | 24,373 | (r3 resolves) | 8,728 | 34.1% |
| full | 4,500 | 27,218 | 26,621 | 26,022 | 10,377 | 4,496 | 16.5% |

Read together: rung 3 is the only big shed (12.8k-15.6k chars); rungs 1-2 in build/audit/janitor shed 1-300 chars (they fire on a 1-char overshoot, still appending ledger rows); rung 4 then destroys 1.2k-5.9k more from the tail. Only plan avoids rung 4, and it overshoots its shed, landing 2,272 chars under budget (11,000-8,728) with the whole ctx tier gone.

Section-reach census across the six live renders (probe flags `has_*` + probe 2 unit proofs):

| Section | Reaches the model |
|---|---|
| objective (L0b) | 6/6, but mid-word truncated in janitor+route (see D2) |
| compiled laws (L0b) | 4/6 (build/audit/plan/full); never janitor/route |
| nervous / tip lines | 6/6 |
| bonds (L1) | 4/6; dies to rung 4 in janitor/route |
| skills+ijl (L1b) | per cfg; build/audit/full yes |
| frozen BUILD / scope (L2b/c) | build/audit yes; protected ahead of bonds in rung rebuilds (:1241, :1259, :1274) |
| trail (L2) | 1/6 (plan only; rung 4 eats it elsewhere) |
| L3 brief/loops/todo | 1/6 (plan, compacted to 800-char brief) |
| L4 heat (live_tail+attention) | 0/6 (rung 1 everywhere) |
| doctrine (L0d) | 0/6 (rung 3 everywhere) |
| directives (L0c) | 0/6 (see D4) |
| continuity/behavioral/coordination/resonance/zeitgeist/proven/solved | 0/6 (rung 3) |

## 4. Stage C: downstream tails

- freeze_system_prompt (:452-489) + evolving_tail (:492-525) implement the session-prefix cache law; measured on the full-mode render: tail 4,645 chars vs 5,200 cap (:498), not clipped today; preamble 2,068 vs 2,200 (:1286), not clipped today. The tail's own clip (:523-524) emits no offload row, so a future tail clip would be silent.
- format_agent_preamble (:1282-1362) has no ladder, single hard clip (:1360-1361); trail text is pre-capped at 700 (:1315-1316).

## 5. Stage D: observability

PACK_OFFLOAD.jsonl (watch/inbox/, :16, :34-49) gains up to 4 rows per overflowing build with stage + shed names. My probe session: rows 831 -> 858 (27 rows: 23 from the six-mode loop, 4 from the downstream rebuild). s2-08 observed 799 -> 823 for its runs, same ~4/build drift. Probe 2 redirected PACK_OFFLOAD_FILE to the instrument-local `_arch01_offload_probe.jsonl` (7 rows) so the live ledger was not touched again. No downsampler or consumer of this ledger is referenced anywhere in this module.

## 6. Findings: information destroyed that should not be

- D1. The hard clip amputates the task. Rung 4 cuts from the end (:1276-1278) and L3 task is last in parts order (:1235 and every rebuilt parts list :1241/:1259/:1274), so in 5/6 live renders the model received no brief, no open loops, no todo (`has_task_brief=False` for janitor/route/build/audit/full; full rung 4 destroyed 5,881 chars entering at 10,377). The pack retains estate status while losing the job. Caveat: some callers re-inject the goal outside the pack (agent_cli.py:1000 evolving_tail carries goal; autorun_common.py:56 preamble carries goal[:300]), so seat-level blindness varies by caller; the pack's own L3 is gone.
- D2. Janitor and route budgets are smaller than one uncapped input. CURRENT_OBJECTIVE.md measures 2,198 chars today against budgets of 1,200 and 1,800 (:57, :72), and the objective is inserted with no cap (:1063-1068). The objective alone overflows both modes; rungs 1-3 cannot help; rung 4 clips mid-word inside the objective (janitor tail: "for what the mine provably c... (pack clipped)"; route tail: "load your knowledg... (pack clipped)"). Consequence measured: compiled laws (`has_compiled_laws=False`) never reach janitor or route seats, although the quantizer docstring (:344-353) names janitors as its audience and 3eb6dc251 placed laws after L0b precisely to survive the clip. The fix is dark on exactly the lowest tiers.
- D3. Rung 3 is all-or-nothing and overshoots. It drops the whole ctx tier (15,645 chars in full mode) regardless of how small the overflow is; plan shed the tier and then sat 2,272 chars under budget. Blocks that would have fit partially (doctrine alone is 2,800-capped) die wholesale. There is no per-block or partial-shed rung.
- D4. Operator directives reach the model 0/6, and the code comment claims otherwise. L0c renders only in plan/full (:1146), then rung 3 drops it even there (probe 2: DIRECTIVE_BODY absent from the post-rung-3 text). The rung 3 comment "Directive tier survives the ladder; only contextual history sheds" (:1262) is false for L0c: directives live in policy_ctx_b (:1146-1151), which policy_bare (:1269) discards. Only the objective and quantized laws, which live in `policy` proper, actually survive.
- D5. The RIB doctrine seam is dark at render time. _rib_doctrine builds all 43 entries (43/43 fit the 2,800 cap today, DRIVING_LADDER included, probe flag `driving_ladder_in_doctrine=True`) on every build (:935, 43 file opens), renders only in plan/full/build/audit (:1092), and rung 3 shed it in all six live renders: 0/6 reach. Alphabetical file order (:315) would make the cut priority-blind once entries exceed the cap, but today nothing is cut; the waste is 43 reads per build for zero render.
- D6. The objective read is crash-prone and unbounded. `read_text(encoding="utf-8")` (:1065) has no errors="replace", unlike _clip (:280); one non-UTF8 byte in CURRENT_OBJECTIVE.md raises inside format_context_pack_text with no try/except, breaking every pack render for every caller. Not induced this session (stated from code read, not run).
- D7. Read-then-clip waste with zero render: janitor reads live_from_grok at max_live=0 (:619 + :56); attention is read in all modes (:620) but rendered only in plan/full heat (:1230) and rung 1 dropped heat in all six renders (0/6 reach, measured); same fate for live_tail.
- D8. Wired-but-never-rendered keys, byte-verified. Quoted-key scan over the render region (lines 993-1362, both quote styles) returns zero hits for: compass_framework (built every build, :795/:925), checkpoint_restore (:733-740/:926), commands (:944-952), token_note (:891), layers (:893), resonance_cards raw (:929; only the resonance_l0e string renders, :1156-1157). Probe 2 confirms with marker bodies: COMPASS_BODY and CKPT_BODY absent even from a 200,000-char-budget unclipped render. This is the same wired-but-never-rendered disease the quantizer landing (3eb6dc251) named and fixed for laws; compass_framework is a live recurrence (900 chars of FRAMEWORK_BLOCK assembled per build for nothing).

## 7. Findings: noise preserved that should shed

- N1. Raw Python dict reprs ship as model-facing text: `- health: {...}`, `- models: {...}`, `- bonds_meta: {...}` (:1058, :1123-1124; probe 2 `dict_repr_lines` shows the literal rendered lines). bonds_meta also carries raw exception strings on failure (:647), so a bonds error prints an exception repr into the pack.
- N2. Exception text as content: ijl failure renders "(ijl skills: {e})" (:707); tip/agent_state/nervous/checkpoint failures render their error strings (:1013, :758, :775, :740). Visibility has value (the estate's visible-debt law), but raw exception reprs are noise where a one-line status would do.
- N3. Silent mode coercion and loose routing: _normalize_mode maps any unknown mode string to full (:149-151), so a typo silently gets the tightest multi-layer budget; infer_pack_mode routes any goal containing "audit" to audit mode (:984) and everything untagged to full (:990). The default path therefore lands in the mode with the largest assembly and 16.5% measured survival.
- N4. Rungs fire on 1-char overshoots and still append ledger rows (build/audit/janitor r1 shed exactly 1 char, measured above): ledger churn of ~4 rows per default build, 831 -> 858 in one probe session, no consumer named in-module.
- N5. The keyword open-loop fallback (:666-673) keeps only brief lines matching open/next/loop/re-read/check and caps at 8 x 160 chars; loops phrased otherwise are silently lost, and when bonds provide loops the brief scan is skipped entirely (:666-667). Meanwhile the always-rendered boilerplate (contract lines :1054-1055, commands block :944-952, dirac count :1057) survives every clip by virtue of position.

## 8. Checks run (exact commands, this session)

1. Full file read: Read tool on mag/context_pack.py (1,362 numbered lines shown; python splitlines 1,362; stat 54,863 bytes).
2. `git log --oneline -8 -- mag/context_pack.py` and `git log -1 --format="%H %ad %s" --date=iso -- mag/context_pack.py` -> tip a23928aca 2026-09-27 22:53:18 -0400.
3. Entry-surface greps (command quoted in section 1) -> 17 build sites / 11 files, listed above.
4. Probe 1: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_arch01_probe.py` -> per-mode budgets, assembled/rendered chars, stages fired, has_compiled_laws / has_objective / has_task_brief flags, rib 43/43 with DRIVING_LADDER included, objective 2,198 chars, quantizer flash rows 12, offload 831 -> 858, downstream tail 4,645/2,068 unclipped. Raw: _arch01_out.json.
5. Probe 2: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_arch01_probe2.py` -> quoted-key scan (dq+sq) over lines 993-1362; hand-built-pack proofs: unclipped build renders doctrine+directives+continuity+behavioral+coordination+zeitgeist+proven+solved (all true) while COMPASS_BODY/CKPT_BODY are absent even unclipped; rung-3 render (max_chars=5000) sheds exactly that tier while keeping LAW_BODY/BONDS_BODY/BUILD_BODY/BRIEF_BODY; janitor 1,200 render has no laws/brief/bonds and clips mid-objective. Raw: _arch01_out2.json.
6. Offload row attribution: `tail -12` / `sed -n 832,846p` on watch/inbox/PACK_OFFLOAD.jsonl parsed with the venv python -> the funnel table in section 3.
7. Dash scan: `python _arch01_probe.py dashscan <file>` on this receipt and both instruments -> em=0 en=0 on all three (final bytes re-scanned before commit).

## 9. Not run / limits

- I did not run the pytest suite (not part of this ask) and did not count tests.
- I did not induce the D6 UnicodeDecodeError crash; it is a code-read finding, labeled as such.
- The 29.7MB coordination read and the s2-08 assembled totals are cross-cited from receipt d8fa1f2d8, not re-measured; my own numbers stand on probe 1 alone.
- Probes ran with fast=True (:582, :600-617), so the non-fast sanity() probe and the residual census (:726) were not exercised; the funnel numbers are therefore the fast-lane numbers. Non-fast builds add the sanity probe and dig census but the ladder math is mode/budget-driven and identical.
- Line drift: the ask's "1,277 lines" and any line numbers in s2-08 predate a23928aca; this receipt's numbers are authoritative for the current tree only.

## 10. Instruments banked beside this receipt

- _arch01_probe.py (six-mode render probe + region scans + dashscan subcommand)
- _arch01_probe2.py (hand-built-pack render-logic proofs, offload redirected)
- _arch01_out.json, _arch01_out2.json (raw probe output)
- _arch01_offload_probe.jsonl (probe 2's redirected offload rows, 7 rows)
