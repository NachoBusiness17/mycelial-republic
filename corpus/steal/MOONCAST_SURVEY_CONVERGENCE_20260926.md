# MOONCAST SURVEY CONVERGENCE (steal receipt, gopher t22, 2026-09-26)

Covers the two a22 laws left uncovered after MOONCAST_SPEND_FIREWALL_20260926.md took HOMOGENEITY-DECAY and SPEND-FIREWALL: MOONCAST-AS-SURVEY-PATTERN and CONVERGENCE-AS-LOOT. Sources read: roblox/src/server/MudBasecamp.luau and watch/inbox/gala_20260925/w3/lanes/a22-councils.json. All quotes byte-verified with grep -F, evidence in watch/inbox/gala_20260925/afterparty/lanes/t22.check.txt.

## LAW

1. MOONCAST-AS-SURVEY-PATTERN: an external law lands in the default running config; the survey witness list is pinned inside the server code that runs, with the law named in a comment at the point of use.
2. CONVERGENCE-AS-LOOT: council agreement is a game mechanic; >=2 witnesses agreeing folds to CORE = loot, divergence is kept as a swarm log.

## CLAIM

MudBasecamp.survey does not cite the Mooncast law from a doc, it compiles the law into the running game. WITNESS_MODELS is a literal table in the server script: three seats, three different families (stealth + inclusionai + poolside), all free slugs, so cross-family heterogeneity is what the survey runs by default, not an opt-in. The mechanic pays both outcomes: content words shared by >=2 witnesses fold to CORE and increment Invariants; zero overlap routes the split verdict to the swarm as a retained ShadowLedger row, so a divided council discards nothing.

## VERBATIM QUOTE

1. MOONCAST-AS-SURVEY-PATTERN (grep -F count=1 each, roblox/src/server/MudBasecamp.luau):
   `-- Mooncast law (LINKS-335): same-model councils agree too cheaply. The three`
   `-- witnesses run on THREE DIFFERENT families (stealth + inclusionai + poolside),`
   `-- all $0, so ROSHOMON CORE (>=2 agree) measures convergence, not consistency.`
   `local WITNESS_MODELS = {`
   `"inclusionai/ling-3.0-flash-sante:free",`
2. CONVERGENCE-AS-LOOT (grep -F count=1 each, same file):
   `-- survey: the party witnesses the same scene; converge = core, diverge = swarm log`
   `if n >= 2 then table.insert(core, word) end`
   `novel-divergence in %s routed to swarm`

## STEAL

Action: when adopting an external design law, edit the default witness/seat list in the code that runs and name the law in a comment at the point of use; and design councils so both outcomes pay, consensus produces the artifact while dissensus produces a retained log entry. Landing: this receipt; check evidence in watch/inbox/gala_20260925/afterparty/lanes/t22.check.txt.

## FALSIFIER

MOONCAST-AS-SURVEY-PATTERN dies if survey witnesses revert to one family or a paid slug while the gate still passes. CONVERGENCE-AS-LOOT dies if CORE loot or swarm logging fires regardless of actual witness reply overlap, mechanic decoupled from the votes.

## BIBLIOGRAPHY

Closed, only sources actually read for this receipt:
1. C:/Users/foste/Documents/projects/local_sovereign_agent/roblox/src/server/MudBasecamp.luau (lines 1-10, 225-280)
2. C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/w3/lanes/a22-councils.json
3. C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/steal/MOONCAST_SPEND_FIREWALL_20260926.md
