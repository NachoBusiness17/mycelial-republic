# DUEL_JUDGE2 - DeepSeek as judge number two over the material-carrying duel bank (2026-10-01)

Shoulder 3 of RIB_DEEPSEEK_SHOULDERS_20261001: a third judge family over the duel
verdicts that carried material. Run: `tools/ds_workhorse.py run --in
memory/runs/hermes_burn/judge2_items.jsonl --prompt-file
memory/runs/hermes_burn/ds_baseline_prompt.md --out
memory/runs/hermes_burn/judge2_duel.jsonl`. 9 items, all ok, 1 attempt each,
$0.0102 total. Judge: deepseek-chat (thinking off, temp 0.3), blind: slots labeled
ANSWER 1 / ANSWER 2, no model names, no costs, no material bytes.

## Format reality (read before the table)

The DUEL1_hidden_* / DUEL2_train_* files are ONE contender pass each, not duel
transcripts. The format names ONE contender per file (header line names the model;
the body title names the ask and draw, e.g. "Contender answer: ab1-coremem-safeguard
(draw v1h-0008)"). No file states a verdict. The estate's only banked answers to the
SAME ask ids live in `watch/inbox/last_mile_20260930/d6_contenders.jsonl`
(glm-prime and gemini-3.8-flash, 3 rounds each on ab1-coremem-safeguard, judged by
ember with verdicts in `logs/duel/duels.jsonl` rows d6ab-r1/r2/r3).

Poison census (skip rule applied by substance, not literal string): all 19 r1
outputs are poisoned - every one opens with a no-material status in varying
wording ("material not received", "BLOCKED on material", "the material is not in
my input", ...); the two literal mission strings matched only train_01 and
train_06. DUEL1_hidden_5 r1 never landed (the 46x refusal loop); its r2 landed
clean and did NOT refuse. Clean set at run time: 6 hidden r2s (train r2s were
still landing; 11 of 20 on disk at report time). Of the clean outputs only
DUEL1_hidden_1_r2 (ab1-coremem-safeguard) has same-question incumbents banked, so
only it yields judgeable duels; the other clean r2s (gates/cml/chainreg/mcpman
asks) have no opponents yet and await the contender store pairing - that is by
design ("CONTENDER PASS ... banks into the contender store for later blind
judging"), not a defect of this pass.

Question used (identical for all 9 items): bank v1 body of ab1-coremem-safeguard
(read from `configs/ask_bank/v1/hidden/bank.jsonl`; per the AJ2 convention only the
first line is quoted here: "You are an adversarial specification reviewer hunting
the missing guardrail. Below is the full text of docs/ref/CORE_MEM"). Slots
alternate across items to blunt first-position bias (V8: slot-A favoritism is real,
p=0.0436).

## Results

| duel id | judge2 pick | confidence | original verdict (stated where it exists) |
|---|---|---|---|
| j2-d6ab-r1-glm-gem | glm-prime | 82 | ember winner A = glm-prime (duels.jsonl d6ab-r1-glm-gem) - AGREE |
| j2-d6ab-r2-glm-gem | glm-prime | 78 | ember winner A = glm-prime (d6ab-r2) - AGREE |
| j2-d6ab-r3-glm-gem | glm-prime | 88 | ember winner A = glm-prime (d6ab-r3) - AGREE |
| j2-claude-glm-r1 | claude (DUEL1_hidden_1_r2) | 82 | none stated (no prior verdict exists for a claude pairing) |
| j2-claude-glm-r2 | claude | 82 | none stated |
| j2-claude-glm-r3 | claude | 82 | none stated |
| j2-claude-gem-r1 | claude | 84 | none stated |
| j2-claude-gem-r2 | claude | 88 | none stated |
| j2-claude-gem-r3 | claude | 82 | none stated |

Agreement rate where comparable: 3/3 = 100% (judge2 vs ember on the only three
askbank duel verdicts that carried material; both judges took glm-prime over
gemini-3.8-flash every round, and judge2's slot alternation shows the pick is not
a position artifact: 5 picks landed on ANSWER 1, 4 on ANSWER 2).

Cross-read on the not-comparable rows: judge2 ranks the NEW contender family
(claude-sonnet-5.5) 6-0 over BOTH incumbents on the one shared ask, confidence
82-88, winning 3 times from each slot. The decisive criterion DeepSeek cited in 5
of the 6 claude wins is the same observation: the spec's own Section 1 test
("the read fragment's hash exists in the chain post-read") is satisfied by the
fragment's ORIGINAL commit row, so the audit passes falsely with zero re-anchor
activity - claude's answer is the only one that names that false-pass mechanism
and binds the fix to a read_id receipt.

## What blind judging cannot see (the honest note)

- The material bytes. The judge sees only the question and the two answers, so it
  cannot verify that any quoted clause exists in CORE_MEMORY_PROTOCOL.md. It
  cross-checks answers against each other, not against the document: a confident,
  well-shaped fabrication quoting invented clauses could win. Verification of the
  winning citations still has to happen against the file (sha
  f014e1bd...e107977).
- Identity and price. The judge cannot weigh cost per answer: claude's r2 cost
  $0.0616 (usage.jsonl) vs glm-prime $0.0146-0.0174 and gemini $0.0287-0.0400 in
  the D6 series. On value-per-dollar glm-prime's 3 losses narrow considerably;
  claude's sweep is a quality result, not a router verdict.
- Channel shape. Two clean hidden r2s (hidden_4, hidden_5) landed on the reasoning
  channel (content empty); hidden_1_r2 judged here was content-channel. A blind
  judge can penalize reasoning-channel prose style without knowing why it reads
  differently.
- Estate style laws. glm#r2 contains an em-dash; the judge was not told about the
  no-em-dash law, so style-law violations do not factor into picks.
- The original rubric. Ember scored 4 criteria (coverage, severity, citations,
  actionability) per duel; judge2 gave a holistic pick. The 3/3 agreement is
  family-level, not criterion-level.
- n=1 per item. The rib itself says single-judge flips are a known factor; each
  item above is one temperature-0.3 DeepSeek opinion. The 3-round-per-matchup
  shape and the ember agreement mitigate but do not remove this.

## Files

- Items: `memory/runs/hermes_burn/judge2_items.jsonl` (9 rows, slot map encoded in ids)
- Results: `memory/runs/hermes_burn/judge2_duel.jsonl` (9 rows, ok, $0.0102)
- Incumbent answers: `watch/inbox/last_mile_20260930/d6_contenders.jsonl`
- New contender answer: `watch/inbox/hermes_burn/DUEL1_hidden_1_r2.md`
- Original verdicts: `logs/duel/duels.jsonl` rows d6ab-r1/r2/r3-glm-gem
