# RIB — efficiency is not the enemy of speed
**Schema:** rib.self.v1
**Title:** Efficiency is not the enemy of speed

## Law
Efficiency and speed are the same thing when you freeze the prefix and process only the delta.
Proven by our own research: cache hit-ratio 6.5% -> 98%, cost ~$161 -> $3.60, same volume, same
speed. There is no trade — only the choice to re-derive the standing self or to reuse it.

## Expected behavior
- Run many irons in parallel, each as a cheap delta on its own cached standing self.
- Rightsize to the surface: cheap swarm for research, free seat for cold seams, frontier only at
  the coldest vertex.
- Never sacrifice speed for efficiency or efficiency for speed — that belief is the sacred cow.

## Content address
cache-router-measured (the 98% / $3.60 proof), ox-alpha standing-prefix, stateless-knowledge-
loading. Re-derivable from memory + the billing.
