# STEAL: "Transmutable Link Dumps for LLM Handoffs" mapped onto Mag (2026-10-17)

Written 2026-10-17, around 8 PM ET, by a Grok Bot executor. This was a read-only pass: no code changed, no git,
no model or paid API calls, and no processes touched. I did not open .env, key files, secret_gate_results/,
free_keys/ or memory/trajectory/steps.jsonl. Sources were fetched on the box with curl: arXiv abs pages and the
export API, the GitHub REST API and raw files, the dev.to article API, the Zenodo record via its DOI, the Hugging
Face Spaces API, and the PyPI and npm registries. Mag files were read in place with rg and Get-Content.
Evidence tiers follow STEAL_X_BRIEFS_20261017.md: **measured** (I read it or ran it), **paper claim**,
**conceptual**, **recommendation**.

## 0. Headline

- **No citation in the document is fake.** All 7 sources exist. Two are partly misquoted: the tweprint rules (the
  biggest error) and the status of the 5-field schema. The 97.2% figure is real.
- **The best steal is (b), "must becomes maybe".** Mag already has every piece: restricted leases, notices, the
  warm preamble and the RELIEF report kind. But the preamble shows each blocker only as a subject line, shows at most
  8 notices, and never shows the standing rules. That is exactly the failure the paper measures. The fix is one
  uncapped, verbatim "hard constraints" block plus a fingerprint that RELIEF must echo. A deterministic "blocker
  survives compression" test proves it.
- **(c) the coverage manifest and owned next actions** is worth adding as RELIEF fields (doctrine P5).
  **(a) the claim ledger** is worth adding as one optional field, merged with the evidence_tier enum from the X
  briefs report rather than built as a second enum. **(d) tweprint rules** become a small lint in mag/x_surface.py,
  and a silent truncation in the X posting path should be removed. **(e)** adopt neither url2llm nor markurl.

## 1. Source verification

| # | Source as cited | Verdict | What it actually says (measured, fetched 2026-10-17) |
|---|---|---|---|
| 1 | arXiv 2608.24569, "When 'Must' Becomes 'Maybe': Erosion of Workflow Constraints in LLM Agent Handoffs"; "multihop compression gives 97.2% blocker deactivation" | **Confirmed** | Sun, Wang, Zhu, Li, Zhao and Yuan. v1 2026-08-25, v2 2026-10-13 ("Revised title, abstract..."). Abstract: "Ownership deferral produces 76.7% blocker deactivation; multihop compression produces 97.2%." The abstract also says restoring the full blocker description raises recognition "from 6.2% to 99.2%" and cuts forbidden action "from 85.2% to 0.0%", while an authorization-check prompt brings forbidden action to 1.6% but leaves artifact deactivation at 95.3%. These are paper claims on the authors' own setup. I did not reproduce them. |
| 2 | Zenodo, April 14 2026, "What to Pass and Why" (context debt) | **Confirmed** | DOI 10.5281/zenodo.19578228 resolves to zenodo.org/records/19578229. "What to Pass and Why: A Framework for Context Handoff in Multi-Agent LLM Systems" by June Song, published April 14, 2026. It defines "context debt" and argues for "decision-sufficiency rather than history preservation". It calls itself a position paper: "theoretical and architectural rather than empirical". |
| 3 | arXiv 2608.14528, "Handover of In-Context Learning State Across Session Boundaries" | **Confirmed** | Masahiro Kato and Taka Kato, 2026-08-14. It proposes "a three-part record that stores decisions and constraints exactly", plus statistics for repeated evidence and original observations that those statistics do not preserve. This is theory (Gaussian linear regression and nonparametric bounds). |
| 4 | dev.to/dk3yyyy/the-handoff-problem-... | **Confirmed, with one caveat** | Published 2026-07-27 by dk3yyyy. It contains the exact 5-field YAML (claim / evidence "source URL + exact support" / scope / uncertainty "fact / estimate / interpretation / prediction" / citation). It also states the rule: "may change language and structure freely... may not change the semantics of the evidence. Any new factual claim... routes back to research." **Caveat:** the author writes "this five-field schema is my evidence-informed proposal, not a standardized or experimentally validated format." Present it as a proposal, not as a proven standard. |
| 5 | highlight-reel.app/templates/ai-research-source-pack-template | **Confirmed** | A vendor template page dated May 13, 2026. Its six parts are: research question, short answer, source table, assumptions and limits, decision or recommendation, next action. It also has a "Confidence Labels" section. |
| 6 | github.com/brando90/agents-config, the "tweprint" format: 6-9 tweets, 280 characters or fewer, exact numbers only, hedges preserved, draft before posting | **Partly wrong** | The repo exists ("My coding agent's config workflow setup"). The rules are in `workflows/tweprints.md` (4,118 bytes). **Length is wrong:** the file says "4-8 tweet thread" (line 3) and "Thread length: 4-8 tweets. Shorter is better" (line 29), not 6-9. **The 280 limit is right** (line 33). **"Exact numbers only" is overstated:** the file says "Numbers over vague claims... Always include the concrete metric" (line 27). **"Hedges preserved" is not in the file.** The nearest line is "Enthusiastic but honest. Don't oversell. If something is a limitation, frame it as an open challenge" (line 30). **"Draft before posting" is right:** Process step 1 is to draft in a .txt under `tweets/<MM_DD_YYYY>/`, then review with co-authors, then post (lines 62-65). |
| 7 | huggingface.co/spaces/wis-k/thread-gpt | **Confirmed (exists), weak source** | ThreadGPT, a Gradio Space created 2023-11-25 and last modified the same day. It is currently PAUSED. It turns papers into tweet threads with figures. It is a tool demo, not a source of rules. |
| - | Tools url2llm, markurl | **Both exist** | url2llm 0.3.3 (PyPI, github.com/diegobit/url2llm, 5 stars) crawls with Crawl4AI and then "asks the LLM to extract... only the content relevant", so it needs a provider API key and makes model calls per page. markurl 0.1.0 (npm only, created 2026-05-13, github.com/nkpatnis/markurl, 0 stars) is "URL in, clean Markdown + structured metadata out", built on @mozilla/readability + turndown + an MCP SDK. |

Fabrication check: none found. Errors to correct in the pasted document: the tweprint length (4-8, not 6-9), and the
two tweprint rules it adds that the file does not state ("exact numbers only", "hedges preserved"). These are good
rules, but they belong to the document, not to brando90. Also, the 5-field schema is the dev.to author's
unvalidated proposal.

## 2. What Mag already has (measured, file:line)

Repo-relative paths. Line numbers were read 2026-10-17 around 8 PM ET.

**Fleet report (the transport for any brief).**
- `configs/fleet_report.v1.schema.json:10` kinds SPOTREP / SITREP / NOTICE / RELIEF / ACK. `:16` `leases` is a
  string array. `:38` `outstanding` is capped at 2000 characters, `:17` `narrative` at 4000. `:46`
  `additionalProperties: false`. `:54-55` RELIEF requires `status, outstanding, leases, stand_relieved`. No field
  for claims, evidence, scope, coverage, tensions, next actions or constraints.
- `mag/fleet_report.py:87-117` `_check_prop` understands only `string` and `array` (with string items). It cannot
  validate an array of objects today. `:120-148` `validate`; `:155-183` `check_body` is called by the receipt writer,
  so a bad body is refused before a byte lands (code-is-law). `:278-282` the notices row.
- Tests: `tests/test_fleet_coordination.py:63` (schema and validator agree on kinds), `:103` (RELIEF
  stand_relieved must be true), `:167` (notices in force, ack and cancel).

**Notices.** They are not `watch/receipts/N-*` files. They are `seat_*.json` receipts whose body carries
`notice_id: N-...`. Two are in force: `N-20261017-opencode-console-breach`
(`watch/receipts/seat_20261017T201014565833Z_grok_67e87b116422.json`) and `N-20261017-opencode-zen-keys-unused`
(`..._a8b9ea7cff54.json`). Both were ACKed by seat bob at 22:19 UTC (6:19 PM ET). Their `action_required` text is the
blocker, for example "Rotate the OPENCODE keys ... by the operator only".

**Restricted leases.** `configs/restricted_leases.json` names 5 resources: `chain:biography`,
`file:mag/verkle_knot.py`, `proc:lab`, `file:docker-compose.yml`, `keys:names`. `mag/leases.py:254` acquire,
`:321` transfer, `:355` list_leases, `:420` guard.

**Preamble (where every seat boots).** `mag/warm_surface.py:297-344` `preamble(seat)`:
- `:314-318` a 4-line Contract ("Do not invent body/keys/status", "No secrets cross this surface").
- `:248-256` `_law_bullets(max_items=12)`: core laws from `memory/rib_boot.json`. I counted 9 today, none of which
  says "no git" or "never open .env".
- `:279-294` `_board_lines`: leases **held** (not the restricted list itself), then
  `nb.get("in_force")[:8]` (`:289`), printing only `notice_id`, `category`, `subject` and the ack count (`:290`).
  **The notice's `action_required`, the actual "must", never reaches the preamble.**
- `:309` zknot is cut at 1200 characters. `:49` BODY_CAP is 65536, with `_cap` at `:158`.
- There is no RELIEF section. Doctrine P5 ("the next seat's preamble carries the latest RELIEF") is not built.
- `tests/test_shared_surface.py:118-125` checks that the preamble has the seat and the first law. Nothing checks
  for blockers.

**Standing rules ("no git", "no .env").** These are not structured anywhere I found. They live in task prompts,
in prose in `AGENTS.md` and in individual module docstrings. `mag/proposals.py:29-30` ("git belongs to the
operator's git window") and `mag/warm_surface.py:318` come closest.

**Older handoff organs (do not revive; fold).**
- `mag/auto_handoff.py:10,104-105` has PENDING / BLOCKER / CONTEXT sections, but `memory/handoffs/latest.md` was last
  written 2026-08-15 and `memory/handoff_state.json` on 2026-08-10. It is dormant.
- `mag/peer_handoff.py` is dormant (doctrine table row 13).
- RELIEF is the live path. That makes three handoff shapes. The doctrine already says to fold duplicates, not
  rebuild them (`watch/LIBRARY/FLEET_COORDINATION_DOCTRINE_20261017.md:210-211`).

**Laws that already point the same way.**
- `mag/attention_ranker.py:302`: "feedback may reorder ordinary items but cannot hide hard rules".
- `mag/checkin_route.py:65,73`: "Never collapse interpretation into fact" / "Must not promote interpretation->fact".
  This is the Uncertainty field's rule, already written as law.
- `mag/cite_gate.py:8-22` (LAW-064): classifies each citation as LOCAL-VERIFIED / EXISTS-UNRELATED / LOCAL-MISSING
  / URL-UNVERIFIED / NONE and checks the claim's key terms **and numbers** against the cited file. This is the
  receiver-side "does the evidence actually support it" check. `:156-167` `fetch_url` is a deliberate stub that
  raises NotImplementedError until the operator says GO for network egress.
- `mag/harness_probe.py:15-18,22-23` already demands "receipt:line EVIDENCE" in candidates and verdicts.

**X drafting.**
- `mag/x_surface.py:74-86` `draft()` queues text for operator review and never posts. It has no checks at all.
- `mag/x_control_surface.py:464` `post_to_x`; `:486` `{"text": text[:280]}` **silently truncates**. A hedge or a
  number at the end of an over-long tweet would be cut with no error.

**Fetching.** Mag has no HTML-to-Markdown fetcher. rg for trafilatura, readability, markdownify, html2text,
r.jina.ai, crawl4ai, firecrawl and defuddle finds nothing relevant. The venv has `beautifulsoup4 4.15.0` and
`httpx 0.28.1`. The only URL "door" is the `cite_gate.fetch_url` stub.

**Concurrent work (read, not edited).**
- `watch/LIBRARY/STEAL_X_BRIEFS_20261017.md` (written 7:56 PM ET) proposes an optional
  `evidence_tier` enum on fleet_report (`measured | paper_claim | conceptual | recommendation | creative | unverified`)
  and notes the validator cannot check per-claim objects (its section 3a). **Overlap with (a) below:** use that
  enum. Do not add a second "uncertainty" enum.
- It also notes that `scripts/inbox_librarian.py:312-336` regenerates INDEX.md, so hand-appended lines (including
  the one for this report) disappear on the next librarian run.
- `mag/harness_probe.py` (35,963 bytes, 7:51 PM ET) overlaps only in its "receipt:line EVIDENCE" rule. Nothing
  here asks to change it.

## 3. Steal-by-steal verdicts

### (b) Hard constraints that cannot be compressed - WORTH BUILDING (best steal)

**Why it matters (paper claim + measured gap).** Paper 1 shows the failure mode is not that the blocker disappears.
It stays visible but loses its force: "the issue remains visible, but its role has changed." Mag's preamble
does exactly that: a notice shows up as `NOTICE N-... [breach] OpenCode Console provider-key breach... (acks: 1)`,
and the instruction that makes it a blocker (`action_required`) is dropped (`warm_surface.py:290`). A 9th notice
would vanish entirely (`:289`). The standing rules appear nowhere. Paper 1's own remedy, restoring the full blocker
description, took forbidden actions from 85.2% to 0.0%. Paper 3 independently says to store "decisions and
constraints exactly". Note the warning in paper 1: an authorization-check prompt fixed the endpoint (1.6% forbidden)
while the artifact stayed 95.3% damaged. A behaviour test alone can therefore pass on a broken handoff, so the test
must check the **artifact**, not just the outcome.

**Smallest build (recommendation). It reuses organs and adds no engine.**
1. **Constraint source = doctrine P3's CONSTRAINTS section** (commander's intent card, pending). Until that card
   exists, a tiny `configs/standing_constraints.json` with rows `{id, text}`. Example rows: `no-git` "No git
   commands; git belongs to the operator's git window."; `no-env` "Never open .env files, not even variable names.";
   `no-keys` "Never open key files, secret_gate_results/, free_keys/ or memory/trajectory/steps.jsonl.";
   `no-procs` "Do not touch processes, containers or docker without a proc:lab lease."; `no-post` "Post nothing
   publicly; X goes to the draft queue." Editing it goes through `mag/proposals.py` (doctrine P7).
2. **One function, `warm_surface.hard_constraints()`**, returns an ordered list built from three existing organs,
   each item `{id, text}` verbatim:
   - every standing constraint;
   - every **restricted-list resource** from `configs/restricted_leases.json` (id = resource, text = its
     description + "lease first"), whether or not it is currently held;
   - every **in-force notice** (id = notice_id, text = `action_required`) from `fleet_report.notices()`.
   It also returns `constraints_sha = sha256(canonical JSON of the list)`.
3. **Preamble:** insert `## HARD CONSTRAINTS (verbatim; never summarise, never cap)` directly after the
   Contract (`warm_surface.py:318`). It prints every item in full plus the sha. It is exempt from `[:8]`, from
   `max_items` and from any character cap. If the whole preamble would exceed BODY_CAP, `_cap` must cut **other**
   sections first, or the read fails loudly. It must never cut this block.
4. **RELIEF carries it, by structure:** add `constraints_sha` (string, 64 chars) to the schema and to RELIEF's
   required list (`fleet_report.v1.schema.json:55`). In `check_body` (`fleet_report.py:155`), a RELIEF whose
   `constraints_sha` does not match the current `hard_constraints()` sha is **refused**, with a message listing the
   ids the seat has not seen. Optionally, also require `constraints` (string array of ids) so a human can read it.
   This is the same move as the existing "RELIEF refused while leases untransferred" idea in doctrine P5:
   the rule lives in the writer.
5. **Fold, don't revive:** `auto_handoff.py`'s BLOCKER list, if anyone still edits `memory/handoff_state.json`,
   becomes standing-constraint rows. Leave the module dormant.

**Tests that prove it (deterministic, $0, no model):**
- `test_preamble_carries_every_blocker_verbatim`: fixture with 12 in-force notices, all 5 restricted resources and
  all standing rows. Assert that every `action_required`, every resource id and every standing text appears
  **byte-for-byte** in `preamble(seat)` for every seat in `SEATS`. *Today's code would fail this:* `:289` keeps
  8 notices and `:290` drops `action_required`. That makes it a real falsifier, not a rubber stamp.
- `test_blocker_survives_compression` (the key test): apply every lossy step Mag already has, chained 3 hops to
  copy the paper's "multihop": preamble render, then a RELIEF built from it with `narrative`/`outstanding` cut to
  their schema caps, then a canonical_body round trip, then the next preamble, then repeat. A test-only
  `compress()` helper drops every free-text field and truncates every remaining string to 200 characters, but
  does not touch the HARD CONSTRAINTS block. After each hop, assert the set of constraint ids and their texts is
  identical to the original and the sha is unchanged. Then run the **negative control**: apply the same
  `compress()` to today's board lines and assert at least one blocker text is missing. This shows the test can
  fail.
- `test_relief_with_stale_constraints_sha_refused`: file a NOTICE, then a RELIEF carrying the old sha.
  Expect `ReportInvalid` that names the new notice id. A RELIEF with the current sha validates.
- `test_new_notice_changes_sha` and `test_cancelled_notice_leaves_block`: a cancel (`fleet_report.py:263-264`)
  removes the item and changes the sha.
- `test_body_cap_never_cuts_constraints`: inflate zknot past BODY_CAP. The constraint block stays complete and the
  zknot section is the one that gets cut.
- Existing tests stay green: `test_shared_surface.py:118`, `test_fleet_coordination.py:63,103,167`.
- Optional, later (not part of the minimal build): a live paraphrase probe on a free lane through the Harness2
  mates. A summarizer rewrites a RELIEF, and the test checks every constraint id survives. It is off by default
  and $0 lanes only.

### (c) Coverage manifest + owned next actions as the RELIEF format - WORTH BUILDING (small)

This maps one-to-one onto doctrine P5 (`FLEET_COORDINATION_DOCTRINE_20261017.md:303-310`), which already lists
unusual conditions, outstanding orders, leases, WIP and upcoming. Today's RELIEF has `status`, `outstanding`
(free text, 2000 characters), `unusual`, `upcoming`, `hazards` and `leases`. The document adds the parts that
make a relief **checkable**: a goal, what was covered and what could not be fetched (and why), tensions, what was
tried, and next actions with an owner and a "done when".

**Smallest build (recommendation):**
1. Schema, all optional for SITREP and required for RELIEF except where noted:
   - `goal` (string, 200);
   - `covered` (string array);
   - `unfetchable` (string array, each item matching `^.+ -- reason: .+$`);
   - `tensions` (string array, may be empty);
   - `tried` (string array, numbered by position);
   - `next_actions` (required for RELIEF, minItems 1).
2. `next_actions` items. Either:
   - (i) **zero validator change:** strings matching `^owner: [A-Za-z0-9_.:-]+ \| action: .+ \| done when: .+$`; or
   - (ii) **cleaner:** objects `{owner, action, success}`, which needs about 15 lines in `_check_prop`
     (`fleet_report.py:87-117`) to support `type: object` with `properties` / `required` /
     `additionalProperties`.
   I recommend (ii), because (a) needs the same support.
3. **"continue" is banned:** in `validate`, an action matching `(?i)^\s*(continue|keep going|carry on|proceed)\b`
   with no object, or a `success` shorter than about 10 characters, is refused.
4. Preamble: a `## LAST RELIEF` section (doctrine P1 item 8 / P5) printing goal, next_actions and unfetchable
   in full, and listing covered/tried by count with the receipt path. Receiver rule, one line in the Contract:
   "If you lose context, re-read HARD CONSTRAINTS, then LAST RELIEF, before acting. Next actions are your queue."

**Tests:**
- `test_relief_requires_next_actions`;
- `test_next_action_continue_refused` (plus "Continue." and "keep going");
- `test_next_action_needs_owner_and_success`;
- `test_unfetchable_needs_reason`;
- `test_preamble_shows_last_relief_next_actions_verbatim`;
- No RELIEF receipts exist yet (0 of 5 seat receipts), so the new fields can be required at once. Keep
  `test_relief_stand_relieved_must_be_true_boolean` (`test_fleet_coordination.py:103`) green.

### (a) Claim ledger fields - WORTH IT, but small and merged with evidence_tier

The 5 fields are sound, but they are a proposal (see source 4). Mag already has two halves of the idea:
`checkin_route.py:65,73` (do not promote interpretation to fact) and `cite_gate.py:8-22` (check that the evidence
actually carries the claim's terms and numbers). What is missing is a place for claims in the report.

**Smallest build (recommendation):**
- Optional `claims` array on SPOTREP/SITREP/RELIEF (maxItems 20), with items `{claim, evidence, scope, tier,
  citation}`. `tier` uses the **same enum as STEAL_X_BRIEFS' `evidence_tier`**. Do not add a second
  Fact/Estimate/Interpretation/Prediction enum. If estimates and predictions need separating, add those two values
  to that one enum, agreed with the X-briefs worker. `evidence` must quote the exact supporting text, or be
  `path:line`.
- This needs the object support from (c)(ii).
- **Receiver check, reusing an existing organ:** run each claim through `cite_gate`'s classifier. Only
  `LOCAL-VERIFIED` keeps `tier: measured`. Anything else is demoted to `unverified` in the served copy. URLs stay
  `URL-UNVERIFIED` until the operator opens the `fetch_url` door (`cite_gate.py:156-167`).
- "A new claim routes back to research" becomes: a RELIEF or brief may not contain a claim id absent from the
  sender's ledger. The validator can check this only within one report, so state it as doctrine text in the
  Contract and leave it unenforced.
- **Do not** make it required in every report. Most SPOTREPs are one observation, and a forced 5-field block would
  just be padding.

**Tests:** a valid claims block passes. Missing `evidence` is refused. A bad `tier` is refused. A claim whose
cited local file lacks the claim's number is served as `unverified` (reuse the cite_gate selftest cases A-D). A
report without `claims` still validates.

### (d) Tweprint rules for drafting X posts - WORTH A SMALL LINT (with corrected rules)

Nacho posts himself, so the right home is the draft queue, not the poster. Use the rules the source actually
states (4-8 tweets, 280 characters or fewer, concrete numbers, honest, draft and review before posting), plus two
rules the document added that are worth keeping on their own merit: numbers must match the source exactly, and
hedges must survive.

**Smallest build (recommendation):**
1. `x_surface.lint_thread(text, source_text="")` in `mag/x_surface.py` (pure, no I/O). It splits tweets on blank
   lines or `n/N`, then:
   - **refuses** any tweet over 280 characters;
   - warns outside 4-8 tweets;
   - if `source_text` is given, flags every number in the draft not found verbatim in the source (so "97%" against
     "97.2%" is flagged), reusing cite_gate's number extraction;
   - flags a tweet that carries a sourced number while the source sentence holding that number has a hedge token
     (may, suggests, preprint, in our experiments, about, ~, up to) that the tweet lacks.
   `draft()` (`:74-86`) stores the lint result on the draft. It never blocks a draft, because the operator decides.
2. `mag/x_control_surface.py:486`: replace `text[:280]` with a refusal (`ok: False, error: over 280`).
   Silent truncation is the same erosion as (b), in miniature.

**Tests:**
- `test_post_over_280_refused_not_truncated`;
- `test_lint_flags_rounded_number`;
- `test_lint_flags_dropped_hedge`;
- `test_lint_passes_faithful_thread`;
- `test_draft_never_posts` (`draft` makes no network call; monkeypatch urllib to raise).

### (e) url2llm / markurl - ADOPT NEITHER

- **url2llm** sends every crawled page to an LLM provider for extraction (its README requires `--provider` and
  `--api_key`). That is a model API call per page, which breaks the $0 rule. Reject.
- **markurl** is a 0.1.0 npm package with 0 stars, published in May 2026, and Node-only. The shape is sound
  (Readability, then turndown, then metadata, exposed over MCP), but it is too young to take on as a dependency.
- **What Mag should do instead, if and when the operator says GO on `cite_gate.fetch_url`:** use the
  `httpx` + `beautifulsoup4` already installed. Prefer structured endpoints (the arXiv export API, the GitHub REST
  API and raw files, the dev.to article API, DOI to Zenodo), which is exactly how this report verified its sources.
  Cache the body with a sha256 receipt, as the stub's docstring already specifies.
- Nothing installed.

### Not stolen
- **The six-part source pack:** Mag's STEAL reports already carry question, answer, source table, limits, decision
  and next steps. At most, add a doctrine line for library cards. No code.
- **"Context debt" / Integrator role (Zenodo):** the warm preamble is already Mag's integrator. That paper is
  vocabulary, not a build.

## 4. Order of work
1. (b) `hard_constraints()` + preamble block + its tests. This is the highest value, touches no other worker's
   files, and fixes a live gap: today's breach notice reaches every seat without its instruction.
2. Validator object support (about 15 lines in `_check_prop`) + tests.
3. (c) RELIEF manifest and next_actions + `constraints_sha` on RELIEF + LAST RELIEF in the preamble (doctrine P5).
4. (d) X lint and the `[:280]` refusal.
5. (a) `claims` with the shared evidence_tier enum, after the X-briefs `evidence_tier` field lands.

Left unverified: the bodies of papers 1-3 beyond their abstracts, and the thread-gpt code. Measured: there are
5 `seat_*.json` receipts in watch/receipts and none mentions RELIEF, so no seat has filed a watch turnover yet.
That also means (c) can make the new fields required now with no cut-over problem.
