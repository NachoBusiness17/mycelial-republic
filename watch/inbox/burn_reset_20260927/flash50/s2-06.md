# s2-06: secret gate gap census - hardcoded secrets the 31-rule gate MISSES

Item: s2-06 (flash50, burn_reset_20260927) | 2026-09-28 | scanner banked at
`watch/inbox/burn_reset_20260927/flash50/_s206_gapscan.py`, raw findings at
`_s206_findings.json`, scanner stdout at `_s206_summary.txt`.
Mask law: every value in this file is masked to first 6 chars + length. No
full secret value is printed anywhere in this deliverable.

## 1. The instrument under test

`tools/secret_gate.py` + `tools/secret_gate_scan.py` + `tools/secret_gate_rules.py`.
Rule count verified by import in this session:

    .venv/Scripts/python.exe -c "from tools.secret_gate_rules import RULES; print(len(RULES))"
    -> rule_count = 31

The 31 named rules (tools/secret_gate_rules.py:33-65): AWS-ACCESS-KID,
AWS-SECRET-40, GOOGLE-API-KEY, GOOGLE-OAUTH-AQ, GITHUB-TOKEN,
GITHUB-FINEGRAIN, GITLAB-PAT, OPENAI-CLASSIC, OPENAI-PROJ, ANTHROPIC-KEY,
OPENROUTER-KEY, GROQ-KEY, XAI-KEY, DEEPSEEK-KEY, ZHIPU-ZAI-KEY, SLACK-TOKEN,
STRIPE-KEY, SENDGRID-KEY, TELEGRAM-BOT, TWILIO-SID, MAILGUN-KEY, NPM-TOKEN,
PYPI-TOKEN, VERCEL-TOKEN, JWT-TRIPLE, PRIVATE-KEY-BLOCK, CONNSTRING-CRED,
GENERIC-KEYASSIGN, ENV-ASSIGN, HEROKU-API, GENERIC-BEARER.
26 are blockable, 5 never block (AWS-SECRET-40, GENERIC-KEYASSIGN,
ENV-ASSIGN, JWT-TRIPLE, GENERIC-BEARER; rules.py:128-140). Behind the rules
sits one entropy branch: runs of `[A-Za-z0-9+/_-]{25,}` at >= 4.3 bits/char
(rules.py:68, 122-123), report tier only, never in BLOCKABLE_RULES.

Gate full mode walks the whole tree minus SKIP_DIR_PARTS
(.git, node_modules, __pycache__, .venv, secret_gate_results;
secret_gate_rules.py:119-120, secret_gate_scan.py:101-105), skipping files
> 10MB, binary-sniffed files, and lines > 4000 chars (secret_gate_scan.py:218,
224, 236).

## 2. Scope and method of this census

Scope = the git repo surface (tracked + untracked-not-ignored) plus root
.env as an explicit add-on:

    git ls-files | wc -l                     -> 47,528 at session start
    git ls-files --others --exclude-standard ->    186 at session start
    fresh recount at close of session        -> 47,593 tracked / 247 untracked
                                                 (+65 tracked files landed by
                                                 other lanes mid-census; live
                                                 50-wide burn, list drift is
                                                 real and stated, never hidden)

The gap scanner (873.8s runtime) captured its own file list at its own
moment: 47,757 paths. Census of that pass:

    files_seen 47,757 | self_skipped 95 | large_skipped 126 | binary 8,363
    read_error 2 | scanned 39,171 | bytes_scanned 884,204,131
    long_lines_skipped(>4000 chars) 13,921 | gitleaks:allow lines 12
    total_lines 7,919,282

It runs 14 gap patterns OUTSIDE the gate's rule shapes (two-segment JWTs,
connection-string schemes beyond the gate's six, basic-auth URLs, ODBC-style
creds, Azure AccountKey/SAS, keyword-gated base64/std and base64/url blobs,
kubeconfig *-data blobs, docker auth, .npmrc _authToken, .netrc, PuTTY PPK,
and a 17-family vendor alternation). Every hit is then tested against the
gate's own compiled rules three ways, imported from the repo's module:

- token level: does any of the 31 rule regexes match the exact token;
- line level: exact replica of the gate engine (per-rule blockable pass,
  span-overlap skip, then COMBINED; secret_gate_scan.py:250-295);
- entropy tier: would the ENT branch fire on the token (>= 25 chars,
  >= 4.3 bits/char), i.e. is the token at least visible to the report tier.

A finding counts as a MISS only when no named gate rule matches the token.

## 3. Headline finding: .env is 38-values-blind

Method: every non-comment value line in .env was tested against all 31 rules
at value level:

    CAUGHT (a named rule matches the value): 11
    VALUE-SHAPE BLIND (no named rule):       38

The 38 blind lines (value masked, name + length shown; line numbers are
.env:NN): L13 VASTAI_API_KEY (len 64), L16/L17 NVIDIABuild + NVIDIABuild2
(nvapi-..., len 70), L20/L23 ALIBABA-MODEL-STUDIO_1/2 (sk-ws-..., len 117),
L26 VERCEL_KEY (vck_..., len 60), L29/32/35/38/41 ZAI_API_KEY{,_2,_3,_Pro,_Lite}
(len 49), L44/L47 HERMES_API_KEY_1/2 (sk-nous-..., len 40), L50 MAPBOX_TOKEN
(pk.eyJ1Ij..., len 97), L53/L56 OPENCODE/OPENCODE2 (sk-..., len 67),
L80/L81 GEMINI_API_KEY + GOOGLE_API_KEY (AQ.Ab8RN..., len 53), L84/L85
TOGETHER_API_KEY{,2} (tgp_v1_..., len 50), L89 COHERE_API_KEY_PAID (len 53),
L92/L93 CEREBAS_API_KEY{,2} (csk-..., len 52), L98/L101 MISTRAL_API_KEY{,_2}
(len 32), L104 CURSOR_API_KEY (crsr_..., len 69), L107 NOTION_API_KEY
(ntn_..., len 50), L119 X_ConsumerKey (len 25), L120 X_SecretKey (len 50),
L121 X_BearerToken (len 116), L122 X_ClientID (len 34), L123 X_ClientSecret
(len 50), L125 GHOST_X_HANDLE (len 13), L126 AOS_AGENT_MODEL (len 26),
L127 OPENCLAW_GATEWAY_TOKEN (len 48), L128 OPENCLAW_GATEWAY_PASSWORD (len 32),
L129 ANTHROPIC_WORKSPACE_ID (len 31), L62 OPENROUTER_MODEL (len 16).
(Removing the four non-credential names still leaves 34 live credentials
with gate-unnamed value shapes.)

Four sub-findings inside this class:

1. ZHIPU-ZAI-KEY has a rule and still misses. The gate's z.ai rule is
   `\b[0-9a-f]{32}\.[0-9a-f]{16}\b` (rules.py:48). The actual ZAI_API_KEY
   value in .env is 32 hex + dot + 16 chars whose second segment is NOT all
   lowercase hex (verified: split lengths [32, 16], all-hex flags
   [True, False], rule match False). The operator's real z.ai keys are
   invisible to the rule written for z.ai.
2. Mixed-case env names dodge the only generic net. ENV-ASSIGN is
   `^[A-Z][A-Z0-9_]{3,}\s*=...` (rules.py:62), uppercase heads only. The
   X/Twitter lines L120 X_SecretKey, L121 X_BearerToken, L123 X_ClientSecret
   fire NOTHING at line level (gate_line_kinds empty in the findings JSON):
   no named rule, not even the report-only generic. Third-party OAuth
   secrets sitting on fully gate-invisible lines.
3. Google's new dot-format key breaks GOOGLE-OAUTH-AQ. The rule is
   `\bAQ[a-zA-Z0-9_\-]{30,}\b` (rules.py:37); the held value is
   `AQ.<43 chars>` and the dot is outside the rule charset, so GEMINI_API_KEY
   and GOOGLE_API_KEY land as ENV-ASSIGN only.
4. New-format vendor prefixes have no rules at all: nvapi- (nvidia), vck_
   (VERCEL-TOKEN still expects the old `vercel_` head, rules.py:57), tgp_v1_
   (together), csk- (cerebras), crsr_ (cursor), ntn_ (notion), sk-nous-
   (hermes), pk.eyJ... (mapbox), sk-ws- (alibaba), plus 32-char mistral and
   116-char X bearer shapes.

Structural amplification: even where the ENT branch would see a token, the
lowercase-hex ceiling is 4.0 bits/char, under the 4.3 ENT floor, so pure-hex
credentials are ENT-blind (invisible to the report tier too). Per the
findings JSON: L13 VASTAI (64 hex), L92/L93 csk- tails, L104 crsr_ tail,
L127 OPENCLAW_GATEWAY_TOKEN are ENT-blind; the ZAI first segments (32 hex)
are structurally ENT-blind as well.

Store context: .env is the sanctioned host-env store (.gitignore:19) and the
gate does scan it in full mode, but every .env line can only ever land as
ENV-ASSIGN: low severity, NEVER-BLOCK (rules.py:139-140). Nothing in .env
can ever block a push, regardless of value shape. This is the single largest
measured gap: 49 value-bearing lines, 11 caught, 38 unnamed, 0 ever blocking.

## 4. Tree verdict: the tracked surface is clean on gap shapes

Gap pattern counts over the whole scanned surface (counts exact, stored rows
capped at 400 per rule):

    JWT2-UNSIGNED     1     (1 file)   CONN-EXTRA-SCHEME   0
    AZURE-SAS         1     (1 file)   BASICAUTH-URL       0
    B64-CTX-STD   1,676   (216 files)  ODBC-CRED           0
    B64-CTX-URL   1,036   (192 files)  AZURE-ACCTKEY       0
    KUBE-DATA         0                  DOCKER-AUTH         0
    NPMRC-AUTHTOKEN   0                  NETRC-CRED          0
    PPK-HEADER        0                  VENDOR-GAP          0

Both singletons resolved as gate-caught, not misses:

- JWT2 hit: watch/KG_STORE/pdf/ethereum_verkle_trees_overview.html:32, a
  Netlify RUM `data-netlify-cwv-token="eyJhbGciOiJIUzI1NiIs..."` in a vendored
  page; token-level NONE but the line fires JWT-TRIPLE (three segments
  present), so the gate sees it.
- AZURE-SAS hit: memory/corpus/game_design_docs/lostgarden_bootstrap_indie_art_2007.html:1347,
  a 40-char hex token (dc6fdc..., len 40) that AWS-SECRET-40 matches;
  gate-caught.

Zero-count cross-validation, independent of the scanner:

    git grep -I -n -E '(jdbc:[a-z]+|(rediss|amqps)://[^ ]+:[^ ]+@|(mssql|
    sqlserver|snowflake|cassandra|clickhouse)://|_authToken|AccountKey=|
    "auth"\s*:\s*"[A-Za-z0-9+/=]{16,}"|machine\s+.*login\s+.*password|
    PuTTY-User-Key-File|client-certificate-data|BEGIN PGP PRIVATE KEY)'
    -- ':(exclude)memory/trajectory/steps.jsonl' ':(exclude)watch/inbox/
    burn_reset_20260927/flash50/*'
    -> zero real hits.

The only grep hits anywhere were (a) this session's own synthetic probes
echoing into the live harness tape memory/trajectory/steps.jsonl (probes are
labeled synthetic in section 5), and (b) detector regexes, not credentials:
scripts/corpus_packer.py:124 and dist_audit/nacho_business_audit_20260912T214050Z/
scripts/{corpus_packer.py:124,sanitize_dossiers.py:31} compile `dop_v1_[a-f0-9]{32,}`
shapes. The estate already knows these shapes exist; the gate does not.

Base64 mass, classified: 2,712 keyword-line base64 findings (1,676 std +
1,036 url). Verdicts over the 800 stored rows: 764 token-missed by all 31
rules (95.5%), 751 sit on lines with ZERO named gate rule (93.9%), 641 are
ENT-blind (80.1%, invisible even to the report tier), 25 decode to
printable bytes, 19 carry ALLOW_RE placeholder shapes. Extension histogram
of the stored rows: json 355, jsonl 288, html 51, env 45, md 27, txt 15,
py 13, ipynb 3, mdx 2, luau 1 - data-at-rest and doc mass, not code. Spot
reads of the decodable ones: arsenal_pages/*.html carry 48-char url-safe
blobs decoding to `/wiki...` path artifacts; corpus/tmp/oni_dig/* and
jina_*.txt carry 48-char game-asset id blobs; no decoded row was a
credential. The 13 .py rows are in dashboard/dashboard-deploy build output
and test fixtures. No hardcoded credential was found in mag/, tools/,
configs/, scripts/, or docs/ under any gap pattern.

## 5. Shape-level proofs: patterns the 31 rules cannot name

Run against the gate's own compiled rule table (command in section 8):

    two-segment JWT    : token NONE, line [ENV-ASSIGN]
    rediss connstring  : token NONE, line [ENV-ASSIGN]
    amqps connstring   : token NONE, line [ENV-ASSIGN]
    jdbc sqlserver     : token NONE, line [ENV-ASSIGN]
    npmrc authToken    : token NONE, line [ENV-ASSIGN]
    azure acctkey      : token NONE, line [ENV-ASSIGN]
    discord token      : token NONE, line [ENV-ASSIGN]

All seven shapes: zero hits from all 31 rules, line-level notice only from
the never-blocking ENV-ASSIGN generic, zero contribution to blocking_count.
Concrete rule-level gaps, each anchored:

- CONNSTRING-CRED covers exactly postgres/postgresql/mysql/mongodb(+srv)/
  redis/amqp with user:pass@ (rules.py:60). rediss:// and amqps:// (the TLS
  variants, prefix-plus-s) do not match the rule; mssql, sqlserver, oracle,
  snowflake, cassandra, clickhouse, trino, presto, elasticsearch, opensearch,
  influxdb, sftp/ftps, ldaps, mqtt, jdbc are all absent. ODBC/ADO.NET
  `Server=...;User ID=...;Password=...` and Azure
  `AccountName=...;AccountKey=<88-char base64>` and SAS `sv=...&sig=...`
  have no rule.
- JWT-TRIPLE needs three segments (rules.py:58); a two-segment JWT
  (alg:none, or split storage) matches nothing.
- GENERIC-KEYASSIGN's name list is api[_-]key|apikey|secret|
  access[_-]token|auth[_-]token|password|passwd (rules.py:61): no authToken
  (so .npmrc _authToken is unnamed), no accountKey, no sas, no consumerSecret.
- No rules for: kubeconfig client-certificate-data / client-key-data /
  certificate-authority-data blobs, docker config.json "auth" base64
  user:pass, .netrc machine/login/password, PuTTY PPK containers (the PEM
  rule only matches BEGIN ... PRIVATE KEY headers, rules.py:59).
- 17 vendor families absent: discord (M/Nxxx.yyy.zzz), GOCSPX- (GCP oauth),
  1//... (google refresh), dop_v1_ (digitalocean), shp(at|ca|pa|ss)_ (shopify),
  dapi + 32 hex (databricks), hf_ (huggingface), fig[dou]_ (figma), ATATT
  (atlassian), ATBB (bitbucket), lin_api_ (linear), secret_ + 43 (notion),
  hvs. (vault), glsa_ (grafana), PMAK- (postman), ya29. (google access),
  glrt-/gldt-/gloas-/glcb- (gitlab non-PAT). Tree currently carries zero
  instances (section 4), so these are prophylactic gaps, not live leaks.
- Live-in-.env vendor formats the gate cannot name (section 3): nvapi-,
  vck_, tgp_v1_, csk-, crsr_, ntn_, sk-nous-, pk.eyJ, sk-ws-, AQ.<dot>,
  and the actual z.ai 32hex.16mixed shape that defeats ZHIPU-ZAI-KEY.

## 6. Structural blind spots (by design, counted not fixed)

- 126 files over the 10MB cap skipped whole (secret_gate_scan.py:218);
  largest: attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar
  (2.36GB), dashboard/data/ractor_board.jsonl.runaway-evidence-20260903
  (2.24GB), watch/ESTATE_INDEX/ESTATE_INDEX.jsonl and
  dashboard/data/ESTATE_INDEX.jsonl (1.29GB each),
  dashboard/data/ractor_board.jsonl (713MB),
  artifacts/vertigo_boat_20260908/tokyo_river_depth_1080p.mp4 (268MB),
  training/events.jsonl (255MB), attic/20260923_biography_rotation/
  biography_backup_20260825.tar (190MB). Any secret in these is invisible.
- 13,921 lines over 4000 chars skipped per scan (secret_gate_scan.py:236):
  minified bundles and long jsonl rows are dark.
- 8,363 binary-sniffed files, 95 gate self-skips, 12 gitleaks:allow lines,
  2 read errors (1 reproduced: canon/riddler_corpus/liberprimus, Permission
  denied; 1 not reproduced on a recheck pass and therefore unnamed).
- The ENT branch can never block: it is not in BLOCKABLE_RULES
  (rules.py:128-135), so entropy-visible-only secrets are report noise by
  construction (the 09-27 full-tree run recorded entropy_total 3,055,337,
  watch/inbox/secret_gate_results/fulltree_20260927.json).
- Baseline today: zero line-fingerprint acceptances, six path-scoped
  entries (configs/secret_gate_baseline.json), all doc/test fixtures.

## 7. Recommended rule additions (operator call, cheapest first)

1. ENV-ASSIGN: allow mixed-case names (`[A-Za-z][A-Za-z0-9_]{3,}`) or add a
   second mixed-case variant; today X_SecretKey-class lines are invisible
   (rules.py:62, evidence L120/L121/L123).
2. Broaden ZHIPU-ZAI-KEY second segment to `[0-9a-zA-Z]{16}` or add a
   32hex DOT 16 alnum variant (rules.py:48, evidence .env L29-41).
3. GOOGLE-OAUTH-AQ: add dot-tolerant variant `AQ\.[A-Za-z0-9_\-]{30,}`
   (rules.py:37, evidence .env L80/L81).
4. Vendor prefix rules for formats actually held here: nvapi-, vck_,
   tgp_v1_, csk-, crsr_, ntn_, sk-nous-, sk-ws- (evidence .env lines above).
5. HEX-40 / HEX-64 keyword-context rule to catch pure-hex creds under the
   ENT floor (evidence: VASTAI L13, CURSOR L104, OPENCLAW L127 ENT-blind).
6. rediss/amqps plus the extra-scheme and ODBC/AccountKey/SAS connstring
   rules (rules.py:60 today covers six schemes only).
7. Two-segment JWT, _authToken, kubeconfig *-data, docker auth, .netrc, PPK,
   and the 17 absent vendor families (zero live instances today).

## 8. Reproduce

    ./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_s206_gapscan.py
      (writes _s206_findings.json; stdout summary banked as _s206_summary.txt)
    .venv/Scripts/python.exe -c "from tools.secret_gate_rules import RULES; print(len(RULES))"
    git grep -I -n -E '<pattern>' -- ':(exclude)memory/trajectory/steps.jsonl'

Note: the synthetic probes from section 5 were run through this session's
harness and are now echoed in memory/trajectory/steps.jsonl (session tape).
Those strings are fabricated probe payloads, not credentials.

## 9. Not done / caveats

- The gate's own full-tree scan (13.7h, 2.4M files, 30.9GB on 2026-09-27,
  receipt watch/inbox/secret_gate_results/fulltree_20260927.json) was NOT
  rerun; its numbers are cited from the banked receipt, mine are from my
  own 873.8s pass over the git surface + .env.
- The ignored data-at-rest mass (memory/runs, corpus caches, lmcache) is out
  of this census's scope; it is also out of the gate's changed-mode scope
  and was last swept by the 09-27 full run.
- The 2,712 base64 findings were verdict-classified on the 800-row stored
  sample (400 per rule); total counts are exact, per-row decode coverage is
  sample-level. The per-rule store cap is stated in the scanner source.
- 126 >10MB files and 13,921 >4000-char lines were counted, not scanned.
