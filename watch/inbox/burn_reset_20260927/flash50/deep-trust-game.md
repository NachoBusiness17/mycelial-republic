# DEEP-TRUST-GAME: The Estate as a Designed Trust Game: Who Trusts Whom, What Breaks It, What Restores It, and Where the Equilibrium Sits

Item: deep-trust-game (flash50 deep lane) · 2026-09-28 · lane deep-gopher-deep-trust-game
Anchor artifacts: `tools/secret_gate_rules.py` + `tools/secret_gate_scan.py` + `tools/secret_gate.py` (lexical trust) · `mag/headless.py` (constitutional trust) · `mag/verkle_knot.py` (cryptographic trust)

The ask names three trust relations and asks for the game to be designed formally: who trusts whom, what breaks trust, what restores it, and what is the Nash equilibrium, compared against trust-institutions literature. Every estate claim below cites the file and lines read during this ask; every check was run during this ask (check list in section 7). Literature is cited from training knowledge and was not fetched live this session; that limit is stated where it applies.

---

## 0. The three surfaces as they actually run (grounding)

### 0.1 Lexical trust: the secret gate trusts shapes of innocuousness

The gate carries 31 gitleaks-derived provider rules, borrowed verbatim and marked "do not rewrite, do not improve" with provenance bytes at `tools/secret_gate_rules.py:31-65` and `:9-12`. Its exemption surface is `ALLOW_RE` (`tools/secret_gate_rules.py:70-76`): a compiled alternation of placeholder shapes (`your[_-]?api[_-]?key`, `<...>`, `${...}`, `xxxx`, `REDACTED`, `MASKED`, `PLACEHOLDER`, `DUMMY`, `FAKE`, `abcd1234`, ...). The scanner applies it at three points: per token OR against the first 120 characters of the line, on the blockable per-rule path (`tools/secret_gate_scan.py:254`), on the entropy branch (`:275`), and on the combined report path (`:285`). A separate inline marker, `gitleaks:allow`, suppresses a whole line (`tools/secret_gate_rules.py:81`, `tools/secret_gate_scan.py:238-239`).

The gate's exit contract is the trust grammar: 0 clean or report-tier only, 1 blocking finding, 2 scanner error, and "callers must treat 2 as detector blind, never as success" (`tools/secret_gate.py:40-47`). The venv check fails closed to 2 if run on a foreign interpreter (`:139-147`). An unreadable or malformed baseline raises `GateError`, never a silently empty pass (`tools/secret_gate_rules.py:172-195`), and path-scoped baseline entries must carry `by` + `reason` because "a reasonless allowlist is how gates get silently emptied" (`:196-213`).

**Live experiment, this ask.** I wrote two files outside the repo, each containing the same fake key-shaped token `xai-abc123def456ghi789jkl` (matches the XAI-KEY blockable rule, `tools/secret_gate_rules.py:46`):

- `raw.txt` (bare token): `.venv/Scripts/python.exe tools/secret_gate.py --changed "$TEMP/tg/raw.txt"` printed `blocking=1 (threshold=high, provider shapes only)`, `C:/.../raw.txt:1:XAI-KEY:high masked=xai-ab...(len=25)`, `exit=1 BLOCKING findings present`.
- `exempt.txt` first attempt (the word REDACTED on line 1, token on line 2): still `exit=1`. The exemption is line-local; my probe was wrong, the gate was right.
- `exempt.txt` corrected (same line: `XAI_API_KEY=xai-abc123def456ghi789jkl # REDACTED placeholder`): `blocking=0`, `exit=0 clean or report-tier only`.

One word, anywhere in the first 120 characters of the line, walks a key-shaped token through a blocking gate. That is the trust surface: the gate does not trust intent, it trusts a lexical proxy for intent, and the proxy is defeatable by an honest accident (a real secret pasted next to a placeholder comment) or by anyone who has read `ALLOW_RE`.

The estate already caught one cousin of this failure: `COMBINED` ORs all rules into one non-overlapping alternation, so the generic `NAME=value` alternatives at the tail swallowed whole lines and `XAI_API_KEY=xai-...` landed low and did NOT block; the fix compiles the blockable set per-rule, highest specificity wins (`tools/secret_gate_rules.py:144-155`, receipt `watch/inbox/audit_20260926/GATE_DEFECT_ASSIGNMENT_BYPASS_20260927.md`; evaluation order at `tools/secret_gate_scan.py:242-257`). Trust broke there not by evasion but by the mechanism's own composition lying about what it checked.

### 0.2 Constitutional trust: the process tree trusts `creationflags`

`mag/headless.py` is one law with one wording: `no_window_flags()` returns `CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP` on Windows, 0 elsewhere (`:28-36`). The law is installed as a monkey-patch at process start (`main.py:33-39` calls `install_no_window_defaults()` before any command handler), wrapping `subprocess.Popen` as a subclass whose `__init__` first calls `_force_no_window(kw)`, which ORs the flags into whatever the caller passed (`mag/headless.py:39-49, 52-83`). The comment is a museum of past trust breaks:

- `setdefault` was the original bug: callers passing explicit flags without `CREATE_NO_WINDOW` bypassed the default, so headed consoles still popped. The fix deletes the defection move rather than punishing it: OR-ing makes an un-headed spawn structurally impossible from inside the process (`:39-49`).
- The wrapper must be a class, not a function, because `asyncio.windows_utils` subclasses `subprocess.Popen`; a function wrapper crashed every process importing asyncio (`:66-71`, ghost-daemon crash 2026-08-11).
- `DETACHED_PROCESS` alone is not enough (window-storm lesson, header `:3-5`), and combining it with `CREATE_NO_WINDOW` was itself later proven wrong the other way: `mag_launch.py:142-150` records that the two flags are different console-allocation modes whose combination "randomly produced VISIBLE console windows on every respawn"; `CREATE_NO_WINDOW` alone is the correct no-console mode.
- Even a correctly installed law deadlocked: patched `run(capture_output=True)` + `CREATE_NO_WINDOW` filled the OS pipe buffer and hung 360s; the fix reuses `popen_headless` with explicit pipes, `communicate(timeout)`, and forced `PYTHONUNBUFFERED` (`:86-111`).

The law's trust restoration is redundancy at the choke points: `main.py` installs it at import for the process tree; `tests/conftest.py:27-44` installs a second copy under pytest with the operator's own words in the comment ("I've been asking you for months, whenever you invent a new test you forget"), because the per-call-site discipline had 91 unconverted sites. A selfcheck exists (`mag/headless.py:196-199`).

**Live check, this ask:** `.venv/Scripts/python.exe mag/headless.py` printed `headless helper OK`.

### 0.3 Cryptographic trust: the chain trusts recomputable hash algebra

`mag/verkle_knot.py` keeps an append-only JSONL chain of session knots with a persisted tip. The hash function is plain sha256 (`:53-54`). The proof object is sibling-path reconstruction: `VerkleProof.verify()` folds leaf hash plus siblings bottom-up and matches the committed root; it verifies nothing about the world, only an equation (`:443-468`), and `prove()` builds one in O(log n) (`:485-524`). The institution is stated as law in the code: `_verify_chain_consistent()` recomputes the Merkle root over ALL leaves and "refuse[s] to extend an unverified chain (never build on a lie)" before any append (`:536-549`, used by `prove_latest()` at `:527-532`).

The code comments are again a forensics ledger of trust breaks:

- A read-modify-write race between amends and appends left 1,044 chain rows pointing at knot files that no longer existed; the fix is a process-wide single-writer lock with stale-owner probing (`:68-120`).
- Windows `write_text` translated every LF to CRLF and silently changed the bytes the hashes were taken over (B2-393, proved live on the 9,873-line chain); the chain is now written through bytes so LF stays LF (`:430-434`).
- Compaction archives get their own recompute-and-match gate: archived root + sha256 must equal the live counter leaf's record (`mag/verkle_compaction.py:361-390`).
- Corrections never edit history: the Q-020 wave voided a defective grounding row by appending a VOID stamp (`VOID 52db99d28297 executed`, "all 137 rows hash-faithful, none edited in place", commit `b34ccd3ba` message, re-read this ask with `git log --format="%h %s" -1 b34ccd3ba`).

**Live checks, this ask.** `.venv/Scripts/python.exe main.py verkle-audit --dry` returned `ok: true` with tip root `19a2dd614dbb...`, `n_leaves: 8248`, and exactly one integrity gap, severity warn: `chain rows (8248) != knot files (24722)`, prescribed action `python main.py backfill-sessions --all`. `.venv/Scripts/python.exe -c "...vk.prove_latest()..."` returned `{"ok": true, "index": 8247, "n_leaves": 8248, "verified": true}` with the printed reconstruction equation (root `fef442f1441e07d0...`, 14 fold steps), and `_verify_chain_consistent()` returned `True (8248 leaves)`.

One honest observation from those two outputs: the tip file's root (`19a2dd61...`) differs from the root my full-chain recompute produced (`fef442f1...`). The consistency gate compares against the last chain ROW's stored root, not the tip file, and the tip carries its own note ("Tip is the chain tail. An amended older session does not become the boot"). I verified row-level consistency and did NOT reconcile the two root regimes; I report the duality as observed, not as a defect.

## 1. The formal game

Players: a trustor A (a downstream consumer of a verdict: the pre-push hook, the next session's boot, the dashboard, the workflow gate reading a receipt) and a trustee B (the maintainer of the mechanism whose verdict A consumes). B chooses an unobservable action, Maintain (pay maintenance cost m > 0 to keep the mechanism honest) or Drift (save m, let the mechanism rot or add a bypass). A chooses Trust (accept B's mechanism verdict, cost 0) or Verify (recompute it, cost c > 0). Parameterize A's payoffs: v = value of a sound verdict, L = loss from consuming a rotten one, p = probability Drift hurts an un-verifying A, q < p the residual probability under verification. One round:

| | B: Maintain | B: Drift |
|---|---|---|
| A: Trust | (v, -m) | (v - pL, 0) |
| A: Verify | (v - c, -m) | (v - c - qL, 0) |

One-shot analysis: B plays Drift regardless (0 > -m); A's best response is Verify iff c < (p - q)L, else Trust. Either way the equilibrium includes Drift: the mechanism rots and A pays either verification forever or losses. This is the classical result, and the estate's history shows the undesigned equilibrium was actually lived: the 1,044 orphan chain rows (drift undetected until forensics), the `setdefault` bypass (silent defection), the 48,427 AWS-SECRET-40 false positives that buried one critical finding (`tools/secret_gate.py:16-22`), the hand-copied "1,341 tests / 264 files" headline that was "never byte-backed" (AGENTS.md clippy census block), the truncated 532-byte `nav.js` riding at HEAD (commit `d90bc8607`).

The information structure is the crux: Drift is an unobservable action, so the raw game is moral hazard. The estate's institutions all do one of two things: convert the unobservable action into an observable outcome (exit codes, receipts, hash roots), or delete the action from B's strategy set.

## 2. What breaks trust, what restores it: the taxonomy the code itself records

Reading the three surfaces' failure forensics, trust breaks in exactly six recurring ways, each with its restore already landed in code:

1. **Silent bypass.** A mechanism reports "checked" while a path existed unchecked: `setdefault` never applying when flags were explicit (`mag/headless.py:39-49`); the `COMBINED` alternation swallowing provider rules (`tools/secret_gate_rules.py:144-155`). Restore: delete the bypass class structurally (OR-ing; per-rule evaluation) and add a routing self-check probe to the module (`tools/secret_gate_rules.py:108-115`, `COMBINED` group-count assert `:104-107`).
2. **Proxy overreach.** The innocuousness proxy exempts the guilty: the line-head `ALLOW_RE` demo above (exit 1 to exit 0 on one word). Restore: restrict what may ever block vs report (`BLOCKABLE_RULES` / `NEVER_BLOCK_RULES` disjointness asserted, `tools/secret_gate_rules.py:127-142`), and route every surviving exemption through named acceptance (section 3).
3. **Unknowing defection.** B defects without lying: the concurrent append/amend race that orphaned 1,044 rows. Restore: single-writer lock with stale-owner liveness probing (`mag/verkle_knot.py:89-120`).
4. **Channel drift.** The transport alters the artifact between write and verify (CRLF translation, B2-393, `:430-434`). Restore: write through bytes; archive sha256 recorded before any mutation (`mag/verkle_compaction.py:233-244`).
5. **Feigned competence.** A broken detector passing as a clean one. Restore: exit 2 is "detector blind, never as success" (`tools/secret_gate.py:40-47`), `GateError` on unreadable baseline (`tools/secret_gate_rules.py:172-195`), venv fail-closed (`tools/secret_gate.py:139-147`).
6. **Carrier rot.** The claim outlives its evidence: a hand-copied test census riding stale for 12 days while 31 files grew (AGENTS.md, B2-215). Restore: a machine-parsable claim shape with a tripwire and a scheduled deep check that reruns the instrument (`tools/census_drift_patrol.py`, B2-215/216/244/246/249; the carrier shape law makes rewording the claim break the gate instead of silently rephrasing it).

Five restoration institutions recur across all three surfaces: (a) fail-closed defaults; (b) named acceptance, exemptions priced with a who and a why; (c) embedded self-checks and asserts inside the mechanism; (d) recomputable verification on demand; (e) receipts, append-only history, and VOID-instead-of-edit for corrections.

## 3. The designed game and its equilibrium

The estate rewrites the stage game of section 1 with four levers, each pointing at code:

- **L1: Verification is wired into the act of trusting.** A does not get to choose Verify; the mechanism verifies as a precondition of acting. The chain refuses to extend an unverified chain (`mag/verkle_knot.py:536-549`); every spawn is force-ORed headless (`mag/headless.py:39-49`); the gate's per-rule evaluation runs before the report tier (`tools/secret_gate_scan.py:250-257`). This collapses the Trust row of the matrix into the Verify row at near-zero cost c' (O(log n) proofs, `mag/verkle_knot.py:441-442`; the fast-pass prefilter keeps the gate cheap, `tools/secret_gate_rules.py:83-96`). The verification cost was engineered down because a 65s O(n^2) root recompute on append was itself a reason to skip verification (the landmine comment, `mag/verkle_knot.py:732`): an expensive check is a skipped check, so part of trust engineering is making checking cheap.
- **L2: Fail-closed exits remove the lying payoff.** Drift cannot masquerade as success; a blind mechanism announces exit 2. In game terms, the (Trust, Drift) cell where B pretends the mechanism works is cut out: B's deception strategy no longer yields v.
- **L3: Named acceptance prices the residual exception.** When a finding must stand (a test fixture, a documented fixture token like the AWS example probe at `tools/secret_gate_rules.py:108-112`), it is accepted by name into a baseline with author and reason (`:196-218`), or ratchet debt is accepted with `--by <who>` (AGENTS.md build discipline). Drift is not forbidden; it is billed, visibly, to a person. This is a side payment that converts anonymous moral hazard into attributable, auditable debt.
- **L4: Punishment is mechanical, prompt, and cannot renegotiate.** The pre-push ratchet blocks new unnamed debt; "never loosen the hook" is the rule that keeps the threat credible (AGENTS.md build discipline). A hook has no ears: there is no stage at which B can talk A out of the punishment, which is what makes grim-trigger strategies subgame-perfect here in a way human enforcement never is.

**Designed equilibrium.** With L1 through L4, the strategy profiles reduce to: A always accepts verified verdicts (verification is automatic and cheap), B maintains, and any exception B takes is converted at acceptance time into a priced receipt. Call the profile (AutoVerify + PricedException, Maintain). It is a Nash equilibrium: given auto-verification, A has no profitable deviation (manual skipping buys nothing); given mechanical detection and billing, Drift's expected payoff (certain detection at the next hook, audit, or patrol, plus a mandatory named receipt) is dominated by Maintain (-m). It is subgame-perfect because the punishment executes at every information set where defection could pay, without requiring any player to choose revenge. The counter-equilibrium, (Trust, Drift) with rot invisible until forensics, is not hypothetical: it is the documented pre-institution history each code comment preserves.

One more structural observation: the estate assigns the three trust technologies by stakes. Windows popping (annoying, reversible) get constitutional law (defection made impossible). Secrets (moderate frequency, high stakes) get the cheapest and weakest technology, lexical trust, compensated by named acceptance and fail-closed exits. The memory chain (everything downstream depends on it, correction must be visible) gets hash algebra plus append-only VOID. Trust engineering is budgeted proportionally to blast radius, which is itself an equilibrium refinement: spend verification where pL is large.

## 4. Comparison to the trust-institutions literature

(Cited from training knowledge, not fetched this session.)

- **Berg, Dickhaut, McCabe 1995** introduced the trust (investment) game as a measurement device for how much people trust. The estate inverts the program: instead of measuring trust, it engineers the payoff matrix so trusting is optimal. Where BDM's trustee return rates were the finding, the estate's finding would be that return rates can be legislated: exit contracts, OR-ing, and named acceptance are commitment devices.
- **Hardin 2002** (Trust and Trustworthiness) defines trust as encapsulated interest: A trusts B because B has reasons to take A's interests into account. The estate hard-codes encapsulated interest: B's reason is the ratchet and the receipt ledger, not benevolence. The gates are trust-as-incentive made executable.
- **Coleman 1990** treats trust as a rational gamble within social capital; the estate's 50-wide fan-out economy (AGENTS.md fan-out width law) is only profitable because verification was decentralized into mechanisms, a textbook social-capital move: institutions multiply the number of interactions trust can support.
- **Zucker 1986** names three production modes for trust: characteristic-based (similarity), institution-based (formal safeguards), process-based (accumulated exchange history). The estate runs all three deliberately: borrowed-verbatim rule tables with provenance comments (characteristic: trust the donor's bytes, "do not rewrite, do not improve", `tools/secret_gate_rules.py:9-12`), the hook/gate/audit machinery (institution), receipts and ledgers across sessions (process).
- **Shapiro 1987** ("The Social Control of Impersonal Trust") is the closest match: modernity concentrates trust in impersonal intermediaries, and her answer was surveillance of the intermediaries plus insurance. The estate's seats and gates are exactly impersonal agents; the drift patrols, audits, and self-checks are the surveillance, and named acceptance is the insurance policy with premiums paid in receipts.
- **North 1990**: institutions are the rules of the game in a society; the estate's contribution is rules that execute themselves. North's organizations (the seats, lanes, RIBs) shape evolution, but the enforcement curve here is different from all his historical cases: enforcement cost approaches zero.
- **Ostrom 1990** (Governing the Commons): the repo is a commons, and its governance exhibits her design principles with uncanny fidelity: clearly defined boundaries (the shared artifact contract, `watch/inbox/SHARED_SURFACE_CONTRACT.json`), monitoring by accountable agents (audits, patrols), gradated sanctions (warn-level gaps vs exit-1 blocks vs exit-2 incidents; the audit's WARN gap this ask, `chain rows (8248) != knot files (24722)`, is precisely a low-grade sanction with a prescribed cure), and conflict resolution through amend-not-rewrite plus receipts.
- **Milgrom, North, Weingast 1990** (law merchant): judges record disputes, information circulates, and multilateral punishment makes defection unprofitable. The estate's receipt economy plus REGISTRY.jsonl rows plus the FKB is the same triangle: records are cheap, circulation is automatic (inbox, dashboard), and the drift patrol plays the judge that catches a stale or fabricated carrier (B2-215). MNW's cost condition, record-keeping cost below the value of reputation, is engineered to hold.
- **Greif 1993** (Maghribi traders): collectivist enforcement through an in-group registry. The debt-by-name baseline and the workflow gate's per-check registry rows are the same mechanism: you may defect, but your name enters the book.
- **Luhmann 1979**: trust is a reduction of complexity; without it only trivial decisions are possible. The estate's daily shape proves the economics: 50-wide concurrent workstreams are possible because each child does not re-derive the world; the gates are the complexity-reduction layer. Luhmann's "functional equivalents of trust" map to fail-closed design: some interactions need no trust at all because infeasible outcomes are structurally excluded.
- **Williamson 1993** ("Calculativeness, Trust, and Economic Organization") argues most commercial "trust" is calculative and the word should be reserved for genuinely non-calculative relations. The estate is the limiting case that proves him right: nearly all its trust has been made calculative (hashes, exits, receipts, patrols), and what genuinely remains is non-calculative: the operator's GO on plan-only items, seat discipline at the `ALLOW_RE` boundary, entry-point discipline to install the headless law before any spawn. Williamson's residue and the estate's residue coincide, which suggests the estate has, perhaps without naming it, implemented his program.
- **Haber and Stornetta 1991 / Merkle 1988** for the chain's algebra; note the honest branding detail: the header calls it a "Merkle-Verkle hybrid, same spirit" (`mag/verkle_knot.py:3-4`) while the implementation is sibling-path Merkle reconstruction, not a true vector commitment. Even the chain's name is borrowed trust; the math underneath is the older, weaker, sufficient kind.

## 5. Honest limits

- The chain is tamper-evident, not tamper-proof. Tip, chain, and knots are local files; any process with write access can rewrite all three and recompute consistent roots. What I read shows no external notarization; the anchors of last resort are git history, the shared-inbox hash registries, and the operator. Hardin's and Shapiro's point stands: cryptographic verification shifts trust, it does not abolish it.
- The `ALLOW_RE` surface demonstrated live is unpriced residual trust in seat discipline: nothing mechanized stops a real secret from sharing a line head with the word REDACTED. The institution's compensations (only provider shapes may block, named acceptance for survivors) reduce the blast radius, not the surface.
- The headless law's installation is convention at entry boundaries: `main.py` and `tests/conftest.py` install it, a future entry point that forgets is unguarded until it calls a helper.
- Monitoring without automatic healing exists: this ask's audit surfaced the rows-vs-knots gap as a WARN with a manual prescribed action (`python main.py backfill-sessions --all`), not run in this ask.
- The full pytest suite and the pre-push hook were not run in this ask; nothing here claims them. Literature was cited from knowledge, not fetched.

## 6. Check list (all run this ask)

1. `rg -n "ALLOW_RE"` and `rg -n "CREATE_NO_WINDOW"`: located the surfaces (outputs in session).
2. `.venv/Scripts/python.exe mag/headless.py` → `headless helper OK`.
3. `.venv/Scripts/python.exe tools/secret_gate.py --changed "$TEMP/tg/raw.txt"` → `blocking=1 ... XAI-KEY:high`, `exit=1`.
4. Same on `exempt.txt` v1 (REDACTED on the previous line) → still `blocking=1`, `exit=1` (exemption is line-local; first probe was wrong, gate was right).
5. Same on `exempt.txt` v2 (REDACTED on the same line) → `blocking=0`, `exit=0 clean or report-tier only`.
6. `.venv/Scripts/python.exe main.py verkle-audit --dry` → `ok: true`, tip root `19a2dd614dbb...`, n_leaves 8248, one WARN gap (rows 8248 != knots 24722), action `backfill-sessions --all`.
7. `.venv/Scripts/python.exe -c "...prove_latest() + _verify_chain_consistent()"` → `{"ok": true, "index": 8247, "n_leaves": 8248, "verified": true}`, equation root `fef442f1441e07d0...`, `chain_consistent: True (8248 leaves)`; the tip-root vs recomputed-root duality noted, unreconciled.
8. `git log --format="%h %s" -1 b34ccd3ba` → Q-020 line confirming VOID 52db99d28297, 137 rows hash-faithful, none edited in place.
