---
name: events-key-schema-registry-20260927
description: B2-342 events key schema registry — 30 writer keys pinned with
  provenance, both gates armed (validate ERROR + fold WARN), two self-caught
  defects fixed pre-landing
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

B2-342 landed 9/26-27 — the events key schema registry makes the writer-key vocabulary load-bearing and self-enforcing. `configs/events_key_schema.json` (events_key_schema.v1) pins all 30 keys with census count, first-seen line/seq/ts, owning writer, carries-note. Both sides gate: `mag/shared_surface.py` validate names NEW never-seen keys as ERROR; the fold warns per distinct unknown key on exit-2 channel. 49 tests green across three suites; the falsifier ran both ways on throwaway bytes (fresh key caught by validate AND by fold). Key finding: the schema census is 30 keys over 3,481 parseable lines at recorded sha ab7f6cde. Self-caught defects fixed pre-landing: Set.size-vs-.length loader bug (gate was silently disabled) and shared_surface.py file-too-long (module extracted instead of debt registered). Related: [[b2-42-events-hygiene-20260926]], [[b2-329-dump-purity-law]].
