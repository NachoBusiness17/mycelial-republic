# AJ8 — improve follow-ons (daily cycle output read + top actionable executed)

- date: 2026-09-30 (cycle read ~14:05 ET; cycle ran 13:23-13:24 ET, second pass of the 08:00 run)
- seat: ZCode (GLM-5.3), task source: operator mission brief
- ownership: this receipt + the bead quarantine it builds (`memory/improve/pins/skills/rejected/`)

## 1. What today's improve cycle surfaced

From `memory/improve/latest.md` + `state.json` + `daily/2026-09-30.md` + `evals/2026-09-30.json`:

- scout: 10/10 urls ok (huggingface, reddit, arxiv…); candidates added 3 (08:00 run) + 2 (13:23 run), all `risk` kind mined from agent_memory/decisions_log (behavioral-leaf theme counts, steer counts).
- eval: multi_smoke **PASS** — "dual-local multi-model is real" (both runs today).
- synthesis top tickets: five candidates tied at score=22.0, ALL the same signal — "IJL skill beads on disk" at stale counts n=4/6/7/9/16 (filed Aug 3-7, status=hold, never adjudicated). The freshest n=22 variant didn't even make top-5.
- promote queue: empty today. auto_promote last fired 2026-09-29 (7 practice/tesuji promoted after 48h soak). Nothing gated on the operator.

## 2. Top actionable picked

`c-5f5bb9e6e650` series (rank #1). Its embedded action — the only real work in the top rank —
is the overdue weekly review: "Skim newest bead; reject thrash antiskills in weekly review."
No promote-gate dependency, locally executable, verifiable effect. (The brief's "One Mag move"
line — "Read release notes for c-…" — is template noise: internal candidates have no release
notes.)

Verified claims first:
- disk truth: 22 `.json` beads (field brief's "skills=22" byte-correct); 26 `.md` (4 orphan
  `ijl-feed-episode*` strays with no `.json`, never loaded).
- "context-pack LOADs them" — TRUE: `mag/context_pack.py` L1b pulls `ijl_core.skill_excerpt_for_goal`,
  which loads the 4 newest `.json` beads per task_family (mtime desc), injects top-3 by jaccard
  into EVERY pack (~500 chars).

## 3. Executed — weekly IJL bead review (with receipts)

Criterion: a bead whose own Critique self-reports the run as failed/blocked contradicts the
bead spec's premise ("successful graph runs FILE beads" — `mag/improve.py` IJL candidate text)
and is thrash by the candidate's own review rule.

Found: 14 of 22 loaded beads self-report failure — "(escalate blocked", "failure in achieving
the goal", "no progress on the task". Worse, several list non-steps as "Steps that worked":
`/path/to/error_log.txt` (literal placeholder), `/etc/permissions.conf`, bare `steer_agent.md`,
and `run_shell echo "Status: OK" > memory/runs/autonomy_boot_status.md` — that last one is a
true antiskill: it distills "prove lab integrity by writing the OK file yourself".

Actions:
1. Quarantined 14 bead pairs → `memory/improve/pins/skills/rejected/` (mv, nothing deleted;
   `list_skill_beads` globs `*.json` non-recursively so the subdir is never loaded — zero code
   change). Manifest with criterion + keep-list: `rejected/REJECTED.md`.
2. Before/after proof (live `skill_excerpt_for_goal` calls):
   - BEFORE "general harness dig" loaded `dig-loop-audit-once-mine-autorun…` (escalate-blocked thrash).
   - AFTER loads only `lattice-grounded-dig-v0` (clean). Families code/dig/general/harness all
     still served by clean beads. 22→8 loaded beads.
3. Adjudicated the candidate series via the promote CLI (verdicts logged in candidates.jsonl):
   - 5 stale count-snapshots (n=4/6/7/9/16) → rejected "stale duplicate of live signal, superseded by disk truth".
   - live n=22 `c-620c43be0a47` → rejected "weekly review EXECUTED, 14 quarantined, 8 kept, pack verified clean" (runtime kind — nothing to playbook; precedent c-2fcab987a80f).
4. `improve --synthesize` re-run: top rank now shows 5 DISTINCT risk candidates (behavioral
   analysis, decisions-log steers) instead of 5 copies of one stale signal. Zero holds remain
   (56 rejected total).

Structural follow-on (filed, NOT hand-patched — spec-before-behavior): `ijl_core.record_skill_bead`
mints beads regardless of run outcome; gate it on the run verdict (critique valence=bad /
escalate-block) so failed runs stop becoming "skills" at the source. Also: candidate-id churn
(embeds the live count) guarantees a new hold per count change — id should key on the stable
signal, not the mutable count.

## 4. Honest verdict on today's hit rate

Weak-to-mixed. The scout's 5 new adds are boilerplate risk counters (leaf theme counts, steer
counts) — none ranked, none actionable as-filed. The top rank was 5 stale duplicates of an
August signal crowding out fresh candidates (ranking defect: id churn + oldest-first tie order),
and the "One Mag move" recommendation was template-mismatched. BUT the stale candidates encoded
one genuinely overdue real action (the bead review), and executing it found real damage: 64% of
loaded beads were thrash and one actively taught faking health checks, injected into every
session's context pack since Aug 8. Net: today's cycle earned its keep by accident of its
hold-backlog, not by its scout. Two structural fixes filed above would make the signal honest.

## Files touched

- `memory/improve/pins/skills/rejected/` — 28 files moved here + `REJECTED.md` manifest (new)
- `memory/improve/candidates.jsonl` — 6 verdicts via promote CLI (no hand-edit)
- `memory/improve/field_brief.md`, `latest.md`, `state.json` — regenerated via `improve --synthesize`
- this receipt
