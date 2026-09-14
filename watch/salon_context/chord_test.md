CONTEXT — the chord test (fold vs best post)

What exists:
- watch/seed_percolator.py: registry.jsonl + sha256 ids, paired blind win-rate >=55% vs
  baseline, 30 pairs/epoch, 3 clean epochs to freeze, null-variant canary to catch judge
  bias. Built for prompt seeds, never run on folds.
- Salon artifacts accumulating at memory/runs/salons/<name>/: BRIEF.md, post_S1..S7.md
  (durable), SALON_ARTIFACT.md containing the fold's VERDICT. Three runs today.
- MAG CHORD v4 protocol (watch/MAG_CHORD_V4_ADOPTED_20260903.md): blind divergence,
  collision ledger, promotion gate (human-only).
- The chord theory just filed (watch/SELF_STEAL_CHORD_THEORY_20260903.md): coherent corpus
  + roleplay in boundaries -> ensemble exceeds participant boundaries. Its falsifier IS
  this test: if folds don't beat best-posts at >=55%, the theory dies as poetry.
- Lanes: posts on free lanes; judge on zai-pro (Max plan, $0 marginal) or deepseek pennies.
  A blind judging call per pair is therefore near-free.

The design problem to rightsize:
- What exactly is a "pair"? (fold vs the strongest post on the same question, judged blind
  on identical rubric — but who picks "strongest" without bias? Random post? All 7 rotated?)
- What rubric makes the judge measure VALUE (decision-usefulness) not taste?
- N: 30 pairs needs 30 salon-equivalents — we have ~1-3. Do we mine OLD salon runs
  (pre-runner, hand-run salons in memory/runs/salons/) as pairs? Are hand-salons
  comparable? Smallest honest N?
- Judge lane: one model judging its own family's output (zai-pro judging zai posts) —
  bias risk the percolator's null-variant canary was built to catch.
- What result kills the theory, and what result promotes it?
