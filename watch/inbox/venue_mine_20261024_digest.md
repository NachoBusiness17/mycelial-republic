# Signal digest - 2026-10-24

29 unique stories carried at least one estate law. Venues: free only (HN, Lobsters, Reddit RSS, arXiv). X excluded: no anonymous API.

## backpressure - intake must not exceed drain; a queue that only grows is not a queue
_binds to:_ `tools/commit_sweeper.py - 10-minute drain vs multi-thousand-file intake; observed 20+ min sweeps (2026-10-21)`
- **The Irreversibility Budget: Fleet-Level Risk Accounting and Admission Control** [hn · 1pts] https://arxiv.org/abs/2609.00275
  - matched admission control; score 0.303

## append-only-tape - the record appends; corrections are new rows, never rewrites
_binds to:_ `memory/percolator/explore_decay.jsonl (classify by append), memory/biography/verkle_chain.jsonl`
- **Event Sourcing and Actor model in Ruby [video]** [hn · 2pts] https://www.youtube.com/watch?v=Q6owchf4WEo
  - matched event sourcing; score 0.3
- **Show HN: Hekla, an event sourcing runtime with its own language** [hn · 1pts] https://hekla.tqwewe.com/
  - matched event sourcing; score 0.282

## decay-gc - undrained state is indistinguishable from dead state unless it is aged out
_binds to:_ `tools/explore_decay.py (wave 6), tools/fossil_check.py tombstone registry`
- **Stateful garbage collection: only process what changed** [hn · 1pts] https://valk-lang.dev/blog/stateful-garbage-collection
  - matched garbage collection; score 0.658
- **PEP 848: Generational Incremental Garbage Collection** [hn · 4pts] https://discuss.python.org/t/pep-848-generational-incremental-garbage-collection/109214
  - matched garbage collection; score 0.431
- **High-performance garbage collection for C++** [hn · 77pts] https://v8.dev/blog/high-performance-cpp-gc
  - matched garbage collection; score 0.422
- **Garbage Collection: Generational? Incremental? Both** [hn · 1pts] https://blog.python.org/2026/09/language-summit-2026-garbage-collection-generational-incremental-both/
  - matched garbage collection; score 0.284

## repeat-gate - a single observation is not an invariant
_binds to:_ `tools/invariant_promote.py policy v2 (count>=2, span>=1d, cycle sources>=2)`
- **P-Hacking with Claude** [hn · 1pts] https://vitaexmachina.substack.com/p/p-hacking-with-claude
  - matched p-hacking; score 0.282

## provenance - who asserted this, and on what evidence - stored with the claim
_binds to:_ `memory_store.db facts (no provenance column - known gap from the 2026-10-20 paper check); receipts in memory/runs/`
- **Compaction Laundering:Provenance Destruction in Context-Compacting Coding Agents** [hn · 2pts] https://arxiv.org/abs/2610.29869
  - matched provenance; score 0.921
- **Sourcey's open startup-credit registry: twelve dated records with provenance** [hn · 2pts] https://sourcey.com/startup-credits
  - matched provenance, ~source; score 0.848
- **Rsync – Release manager change doesn't have provenance** [hn · 2pts] https://github.com/RsyncProject/rsync/issues/1097
  - matched provenance; score 0.834
- **EPGM: Execution Provenance for Budgeted Agent Memory Retrieval** [hn · 2pts] https://arxiv.org/abs/2609.25913
  - matched provenance; score 0.755

## leaf-graph - structure is what survives ablation; a node nothing depends on is a leaf
_binds to:_ `I5 gate (0/17 promoted rows declare depends_on; 963 edges elsewhere)`
- **Building a Dependency Graph of Our Python Codebase** [hn · 2pts] https://www.hudsonrivertrading.com/hrtbeat/dependency-graph-python-codebase
  - matched dependency graph, ~graph, ~dependency; score 0.631

## fossil-tombstone - dead artifacts are named dead, not left looking alive
_binds to:_ `tools/fossil_check.py registry (SEATS.md recompiled 2026-10-21; jev trail watch-only)`
- **Upcoming deprecation of selected GitHub Copilot models in mid-November** [hn · 2pts] https://github.blog/changelog/2026-10-15-upcoming-deprecation-of-selected-github-copilot-models-in-mid-november/
  - matched deprecation, ~deprecat; score 0.51
- **HCP Vagrant Deprecation** [hn · 3pts] https://www.hashicorp.com/en/blog/hcp-vagrant-deprecation-important-dates-and-migration-guidance
  - matched deprecation, ~deprecat; score 0.473
- **Deprecation of HashiCorp Boundary Community Edition** [hn · 2pts] https://discuss.hashicorp.com/t/deprecation-of-boundary-community-edition/77828
  - matched deprecation, ~deprecat; score 0.443
- **OpenAI Deprecations** [hn · 3pts] https://developers.openai.com/api/docs/deprecations
  - matched deprecation, ~deprecat; score 0.25

## immune-memory - detect the anomaly you have seen before faster than the one you have not
_binds to:_ `tools/fossil_check.py, precommit_secret_check.py, falsifier log_zero kinds`
- **Clustering and Anomaly Detection on Handwritten Digits** [hn · 3pts] https://stochastic.blog/clustering-and-anomaly-detection-on-handwritten-digits/
  - matched anomaly detection, ~detection, ~anomal; score 0.271
- **Gmail AI Threat Scanner–zero-infra email anomaly detection** [hn · 1pts] https://github.com/ajaynyayapathi/Gmail-AI-Threat-Scanner
  - matched anomaly detection, ~detection, ~threat, ~anomal; score 0.24

## homeostasis - regulation is a loop with a sensor, a setpoint, and a cost
_binds to:_ `fossil_check bars (168h/720h), falsifier review dates, sweeper cadence`
- **Human homeostasis is more efficient in social proximity** [hn · 4pts] https://www.science.org/doi/10.1126/sciadv.aeg4937
  - matched homeostasis; score 0.28

## energy-budget - every operation spends something; unmeasured spend is unbounded spend
_binds to:_ `lane spend policy (~$220 credits, conservative default); local 7B on a 6GB box`
- **Hibernating bacteria survive outer space but energy budget reveals a weakness** [hn · 3pts] https://phys.org/news/2026-09-hibernating-bacteria-invade-hospitals-survive.html
  - matched energy budget; score 0.229
