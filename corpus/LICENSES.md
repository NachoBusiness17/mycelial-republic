# Corpus License Ledger — the legal spine

Scope: the material physically on disk (`corpus/library/` + `docs/ref/zai_docs_mirror`).
The full 33-material catalog with per-source verdicts lives in `corpus/CURRICULUM.md`
(scout, 2026-09-04); this ledger records the licenses of what is actually cloned, as read
from each repo's own LICENSE file at clone time. Law applied: weights-eligible IFF the
license is MIT, Apache, or CC-BY. Everything else is RAG/reference-only.

The operator will eventually FINE-TUNE on the eligible set. This file is the record of what
may lawfully enter that set. Update this file BEFORE any new source enters the corpus.

## Weights-eligible (may enter fine-tuning data)

| Source | Clone | License | Evidence |
|---|---|---|---|
| microsoft/ai-agents-for-beginners | `corpus/library/ms-agents-beginners/` | MIT (c) Microsoft Corporation | root LICENSE, read 2026-09-04 |
| microsoft/generative-ai-for-beginners | `corpus/library/ms-genai-beginners/` | MIT (c) Microsoft Corporation | root LICENSE, read 2026-09-04 |
| huggingface/agents-course | `corpus/library/hf-agents-course/` | Apache License 2.0 | root LICENSE, read 2026-09-04 |
| openai/openai-cookbook | `corpus/library/openai-cookbook/` | MIT (c) 2025 OpenAI | LICENSE at HEAD a78f3f3, read 2026-09-04 |

MIT/Apache obligations when redistributing or training: preserve copyright/license notices.
Keep each repo's LICENSE file with any extracted/processed derivative of its content.

## RAG-only (reference and retrieval use; NEVER into training data)

| Source | Location | License | Why excluded |
|---|---|---|---|
| anthropics/courses | `corpus/library/anthropic-courses/` | CC-BY-NC-4.0 | NonCommercial clause — commercial fine-tuning not licensed |
| z.ai docs mirror | `docs/ref/zai_docs_mirror/` | Proprietary vendor docs | Not ours to train on; includes vendor legal-agreement |

## Notes
- Licenses were read from each repo's own LICENSE file at clone time (see .corpus-meta.json
  per repo for the exact text pointer and clone timestamp). Re-verify upstream before any
  license-sensitive release built on this corpus.
- openai-cookbook working tree excludes `examples/data/hotel_invoices/` (31 sample-data files
  under an NTFS-invalid trailing-space directory path; excluded for filesystem reasons, not
  license reasons — full MIT content otherwise intact, 3133 files size-verified).
- Corpus total ~4.4GB on disk (~2.7GB working trees + .git promisor packs). Over the ~500MB
  clone budget; trim candidates (non-English translation dirs in the two Microsoft courses)
  are identified in CURRICULUM.md but not deleted without an operator GO.
