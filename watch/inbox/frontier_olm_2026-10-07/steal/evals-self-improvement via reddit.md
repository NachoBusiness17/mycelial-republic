# STEAL CARD: evals-self-improvement via reddit (frontier OLM 2026-10-07)

Two confirmed r/LocalLLaMA finds, both practitioner threads, both converging on laws the
estate cares about. Card drafted by the steal gopher this session; every code cite below
was read this session, every command below was run this session.

## Find 1: decontamination reports cannot fix benchmark contamination (1wli359)

- URL: https://www.reddit.com/r/LocalLLaMA/comments/1wli359/why_decontamination_reports_cant_fix_benchmark/
- Finder quote (from the ask's confirmed find, read post + all 9 comments): "When a model's
  public score climbs but the private score stays flat, that's your contamination signal"
- Post-level verification (this session): arctic-shift archive API `posts/ids?ids=1wli359`
  returned the exact title "Why decontamination reports can't fix benchmark contamination,
  and what an evaluator has to do instead", 9 comments, created_utc 1789913383 (2026-09-20).
  The selftext opens on OpenAI stopping SWE-bench Verified reporting because frontier models
  could reproduce the human-written reference fix.
- Comment-level quote refetch: OWED. `arctic-shift.photon-reddit.com/api/comments/search`
  422'd on both param shapes tried (link_id=t3_1wli359 and link_id=1wli359). The quote
  stands on the confirmed find in the ask, not on a fresh fetch by this seat.
- Community mechanism (the steal): lab-side decontamination search is structurally unable to
  prove unseen-ness. What an evaluator does instead: (a) generate eval tasks AFTER the eval
  set froze (provably unseen by construction), and (b) treat public/private score DIVERGENCE
  as the standing contamination signal, not any single score.

### Estate prior art (reverse-GPS, read this session)

- Held-out sets exist and are hash-sealed: `tools/battery_rerun.py:18-22` never opens
  GROUND_TRUTH_HELDOUT.md outside the score phase, `:143-153` fails HELDOUT DRIFT on any
  sha256 change.
- Post-freeze task generation exists: `tools/duty_fuzz.py:14` "Held-out by construction:
  case global index g = cycle*1000 + i" mints fresh cases per gate cycle.
- Contamination epistemics exist for one instrument: `mag/mirror_control.py:16-24` condition
  C probes the zeitgeist mirror with doctrine in orthogonally-worded text (does the mirror
  measure words or ideas).
- The eval cadence organ: `mag/improve.py:1-33`, scout to candidates to eval to promote,
  with B2-106 provider-health showing the landing pattern for a new signal class: a stale
  cadence fires a probe and lands a candidate row (kind=risk on alarm, status=hold when
  quiet).

### The delta (what is actually new to port)

No estate organ computes the PAIR. Duty-fuzz mints unseen cases, battery seals held-out
truth, mirror_control runs a one-shot instrument control; nothing runs the same eval twice,
once on corpus-SEEN material and once on a post-freeze MINTED twin, and tracks the delta as
a standing tripwire. That pair-divergence-as-signal is the community's converged answer and
it is the steal.

### Organ map

Feeds the SOVEREIGN MIRROR plus the improve loop. Port move: graduate mirror_control's
condition C from lexical-instrument calibration to a standing paired-score tripwire; every
improve-cadence eval that scores a lane/model on seen material also scores a same-shape
minted-twin set (duty-fuzz-style generation), and the DIVERGENCE lands as an improve
candidate row using the existing B2-106 kind=risk pattern (`mag/improve.py:26-33`).

### Falsifiable probe (cheap, $0, one lane)

Mint 12 unseen-arm asks from TODAY's closeout receipts (answers did not exist before today,
post-freeze by construction) and pair them with 12 seen-arm asks of the same shape whose
answers are present in pre-today catalog/memory bytes. Run both arms through one local
ollama janitor lane (gemma:2b or gemma4) with one deterministic grader, twice. Contamination
signal fires iff the seen arm climbs while the minted arm stays flat. Both arms tracking
each other falsifies the contamination worry for that lane. Either outcome is a landed row.

## Find 2: citation allowlist hard-fail for grounded generation (1uolb4y)

- URL: https://www.reddit.com/r/LocalLLaMA/comments/1uolb4y/local_llm_for_legaldocument_adaptation_keeps/
- Finder quote (from the ask's confirmed find, read post + all comments): "any citation in
  the output that isn't in the input list fails the run"
- Post-level verification (this session): arctic-shift `posts/ids?ids=1uolb4y` returned the
  title "Local LLM for legal-document adaptation keeps hallucinating citations with total
  confidence" plus a trailing question clause about grounding, model, and pipeline ideas;
  34 comments at fetch time vs 38 in the find record (thread counts drift; noted, not a
  blocker); created_utc 1783306646 (2026-07-06). Selftext: a criminal defense lawyer,
  client-confidential material, local-only non-negotiable.
- Comment-level quote refetch: OWED, same 422 as Find 1.
- Community mechanism (the steal): 38-comment convergence on three rules: citations must
  come from an INPUT ALLOWLIST (fail the run on any cite outside it), grep each citation
  against the actual source text, and gate on grounding never on model confidence.

### Estate prior art (read this session)

- Repo-time prose lint: `tools/citation_lint.py:17-32` (PATH-MISSING, LINE-OOB, EMPTY-SPAN,
  PHANTOM-NUMBER, TOKEN-MISS) with scope `--changed`/`--files` per `:34-38`.
- Runtime per-card gate: `mag/cite_gate.py:8-14` tri-state classes, where LOCAL-VERIFIED
  means "path exists under ROOT and is non-empty" (`:9`), plus LAW-064 subject-match.
- Batch material law: ds_workhorse STANDING_RAILS ok_api + ok_material (AGENTS.md Commands).

### The delta (what is actually new to port)

Both estate gates verify against the WHOLE repo. citation_lint passes any cite whose path
exists and whose span mentions the claim tokens; cite_gate LOCAL-VERIFIES any non-empty
path under ROOT. Neither checks that the cited source was in the AUTHOR'S INPUT SET. A seat
citing a sibling lane's file it never read passes both gates today. The community rule is
input-scoped: the allowlist is the input list, and a cite outside it fails the run.

### Organ map

Feeds the GOPHER FLEET plus the CONTEXT PACK. Port move: an INPUT-ALLOWLIST gate on subagent
outputs. The ask's source material (finds JSON, research pack, context pack; organ card
`mag/organ_map.py:81-90`) defines the allowlist; every path/URL cite in a returned card
must resolve into that set or be explicitly marked OWED / verified-this-session with a
receipt. This tightens, not replaces, `tools/citation_lint.py` and `mag/cite_gate.py`.

### Falsifiable probe (deterministic, $0, one script)

Write one script over the banked steal cards (corpus/steal/*.md and any prior
watch/inbox/frontier_olm_*/steal/*.md): extract every cited path/URL, test membership in
that card's input find material, and count INPUT-ESCAPE findings where the cite resolves
repo-wide (so PATH-MISSING would pass) but is absent from the input set. Prediction: a
nonzero count proves the new gate class catches real input-escapes the current lint cannot
see; a zero count downgrades this steal to converged validation of existing drafting
discipline. One run answers it either way.

## Overlap receipt (this session)

Command: `git grep -n -e "1wli359" -e "1uolb4y" -e "decontamination report" -- catalog memory`
Output: zero hits, `grep_exit=1`. No prior estate record of either thread ID or the
decontamination topic; both finds are new material to this catalog and memory tree.

## Verification ledger

Verified this session: both post titles/topics/comment counts/created_utc via arctic-shift
posts API; zero-overlap grep; code cites above read via sed/dir (organ_map, cite_gate,
mirror_control, garden_grade, improve, state_quantizer, duty_fuzz, battery_rerun,
citation_lint). OWED: comment-body refetch for both quotes (archive search endpoint 422,
three attempts); the paired-run probe and the input-allowlist audit are named, not run, per
the card's scope (draft and bank, probes are next).
