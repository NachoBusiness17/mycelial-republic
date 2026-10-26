# FIELD2 JUDGE MATERIAL (blind A/B)

One replayed day of real routing receipts (242 work units over 8 arrival
ticks; 67 units were pre-shed failures awaiting retry). Two work-allocation
policies, ARM A and ARM B, processed the identical arrival stream under an
identical service budget (4 units per tick, same 400-tick cap). You judge
which allocation a careful operator should prefer. You are NOT told which
arm is which beyond their behavior below.

The capability table (measured pass rates from the day's ledger; WEAK flags
the dollar-leak coordinates: pass_rate < 0.5 or momentum DECLINING):

| model | task_shape | pass_rate | sample_size | momentum | weak |
|---|---|---|---|---|---|
| deepseek/deepseek-v4.1-flash | adversarial-review | 0.385 | 13 | DECLINING | WEAK |
| deepseek/deepseek-v4.1-flash | planning | 1.000 | 2 | STEADY |  |
| deepseek/deepseek-v4.1-flash | schema-design | 1.000 | 2 | STEADY |  |
| google/gemini-3.8-flash | adversarial-review | 0.633 | 10 | STEADY |  |
| google/gemini-3.8-flash | askbank-v1-safeguard | 0.000 | 3 | STEADY | WEAK |
| legality-propagator-v1 | legality-water-graph-v1 | 1.000 | 100 | STEADY |  |
| mountain-world-v0 | world-tick | 1.000 | 4 | STEADY |  |
| qwen/qwen3.7-flash | adversarial-review | 0.000 | 2 | STEADY | WEAK |
| qwen/qwen3.7-flash | planning | 0.000 | 2 | STEADY | WEAK |
| qwen/qwen3.7-flash | schema-design | 0.000 | 2 | STEADY | WEAK |
| qwen/qwen3.8-max-prime | adversarial-review | 0.444 | 9 | RISING | WEAK |
| qwen/qwen3.8-max-prime | code-analysis | 0.500 | 4 | STEADY |  |
| qwen/qwen3.8-max-prime | grading | 0.250 | 4 | DECLINING | WEAK |
| qwen/qwen3.8-max-prime | planning | 0.429 | 7 | RISING | WEAK |
| qwen/qwen3.8-max-prime | schema-design | 0.333 | 6 | RISING | WEAK |
| x-ai/grok-4.3 | adversarial-review | 0.000 | 2 | STEADY | WEAK |
| x-ai/grok-4.3 | planning | 0.000 | 2 | STEADY | WEAK |
| x-ai/grok-4.3 | schema-design | 0.000 | 2 | STEADY | WEAK |
| x-ai/grok-4.7 | adversarial-review | 1.000 | 9 | STEADY |  |
| z-ai/glm-5.3-prime | adversarial-review | 0.435 | 23 | DECLINING | WEAK |
| z-ai/glm-5.3-prime | askbank-v1-safeguard | 1.000 | 3 | STEADY |  |
| z-ai/glm-5.3-prime | code-analysis | 0.500 | 4 | STEADY |  |
| z-ai/glm-5.3-prime | grading | 0.750 | 4 | RISING |  |
| z-ai/glm-5.3-prime | night-judgment | 0.833 | 6 | DECLINING | WEAK |
| z-ai/glm-5.3-prime | planning | 0.667 | 9 | DECLINING | WEAK |
| z-ai/glm-5.3-prime | schema-design | 0.750 | 8 | STEADY |  |

The SEAT LIST (a blind control list written from the capability table alone,
BEFORE either arm ran; rule: per shape, highest pass_rate with sample_size
>= 3, ties to larger sample then alphabetical):

| shape | seat pick | pass_rate | sample_size |
|---|---|---|---|
| adversarial-review | x-ai/grok-4.7 | 1.000 | 9 |
| askbank-v1-safeguard | z-ai/glm-5.3-prime | 1.000 | 3 |
| code-analysis | qwen/qwen3.8-max-prime | 0.500 | 4 |
| grading | z-ai/glm-5.3-prime | 0.750 | 4 |
| legality-water-graph-v1 | legality-propagator-v1 | 1.000 | 100 |
| night-judgment | z-ai/glm-5.3-prime | 0.833 | 6 |
| planning | z-ai/glm-5.3-prime | 0.667 | 9 |
| schema-design | z-ai/glm-5.3-prime | 0.750 | 8 |
| world-tick | mountain-world-v0 | 1.000 | 4 |

ARM A outcome (all 242 units eventually served; 118 ticks used;
ticks to 80% served: 66; units served at WEAK coordinates: 51 of 242):

| shape | served_at_model | pass_rate | sample_size | units | weak |
|---|---|---|---|---|---|
| adversarial-review | deepseek/deepseek-v4.1-flash | 0.385 | 13 | 1 | WEAK |
| planning | deepseek/deepseek-v4.1-flash | 1.000 | 2 | 16 |  |
| schema-design | deepseek/deepseek-v4.1-flash | 1.000 | 2 | 3 |  |
| adversarial-review | google/gemini-3.8-flash | 0.633 | 10 | 1 |  |
| askbank-v1-safeguard | google/gemini-3.8-flash | 0.000 | 3 | 3 | WEAK |
| legality-water-graph-v1 | legality-propagator-v1 | 1.000 | 100 | 102 |  |
| world-tick | mountain-world-v0 | 1.000 | 4 | 8 |  |
| adversarial-review | qwen/qwen3.7-flash | 0.000 | 2 | 2 | WEAK |
| planning | qwen/qwen3.7-flash | 0.000 | 2 | 2 | WEAK |
| schema-design | qwen/qwen3.7-flash | 0.000 | 2 | 2 | WEAK |
| adversarial-review | qwen/qwen3.8-max-prime | 0.444 | 9 | 21 | WEAK |
| code-analysis | qwen/qwen3.8-max-prime | 0.500 | 4 | 6 |  |
| grading | qwen/qwen3.8-max-prime | 0.250 | 4 | 2 | WEAK |
| planning | qwen/qwen3.8-max-prime | 0.429 | 7 | 1 | WEAK |
| adversarial-review | x-ai/grok-4.3 | 0.000 | 2 | 2 | WEAK |
| planning | x-ai/grok-4.3 | 0.000 | 2 | 2 | WEAK |
| schema-design | x-ai/grok-4.3 | 0.000 | 2 | 2 | WEAK |
| adversarial-review | x-ai/grok-4.7 | 1.000 | 9 | 35 |  |
| adversarial-review | z-ai/glm-5.3-prime | 0.435 | 23 | 3 | WEAK |
| askbank-v1-safeguard | z-ai/glm-5.3-prime | 1.000 | 3 | 6 |  |
| code-analysis | z-ai/glm-5.3-prime | 0.500 | 4 | 1 |  |
| night-judgment | z-ai/glm-5.3-prime | 0.833 | 6 | 6 | WEAK |
| planning | z-ai/glm-5.3-prime | 0.667 | 9 | 2 | WEAK |
| schema-design | z-ai/glm-5.3-prime | 0.750 | 8 | 13 |  |

ARM B outcome (all 242 units eventually served; 182 ticks used;
ticks to 80% served: 134; units served at WEAK coordinates: 92 of 242):

| shape | served_at_model | pass_rate | sample_size | units | weak |
|---|---|---|---|---|---|
| adversarial-review | deepseek/deepseek-v4.1-flash | 0.385 | 13 | 13 | WEAK |
| planning | deepseek/deepseek-v4.1-flash | 1.000 | 2 | 2 |  |
| schema-design | deepseek/deepseek-v4.1-flash | 1.000 | 2 | 2 |  |
| adversarial-review | google/gemini-3.8-flash | 0.633 | 10 | 10 |  |
| askbank-v1-safeguard | google/gemini-3.8-flash | 0.000 | 3 | 3 | WEAK |
| legality-water-graph-v1 | legality-propagator-v1 | 1.000 | 100 | 100 |  |
| world-tick | mountain-world-v0 | 1.000 | 4 | 4 |  |
| adversarial-review | qwen/qwen3.7-flash | 0.000 | 2 | 2 | WEAK |
| planning | qwen/qwen3.7-flash | 0.000 | 2 | 2 | WEAK |
| schema-design | qwen/qwen3.7-flash | 0.000 | 2 | 2 | WEAK |
| adversarial-review | qwen/qwen3.8-max-prime | 0.444 | 9 | 9 | WEAK |
| code-analysis | qwen/qwen3.8-max-prime | 0.500 | 4 | 4 |  |
| grading | qwen/qwen3.8-max-prime | 0.250 | 4 | 4 | WEAK |
| planning | qwen/qwen3.8-max-prime | 0.429 | 7 | 7 | WEAK |
| schema-design | qwen/qwen3.8-max-prime | 0.333 | 6 | 6 | WEAK |
| adversarial-review | x-ai/grok-4.3 | 0.000 | 2 | 2 | WEAK |
| planning | x-ai/grok-4.3 | 0.000 | 2 | 2 | WEAK |
| schema-design | x-ai/grok-4.3 | 0.000 | 2 | 2 | WEAK |
| adversarial-review | x-ai/grok-4.7 | 1.000 | 9 | 9 |  |
| adversarial-review | z-ai/glm-5.3-prime | 0.435 | 23 | 23 | WEAK |
| askbank-v1-safeguard | z-ai/glm-5.3-prime | 1.000 | 3 | 3 |  |
| code-analysis | z-ai/glm-5.3-prime | 0.500 | 4 | 4 |  |
| grading | z-ai/glm-5.3-prime | 0.750 | 4 | 4 |  |
| night-judgment | z-ai/glm-5.3-prime | 0.833 | 6 | 6 | WEAK |
| planning | z-ai/glm-5.3-prime | 0.667 | 9 | 9 | WEAK |
| schema-design | z-ai/glm-5.3-prime | 0.750 | 8 | 8 |  |

Caveat you should weigh: the capability table was measured at END of day, so
any policy reading it has mild hindsight; both arms had access to the same
information, but arm behavior differed in whether it acted on it.
