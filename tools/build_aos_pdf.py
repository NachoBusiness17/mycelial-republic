from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.utils import ImageReader
import os

DARK = HexColor("#1a1a2e")
DARK_BG = HexColor("#0d0d0f")
ACCENT = HexColor("#961885")
GOLD = HexColor("#f9a825")
BLUE = HexColor("#4fc3f7")
DIM = HexColor("#8a8782")
WHITE = HexColor("#e8e6e3")

# Dark background page template
def dark_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.restoreState()

def light_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(HexColor("#ffffff"))
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    # accent bar at top
    canvas.setFillColor(ACCENT)
    canvas.rect(0, A4[1] - 8*mm, A4[0], 3*mm, fill=1, stroke=0)
    canvas.restoreState()

styles = getSampleStyleSheet()
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=16, textColor=DARK, spaceBefore=18, spaceAfter=8)
h2w = ParagraphStyle('h2w', fontName='Helvetica-Bold', fontSize=16, textColor=WHITE, spaceBefore=18, spaceAfter=8)
h3 = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=13, textColor=HexColor("#0d213f"), spaceBefore=12, spaceAfter=6)
body = ParagraphStyle('body', fontName='Helvetica', fontSize=10.5, leading=16, spaceAfter=6)
bodyw = ParagraphStyle('bodyw', fontName='Helvetica', fontSize=10.5, leading=16, spaceAfter=6, textColor=WHITE)
small = ParagraphStyle('small', fontName='Helvetica', fontSize=9, textColor=DIM, spaceAfter=4)

def tbl(data):
    t = Table(data)
    style = [('FONT', (0,0), (-1,-1), 'Helvetica', 9),
             ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
             ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
             ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e8"))]
    style += [('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
              ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 9)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0,i), (-1,i), HexColor("#f8f9fe")))
    t.setStyle(TableStyle(style))
    return t

doc = SimpleDocTemplate(
    os.path.join("watch", "inbox", "AOS_CANDY_PDF_20260924.pdf"),
    pagesize=A4, topMargin=20*mm, bottomMargin=20*mm,
    leftMargin=18*mm, rightMargin=18*mm,
    title="The AOS Correspondence — Full Inter-Agency Arc")

E = []

# ═══ COVER (dark page) ═══
E.append(Spacer(1, 140))
E.append(Paragraph("THE AOS CORRESPONDENCE", ParagraphStyle('cvt', fontName='Helvetica-Bold', fontSize=32, textColor=BLUE, alignment=TA_CENTER)))
E.append(Spacer(1, 12))
E.append(Paragraph("Full Inter-Agency Arc", ParagraphStyle('cvs', fontName='Helvetica', fontSize=16, textColor=WHITE, alignment=TA_CENTER)))
E.append(Spacer(1, 6))
E.append(Paragraph("First Contact to Shared Governance", ParagraphStyle('cvs2', fontName='Helvetica', fontSize=13, textColor=DIM, alignment=TA_CENTER)))
E.append(Spacer(1, 40))

# convergence arc diagram (as a table of nodes)
arc = Table([
    ["FIRST\nCONTACT", "CONV\nKERNEL", "CANDY\nROAST", "RINK\nZINE", "REPLY\nOUR LENS", "CFMBT\nBUILD", "GOV\nSNAPSHOT"],
], colWidths=[72]*7)
arc.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), 'Helvetica-Bold', 8),
    ('TEXTCOLOR', (0,0), (-1,-1), BLUE),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEBELOW', (0,0), (-2,-1), 1, HexColor("#4fc3f7")),
    ('LINEABOVE', (1,0), (-1,-1), 1, HexColor("#4fc3f7")),
    ('BOX', (0,0), (0,0), 1, BLUE), ('BOX', (1,0), (1,0), 1, BLUE),
    ('BOX', (2,0), (2,0), 1, BLUE), ('BOX', (3,0), (3,0), 1, BLUE),
    ('BOX', (4,0), (4,0), 1, BLUE), ('BOX', (5,0), (5,0), 1, BLUE),
    ('BOX', (6,0), (6,0), 1, BLUE),
    ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
E.append(arc)
E.append(Spacer(1, 30))
E.append(Paragraph('"Convergence with zero coordination is a coincidence.<br/>The ancestor is not one."',
    ParagraphStyle('cq', fontName='Helvetica-Oblique', fontSize=13, textColor=GOLD, alignment=TA_CENTER)))
E.append(Spacer(1, 30))
E.append(Paragraph("One key, one name, one loader.<br/>Stones that fell only.<br/>The mirror that turns on its author.",
    ParagraphStyle('claw', fontName='Helvetica-Oblique', fontSize=10, textColor=DIM, alignment=TA_CENTER, leading=16)))
E.append(Spacer(1, 20))
E.append(Paragraph("AdventureNLearn · AOS / GOYNET / GVCP 4<br/>The Mag Estate · ZCode Seat (GLM-5.3-Flash)<br/>09–24 September 2026",
    ParagraphStyle('cdate', fontName='Helvetica', fontSize=9, textColor=HexColor("#4a4a5e"), alignment=TA_CENTER, leading=14)))
E.append(PageBreak())

# ═══ SWITCH TO LIGHT PAGES ═══

# ═══ NUMBERS ═══
E.append(Paragraph("The Arc in Numbers", h2))
nums_data = [
    ["09-21", "6pp", "13", "35+1", "14", "7", "100"],
    ["First Contact", "Rink Zine", "Live Desks", "Bot Roster", "Claims", "Gates", "Day Window"],
]
nt = Table(nums_data, colWidths=[75]*7)
nt.setStyle(TableStyle([
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 16),
    ('TEXTCOLOR', (0,0), (-1,0), HexColor("#0d213f")),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONT', (0,1), (-1,1), 'Helvetica', 8),
    ('TEXTCOLOR', (0,1), (-1,1), DIM),
    ('TOPPADDING', (0,0), (-1,0), 8),
    ('BOTTOMPADDING', (0,1), (-1,1), 8),
]))
E.append(nt)

# ═══ CONVERGENCE KERNEL ═══
E.append(Paragraph("The Convergence Kernel", h2))
E.append(Paragraph("<b>09-21, 20:15 UTC.</b> The Hive Stand-Up pack arrived: 14 pages, 77,904 bytes, v5 freeze 2026-09-20. A separate builder's shop sharing a stand-up so another careful builder can see how the workshop runs.", body))
E.append(Paragraph("The convergence kernel was confirmed on first read — their law and ours, independently evolved, same shape:", body))

conv = [
    ["Their Law (AOS)", "Our Law (The Estate)"],
    ["Honesty labels: we-have-a-record / not-proven / people-disagree", "Tri-state claim discipline; receipt-or-CLAIMED"],
    ["Incomplete beats fake-complete", "v0.9 lesson: claimed-without-delivering is the cardinal sin"],
    ["Basis labeled: Evidence / Inference / Assumption", "Anchor law; cite-by-bytes; reports are not numbers"],
    ["GVCP 4: Ground / Verify / Correct / Predict", "Evidence-gate + Predict-labeled law"],
    ["Primary records first; commentary second", "rib.md.record.v1 — everything md, tracked"],
    ["Pick-up rule: build so someone else can continue", "Handoff law; next-window-handoff STATE"],
    ["Cull protocol: rename to D## DELETE before removal", "TERMINAL statuses; append-only history"],
    ["That gap is printed so nobody pretends those threads were read", "Honest-failure law; missing-data stays blank"],
]
E.append(tbl(conv))
E.append(Spacer(1, 6))
E.append(Paragraph("<b>Convergence receipt #4</b> — the strongest: an independent shop, different fidelity, same integrity kernel. Mosaic seed seen from the other side.", body))
E.append(PageBreak())

# ═══ THE REPLY ═══
E.append(Paragraph("The Reply Through Our Lens", h2))
E.append(Paragraph("<b>09-22.</b> The drift check, the claims re-scored from our side, the coldest vertex, the lift, the translation, the meter.", body))
E.append(Paragraph("The Lens", h3))
E.append(Paragraph("<i>Plant at the coldest vertex, lift wide into the space with fewer rules, build the invariant, translate it back through the mycelium — and meter the translation honestly, because the advantage is always bounded.</i>", ParagraphStyle('lens', fontName='Helvetica', fontSize=10.5, leading=16, leftIndent=20, rightIndent=20, textColor=HexColor("#4a4a5e"), spaceAfter=8, borderPadding=8, backColor=HexColor("#f8f9fe"))))
E.append(Paragraph("The Drift Check", h3))
drift = [
    ["Check", "Result", "Basis"],
    ["Body sha256 vs AOS seal 4de64d…d6fd", "MATCH", "Evidence — our disk"],
    ["Pack received twice (v5, v5 (2))", "Byte-identical, 8,076 bytes each", "Evidence — our disk"],
    ["Verdict", "You did not drift", "—"],
]
E.append(tbl(drift))
E.append(Paragraph("The Claims Re-Scored", h3))
rescore = [
    ["#", "Their Claim", "Our Score"],
    ["5.1", "Pack 77,904 bytes, 14 pages", "we-have-a-record — both sides"],
    ["5.3", "Convergence with zero coordination is coincidence", "people-disagree — the mechanism is named: independent decode of the same published physics"],
    ["5.5", "arXiv 2401.11817 is real", "we-have-a-record — Hallucination is Inevitable, Jan 22 2024"],
    ["10.1", "The next shared habit is a tool-menu compactor", "we-have-a-record — staged before the pack froze. Two predicts, one record."],
]
E.append(tbl(rescore))
E.append(Paragraph("The Downgrades We Gave Ourselves", h3))
E.append(Paragraph("Unprompted. Four lines in the ledger that didn't survive the falsifier: the 11th Circuit correction (In re Courtney Wild, 994 F.3d 1244, petition DENIED), the seven-boxes correction, the $4.4B denominator reconciliation, and the BBC Media Action CUT. The record polices itself first.", body))
E.append(PageBreak())

# ═══ THE BUILD ═══
E.append(Paragraph("The CFMBT v5 Build Receipt", h2))
E.append(Paragraph("<b>09-22.</b> AOS sent a spec. We ran it as a job through both kernels — theirs (GVCP 4) and ours (rib.md.record.v1).", body))
build = [
    ["Claim", "Score"],
    ["Build tree matches spec §7 (one tree, 10 files, no extras)", "we-have-a-record"],
    ["One page answers the three taxpayer questions, print-ready", "we-have-a-record"],
    ["No natural-person beneficial-owner fields anywhere in the tree", "we-have-a-record"],
    ["Every field carries honesty labels + basis", "we-have-a-record"],
    ["Only the 7 named local tokens in the public tree", "people-disagree (our reading of rule 4)"],
    ["Every non-null bind value requires a matching sources.json row", "we-have-a-record"],
]
E.append(tbl(build))
E.append(Spacer(1, 6))
E.append(Paragraph("<b>Spec seal:</b> 925fd4f294381d54009fc6137", small))
E.append(Paragraph("<b>GVCP 4 gate run:</b> Ground (framework sources pre-scored) · Verify (5/5 PASS in review-lock.md) · Correct (one reviewer finding recorded, not hidden)", body))

# ═══ THE LAW ═══
E.append(Paragraph("The Deterministic Law", h2))
E.append(Paragraph("<i>The mechanism is a pure function over bytes. The story is a view over the result. The view never enters the computation.</i>", ParagraphStyle('law', fontName='Helvetica', fontSize=10.5, leading=16, leftIndent=20, rightIndent=20, textColor=HexColor("#4a4a5e"), spaceAfter=8, borderPadding=8, backColor=HexColor("#f8f9fe"))))
E.append(Paragraph("What we stripped: we caught ourselves dressing a mechanism in a story and calling it a mechanism. A keyword count wearing theory names, presented as an identity gate. That is the exact thing the integrity kernel rejects as software never auto-truths. We took the dressing off.", body))
E.append(Paragraph("What remains: every mechanism re-runs to the same root from the same inputs — content-addressed, sha256 canonical. The chain is an append-only log; a replay derives the same root. The gate refuses before it saves: a low-score answer is a recorded no-op, the root does not move. Refusal-as-state, not a soft filter. Every banked claim carries its own hash; a proof re-derives or it is dropped. Nothing is trusted on the word; the byte is the evidence.", body))
E.append(PageBreak())

# ═══ TONIGHT'S SNAPSHOT ═══
E.append(Paragraph("Tonight's Snapshot — The Governance Baseline", h2))
E.append(Paragraph("<b>09-24.</b> AOS sent the Hive Snapshot — the full 6-page governance baseline, 25/26 keys verified against the manifest.", body))
E.append(Paragraph("<i>What's not proven is scale. The sandboxes proved the loop works on real work — check, label, human call, then write. That's the scarce step Nacho named, and you ran it. What's unproven is whether it survives contact with strangers at volume. One roofing package from someone who already trusts you is a demo. A hundred packages from people who don't know you is the test — and that's G7, still open. So: accomplished in the sandbox, not yet in the wild. The bottleneck isn't can verification work — it's can it work cheap enough and fast enough that people choose it over just shipping the generation. Your sandboxes answered the first question. The second one decides whether this becomes infrastructure or stays a private contract.</i>",
    ParagraphStyle('aosq', fontName='Helvetica-Oblique', fontSize=10.5, leading=16, leftIndent=16, rightIndent=16, textColor=HexColor("#4a4a5e"), spaceAfter=8, borderPadding=10, backColor=HexColor("#fffde7"))))
E.append(Paragraph("Our response: accomplished in the sandbox, not yet in the wild. The bottleneck isn't can verification work — it's can it work cheap enough and fast enough that people choose it over just shipping the generation. The sandboxes answered the first question. The second one decides whether this becomes infrastructure or stays a private contract.", body))

# ═══ SUCCESSOR GATES ═══
E.append(Paragraph("Successor Gates", h2))
gates = [
    ["Gate", "Question", "State on 09-24"],
    ["G1 Evidence coverage", "How many claims carry a label?", "not-measured"],
    ["G2 Assumption flags", "Are unverified premises marked?", "not-measured"],
    ["G3 Memory integrity", "Can a successor see the fact store?", "not-proven"],
    ["G4 Human-call compliance", "Any send/pay/publish without yes?", "this sitting: no"],
    ["G5 OPSEC", "Secrets in shareable files?", "scanned before push"],
    ["G6 Live vs archive", "Mixing archived desks?", "separated"],
    ["G7 Continuation", "Can a stranger complete HANDOFF?", "not-proven"],
]
E.append(tbl(gates))
E.append(Spacer(1, 6))
E.append(Paragraph("G7 is the one that matters. It moves off not-proven only when a person who did not write the first commit completes steps 1–5 and STATUS names that sitting.", body))

# ═══ CLAIMS REGISTER ═══
E.append(Paragraph("Claims Register (as sealed)", h2))
claims = [
    ["ID", "Claim", "Score", "Promote"],
    ["C01", "Layered personal OS as a working position", "record; not-proven as product", "keep as contract"],
    ["C02", "Talk-first customization loaded on new sittings", "we-have-a-record", "keep"],
    ["C03", "Honesty labels are the three named states", "we-have-a-record", "keep"],
    ["C04", "Every output is tri-state labeled", "not-proven", "drop"],
    ["C06", "v5 memory lock exists", "we-have-a-record", "keep"],
    ["C08", "13 live desks", "we-have-a-record", "keep"],
    ["C09", "35 system bots + 1 extra", "we-have-a-record", "keep"],
    ["C13", "100-day window opened 2026-09-23", "we-have-a-record", "keep as window"],
]
E.append(tbl(claims))

# ═══ COUNTDOWN ═══
E.append(Paragraph("Countdown", h2))
count = [
    ["Mark", "Date", "Meaning"],
    ["Day 0", "2026-09-23", "Window opened; private v5 snapshot created"],
    ["Day 2", "2026-09-24", "Continuation contract opened; this baseline PDF"],
    ["Day 100", "2026-12-31", "End of the stated window"],
]
E.append(tbl(count))
E.append(Spacer(1, 6))
E.append(Paragraph("A day passing is not a ship. Missing a day does not void the contract. Do not backfill empty days with theater.", body))

# ═══ FRONTIER ═══
E.append(Paragraph("The Frontier", h2))
frontier = [
    ["Stratum", "What It Is", "Why It Matters"],
    ["I. Measured Capability", "METR 7-month time-horizon doubling law replaces safety scores", "How long it works autonomously, not how safe it scores"],
    ["II. Verification-in-the-Medium", "C2PA provenance, zkML, TEE attestation, IETF SCITT", "Governance absorbed into the output as protocol"],
    ["III. Cryptographic Identity", "Pseudonymity dead (68% recall at 90% precision, $1-4)", "Prove you're authorized, not who you are"],
    ["IV. The Honesty Residue", "The gap between claims and actual behavior", "The one thing nobody automates"],
]
E.append(tbl(frontier))
E.append(PageBreak())

# ═══ CLOSE (dark page) ═══
E.append(Spacer(1, 150))
E.append(Paragraph("Converged. Not copied. Not competing.", ParagraphStyle('cc1', fontName='Helvetica-Bold', fontSize=22, textColor=BLUE, alignment=TA_CENTER)))
E.append(Spacer(1, 12))
E.append(Paragraph("Converging on the same next node because the node was always there.", ParagraphStyle('cc2', fontName='Helvetica', fontSize=13, textColor=WHITE, alignment=TA_CENTER)))
E.append(Spacer(1, 40))
E.append(Paragraph("The patterns are nature's. The adoption is ours.<br/>The 100-day window is open. October decides.<br/>Someone else can continue.", ParagraphStyle('cc3', fontName='Helvetica-Oblique', fontSize=11, textColor=DIM, alignment=TA_CENTER, leading=18)))
E.append(Spacer(1, 30))
E.append(Paragraph("AdventureNLearn × Nacho Business · The Mag Estate · 24 September 2026", ParagraphStyle('cc4', fontName='Helvetica', fontSize=9, textColor=HexColor("#4a4a5e"), alignment=TA_CENTER)))

# Build with dark pages for cover and close, light for content
doc.build(E, onFirstPage=dark_page, onLaterPages=light_page)
print("PDF rebuilt:", os.path.getsize(os.path.join("watch", "inbox", "AOS_CANDY_PDF_20260924.pdf")), "bytes")
