# FW-13 — hermes_wings/_ALL_WINGS.md: mag/docs wing annotations (2026-09-28)

- Ask: the wings file's 10 dead mag/docs paths → wing annotations.
- Dead set recomputed this session with the fixed instrument: **9 refs dead** (09-17 census
  said 10 — one was an artifact of the old regex; the fixed count is authoritative), of which
  **8 are `mag/docs/*`** and 1 is `memory/honcho/client.py` (a cross-repo tail of
  `hermes-agent/plugins/memory/honcho/client.py` — classified CROSS-REPO in FW-14's sample,
  not a wing annotation case).
- All 8 mag/docs paths have live twins at the repo root (each verified with exists() this
  session): ARCHITECTURE, BEHAVIORAL_ROUTER_INTERFACE, BOOT_DOC, BUILD_FOR_ZERO_BLUEPRINT,
  BUILD_LOG_2026-08-05_GROK_HANDOFF, CONTAINER, COORDINATION, DASHBOARD_REORIENTATION_V2 —
  `mag/docs/` was flattened into root `docs/`.
- Landed: a `> MOVED (FW-13 2026-09-28): …` annotation line under each wing entry — 7 after
  their `**/mag/docs/<NAME>.md**` path line, and the 8th (DASHBOARD_REORIENTATION_V2, whose
  entry carries only the quoted hermes complaint, no path line) directly under its
  `# docs/DASHBOARD_REORIENTATION_V2.md` wing header. `grep -c "MOVED (FW-13"` → 8.
  Annotations are additive; no wing text altered.
- The wings keep their original mag/docs citations as historical provenance — the annotation
  is the pointer, not a rewrite (never-rewrite law).
