# B2-15 x-intel dig: append verified-source rows to watch/inbox/LINKS.jsonl
# All rows fetched and quoted live 2026-09-26 by lane B2-15. No synthesized sources.
import json
from datetime import datetime, timezone

TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
W = "x-intel-dig"

rows = [
    {
        "ts": TS, "writer": W, "id": "XIDIG-SWARM-AWS-JITTER", "kind": "finding",
        "title": "AWS builders library: no-jitter exponential backoff is the loser under contention; full jitter cuts call count by more than half with 100 contending clients",
        "detail": "Direct quotes verified live: 'The solution isn't to remove backoff. It's to add jitter.'; 'In the case with 100 contending clients, we've reduced our call count by more than half.'; 'With N clients contending, the total amount of work done by the system increases with N2.'; guidance: jittered backoff 'should be considered a standard approach for remote clients'. Feeds union driver v2 (gap-analysis row: swarm/orchestration, 4 rows)",
        "sources": ["https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-SWARM-SRE-RETRY-BUDGET", "kind": "finding",
        "title": "Google SRE Addressing Cascading Failures: 'Always use randomized exponential backoff'; retry budget (e.g. 60 retries/min/process) turns capacity failure into dropped queries instead of global cascade",
        "detail": "Direct quotes verified live: 'Limit retries per request. Don't retry a given request indefinitely.'; 'Consider having a server-wide retry budget. For example, only allow 60 retries per minute in a process'; 'Don't retry permanent errors or malformed requests in a client, because neither will ever succeed.'; layered retries multiply: attempts 'as large as the product of the number of attempts at each layer'",
        "sources": ["https://sre.google/sre-book/addressing-cascading-failures/"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-SWARM-CIRCUIT-BREAKER", "kind": "finding",
        "title": "Azure Architecture Center circuit breaker: closed/open/half-open state machine, half-open prevents flooding a recovering service; retry and breaker are distinct purposes",
        "detail": "Direct quotes verified live: 'The Retry pattern enables an application to retry an operation with the expectation that it eventually succeeds. The Circuit Breaker pattern prevents an application from performing an operation that's likely to fail.'; 'The Half-Open state helps prevent a recovering service from suddenly being flooded with requests.'; HTTP 429/503 responses can carry the anticipated delay (accelerated circuit breaking)",
        "sources": ["https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-SWARM-TOKEN-COST", "kind": "finding",
        "title": "Vercel six agent orchestration patterns: multi-agent uses up to 15x token volume of chat; fan-out and orchestrator-worker are the high-cost rows; single-agent matches multi-agent accuracy under equal compute",
        "detail": "Direct quotes verified live: 'Multi-agent systems can use up to 15x the token volume of standard chats, so task value has to justify the added complexity.'; 'Under equal compute budgets, single-agent loops match or exceed multi-agent accuracy on multi-hop reasoning tasks across Qwen3, DeepSeek-R1, and Gemini 2.5.'; parallelization/fan-out cost 'High, varies with fan-out'; 'At 95% per-step accuracy across ten steps, end-to-end accuracy is about 60%, and at 90% it is about 35%.'",
        "sources": ["https://vercel.com/i/agent-orchestration-patterns"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-SWARM-ANTHROPIC-15X", "kind": "finding",
        "title": "Anthropic multi-agent research system (origin of the 15x figure): 'agents typically use about 4x more tokens than chat interactions', 'multi-agent systems use about 15x more tokens than chats'; multi-agent beat single-agent Opus 4 by 90.2%",
        "detail": "Direct quotes verified live: 'outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval'; 'These changes cut research time by up to 90% for complex queries' (parallel tool calling); 'One step failing can cause agents to explore entirely different trajectories'; no numeric coordination-failure rates given (qualitative only)",
        "sources": ["https://www.anthropic.com/engineering/built-multi-agent-research-system"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-SWARM-DENOMINATOR-DRIFT", "kind": "ALERT", "severity": "process-debt",
        "title": "Gap-analysis seed denominator drifted: RESEARCH_GAP_ANALYSIS_20260918.md says union driver '143 attempts/88.8% ok' but watch/inbox/union_fullsend_20260917/raw.jsonl counted 2026-09-26 holds 184 attempt rows with 156 ok (84.8%)",
        "detail": "Recounted from bytes this lane: len(rows)=184, ok-true=156, 156/184=0.8478. The file grew after the 09-18 analysis; every gap-row denominator should be re-derived from ledger bytes before driver v2 work uses it (trust bytes, not reports)",
        "sources": ["watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md", "watch/inbox/union_fullsend_20260917/raw.jsonl"],
        "flag": "process-debt",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-WIN-REPARSE-LAW", "kind": "finding",
        "title": "Microsoft Learn reparse points: reparse data+tag max 16KB, limit of 63 reparse points per path (31 if fully qualified target), directory must be empty to take a reparse point",
        "detail": "Direct quotes verified live: 'A file or directory can contain a reparse point, which is a collection of user-defined data.'; 'Reparse point data, including the tag and optional GUID, cannot exceed 16 kilobytes.'; 'There is a limit of 63 reparse points on any given path.'; 'the limit becomes 31' for fully qualified targets; 'Reparse points can be established for a directory, but the directory must be empty.' Feeds catalog v3 junction policy (gap-analysis row: windows/storage, 4 rows)",
        "sources": ["https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-WIN-JUNCTION-RULES", "kind": "finding",
        "title": "Microsoft Learn hard links and junctions: junctions link directories only, may cross local volumes, and may NOT target mapped network volumes or files; junctions are implemented through reparse points",
        "detail": "Direct quotes verified live: 'A junction (also called a soft link) differs from a hard link in that the storage objects it references are separate directories. A junction can also link directories located on different local volumes on the same computer.'; permitted examples C:\\dirx -> D:\\diry; not permitted 'because they reference mapped network volumes, or they directly reference files'; 'Junctions are implemented through reparse points.' Catalog v3 mirror-vs-duplicate test needs this rule: a junction to another local volume is NOT a network share and is NOT a duplicate file",
        "sources": ["https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-WIN-SYMLINK-RULES", "kind": "finding",
        "title": "Microsoft Learn creating symbolic links: symlinks may be absolute or relative, may target UNC remote paths directly, relative symlinks restricted to a single volume",
        "detail": "Direct quotes verified live: 'Symbolic links can point directly to a remote file or directory using the UNC path.'; 'Relative symbolic links are restricted to a single volume.'; 'A symbolic link can also contain both junction points and mounted folders as a part of the path name.' Contrast rule for the junction policy: UNC target implies symlink not junction",
        "sources": ["https://learn.microsoft.com/en-us/windows/win32/fileio/creating-symbolic-links"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-WIN-MFT-ENUM", "kind": "finding",
        "title": "Microsoft Learn FSCTL_ENUM_USN_DATA: MFT-record enumeration for full-volume listings; FSCTL_READ_USN_JOURNAL for selecting recent changes by USN",
        "detail": "Direct quotes verified live: 'Enumerates the update sequence number (USN) data between two specified boundaries to obtain master file table (MFT) records.'; 'To enumerate files on a volume, use the FSCTL_ENUM_USN_DATA operation one or more times.'; start at StartFileReferenceNumber 0, each call returns the next starting point; volume 'must be NTFS'; SMB 3.0: No (local-volume technique). This is the MFT-style enumeration path the 09-18 gap row names for catalog v3 fast refresh",
        "sources": ["https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_enum_usn_data"],
        "flag": "verified-live",
    },
    {
        "ts": TS, "writer": W, "id": "XIDIG-WIN-USN-REFRESH", "kind": "finding",
        "title": "Microsoft Learn FSCTL_READ_USN_JOURNAL: change-journal reads between two USNs give the incremental-refresh path; enum for listings, journal for deltas",
        "detail": "Direct quotes verified live: 'Retrieves the set of update sequence number (USN) change journal records between two specified USN values.'; 'Use the latter when you want a listing (enumeration) of the USN records between two USNs. Use the former when you want to select by USN.' (former = READ_USN_JOURNAL, latter = ENUM_USN_DATA); Walking a Buffer of Change Journal Records is the documented example pattern. Catalog v3 design split: full walk via ENUM once, then journal deltas for fast refresh",
        "sources": ["https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_read_usn_journal"],
        "flag": "verified-live",
    },
]

path = "watch/inbox/LINKS.jsonl"
with open(path, "a", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=True) + "\n")
print("appended", len(rows), "rows to", path)
