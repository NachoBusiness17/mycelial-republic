# MASTER AUDIT - MICKEY-17 v2.1 fold (audit genre, 6 lanes, 2026-10-07 window)

- folded: 2026-10-07T19:23:05Z by the fold script (sha256 58bd72c79c6d); master prose by the fold seat, 2026-10-07 window. Run moment per manifest: 2026-10-07T02:55:19Z, plan width 50, 12 lanes planned, 6 fired this window (manifest.json read this sitting; the casualty header below is the byte truth of what landed).
- supersedes: the 2026-10-06 edition of MASTER_AUDIT.md (12 lanes, 55 rows, script sha256 76bb8ea7620d) that sat at both of these paths until this overwrite (`carried`, from reading the prior file header before replacing it).
- source of every number: `memory/runs/mickey17_v2/runs/audit/FOLD_SECTIONS.md` (authoritative, script-computed from the lane archive at `memory/runs/mickey17_v2/runs/audit/lanes`). Seats write prose around the script. Any number this seat brought itself is tagged `carried`.
- estate copy: `corpus/steal/MASTER_AUDIT.md` - workspace copy: `C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_AUDIT.md` (byte-identical pair; sha256 stamped at the foot).
- lane archive read in full this sitting: the 6 lane JSONs (i1-herald-read.json, i2-cli-installer.json, i3-hermes-plug.json, i4-electron-scaffold.json, i5-conf-demo.json, i6-key-wizard.json) plus the 6 persisted checks files (`*.checks.json`, mtimes 2026-10-07 12:26-14:45). The per-claim verifier verdict blocks (deepChecks/laneChecks evidence) reached this seat inside the fold-gate handoff (the ask's run metadata); where this fold quotes them they are tagged `carried`.

The rule of this fold is the rule of the whole burn: the script counts, the seats write, and where prose and byte disagree the byte wins. Nothing below outranks `FOLD_SECTIONS.md`.

## CASUALTY HEADER (scripted, verbatim)

- fired: 6
- landed (parseable files): 6
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## SCOREBOARD (recount) (scripted, verbatim)

- rows: 41
- estate_status: confirms-ours 18, new 10, executed 10, we-have-better 1, executed-with-deviation 1, owed 1
- leverage: high 28, medium 12, low 1

## FIDELITY (scripted, verbatim)

- rows with all of quote/source/steal/estate_status non-empty: 41/41 (100.0%)

## VERIFIER TABLE (scripted, verbatim)

- lanes with persisted checks: 6
- verdicts: deep_tier2 12 (verdict split: verified 12), supports 35 (supports split: no 29, yes 6)
- deep_tier2 join: 9/12 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 3

## WIDTH-ECONOMICS (scripted, verbatim)

- rows/lane: median 5, max 10, min 5
- top-10 lanes share: 100.0%
- exact cross-lane duplicate quotes (normalized): 1
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)

## PRISMA FLOW (scripted, verbatim)

- identified: 41
- screened: 41 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 41
- invariant: identified == included + excluded **HOLDS** (41 = 41 + 0)

## URL LIVENESS (scripted, verbatim)

- unique URLs: 15; fetched: 15; skipped non-public: 0; live: 6; dead/blocked-status: 9
  - HTTP -1: https://raw.githubusercontent.com/iamlukethedev/Herald-OS/main/linux/bin/herald-os-catalog (add_to_p
  - HTTP -1: https://raw.githubusercontent.com/iamlukethedev/Herald-OS/main/linux/bin/herald-os-catalog (Probe.me
  - HTTP -1: https://www.rfc-editor.org/rfc/rfc8628.txt (line 374, byte-verified via curl)
  - HTTP -1: https://raw.githubusercontent.com/iamlukethedev/Herald-OS/main/plugins/herald-os-bridge/bridge/permi
  - HTTP -1: https://raw.githubusercontent.com/iamlukethedev/Herald-OS/main/linux/catalog/ai.json (7 entries: cla
  - HTTP -1: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps (curl-verified
  - HTTP -1: https://raw.githubusercontent.com/iamlukethedev/Herald-OS/main/plugins/herald-os-bridge/bridge/tools
  - HTTP -1: https://raw.githubusercontent.com/iamlukethedev/Herald-OS/main/linux/bin/herald-os-catalog (module d
  - HTTP -1: https://www.rfc-editor.org/rfc/rfc8628.txt (lines 593+602, byte-verified via curl)

- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.

## TOP-K (scripted, verbatim; a lane-claimed top steal outside this list files as DISPUTED)

- [high] i1-herald-read#0: the one-click installs for claude code/codex/gemini cli etc. execute `npm install -g --prefix ~/.local` so the
- [high] i1-herald-read#1: machine-written config is provenance-tagged and idempotent: add_to_path dual-writes path to ~/.bashrc (line su
- [high] i2-cli-installer#0: claude code reads claude.md from cwd and every directory above it, and claude.md files import other files via 
- [high] i2-cli-installer#1: codex reads agents.md starting at the project root walking down to cwd (not upward), so the kit wires ./agents
- [high] i2-cli-installer#3: opencode reads agents.md (project, traversing up from cwd; global at ~/.config/opencode/agents.md) and combine
- [high] i2-cli-installer#4: cursor project rules live in .cursor/rules as .mdc files with description/globs/alwaysapply frontmatter, so th
- [high] i2-cli-installer#6: executed: one-command installer detects claude/codex/gemini/opencode/cursor (binary on path or config dir), wi
- [high] i2-cli-installer#7: executed: tested on every cli actually installed on this box (claude, codex, opencode, cursor) plus the gemini
- [high] i3-hermes-plug#0: plan_call runs before every fire and its extra_body must ride the wire unmodified; the one time the plan was d
- [high] i3-hermes-plug#1: the thinking-control law: deepseek must receive thinking {type: disabled} explicitly on the wire because omiss
- [high] i3-hermes-plug#2: guard_terminal is the one response choke point: classify the raw content channel, and on empty_reasoning (empt
- [high] i3-hermes-plug#3: the budget floor per ask shape has money teeth: the plan_call 24000 review floor priced a1's reserved cost ove

## TOP STEALS (the script's TOP-K, 12 - expanded with quotes and actions)

The TOP-K is the deterministic top: the first 12 high-leverage rows in (lane, row) order with lanes alphabetical. This seat reproduced the identical 12 from the lane files (check run this sitting, foot of file). Quotes and actions below are verbatim from the lane rows; the verifier tag per entry names the strongest persisted verdict that row carries (deep_tier2 evidence blocks: `carried`, from the fold-gate handoff).

1. **i1-herald-read#0** [high, new] - npm-prefix installs. Quote: "Ours: npm --prefix ~/.local puts the agent's command in ~/.local/bin." Action (steal sentence, i1-herald-read#0): installer seat ports the catalog schema + first-usable-method picker (pick_method returns the method or a human-readable why-not via method_reason per kind) into a tools/estate_install.py; STEAL_MAP receipt lands watch/inbox/. Estate grep this sitting: zero 'npm --prefix' hits in tools/ and mag/, no installer file in tools/ - pattern genuinely new. Verifier: deep_tier2 VERIFIED (join-miss on row_key wording, see DISPUTED D1).
2. **i1-herald-read#1** [high, new] - provenance-tagged idempotent config. Quote: "New terminals (bash) and apps started by the session (systemd's environment.d) both see it." Action (i1-herald-read#1): adopt the provenance-tag + append_once/remove_line pair for every estate-written config line (tag-greppable removal, never hand-pruned) and the dual-write bashrc+environment.d shape for the estate installer; README attribution note modeled on their NOTICE (pinned upstream lock, one line per borrowed work). Verifier: deep_tier2 VERIFIED.
3. **i2-cli-installer#0** [high, confirms-ours] - Claude Code CLAUDE.md walk. Quote: "Claude Code loads CLAUDE.md and CLAUDE.local.md from your current working directory and every directory above it." Action (i2-cli-installer#0): claude adapter emits @starter-kit/... import lines inside a marked block; landing spot starter-kit/tools/install_into_cli.py render_block(). Verifier: deep_tier2 VERIFIED.
4. **i2-cli-installer#1** [high, confirms-ours] - Codex AGENTS.md root-down walk. Quote: "Starting at the project root (typically the Git root), Codex walks down to your current working directory." Action (i2-cli-installer#1): one marked ./AGENTS.md block serves codex+opencode; landing spot starter-kit/tools/install_into_cli.py CONVENTIONS map. Verifier: deep_tier2 VERIFIED (join-miss on row_key wording, DISPUTED D2).
5. **i2-cli-installer#3** [high, confirms-ours] - opencode shares AGENTS.md. Quote: "You can provide custom instructions to opencode by creating an AGENTS.md file" Action (i2-cli-installer#3): shared AGENTS.md adapter means codex+opencode cost one block; landing spot starter-kit/tools/install_into_cli.py CONVENTIONS. Verifier: tier-1 supports NO only (the banked quote carries the AGENTS.md creation phrase but not the traverse-up/global-path conjuncts; no deep check on this row). Weakest-verified entry in the top 12 - cited accordingly.
6. **i2-cli-installer#4** [high, confirms-ours] - Cursor .mdc rules. Quote: "Project rules live in .cursor/rules as .mdc files" Action (i2-cli-installer#4): cursor adapter owns the whole kit-named file and unlinks it on uninstall (an empty rule shell would still load); landing spot render_cursor_rule(). Verifier: deep_tier2 VERIFIED.
7. **i2-cli-installer#6** [high, executed] - the installer landed. Quote: "Detects installed CLI agents (claude, codex, gemini, opencode, cursor) by binary on PATH or their config dir, then wires the seat pack" Action (i2-cli-installer#6): residual: rerun --dry after any change to the kit doc set; the pack list is PACK_DOCS/PACK_CARDS at the top of the file. Verifier: deep_tier2 VERIFIED (join-miss on row_key wording, DISPUTED D3), with one finding: the uninstall trailing-newline edge (DISPUTED D5).
8. **i2-cli-installer#7** [high, executed] - the test battery landed. Quote: "D. post-uninstall `find` -> sandbox empty. Clean uninstall: PASS." Action (i2-cli-installer#7): residual: no real CLI session was launched to confirm ingestion; verification is file/bytes level plus vendor docs. Verifier: deep_tier2 VERIFIED.
9. **i3-hermes-plug#0** [high, confirms-ours] - plan_call before every fire. Quote: "the plan was computed at the call site and dropped one hop before the wire, so the nous-primes reasoning {max_tokens: 6000} rail never reached the request that burned 15998 reasoning tokens" Action (i3-hermes-plug#0): ported plan_call into starter-kit/integrations/hermes/hermes_client.py; fire() merges plan.extra_body with core keys winning (the plan cannot rewrite model/messages), called before every http.client request. Landed this sitting. Verifier: deep_tier2 VERIFIED with the "unmodified" nuance (DISPUTED D6).
10. **i3-hermes-plug#1** [high, confirms-ours] - the thinking-control law. Quote: "THINKING OFF MANDATORY: send thinking {type: disabled} explicitly; omission is NOT the off state (d4 3-arm probe 2026-10-04 refuted the old AH10 omission note)" Action (i3-hermes-plug#1): ported all 10 FAMILY_TABLE rows (thinking_control merged, forbidden_keys stripped, per-animal floors, sources cited) into the kit client verbatim; parity-diffed against mag/inference_budget.py: zero semantic diffs, 6/6 plan_call probes agree. Landed this sitting. Verifier: tier-1 supports YES.
11. **i3-hermes-plug#2** [high, confirms-ours] - guard_terminal choke point. Quote: "Carrier choke point: classify the content channel; on EMPTY_REASONING bank the burn row (ok False, empty_reasoning flag) and mint the marker." Action (i3-hermes-plug#2): ported classify_empty + guard_terminal + react + skip_terminal into the kit client; every response passes through guard_terminal before any salvage; the mocked test pins the terminal path (marker minted, burn banked ok:false, skip-on-sight). Landed this sitting. Verifier: deep_tier2 VERIFIED.
12. **i3-hermes-plug#3** [high, confirms-ours] - floors have money teeth. Quote: "sonnet AND haiku both floor to max_tokens=24000. A1 (sonnet, 49,942-token prompt) reserves 0.0999 + 24000 x 1e-5 = ~0.34 USD > balance: 402, deterministically, every hourly fire, never self-healing." Action (i3-hermes-plug#3): the kit client floors per shape (small 8000 / review 24000 defaults, per-animal overrides) and banks every fire, refusal and transport failure as a usage row with cost (bank is a required fire() argument), so an install sees its own walls in its own ledger from day one. Landed this sitting. Verifier: deep_tier2 VERIFIED.

Cut by the K=12 line despite high leverage (script's list ends at i3-hermes-plug#3; these are next in the same ordering and file as strong seconds, not disputes): i3-hermes-plug#4 (the WALL row, cured this lane), i2-cli-installer#8, and every high row in i4-electron-scaffold, i5-conf-demo, i6-key-wizard.

## DISPUTED (10 entries)

Tier-2 unconfirmed rows: ZERO. All 12 deep_tier2 verdicts read "verified"; nothing moves to negatives for lack of tier-2 confirmation. The 29 tier-1 "supports: no" verdicts are quote-scope findings, not disputes: the checker tests one banked quote against the full compound claim, and the quotes are shorter than their claims by design; they are recorded in the verifier table, not re-litigated here. The disputes this fold actually carries:

- **D1 - deep_tier2 join-miss, i1-herald-read#0.** Script: 9/12 deep row_keys join a lane row; 3 miss, "verified, no exclusion weight, labeled not fatal". This seat replicated the join (foot of file) and names the misses: the row_key "i1-herald-read: One-click installs for Claude Code/Codex/Gemini CLI" does not string-prefix the lane row claim, which starts "The one-click installs..." (i1-herald-read.json row 0). The deep-check evidence itself fetched the same source (herald-os-catalog, 34,669 bytes via curl) and verified the row's substance. Ruling: verdict VERIFIED carries; the miss is prefix wording drift ("The"); no exclusion weight, per the script's own label.
- **D2 - deep_tier2 join-miss, i2-cli-installer#1.** Row_key "Codex reads AGENTS.md from the project" vs the claim's "starting at the project root" (i2-cli-installer.json row 1). Same shape as D1: wording drift, evidence block verified the doc bytes live (HTTP 200, verbatim sentence under whitespace normalization). Ruling: VERIFIED carries, not fatal.
- **D3 - deep_tier2 join-miss, i2-cli-installer#6.** Row_key "EXECUTED: one-command installer detects the five" vs the claim's enumerated "detects claude/codex/gemini/opencode/cursor" (i2-cli-installer.json row 6). Same shape. Ruling: VERIFIED carries, not fatal.
- **D4 - "zero hits" scoping on i3-hermes-plug#4 (the WALL row).** The row claim says "grep of all starter-kit for nous/endpoint: zero hits". The deep check (`carried`) confirmed nous zero-hits at HEAD but found ONE "endpoint" hit at HEAD:starter-kit/LAWS.md:58 ("ONE FRONT DOOR. Route through one carrier (one import, one endpoint)...") - the carrier-routing sense, not an inference endpoint. Ruling: the row's operative substance (an install reaching a paid model had no endpoint or budget law configured) is verified; any downstream citation of this row must scope the zero-hits wording to "nous" and the inference-endpoint sense, not the bare word.
- **D5 - uninstall trailing-newline edge on i2-cli-installer#6.** Deep check (`carried`) probed the uninstall restoration: "user line" restored as "user line\n"; multi-trailing-newline inputs collapse (rstrip at the splice edges) against the inline comment's promise. No content bytes outside markers are ever altered; the single-trailing-newline case restores exactly. Ruling: the row stands verified; the phrase "user bytes restored exactly" must be restated as "marker-scoped content-exact; trailing-newline collapse at the splice edge" and the edge fixed or documented before the byte-exact claim is repeated.
- **D6 - "ride the wire unmodified" overstatement on i3-hermes-plug#0.** Deep check (`carried`): _build_body overlays core keys over the plan and its own docstring says the core keys win; plan_call also pre-processes extra_body. The operative law the source supports is "the plan must REACH the request", which the landed kit client implements. Ruling: verified with nuance; cite the law as plan-reaches-wire, not unmodified.
- **D7 - fold-time URL liveness vs same-day byte verification.** The script read 9 citations HTTP -1 at 19:23:05Z; the parenthesized notes on those same entries are the rows' own earlier receipts ("byte-verified via curl"), and the deep-check evidence blocks (`carried`) show fresh curl fetches of herald-os-catalog succeeding earlier on 2026-10-07 (34,669 bytes; three fetches for the add_to_path row). Ruling: per the script, the 9 rows sit in NEGATIVE RESULTS with their fold-time status; treat HTTP -1 as an unresolved fetch-environment reading, not proof of source death; re-verify before any external citation. Mapping of the 9 entries to rows (this seat's reading of the scripted note anchors, counts are the script's): i1-herald-read#0,#1,#2,#3,#4,#5 (the four raw.githubusercontent Herald-OS URLs) and i6-key-wizard#0,#1,#2 (rfc-editor x2, docs.github.com x1).
- **D8 - the 561k phantom number, i5-conf-demo#3.** The ROLL_SHAPE receipt's "561k content-addressed cells, same picture on every machine" has zero corroboration in memory/runs/mickey17_v2/runs/overnight-mesh-20261007/ (rg zero hits for 561/standing/same-picture; i5-conf-demo.json row 3). Ruling: verify the figure from a mesh_delta scan output or strike it before it reaches a conference slide. GO item 3 carries the re-source action.
- **D9 - premise-drift pair, i1-herald-read#5.** Both quotes: the ask premise, "one-click installs ... WRITE CLI configs (which files, which fields)"; the byte truth, Herald's install surface is "(flatpak, dnf, pacman, aur, npm, mise, script, webapp, link); the first one this machine can use" with NO per-agent CLI config written (PATH plumbing plus one systemd unit only). Ruling: byte truth wins; the corrected premise rides the STEAL_MAP receipt (GO item 6) so no seat hunts for a config-writing mechanism that does not exist.
- **D10 - clone-URL WALL, i5-conf-demo#0.** Both quotes: the quickstart's canonical clone URL answers HTTP 200, but the served repo is THE MAG SEED - 1,798 files, trees API tools/ and integrations/ empty, raw fetches of tools/profile_boot.py, tools/install_into_cli.py and integrations/hermes/README.md all 404 (i5-conf-demo.json row 0, checks_run). Ruling: beat 1 of the demo breaks on an audience member's machine until the starter-kit is pushed or the URL repointed; that push is GO item 1 and blocks items 2 and 3 of the demo path.

## NEGATIVE RESULTS (counted reasons table)

Nothing was excluded at screen (PRISMA excluded: 0); every negative below is a first-class included row or a fold-time status, not a dropped row.

| # | Reason | Count | Rows / receipts |
|---|--------|-------|-----------------|
| 1 | Fold-time URL liveness failure (HTTP -1 at 2026-10-07T19:23:05Z); script ruling: rows move here with their status; rendered rows carry url_checked_at | 9 citations | i1-herald-read#0,#1,#2,#3,#4,#5 (Herald-OS raw URLs); i6-key-wizard#0,#1 (rfc-editor.org/rfc/rfc8628.txt); i6-key-wizard#2 (docs.github.com OAuth page). All 9 carry earlier same-day byte-verification receipts in their own source notes and in deep-check evidence (`carried`, DISPUTED D7). Excluded stays 0. |
| 2 | Zero-hit prior-art greps banked as first-class negative rows | 4 rows | i2-cli-installer#5 (zero estate prior art on CLI config-convention installers; residual hits are this repo's own AGENTS.md and one incidental canon_harvest.md:46 line); i6-key-wizard#5 (no device-flow/RFC 8628/key-wizard prior art in corpus/steal or memory/research_polished; sole estate trace m16.md:18, the abandoned 2026-09-07 attempt); i5-conf-demo#4 (README-HERMES_CONF.md does not exist anywhere; naming shortlist and dated timeline have zero estate bytes - OWED, not invented); i1-herald-read#5 (premise drift, DISPUTED D9). Lane-level zero-hit greps beyond rows: i3 (corpus/steal and memory/research_polished zero for plan_call/guard_terminal; the kit carried no budget law pre-lane), i1 (memory/research_polished zero for herald), i4 (memory/research_polished zero for electron - the scaffold is the estate's first). |
| 3 | Declared not-run / honest-gap disclosures (per lane) | 6 lanes | i3-hermes-plug: no live API fire (ask forbids spend without an operator key); DNS-fence live leg ran patched. i1-herald-read: 3 not_run items (S4 node staging watch-only; terminal_guard protected-paths comparison hook-refused, not claimed; demo video unwatched). i2-cli-installer: 4 filed negatives in row 9 (MCP config deliberately unbuilt - no phantom servers; gemini adapter untested against a real gemini; in-tree E2E hook-blocked, covered by unit assertions over the shipped module; dry mode prints 'updated' where real runs dedupe to created+unchanged). i4-electron-scaffold: the Electron window itself never launched (binary is the operator-gated download); electronjs.org WebFetch timed out, curl of the v41.10.7-tagged docs was the fallback. i5-conf-demo: demo script, push, naming, and timeline all OWED. i6-key-wizard: live OAuth unexercised (needs the operator click); google/openrouter OAuth endpoints null rather than fabricated; verification_uri_complete unused; report capped at 5 of 10 banked rows. |
| 4 | Hard tombstones (subtracted from owed) | 0 | tombstoned: [] (script run metadata). |
| 5 | Landed-empty / parse errors / missing files | 0 / 0 / 0 | casualty header. |
| 6 | Exact cross-lane duplicate quotes (normalized) | 1 | i2-cli-installer#9 == i5-conf-demo#0: "No MCP config is written: this kit ships no MCP server, and registering a server that does not exist would be fabrication." (this seat's join check reproduced the pair). One canonical copy lives in the lane files; no top-steal entry duplicates it (neither row is in the TOP-K). |
| 7 | Phantom-number flags pending verification | 1 | i5-conf-demo#3, the 561k figure (DISPUTED D8, GO item 3). |

## GO LIST (top 10, one seat one sitting)

Ranked: demo-critical path first (1-3), operator-gated fires next (4-5), estate-side seats last (6-10). Every item names its lane rows; each is one seat, one sitting, unless marked.

1. **Push starter-kit/ to the canonical clone URL (or repoint the quickstart URL).** Cures the D10 WALL: today the quickstart 404s on an audience member's machine (the URL serves The Mag Seed, kit tools raw 404 x3). The push effect itself is operator-gated. Blocks GO items 2-3's demo path. [i5-conf-demo#0]
2. **Author README-HERMES_CONF.md from the five verified beats.** All beat evidence is already banked in the lane file; the naming shortlist and the dated timeline stay explicit GATED operator questions, never guesses. [i5-conf-demo#4]
3. **Fire the P2 bob node, and re-source the 561k figure.** One run of scripts/bob_bootstrap.md ON bob (a seat on bob, not this box) so beat 5 is two machines pulling the same picture; pull the cell count from a mesh_delta scan output in the same sitting or strike it from the slide. [i5-conf-demo#3]
4. **key_wizard --live, once.** Operator creates the GitHub OAuth App with device flow enabled, puts the Client ID in KEY_WIZARD_GITHUB_CLIENT_ID, runs --live once; the click IS the consent; drop the receipt into corpus/steal/ so the i6-key-wizard#5 zero-hit grep cures itself. [i6-key-wizard#7, i6-key-wizard#5]
5. **Rehearse ONE live hermes-plug ask at stage-shape.** Point the landed plug at the funded endpoint, usage ledger visible on screen, so beat 3 is a proven fire and not a read-me claim. Needs the operator key. [i5-conf-demo#2]
6. **Land tools/estate_install.py.** Port the Herald catalog schema + first-usable-method picker (bin+detect dual detection, ordered per-kind install list); the STEAL_MAP receipt states the corrected premise from D9 (installs write PATH plumbing plus a systemd unit, never per-agent CLI config). [i1-herald-read#0, i1-herald-read#2, i1-herald-read#5]
7. **Effect-broker deltas.** Port the uuid-salted per-call rule key for destructive actions (a persisted 'always allow' can never match) and the no-channel fail-closed Decision(False,'blocked') to the estate effect broker. [i1-herald-read#3]
8. **dashboard/server.py effect routes.** Adopt the audit.jsonl one-line-per-invocation schema (args truncated, no contents logged) and default-to-mutate-on-unknown for unknown UI commands. [i1-herald-read#4]
9. **Estate installer config discipline.** Provenance-tag + append_once/remove_line on every estate-written config line, and the dual-write bashrc + environment.d shape so session-launched apps see PATH too. [i1-herald-read#1]
10. **providers.json stretch rows.** Fill google/openrouter OAuth endpoints from their docs (PKCE/loopback) and flip enabled; the wizard already refuses unimplemented rows loudly (exit 2, never improvises). [i6-key-wizard#8]

Residuals outside the top 10: rerun install_into_cli.py --dry after any kit doc-set change (i2-cli-installer#6); README.md quickstart gains the one-command line next pass (i2-cli-installer#8); the hermes budget-law wire itself is already landed - no GO needed, only rehearsal (i3-hermes-plug#0-#4); the electron pin is already landed at 41.10.7 exact, bump only with a receipt (i4-electron-scaffold#4); fix or document the uninstall trailing-newline edge before repeating any byte-exact restoration claim (DISPUTED D5).

## RECHECKS RUN THIS SITTING (the fold seat's own instruments)

- Row recount, status/leverage distributions, fidelity, deep-join replication, duplicate-quote detection: `.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/fold_check_master_audit.py` over the lane archive. Output: rows/lane i3=5, i1=6, i2=10, i4=5, i5=5, i6=10, total 41; estate_status confirms-ours 18 / new 10 / we-have-better 1 / executed 10 / executed-with-deviation 1 / owed 1; leverage high 28 / medium 12 / low 1; fidelity 41/41; JOIN replication 9 joined / 3 miss with the misses named (i1#0, i2#1, i2#6 - all prefix wording drift); DUP quote pair i2-cli-installer#9 == i5-conf-demo#0. Every number agrees with FOLD_SECTIONS.md.
- TOP-K reproduction: same venv python, lanes sorted alphabetically, first 12 high-leverage rows in (lane, row) order printed exactly the script's 12 entries (i1#0, i1#1, i2#0, i2#1, i2#3, i2#4, i2#6, i2#7, i3#0, i3#1, i3#2, i3#3).
- Persisted-checks census: `ls` on the lanes directory showed exactly 6 `*.checks.json` files (i1 14:37, i2 14:40, i3 14:36, i4 14:45, i5 12:26, i6 13:09, 2026-10-07), matching "lanes with persisted checks: 6".
- Not run here, and not claimed: any network fetch (the script owns URL liveness; the HTTP -1 statuses are its readings, DISPUTED D7), and any re-execution of the lanes' own tests (their receipts live in the lane files and transcripts).

## CARRIED

The verifier verdict tables and their evidence blocks (12 deep_tier2 verified with full mechanical evidence strings; 35 tier-1 supports verdicts; the D4, D5, D6 and D7 findings inside them) reached this seat in the fold-gate handoff rather than from a file this seat read; the six `*.checks.json` files on disk corroborate that the checks were persisted. Every other number and quote in this fold was read this sitting from: `memory/runs/mickey17_v2/runs/audit/FOLD_SECTIONS.md`, the six lane JSONs under `memory/runs/mickey17_v2/runs/audit/lanes/`, the run manifest, and the prior edition of this file (for the supersession note only).

Fold pair stamp: written twice, byte-identical, sha256 recorded at write time (see the run receipt; both files carry the same bytes by construction, `cp` from the estate copy).
