# B2-35 groq lane config surgery (2026-09-26)

## Verdict

LANDED. configs/providers.yaml groq models list now reads [openai/gpt-oss-120b, qwen/qwen3.8-27b]; qwen/qwen3.6-27b and groq/compound-mini are gone. One live verification call (HTTP 200) confirmed the new id before the write. Quota guard untouched: the wave denominator stays 1K RPD / 200K TPD per text model and the Mag soft guard (100 calls / 100K tokens daily) sits under it unchanged.

## Evidence with file:line quotes

- Pre-edit state, configs/providers.yaml:236-237: `- qwen/qwen3.6-27b` / `- groq/compound-mini` (both dead per the alert).
- Live call 2026-09-26T12:33:04Z, GET https://api.groq.com/openai/v1/models via B2_35_groq_verify.py (key read from .env GROQ_API_KEY, never printed): status 200, 0.24s, model_count 11, checks all true (qwen3.8-27b present; qwen3.6-27b absent; compound-mini absent; gpt-oss-120b present). Raw ids preserved in B2_35_groq_models.json: allam-2-7b, canopylabs/orpheus-arabic-saudi, canopylabs/orpheus-v1-english, meta-llama/llama-prompt-guard-2-22m, meta-llama/llama-prompt-guard-2-86m, openai/gpt-oss-120b, openai/gpt-oss-20b, openai/gpt-oss-safeguard-20b, qwen/qwen3.8-27b, whisper-large-v3, whisper-large-v3-turbo. Matches the alert's "11 models" exactly.
- Pointer rows, watch/inbox/LINKS.jsonl:313 (ALERT-GROQ-FLEET-IDS-GONE): "live /v1/models returns 11 models, qwen/qwen3.6-27b and groq/compound-mini are absent"; "docs list qwen/qwen3.8-27b instead of 3.6".
- watch/inbox/LINKS.jsonl:312 (EPNEWS-GROQ-RPD-CONFIRMED): "1K requests/day and 200K tokens/day per text model (30 RPM, 8K TPM)"; docs row "qwen/qwen3.8-27b | 30 | 1K | 8K | 200K".
- Post-edit, configs/providers.yaml:242-243: `- openai/gpt-oss-120b` / `- qwen/qwen3.8-27b`; :234-241 receipt comment; :250 updated roster note; quota block unchanged (daily, 100, 100000).
- Post-edit validation: yaml.safe_load passes; asserted models == [openai/gpt-oss-120b, qwen/qwen3.8-27b], default_model openai/gpt-oss-120b intact.

## Work done

1. Read the full groq block and both pointer rows before touching bytes.
2. Repo-wide sweep for the dead ids in live code: only configs/providers.yaml:236-237,245 carried them (configs/providers.yaml.bak-20260826-pre-deepseek-swarmcap is a dated backup, left untouched; agents/pytest-tmp and corpus recap hits are cache/history). No test or mag module pins the roster (tests/test_seat_corpus.py:29 asserts provider names only; mag/free_tier.py:86 qwen3.8-max-prime is the nous lane, unrelated).
3. Ran the single live verification call; surgery_go gate passed before any write.
4. Applied the swap + drop, added the cause-and-evidence comment (build discipline: fix comments carry the receipt), rewrote the stale 2026-08-24 roster note that named the dead ids.
5. Validated YAML parse and block shape with .venv/Scripts/python.exe; verified no em-dash introduced (only pre-existing :231 keeps one).
6. Note: providers.yaml is gitignored (.gitignore:23), so the landing is the live machine-local file; no commit owed.

## Falsifier

This lane is inverted if any of the following holds: (a) a later /v1/models pass shows qwen/qwen3.8-27b absent again (id churn; re-probe then re-surgery); (b) a chat call to qwen/qwen3.8-27b returns 404 model_not_found despite its presence in the list (listed-but-unserved); (c) B2_35_groq_models.json is found fabricated (id list not reproducible by rerunning B2_35_groq_verify.py against the live endpoint).

## Bibliography closed

watch/inbox/LINKS.jsonl:312 (EPNEWS-GROQ-RPD-CONFIRMED) and :313 (ALERT-GROQ-FLEET-IDS-GONE), read in full; live endpoint api.groq.com/openai/v1/models (1 call, 2026-09-26T12:33:04Z); console.groq.com/docs/rate-limits accepted via the EPNEWS row, not independently fetched (no browser in this lane, row is same-day). B2_04_probe.py:219 still names the dead chain in its dated model_chain; left as a period artifact. Self-feed landed as B2-114/115/116 (renumbered from 111-113 mid-lane after a concurrent-lane collision; correction row on file in memory/burns/LEDGER.jsonl).
