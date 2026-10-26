# H247_STUDYB_COVERAGE_RECEIPT_DESIGN (nvidia/nemotron-3-super-120b-a12b:free, turn 1, channel: content)

# COVERAGE RECEIPT v0 DESIGN SPEC

## 1. Exact receipt schema  
- Fields: `cert_id` (uint64), `checks_run` (uint32), `checks_checkable` (uint32), `gap_mask` (bytes32), `hash_anchor` (bytes32)  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  
- `hash_anchor` = keccak256(abi.encodePacked(prev_receipt_hash, block.timestamp, msg.sender))  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  
- Attaches to the existing soak cycle as a log emitted after each verification step, before the PR #1 bonus-deferred event is settled  # SPECULATIVE (watch/inbox/outerweb_research_20261013/GAP_ANALYSIS.md:UNVERIFIED)  
- The PR #1 bonus-deferred event consumes the receipt to adjust the bonus payout proportional to `checks_checkable - checks_run`  # SPECULATIVE (watch/inbox/outerweb_research_20261013/GAP_ANALYSIS.md:UNVERIFIED)  

## 2. Resolver and challenger separation  
- Resolver executes in context A, challenger in context B; contexts are isolated by separate memory stacks and distinct gas metering  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  
- Merging the contexts incurs a fixed 0.8-point penalty applied to the certification score for that cycle  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  
- The penalty is deducted from the resolver’s reputation before the challenger’s rebuttal is evaluated  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  

## 3. Exposure counter  
- `gaps_exposed_per_10` = (number of certifications where `gap_mask` != 0) / 10, rounded down  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  
- The counter increments a banked value `exposure_bank` by `gaps_exposed_per_10` at the end of each soak cycle  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  
- `exposure_bank` is readable by the governance contract and can be spent to reduce future merge penalties  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  

## 4. Falsifier (explicit if‑then)  
- IF 40 consecutive certifications are observed with `gap_mask` == 0 (zero exposed gaps)  
- THEN the moat correction is deemed overcorrected; the contract triggers a bank‑and‑relax action:  
   * `exposure_bank` is halved and added to the resolver’s reputation pool  
   * The 0.8‑point merge penalty is temporarily reduced to 0.4 points for the next 10 cycles  # SPECULATIVE (watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT.md:UNVERIFIED)  

## 5. Smallest first version that could ship this week  
- Add the `CoverageReceipt` struct with the five fields listed in section 1  # SPECULATIVE  
- Emit a `CoverageReceipt` log in the verifier’s `verify()` function after computing `checks_run` and `checks_checkable`  # SPECULATIVE  
- Hook the PR #1 bonus‑deferred event to read the latest `CoverageReceipt` and adjust the bonus amount  # SPECULATIVE  
- Implement resolver/challenger context separation with separate call stacks and apply the 0.8‑point merge penalty on any cross‑context call  # SPECULATIVE  
- Implement the exposure counter logic and bank update in the soak‑cycle finalizer  # SPECULATIVE  
- Add the falsifier check as a view function that governance can call to trigger the bank‑and‑relax action  # SPECULATIVE  
- No changes to core consensus; all new logic resides in the existing verification contract  # SPECULATIVE  
- Test plan: unit test for schema encoding, integration test for emission soak cycle, property test for falsifier threshold  # SPECULATIVE  

---  
*All speculative rows are marked SPECULATIVE. Citations that cannot be resolved to quoted bytes are marked UNVERIFIED per the evidence‑trust rule.*
