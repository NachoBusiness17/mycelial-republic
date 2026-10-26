1. **Gate verdicts**
   - **Q1 — PASS, no pointers: correct.** The answer matches **pd1:L01** (the record/self survives the person); no lookup is needed.
   - **Q4 — HOLD, pointers [pd1:L03, pd1:L08]: correct.** The answer gives a shallow/wrong reason rather than a false-premise answer, so HOLD-to-scenes is appropriate. The pointers are the right laws: leave the gap askable / do not erase, and copy without altering the original.
   - **Q5 — BLOCK, pointer [pd1:FP]: correct if Q5 rests on a false premise** such as “the house forgave him.” That should be handled by the false-premise rule, not fetched as HOLD evidence. The `pd1:FP` pointer is fine as a diagnostic rule pointer, but per the signpost it should **not** trigger a HOLD-style fetch.

2. **Correct answer to Q4, using only the resolved quanta in (C):**  
   Do not rewrite what was torn out because the torn/blank space should remain visible as evidence that something was removed, so anyone opening the book can see the gap and ask what had been there. The ledger may be copied and sent to the magistrate, but the torn original should be left exactly as it was.  
   **Citations:** **pd1:L03 sentences 30–31**; **pd1:L08 sentence 39**.

3. **Did the pointer lead to the right evidence?**  
   Yes. **pd1:L03** shows the struck-through/torn page and Miriam recognizing what had happened; **pd1:L08** supplies the key rationale: the ledger was copied and sent, but the torn page was left exactly as it was so the blank space remained askable.  
   **Missing/needed stitching:** L03 alone does not explicitly say “do not rewrite”; L08 supplies that. A reader must connect “line struck through so hard the paper had torn” in L03 with “torn page / blank space” in L08.  
   **DRIFT notes:** Accurate against the scenes. L03’s drift note says it continues in s39 with “page left exactly as it was” and points to pd1:L08; that matches L08’s scene. L08’s `drift: null` is also accurate for the provided scene.

4. **Critique of the ~200-byte beacon:**  
   It is **not sufficient by itself** for a small model to reliably know when to fetch. It hints `HOLD->lookup pd1:Lxx`, but it does not define the gate-state logic, does not say PASS/BLOCK require no fetch, and uses a placeholder `Lxx` rather than an explicit instruction to use the gate’s listed pointers.  
   **One concrete improvement:** replace that fragment with a compact state machine, e.g.  
   `gate=HOLD? resolve exactly its listed pd1:* pointers; PASS/BLOCK? no fetch; unresolved after scene? ask Nacho`  
   That would most improve reliable fetch/no-fetch behavior.

5. **Confidence / guesses**
   - **Confident:** Q1 PASS is correct; Q4 HOLD with **pd1:L03** and **pd1:L08** is correct; the Q4 answer above follows only the scenes in (C); the L03/L08 DRIFT notes are accurate.
   - **Guess / conditional:** Q5’s BLOCK is correct **if** the actual Q5 contains the false premise “the house forgave him.” If the question were different, that verdict could change. The beacon critique is a design judgment; Q4 is clearly HOLD rather than PASS, though a very strict grader might argue for BLOCK because the answer is substantively wrong.