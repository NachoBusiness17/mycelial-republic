# BOT_C — Deep Research agents + corpus-grounded assistants (STEAL-BOT triangulation, 2026-09-10)

Lane: OpenAI Deep Research / Gemini Deep Research / NotebookLM. Sources: public pages,
the PromptLayer methodology teardown, Gemini's official overview page, ZenML's
NotebookLM architecture entry, plus a hallucination-eval search. No logins, no paywalls.
Zero shared context with other bots.

## THE POINT

All three products get their reliability the same way: citation metadata is attached to
every fact at EXTRACTION time (URL + passage excerpt), so the writing phase can only cite
what was actually retrieved — verification is bookkeeping, not a smarter model. Stopping
is never "done", it is coverage thresholds (2+ independent sources per sub-question) plus
hard budgets, and when the budget hits they ship a partial report that flags the gaps
instead of padding. The single most stealable idea: our cite_gate runs as a final
verification pass, but NotebookLM and OpenAI make the citation structurally unavoidable —
the claim and its provenance are born joined, which we can do to every knot we carve from
the 1.2M-file corpus at zero model cost.

## Mechanism table

| Mechanism | How it works | Steal cost | Our current equivalent |
|---|---|---|---|
| **Citation-at-extraction (OpenAI + NotebookLM)** | Every extracted fact carries (source URL + exact text excerpt) in a metadata store as it is fetched; the report writer cites from that store, never from memory. NotebookLM's numbered footnotes point to the retrieved passage, not the document. | LOW | mag/cite_gate.py — verifies AFTER writing, can only reject. Attach (path + excerpt + hash) at carve time instead and the write phase can't fabricate provenance. |
| **Coverage-threshold stopping (OpenAI)** | Stops per sub-question when 2+ independent sources agree (or 1 if authoritative), when novelty is exhausted, or when contradictions are resolved/documented. Budget hard caps beneath it: ~20-30 min, 30-60 searches, 120-150 fetches. | LOW | Wave protocol has no sufficiency test — waves end on fold, not on coverage. Tri-state already has the vocabulary: uncorroborated = Unproven, never Supported. |
| **Partial-report honesty (OpenAI)** | When the budget hits, ships what it has WITH an explicit list of what remains — never fills gaps with inference. | LOW | We tend to fold cards silently. Add "GAP:" rows to every wave output. Free. |
| **User-editable plan gate (Gemini)** | The research plan is rendered BEFORE execution and the user edits/approves it — control sits at the cheapest intervention point, not at the output. | LOW | Beacon gate + operator GO gates already have this shape; apply it to wave plans (post the plan, wait for one-word go before burning width). |
| **Shared-state async task manager (Gemini)** | Planner and task models share state; a failed sub-task recovers and resumes WITHOUT restarting the whole task. Fully asynchronous (turn off your computer, come back). | MEDIUM | The verkle chain IS the shared state, but our waves have no per-sub-task resume — a dead lane means re-run. Steal the "resume the knot, not the wave" semantics. |
| **Per-step re-grounding (Gemini)** | At each iteration the model re-grounds on ALL info gathered so far, then names missing info and discrepancies to chase. Drives the loop with gaps, not with the original query. | LOW | Re-run-once query refinement exists in the vision pipeline; formalize "list what's missing" as an explicit wave triage row. |
| **Self-critique passes at synthesis (Gemini)** | Multiple passes of self-critique over the draft for inconsistencies and detail before release. | LOW | One-builds-one-verify across seats is our version; a self-pass on the draft is cheap filler when no verifier seat is awake. |
| **RL-trained backtracking (OpenAI)** | o3 trained end-to-end with RL in simulated browsing environments; rewarded for pivoting on dead ends (paywall → government mirror). | NOT STEALABLE | We can't train. Imitate the behavior in prompts: on a dead end, name the pivot, don't fail the lane. |
| **Corpus-locked generation (NotebookLM)** | Answers are generated ONLY from retrieved passages of uploaded sources; parametric knowledge is demoted. ~13% response-level hallucination rate in one eval — nonzero, but far below general chatbots. | LOW | Our grounded QA isn't corpus-locked by construction. A system-prompt lock + "answer only from supplied excerpts" on the corpus lane is a config change. |
| **Granularity-aware retrieval (NotebookLM)** | Users report smaller/well-structured sources retrieve more accurately; 1.2M-word-scale corpora work via long-context + retrieval hybrid, not context alone. | MEDIUM | topic_index.py (1,040 cards/23 buckets) is the index; the lesson is chunk by card granularity, never feed raw directories. |
| **Citations as output infrastructure (NotebookLM)** | Passage-level citations double as the substrate for derived outputs (Audio Overviews cite the same sources) — one provenance spine serves every surface. | MEDIUM | Our corpus feeds cards, salons, tesuji. One provenance spine (carve-time metadata) would let every downstream surface cite for free. |

## Known failure modes (their honesty, our falsifiers)

- NotebookLM still misreads under adversarial pressure ("give me extreme criticism of
  this" produces criticisms that don't land) and overweights minor details when hunting
  for "interesting" content. Grounding constrains fabrication, not misreading — our
  corpus QA needs a verify-the-excerpt-actually-supports-the-claim step (cite_gate's job,
  extended from post-hoc to built-in).
- NotebookLM retrieval degrades on large/poorly-structured sources — file granularity is
  a retrieval-quality lever, not a cosmetic one.
- OpenAI Deep Research's citations can attach to the wrong excerpt when bookkeeping is
  sloppy; the fix is the excerpt-in-metadata pattern above.

## Top-3 stealable mechanisms, ranked

1. **Citation-at-extraction (NotebookLM/OpenAI).** Every fact carved from the corpus
   gets (path + excerpt + content hash) at carve time, into the knot itself. The write
   phase then cites only from that store. Converts cite_gate from a rejection filter
   into a structural guarantee. Cost: LOW. Fits the hash chain like a glove.
2. **Coverage-threshold stopping + partial-report honesty (OpenAI).** Per-sub-question
   sufficiency rule (2+ independent sources or 1 authoritative, else Unproven) plus a
   mandatory "what remains" section on every budget-limited output. Cost: LOW. Directly
   strengthens tri-state law with a mechanical trigger.
3. **Shared-state async task manager (Gemini).** Per-sub-task checkpoint and resume off
   the chain: a dead lane resumes its own knot, the wave never restarts wholesale. Cost:
   MEDIUM. Highest leverage for 8-wide night waves.

## Sources

- https://blog.promptlayer.com/how-deep-research-works/ (OpenAI DR loop internals, budgets, stopping)
- https://openai.com/index/introducing-deep-research/ (RL training, backtracking, 5-30 min runs — via search summary, direct fetch 403'd)
- https://gemini.google/overview/deep-research/ (plan editing, per-step grounding, async state manager, self-critique)
- https://www.zenml.io/llmops-database/source-grounded-llm-assistant-with-multi-modal-output-capabilities (NotebookLM grounding architecture, citation mechanics, failure modes)
- https://www.emergentmind.com/topics/notebooklm (13% response-level hallucination eval)
- https://www.datacamp.com/tutorial/notebooklm, https://medium.com/data-and-beyond/notebooklm-explained-a-complete-guide-to-googles-ai-powered-research-assistant-36c57586ada2 (grounding behavior)
- https://www.reddit.com/r/notebooklm/comments/1rmruhv/ (granularity-retrieval reports)
