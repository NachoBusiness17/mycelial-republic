# B2-456 Burn-era line-number pointer sweep (SW-07, 2026-09-26)

## Verdict

LANDED. Every Open-section line-number citation into a burn-hot file was anchor-verified on current bytes. Result: 2 drift classes re-pointed with dated annotations (the providers.yaml:473-488 mistral block, now at :598-626; the md_record_seal.py:46-52 size-only branch, now at :92 after the B2-294 helper insert), 4 citations verified in place (lattice_check.py:59-75 whitelist block, grounding_chain.py:155-218 lane_state/record region, link_library.py:16 schema line, providers.yaml:66-67 saelis region), and the remainder reviewed: shared_surface.py:447 is now out of range (the file shrank under B2-342's edits; both citing rows are landed contextual notes, not live pointers), and the mag/improve.py:640, models/providers.py:164, mag/doctor.py:383 citations still name their subjects' regions.

## Evidence file:line quotes

- QUEUE.md row: "sweep the Open section for line-number pointers into files edited during this burn wave, re-verify each target by string anchor, and re-point the drifted ones with dated annotations; falsifier: an Open row whose cited lines name a different symbol than the brief's subject".
- Drift 1, verified by bytes: grep configs/providers.yaml for the mistral block -> `598:  mistral:` / `599:    name: Mistral (request-minute limit 0 for the on-file key, dormant 2026-09-26)` / `626:      note: "Dormant 2026-09-26 (B2-61)..."`; the cited :473-488 now opens at ` kind: openai_compat` (a different block). Re-point annotation appended to the B2-105 row.
- Drift 2, verified by bytes: grep tools/md_record_seal.py -> `92:            rec["sha256"] = "size-only(>256KB)"` (the cited :46-52 region now holds the B2-41 comment block; the B2-294 register_sha256 insert shifted everything below :78). Re-point annotations appended to both B2-196 early-claimant rows (kept by the B2-255 renumber law, subject landed as B2-294).
- Anchor-OK citations: scripts/lattice_check.py:59-75 contains the LAW-11/SANCTIONED block; scripts/grounding_chain.py:155 opens `def lane_state(name: str) -> dict:`; mag/link_library.py:16 is the ledger schema line with canonical_sha256; configs/providers.yaml:66-67 is the saelis comment its citing rows describe.
- Out-of-range note: mag/shared_surface.py has fewer than 447 lines after B2-342's edit; the two citing rows are landed board notes quoting the ratchet hit, annotated here rather than re-pointed.

## Work done

- Extracted every file:line citation from the board (uniq census), intersected with files working-tree-modified during the wave (git status: agent_cli, doctor, improve, link_library, shared_surface, models/providers, grounding_chain, lattice_check, md_record_seal, providers.yaml), and ran a string-anchor probe per citation group.
- Re-pointed the 2 drifted classes with dated [B2-456 re-point 2026-09-26: ...] annotations on 3 rows (B2-105, B2-196 x2).
- Left already-landed rows' historical quotes untouched except where the citation is the row's live instruction (the two drift classes above).

## Falsifier

The brief's falsifier: "an Open row whose cited lines name a different symbol than the brief's subject" -- the two remaining live classes were re-pointed with dated annotations, and the anchor probe output quoted above names the symbol each cited range now holds. Reopen if: a fresh anchor probe (same script shape, quoted in this receipt) finds a cited range whose text does not contain its row's subject marker, or the providers.yaml mistral block moves again without a dated annotation (it has moved twice today: B2-61, then the B2-134-era edits).

## Bibliography closed

Read: QUEUE.md citation census (grep output), configs/providers.yaml (mistral block, saelis region), tools/md_record_seal.py (post-B2-294 layout), scripts/lattice_check.py, scripts/grounding_chain.py, mag/link_library.py, mag/shared_surface.py (line-count check), mag/improve.py, models/providers.py, mag/doctor.py (anchor probes). No external sources.
