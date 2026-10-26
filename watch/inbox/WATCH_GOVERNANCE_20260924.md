# WATCH GOVERNANCE — full inventory + how watch/ exists moving forward
2026-09-24 00:xx UTC · scope: watch/ and watch/inbox, project folders only

## The inventory (measured, not guessed)
- **16,349 files · 5.6 GB** · oldest 2016-10-29 · newest today
- **By directory**: inbox 9,000 · organs 2,327 · .mimosa 1,563 · march 1,329 · root 1,131 · hermes_wings 176 · sea 90 · astra_hold0 84
- **By type**: 5,828 PNG · 2,396 MD · 2,115 JPG · 1,881 JSON · 1,550 .source · 403 MP4 (3.48 GB) · 303 CPP · 187 CU · 221 TXT · 172 JSONL
- **The heavy tail**: ESTATE_INDEX.jsonl 395 MB (grows every spine run) · engine_e1.log 258 MB · overnight_churn.log 133 MB · mrpool_export media MP4s 95–137 MB each

## The four diseases
1. **Media lives among records.** 3.48 GB of MP4 + 0.9 GB of images sit in the text-record tree. They are evidence *attached to* records, not records.
2. **Logs grow unbounded.** A 258 MB engine log and a 133 MB churn log are unreadable and unsearchable in place. Logs are process exhaust, not records.
3. **The master index is a monolith.** ESTATE_INDEX.jsonl at 395 MB gets rewritten by every spine run and grows forever.
4. **Code lives in the watchtower.** 303 .cpp + 187 .cu files are source code, not watch records.

## How watch/ exists moving forward (the law)
1. **inbox/ = intake, append-only, dated.** New records land here with a date in the name. Nothing is ever edited in place; corrections append.
2. **Promotion, not duplication.** A record that becomes canon/law moves to corpus/canon/ or docs/ref/ with a pointer left behind (one line: "promoted to X on date"). The inbox shrinks by graduation, never by deletion.
3. **Media referenced, not embedded.** Images/video live under watch/assets/ (or corpus/assets for permanent evidence); records link to them by relative path. The text tree stays text.
4. **Logs rotate.** Any log over 50 MB rotates: keep the last N MB + a .gz of the rest. The wall report reads the tail; the archive keeps the history.
5. **The index rolls.** ESTATE_INDEX.jsonl compacts monthly: current month live, prior months to .gz rollups. rollup.json stays the query surface.
6. **Code goes home.** .cpp/.cu/.py sources move to corpus/library/ or src/ — the watchtower watches, it doesn't store toolchains.
7. **Everything above applies going forward.** Nothing is deleted retroactively — the 2016 file is a record too.

## The GPU (answered live)
Idle. Nothing local is running. Driver update pending = the night lane's speed unlock (5600 XT, Vulkan-capable, driver too old for ollama's GPU path).
