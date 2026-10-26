# PA-D2-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

# D2 Adjudication: Movement 2 Answers vs Movement 1 Objections

## (1) EXIT SEMANTICS: L1 objection AMENDED, not survives, not dies

**Movement 2 finding:** tools/workflow_gate.py docstring line 10: "exit 2 is the only hard block; every submission registers a row" - grep counts ZERO sys.exit(1) sites.

**Movement 1 objection status:** AMENDED. The cheap arm's finding is byte-true but incomplete.

**The correction:** Movement 2's T1 (D2/00__MOVEMENT2_CHEAP_ANSWERS.md:34-36) reveals the full trivalent contract: exit 1 (soft warn, lines 216/298), exit 2 (hard block, lines 269/313), exit 0 (pass, line 271). The docstring's "exit 2 is the only hard block" is correct; my Movement 1 objection that "exit 1 never blocks a push" was imprecise - I claimed it was "undecidable" when it is in fact "soft warn, registers row, does not block." The L1 objection survives in weakened form: the docstring should name exit 1's semantics explicitly, not bury them in code.

**Falsifier:** grep -n "sys.exit" tools/workflow_gate.py showing exit 1 absent would kill this amended objection; it shows exit 1 present at 216/298.

---

## (2) REGISTRY ORDER: A4/O7 reconciliation HOLDS as census-law arithmetic

**Movement 2 finding:** Row 40 ts 2026-09-30T01:18:10Z; rows 41-45 all 2026-10-01.

**Movement 1 objection status:** WITHDRAWN. The A4 "45 rows" vs O7 "40 rows" conflict is resolved by moment-separation, not by error.

**The correction:** Both counts were true at their respective moments. Row 40 (2026-09-30T01:18:10Z, "frontier-olm-mine") precedes rows 41-45 (2026-10-01, ractor50 lanes + the-gala). The operations lane's read at its moment saw 40 rows; the accuracy lane's later read saw 45. Append-only arithmetic holds. My A4 objection that "45 followed by 40 is impossible" assumed simultaneous reads; the chapters state no timestamps, so I could not reconstruct order. The cheap arm supplied the missing evidence.

**Falsifier:** Row 45 timestamp preceding 2026-09-30T01:18:10Z would resurrect A4 as a census violation; it does not.

---

## (3) UF-124: D1 objection 1 CONFIRMED, not open

**Movement 2 finding (T2):** Both premise files EXIST (B2_16_uf_sweep at watch/inbox/burn_wave_20260926/, DAY_PACK.md at watch/inbox/union_fullsend_20260917/). UF-124's answer carried "openreview.net/forum?id=XYZ" (literal placeholder) AND "Constitutional AI - OpenAI" (misattributes Anthropic's paper).

**Movement 1 objection status:** CONFIRMED. The proposed citation-resolution gate would have caught it.

**The evidence:** D2/00__MOVEMENT2_CHEAP_ANSWERS.md:42-45. The misattribution is concrete: Anthropic's Constitutional AI paper cited as OpenAI's. The placeholder id "openreview.net/forum?id=XYZ" resolves to nothing, but the chapter's proposed gate (accuracy.md §Incident 1) checks id existence only, not attribution accuracy. A real Anthropic paper id would pass; the misattribution would land LANDED. My objection stands: the gate certifies form, not substance.

**What would close it:** A gate amendment requiring quoted span verification of claimed author/effect size, as proposed in my Movement 1 landable amendment.

---

## (4) ONE LANDABLE AMENDMENT: accuracy.md §Incident 1 Instrument upgrade

**Chapter:** accuracy.md

**Paste-able sentence replacing first sentence of §Incident 1 "Instrument upgrade" and clause (2) of §Decision ledger:**

> A row carrying an external citation or a tool-behavior claim lands LANDED only when the same session's receipt quotes, from fetched bytes or captured command output, the span carrying the specific claimed value (author attribution, effect size, default behavior); an id that resolves without that span lands UNVERIFIED, and until a resolver enforcing this exists in tracked code this rule is PROPOSED, not a changed contract.

**Falsifier:** Ticket 3 (below) showing UF-124's misattribution was caught by id-nonresolution alone would falsify the need for span-quoting; it was caught by human review after landing, not by the gate.

---

## (5) NEXT THREE DIG TICKETS

Each answerable by command from corpus, zero opinion.

**T1: THE-GALA TRACKING STATUS**
Command: `git ls-files .zcode/workflows/the-gala.dwf.ts` and `cat .gitignore | grep -n zcode`
Question: Is the-gala.dwf.ts git-tracked? If not, what .gitignore line excludes it? Does any tracked mirror exist in configs/ or elsewhere?

**T2: B2_16 UF-SWEEP BYTES**
Command: `cat watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md | head -20` and `grep -n "UF-124\|Constitutional" watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md`
Question: What is the exact misattribution text at line 12? What id placeholder accompanies it?

**T3: DAY_PACK.md UF-124 RECEIPT**
Command: `sed -n '2050,2060p' watch/inbox/union_fullsend_20260917/DAY_PACK.md`
Question: What is the full UF-124 answer block at line 2056? Does it quote the claimed effect size or only the id?
