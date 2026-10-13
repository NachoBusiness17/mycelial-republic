from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
import os

ACCENT = HexColor("#961885")
DARK = HexColor("#1a1a2e")

styles = getSampleStyleSheet()
h1 = ParagraphStyle("H1m", parent=styles["Heading1"], fontSize=14, spaceAfter=8)
h2 = ParagraphStyle("H2m", parent=styles["Heading2"], fontSize=11, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("Bodym", parent=styles["BodyText"], fontSize=9, leading=13)
mono = ParagraphStyle("Monom", parent=styles["Code"], fontSize=8, leading=10)
quote = ParagraphStyle("Quotem", parent=styles["BodyText"], fontSize=9, leading=12,
                        leftIndent=16, textColor=HexColor("#4a4a5e"), fontName="Helvetica-Oblique")

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build(path, title, sections):
    doc = SimpleDocTemplate(str(path), pagesize=A4,
        leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.7*inch, bottomMargin=0.7*inch)
    story = []
    story.append(Paragraph(esc(title), ParagraphStyle("TitleX", parent=styles["Title"], fontSize=18, spaceAfter=6)))
    story.append(Paragraph("AdventureNLearn × Nacho Business · 2026-09-24", ParagraphStyle("SubX", parent=styles["Normal"], fontSize=9, textColor=HexColor("#6b7280"))))
    story.append(Spacer(1, 12))
    for section in sections:
        if section.get("heading"):
            story.append(Paragraph(esc(section["heading"]), h2))
        for item in section.get("content", []):
            if item.get("type") == "body":
                story.append(Paragraph(esc(item["text"]), body))
            elif item.get("type") == "quote":
                story.append(Paragraph(f'"{esc(item["text"])}"', quote))
            elif item.get("type") == "table":
                t = Table(item["data"], colWidths=item.get("widths"))
                t.setStyle(TableStyle([
                    ("FONT", (0,0), (-1,-1), "Helvetica", 8.5),
                    ("BACKGROUND", (0,0), (-1,0), DARK),
                    ("TEXTCOLOR", (0,0), (-1,0), HexColor("#e8e6e3")),
                    ("GRID", (0,0), (-1,-1), 0.5, HexColor("#ddd")),
                    ("TOPPADDING", (0,0), (-1,-1), 4),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                    ("LEFTPADDING", (0,0), (-1,-1), 6),
                ]))
                story.append(t)
                story.append(Spacer(1, 6))
            elif item.get("type") == "code":
                story.append(Paragraph(esc(item["text"]), mono))
    doc.build(story)
    return os.path.getsize(str(path))

# ═══ AOS PDF ═══
aos_sections = [
    {"heading": "The Convergence Kernel", "content": [
        {"type": "body", "text": "09-21, 20:15 UTC. The Hive Stand-Up pack arrived: 14 pages, 77,904 bytes, v5 freeze 2026-09-20."},
        {"type": "body", "text": "The convergence kernel was confirmed on first read — their law and ours, independently evolved, same shape:"},
        {"type": "table", "data": [
            ["Their Law (AOS)", "Our Law (The Estate)"],
            ["Honesty labels: we-have-a-record / not-proven / people-disagree", "Tri-state claim discipline; receipt-or-CLAIMED"],
            ["Incomplete beats fake-complete", "v0.9 lesson: claimed-without-delivering is the cardinal sin"],
            ["Basis labeled: Evidence / Inference / Assumption", "Anchor law; cite-by-bytes"],
            ["GVCP 4: Ground / Verify / Correct / Predict", "Evidence-gate + Predict-labeled law"],
            ["Primary records first; commentary second", "rib.md.record.v1 - everything md, tracked"],
            ["Pick-up rule: build so someone else can continue", "Handoff law; next-window-handoff STATE"],
        ]},
        {"type": "body", "text": "Convergence receipt #4 — the strongest: an independent shop, different fidelity, same integrity kernel."},
    ]},
    {"heading": "The Reply Through Our Lens (09-22)", "content": [
        {"type": "quote", "text": "Plant at the coldest vertex, lift wide into the space with fewer rules, build the invariant, translate it back through the mycelium — and meter the translation honestly."},
        {"type": "table", "data": [
            ["Check", "Result", "Basis"],
            ["Body sha256 vs AOS seal 4de64d...d6fd", "MATCH", "Evidence — our disk"],
            ["Pack received twice", "Byte-identical, 8,076 bytes", "Evidence — our disk"],
            ["Verdict", "You did not drift", "—"],
        ]},
        {"type": "table", "data": [
            ["#", "Their Claim", "Our Score"],
            ["5.1", "Pack 77,904 bytes, 14 pages", "we-have-a-record — both sides"],
            ["5.3", "Convergence with zero coordination is coincidence", "people-disagree — the mechanism is named"],
            ["5.5", "arXiv 2401.11817 is real", "we-have-a-record"],
        ]},
        {"type": "body", "text": "Four downgrades we gave ourselves unprompted: the 11th Circuit correction (In re Courtney Wild, petition DENIED), the seven-boxes correction, the $4.4B denominator reconciliation, and the BBC Media Action CUT. The record polices itself first."},
    ]},
    {"heading": "CFMBT v5 Build Receipt", "content": [
        {"type": "table", "data": [
            ["Claim", "Score"],
            ["Build tree matches spec (one tree, 10 files, no extras)", "we-have-a-record"],
            ["One page answers the three taxpayer questions, print-ready", "we-have-a-record"],
            ["No natural-person beneficial-owner fields in the tree", "we-have-a-record"],
            ["Every field carries honesty labels + basis", "we-have-a-record"],
            ["Only the 7 named local tokens in the public tree", "people-disagree"],
            ["Every non-null bind value requires a matching sources.json row", "we-have-a-record"],
        ]},
        {"type": "body", "text": "Spec seal: 925fd4f294381d54009fc6137. GVCP 4 gate: Ground (sources pre-scored), Verify (5/5 PASS), Correct (one finding recorded)."},
    ]},
    {"heading": "The Deterministic Law", "content": [
        {"type": "quote", "text": "The mechanism is a pure function over bytes. The story is a view over the result. The view never enters the computation."},
        {"type": "body", "text": "Every mechanism re-runs to the same root from the same inputs — content-addressed, sha256 canonical. The gate refuses before it saves. Every banked claim carries its own hash; a proof re-derives or it is dropped."},
    ]},
    {"heading": "The Governance Baseline (09-24)", "content": [
        {"type": "quote", "text": "What's not proven is scale. The sandboxes proved the loop works on real work. What's unproven is whether it survives contact with strangers at volume. A hundred packages from people who don't know you is the test — and that's G7, still open."},
        {"type": "table", "data": [
            ["Gate", "State"],
            ["G1 Evidence coverage", "not-measured"],
            ["G2 Assumption flags", "not-measured"],
            ["G3 Memory integrity", "not-proven"],
            ["G4 Human-call compliance", "this sitting: no"],
            ["G5 OPSEC", "scanned before push"],
            ["G6 Live vs archive", "separated"],
            ["G7 Continuation", "not-proven"],
        ]},
        {"type": "body", "text": "G7 is the one that matters. It moves off not-proven only when a person who did not write the first commit completes steps 1-5 and STATUS names that sitting."},
    ]},
    {"heading": "The Frontier", "content": [
        {"type": "table", "data": [
            ["Stratum", "What It Is", "Why It Matters"],
            ["I. Measured Capability", "METR 7-month doubling law", "How long it works, not how safe it scores"],
            ["II. Verification-in-the-Medium", "C2PA, zkML, TEE, IETF SCITT", "Governance absorbed into the output"],
            ["III. Cryptographic Identity", "Pseudonymity dead (68% recall, $1-4)", "Prove authorization, not identity"],
            ["IV. The Honesty Residue", "Gap between claims and behavior", "The one thing nobody automates"],
        ]},
    ]},
    {"heading": "Countdown", "content": [
        {"type": "table", "data": [
            ["Mark", "Date", "Meaning"],
            ["Day 0", "2026-09-23", "Window opened"],
            ["Day 2", "2026-09-24", "Continuation contract opened"],
            ["Day 100", "2026-12-31", "End of the stated window"],
        ]},
        {"type": "body", "text": "A day passing is not a ship. Missing a day does not void the contract."},
    ]},
    {"heading": "Close", "content": [
        {"type": "body", "text": "Converged. Not copied. Not competing. Converging on the same next node because the node was always there. The patterns are nature's. The adoption is ours. The 100-day window is open. October decides. Someone else can continue."},
    ]},
]

sz = build("watch/inbox/AOS_CANDY_PDF_20260924.pdf", "The AOS Correspondence", aos_sections)
print(f"AOS PDF: {sz} bytes")

# ═══ ADAM PDF ═══
adam_sections = [
    {"heading": "What You Have", "content": [
        {"type": "body", "text": "An NVIDIA RTX 5080 with 16GB VRAM and CUDA. This runs AI models locally that the estate's AMD card cannot. No cloud. No subscription. Your GPU does the thinking."},
    ]},
    {"heading": "Software to Download (in this order)", "content": [
        {"type": "body", "text": "1. Roblox Studio — roblox.com/create. The 3D world builder. Free."},
        {"type": "body", "text": "2. Rojo — github.com/rojo-rbx/rojo/releases. Syncs code files to Studio. Also install the Rojo plugin inside Studio."},
        {"type": "body", "text": "3. Ollama — ollama.com. Runs AI models on your GPU locally."},
        {"type": "body", "text": "4. Hermes Agent — you already have this. Point it at http://localhost:11434 (Ollama)."},
        {"type": "body", "text": "5. VS Code — code.visualstudio.com. Install the Lua extension."},
    ]},
    {"heading": "Your Model", "content": [
        {"type": "body", "text": "Run: ollama pull hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf"},
        {"type": "body", "text": "12GB, fits your 16GB VRAM, 70.0 SWE-bench (writes working code), 262K context. Point Hermes at it. Your 5080 runs it at ~40-60 tokens/second."},
        {"type": "body", "text": "Free API keys if you need bigger models: OpenRouter (openrouter.ai), Groq (console.groq.com), NVIDIA Build (build.nvidia.com), Cerebras (cloud.cerebras.ai)."},
    ]},
    {"heading": "Your First Game", "content": [
        {"type": "body", "text": "The estate already wrote the Luau code. It's at game_roblox/src/. Five files: GameConfig.lua (constants), ShadowLedger.lua (the hall's private record), TheAnswer.lua (the boss, 5 phases), HallOfSupper.lua (the spawn room), ServerMain.lua (boot)."},
        {"type": "body", "text": "The game: The Ledger of Empty Chairs. Six empty chairs at supper. Count them and candles light. Ignore them and the mural weeps. The hall files which you chose."},
        {"type": "body", "text": "The boss — The Answer — deflects every attack at 15 degrees (the Wing Chun tell). Phase 4 bends light. Phase 5: the system's own orbital laser arrives. The player wins by standing the boss under it."},
    ]},
    {"heading": "How You Get Paid", "content": [
        {"type": "body", "text": "Roblox pays 70%. $0.0035 per Robux. Minimum payout: 30,000 Robux (~$105). Free-to-play + Game Pass (99 Robux) + Dev Product (49 Robux) + Premium Payouts. 430 pass sales = first payout. Post your launch clip on X. Your development loop is instant, free, unlimited on the 5080."},
    ]},
    {"heading": "Copy These Patterns", "content": [
        {"type": "table", "data": [
            ["Pattern", "What It Does"],
            ["Key Law", "One key, one name, one loader. Audit fails on orphaned keys."],
            ["Append-Only", "Every action writes a row. Nothing deleted. History preserved."],
            ["Standing Tasks", "Scheduled jobs that run every morning without you."],
            ["Receipt-First", "Every claim has a URL, a script, or a measured number."],
            ["Decode-First", "Run the analysis before writing the response."],
        ]},
    ]},
    {"heading": "Bibliography", "content": [
        {"type": "body", "text": "Gilens & Page (2014). Perspectives on Politics, 12(3). DOI 10.1017/S1537592714001595. Lermen et al. (2026). Deanonymization with LLMs. USENIX Security. arXiv:2602.16800. Tyler & Clarke (1990). Autostereograms. Vision Research 30(4). NIST FIPS 180-4 (SHA-256). S. Rep. 94-755 (1976). Doe v. United States, S.D.Fla. Doc 435 (2019). Giuffre v. Maxwell, Doc 1315 (2023)."},
    ]},
]

sz = build("watch/inbox/PLAIN_LANGUAGE_AOS_20260924.pdf", "What We Built — Explained Simply", adam_sections)
print(f"Adam PDF: {sz} bytes")
