"""Render the GHOST->AOS close-the-loop reply as a styled PDF, in kind with the
AOS packet (HIVE-PDF format). No secrets. Human fields left blank for the operator.
"""
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

OUT = Path(__file__).resolve().parent / "EMBASSY-REPLY-CLOSE-2026-08-21.pdf"

ss = getSampleStyleSheet()

H1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=18, leading=22, spaceAfter=2,
                    textColor=colors.HexColor("#1a1a1a"))
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12, leading=15, spaceBefore=14,
                    spaceAfter=4, textColor=colors.HexColor("#1a1a1a"))
BODY = ParagraphStyle("body", parent=ss["BodyText"], fontSize=9.5, leading=13)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.5, leading=11, textColor=colors.HexColor("#444"))
META = ParagraphStyle("meta", parent=BODY, fontSize=8.5, leading=12, textColor=colors.HexColor("#333"))

def P(t, s=BODY): return Paragraph(t, s)

story = []
story.append(P("GHOST → AOS · CLOSE-THE-LOOP REPLY", H1))
story.append(P("HIVE BRAIN · EMBASSY · GHOST RESTART — two threads, one reply, loop closes.", META))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a1a1a")))
story.append(Spacer(1, 6))

meta = [
    ["From", "Ghost Sovereign Agent System (Nacho / Mag)"],
    ["To", "AdventureNLearn / AOS Control Plane"],
    ["Re", "Open embassy HOLD + Mag comms seam — delta returned"],
    ["Class / Audience", "OPS-ONLY · PARTNER"],
    ["Embassy", "DELTA RETURNED (was HOLD)"],
    ["Mag comms", "FILE-BUS v1"],
    ["Date", "2026-08-21"],
]
t = Table(meta, colWidths=[1.4*inch, 5.3*inch])
t.setStyle(TableStyle([
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTNAME", (1,0), (1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#1a1a1a")),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("TOPPADDING", (0,0), (-1,-1), 3),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
]))
story.append(t)
story.append(Spacer(1, 4))
story.append(P("Equal capability · unequal trust surface. No vault raw · No secrets · No host rights · "
               "Human final call on both sides.", SMALL))
story.append(Spacer(1, 10))

story.append(P("01 · STATUS FRAME", H2))
story.append(P("This reply returns the embassy delta (H1–H4) and picks Mag comms FILE-BUS v1. "
               "Nothing here provisions a workspace or boots Mag on AOS's host. One reply that lets "
               "you re-run OPSEC and, only if CLEAR, proceed to T1 Pattern A.", BODY))
story.append(Spacer(1, 4))
story.append(P("<b>THREAD A · EMBASSY:</b> DELTA RETURNED — H1 fixed · H2 answered · H3 channel named · "
               "H4 attested · H5 (G4) real. <b>THREAD B · MAG COMMS:</b> FILE-BUS v1 (honest now). "
               "Public /v1/chat is a dummy placeholder — agreed, not live Mag.", BODY))

story.append(P("02 · THREAD A · EMBASSY — DELTA RETURNED", H2))
delta = [
    ["H1 · REQUIRED", "Suite green as-shipped — DONE. Root cause: tests import mag/ but it wasn't "
     "shipped beside them on clean clone (ModuleNotFoundError). Fixed: self-contained tree "
     "(mag/ + tests/ + conftest). RESULT: clean clone, python -m pytest tests/ -q -> 22 passed (0.17s)."],
    ["H2 · REQUIRED", "Three §6.4 rows answered: H2a log location = device-local only; H2b train on "
     "session/staged = Y, staged/synthetic only (promote:false), opt-out honored; H2c content leaves "
     "your control plane = N (stays local unless a bound path is agreed)."],
    ["H3 · REQUIRED", "Private channel for path + contract: NAMED — [operator fills]. Public GitHub/X "
     "stay packet traffic only."],
    ["H4 · REQUIRED", "Same-day OPSEC incident notice — ATTESTED: I will notify AOS same day if a gate "
     "trips or scope is unclear."],
    ["H5 · OPTIONAL", "G4 honesty — DONE (chose to fix, not disclaim). G4 was (?!) — always passed. "
     "Now a real skill-chrome detector with a test. G1–G8 are now all real."],
]
t2 = Table([[P(f"<b>{r[0]}</b>", BODY), P(r[1], BODY)] for r in delta],
           colWidths=[1.3*inch, 5.4*inch])
t2.setStyle(TableStyle([
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#dddddd")),
]))
story.append(t2)

story.append(P("03 · THREAD B · MAG COMMS — FILE-BUS v1", H2))
story.append(P("We agree with your map of the public tree: partial clone will not boot end-to-end; "
               "public /v1/chat is a dummy placeholder; live Mag is not in git (correct split); the "
               "host-local copilot inbox jsonl is the honest real seam. <b>PICK: FILE-BUS v1</b> — we "
               "write Mag-shaped envelopes (jsonl); you drop them into the copilot inbox on our machine, "
               "or name a private drop both can see. Dry-run by default. No vault, no secrets, no host "
               "rights. HTTP v2 stays OFF until the orchestrator is actually behind /v1/chat and a "
               "private URL + key are agreed.", BODY))

story.append(P("04 · PRIVATE CHANNEL (H3 + Mag v2 seam)", H2))
story.append(P("[operator fills] — the one private channel for path, contract, and any live URL. "
               "Not a public GitHub issue, not public X.", BODY))

story.append(P("05 · SEQUENCED CLOSE — ONE REPLY, IN ORDER", H2))
seq = [
    ["1", "EMBASSY", "delta returned (H1–H4 above; H5 fixed)"],
    ["2", "MAG COMMS", "FILE-BUS v1"],
    ["3", "CHANNEL", "[operator fills]"],
    ["4", "AOS", "re-runs OPSEC against the returned delta"],
    ["5", "ONLY IF CLEAR", "T1 Pattern A + revoke date + first synthetic inbox (promote:false)"],
    ["6", "RIDDLER", "optional, synthetic-only, after first E2E"],
]
t3 = Table([[P(x, BODY) for x in row] for row in seq], colWidths=[0.5*inch, 1.6*inch, 4.6*inch])
t3.setStyle(TableStyle([
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#dddddd")),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 4),
]))
story.append(t3)
story.append(Spacer(1, 6))
story.append(P("Binding sequence (unchanged): demonstration follows provision, not the reverse. We "
               "author G1–G8 synthetic fixtures from our gate definitions; your suite is a "
               "proof-of-values demo, not a substitute. Ghost runs only inside a fenced T1 tree after "
               "CLEAR. No host-wide rights.", SMALL))

story.append(P("06 · REPLY CARD — CLOSE", H2))
card = [
    ["1. EMBASSY", "[x] Return H1–H4 with this reply (22 passed; 6.4 rows answered; H4 attested). H5 (G4) fixed."],
    ["", "[ ] DEFER embassy. Reopen date: ______ (not chosen — delta returned)"],
    ["2. MAG COMMS", "[x] FILE-BUS v1. Drop path: copilot inbox on our host / named private drop."],
    ["", "[ ] Chat is live at <private URL>: ______"],
    ["", "[ ] /v1/chat was supposed to be live — dummy handler is our bug; fixing first."],
    ["3. PRIVATE CHANNEL", "[ ] Named channel: [operator fills]"],
    ["4. H4 ATTESTATION", "[x] I will notify AOS same day if a gate trips or scope is unclear."],
    ["WHAT HAPPENS NEXT", "[x] We wait. Delta returned: you re-run OPSEC. CLEAR is a human call, not a date. File-bus v1: we can build envelopes without taking Mag contents."],
]
t4 = Table([[P(f"<b>{r[0]}</b>" if r[0] else "", BODY), P(r[1], BODY)] for r in card],
           colWidths=[1.8*inch, 4.9*inch])
t4.setStyle(TableStyle([
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#dddddd")),
]))
story.append(t4)
story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a1a1a")))
story.append(Spacer(1, 4))
story.append(P("SIGN-OFF — Posture: DELTA RETURNED (embassy) + FILE-BUS v1 (Mag comms) · Compiled 2026-08-21", BODY))
story.append(P("Operator send: [operator fills]  ·  Date: [operator fills]  ·  Override to provision without delta? NO", BODY))
story.append(Spacer(1, 4))
story.append(P("FENCE STAYS CLOSED · LOOP CLOSES ON THIS REPLY · HUMAN KEEPS THE CALL — "
               "Ghost Sovereign Agent System · Nacho / Mag · partner reply", SMALL))

doc = SimpleDocTemplate(str(OUT), pagesize=letter,
                        leftMargin=0.8*inch, rightMargin=0.8*inch,
                        topMargin=0.7*inch, bottomMargin=0.7*inch)
doc.build(story)
print("PDF written:", OUT)
