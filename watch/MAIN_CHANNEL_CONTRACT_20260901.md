# Main channel contract

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: the main channel is a bounded notepad ingress (watch/main_window.md → mag.main_channel) with closed roles and hard bounds; proposals are never permissions — SUPPORTED (mag/main_channel.py and watch/main_window.md both exist on disk) · falsifier: self-test failing, or an intake batch exceeding the stated bounds (4 entries, 2 jobs, 1 child level) without denial

The main channel is a notepad-shaped ingress, not a giant conversational transcript.

```text
watch/main_window.md
  -> durable byte cursor
  -> map-first WARM_PACK.json
  -> BabelFish deterministic envelope
  -> Calcifer/local 7B closed-enum advisory (optional)
  -> Elder evidence snapshot + Ractor Congress review slots
  -> bounded gopher proposal
  -> mag.orchestrator queue
  -> existing switchboard/effect boundary
  -> receipt in memory/runs/main_channel/
```

## Closed roles

| Alias | Actual role | Authority |
|---|---|---|
| Calcifer | local 7B route/scout | none; advisory JSON only |
| BabelFish | text-to-envelope normalizer | none |
| Elder | `mag.elder.audit()` registry/evidence audit | evidence veto; no grant |
| Ractor Congress | independent review slots | dissent only; staged unless explicitly run |
| Gopher | one queue item | no child spawning; depth ≤ 1 |

## Hard bounds

- Four entries per intake batch.
- Two `main-window-*` jobs in flight.
- One child level only; children are explicit, never inferred from prose.
- Five closed channels: research, code, audit, draft, observe, plus hold.
- Local 7B can classify; it cannot authorize, write the board, spend, or launch.
- A queue entry is not completion. Completion requires the existing worker result and evidence receipt.
- The warm pack is a map of paths, hashes, and short heads. Agents dereference territory on demand.

## Operator use

```text
append text to watch/main_window.md
python -m mag.main_channel run
python -m mag.main_channel run --7b --dispatch
python -m mag.main_channel status
python -m mag.main_channel self-test
```

The first command only creates proposals. `--dispatch` may queue bounded local gophers; the normal
orchestrator/drainer remains the execution owner. The board, model chatter, and a review opinion
may produce a proposal, but none of them is permission.

