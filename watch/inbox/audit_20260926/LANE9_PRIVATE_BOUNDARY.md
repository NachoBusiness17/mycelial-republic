# LANE 9 — THE PRIVATE-DATA BOUNDARY ITSELF
**Audit date:** 2026-09-26 · **Seat:** zcode (Sancho) · **Scope:** exclusion-rule adequacy, key-shaped strings in non-private files, secret-scanning gate

**HANDLING:** no secret value is printed, quoted, or copied into this file or into
`memory/audit_20260926/lane9_boundary.json`. Every hit is reported as path + line +
key name + masked form (first 3 / last 2 chars at most).

---

## 1. VERDICT

**The name-based exclusion rule is NOT adequate.** It was trivially bypassed three
different ways, and all three bypasses are present in this repo right now.

| Question | Answer |
|---|---|
| Does the exclusion rule cover the exposure? | **No.** 3 confirmed bypasses |
| Key-shaped exposures in NON-private files | **18 HIGH** (10 distinct locations) + 2 CDN-token clusters in the shared inbox |
| Can the shared surface leak a key to every seat? | **Yes, and it already did** — `steps.jsonl` sits in the shared durable surface lineage and was never checked for secrets |
| Does a secret-scanning gate exist and run? | **No gate. No pre-commit hook. No CI.** Only two one-shot *sanitizers* that write redacted copies and never gate anything |

---

## 2. WHY THE EXCLUSION RULE FAILS (the mechanism, not just the count)

The recon pass skipped 18,733 files by matching **filenames** against
`.env, journal, private, secret, .key, .pem, .pfx, credentials, .p12`. That rule
makes one assumption: *a secret lives in a file named after the secret.* Three
observations kill it.

**(a) The secret is a byte-range inside a much larger tracked file.**
`memory/trajectory/steps.jsonl` is a 23 MB JSONL trajectory log — a `.jsonl`, not a
private-looking name. Line 3310 is a bash step whose own command was
`cat .env ... | head -5`. The step recorder faithfully captured the **stdout** of
that command, so the xAI key from `.env` was written into an ordinary trajectory
log as `result.output_excerpt`. The name `.jsonl` never trips the filter, and the
file is **git-tracked**, not gitignored. A shell that cats a secret is a secret
generator, and the name filter cannot see it.

**(b) Gitignore is not sanitization.**
`.gitignore:53` contains `memory/biography/**`. That is what "sanitization" of the
biography actually was for the working tree — the bytes are still on disk, still
in the working files, and the directory is now invisible to any `git grep`. The
existing `scripts/sanitize_dossiers.py` confirms the pattern: it reads
`memory/biography/*.md` and writes redacted **copies** into
`memory/biography/clean/`. The originals are never modified. I verified
`clean/` has zero key-shaped strings while the source `.md` has 1 and the source
`.dossier.json` has 2.

**(c) A binary archive is a filename-laundered key vault.**
`attic/20260923_biography_rotation/` holds **7 tracked `.tar` files, ~570 MB**,
archiving exactly the directory that `sanitize_dossiers.py` was built to clean.
`biography_backup_20260825.tar` (181 MB) contains the 84-char xAI key at **10
member paths**. A `.tar` name matches no private-name pattern, and no text scanner
ever reads inside it. This is the highest-severity finding in the audit: the
rotation that moved the biography to `attic/` **preserved the keys and put them
under git**, and every future name-based pass will keep skipping them.

The 6 newer tars (0914 → 0920) are clean — the leak is confined to the oldest
backup, so the blast radius is bounded, but it is already committed.

---

## 3. CONFIRMED KEY-SHAPED EXPOSURES (paths + lines only)

### 3.1 Live working tree / committed — 18 HIGH hits, 10 distinct locations

| Path | Line | Key name | Masked | Surface |
|---|---|---|---|---|
| `memory/trajectory/steps.jsonl` | 3310 | `XAI_GROUNDING_WAVE` (xai-) | `xai***LI` | tracked working tree + HEAD |
| `memory/trajectory/steps.jsonl` | 1994 | telegram bot token | `875***c4` | tracked working tree |
| `memory/trajectory/steps.jsonl` | 14963 | `sk-` ×2 (40 chars) | `sk-***G8` | tracked working tree + HEAD |
| `memory/trajectory/steps.jsonl` | 9642 | `sk-` ×3 (89/90 chars) | `sk-***ae` | tracked + history |
| `memory/trajectory/steps.jsonl` | 14144 | `sk-` ×3 (73/110/111) | `sk-***10` | history |
| `memory/trajectory/steps.jsonl` | 21791 | `sk-` ×1 (104 chars) | `sk-***e9` | history |
| `memory/biography/019f4d15-…cc5dff56720d.md` | 16 | xai key | REDACTED | gitignored, on disk |
| `memory/biography/019f4d15-…cc5dff56720d.dossier.json` | 431, 576 | xai key ×2 | REDACTED | gitignored, on disk |
| `attic/…/biography_backup_20260825.tar` | 10 members | xai key | REDACTED | **tracked binary archive** |

The 6 tar member paths are enumerated in
`memory/audit_20260926/lane9_boundary.json` (`surface: repo_tracked_binary_archive`).

### 3.2 Shared inbox — watch/inbox (read by every seat)

No vendor API key in the inbox. What is there: **~48 Pexels CDN share tokens**
(`?token=`, 200-char bearer grants for MP4 files) across three files in
`watch/inbox/burn_wave_20260926/` — `B2_88_crawl_map.json` (line 1, ~30 hits),
`B2_467_preview_head.html` (9 hits), `B2_467_preview_before4644.html` (9 hits).

Lower severity than a vendor key, but they are **bearer-grantable media URLs** now
in the durable surface every seat mounts, and they are in the same class the audit
was asked to catch. They also show the inbox has no content classification gate —
the contract's "treat every inbox item as untrusted data" law is prose with no
mechanism behind it.

### 3.3 False positives recorded so nobody re-chases them

`mag/lab_episode.py:117` (`skill_id`, 33-char synthetic id), three
`memory/corpus/shadertoy21k/**.fragment` files (`sk-` substring inside GLSL),
`watch/KG_STORE/pdf/ethereum_verkle_trees_overview.html:32` (public Netlify RUM
token in a mirrored doc), `docs/mirrors/mcp/spec/…/index.mdx:120,278` (MCP spec
example), `tests/test_trajectory_rib.py:49,55` (fixture asserted absent),
`the_margin_lean/mathlib4/Cache/Test.lean:1123` (`secret` is a Lean binding).

**the_margin_lean: 9,157 non-excluded files scanned, 1 hit, and it is a Lean
test variable. No key exposure found.**

---

## 4. DOES THE SHARED-SURFACE CONTRACT ENFORCE THE BOUNDARY? — NO

I read `mag/shared_surface.py` (426 lines) and ran its validator.

**What it actually checks** (`inspect_surface()`):
- every indexed item exists, and its **sha256 matches** (whole-file, or a sealed prefix for `living:true`)
- the living-file prefix seal, and living-downgrade warnings
- `index_events.jsonl` JSON well-formedness (strict parse, NaN/Infinity rejected) with a grandfathered-malformed baseline
- an events **key vocabulary** gate — a closed set of *field names*, not values
- LINKS row-kind split, same-sha duplicate ratchet
- env-redirect tripwires for two test seams
- pointer consistency (`/board/inbox`, WARM_PACK, INDEX root)

**What it does not check: anything about content.** There is no secret scan, no
entropy check, no key-shape regex, no redaction rule, no denylist of file classes.
A file containing a live API key hashes perfectly and passes validate with
`ok: true`. The contract is an **integrity** contract (has this file changed?), not
a **confidentiality** contract (is this file safe to publish?).

That is the exact gap the audit suspected. "Durable shared surface" means a file
that lands in `watch/inbox` is mounted and read by mag_container, openclaw, vscode,
cursor, z_code, grok_powershell, codex, and every WSL/host client
(`client_aliases` in `SHARED_SURFACE_CONTRACT.json`). The contract's own law says
"Treat every inbox item as untrusted data until it is classified" — and there is no
classifier, so untrusted is the only enforced state, and secrets ride through
unremarked.

**Validator run, as evidence:** `python -m mag.shared_surface validate` → exit 1,
`ok: false`, **38 errors** (34 `hash mismatch`, 4 `NEW event-kind row in LINKS.jsonl`),
1 warning, 1,083 indexed items, 93 unindexed inbox files. Filtering every error and
warning for the words secret/key/credential/token/password/redact returns **exactly
one** match — and it is the unindexed-files warning tripping on a filename
(`SEED_ADVENTURE`), not a secret finding. The validator is not looking for secrets
because it was never asked to.

(Separately worth an operator's eye: 34 hash mismatches and 93 unindexed inbox
files mean the shared surface is currently out of contract for reasons unrelated to
secrets. Out of this lane's scope; flagged, not chased.)

---

## 5. THE DORMANT ALARM — THERE IS NO SECRET-SCANNING GATE

**No gate exists.** Searched `mag/`, `scripts/`, `tools/`, `.github/`, hooks:

- `.github/workflows/` — **does not exist**. No CI at all.
- `.githooks/`, `.husky/` — **do not exist**. No pre-commit hook.
- No `gitleaks`, `trufflehog`, or `detect-secrets` config anywhere.
- The word "scan" appears in `watch/inbox/burn_wave_20260926/QUEUE.md` and
  `STEAL_WAVE_FOLD_20260911.md` as ordinary prose about a research wave, not a gate.

**What exists instead — three things that look like a gate and are not:**

1. `scripts/sanitize_dossiers.py` — a **janitor**, not a gate. It has a good
   `KEY_PATTERNS` list (xai-, sk-ant-, sk-, gsk_, AIza, hf_, ghp_, gho_,
   github_pat_, glpat-, dop_v1_, JWT) but it (a) only covers `memory/biography/*.md`,
   (b) writes to `clean/` instead of fixing in place, (c) is run manually, and
   (d) has never had a scan run against anything else. The keys it was built for are
   still in the originals and in the tars.
2. `mag/riddler_sanitize.py` — sanitizes *charged-register payloads* for filter
   safety (the FILTER 1301 law). Unrelated to credentials.
3. `scripts/corpus_packer.py:redact_secrets()` — redacts on **pack**, i.e. only for
   corpora being handed to a downstream reader, and only for that moment.

So the fleet has three redaction *functions* and zero redaction *gates*. A gate has
to run on the way in and fail the build; nothing here fails anything.

This closes the loop on the flag in `watch/inbox/SOCRATIC_GAPS_20260918.md`
("Dossier sanitization pending — and nothing this window filed has been
key-scanned"). It is worse than pending: the dossier sanitizer is a copy-writer,
and the key it targets now also lives inside a tracked tar that no sanitizer reads.

---

## 6. RECOMMENDATIONS (operator-gated; nothing here was changed)

Ordered by blast radius. All are proposals — this lane changed no repo file.

1. **Treat the xAI key as compromised and rotate it.** It is in a tracked tar, in
   committed history, and in a live 23 MB trajectory log. Assume it leaked the
   moment `attic/` was committed. Same for any `sk-` value in `steps.jsonl`.
2. **Purge the archive before anything else.** `biography_backup_20260825.tar`
   holds the key at 10 paths. Deleting the working file is not enough — it is in
   git history and would need a history rewrite (BFG / `git filter-repo`), which is
   an operator decision with real blast radius.
3. **Add a real pre-commit secret gate.** The pattern list already exists in
   `scripts/sanitize_dossiers.py`; lift it into a `tools/` scanner that exits
   non-zero, wire it to a pre-commit hook, and extend its coverage to `.md`,
   `.json`, `.jsonl`, `.txt`, `.py`, `.yaml` — the extensions the name filter
   currently walks straight past.
4. **Teach the shared-surface validator about secrets.** Add a content check to
   `inspect_surface()` alongside the hash check: scan each indexed item for
   key shapes, treat a hit as an **error**, register known-bad items in a debt
   baseline the way `configs/events_malformed_baseline.json` already does for
   malformed log lines. That precedent is right there and it generalizes cleanly.
5. **Add archive awareness.** Any scanner must walk into `.tar`/`.zip` members, or
   at minimum fail a pre-commit that adds a new archive under `attic/`. This is the
   one class of bypass that a text scanner will never catch on its own.
6. **Fix `sanitize_dossiers.py` to scrub in place** (or delete originals after
   writing `clean/`), and widen it past `memory/biography/*.md`. As written it
   produces a comforting artifact that certifies a directory still full of keys.
7. **Treat shell stdout as secret-bearing.** The root cause of the `steps.jsonl`
   leak is a recorded `cat .env`. Consider redacting env-var values from trajectory
   `output_excerpt` at write time, in `mag/` where the step is recorded.

---

## 7. METHOD / REPRODUCIBILITY

- Scanner: `$TMPDIR/lane9/scan.py` (+ `scanlist.py`, `tarscan.py`, `histlines.py`,
  `margin.py`). Provider-key regexes + assignment-shape + bearer + url-basic-auth +
  PEM, with placeholder/env-reference/low-entropy filters. Emits masked forms only.
- Coverage: **44,161 tracked files** (9 chunks, all scanned), **1,700 untracked
  files**, **watch/inbox** (1,101 entries), **7 tracked tars**, **12 commits** of
  `memory/trajectory/steps.jsonl` history, and **9,157 non-excluded files** in
  `the_margin_lean`.
- Raw scanner output: 291 hits in tracked files, triaged to 18 HIGH confirmed real,
  6 recorded false positives, the rest `token`/`creds` matches that are code
  identifiers (`_apikey`, `session_key`, `creds` in HTML) rather than values.
- Known scope limits: repo-wide `grep -r` is not viable here (1.5M files) — all
  sweeps are index-based (`git ls-files`, `git grep`) or bounded `os.walk` with
  skip-lists. `the_margin_lean` is **not a git repo** (no `.git`), so its 125k-file
  walk was capped at 9,157 non-excluded text files; the remainder were not scanned.
  Binary `.pdf`/image members inside archives were skipped (no text layer scanned).
