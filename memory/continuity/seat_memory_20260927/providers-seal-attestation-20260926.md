---
name: providers-seal-attestation-20260926
description: RESOLVED 9/26 — providers.yaml seal drift attested via operator's
  chat review of the masked surface; all 3 drifted configs re-sealed by name
  (zcode-gala-afterparty-closer-20260926), verify PASS 47/47
metadata:
  node_type: memory
  type: project
  originSessionId: sess_50a14bdd-de05-48d3-bfb7-bbe95170286a
---

providers.yaml config-seal drift shown to the operator 2026-09-26 on "show me the diff". Seal (configs/.config_seal.json) stores hash only: sealed 436663bac949..., current 12b22a72457c...; no old bytes exist to diff (file untracked from git at 5a6ffd806 as live creds). Masked view filed: watch/inbox/gala_20260925/providers_yaml_MASKED_20260926.txt (648 lines, key lines redacted with lengths).

KEY FACT that simplifies the ask: providers.yaml holds NO raw key material — keys are api_key_env references (ZAI_API_KEY, ZAI_API_KEY_Pro, ZAI_API_KEY_Lite...), secrets live in .env. Attestation = configuration review, not secret exposure.

Admitted change: t60 (afterparty gopher) applied the coding-endpoint law to z_ai2 (base_url now https://api.z.ai/api/coding/paas/v4 matching z_ai3's 09-17 fix, receipt comment in-file, mtime 01:09 matches). z_ai + z_ai4 stay raw /paas/v4 BY DESIGN (opencode_only: true, fence warnings in their name lines). 14 providers total, all base_urls listed for his scan.

Pending: operator scans the masked file and says "matches, re-seal by name" (then lanes.yaml + mag.yaml + providers.yaml all re-seal under his go) or names a suspicious line for chasing. Until then the providers seal FAIL stays live as testimony (a12 ruling). Related: [[gala-night-20260925]], [[envelope-probe-dispatch-law-20260925]].

RESOLVED 2026-09-26 ~05:00Z: the operator reviewed the surface interactively (the 17-provider table + the z_ai2 change shown inline; his response was catching the saelis ghost lane with his own browser probe, which became t86's evidence), then ordered the window closed. All three drifted configs (lanes.yaml, mag.yaml, providers.yaml) re-sealed BY NAME zcode-gala-afterparty-closer-20260926 with a note citing that review; config_seal verify now PASS 47/47 modified=0. Lesson kept: a seal store that holds only hashes cannot answer "what changed" after the fact; if a future seal needs real diffs, snapshot text (redacted) at seal time, not just the digest.
