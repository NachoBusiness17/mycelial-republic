# FW-27 — Ractor-salon publish manifest (operator gate packet)

- Board item: `watch/inbox/FIFTY_WIDE_BOARD_20260917.md:53` — "every OWNER placeholder listed with line refs + exact gh repo create sequence"
- Source of record: `watch/inbox/wave_20260916/receipts/P1_RACTOR_PACKAGE.md` (the P1 publish checklist)
- Package root: `C:\Users\foste\Documents\projects\ractor-salon\` (standalone git repo, outside local_sovereign_agent)
- Packet filed: 2026-09-28, Q-025 queue gopher. All byte-state below re-verified 2026-09-28 against the live repo.

## 1. Every OWNER placeholder, with line refs (re-verified 2026-09-28)

In the repo (2 placeholders — these are the ones to edit):

| # | File:line | Current bytes | Replace OWNER with |
|---|---|---|---|
| 1 | `plugin.json:8` | `"homepage": "https://github.com/OWNER/ractor-salon",` | your GitHub username |
| 2 | `README.md:65` | `git clone https://github.com/OWNER/ractor-salon` | same username |

Verification run 2026-09-28: `grep -rn "OWNER" --include="*.json" --include="*.md" ...` over the
repo returned exactly these two lines; no other OWNER instances exist in tracked files.

In the not-yet-filed catalog draft (3 more OWNER instances, inside the receipt, not the repo):
`watch/inbox/wave_20260916/receipts/P1_RACTOR_PACKAGE.md:97` (`repo:`), `:101` (`maintainer:`),
`:111` (`docs_url:`). These get the same username when you open the catalog PR (section 4 below).

## 2. Repo state today (changes the P1 checklist's step 1)

Verified 2026-09-28 (`git log`, `git rev-parse v0.1.0^{commit}`, `gh auth status` in the package dir):

- HEAD = `438a1c0` ("tests: add test_mcp_server.py"), 3 commits past the tag:
  `d13625f` (N5 external-dogfood checkpoint), `4451d24` (BUG REPORT 001), `438a1c0` (test_mcp_server).
- Tag `v0.1.0` still points at `70e2d8923501e921d8260ee839e549ad489ce1e4` — the exact SHA the P1
  receipt pinned for the catalog entry.
- `gh auth status`: "You are not logged into any GitHub hosts." (still true today).
- Untracked `salon_fiber_20260916/` sits in the working tree. Do NOT `git add -A`; add only the two files.

**The P1 step-1 command (`git commit --amend` + re-tag) is now stale**: it was written when HEAD
was the tagged commit. Amending today would amend `438a1c0`, not the tagged release commit, and
the catalog pins the SHA of the v0.1.0 release commit. Corrected sequence below: fix the two files
in a NEW commit, then re-point the tag (still free; nothing has ever been pushed).

## 3. Exact publish sequence (operator executes, in order)

```bash
cd C:\Users\foste\Documents\projects\ractor-salon

# 1. Fill the two placeholders (plugin.json:8, README.md:65) -> your GitHub username
#    (human scrub review of the 19+ files is your gate; P1 says the automated sweep was clean)

# 2. Commit ONLY the two files (the untracked salon_fiber_20260916/ stays out)
git add plugin.json README.md
git commit -m "publish: fill OWNER placeholders (homepage, clone URL)"

# 3. Re-point the release tag at the new HEAD (nothing pushed yet, so this is free)
git tag -fa v0.1.0 -m "v0.1.0 — first open-source release"

# 4. Authenticate (verified not logged in as of 2026-09-28)
gh auth login

# 5. Create the public repo and push (your account, your call)
gh repo create <owner>/ractor-salon --public --source . \
  --description "Multi-model deliberation salons with receipts" --push
git push origin v0.1.0

# 6. Real release (catalog requires releases/tags, not just a default branch)
gh release create v0.1.0 --title "ractor-salon 0.1.0" \
  --notes "First open-source release. See CHANGELOG.md."

# 7. Pin the NEW sha for the catalog PR (get it after step 2/3):
git rev-parse HEAD    # replaces 70e2d8923501e921d8260ee839e549ad489ce1e4 in the YAML below
```

## 4. Catalog PR (after the repo is public)

Fork `NousResearch/hermes-agent`, add `plugin-catalog/ractor-salon.yaml` (draft from
`P1_RACTOR_PACKAGE.md:94-112`, with OWNER filled and the sha updated to the new HEAD):

```yaml
name: ractor-salon
repo: https://github.com/<owner>/ractor-salon
sha: <new-40-hex-sha>          # pin on the v0.1.0 release commit after the re-tag
tier: community
category: tools
maintainer: <owner>
capabilities:
  tools: []
  env:
    - GROQ_API_KEY
    - CEREBAS_API_KEY
    - OPENROUTER_API_KEY
    - MISTRAL_API_KEY
    - ZAI_API_KEY_Lite
requires_hermes: ">=0.19"
docs_url: https://github.com/<owner>/ractor-salon#readme
```

Align field names with that repo's `plugin-catalog/README` checklist before opening the PR
(admission is maintainer-reviewed; their validation Action checks schema, SHA format, reachability).
After merge: `hermes plugins install ractor-salon` then `hermes plugins enable ractor-salon`.

## 5. What this packet did NOT do

No bytes were edited in the ractor-salon repo, no tag moved, no gh command run beyond the
read-only `gh auth status`, no repo created. Every publish/ops effect stays operator-gated,
per the board section header ("his hands, our runbooks") and the Q-025 queue-index roam verdict
(`queue/queue_index.jsonl:25`).

Receipt: `watch/inbox/burn_reset_20260927/queue/Q-025.md` (FW-27 section).
