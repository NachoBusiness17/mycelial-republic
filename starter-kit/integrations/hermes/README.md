# Hermes-class agent integration

The kit plugs into any Hermes-style autonomous agent runtime (a
persistent agent host with skills, a dispatch log, and background
workers). Three wires:

## 1. Skills mount (discovery-shaped)

Runtime skill discovery expects a CATEGORY DIRECTORY per skill, each
holding a SKILL.md - a flat pile of .md files will not be found. Mount
the kit's cards in that shape:

```
starter-kit/
  skills/
    conversation-miner/SKILL.md   <- copy of agent/conversation-miner.md
    profile-grower/SKILL.md
    law-minter/SKILL.md
```

```bash
for c in conversation-miner profile-grower law-minter; do
  mkdir -p <your-runtime-skills-dir>/$c
  cp agent/$c.md <your-runtime-skills-dir>/$c/SKILL.md
done
```

If your runtime reads a manifest instead, register each card with its
name + description line. The three cards are the reactive loop - mount
those first.

## 2. Profile as the boot state (state OUTSIDE the read-only mount)

Point the runtime's boot at the kit's profile:

```bash
python tools/profile_boot.py --memory /state/profile
```

Exit contract the host keys on: 0 profile found (boot brief printed) /
1 FIRST BOOT (trigger the mining loop's first run) / 2 corrupt (phantoms
or traversal-law violations - block batch dispatch until the census
passes) / 3 crash (treat as an incident, never as first boot).

If your Hermes runs in a container, keep the profile OUTSIDE the
read-only kit mount, on its own read-write volume:

```
docker run -v /path/to/starter-kit:/kit:ro -v hermes-state:/state:rw ... \
  <hermes-image> python /kit/tools/profile_boot.py --memory /state/profile
```

The one-way-mirror shape: the runtime pulls the body of law read-only,
pushes only memory rows and receipts. A read-only --memory path will
crash first boot with exit 3 - that is the contract working.

## 3. Headless lanes

The kit's lanes (SUBSYSTEMS.md organ 4) run as scheduled jobs in your
runtime's scheduler. Laws: bounded ask/steps/tokens per wave
(PROTOCOLS.md), checkpoints per leg, receipts to the inbox, and the
master watcher gets past wedges (refusals, loops) by repairing the ask
once, then escalating. Interrupts steer, never kill - the lane resumes
from its checkpoint; nothing touches host processes it did not start.

## 4. The paid wire (budget laws from day one)

`hermes_client.py` reaches a Nous-shape inference API with the budget
laws already on. Stdlib only (`http.client`); no live spend without an
operator key, and `test_hermes_client.py` proves every law offline with
a mocked transport:

```python
from hermes_client import fire, make_jsonl_bank

out = fire(
    "anthropic/claude-haiku-4.5",
    [{"role": "user", "content": ask_text}],
    key=operator_key,                      # fire refuses without one
    bank=make_jsonl_bank("state/usage.jsonl"),  # every dispatch banks its burn
    ask_dir=Path("queue") / ask_id,        # terminal markers live here
    ask_id=ask_id,
)
```

The four laws `fire()` enforces, each ported from the estate carrier
that paid for it (`tools/hermes_burn.py` + `mag/inference_budget.py`):

1. **plan_call before every fire** - a `max_tokens` floor per ask shape
   (small 8000 / review 18KB+ 24000, per-animal overrides), thinking
   control merged, forbidden params stripped; the plan rides the wire
   unmodified. A plan dropped between compute and wire is the burn that
   paid for this law (15998 reasoning tokens, empty content).
2. **guard_terminal on every response** - an empty content channel with
   `finish=length` plus token evidence of burn mints an
   `EMPTY_REASONING` marker in the ask dir and the same params are
   NEVER refired (recover: re-stage with the recipe or switch family).
   Call `skip_terminal` (done inside `fire`) before every retry.
3. **The thinking-control law** - per-animal, and explicit: omission of
   the thinking key is a measured ON state for some animals (deepseek),
   so the off switch is SENT on the wire (`thinking {type: disabled}`);
   others are capped (`reasoning {max_tokens: 6000}`) or uncapped
   entirely (glm-5.3-flash: any cap returns empty). The table is
   `FAMILY_TABLE` in `hermes_client.py`, every row citing its receipt.
4. **A ledger, not vibes** - every fire, refusal, transport failure and
   burn appends a usage row with its cost. A floor is a routing
   decision with money teeth: the estate's review floor once priced an
   ask's reserved cost over the provider balance and it 402ed
   deterministically every hourly fire until the ledger made the wall
   visible.

The endpoint is a configured literal (`DEFAULT_ENDPOINT`, one
allowlisted https host), re-fenced per call: wrong host, wrong scheme,
altered port, or DNS resolving to a private/loopback address all refuse
before any bytes move. Point it at your own compatible endpoint by
editing `ENDPOINT_HOST`/`DEFAULT_ENDPOINT` - the fence shape stays.
