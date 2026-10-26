from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER
import os

DARK = HexColor("#1a1a2e")
BLUE = HexColor("#1565c0")
DIM = HexColor("#6b7280")
ACCENT = HexColor("#0d213f")

body = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=15, spaceAfter=6)
code = ParagraphStyle('code', fontName='Courier', fontSize=8, leading=11, textColor=HexColor("#1e293b"), backColor=HexColor("#f1f5f9"), borderPadding=6, leftIndent=10, rightIndent=10, spaceAfter=8)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=15, textColor=DARK, spaceBefore=20, spaceAfter=8)
h3 = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=12, textColor=ACCENT, spaceBefore=12, spaceAfter=4)
small = ParagraphStyle('small', fontName='Helvetica', fontSize=8.5, textColor=DIM, spaceAfter=4)

def tbl(data, widths=None):
    t = Table(data, colWidths=widths)
    style = [('FONT', (0,0), (-1,-1), 'Helvetica', 8.5),
             ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
             ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
             ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e8"))]
    style += [('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), HexColor("#e8e6e3")),
              ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8.5)]
    t.setStyle(TableStyle(style))
    return t

doc = SimpleDocTemplate(
    os.path.join("watch", "inbox", "PLAIN_LANGUAGE_FOR_AOS_20260924.pdf"),
    pagesize=A4, topMargin=18*mm, bottomMargin=18*mm, leftMargin=15*mm, rightMargin=15*mm,
    title="The Mag Estate - Plain Language Technical Summary")

E = []
E.append(Paragraph("The Mag Estate", ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=22, textColor=DARK, alignment=TA_CENTER, spaceAfter=4)))
E.append(Paragraph("Plain Language Technical Summary", ParagraphStyle('st', fontName='Helvetica', fontSize=13, textColor=BLUE, alignment=TA_CENTER, spaceAfter=4)))
E.append(Paragraph("For AOS / AdventureNLearn · 2026-09-24", ParagraphStyle('d', fontName='Helvetica', fontSize=9, textColor=DIM, alignment=TA_CENTER)))
E.append(Spacer(1, 16))

E.append(Paragraph("What this system is", h2))
E.append(Paragraph("A local AI operations platform running on a single Windows PC. No cloud dependency. Every component is locally hosted, locally verified, and locally recoverable.", body))

E.append(Paragraph("1. Canon Verification", h2))
E.append(Paragraph("205 files in the canon. A SHA-256 manifest covers every file. A Python script recomputes all 205 hashes every morning. If any file changed, the audit reports which one and what the expected vs actual hash is.", body))
E.append(Paragraph("import hashlib<br/>from pathlib import Path<br/>canon = Path('corpus/canon')<br/>for line in (canon / 'MANIFEST.sha256').read_text().splitlines():<br/>&nbsp;&nbsp;parts = line.split(None, 1)<br/>&nbsp;&nbsp;want, rel = parts[0], parts[1].strip().lstrip('*')<br/>&nbsp;&nbsp;fp = canon / rel<br/>&nbsp;&nbsp;if fp.is_file():<br/>&nbsp;&nbsp;&nbsp;&nbsp;h = hashlib.sha256(fp.read_bytes()).hexdigest()<br/>&nbsp;&nbsp;&nbsp;&nbsp;if h != want: print(f'DRIFT: {rel}')", code))
E.append(Paragraph("SHA-256 is NIST FIPS 180-4. The manifest pattern is content-addressable storage, identical to Git's internal object model.", small))

E.append(Paragraph("2. Key Management", h2))
E.append(Paragraph("26 API keys across 14 providers, declared in one JSON manifest (configs/keys.json), loaded through one function (mag/key_law.py). The audit checks that every registered lane points at a key that actually exists.", body))
E.append(Paragraph("Why: the NVIDIA lane was down for weeks because three files referenced the same key under three different names. No reader agreed on the name.", small))

E.append(Paragraph("3. Multi-Lane Model Routing", h2))
E.append(Paragraph("10 API providers plus local Ollama. Each lane is measured for ok-rate, latency, tokens/second, and correctness.", body))
E.append(Spacer(1, 6))
matrix = [
    ["Lane", "OK", "Correct", "Latency", "tok/s", "Verdict"],
    ["OpenRouter key 2", "5/5", "5/5", "1.6s", "114.9", "carry"],
    ["DeepSeek chat", "5/5", "5/5", "1.1s", "70.4", "carry"],
    ["OpenRouter key 1", "5/5", "5/5", "3.8s", "48.1", "carry"],
    ["NVIDIA glm-5.3-flash", "5/5", "5/5", "25.6s", "12.8", "carry"],
    ["Groq (both keys)", "0/10", "0/10", "-", "-", "cut"],
    ["Together", "5/5", "0/5", "-", "-", "cut"],
    ["Nous Hermes-4-70b", "5/5", "0/5", "-", "-", "cut"],
]
E.append(tbl(matrix))
E.append(Paragraph("Correct = the model cited 1976 for the Church Committee final report. Every failure has a named cause.", small))

E.append(Paragraph("4. Concurrent Task Execution", h2))
E.append(Paragraph("A task wall queues real backlog chores and dispatches them across all lanes with ramping concurrency. Each lane starts at 1, ramps every 8 successful calls, backs off on 429/quota. 47 chores completed across 4 runs. Chores are real: label extraction, anchor notes, gap questions. Output lands in append-only JSONL ledgers.", body))

E.append(Paragraph("5. Evidence Verification Pipeline", h2))
E.append(Paragraph("Six evidence families. Each verified by a two-pass process: a digger agent fetches primary sources and extracts verbatim quotes; an independent stranger agent re-fetches the URLs and checks every quote character-by-character.", body))
E.append(Paragraph("Example - the Gilens & Page falsifier: downloaded the authors' replication file (4.4MB) from Cambridge Core, recomputed with pandas. N=1,779, overall adoption 33.05%, matching the paper. The popular '90% of the time elites win' claim appears nowhere in the paper. The 89.6% figure is the agreement share, not a capture rate.", body))

E.append(Paragraph("6. Stereogram Decoding", h2))
E.append(Paragraph("A single-image autostereogram decoded using per-pixel shift correlation: for each 16x16 block, find which horizontal displacement produces the best match. The winning displacement per block forms a depth map. Result: a letter Q recovered from a 682KB image. Validated by round trip: encode a Q, decode a Q, same Q.", body))
E.append(Paragraph("Pure NumPy + PIL. No ML model. No API call.", small))

E.append(Paragraph("7. Scheduled Operations", h2))
sched = [
    ["Time", "Task", "What it does"],
    ["09:00", "Estate Spine Index", "Walks every project file (1.2M files)"],
    ["09:15", "Estate Librarian", "Shelf catalog + canon hash verification (205/205)"],
    ["09:25", "Estate Gopher", "Label-farm chores on idle API keys"],
    ["09:35", "Estate FullScan", "Semantic catalog: one-line brief per record"],
    ["09:45", "Estate KeyAudit", "Key law audit: every lane resolves or fails"],
]
E.append(tbl(sched))
E.append(Paragraph("Each was fired manually at least once before being trusted to the scheduler.", small))

E.append(Paragraph("What this system does NOT have", h2))
E.append(Paragraph("G7: a stranger-continuation test that passes without the original operator. Multi-day autonomous operation without human intervention. A formal succession plan tested by someone other than the operator. These are the same gaps.", body))

E.append(Paragraph("Bibliography", h2))
biblio = [
    [u"1. Gilens & Page (2014). Perspectives on Politics, 12(3), 564-581. DOI 10.1017/S1537592714001595"],
    [u"2. Lermen et al. (2026). Large-scale deanonymization with LLMs. USENIX Security 2026. arXiv:2602.16800"],
    [u"3. Tyler & Clarke (1990). Autostereograms. Vision Research, 30(4)."],
    [u"4. NIST FIPS 180-4: Secure Hash Standard (SHA-256)."],
    [u"5. METR (2026). Time Horizons. metr.org/time-horizons/"],
    [u"6. IETF SCITT WG. draft-mih-scitt-agent-action-capsule-04. datatracker.ietf.org/"],
    [u"7. Senate Select Committee on Intelligence (1976). S. Rep. 94-755."],
    [u"8. United States v. Epstein, S.D.N.Y. 1:19-cr-00490. CourtListener RECAP."],
    [u"9. Doe v. United States, S.D. Fla. 9:08-cv-80736, Doc 435 (Marra, J., 2019)."],
    [u"10. Giuffre v. Maxwell, S.D.N.Y. 15 Civ. 7433, Doc 1315 (Preska, J., 2023)."],
]
E.append(tbl(biblio))

E.append(Spacer(1, 20))
E.append(Paragraph("Every claim above traces to a fetched URL, a run script, or a measured output. The metaphors are stripped. The numbers are the numbers.", ParagraphStyle('close', fontName='Helvetica-Oblique', fontSize=10, textColor=DIM, alignment=TA_CENTER)))

doc.build(E)
print("PDF:", os.path.getsize(os.path.join("watch", "inbox", "PLAIN_LANGUAGE_FOR_AOS_20260924.pdf")), "bytes")
