---
name: late-burn-engineering-cluster-20260927
description: 9/27 late-burn engineering cluster — behavioral scout census
  replaces substring math, crash stanza pin from single regex import, chain
  census 0 on real bytes, resolver getaddrinfo 2s bound, base_url locality
  sweep, pointer-anchor law, events key schema registry 30 keys
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

9/27 late-burn engineering cluster (B2-357, B2-372, B2-373, B2-383, B2-384, B2-489, B2-490, B2-491, B2-342):

**Behavioral scout census** (B2-374): `behavioral_events_census()` replaces substring counting in behavioral-events block; kind field only counts, detail never counts even when quoting a literal; non-dict JSON row was silently dropping the whole block.

**Crash stanza pin** (B2-373): `_CRASH_STANZA_RE` imported from mag.improve into the writer's test so reader and writer cannot drift; brief's falsifier was wrong (nothing went red pre-pin) but the real hole was worse: census silently collapsed a 2-crash log to 1.

**Chain census** (B2-372/383/384): chains=N named in row detail; quoted chain-marker sentences hardened with column-anchored regex + structural 2-header rule; **52 real crashes count zero chains**, only synthetic fixtures exercise the chains feature.

**Resolver bound** (B2-489): `_host_resolves` getaddrinfo runs on 2.0s daemon thread; blackhole DNS can't hold the doctor hostage; falsifier reproduced 30s stall pre-fix, bounded post-fix.

**base_url locality sweep** (B2-490): OLLAMA_HOST trap is tri-scope (host/compose/k8s); SAELIS_BASE_URL dormant short-circuits every doctor branch; VAST_OPENAI_BASE_URL wrong-scope name reads REMOTE-UNVERIFIED.

**Pointer-anchor law** (B2-491): every NEW file:line pointer in a burn brief carries a byte anchor `path:NN#token`; `tools/pointer_rot_check.py` names rotted pointers; born from two same-day pointer rots.

**Events key schema registry** (B2-342): 30 writer keys pinned in configs/events_key_schema.json with both gates armed (validate ERROR on new key, fold WARN); both falsifiers executed on real bytes.
