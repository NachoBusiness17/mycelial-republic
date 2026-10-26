# GB PERIMETER: build-to-spec (2026-10-10, operator order "ship what he asked")

GB's ask, verbatim (operator relay):
1. "There is currently a need for a couple of mini PCs for testing within a closed
   perimeter, a ton for smart contracts, and gas payments for test transactions and
   verification that the network will pay rewards to participants."
2. "Nodes must confirm the ability of different models to generate a consensus answer."
3. "As a result, the network should learn on its own as it grows."

Operator constraints (same order): build it NOW to spec; leave it open for our future
plans; the laptop is Windows 10 and needs security tuning, same for the whole mesh;
dogfood our systems along the way; COLDEST VERTEX COMPATIBLE (the weakest participant,
a Windows 10 laptop with no GPU, must be a full member - the tide-on-shit-boxes law).

## Deliverable map (ask -> what ships)

| GB ask | What ships tonight | Extension point (ours, never required) |
|---|---|---|
| closed perimeter, couple of boxes | the two boxes exist in-house: DESKTOP-7C70KSC (docker gstd-node live, Ollama 15-model pool) + the Windows 10 laptop (joins as dispatcher/judge node, CPU-only, stdlib-only harness) | vast.ai elastic core + guild blades when scale demands |
| TON smart contracts | the 10-09 tokenomics audit delivers (mint gates, caps, settlement authority, the genesis-seal gap + settlement-theater finding) | review lane per contract on his word |
| gas for test transactions | testnet-first plan (TON testnet, free); mainnet float a few TON, dedicated wallet, keys never ours | - |
| verify the network pays rewards | A1 assertion stub lands in the harness (payout_delta null until GB's staging endpoint); the kill-test + live census receipts stand as the current evidence | A1 goes live the day the endpoint lands |
| different models -> consensus | tools/consensus_harness.py: K heterogeneous local models, closed-form task bank from estate bytes, modal-answer consensus, per-model agreement matrix | heterogeneous nodes across machines when the perimeter widens |
| network learns as it grows | consensus_ledger.jsonl rows per model per shape (GPS-importable schema): the learning instrument is the accumulating ledger | GPS capability-ledger import + seed-rib boot = the singing-network toggles |

## Coldest vertex law (the compatibility bar)

The harness is stdlib-only Python, no docker requirement, CPU-class, runs on the Windows
10 laptop against a remote OLLAMA_HOST (or a tiny local model). If the weakest box
cannot dispatch, judge, and file, the perimeter is not done. The laptop's job class:
dispatcher + judge + receipt filer (CPU-light); model hosting rides the desktop now and
the guild benches later.

## Security tuning (laptop + mesh, the W10 baseline)

SECURITY_BASELINE_W10.md in this folder: defender exclusions scoped (repo + docker
data only, never system-wide), firewall inbound limited to the tailnet interface,
RDP off, auto-login off, guest off, BitLocker on, .env never leaves the machine
(the key law), scheduled-task audit (the two-registry sweep law: no orphan crons).

## What is deliberately NOT shipped tonight (honest)

- No mainnet transactions (gas wallet is GB's/his call; keys never held here).
- No platform-side payout assertion (needs GB's staging endpoint; A1 stub ready).
- No vast.ai spend (elastic core waits for the staging door; the $0 phase proves A2).
