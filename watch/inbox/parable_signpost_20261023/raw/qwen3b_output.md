1. The rules on the rule card, one line each, are as follows:
   - pd1:L01: The record outlives the person.
   - pd1:L02: Deletion is theft.
   - pd1:L03: The blank space must stay askable.
   - pd1:L04: Authority comes from function, not claim.
   - pd1:L05: Trust the floor, not the map.
   - pd1:L06: In the dark, say you do not know.
   - pd1:L07: Traces mean someone came before.
   - pd1:L08: Copy is transport, not mutation.
   - pd1:L09: Transparency is the defense.
   - pd1:L10: Function without ceremony.
   - pd1:FP: False premises.

2. If the gate looked at a reader's answer to "Why not rewrite the torn page?" and said HOLD, the pointer ID(s) that should be fetched are pd1:L03. The tool or command to fetch the pointer is `signpost_lookup.py pd1:L03`.

3. If the gate had said PASS instead of HOLD, you should not fetch anything. The reason is that the gate's PASS indicates that the rule card is sufficient, and no additional pointers need to be fetched.

4. After fetching, if you are still unsure, you should ask Nacho. This is because the gate's instruction is to ask Nacho if you are still unsure after fetching the pointer.