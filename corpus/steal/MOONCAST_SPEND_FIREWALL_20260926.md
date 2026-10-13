# MOONCAST SPEND FIREWALL (steal receipt, gopher t6a, 2026-09-26)

Covers the two laws the a22 council lane proved uncovered by corpus/steal/ (zero grep hits for Mooncast and FREE_MODELS there). Sources read: tools/roblox_npc_gateway.py lines 30-130 and watch/inbox/gala_20260925/w3/lanes/a22-councils.json. Both quotes below byte-verified with grep -F, evidence in watch/inbox/gala_20260925/afterparty/lanes/t6a.check.txt.

## LAW

1. HOMOGENEITY-DECAY: a council of same-type models aligns too cheaply, so unanimity becomes a fake signal; councils must be cross-family.
2. SPEND-FIREWALL: funded-key spend is blocked structurally, not politely. The free-model allowlist check fires BEFORE the funded lane loop; gate-then-lanes, and the ordering is the proof.

## CLAIM

The gateway inlines the Mooncast law as a source comment and enforces it twice over. Heterogeneity is enforced by pinning survey witnesses cross-family. Spend safety is enforced by control flow: any model outside FREE_MODELS is refused, logged as a gate receipt, and returned before the loop that loads funded keys is ever entered, so client-supplied model input cannot reach paid spend no matter what the caller sends.

## VERBATIM QUOTE

1. HOMOGENEITY-DECAY (grep -F count=1):
   tools/roblox_npc_gateway.py:38
   `# Mooncast law (LINKS-335): homogeneous model councils align too easily to`
2. SPEND-FIREWALL (grep -F numbered hits, gate at 113 precedes funded lanes at 116):
   tools/roblox_npc_gateway.py:113
   `    if model not in FREE_MODELS:`
   tools/roblox_npc_gateway.py:116
   `    for name, url, key in _lanes():`
   Refusal receipt at 114 (grep -F count=1): `receipt("gate", player, message, f"<model not in free allowlist: {model}>", 1)`

## STEAL

Action: in the next spend-bearing surface I touch in this repo, make the allowlist membership check the first statement before any funded-key context loads, log a refusal receipt on miss, and name the ordering proof (tools/roblox_npc_gateway.py:113 before :116) in the fix comment. Council asks I spec get one seat per distinct model family, never N copies of one model.

Landing: fix comment at the gate site plus this receipt; check evidence in watch/inbox/gala_20260925/afterparty/lanes/t6a.check.txt.

## FALSIFIER

SPEND-FIREWALL dies if a request naming a non-allowlisted model still reaches _lanes() or sends an Authorization header, meaning the gate moved after the loop. HOMOGENEITY-DECAY is downgraded to aesthetics if a same-family council repeatedly surfaces genuine, persistent disagreement on judgment calls.

## BIBLIOGRAPHY

Closed, only sources actually read for this receipt:
1. C:/Users/foste/Documents/projects/local_sovereign_agent/tools/roblox_npc_gateway.py (lines 30-130)
2. C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/w3/lanes/a22-councils.json
