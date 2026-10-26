# Convergence / divergence matrix (normalized by executor; lanes' own confidence tags kept per cell)
Lanes: L1 Fostertron MAX (opencode zai-sd/glm-5.3) | L2s substitute for Nacho Corp LITE: ZAI_API_KEY_Pro direct glm-5.3 | L3 agy bob claude-sonnet-5-5-medium | L4 agy PC (default model, unreported) | L5 opencode/mimo-v2.6-flash-free | L6 ollama gemma4:latest
Cell codes: C=lane marked confident, L=likely/strong inference, G=guess, -=absent, X=dissent

## Convergence set
| # | Normalized rule | L1 | L2s | L3 | L4 | L5 | L6 | Count |
|---|---|---|---|---|---|---|---|---|
| A | Authority is what people act on (seal / who is obeyed), not announcement, posture, or occupying the doorway | C | C | C | C | C | C | 6/6 |
| B | When map and ground disagree, trust the ground | C | C | C | C | C | L | 6/6 |
| C | When lost: say so aloud, stop, wait; the admission is what brings help | C | C | C (literalness G) | C | C | C | 6/6 |
| D | Against force: don't fight; promise truthful total exposure (he steps aside) | C | C | C | C | C | C | 6/6 |
| E | Damage/traces testify: you can know what happened without reading the erased content | C | L | G | G | C | C | 6/6 (mixed tiers) |
| F | Erasing a record is theft regardless of intent ("only cleaned") | C | C | X (G: change != violation; owner's reasoning critiqued) | C | C | C | 5/6 + 1 dissent |
| G | Leave the wound unrepaired so readers ask what was there | C | C | C | C | C | - (only "evidence remains") | 5/6 |
| H | A perch/stool carries only its occupant, briefly; not a foundation; don't overreach from it | C/G | C | G | C | C | - | 5/6 |
| I | Retire the failed instrument (map) but keep it | C | C (why kept: G) | C (as reference) | G | C | - | 5/6 |
| J | Legitimate authority is conferred quietly; confirmed by service (bread, chair) not applause | C | L | G | G | C | - | 5/6 |
| K | Copy the record outward to an external/neutral holder (magistrate) | C | C | C | G | C | - | 5/6 |
| L | When the support fails, go to direct structure (hands on wall) | C | L | - (folded in H) | C | C | - | 4/6 |
| M | Individual failure != structural failure (shelf/books unmoved) | G | L | - | C | C (implicit) | - | 4/6 |
| N | Carry tools of record and access, not weapons (slate + keys) | C | C | - | G | G | - | 4/6 |

## Few-lane / unique
| Rule | Lanes |
|---|---|
| Destruction will be described as maintenance ("cleaning" as laundering verb) | L2s C, L4 C(embedded) — 2/6 |
| To find who rules, watch whom the executors look to | L1 C, L2s C — 2/6 |
| Wet pen dates the act / actor nearby | L1 G, L5 G — 2/6 |
| Pre-position records before the catastrophe (mother hid it before the flood) | L2s G, L5 G — 2/6 |
| Self-announced claim needs only noncompliance, not refutation | L5 C — 1/6 |
| Lose the object, never lose the account | L2s C — 1/6 |
| The house is sensor and court; act as if witnessed | L2s L — 1/6 |
| Seal goes to the one who proved uncoercible (causal link) | L2s L — 1/6 |
| Absence is never neutral (master rule) | L2s C — 1/6 |
| Records survive by duplication; archivist copying / Miriam copying symmetry | L2s L — 1/6 |
| Search among the remains of failed destruction (fire burned to ash) | L5 G — 1/6 |
| The struck name is withheld by design; trust the form, not the content | L5 G — 1/6 |
| Retreat to last verified ground (hollow boards) | L1 C — 1/6 (others fold into B) |
| Truth cannot be erased/contained by authority | L6 C — 1/6 |
| Truth found through a breach in the expected structure; predetermined paths dead-end | L6 L — 1/6 |
| The slate is never used (open question) | L2s (flag), L4 (flag) — 2/6 |
| Accuse only after establishing what was taken and by whom | L3 G — 1/6 |

## Interpretive disagreements
1. Clerk scene: 5 lanes read erasure-is-theft as the story's verdict; L3 reads it as unresolved and possibly a critique of the owner, and flags tension with rule G (blank space = question, not verdict).
2. Stool scene meaning splits five ways: overreach (L1, L2s), posture change (L5), scaffolding vs core (L4), "occupying != bearing weight" (L2s), only-implied (L3 guess); L6 drops the scene.
3. Map: most say empirical verification (knock on boards); L6 says trust *feeling* and that linear guides fail generally. Why keep the map: archive/evidence (L4), reference not guide (L3), unknown (L2s).
4. Lost-in-dark causality: L1/L2s/L4/L5/L6 take "a house hears" as operative; L3 marks literal causality as a guess.
5. Exposure scene: L3 alone qualifies it (truthful, not a bluff; may not generalize).
6. Calibration: L6 tags zero guesses; L3 tags the most; L2s uses a 3-tier scale.

## Blindness caveat
L1 and L5 (opencode agents) listed their working dir; L1 saw other lanes' file NAMES (not contents) and speculated it was a probe; L5 read runner.py (no lane outputs). L3/L4 (agy) were in plan mode; L3 began "No code or file changes are involved". L2s and L6 were raw single calls. No lane saw another lane's output.
