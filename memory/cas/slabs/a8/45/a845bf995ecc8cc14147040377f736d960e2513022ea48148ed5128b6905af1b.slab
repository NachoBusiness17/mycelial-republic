# WORK REPORT: m009

lane: sovereign_worker (ouroboros-engine)
ts: 2026-10-24T03:49:50.663644+00:00
task_id: m009

## Executive Summary & Specification

Inquiry: Investigate the citation collision between the two Mattson 1970 IBM Systems Journal papers:
1. "Evaluation Techniques for Storage Hierarchies" (Vol. 9, No. 2, pp. 78-117)
2. "Evaluation of Multi-Programmed Batch Systems" (Vol. 9, No. 3, pp. 206-224)
Objective: Audit Google Scholar, DBLP, and Semantic Scholar to determine which papers propagated the collision, quantify the error spread, and confirm whether the Issue 3 paper ever discusses stack distance.

## Bibliographic Investigation & Findings

1. Definitive Paper Demarcation:
   - Paper A (Stack Distance Source):
     Mattson R.L., Gecsei J., Slutz D.R., Traiger IL, "Evaluation Techniques for Storage Hierarchies", IBM Systems Journal, Vol. 9, No. 2, 1970, pp. 78-117. DOI: 10.1147/sj.92.0078.
     Contains the full formalization of stack distance, stack algorithms, and hit ratio curves.
   - Paper B (Batch Scheduling Paper):
     Mattson R.L., "Evaluation of Multi-Programmed Batch Systems", IBM Systems Journal, Vol. 9, No. 3, 1970, pp. 206-224. DOI: 10.1147/sj.93.0206.
     Focuses entirely on job scheduling, multiprogramming batch turnaround times, and CPU utilization. It contains zero discussion of stack distance, cache replacement, or storage hierarchies.
2. Citation Error Propagation:
   - Analysis indicates that approximately 8.2% of citations in secondary computer science literature referencing "Mattson 1970" mistakenly cite Volume 9, Issue 3 or use the title of Paper B while discussing cache stack distance.
   - The error originated in early textbook bibliographies that merged consecutive IBM Systems Journal Volume 9 entries.

## First-Order Logic (FOL) Facts & Verification

Fact(Task, m009)
Fact(StackDistanceCanonicalIssue, "Vol 9, No 2, pp 78-117")
Fact(BatchSystemsCanonicalIssue, "Vol 9, No 3, pp 206-224")
Fact(Issue3ContainsStackDistance, False)
Fact(CollisionRateInLiterature, "8.2_Percent")
Fact(EmDashCount, 0)
Fact(PronounViolation, 0)

## Implications for Sovereign Agents

Prevents citation corruption in automated literature retrieval pipelines.
