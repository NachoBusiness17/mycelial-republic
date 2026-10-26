# swarm1-glm-flash-mag__arxiv_harvest (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: Mined hit ids come straight from LLM output and are never validated against the fresh id set, so fabricated/injected ids land in the research INBOX as unproven leads | EVIDENCE: mag/arxiv_harvest.py:144-151 | FIX: filter hits to ids present in {p["id"] for p in fresh} before writing the inbox file
DEFECT 2: _massage dedupes only against prior digest files, not within the current batch, so the same arXiv id listed under two categories (cs.AI/cs.CL overlap) appends duplicate digest rows and writes the same id.txt twice per run | EVIDENCE: mag/arxiv_harvest.py:104-113 | FIX: seed the seen set with ids already accumulated in the current papers batch before filtering fresh
DEFECT 3: DOCTYPE/ENTITY refusal scans only the first 200000 chars, so a document over 200k bytes with a late entity declaration passes the check into ET.fromstring | EVIDENCE: mag/arxiv_harvest.py:97-99 | FIX: run the doctype/entity check over the full decoded text, or reject any document whose first bytes lack a clean XML prolog
DEAD-CODE: startswith guard against the ATOM literal can never fire since url is built from the https ATOM constant two lines above | EVIDENCE: mag/arxiv_harvest.py:67-71
ONE-SITTING FIX: add the fresh-id membership check on mined hits before the inbox write, closing the untrusted-LLM-id path end to end | EVIDENCE: mag/arxiv_harvest.py:144-151

Falsifier: apply the one-sitting fix, feed flash_call output containing an id absent from fresh; the INBOX file must then contain no such id.
