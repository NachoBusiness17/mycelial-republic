# XAI GROK-4.7 SEAT REPOINT receipt · 2026-09-25

Task: long-horizon seat repoint to grok-4-7 ($2/$6, fast variant where latency-bound).
Seat: grok-repoint (MICKEY-17 wave, xai-week lane). Status: PLANNED, not wired.

## What is true on the wire (ran this session)

1. Catalog probe (ran: `.venv/Scripts/python.exe _tmp_grok47_catalog_probe.py`, GET
   `https://api.x.ai/v1/models` with `XAI_API_KEY` from `.env`, HTTP 200, $0 spent,
   no completion call): 13 models. `grok-4.7` is PRESENT (created epoch 1788307200,
   ~2026-09-02). Neighbors: grok-4.5, grok-4.6, grok-4.3, grok-4.20-* trio,
   grok-build-0.1, imagine models. Live id uses dots: `grok-4.7` (the ask's
   "grok-4-7" shorthand resolves to this).
2. Key state: `.env:7` `XAI_API_KEY` set (84 chars, alive per the 200 above);
   `.env:8` `XAI_MODEL=grok-4` (stale alias, sees the 4.x chain today);
   `.env:114/115` `GROK_API_KEY` / `GROK_API_KEY_2` empty. Chain per
   `mag/grok_rightsize.py:91`: XAI_API_KEY, XAI_API_KEY_2, GROK_API_KEY, GROK_API_KEY_2.
3. Pricing (ran: fetched `https://docs.x.ai/developers/pricing`): grok-4.7
   <200k prompt tokens $2.00 in / $6.00 out per 1M; >=200k $4 / $12. Matches the ask.
   grok-4.5 and grok-4.6 share the same $2/$6 band, so the repoint is same-money,
   newer-frontier.
4. Fast variant: NO `grok-4.7-fast` id in the live API catalog (13 models checked).
   "Grok 4.7 Fast" exists only on Cursor and Grok Build surfaces at 2x rates
   ($4/$12 below 200k). Latency-bound lanes that want Fast stay on those surfaces;
   the raw-API seat wires plain `grok-4.7`.

## Why the wiring stays commented (gate law)

- `mag/grok_rightsize.py:330` (grok_route.v1, operator law 09-05): cash API blocked
  unless `GROK_ALLOW_PAID=1` or `XAI_CASH_ALLOWED=1`. `configs/keys.json` `grok_cash`
  role: `PAYG_blocked_by_grok_route_law`, status `armed-only-by-operator`.
- `configs/providers.yaml` (xai block, lines 348-369, default_model `grok-3-mini`,
  models [grok-3-mini, grok-3, grok-4.5]) is hash-sealed by
  `configs/.config_seal.json:31`; any byte edit fails `tools/config_seal.py verify`
  until a named re-seal. Editing it now would put the live seal red while the lane
  is still gated. So: commented-ready lines here; operator applies + re-seals by name
  when arming.

## Commented-ready config lines (paste when operator arms the lane)

In `configs/providers.yaml`, xai block (after line 359, the grok-4.5 entry):

```yaml
      # - grok-4.7   # xai-week 2026-09-25 repoint: frontier slot, $2/$6 <200k
      #               # ($4/$12 >=200k). Live in catalog 2026-09-25 probe.
      #               # Fast variant is Cursor/Grok-Build only, NOT wireable here.
```

and flip the frontier default (orchestrate tier) when arming:

```yaml
    # default_model: grok-3-mini   # keep: rightsize law, cheap tiers stay here
```

In `mag/grok_rightsize.py:49`, BUDGETS orchestrate tier:

```python
    "orchestrate": {"model": "grok-4.7",     "max_tokens": 4096, "temp": 0.3, "est_cost": 0.0250},  # was grok-4.5, same $ band
```

and `mag/grok_rightsize.py:437-438` cost tables:

```python
    cost_per_1m_in  = {..., "grok-4.7": 2, ...}   # <200k band
    cost_per_1m_out = {..., "grok-4.7": 6, ...}
```

In `configs/cost_rates.yaml` model_rates (next to grok-4.5 at line 86):

```yaml
  grok-4.7:
    provider: xai
    rates: {cache_hit_per_m: 0.3, cache_miss_per_m: 2.0, output_per_m: 6.0}
    source: https://docs.x.ai/developers/pricing
```

Optional: `.env` `XAI_MODEL=grok-4.7` replaces the stale `XAI_MODEL=grok-4`.

Operator apply sequence: arm gate env, apply lines, then
`python tools/config_seal.py update --by <name> --note "grok-4.7 repoint"`.

## Ledger

Row appended to `watch/inbox/endpoint_news/endpoint_news.jsonl` (first `source: xai`
row in the file): `kind: seat_repoint_planned`, model `grok-4.7`, wired false,
gate named. Appended via json.dumps, verified by re-reading the tail.

## Honest limits

- No paid completion was made (gate blocked + budget law); latency of grok-4.7 is
  UNMEASURED. The Fast-variant guidance comes from the pricing page, not a run.
- `configs/.config_seal.json` was already FAILING on `lanes.yaml` (modified today
  20:17, after the 19:35 re-seal) before this seat wrote anything. Pre-existing
  drift from another seat; not re-sealed here (named act). This seat wrote nothing
  under `configs/`.
- Seat playbook prior `configs/seat_playbook.yaml:90` (grok_tui 3.0/15.0) is stale
  vs the $2/$6 page; updating it is part of the same named re-seal when this lands.

## Read trail

`configs/providers.yaml:348-369`, `mag/grok_rightsize.py:43-50,88-137,437-438`,
`configs/lanes.yaml:19-22,71-74`, `configs/seat_playbook.yaml:74-90`,
`configs/cost_rates.yaml:86-89,106-112`, `configs/keys.json` grok_cash block,
`configs/.config_seal.json:31`, `tools/config_seal.py:50-73`,
`watch/inbox/COMPUTE_WEALTH_INVENTORY_20260918.md` (xai ALIVE 293ms),
`watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md:25` (xai-week lane context),
`scripts/endpoint_news.py` (row schema).
