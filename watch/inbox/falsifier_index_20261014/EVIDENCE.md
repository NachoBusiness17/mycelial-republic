# EVIDENCE - the chain's own receipts, linked (2026-10-14)

Master under test: SettlementMaster v7 `EQCteLhGv7dCLtCtbSK8bs5mxikKF-ckZ11vvf-5WUjpjrLb`
(testnet), deployed from PR #1 head 185b3d8. Every record below is verifiable
on the public testnet explorer.

## THE BOUNCE RECORD (theses 48, 87; index entries 48, 87) - CORRECTED COUNT

Five bounces with exit code 24976 ("Master balance below band floor"), not
four as the soak receipt first recorded: the chain's transaction list shows
the client poll missed one. **The fourth "TIMEOUT" of the soak ledger was
itself a wild band bounce** - the settle landed, the band bounced it, the
worker wallet never moved, and the driver's poll called it absence. The
correction is dated 2026-10-14 and is itself entry-level evidence: the
chain's exit codes outrank the client's absence-of-evidence.

| # | lt | taskId | exit | tx |
|---|---|---|---|---|
| 1 | 102950108000003 | 53001310597 | 24976 | https://testnet.tonviewer.com/transaction/ae48654b8e7390072bdbc5ad8700258e03dd235426333fe33f1ef15708f1ae02 |
| 2 | 102951002000003 | 53001667961 | 24976 | https://testnet.tonviewer.com/transaction/2cbbebab6790c5252ff9a2242e250679ef5af0907e1d736b0db23e58d3ff5d97 |
| 3 | 102951894000003 | 53001024865 | 24976 | https://testnet.tonviewer.com/transaction/9928dae3818d61df916a413d9ea97eaac1195ac50fd547f13366baeece99455f |
| 4 | 102954671000003 | 53001133109 | 24976 | https://testnet.tonviewer.com/transaction/767b2318834364fb2ff1ec3c72e8efb39fbb33888551f5c14191547b869a592a |
| 5 | 102955789000003 | 53001580342 | 24976 | https://testnet.tonviewer.com/transaction/834aa422202bc2c67b8d844a431bb889268efa5faba0ef4080ac5dc8d36cb28c |

Rows 1-4 are wild bounces from the soak (the band invariant firing on
congestion-era settles); row 5 is the deliberate probe (the floor was raised
through the DAO setter, one settle fired, the bounce read, the floor
restored). All five: state clean, taskCount untouched, revert held.

## THE SETTLE RECORD (theses 47, 48, 88; index entries 47, 88)

Thirty settles cleared clean the same window. First:
`50d3818bd6724bf9bfe43eb57c9b072b80bacfd3fc821ccec6aa58cd51444e3d`
(lt 102945029000003, taskId 53001282225,
https://testnet.tonviewer.com/transaction/50d3818bd6724bf9bfe43eb57c9b072b80bacfd3fc821ccec6aa58cd51444e3d).
Last:
`c11652729b2b66b19d7a31fc5baa78424f502a8fbf3d03c5c7ecee6ce8504599`
(lt 102949802000003, taskId 53001188758,
https://testnet.tonviewer.com/transaction/c11652729b2b66b19d7a31fc5baa78424f502a8fbf3d03c5c7ecee6ce8504599).
The complete machine-readable record - all five bounces, all thirty settles, hashes and explorer links - is `evidence/chain_records.json`, pulled from the public chain 2026-10-14. Pool drawdown across
the window: 100,000 -> 99,250 GSTD, exactly 25 x 30 (byte-checked against
the on-chain jetton wallet).

## THE REHEARSAL RECORD (thesis 47)

`evidence/soak_cycles.jsonl` (35 rows) and `evidence/soak_summary_v1.json`
are the soak ledger as the driver banked it, preserved uncorrected; the
bounce-count correction above rides THIS file, not the original. The
rehearsal-never-settles proof (the dry gate, post-fix, zero on-chain
movement) is receipted in the harness record of 2026-10-13.

## THE COUNCIL RECORD (theses 28, 40, 44, 68)

The five-model council's certification runs, as banked:
- `evidence/council/run_20261014T120012Z.json`: run_id
  consensus-20261014T120012Z, verdict STRUCTURE, consensus 0.8462, correct
  0.6923, models: gemma:2b, deepseek-r1:1.5b, qwen2.5:3b-instruct,
  gemma2:2b-instruct-q5_K_M, qwen-desk:latest.
- `evidence/council/run_20261013T215230Z.json` and
  `evidence/council/run_20261013T102847Z.json`: the cadence receipt (the
  council runs daily without anyone awake - thesis 69's concrete).
The dispute-vs-agree value split (+6.1 / +0.6, thesis 44) rides the harness
logs; the raw dispute-set run is the remaining owed link.

## THE AUDIT PROTOCOL (theses 61, 63)

`AUDIT_PROTOCOL.md` beside this file: how to enumerate the permission path
for each of the four possessions (keys, memory, weights, settlement) and
where a single permission anywhere kills the node claim. Publish a vendor's
completed audit and their "decentralized" marketing is checkable line by
line.
