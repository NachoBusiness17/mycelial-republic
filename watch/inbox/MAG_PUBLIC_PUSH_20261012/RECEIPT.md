# RECEIPT: mag branch published to GitHub as `mag-public` (2026-10-12)

## FINAL STATE (supersedes everything below): curated snapshot model

After the operator's satoshi/riddler directive, the public branch was REPLACED by a
single curated snapshot commit:

- **Remote tip now:** `32e89e62112bea21ed7bdf1b98514f7f4fab8a8b` (orphan, one commit, 9,085 entries)
- **The face is the machine only:** harness code, docs, instruments, canon corpus, dashboard public assets, hitler digs (operator ruled them fine - declassified-docs research)
- **Stripped from the face:** voice memos (19, memory/agent_uploads/voice_stt), zknot session recaps (29), the whole diary layer (memory/, watch/, queue/, bridge/, memories/, agents/ scratch), person dossiers/drafts (person_mine/LilithDatura_DOSSIER.md, paste-ready drafts, thread tap-ins, desk frames, docs/ref/ANNALEA_STANDARD.md), mind organs (memory/MEMORY.md, facts, briefs, attention), receipt-text indexes (catalog/receipt_fts.sqlite, catalog.jsonl/manifest/junctions), 11 mangled junk files
- **Gone entirely with the snapshot model:** the 34 commit messages quoting the operator verbatim, and every other history-borne detail
- **Local bookkeeping:** `mag-public` = remote snapshot tip; `mag-public-full-20261012` = the full 1,027-commit rewritten line (archive, `a77a92ac0cce`); private `mag/run-beta1-...` untouched at `ea8456d32001`
- **Exposure window for the raw content:** ~1 hour (17:5x-18:5x ET), branch (not default), near-zero discovery; GitHub retains unreachable objects until its gc
- **Standing law minted:** `watch/inbox/riddler_face_20261012/CARD.md` - RIDDLER FACE (riddled not decipherable, hotdog-dressing allowed, invariants byte-true; satoshi-mode for the operator; friends protected from his thoughts; memory separate from machine)

## Original push receipt (for the record)

## What landed

- **Remote:** `github.com/NachoBusiness17/mycelial-republic`, branch **`mag-public`**
- **Remote tip:** `a77a92ac0cce225ac6c9483e6f598b700b056ff2`
- **Commits published:** 1,027 (everything on `mag/run-beta1-factory-build-audi-20260806T231709Z` since `github/master` at `dc66499434`, including all three GSTD economy commits: `80d9e0883` multi-node rail + drain + internal economy + beacon + MCP wire, `5da167abb` drain v3 + light maze router, `18a902f8f` reputation-gated cell board, plus `ea8456d32` commit-harness seat)
- **Main repo untouched:** local `mag/run-beta1-...` tip still `ea8456d32001` (hash receipts intact); `mag-public` local branch now tracks the remote twin (`a77a92ac0cce`)

## Why a twin, not the branch

The raw branch carries 47.28 GB of new blob bytes, 39.57 GB of it in 123 blobs over GitHub's 100 MB hard limit (2.4 GB retired estate index, 2.2 GB backup tars, 2.1 GB runaway-evidence jsonl, 16.7 GB training/events.jsonl, multi-GB catalog/index history). GitHub rejects the whole push. The twin is the same commit line rewritten in a throwaway bare clone with:

- every blob >100 MB stripped (size strip)
- `attic/` (backup tars), `tools/godot` (vendored binary), `dashboard/data` (machine indices), `memory/biography_backup_20260825` (personal backup) path-stripped
- `watch/inbox/mrpool_export` stripped (exported chat media, private, never public)
- `corpus/papers_reference_nonredistributable` stripped (the name is the law)

Post-strip: 1,027 commits, max blob 69.7 MB (sutton_barto RL pdf), zero blobs over the limit.

## Secrets posture (why publishing is safe)

- Full-content audit of the unpushed range pre-strip: no .env files, no PEM, no hex64 keys, no mnemonics, no literal key assignments, clean commit messages. Only key-shaped strings found: the secret gate's own synthetic test fixture (constant at `tests/test_gate_blocking_paths.py:217`) and a third-party analytics UUID inside a scraped NI page (public by construction).
- GitHub Push Protection independently caught **one** thing the audit's grep class missed: a **Mapbox secret token** at line 1 of `watch/inbox/frontier_olm_2026-10-03/sweep/tmp/x_evening/lw_swarm.html` (a swept web artifact entering at the GAP-ANALYSIS-EVENING fold commit). NOT bypassed; the file was stripped from the twin. **Open item:** determine whether that Mapbox token is ours (mapbox MCP env) and rotate if so; if scraped from a third-party page, it is their leak and we declined to republish it.

## How the push actually went (laws learned)

1. `git filter-repo` on a non-bare repo runs `git reset --hard` unconditionally (line-level verified in the tool source) - in-place rewriting would have destroyed sibling sessions' uncommitted work. Always rewrite in a separate bare clone.
2. filter-repo does NOT auto-clone `--source`/`--target`; the target must already be a repo. robocopy of `.git` + `core.bare true` works; `git clone --bare` also works but was 5x slower here (17 GB).
3. robocopy copies the source's stale `.git/filter-repo/already_ran` marker, which makes filter-repo prompt interactively (EOFError in background). Delete the copy's `filter-repo/` dir before rewriting.
4. GitHub's push cap is 2 GB/pack; the cleaned pack was 2.06 GB. Sliced chronological anchor pushes (3 commits/slice) fast-forward the remote under the cap.
5. GitHub Push Protection pads stderr paths with trailing spaces; passing the padded string to filter-repo `--path` silently matches nothing (same hashes, same flag, infinite loop). Trim before stripping. Verify a strip worked by checking the tip hash actually moved.

## Refresh pipeline (future publications)

`publish_mag_public.sh` then `slice_push_v2.sh` (both in this dir; temp clone at `%TEMP%/mag-public.git`). The local `mag-public` branch is the publish projection line; the `mag/run-beta1-...` branch remains the private full-fidelity line. Receipts and commit-hash citations stay valid because the private line is never rewritten.
