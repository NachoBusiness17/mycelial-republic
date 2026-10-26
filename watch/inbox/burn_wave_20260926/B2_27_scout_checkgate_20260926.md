# B2-27 scout check-gate 2026-09-26

## Verdict

Landed. `python -m mag.link_library check` is now wired into the free-resource-scout filing path at three layers: the module spec (docstring law), the code (new `check_url()` gate, CLI `check` delegates to it, `add` stamps `duplicate_of` at submission), and the scout's actual firing config (memory/burns/MANIFEST.json free-resource-landscape topic pointer). Lived demo: both live `check` calls on real B2-06 dupe URLs answer known=true, exit 1. Note: the scout is an agent writer, not a script (no module, no schtasks entry); QUEUE.md:39 was pre-marked [x] with no receipt on disk (the B2-37 shape), so this receipt is the lane's first landing.

## Evidence

- `mag/link_library.py:168-169`: `if canon in known: entry["duplicate_of"] = known[canon].get("url", canon)` is the only place duplicate_of gets stamped, and only filers through `add_urls` reach it.
- `watch/inbox/LINKS.jsonl` (read 2026-09-26): writer free-resource-scout holds 46 rows (21 link-schema, 25 event-schema); all 21 link rows carry `duplicate_of: ""`, zero PENDING-URL (B2-26 backfilled shas today). Every scout link filing bypassed the gate; 4 were flagged only by B2-06's later triage rows (seq 1790422303798117..1790422309864941).
- B2-06 receipt (`B2_06_link_dupes_20260926.md:10`): "arxiv 2609.19107 re-filed 2026-09-18 with `"duplicate_of": ""` while the identical canonical existed since 09-17"; the 5 silent dupes are exactly scout re-confirmations.
- Live, this hour: `.venv/Scripts/python.exe -m mag.link_library check https://www.thundercompute.com/blog/free-cloud-gpu-credits` and `.../abs/2609.19107` both print `"known": true` with the first_entry block and exit 1.
- Scout has no driver: repo-wide grep for free-resource-scout in scripts/tools/mag/configs returns nothing; root schtasks inventory has no scout task (Estate Cooker 09:00 fires mag/cooker.py, whose ledger only logs stealth_sweep/task_wall/lite meter reads); DIRECTIVE_WATCHERS_20260926.md:14 classified it "by observed work".

## Work done

1. Spec before behavior: added the scout check-gate law to the `mag/link_library.py` docstring, citing B2-06; `add` is the only sanctioned filing door, `check` the read-only pre-flight.
2. Code: extracted `check_url(url)` (the canonical/known/first_entry verdict) as the shared library door; CLI `check` now delegates (single implementation, no behavior change).
3. Tests: 4 new tests pin the B2-06 shape (gate reports first_entry; unknown passes; scout re-confirmation carries duplicate_of in returned row AND ledger bytes; `add` CLI prints DUPLICATE). Suite: 30 passed (was 26).
4. Wired the firing config: MANIFEST.json free-resource-landscape topic gained the filing-law pointer (roundtrip-verified byte-identical formatting before edit).
5. Verified live gate against two real dupe URLs on the unmodified ledger (read-only).

## Falsifier

Verdict dies if: (a) the next scout fire re-files a known canonical with empty duplicate_of (grep new LINKS rows for writer free-resource-scout); (b) `pytest tests/test_link_library.py` goes red; (c) `add_urls` stops stamping duplicate_of; (d) MANIFEST topic pointer is reaped without a replacement carrier.

## Bibliography closed

Read in full: `mag/link_library.py`, `tests/test_link_library.py`, `mag/cooker.py`, `tools/stealth_sweep.py`, `scripts/endpoint_news.py` (filing grep), `tests/test_link_library.py` suite run. Read in part with line quotes: `watch/inbox/LINKS.jsonl` (writer/duplicate_of census via python), `B2_06_link_dupes_20260926.md`, `DIRECTIVE_WATCHERS_20260926.md`, `BURN_free-resource-landscape_20260926_e.md`, `QUEUE.md`, `scripts/register_endpoint_news_task.ps1`, `paste_pipeline.py` (grep), schtasks inventory + MANIFEST/BURN_WAVE_STATE mtimes. No web sources used. Nothing synthesized.
