## Defect 1: fire() retry does not actually rotate keys

Where: fire(), the line `key = keys[hash((tag, attempt)) % len(keys)]`.

Evidence: the module docstring promises "Retries reuse the same model with the next key", but the index for attempt 2 is `hash((tag, 2)) % len(keys)`, which is not guaranteed to differ from `hash((tag, 1)) % len(keys)`. Worse, Python salts str hashing per process (PYTHONHASHSEED), so which key each attempt picks is nondeterministic across runs. With a two-key list there exist tags where both attempts draw the same key, and which tags do this changes every process start.

Damage: if the drawn key is dead (expired quota, 402), both attempts hit the same dead key and the duel aborts even though a live key was in the list. Failures are also un-reproducible: the same ask can pass in one process and abort in another.

Falsifying predicate: inject keys [dead, live] where dead returns HTTP 402; for a sweep of 1000 tags assert that attempt 2 never reuses the attempt-1 key when the attempt-1 key just failed. Fails today; passes when selection is `keys[(i + attempt - 1) % len(keys)]` with the failed key rotated out.

## Defect 2: cost_of() fallback fabricates costs silently

Where: PRICE dict plus cost_of().

Evidence: cost_of() prefers usage.cost but silently falls back to the static PRICE table when it is absent. The comment admits the table is "budget meter fallback only", yet the ledger row written by run_duel() records the resulting number in a_cost/b_cost/judge_cost with no marker of its source. Nothing downstream can distinguish an API-metered dollar from a guessed dollar.

Damage: every cost-per-quality ratio computed from the ledger (the exact feed a future router wants) inherits invented numbers whenever usage.cost goes missing, with no way to filter those rows out later. A fallback that can be wrong by multiples (rates drift; UNPROVEN how far, the live catalog is outside this source) and is unmarked is worse than no fallback.

Falsifying predicate: call cost_of("fireworks/ember-1", {"prompt_tokens": 1000000, "completion_tokens": 0}) with usage.cost removed; today it returns 0.3 from the stale table. Assert instead that it either raises, or the row gains a meter_source field set to "fallback" so analysis can drop it. Also assert the ledger schema rejects rows lacking meter_source once introduced.

## Defect 3: parse_judge() banks verdicts that skipped the criteria table

Where: parse_judge(), the line `parsed = winner in ("A", "B", "TIE") and bool(rationale)`.

Evidence: a judge reply of just two lines, "WINNER: A" and "RATIONALE: ...", parses as fully valid with criteria == []. run_duel() banks the row and main() returns 0. len(criteria) is never compared to len(rubric), so an un-scored verdict is indistinguishable, in every downstream consumer, from a scored one.

Damage: the per-criterion scores are the raw material for style-control and rubric-drift regression; losing them silently shrinks that analysis with no trace, and a judge that stops producing tables degrades the ledger quality invisibly.

Falsifying predicate: feed parse_judge the text "WINNER: B\nRATIONALE: why" and assert parsed is False (or run_duel refuses to bank / banks with an explicit criteria_missing flag). Today parsed is True and the row lands with empty criteria.

## Missing safeguard: no truncation marker at ANSWER_LIMIT and CONTEXT_LIMIT

Where: judge_prompt(), the slices `a_text[:ANSWER_LIMIT]`, `b_text[:ANSWER_LIMIT]`, `context[:CONTEXT_LIMIT]`.

Evidence: any answer over 20000 chars or context over 9000 chars is cut with no notice to the judge and no note in the ledger row. The judge scores a prefix believing it is the whole answer.

Damage: long-form contenders are systematically judged on whatever happened to sit in the first 20000 chars; the bias is invisible because the row logs full a_chars/b_chars, which makes the truncation look like the judge saw everything.

Falsifying predicate: build judge_prompt with a 25000-char answer and assert the prompt contains an explicit truncation notice naming how many chars were cut; today no such marker exists.

UNPROVEN: swap alternation reads global ledger parity (`ledger_row_count(out_path) % 2 == 1`), which assumes a single writer to duels.jsonl; I have not observed concurrent writers, but any second lane appending rows would flip parity of subsequent duels unpredictably.

Ranking by damage: defect 2 (silent cost fabrication poisons all downstream economics), defect 1 (nondeterministic aborts), defect 3 (invisible loss of scoring), then the missing truncation marker.
