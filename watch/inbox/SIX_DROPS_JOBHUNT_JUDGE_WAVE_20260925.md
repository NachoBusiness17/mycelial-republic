# SIX DROPS — JOB HUNT + JUDGE CASCADE WAVE — 2026-09-25

Six operator drops, one flagged actionable. Filed LINKS-327..332.

## 1. ai-job-search (ACTIONABLE — operator: "should do this in my job Hunt")

@tom_doerr 2103093645331005697 → github.com/MadsLorentzen/ai-job-search (MIT). Claude Code as a local job-application assistant: /setup builds profile files (candidate profile, behavioral profile, writing style, rubric, STAR examples) from your documents or a chat interview; /scrape + /rank pull boards, dedupe, score fit on five dimensions with deal-breaker veto; /apply runs a drafter-reviewer pipeline (parse posting → fit score → LaTeX CV + cover letter → fresh-context reviewer agent researches the company and critiques → revise → compile → visual layout inspection → pdftotext ATS check → verification checklist). Author's receipt: 69 applications, 20 interviews, AI engineer role.

Built-in laws we already hold: no fabricated skills, keyword gaps flagged never stuffed, every claim verified against profile. Sparse attributable edits: one application per archive folder. The reviewer is fresh-context = our A3 shape.

**Staged:** cloned to `C:\Users\foste\Documents\projects\ai-job-search` (sibling, private use).
**Gaps to close before first run:** bun MISSING, LaTeX (lualatex/xelatex) MISSING; Python 3.12 OK. Board skills are Denmark-first; `/add-portal` scaffolds US/remote boards (linkedin guest endpoints + freehire.me ship with it). README warns: keep the personal repo private with upstream remote, setup writes personal data into tracked files.
**Runbook:** install bun + MiKTeX/TinyTeX → private repo init with this as upstream → drop CV + LinkedIn export into documents/ → /setup → /scrape → /apply.

## 2. Hermes backlog as vector space

@imbabybrooklyn 2103296417448284191: turned the Hermes Agent backlog into a vector space, unleashed the agent on it, 540+ issues closed in 1.5 days (~2x steipete's best day, ~6x his average). Steal shape: vectorize the queue, agent self-selects next item by similarity to what it just fixed, batch-drains. Maps to our queue/todo + UF backlog + HELP_WANTED.md: those are lists, not a field the janitor can roam.

## 3. JEV-as-a-Judge (folds onto LINKS-326)

@askalphaxiv 2103368968014848400 → CMU paper arXiv 2609.26550 (Li, Miao, Krishnan, Padman). A cheap decision-only judge (JEV) returns verdict + confidence. Frozen cascade: accept confident verdicts, escalate unsure ones to the strong comparator. Numbers: within 3pp of SOTA LLM judge on ordinary preference and evidence-grounded factuality at 0.36x the fee, retains 99% of comparator accuracy at lower cost; the gap concentrates where judging requires re-deriving math or long derivations.

This is the tier ladder applied to judging and it completes this morning's Google fold: factored per-axis verdicts (what the bandit needs) + confidence gate (when to escalate to a frontier judge) = the whole judge lane spec. Derivation-heavy verdicts stay frontier; the long tail of ok/fail goes local (gemma janitors judge their own tier's output).

## 4. Recursive self-improvement harness (mirror receipt)

@muratcan 2103228946292601281: with Opus 5.5 + GPT-6 Astra their harness improves itself, agents do almost every step. The card is a diagram of our own constitution run by someone else: agents write evals (failing call traces → versioned scenario cards: persona/goal/expected tools/end state), agents spawn agents, agents call agents (real tools, sandbox), sparse attributable edits (one root cause per PR), loop = simulate → judge & grade → cluster failures → propose (one fix + one new scenario per PR) → agent review → human gate at merge. Survivors rule: end-state grading (LLM judge plus deterministic graders plus recorded runtime events), dual-runtime regression (fix must hold on both runtimes, stable path stays default with rollback), every review finding fixed with a test or rejected with evidence, customer-specific stuff goes to config not harness. Accept only if every scenario passes in both runtimes.

Fleet mirrors, already held: evals-from-traces = our A/B/C falsifier pre-registration; dual-runtime = dual-window breeding; one-root-cause-per-PR = sparse attributable receipts; human gate = promote --apply. What they have that we should name: the cluster-failures-by-runtime step between judging and proposing (our rejection taxonomy did this once by hand; make it a standing organ), and "harness stays as was" as the default on any failed gate.

## 5. Prompt Optimizer (the joke lands)

@godofprompt 2103061925521498393: Prompt Optimizer, ~32.5k stars, takes the lazy prompt you typed and returns the structured one you should have written. Operator: "haha everything falling into place." Third independent arrival of the same loop in one day: VQQA semantic gradients (Google), JEV confidence-gated verdicts (CMU), and now a consumer tool for prompt uplifting. The pattern is confirmed from three directions; the fleet's version already exists in the prompt library + falsifier law. No build owed; cite it when the prompt-lane work lands.

## 6. Odyssey Agora-2

@odysseyml 2103146841378586820: Agora-2, multi-agent world model, up to 20 humans and agents in one shared real-time simulated environment; multiplayer research preview live (odyssey.systems). Precedent for NPC = SEAT (every NPC a seat over the lane mesh) and the mud layer: a shared world where human and agent actors are peers is now a shipped product, not a design. Watch lane: how they handle identity persistence and drift across 20 actors (their answer will rhyme with CANVAS anchors).

## Wave verdict

The day's three research-flavored drops (LINKS-326 Google, 329 JEV, 330 muratcan) converge on one spec: **factored verdicts + confidence-gated escalation + evals written from real traces + human gate at merge**. That is a build order, not a reading list. The job-hunt tool is the one operator-flagged actionable and is staged with its gap list above.
