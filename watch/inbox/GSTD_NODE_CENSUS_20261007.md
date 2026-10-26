# GSTD NODE CENSUS RECEIPT (2026-10-07, lane gstd-mycelial-kickoff-20261007)

Purpose: byte bank for the P1 first-start ground truth appended to
docs/ref/GSTD_DOGFOOD_PLAN.md this day. Every number in that section cites
this file. One curl, as ordered; no container started at any point.

## 1. Clone state (probe + cure)

Command: git fetch origin main; git status -sb (run in reference/gstdcoin/gstdbot)

    ## main...origin/main [behind 160]

Cure: git merge --ff-only origin/main. Post-merge tip:

    e0bbe48 chore: add npm package for MCP Registry submission (gstd-network-mcp)

Remote: https://github.com/gstdcoin/gstdbot.git

## 2. Compose validation (no container started)

Command: docker compose config (run in reference/gstdcoin/gstdbot)
Docker: client=29.6.2 server=29.6.2. Exit code: 0.

Rendered facts quoted from output:

    memory: "536870912"
    reservations:
      memory: "134217728"
    ports:
      - mode: ingress
        target: 8080
        published: "8080"
        protocol: tcp

    healthcheck:
      test:
        - CMD
        - curl
        - -sf
        - http://localhost:8080/health
      interval: 30s
      start_period: 15s

    volumes:
      - type: volume
        source: gstd-data
        target: /data/gstdbot

## 3. Live node census (the one permitted curl)

Command:

    curl -s -m 20 -w "\nHTTP_STATUS=%{http_code}\n" "https://platform.gstdtoken.com/api/v1/nodes"

HTTP_STATUS=200. Body verbatim (one line, byte-copied from tool output):

{"nodes":[{"node_id":"d8edbeee-909a-49e5-908d-922b9bf98c43","name":"GSTD Bootstrap Pi","wallet_address":"UQB03R2DuNR9LKkW1AxbWUDsegAjxCRVwRimZlyNQX2Gc8ve","node_url":"https://sussex-picked-selection-judge.trycloudflare.com","version":"13 (trixie)","capabilities":["llama3.2:3b"],"tasks_completed":272,"gstd_earned":47.39141499999884,"last_seen":1791376427,"registered_at":1787950356,"reputation_score":55,"avg_response_ms":25138,"early_adopter":1},{"node_id":"node-LAPTOP-UTO92FB9","name":"LAPTOP-UTO92FB9-node","wallet_address":"UQD0gCwCSDTpuwxuENPuuiFhtp3DypGNe6gSLkUaYOzEU1KM","node_url":"","version":"3.4.0","capabilities":[],"tasks_completed":0,"gstd_earned":4.73463399999999,"last_seen":1791278734,"registered_at":1789714918,"reputation_score":20,"avg_response_ms":0,"early_adopter":1},{"node_id":"3e8398d6-57ab-47dc-83e8-4d0c523c592d","name":"unknown","wallet_address":"","node_url":"","version":"24.04.4 LTS (Noble Numbat)","capabilities":[],"tasks_completed":0,"gstd_earned":0,"last_seen":1791009845,"registered_at":1789458242,"reputation_score":0,"avg_response_ms":0,"early_adopter":1},{"node_id":"4d6f7704-d7a8-451d-88e0-afe87d51849b","name":"localhost-node","wallet_address":"UQDTMU95vkCrItikGVqnaxMB0SqNldAh65oFTCeRXMP3hAsH","node_url":"","version":"3.5.0","capabilities":["qwen2.5:7b"],"tasks_completed":0,"gstd_earned":0.3443589999999988,"last_seen":1789291425,"registered_at":1788324390,"reputation_score":25,"avg_response_ms":0,"early_adopter":1}],"count":4}

## 4. Epoch conversions (run on .venv python, datetime.fromtimestamp, UTC)

    pi              2026-10-07T12:33:47Z   (last_seen 1791376427)
    laptop          2026-10-06T09:25:34Z   (last_seen 1791278734)
    ubuntu-unknown  2026-10-03T06:44:05Z   (last_seen 1791009845)
    localhost       2026-09-13T09:23:45Z   (last_seen 1789291425)
    pi-registered   2026-08-28T20:52:36Z   (registered_at 1787950356)

## 5. Reading

count 4, unchanged from the 2026-09-29 research census
(watch/inbox/GSTD_RESEARCH_20260929/VERDICT.md named the same four shapes:
Pi, laptop hostname, localhost, and an Ubuntu box): falsifier 5 (swarm growth
beyond the household) has NOT fired. The Pi is the only live earner: 272
tasks completed, 47.39141499999884 gstd_earned, last seen today
2026-10-07T12:33:47Z. The localhost-node has been dark 24 days.
