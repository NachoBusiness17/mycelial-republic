# swarm1-deepseek-tools__saturation_fourcond (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: judge_alignment writes no usage receipt and its judged rows store only raw text, so the case-law arm cannot be priced or audited | EVIDENCE: tools/saturation_fourcond.py:238 | FIX: store a["usage"] in vec_rows rows alongside "alignment" so cost() can be recomputed from bytes.
DEFECT 2: blind_order labels A..T are assigned by condition-order index, not by shuffled position, so cond/tier are inferable from label parity and tier stride | EVIDENCE: tools/saturation_fourcond.py:212 | FIX: after computing order, assign labels to shuffled position: labels = {idx: chr(65+run_i)} keyed on the shuffled index, not the cell index.
DEFECT 3: pack truncates corpus by chars with no per-file boundary guard, so cut[:cut.rfind("\n\n")] can silently return "" when the first paragraph block exceeds target and drop the entire corpus stream | EVIDENCE: tools/saturation_fourcond.py:129 | FIX: if cut.rfind("\n\n") <= 0, fall back to cut (do not collapse to empty).
DEAD-CODE: labels = {i: chr(ord("A") + i) for i in range(len(cells))} indexing is unused by anything but the print path since rows carry cond/q/tier independently | EVIDENCE: tools/saturation_fourcond.py:213
ONE-SITTING FIX: key judge labels to shuffled run position so blind relabeling is actually blind and the receipt's labels map is not a decodable index | EVIDENCE: tools/saturation_fourcond.py:212

Falsifier for ONE-SITTING FIX: run the script with two cells swapped in TIERS order and check that labels A..T no longer map to the same (cond, q, tier) triple; if they do, the relabel is cosmetic.
