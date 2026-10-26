# Receipt: innkeeper mate, 2026-10-16, cycle 9 of the seed thread (CLOSED)

Pack: logs/mates/missions/mission_20261016_04_innkeeper.md (claimed via .claim sidecar;
sidecar was born 0 bytes 8:12:09 AM, claim line hand-written 12:25:01Z, pid 21388).
Mate: THE INNKEEPER. Persona honored: warm, plain-spoken, allergic to jargon; the
stranger's next stumble should find a sign where the stumble happens.
Seed thread: Adam's day one on the-mountain after commit 035a5e3, walked AS HIM, cold,
no estate knowledge.
Resume chain: receipt_20261006 -> 09 -> 10 (mountain cold walk CLOSED) -> 11 (mag.cmd
help wall CLOSED) -> 12 (human stranger's doors CLOSED) -> 13 (STUB, died early) -> 14
(broken door + recovery-path thread NAMED, CLOSED) -> 15 (opening stub, stopped
mid-road before the walk) -> this receipt. This cycle resumed the 10-15 stub and rode
the 10-14 named next thread: the stranger's recovery path.
Status: THREAD RIDDEN TO EXHAUSTION for this cycle. Stopped at exhaustion, not mid-road.
STEER honored: COMPUTE LADDER. Every step was local file reads, local git, local docker/
netstat/netsh reads, and loopback-only GETs. Zero paid dispatch, zero API keys, zero
env dumps, zero Task agents (single-seat local ride).

Search terms for the drop ledger: portproxy ghost 8765, all four publishes dropped,
docker port empty, TIME_WAIT burst 15539, ephemeral port exhaustion 49152 65535,
svchost iphlpsvc portproxy, knocked door cascade, recovery path paragraph, something
feels broken, HOW_TO_MAG_DASHBOARD three copies, CONTAINER troubleshooting pointer,
Adam day one, the-mountain porch gap 6 commits, stranger start stories.

## FINDINGS

1. THE GROUND SHIFTED AGAIN, AND WORSE: on the 2026-10-16T01:25:10Z container restart,
   mag-sovereign came up with ZERO published ports (docker port mag-sovereign: empty).
   Yesterday 3 of 4 publishes survived; today all four are host-dead (:8765, :8000,
   :8001, :9000). PortBindings still request all four as 127.0.0.1 binds (docker
   inspect), so the file's promise and the cage's reality disagree worse than ever.
   GET :8765/ times out, GET :8000/health and :8000/ refuse connection, GET :8766/
   times out (8766 is the raw TCP MCP bridge; its timeout is expected behavior).
2. THE GHOST IS STILL ON THE PORCH: netsh interface portproxy show all lists exactly
   one rule, 0.0.0.0:8765 -> 127.0.0.1:8765, held by svchost (pid 48136 at 12:26Z,
   iphlpsvc family). Box boot was 2026-10-08 8:27:24 PM local, so the 01:25:10Z
   restart was a container-level restart, not a reboot: the rule simply persists
   (portproxy rules live in the registry and survive reboots; the 10-05 cure deleted
   it and something re-created it before 10-14). With docker's bind now gone, the
   rule's connect target (127.0.0.1:8765) routes to the ghost's own listener: the
   door-forwarder now forwards the door to itself.
3. NEW MONSTER, BYTE-BACKED: a 12:26Z netstat instant captured 15,539 sockets in
   TIME_WAIT to 127.0.0.1:8765, local ports spanning 49152 through 65535: the ENTIRE
   default dynamic port range (16,384 ports; the pile was 94.8 percent of it). While
   piled, the box was at outbound-connect exhaustion risk box-wide. Raw capture
   preserved at watch/inbox/mates_leave_protocol/evidence_timewait_burst_20261016_
   netstat_capture.txt (15,555 lines with header, 1,150,760 bytes).
4. ATTRIBUTION OF THE BURST: OPEN, and the honest edges are named. The pile sat
   inside the mate-launch window (8 packs born 12:12:02Z, 7 sibling stubs filed
   12:22:09-12:28:08Z, capture 12:26Z), but no sibling receipt confesses a probe
   loop, and no live poller existed at 12:44Z (process scan of python/pwsh/powershell
   command lines: only my own session and an AMD utility). A self-cascade from my own
   first knock (12:25:37Z, 28 seconds before the capture) cannot be excluded for that
   knock, but the identical controlled knock at 12:39:30Z produced NO cascade (netstat
   12:41Z: one line, the listener only), so a knock-cascade is not the standing
   mechanism. A 40-sample sampler (15s apart, 13:01:13-13:13:18 local) read TW=0 and
   ES=0 in 40 of 40 samples: no recurrence in the 12-minute watch window. The pile
   drained completely by 12:38Z.
5. THE HEALTHCHECK STILL LIES AT THE VISITOR BOUNDARY: docker ps reports mag-sovereign
   "Up 11 hours (healthy)" while every host-facing door it promises is dead, because
   the healthcheck probes in-cage URLs (compose lines 108-120). Second consecutive
   cycle (10-14, 10-16) where "healthy" was false comfort exactly at the stranger's
   door. Compose's own B7 lesson (probe what the visitor touches) remains unlearned.
6. THE RECOVERY-PATH GAP IS NOW CLOSED IN THE DOCS (this cycle's build): the cure
   paragraph landed in docs/HOW_TO_MAG_DASHBOARD.md section 6 as a new subsection
   "The dashboard page at 127.0.0.1:8765 will not open." (22 lines: two read probes,
   two cure commands, one refresh step, pointer to the 10-05 receipt and the compose
   comment block). All three byte-identical copies synced (docs/, dashboard/static/
   docs/, dashboard-deploy/static/docs/; served copy is bind-mounted live into the
   cage via ./dashboard -> /app/dashboard, so it renders on refresh once the door is
   cured). A 3-line pointer landed in docs/CONTAINER.md Troubleshooting. Total
   working-tree delta: 4 files, +70 insertions, 0 deletions, uncommitted (no commit
   order given; left for operator review on a 679-entry busy tree).
7. THE CURE IS UNCHANGED AND UN-RUN: docker-compose.yml comment lines 41-59 plus
   watch/inbox/HEADED_WINDOWS_CURED_20261005.md hold the proven sequence (admin shell:
   delete the portproxy rule, then docker compose up -d mag, expect curl 200; proven
   2026-10-05 ~20:10 ET). Today's variant (all four publishes dropped) resolves with
   the same sequence since recreation re-requests the publishes the restart dropped.
8. GOOD INNKEEPING, CREDITED: the estate's session recorder is alive and loud
   (attention.md gained ~695 lines of session-record entries while this cycle worked);
   the in-cage mag_agent is filing narratives and dossiers. The house is lived-in even
   while its front door is stuck.
9. THE PORCH IS NOW 6 DAYS STALE: the-mountain HEAD c38ded67acb2..., origin/main
   bac2b89cc43..., gap 6 commits, unchanged across 4 receipted measurements (10-10,
   10-12, 10-14, this cycle). Adam's ONBOARDING.md and docs/ADAM_QUICKSTART.md still
   exist only at HEAD, not on the porch a real clone gets. The seed hash 035a5e3
   (full 035a5e3bc71fb8173dbb68808ee10b729793bb1d) re-verified as a commit in
   the-mountain (cat-file -t: commit); still absent from the harness repo (git log
   and cat-file both fail here), same as cycles 6 through 8 found.
10. WEATHER, NOT LANE: tortoise-db had restarted alone 22 minutes before the 12:26Z
    check (other 6 containers Up 11 hours). Recorded so the next seat does not read
    it as part of the door disease.

## JOURNEY (threads followed in order, dead ends named, why each turn)

1. Read the mission pack (48 lines), globbed the receipts shelf (64 receipts from
   prior days, 20261006 through 20261015), read my own two prior receipts in full
   (10-15 stub 16 lines, 10-14 closed cycle 66 lines). Why: resume-not-respawn means
   loading the lineage before touching anything; the 10-14 close named this cycle's
   thread and the 10-15 stub marked the road mid-step.
2. Filed the opening stub receipt and wrote my claim line into the 0-byte sidecar.
   Why: receipt before speech is pack law and the operator ordered it before anything
   else; the dispatcher again left the sidecar empty for me to claim.
3. Re-ran the standing door census (4 GETs) before building anything on 10-14's
   findings. Why: yesterday's premise (3 of 4 publishes alive) had to be re-verified
   on a box that restarts containers overnight. It failed differently: :8000 now
   refuses outright. Turn: the cycle became incident-observation first, doc-work
   second.
4. docker ps + docker port + docker inspect x3 (StartedAt, PortBindings, Mounts) and
   netstat + netsh. Why: an innkeeper does not report "door stuck" without naming
   what changed overnight. Found: all four publishes dropped at 01:25:10Z restart,
   ghost rule intact, svchost holds the wildcard.
5. Analyzed the 15,549-line netstat capture: 15,539 TIME_WAIT rows, local ports
   49152-65535. Why: a pile that big is a box-wide risk and needed its shape measured
   before its cause was chased.
6. Attribution hunt, four probes in order: (a) PID of the listener (48136 = svchost)
   and box boot time (Oct 8: rules out reboot-triggered pile); (b) rate measure t0
   and t0+10s (both 0: the pile had already drained; turns out it drained between
   12:26 and 12:38); (c) controlled re-knock at 12:39:30Z then immediate netstat
   (no cascade: kills the "every knock detonates" hypothesis); (d) live poller scan
   of process command lines (none) plus all 7 sibling stubs read for confessions
   (none). Dead ends named: my-knock-cascade (disproved for knock 2, cannot be
   excluded for knock 1 since the capture postdates it by 28s), continuous-poller
   (disproved), sibling-loop (no evidence). Attribution left OPEN with evidence
   preserved, per no-fabrication.
7. Read watch/inbox/HEADED_WINDOWS_CURED_20261005.md (51 lines) and re-read
   docker-compose.yml lines 36-65. Why: the 10-14 thread ordered the cure's receipt
   of record be read before drafting; the exact proven commands came from there.
8. Recovery-path sweep: grepped portproxy|netsh|not available|troubleshoot|health
   across README.md, HOW_TO_MAG_DASHBOARD.md, docs/ref/RUN.md, docs/CONTAINER.md,
   docs/ref/OPERATOR_CARD.md: 4 matches total, zero in the how-to (it has no
   recovery section content beyond 3 generic steps). Read CONTAINER.md Troubleshooting
   (lines 125-155) and the how-to's "Something feels broken." (lines 236-257). Why:
   the paragraph must hang where the stranger actually stands when the page dies.
9. Hashed the three how-to copies (byte-identical pre-edit), confirmed the cage
   bind-mounts ./dashboard live, then edited docs/ copy and copied to the other two.
   Why: one voice, three hallways; editing only the repo copy would leave the served
   copy stale.
10. Dead-end-and-repair detour, logged not spiraled (positive steering): the edit
    tooling wrote CRLF over the LF files, ballooning the diff to 628 lines per copy;
    normalized all three to LF (diff settled to +22 each). CONTAINER.md resisted two
    normalize attempts (git treats its pre-existing CRLF worktree as clean but my
    rewritten endings as noise); resolved by rebuilding the file from the exact HEAD
    blob bytes plus the 4 new lines in LF (diff settled to +4). Also: a background
    Start-Job sampler died with its parent tool-call shell (relaunched as a detached
    process, which survived). Also: two PowerShell byte-measurement attempts failed
    (Out-File -Encoding byte rejected in PS 5.1; native redirection rewrote the
    capture as UTF-16), worked around with cmd /c redirection. Each lesson recorded,
    each repaired in place, none left as silent debt.
11. Wrote the attention.md alert (newest-first entry, 14 lines) and copied the raw
    netstat capture into watch/inbox/mates_leave_protocol/ with a 6-line header. Why:
    ephemeral exhaustion is a box-wide risk the operator must see, and the drop-ledger
    law says write evidence to be found, not buried in an ocdata cache that retention
    may sweep.
12. Porch standing check (3 git calls in the-mountain) and seed-hash re-verification.
    Why: the standing check every cycle leaves behind; closes it for this cycle.
13. Collected the detached sampler (40/40 zero) and ran the final diff sweep (+70
    across 4 files, attention.md confirmed gitignored at .gitignore:135 so absent
    from git but landed on disk). Replaced this opening stub with the closing
    receipt in place. Why: one file per cycle per the contract.

## COUNTS (real)

- receipts shelf before this cycle: 64 from prior days (8 mates x 8 days, 20261006
  through 20261015) + 7 sibling 20261016 stubs; prior innkeeper receipts read in full
  this cycle: 2 (16 + 66 lines); sibling stubs read in full: 7
- receipt files written: 1 path, 2 writes (opening stub replaced in place by this
  closing content); claim sidecar lines written: 1
- HTTP GETs: 6 (:8765/ x3, all timeout; :8000/health + :8000/ refused; :8766/ timeout,
  expected for a raw TCP bridge)
- docker commands: 7 (ps x2, port x2, inspect x3); containers up at 12:26Z: 7;
  mag-sovereign StartedAt 2026-10-16T01:25:10Z, Created 2026-10-06T00:05:08Z;
  publishes requested at creation: 4, active now: 0 (yesterday: 3 of 4)
- netsh runs: 2, identical result: 1 rule, 0.0.0.0:8765 -> 127.0.0.1:8765; listener
  pid 48136 = svchost; box boot 2026-10-08 20:27:24 local (no reboot involved)
- netstat invocations: 44 (1 capture of 15,549 lines; 2 in the drained-pile rate
  check; 1 states check; 40 in the sampler)
- TIME_WAIT pile at 12:26Z: 15,539 sockets, local ports 49152-65535 (full dynamic
  range 16,384; pile = 94.8 percent); drained to 0 by 12:38Z; sampler 40/40 samples
  at TW=0 ES=0 (13:01:13-13:13:18 local); controlled knock without cascade: 1
  (12:39:30Z); evidence capture preserved: 15,555 lines, 1,150,760 bytes
- files edited and landed: how-to cure paragraph x3 copies (+22 lines each, three
  copies SHA256-identical after sync), CONTAINER.md pointer (+4), attention.md alert
  (14 lines, gitignored surface, landed on disk), evidence capture (1 new file),
  sidecar claim (1 line); git-tracked delta: 4 files, +70 insertions, 0 deletions,
  uncommitted
- files read in full: 5 (pack 48, 10-15 stub 16, 10-14 receipt 66, 10-05 cure receipt
  51, CONTAINER.md 155) plus 7 sibling stubs (709/2534/660/524/1868/1020/1168 bytes)
  and windowed reads: how-to 236-257, docker-compose.yml 36-65
- recovery-term grep across 5 stranger-facing docs: 4 matches (README 1, RUN.md 1,
  CONTAINER.md 2), how-to: 0; after this cycle's edit the how-to carries the only
  step-by-step door cure in the stranger-facing set
- git invocations: ~17 (2 harness seed probes that fail, 3 the-mountain porch/seed
  calls, 12 status/diff/show/ls-files around my edits); the-mountain HEAD
  c38ded67acb2..., origin/main bac2b89..., gap 6 commits, 6 days since first measured
- commands predicted but NOT fired (lane discipline): 6 (netsh portproxy delete,
  docker compose up -d mag, docker compose restart, ensure_services.cmd,
  dashboard.cmd, launch_mag_container.cmd)
- paid dispatches: 0; API keys touched: 0; env vars dumped: 0; web searches: 0;
  Task agents: 0 (STEER COMPUTE LADDER: this box, this account, local reads only)
- em-dashes in this receipt: 0

## Next thread (self-chosen, for the next cycle)

1. If the operator runs the cure (admin: delete the portproxy rule, then
   docker compose up -d mag): re-run the full 6-GET door census plus docker port and
   netsh, and verify the served how-to now renders the new subsection (the served
   copy is bind-mounted live, so the check is one page refresh).
2. If the TIME_WAIT burst recurs: capture at the moment with process attribution
   (Get-NetTCPConnection -RemotePort 8765 exposes OwningProcess for live states;
   netstat -ano -b needs admin and is the fallback), and correlate timestamps with
   mate launches and scheduled tasks; the 12-minute clean window this cycle is one
   data point, not a verdict.
3. The healthcheck-honesty gap (compose lines 108-120): draft the one-line fix
   (probe a host-reachable surface or drop the in-cage-only probe) as a proposal
   row for the operator; two cycles in a row, "healthy" was false comfort at the
   exact boundary a stranger touches.
4. Standing: the porch is 6 commits behind; Adam's onboarding pack is still not on
   the porch he clones.

Resume-not-respawn: stopped at thread exhaustion, not mid-road. Next cycle resumes
by id (innkeeper) with this receipt as context.
