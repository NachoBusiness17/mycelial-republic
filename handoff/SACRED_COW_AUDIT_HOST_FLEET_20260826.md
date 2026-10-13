# SACRED-COW AUDIT — host-fleet burners (2026-08-26)

Operator: "almost all of that is legacy shit... the best ideas we had at the time that have good
bones and should be stolen extensively from and interpreted in new understanding. We call those
sacred cows."

Doctrine applied (bones-not-sacred-cows, 2026-08-15): the accumulated desktop-era daemons are ONE
DRAFT of the night-shift/desktop sovereign. NOT sacred institutions to preserve. The bones inside
them are what inspired the container era. Sacred = only the explicitly stated invariants. The right
frame: write the NEXT DRAFT from the bones, free to be cleaner than the draft.

CPU burners (from the other seat's process diagnosis, 1:53 AM fleet restart, host-side):
  main.py lab              3.5 CPU-hrs   lab loop, polling
  main.py autorun          2.5 CPU-hrs   the supervisor/respawner
  mag.ghost --daemon x2    1.4 + 0.6     two ghost daemons fighting over port 9000
  synthesis_agent.py       0.5 CPU-hrs   synthesis loop
  main.py dashboard        0.3 CPU-hrs   host dashboard shadowing container 8765

## THE AUDIT — bone in each, reinterpretation, verdict

| daemon | the BONE (the good idea) | container-era reinterpretation | verdict |
|---|---|---|---|
| main.py lab | tight cadence loop — stateless work on short cycles, rightsized not conservative | mag_launch is the canonical controller; the container runs the lab loop inside the sovereign | STEAL the cadence-rightsize bone (already folded) → RETIRE host loop |
| main.py autorun | SELF-HEALING — "keeps the family alive," respawns fallen services | the real invariant. Now owned by docker restart policies + mag_launch respawn | KEEP the invariant → RETIRE the host supervisor (container owns respawn) |
| mag.ghost --daemon x2 | the ghost daemon surface — a resident worker for a stateless seat | the container's sovereign service is the next draft of the same surface; two instances = host+container collision on 9000 | KEEP one (container's) → RETIRE host ghosts |
| synthesis_agent.py | synthesis loop — folding outputs into understanding | percolator / refine_chain in the container do this now | STEAL the pattern (already folded) → RETIRE host loop |
| main.py dashboard | the dashboard SURFACE — the operator's window | container dashboard at 8765 is the same surface, newer draft | KEEP the surface → RETIRE host daemon, container serves |

## THE PATTERN
Every burner contains a real invariant that ALREADY has a container-era next draft (cadence loop,
self-healing, daemon surface, synthesis, dashboard surface). The host processes are the drafts we
built in the desktop era; the container sovereign is the rewrite. Nothing good dies in the transfer
IF we capture the bones first — most are already folded, which is why the retirement is safe.

So the surgery is NOT "kill the legacy." It is: verify each bone has a live container counterpart
(this audit), THEN retire the host drafts. Keep the invariants, cut the drafts. Reversible, known
relaunch commands, half the CPU back.

## GO/NO-GO
Sequence (steal-first): 1) confirm each bone's container counterpart is live (done above at the
surface level — verify at the bytes), 2) stop autorun first (kills the respawn), 3) retire the rest,
4) verify container 8765 answers, 5) one compose restart only if the shadow needs clearing.
