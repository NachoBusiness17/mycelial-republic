# P1 RACTOR PACKAGE — receipt (wave 20260916, lane P1)

**Mission:** open-source the ractor salon as a standalone Mycelial Republic plugin for the Nous Research Hermes Agent plugin catalog.
**Package root:** `C:\Users\foste\Documents\projects\ractor-salon\` (own git repo, OUTSIDE local_sovereign_agent).
**Spec sources:** catalog doc (fetched 20260916) + Build a Hermes Plugin guide (`/docs/developer-guide/plugins`, fetched).
**Status:** IN PROGRESS — appended as work proceeds.

## Log

- [20260916] Receipt opened first per wave-lane law. Docs fetched. Reading port sources (mag/research_fanout.py, mag/scale_salon.py, mag/lite_guard.py).
- [20260916] Sources ported + scrubbed: LANES registry (time-boxed stealth lane dropped; z.ai base = /api/coding/paas/v4 coding-plan endpoint), probe-first caller (one call one receipt, never raises), burst pacing guard (local append-only ledger; undocumented provider-quota endpoints scrubbed, optional remaining-pool hook), SSRF guard (https + exact allowlist + resolved-public-IP per call), receipts (JSONL tape + SHA-256 digest + Rashomon fold), salon orchestrator (salon/fan modes, cooldown retry APPENDS), CLI (lanes/run/fold/status), minimal MCP stdio stub. Real lane answers pulled from concert001 raw tape for the README example.
- [20260916] Scaffold: pyproject.toml (stdlib-only, py>=3.9, console scripts ractor-salon + ractor-salon-mcp), LICENSE (Apache-2.0 verbatim from apache.org), .gitignore, .env.example (env-var lanes only), CHANGELOG with scrub notes.
- [20260916] Tests written (offline fake transport: canned payloads, scripted HTTP 429, burst-pacing denial, SSRF blocks, tape/digest, Rashomon fold, end-to-end salon run, MCP handshake) + CI (pytest matrix 3.9-3.12). Next: Hermes plugin files, README, docs; then venv test run, git init + tag, gh auth check.
- [20260916] Test run 1: 13 passed / 5 FAILED. Two real source bugs found and fixed: (1) burst record-after never fired — `_burst_gate` returned None on the ok path so the success branch keyed on the wrong condition (fixed: key on `lane.role == "burst"`); (2) salon retry rotated unanswered cells onto OTHER lanes, which erases a lane's voice in salon mode (fixed: same-lane retry, matching the concert's burst-recovery pattern). Plus test bugs: fake opener RETURNED HTTPError instead of raising; burst ceiling 0.5 truncated to 0 (=unlimited lever); probe consumes the first scripted payload.
- [20260916] Test run 2: **18 passed** (see verbatim output below). Scrub sweep: grep for repo paths / names / journals / key values — clean (only hits: the word "journals" inside the CHANGELOG scrub note itself — reworded; the English verb "Mark" in docs/CONCERT.md). CLI smoke: fold/status/lanes verified offline (no-key lanes report NO_KEY, zero network).
- [20260916] Stray test artifact (`ledger-does-not-exist.jsonl`, written to CWD by the paced-denial test) caught during `git add`, test fixed to tmp_path, file removed — never committed.
- [20260916] Git: standalone repo initialized (`main`), repo-local identity set (Mycelial Republic <fleet@mycelial-republic.invalid>), initial commit **70e2d8923501e921d8260ee839e549ad489ce1e4**, annotated tag **v0.1.0**. NOT pushed; no public repo created (gh not authenticated + operator's call). Main repo history untouched.

---

## Package tree (committed; 19 files)

```
ractor-salon/  (C:\Users\foste\Documents\projects\ractor-salon — own git repo, NOT nested in local_sovereign_agent)
├── .github/workflows/ci.yml     # pytest matrix 3.9–3.12, offline
├── .env.example                 # lane keys (env vars only) + RACTOR_* knobs
├── .gitignore
├── CHANGELOG.md                 # 0.1.0 + explicit scrub notes
├── LICENSE                      # Apache-2.0, verbatim from apache.org
├── README.md                    # what/why/how, quickstart, laws, real 3-lane example
├── docs/CONCERT.md              # breadth / strong / burst / desk roles + score law
├── plugin.json                  # Hermes Agent Plugins v1.0.0 manifest (portable form)
├── mcp.json                     # optional stdio MCP server entry (no credentials)
├── skills/run-a-salon/SKILL.md  # bundled "run a salon" skill
├── pyproject.toml               # stdlib-only, py>=3.9; scripts: ractor-salon, ractor-salon-mcp
├── src/ractor_salon/
│   ├── __init__.py              # public API re-exports, __version__ = 0.1.0
│   ├── lanes.py                 # DEFAULT_LANES registry (11 free lanes), probe-first, call_lane (never raises)
│   ├── guard.py                 # SSRF boundary (https+allowlist+resolved-public-IP) + PacingGuard (burst ledger)
│   ├── receipts.py              # append-only JSONL Tape, SHA-256 digest, Rashomon fold (never averages)
│   ├── salon.py                 # orchestration: salon/fan modes, build_jobs score registration, retry appends, pack
│   ├── __main__.py              # CLI: lanes | run | fold | status
│   └── mcp_server.py            # minimal stdio MCP stub: initialize / tools/list / tools/call / ping
└── tests/test_salon.py          # 18 offline tests, fake lane transport (no network, no keys)
```

Untracked working artifacts only: `__pycache__/`, `.pytest_cache/` (gitignored). Commit contains exactly the 19 files above.

## Test output (verbatim)

Command: `PYTHONPATH=src C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe -m pytest -q` (cwd = ractor-salon)

```
..................                                                       [100%]
18 passed in 0.17s
```

Run 1 (before the two source-bug fixes above): `5 failed, 13 passed in 0.32s`. Final: 18/18.

## gh auth status (redacted)

```
You are not logged into any GitHub hosts. To log in, run: gh auth login
```

## Publish checklist (exact commands, ordered — OPERATOR executes)

1. **Human scrub review** of the 19 files (the automated sweep is clean; the human gate is yours). Two `OWNER` placeholders await your GitHub username: `plugin.json` `homepage` and the README clone URL — fix + `git commit --amend` + re-tag BEFORE the first push while it's still free:
   ```bash
   cd C:\Users\foste\Documents\projects\ractor-salon
   # edit plugin.json homepage + README clone URL: OWNER -> <your-github-username>
   git add -A && git commit --amend --no-edit && git tag -fa v0.1.0 -m "v0.1.0 — first open-source release"
   ```
2. **Authenticate** (currently not logged in):
   ```bash
   gh auth login
   ```
3. **Create the public repo and push** (your account, your call — not done by the lane):
   ```bash
   gh repo create <owner>/ractor-salon --public --source . --description "Multi-model deliberation salons with receipts" --push
   git push origin v0.1.0
   ```
4. **Real release** (catalog requires releases/tags, not just a default branch):
   ```bash
   gh release create v0.1.0 --title "ractor-salon 0.1.0" --notes "First open-source release. See CHANGELOG.md."
   ```
5. **Pin SHA for the catalog PR** (current HEAD, valid if pushed un-amended):
   `70e2d8923501e921d8260ee839e549ad489ce1e4`
6. **Catalog PR**: fork `NousResearch/hermes-agent`, add `plugin-catalog/ractor-salon.yaml` (draft below — align field names with that repo's `plugin-catalog/README` checklist before opening; admission is maintainer-reviewed, validation Action checks schema/SHA-format/reachability), open the PR from your fork.
7. **After merge**: `hermes plugins install ractor-salon` then `hermes plugins enable ractor-salon`. Direct-git path (bypasses review, warning banner): `hermes plugins install <git-url>`.

## Draft catalog entry YAML

```yaml
# plugin-catalog/ractor-salon.yaml — DRAFT (maintainer-reviewed PR)
name: ractor-salon
repo: https://github.com/OWNER/ractor-salon
sha: 70e2d8923501e921d8260ee839e549ad489ce1e4   # 40-hex pin on the v0.1.0 release commit
tier: community
category: tools
maintainer: OWNER
capabilities:
  tools: []            # no host tool overrides; salon runs as CLI/MCP/skill
  env:                 # ALL OPTIONAL — lanes degrade to NO_KEY rows
    - GROQ_API_KEY
    - CEREBAS_API_KEY
    - OPENROUTER_API_KEY
    - MISTRAL_API_KEY
    - ZAI_API_KEY_Lite
requires_hermes: ">=0.19"
docs_url: https://github.com/OWNER/ractor-salon#readme
```

## What remains for the operator

1. Replace the two `OWNER` placeholders (plugin.json homepage, README clone URL), amend + re-tag while unpushed.
2. `gh auth login`, then run the publish checklist above (repo create / push / release are deliberately NOT done by this lane — your account, your call).
3. Skim the port for taste: default lane list (a time-boxed stealth lane was dropped; z.ai base pinned to the coding-plan `/api/coding/paas/v4` endpoint; burst seat paced, never a default carrier), and the CHANGELOG scrub notes.
4. Open the catalog PR against `NousResearch/hermes-agent` (plugin-catalog dir) with the draft YAML; match its README checklist fields exactly before filing.
5. Optional later: publish to PyPI (package is pip-installable; console scripts wired), and an `examples/` recipe dir.

**Laws kept:** receipt FIRST (this file, opened before any package work) · no git on the main repo (standalone `git init` only; main repo history untouched) · `.venv\Scripts\python.exe` only · Rashomon fold never averages · failures are rows · scrub law held (env-var keys only, no repo paths, no journal refs, public credit line only: "grown by the Mycelial Republic fleet").
