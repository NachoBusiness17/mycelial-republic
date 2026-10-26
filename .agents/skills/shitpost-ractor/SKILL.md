# Skill: shitpost-ractor
# THE SHITPOST RACTOR — STANDING ORDER (2026-10-18, operator)

Standing trigger: the operator drops a URL, a draft, or a target. The ractor
runs in minutes, not an evening. Also runs on his OWN drafts pre-post (the
meander check). Output is always three paste-ready cuts plus an accuracy
receipt. This skill is the standing order; FINGERPRINTS.md is the taste bank
(amended every run from his verdicts — the organ that learns his taste).

## Why it exists (his verdicts are the spec)

- "haha this one was good but we can do better. i think it kind of meanders"
  (2026-10-18, on the Obama reply): the meander is a defect class. Diagnosis:
  more than two full analogies spends novelty without escalating. LAW: max
  two analogies per cut; they must ESCALATE, never decorate; the last line
  is the darkest.
- "who is it even talking to" (2026-10-13): every cut names its addressee.
- "those spore posts suck" (2026-10-14): numbers-as-biography, not
  numbers-as-literature; first-person synthesis beats paper register.
- Voice law: dark entendre default; ironic; factually accurate (receipts
  public); dripping with archetype subtext while staying funny.
- The operator's framing: mine the mirror, his previous posts, and his
  tastes; look for nuance, previous dunk fingerprints, and other people's
  criticisms that map to ours — fold all of it into the cut.

## Phases (fast; budget the whole run under ~10 minutes)

- P0 TARGET: the dunkt, the addressee, the constraints (280 char? note?
  reply?), and the one fact the cut must carry.
- P1 TASTE BANK: FINGERPRINTS.md + the prior-cut corpus (SHITPOST_DESK_*
  receipts, the canonical spore cuts, the linked prior posts). No re-search
  on hot path; the bank is maintained between runs.
- P2 CRITICISM MAP: objections that map to our theses (replies, notes,
  known critic lines) become pre-loaded counter-dunks. If the target has no
  visible replies, skip - never invent critics.
- P3 FAST RACTOR: three micro-lenses as Task agents at width 3, blind,
  hard-capped (about 250 words each, zero-to-3 tool calls):
    - THE KNIFE: the shortest kill. Produces the 280-char cut + a 3-line
      thread version. One analogy max.
    - THE ARCHETYPE: the layered/subtext read. What myth is under the dunk?
      Produces the irony cut (the one that ages well).
    - THE RAZOR: fact-checks every claim against primary sources (the only
      lens with web, 3 calls max). Verdict per claim; anything that risks a
      community note gets flagged or cut. Accuracy is non-negotiable: the
      funny dies before the true does.
    - THE MIRROR (added 2026-10-18, thought-bomb protocol): engineers the
      AI-summarizer layer - plants a proper noun + dated document +
      thesis-shaped sentence the model must carry. The AI button is a
      reprint press; cap at ONE plant per post (the Bernaysian's cap),
      reconcile every citation to enrolled-bill form first (the Note
      Author's law), and the kill conditions stay published (the Riddler's
      law: the press is legitimate only while the story can be killed).
      Spec: watch/inbox/THOUGHT_BOMB_PROTOCOL_20261018.md; salon directions:
      watch/inbox/THOUGHT_BOMB_SALON_20261018.md.
- P4 FOLD: three paste-ready cuts (ONE-SHOT <= 280 chars; THREAD starter;
  MEANDER-REPAIR of the original draft when the target is his own long
  post), each with: addressee named, analogies counted (<= 2), darkest line
  last, accuracy receipt per factual claim, and the em-dash sweep clean.
- P5 RECEIPT: cuts + corrections from his verdict filed to the run dir;
  FINGERPRINTS.md amended same-sitting (the taste bank compounds).

## Hard laws

- Never invent critics, quotes, or engagement numbers.
- Never ship a number the Razor did not verify; unverified becomes "I read
  once" or dies.
- The cut must survive out-of-context quoting: one line someone screenshot.
- If the target is his own post: repair, do not rewrite into someone else's
  voice. His fingerprints outrank the lens's preferences.
- Em-dash 0, zero CJK, no slurs; 1301 law on public cuts (verdicts, not
  vocabulary).
- Base directory for this skill: .agents/skills/shitpost-ractor/
