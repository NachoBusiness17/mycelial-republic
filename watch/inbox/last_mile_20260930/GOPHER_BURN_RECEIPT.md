# Hermes gopher burn G1-G6 receipt (2026-09-29/30, Nous, $1.43 total) — MOSTLY EMPTY RETURNS

Raw: logs/hermes_gopher_burn_20260929/output.jsonl (round 1, $0.3564) + output2.jsonl (round 2, $1.0768).

## Honest verdict

11 of 12 returns have ZERO content. Only `G4-ember-workhorse-test` on glm-5.3-prime
(round 2, 5,768 chars) delivered a real answer. Round 1 burned $0.36 for nothing;
round 2 burned $1.08 for one answer. Total wasted: ~$1.29.

Root cause: the known reasoning-eats-completion disease on Nous primes (LESSIG RAILS:
reasoning {max_tokens} cap + retry — the stealth driver already carries the cure; these
gopher calls did not). The duel driver (v1_multifamily_duel.py) independently hit and
fixed the same disease this session with a STREAMING contender caller + per-family
failure tolerance. The gopher driver needs the same rails before any round 3.

## What did land

- G4-ember-workhorse-test (glm-5.3-prime, 5,768 chars): the only real content; read + banked into the duel calibration lane.
- Per-model cost truth (usable for the price table): qwen3.8-max-prime ~$0.07-0.25/ask depending on reasoning burn; glm-5.3-prime $0.07-0.15; ember-1 $0.0055 (cheap but empty on round 1).

## Law

A burn that returns empty content is not a burn, it is a metering error. Before any
future gopher round: (1) the driver must assert content_len > 0 per row and retry with
the rails on empty; (2) round N+1 must not fire until round N's empties are explained.
The night burn (N1-N6) shows the same driver WITH rails returns full content every time
($0.41, 6/6 non-empty) — the disease is the driver, not the models.
