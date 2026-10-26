# Z18 - STYLE REGRESSION: is glm's duel lead style or content? - 2026-09-29/30

Mission (S5 full fix, analysis pass): fit a style-control logistic
regression over `logs/duel/duels.jsonl` (blind v1.1 era rows carrying
a_chars/b_chars/a_headers/b_headers) predicting win probability from
normalized char and header differences plus a model-identity dummy,
then answer: does length hurt? do headers hurt? is glm's lead
explained by style or by content? No API spend, no commit.

## What landed

- `tools/duel_style_regression.py` (new): numpy-only IRLS/Newton
  logistic regression, Wald SEs from the inverse Fisher information,
  read-only over the ledger, `--json` for machine output, `--ledger`
  to pin a snapshot. Zero network, zero spend.
- `watch/inbox/hydrology/z18_duels_snapshot.jsonl`: frozen byte copy
  of the ledger at analysis time. The ledger is LIVE (a sibling lane
  fired duels while this ran: 12 -> 16 -> 18 rows), so every number
  below is pinned to this snapshot, per the census law (name the
  instrument, the moment, and the delta; rerun the tool for fresh
  numbers).

## Data snapshot

- sha256 `1a746c3be8b395f8fd98ff4aaefed847fa5e498200e0cd24be7c725b8741c66e`,
  taken 2026-09-30T09:23Z, 18 rows.
- 1 row skipped (retro baseline row 0 predates header fields),
  1 TIE dropped in the primary fit (duplicated 0+1 in sensitivity S1),
  16 effective rows, all one pairing: qwen3.8-max-prime vs glm-5.3-prime.
- Raw glm record 10-6 (62.5 percent); exact one-sided binomial
  p = 0.227. The lead itself is not yet statistically solid ground.

## Design honesty (why no literal identity dummy column)

The mission asked for a model-identity dummy. With exactly ONE pairing
in the ledger (glm appears in every row), the side-identity dummy is
constant and perfectly collinear with the intercept, so the tool
detects this, drops the column, and the INTERCEPT IS the identity
term: glm's win log-odds at style parity, i.e. glm's content-driven
lead after style control. If a future ledger gains mixed pairings the
dummy gains variation and enters for real. All regressions are from
the glm perspective: y = glm win; char_diff = (glm_chars - qwen_chars)
/ mean; hdr_diff likewise; positive char_diff = glm relatively longer.

## Coefficients (primary spec M1, n=16; log-odds, Wald SE)

| term | b | se | z | p (2-sided) |
|---|---|---|---|---|
| intercept (= glm identity at style parity) | +2.26 | 1.55 | +1.45 | 0.146 |
| char_diff_norm | +5.89 | 3.67 | +1.60 | 0.109 |
| hdr_diff_norm | +0.33 | 1.67 | +0.20 | 0.843 |

Supporting specs agree in direction: M0 intercept-only gives the raw
0.625; M2 adds a presentation-slot dummy (glm in slot A, i.e. swap)
which is null (b +0.27, p 0.83), so no slot-order artifact; S1 (ties
duplicated, n=18) gives intercept +2.15, char +4.94, hdr +0.35.

## Findings (all suggestive; n=16, nothing clears p < 0.10)

1. DOES LENGTH HURT? Not in the naive direction. The char_diff slope
   is POSITIVE: win probability falls as the glm side gets much
   SHORTER than qwen. glm's losses (and qwen's wins) cluster at
   char_diff -0.30 to -0.66; glm's wins cluster near parity (-0.05,
   -0.01, +0.16). Read plainly: qwen's 2x-verbose answers did not
   visibly cost it; the much-shorter side lost more. Pearson
   r(char_diff, glm_win) = +0.51.
2. DO HEADERS HURT? No detectable effect (b +0.33, p 0.84), but the
   design cannot test it honestly: glm has FEWER headers in every
   effective row (constant-sign collinearity with identity), so a
   header effect is unidentifiable in this ledger, only weakly
   bounded toward zero.
3. IS GLM'S LEAD STYLE OR CONTENT? Style control does NOT explain it
   away; it grows. Raw win prob 0.625 vs 0.905 at style parity
   (intercept +2.26 log-odds, p 0.146). Under this fit glm's short,
   header-light style is a HEADWIND against it, and a content
   advantage survives anyway. The rival reading stands: length and
   identity are entangled (glm was the shorter side in 15 of 16
   effective rows), so the split is weakly identified and could move
   as n grows.

## VERDICT

Suggestive, not established (n=16, all p > 0.10): glm-prime's 10-6
blind-era lead is CONTENT-shaped, not style-shaped; the only style
gradient visible runs opposite the folklore: writing much shorter
than the opponent is the liability, verbosity up to 2x is not
penalized by the ember judge; headers show no measurable effect and
cannot be separated from identity until a duel lands where the glm
side out-headers qwen. Keep sampling toward n=30 per the T3 clause
before any router row is rewritten; rerun this tool then.

## Repro

    .venv/Scripts/python.exe tools/duel_style_regression.py \
        --ledger watch/inbox/hydrology/z18_duels_snapshot.jsonl
    .venv/Scripts/python.exe tools/duel_style_regression.py --json

No em-dashes in the tool or this receipt (byte check chr(0x2014)).
No commit made; no API spend; ledger untouched (read-only; snapshot
is a copy).
