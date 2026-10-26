# Secret-scan rule set + solo-operator rotation policy (2026-09-26)

Lane B2-73, the UF-129 dead redo. The 2026-09-18 gap analysis row
(`watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md`, secret-scanning row: 9 rows,
"dossier sanitization (pending) + 60 filed artifacts never key-scanned")
asked for CI-grade scanning patterns turned into an estate hygiene pass the
operator can actually run. UF-129 died on provider model 404s
(`watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md`, dead-row
evidence), so this deliverable is local python only: a gitleaks-pattern rule
set plus a Shannon entropy pass, and a rotation policy written for one human.

## 1. The rule set (as shipped)

Instrument: `watch/inbox/burn_wave_20260926/B2_73_secret_scan.py`
Run: `.venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_73_secret_scan.py`
Output: `watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json`
(masked heads only: first 6 chars plus length; full values are never written
by the scanner anywhere).

Scope law: `corpus/` and `watch/inbox/` recursive. Skip classes, each counted
in the results census: git internals (`.git`, `node_modules`, `__pycache__`,
`.venv` dirs), binary-sniffed files (NUL byte or under 85 percent text bytes
in the first 8192), single files above 10 MB, and the scanner's own two
output files. Lines above 4000 chars are skipped (base64 blob bodies, not
key material on a line).

| Rule id | Severity | Pattern (regex source) | Catches |
|---|---|---|---|
| AWS-ACCESS-KID | high | `\bAKIA[0-9A-Z]{16}\b` | Amazon access key ids |
| AWS-SECRET-40 | medium | `\b[A-Za-z0-9/+=]{40}\b` with boundary guards | generic 40-char base64 secret (noisy, triage band) |
| GOOGLE-API-KEY | high | `\bAIza[0-9A-Za-z_\-]{35}\b` | Google/AI Studio keys |
| GOOGLE-OAUTH-AQ | high | `\bAQ[a-zA-Z0-9_\-]{30,}\b` | Google OAuth-start tokens (the B2-63 gemini key class) |
| GITHUB-TOKEN | high | `\bgh[pousr]_[A-Za-z0-9]{36,255}\b` | classic + OAuth + server + user-to-server tokens |
| GITHUB-FINEGRAIN | high | `\bgithub_pat_[A-Za-z0-9_]{20,255}\b` | fine-grained PATs |
| GITLAB-PAT | high | `\bglpat-[A-Za-z0-9_\-]{20,}\b` | GitLab PATs |
| OPENAI-CLASSIC | high | `\bsk-[A-Za-z0-9_\-]{20,}T3BlbkFJ[A-Za-z0-9_\-]{20,}\b` | classic OpenAI keys (base64 marker) |
| OPENAI-PROJ | high | `\bsk-proj-[A-Za-z0-9_\-]{20,200}\b` | project keys |
| ANTHROPIC-KEY | high | `\bsk-ant-[A-Za-z0-9_\-]{20,200}\b` | Anthropic keys |
| OPENROUTER-KEY | high | `\bsk-or-v1-[a-f0-9]{64}\b` | OpenRouter keys |
| GROQ-KEY | high | `\bgsk_[A-Za-z0-9]{20,80}\b` | Groq keys |
| XAI-KEY | high | `\bxai-[A-Za-z0-9]{18,80}\b` | xAI keys |
| DEEPSEEK-KEY | high | `\bsk-[a-f0-9]{32}\b` | DeepSeek keys (32 hex) |
| ZHIPU-ZAI-KEY | high | `\b[0-9a-f]{32}\.[0-9a-f]{16}\b` | Zhipu/Z.ai GLM keys (id.secret hex) |
| SLACK-TOKEN | high | `\bxox[abposr]-[A-Za-z0-9\-]{10,250}\b` | Slack bot/user/app tokens |
| STRIPE-KEY | high | `\b(?:sk\|pk\|rk)_(?:live\|test)_[0-9a-zA-Z]{10,}\b` | Stripe keys |
| SENDGRID-KEY | high | `\bSG\.[A-Za-z0-9_\-]{16,}\.[A-Za-z0-9_\-]{16,}\b` | SendGrid keys |
| TELEGRAM-BOT | high | `\b[0-9]{8,10}:AA[A-Za-z0-9_\-]{33}\b` | bot tokens |
| TWILIO-SID | medium | `\b(?:SK\|AC)[0-9a-f]{32}\b` | Twilio sids/api keys |
| MAILGUN-KEY | high | `\bkey-[a-f0-9]{32}\b` | Mailgun keys |
| NPM-TOKEN | high | `\bnpm_[A-Za-z0-9]{36}\b` | npm tokens |
| PYPI-TOKEN | high | `\bpypi-[A-Za-z0-9_\-]{50,}\b` | PyPI tokens |
| VERCEL-TOKEN | high | `\bvercel_[A-Za-z0-9]{24}\b` | Vercel tokens |
| JWT-TRIPLE | medium | `\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b` | signed JWTs (may be public claims; triage band) |
| PRIVATE-KEY-BLOCK | critical | `-----BEGIN [A-Z0-9 ]*PRIVATE KEY( BLOCK)?-----` | embedded private keys |
| CONNSTRING-CRED | high | scheme `://user:password@` for postgres/mysql/mongo/redis/amqp | credentials in connection strings |
| GENERIC-KEYASSIGN | medium | case-insensitive `api[_-]key\|secret\|...token\|password` followed by `=`/`:` and 16+ token chars | unstructured assignments (triage band) |
| ENV-ASSIGN | low | line-start `UPPER_CASE=` 8+ value chars | dotenv-style dumps (triage band) |
| HEROKU-API | medium | `\bHRKU-[0-9a-fA-F\-]{36}\b` | Heroku keys |
| GENERIC-BEARER | medium | case-insensitive `bearer ` + 20+ token chars | pasted auth headers |

Entropy pass: candidate tokens are runs of `[A-Za-z0-9+/_\-]` of length 25 or
more; a token reports when Shannon entropy over its characters is 4.3 bits or
higher (pure hex tops out at 4.0, so sha256 seals and ledger hashes do not
fire; base64-style key material sits at 4.5 to 5.5). The entropy branch runs
last so concrete provider rules win the match position.

Allowlist (dropped before counting, policy documented here): `your_api_key`
style placeholders, `<...>` and `${...}` templates, `xxxx`/`....`/`***` runs,
`REDACTED`/`MASKED`/`PLACEHOLDER`/`EXAMPLE`/`DUMMY`/`FAKE`, and the two
documented test literals (`abcd1234`, sequential digit runs).

Interpretation bands: critical/high rule hits are confirms until proven
otherwise (revoke first, see policy); medium triage band needs a human look
at the line; low/entropy rows are candidates. A high hit inside a receipt
that quotes a live key is still a live key: quoting it in a filed artifact is
itself the finding.

## 2. Solo-operator rotation policy

Estate facts this policy is built on (byte-cited): keys live at rest in the
root `.env` and `configs/providers.yaml` env references (root `.env` holds
the two OPENCODE keys per `watch/inbox/burn_wave_20260926/B2_253_transport_decision_20260926.md`;
the gemini `AQ.*` credential per `watch/inbox/burn_wave_20260926/B2_63_gemini_auth_20260926.md`).
Both sit OUTSIDE the scan scopes (`corpus/`, `watch/inbox/`), so the scanner
polices the artifact estate, and this policy owns the key rest places.

1. One rest place per key. A key lives in root `.env` (referenced by config),
   never copied into receipts, probes, packs, or session text. The scanner's
   masked-head output (6 chars plus length) is the only quoting format
   allowed in filed artifacts. This is the mask law.
2. Routine cadence: rotate every provider key on a 90-day calendar. One
   sitting, one operator: open each provider console, mint the replacement,
   update `.env`, delete the old key, log one line in the rotation journal
   (`watch/inbox/KEY_ROTATION_JOURNAL.jsonl`, created on first rotation).
3. Event-driven rotation (rotate now, ignore the calendar) on any of:
   a key hits in a scan report, a key is pasted into any filed artifact, a
   pack leaves the machine containing `.env` material, a provider announces
   a breach, or a session transcript containing a key leaves local disk.
4. Leak response order (the load-bearing sequence, gitleaks remediation
   practice adapted to one human): (a) revoke/rotate at the provider FIRST,
   (b) mask or remove the key from the artifact bytes, (c) only then rewrite
   history if the repo is pushed or shared (`git filter-repo` on the named
   paths), (d) rerun the scanner to confirm zero, (e) file a receipt with
   masked value, rule id, and file:line. Rotate before rewrite: a history
   rewrite without revocation leaves the key live in every clone.
5. Scan cadence: rerun the scanner after any burn wave that writes receipts
   (receipts quote probes; probes are where keys leak into artifacts), and
   at minimum weekly. The scan is local python, zero cost, no network, so
   the only limiter is habit. Wire it beside the census patrol when the
   one-automation limit frees a slot; until then it is a manual command.
6. Solo simplifications, stated honestly: no CI, no teammates, no secret
   sharing ceremony, no pre-commit hook requirement. The CI-grade rule set
   runs as a local script; the CI-shaped parts (branch protection, org-level
   push protection) are out of scope for one operator and are not pretended.
7. Out-of-scope honesty: this pass does not read git pack history (`.git`
   internals are a skip class). If a key is ever found in a tracked file,
   the history question opens and rule 4c applies; until then the estate's
   exposure surface is working-tree bytes plus whatever left the machine.

## 3. Pointers

- Gap origin: `watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md` (secret-scanning row)
- Dead-row bodies: `watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md`
  (UF-129 404 evidence, raw.jsonl lines)
- Scanner + results: `watch/inbox/burn_wave_20260926/B2_73_secret_scan.py`,
  `watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json`
- Receipt: `watch/inbox/burn_wave_20260926/B2_73_secret_scan_20260926.md`
