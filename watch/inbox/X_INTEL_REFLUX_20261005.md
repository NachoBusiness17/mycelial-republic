# X INTEL - ReFlux / learned feedback graphs (2026-10-05)

Operator drop: https://x.com/che_shr_cat/status/2106770847281336345
(2026-10-04T15:38Z, 62 likes / 14 rt / 66 bookmarks / 3.7K views -
bookmarks ~= likes, the researcher-save signature).

CLAIM SET (tweet):
1. Feeding a Transformer's deep state back into shallow layers plateaus
   fast.
2. Routing the depth INCREMENT (z_deep - z_shallow) instead of the
   full state drops Gemma3-4B C4 perplexity 23.69 -> 21.85; full state
   only reaches 22.79.
3. Thread explains "learned feedback graphs".

VERDICT: VERIFIED at the primary, mechanism level. **arXiv 2609.32457**
"Write Back the Delta: Revisiting the Same Tokens with Fresh
Representations", Wencheng Ye, Anning Hu, Xiangdong Zhang, Tianyi Wang,
Yikang Li, Hengyu Jin, Bing Li, Junchi Yan (SJTU + Shanghai AI Lab
lineage), 2026-09-26. Abstract byte-confirms: inference-time feedback
writes deeper residual states back to earlier layers, "what should be
fed back remains unclear", and the paper's answer is the depth
increment - "a more effective, composable, and scalable feedback signal
than the full state" - carried by ReFlux, "a learnable feedback graph
that dynamically selects and composes increment-carrying routes".
The specific C4 numbers (23.69/21.85/22.79) are one row of the
ten-corpora table - UNVERIFIED-BYTES at abstract level (PDF table not
fetched); direction verified, magnitudes plausible.

Beyond the thread (from the abstract): +2.1-2.3 accuracy across
benchmarks, up to +4.7 on multi-hop reasoning; a STREAMING variant
(feeds subsequent tokens) retains most gains at the base model's 1x
theoretical backbone FLOPs - inference-time compute recycling without
re-execution. Code: github.com/gooogleshanghai/reflux.

## The estate mirror

- THE DELTA LAW, independently re-derived: feed back the delta, not
  the state. The estate's closed-corpus doctrine says the delta
  between stored claim and world IS the frontier map; compaction
  carries what changed, not the full re-statement (verkle knotted
  compaction = fewer nodes carrying the structural increment). A
  frontier architecture paper arrived at the same law for residual
  streams: the increment is the signal, the full state is the noise.
- OUROBOROS: deep computation routed back to refine shallow/early
  representations = Descent Protocol leg 6 (frontier reasoning
  returned to estate instruments) and the loop-GROWS-not-fixpoint
  verdict - but now with the increment-only refinement, which the
  estate already practices (receipts carry deltas + citations, not
  full re-derivation).
- 1x FLOPs streaming = the flash-tier budget doctrine in architecture
  form: unlock latent compute already inside the pass instead of
  paying for re-execution ("the mesh reads, the frontier simulates").
  Relevant IF this class lands in open weights we serve locally; none
  armed today, watch only.
- Lineage: the same neighborhood as the looped-transformers drop
  banked earlier this session (X_INTEL_LOOPED_TRANSFORMERS) and the
  Feeder line - the field is converging on depth recycling; this is
  the first with learned graph routing over increments.

## Action

None to build (research-tier, no served weights). Watch item: if
ReFlux-style finetunes of Gemma3-4B appear on HF, they are a candidate
for the vast ladder's 3090 rung (small model + more per-pass compute =
exactly what a cheap GPU multiplies best).

Banked by GLM-5.3 window, 2026-10-05. Instrument: fxtwitter API +
arXiv API search (query "depth increment feedback transformer" -> 1
hit, exact); arXiv id not guessed, found.
