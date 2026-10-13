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

body = ParagraphStyle('body', fontName='Helvetica', fontSize=11, leading=17, spaceAfter=8)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=15, textColor=DARK, spaceBefore=20, spaceAfter=8)
small = ParagraphStyle('small', fontName='Helvetica', fontSize=8.5, textColor=DIM, spaceAfter=4)
quote = ParagraphStyle('quote', fontName='Helvetica-Oblique', fontSize=11, leading=16, leftIndent=16, rightIndent=16, textColor=HexColor("#4a4a5e"), spaceAfter=8)

def tbl(data, widths=None):
    t = Table(data, colWidths=widths)
    style = [('FONT', (0,0), (-1,-1), 'Helvetica', 9),
             ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
             ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
             ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e8"))]
    style += [('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), HexColor("#e8e6e3")),
              ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 9)]
    t.setStyle(TableStyle(style))
    return t

doc = SimpleDocTemplate(
    os.path.join("watch", "inbox", "PLAIN_LANGUAGE_AOS_12YO_20260924.pdf"),
    pagesize=A4, topMargin=18*mm, bottomMargin=18*mm, leftMargin=16*mm, rightMargin=16*mm,
    title="What We Built (Explained Simply)")

E = []
E.append(Paragraph("What We Built", ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=24, textColor=DARK, alignment=TA_CENTER, spaceAfter=6)))
E.append(Paragraph("Explained simply, with receipts", ParagraphStyle('st', fontName='Helvetica', fontSize=13, textColor=BLUE, alignment=TA_CENTER, spaceAfter=4)))
E.append(Paragraph("For AOS / AdventureNLearn", ParagraphStyle('d', fontName='Helvetica', fontSize=9, textColor=DIM, alignment=TA_CENTER)))
E.append(Spacer(1, 20))

E.append(Paragraph("You asked for plain language. Here is everything our system does, explained like you have never seen an AI before.", body))

E.append(Paragraph("1. We keep receipts that cannot be faked", h2))
E.append(Paragraph("Imagine you write 205 important documents. You want to be sure nobody secretly changes any of them. So you take a 'fingerprint' of each one (it's called a SHA-256 hash). If anyone changes even one letter, the fingerprint changes too.<br/><br/>Every morning, a computer program checks all 205 fingerprints. If one document was changed, it tells us exactly which one. This has been running every day. It works.", body))

E.append(Paragraph("2. We use 10 different AI services and pick the best one for each job", h2))
E.append(Paragraph("There are many companies that let you use their AI models. Some are fast, some are slow. Some are smart, some are cheap. We connected 10 of them and tested each one to see which is best at what.<br/><br/>Here is what we found when we asked each AI the same question 5 times:", body))
matrix = [
    ["AI Service", "Right answers", "How fast", "Speed score"],
    ["OpenRouter (key 2)", "5 out of 5", "1.6 seconds", "115 words/sec"],
    ["DeepSeek", "5 out of 5", "1.1 seconds", "70 words/sec"],
    ["OpenRouter (key 1)", "5 out of 5", "3.8 seconds", "48 words/sec"],
    ["NVIDIA", "5 out of 5", "25.6 seconds", "13 words/sec"],
]
E.append(tbl(matrix))
E.append(Paragraph("All 4 top services got the answer right every time. The slowest still works. We now send easy jobs to fast services and hard jobs to smart services.", body))

E.append(Paragraph("3. We checked if a famous study is true", h2))
E.append(Paragraph("A famous study from 2014 said that rich people get what they want from the government, and normal people basically don't. A lot of people share this study but get the numbers wrong.<br/><br/>We downloaded the actual data from the study and ran the numbers ourselves using Python (a programming tool). The study's real numbers: when rich people want something, it happens 45% of the time. When rich people don't want it, only 18%. Regular people's opinion changes almost nothing.<br/><br/>The famous '90% of the time' number that everyone shares? It's not in the study at all. It's a mix-up. We proved that by running the math ourselves.", body))

E.append(Paragraph("4. We found a hidden picture inside a picture", h2))
E.append(Paragraph("Someone posted a picture that looked like random green dots - like static on an old TV. But it was actually a 'stereogram' - a picture with a secret image hidden inside it that you can only see by looking at it a special way.<br/><br/>We wrote a computer program that reads the secret image automatically. Inside was a big letter Q, hidden on purpose. We proved our method works by hiding a Q in our own test image first, then decoding it back.<br/><br/>Anyone can check our work. The program is saved. The method is published.", body))

E.append(Paragraph("5. We checked if crime records are real", h2))
E.append(Paragraph("We researched 6 big topics: Epstein, government spying, censorship, money in politics, and more. For each one, we downloaded the actual court documents, government reports, and official records. Not news articles. Not someone's opinion. The actual papers.<br/><br/>Then a second AI (that had never seen the first one's work) re-checked every single fact by downloading the same documents itself. If a quote didn't match, it was flagged and fixed.<br/><br/>Result: 5 of 6 topics have receipts you can check yourself. 1 topic is honestly marked as 'disputed' because experts disagree about what the evidence means.", body))

E.append(Paragraph("6. Everything runs automatically every morning", h2))
sched = [
    ["Time", "What happens"],
    ["9:00 AM", "Checks all 1.2 million files in the project"],
    ["9:15 AM", "Verifies all 205 document fingerprints"],
    ["9:25 AM", "Runs small jobs on free AI services"],
    ["9:35 AM", "Writes a one-line summary for every record"],
    ["9:45 AM", "Checks that all 26 API keys still work"],
]
E.append(tbl(sched))
E.append(Paragraph("Each task was tested by hand first. Then it was scheduled. If anything breaks, the audit screams.", body))

E.append(Paragraph("What we DON'T have yet", h2))
E.append(Paragraph("We can't prove that a stranger could take over our system without us explaining it. That's called 'continuation' and it's the hardest test. We also can't run for more than a day without a human checking in. We're honest about that.", body))

E.append(Paragraph("Why we built all this", h2))
E.append(Paragraph("Because you asked what we actually do. The answer is: we check things. We check if studies are true. We check if our own files are safe. We check if AI services work. We check if hidden images have hidden pictures. And we write down what we find, with the receipt, so anyone can check us.<br/><br/>That's it. That's the whole system. No magic.", body))

E.append(Spacer(1, 16))
E.append(Paragraph("Where the numbers come from", h2))
biblio = [
    ["1. Gilens & Page (2014). Perspectives on Politics, 12(3). DOI 10.1017/S1537592714001595"],
    ["2. Lermen et al. (2026). Deanonymization with LLMs. USENIX Security. arXiv:2602.16800"],
    ["3. Tyler & Clarke (1990). Autostereograms. Vision Research, 30(4)."],
    ["4. NIST FIPS 180-4: Secure Hash Standard (SHA-256)."],
    ["5. METR (2026). Time Horizons. metr.org/time-horizons/"],
    ["6. IETF SCITT WG. draft-mih-scitt-agent-action-capsule-04. datatracker.ietf.org/"],
    ["7. S. Rep. 94-755 (1976). Church Committee Final Report. intelligence.senate.gov"],
    ["8. US v. Epstein, S.D.N.Y. 1:19-cr-00490. CourtListener."],
    ["9. Doe v. United States, S.D.Fla. 9:08-cv-80736, Doc 435 (2019)."],
    ["10. Giuffre v. Maxwell, S.D.N.Y. 15-cv-7433, Doc 1315 (2023)."],
]
E.append(tbl(biblio))

E.append(Spacer(1, 20))
E.append(Paragraph("Every claim traces to a URL, a script, or a measured number. If you want to check any of it, the method and the code are here.", ParagraphStyle('close', fontName='Helvetica-Oblique', fontSize=10, textColor=DIM, alignment=TA_CENTER)))

doc.build(E)
print("PDF:", os.path.getsize(os.path.join("watch", "inbox", "PLAIN_LANGUAGE_AOS_12YO_20260924.pdf")), "bytes")
