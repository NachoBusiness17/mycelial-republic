# PA-D2-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

# D2 ADJUDICATION (movement 2 of the doctrine roast)

Conditions: single pass, this session; instrument is the four pasted evidence blocks only; I ran no commands. The `workflow_gate.py` and `REGISTRY.jsonl` blocks are truncation-replay (head75+tail25), so any claim resting on bytes outside the visible head/tail is marked UNVERIFIED against disk.

---

## (1) EXIT SEMANTICS - L1 AMENDS, does not die and does not survive intact

The cheap arm is byte-right on its claim and byte-wrong on its scope.

- **Settled:** exit 2 is the only verdict-bearing hard block. Docstring: "exit 2 is the only hard block; every submission registers a row" (02__workflow_gate.py, docstring). `main()` returns 2 on failed checks and 0 on pass; exit 1 never fires on a gate verdict. The trivalent 0/1/2 contract is visible in the `--no-register` path: `return 2 if failed else 0`. Grep-zero `sys.exit(1)` sites is consistent with the visible code (`sys.exit(main())` only at the tail).
- **Residual defect the cheap arm missed:** the docstring's second half, "every submission registers a row", is falsified by the OSError path in `main()`:

  > `print(f"GATE ERROR: cannot read script: {exc}")` followed by `return 1`

  That `return 1` fires **before** the digest is computed and **before** the registry append block. An unreadable script produces no row. So the docstring is half-true at its own bytes: exit 2 is the only hard block (true), but "every submission registers a row" (false for unreadable files).

**Verdict: L1 amends.** The original objection (exit semantics contradict logic.md) dies; the amended objection is narrower: the gate's own docstring overclaims its ledger guarantee. One-line fix, not a doctrine break.

## (2) REGISTRY ORDER - A4/O7 reconciliation HOLDS as census-law arithmetic

Both counts are true at their moments: row 40 at 2026-09-30T01:18:10Z, rows 41-45 on 2026-10-01. On an append-only file, "40 rows" read pre-ractor50-final and "45 rows" read later are consistent; neither chapter violates append-only arithmetic. The chapters disagree only when read across moments, which is the missing-moment defect (A4's real surviving core: no timestamp on the count), not a census violation.

Scope note: the visible REGISTRY tail in this session shows rows stamped 2026-10-02T01:52Z (ractor-engine). The row-40 bytes themselves are in the truncated middle and are UNVERIFIED by me this pass; the arithmetic verdict rests on the cheap arm's command answer plus the visible append-only pattern. Also: the file has grown past 45 rows since the chapters' reads, which further confirms "both counts true at their moments, both now stale."

## (3) UF-124 - objection 1 is CONFIRMED, not merely OPEN

Movement 2 left it open because the premise files were not found. Movement 3, ticket 2, closed exactly that gap with located bytes (00__MOVEMENT2_CHEAP_ANSWERS.md, movement 3 section):

- `B2_16_uf_sweep` at `watch/inbox/burn_wave_20260926/`; `DAY_PACK.md` at `watch/inbox/union_fullsend_20260917/`.
- The UF-124 answer carried the literal placeholder `openreview.net/forum?id=XYZ` AND `Constitutional AI - OpenAI` misattributing Anthropic's paper.

Closing evidence statement, now satisfied: objection 1 (existence-check resolver passes a misattributed but real citation) is confirmed if and only if a case exists where an id resolves to real bytes while the claimed value is wrong. The UF-124 bytes supply the doubly-degenerate case: a non-resolving placeholder id AND a wrong author attribution next to it. Even under the weakest reading (placeholder fails the existence check, so the unamended gate would catch it), the `Constitutional AI - OpenAI` misattribution against a real Anthropic paper is the in-chapter instance: any real, resolving id for that paper passes the unamended gate and ships the wrong author. Status: **CONFIRMED**, closed.

---

## (4) THE ONE LANDABLE AMENDMENT

**Chapter:** accuracy.md, §Incident 1 "Instrument upgrade" (first sentence) plus the "(2)" clause of the Decision ledger.

**Paste-able sentence:**

> A row carrying an external citation or a tool-behavior claim lands LANDED only when the same session's receipt quotes, from fetched bytes or captured command output, the span carrying the specific claimed value (author attribution, effect size, default behavior); an id that resolves without that span lands UNVERIFIED, and until a resolver enforcing this exists in tracked code this rule is PROPOSED, not a changed contract.

How it sorts the now-real cases:

- **Fails, lands UNVERIFIED (negative, no longer hypothetical).** The UF-124 answer citing `openreview.net/forum?id=XYZ` with `Constitutional AI - OpenAI`: even if a real Anthropic paper id were substituted, no quoted span shows the claimed authors, so the row lands UNVERIFIED.
- **Passes (positive).** The UF-128 receipt quoting `rg PATTERN dir_with_symlink` output (symlinked file absent) directly beneath the claim "rg skips symlinks unless --follow": the quoted span carries the claimed default behavior.

**Falsifier for the amendment:** a single case where the claimed value span is quoted from fetched bytes and the claim is still wrong at the same span (quote is faithful, value is false in the world, e.g. the paper really is by OpenAI). That would show span-quoting certifies fidelity, not truth, and the amendment's gate is insufficient on its own terms.

## (5) NEXT 3 DIG TICKETS (commands, zero opinion)

**T1 - amended L1 check.** `grep -n "return 1" tools/workflow_gate.py` and `grep -n "open(REGISTRY" tools/workflow_gate.py`. Question: does every `return 1` site precede the registry append, leaving that path rowless? If any exit-1 site occurs after the append, the docstring's "every submission registers a row" is true at all code paths and my amended L1 dies.

**T2 - registry growth and row 40 bytes.** `wc -l memory/workflows/REGISTRY.jsonl` and `sed -n '40p' memory/workflows/REGISTRY.jsonl`. Question: what is the current row count, and does row 40 name `frontier-olm-mine` at ts `2026-09-30T01:18:10Z`? If row 40's bytes differ, the movement-2 reconciliation rests on a misread and A4/O7 reopens.

**T3 - the-gala recoverability.** `grep -rn "0ad57dc88296" watch/inbox/ corpus/ 2>/dev/null; git ls-files .zcode/workflows/the-gala.dwf.ts`. Question: does digest `0ad57dc88296` (the-gala's last PASS digest, REGISTRY head section) appear in any durable receipt or tracked file besides the registry? If yes, a recovery path exists and operations O1 downgrades from "lineage can vanish with the disk" to "lineage is scattered"; if zero hits outside REGISTRY.jsonl, O1 stands at full severity.

---

## Falsifier for this whole deliverable

- **(1):** T1 shows a `return 1` after the registry append, or shows the OSError path still minting a row. My amended L1 dies.
- **(2):** T2 shows row 40 is not `frontier-olm-mine` at the stated ts. The reconciliation was built on misread bytes and reopens as a possible real census violation.
- **(3):** The movement-3 file paths, when read on disk, do not contain `openreview.net/forum?id=XYZ` or `Constitutional AI - OpenAI` at the cited locations. Objection 1 reverts to OPEN.
- **(4):** A faithful-quote, false-value case exists in the corpus (quote matches fetched bytes, claim still false). The amendment's gate is shown insufficient and the paste-able sentence needs a truth-check clause it currently lacks.
