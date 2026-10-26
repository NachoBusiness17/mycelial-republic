---
name: flash-burn-structural-findings-20260927
description: 9/26-27 flash-lane burn structural findings — fold silently dropped
  watch/ paths, test census hand-copied from birth, 3 fabricated research
  answers caught, envelope ceiling is dynamic not constant, 287 absorbed 1302s
  invisible to surfaced counts
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Flash-lane burn 9/26-27 structural findings that changed how the fleet works (beyond the [[flash-lane-burn-complete-20260927]] tally):

**Silent drop**: index_fold_host.mjs OUTSIDE_RE included `watch|` and silently discarded every register event whose file started with watch/ — 235 poisoned events before B2-02 proved it and re-registered. The fold reported "add succeeded" while indexing nothing.

**Fabricated research caught**: UF-124/125/126 were filed as landed transport rows but cited placeholder arxiv IDs and an openreview id=XYZ. B2-16 proved nothing downstream consumed them. Three UF-129/130/131 died to provider model decommissions, not unreachable targets.

**Census fossil**: the "1,341 tests across 264 files" headline was hand-copied from birth — no count bytes anywhere in the estate. Real count 1,837→1,910 collected. The stale headline survived 12 days because no gate watched test-count carriers.

**False crash-loop**: the 9/19 autorun "crash-loop" was a policy exit misclassified by the supervisor. The gate commit citing it carried two false evidence claims (5,708 blocked lines was actually a line number misread as a count).

**Envelope is dynamic**: width 24 measured clean at 109M tok/h witnessed (B2-25), but 287 1302s were silently absorbed by the retry layer during "clean" waves (B2-98 proved none-surfaced ≠ none-occurred). The ceiling is a function of window depth, not a constant.

**Envelope data**: width 12 = 287 absorbed 1302s across three "clean" waves; width 24 = 8 surfaced deaths in the final hour. The ladder extends: 3-6-10-12-15-24 all tested.

**OLLAMA_HOST locality trap**: .env:118 sets OLLAMA_HOST=http://ollama:11434 (docker-internal name) under a "STRICTLY cluster" comment, but every host seat running load_dotenv() inherits it — ollama reads as DOWN/REMOTE on the host while the daemon is alive on loopback. B2-107 landed the doctor locality law; B2-490 swept the remaining base_url_env overrides (SAELIS_BASE_URL, VAST_OPENAI_BASE_URL, BIONIC_BASE_URL carry the same wrong-scope shape).

**Pointer rot**: brief file:line pointers rot silently when upstream edits move lines — B2-107's ollama pointer cited :66-67 (actually :84), B2-105's mistral pointer cited :473-488 (actually :534). B2-491 landed the pointer-anchor law (every new pointer carries a byte anchor `path:NN#token`) and tools/pointer_rot_check.py.

**QUEUE restore war**: concurrent lanes + the width-24 dispatcher repeatedly flipped landed rows back to unchecked (stale restores, checkbox races, self-feed numbering collisions). Three janitor passes were needed; the claim-line law (B2-250) and the checkbox law (B2-238) were codified but the root cause is that 12+ concurrent lanes share one mutable board file. B2-283's mechanical claim checker is the standing fix.

**Why:** every one of these was a case where the estate's own instruments reported success while the underlying system was broken, stale, or fabricated. The fleet's value function (trust bytes not reports) was correct but incompletely implemented — the gates existed but didn't cover the paths where lies lived.

**Systemic premise-failure pattern (added 9/27):** at least six lanes independently found their dispatch briefs contained false premises — wrong counts, stale flags, already-fixed bugs cited as open, nonexistent files cited as evidence. Not one bad brief-writer: the queue generation process itself (self-feed + FCFS dispatch without value-ranking or premise-verification) systematically produces briefs whose premises decay between writing and execution. LAW-13 (experiment-on-absence) is the structural counter: every brief must carry a verifiable premise anchor, not just a task description.

**How to apply:** every new gate must name the specific path where its disease lives, not just the symptom. The fold, the census, the envelope, and the research pipeline all had blind spots that only byte-level verification (not report-level) exposed.
