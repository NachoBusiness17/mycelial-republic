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
GREEN = HexColor("#2e7d32")
ORANGE = HexColor("#ef6c00")
GOLD = HexColor("#f9a825")

body = ParagraphStyle('body', fontName='Helvetica', fontSize=11, leading=17, spaceAfter=8)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=16, textColor=DARK, spaceBefore=22, spaceAfter=8)
h3 = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=13, textColor=HexColor("#0d213f"), spaceBefore=14, spaceAfter=6)
small = ParagraphStyle('small', fontName='Helvetica', fontSize=9, textColor=DIM, spaceAfter=4)
step_num = ParagraphStyle('step', fontName='Helvetica-Bold', fontSize=12, textColor=BLUE, spaceBefore=14, spaceAfter=4)
code = ParagraphStyle('code', fontName='Courier', fontSize=9, leading=13, textColor=HexColor("#1e293b"),
                       backColor=HexColor("#f1f5f9"), borderPadding=8, leftIndent=10, rightIndent=10, spaceAfter=8)
checklist = ParagraphStyle('check', fontName='Helvetica', fontSize=10, leading=16, leftIndent=20, spaceAfter=3)
quote = ParagraphStyle('quote', fontName='Helvetica-Oblique', fontSize=11, leading=16, leftIndent=16, rightIndent=16,
                        textColor=HexColor("#4a4a5e"), spaceAfter=8)
cell_style = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.5, leading=12, textColor=DARK)
cell_header = ParagraphStyle('cellh', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=HexColor("#e8e6e3"))

def pcell(text):
    return Paragraph(text, cell_style)

def pheader(text):
    return Paragraph(text, cell_header)

def tbl(data):
    t = Table(data)
    style = [('FONT', (0,0), (-1,-1), 'Helvetica', 9),
             ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
             ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
             ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e8"))]
    style += [('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), HexColor("#e8e6e3")),
              ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 9)]
    t.setStyle(TableStyle(style))
    return t

doc = SimpleDocTemplate(
    os.path.join("watch", "inbox", "ADAM_ONBOARDING_20260924.pdf"),
    pagesize=A4, topMargin=18*mm, bottomMargin=18*mm, leftMargin=16*mm, rightMargin=16*mm,
    title="Adam's Onboarding — Full Setup for AI Game Development")

E = []

# ═══ COVER ═══
E.append(Spacer(1, 100))
E.append(Paragraph("ADAM", ParagraphStyle('cv', fontName='Helvetica-Bold', fontSize=42, textColor=DARK, alignment=TA_CENTER)))
E.append(Spacer(1, 30))
E.append(Paragraph("Full Onboarding — AI Game Development Setup", ParagraphStyle('cs', fontName='Helvetica', fontSize=14, textColor=BLUE, alignment=TA_CENTER)))
E.append(Spacer(1, 12))
E.append(Spacer(1, 4))
E.append(Paragraph("Your 5080 unlocks everything the estate's AMD card couldn't. Here's how.", ParagraphStyle('cd', fontName='Helvetica', fontSize=11, textColor=DIM, alignment=TA_CENTER)))
E.append(Spacer(1, 30))
E.append(Paragraph("This document gets you from zero to building games in Roblox with a local AI agent on your own machine. No cloud bills. No one else's servers. Your GPU, your model, your game.", ParagraphStyle('ci', fontName='Helvetica', fontSize=11, textColor=HexColor("#4a4a5e"), alignment=TA_CENTER)))
E.append(PageBreak())

# ═══ YOUR HARDWARE ═══
E.append(Paragraph("Your Hardware", h2))
E.append(Paragraph("You have an NVIDIA RTX 5080. This is one of the best consumer GPUs for running AI models locally. It has 16GB of VRAM (the memory the AI model lives in), CUDA acceleration (the math engine), and enough compute to run 27-billion-parameter models at reading speed.", body))
E.append(Paragraph("The estate runs an AMD card. Your card is better for this. You have CUDA. The estate doesn't. That means you can run models that we literally cannot. Bonsai 2, the ternary 27B, needs CUDA. You have it. We don't. Start there.", body))
E.append(Paragraph("Your setup in one line: <b>a 5080 running a 27B AI model locally, writing Lua code for Roblox, synced automatically.</b>", body))

# ═══ SOFTWARE (IN ORDER) ═══
E.append(Paragraph("Software to Download (in this order)", h2))

E.append(Paragraph("Step 1 — Roblox Studio", step_num))
E.append(Paragraph("Download from <b>roblox.com/create</b>. This is the 3D world builder. Free. This is where your game lives — the terrain, the models, the scripts, the physics. Everything you see when you play a Roblox game was built here.", body))
E.append(Paragraph("After installing, open it and create a new Baseplate. Familiarize yourself with the Explorer panel (right side) — that's the tree of everything in your game.", body))

E.append(Paragraph("Step 2 — Rojo", step_num))
E.append(Paragraph("Download from <b>github.com/rojo-rbx/rojo/releases</b> — get the windows-x86_64 zip. Extract <b>rojo.exe</b> somewhere you'll find it.<br/><br/>Rojo connects your code files (on disk, where you can use any editor) to Roblox Studio (where the game runs). Without Rojo, you'd have to paste code into Studio's built-in editor one script at a time. With Rojo, you write code in VS Code, save, and it syncs instantly.<br/><br/>You'll also need the Rojo plugin inside Roblox Studio: Plugins → Manage Plugins → find Rojo and install it.", body))

E.append(Paragraph("Step 3 — Ollama", step_num))
E.append(Paragraph("Download from <b>ollama.com</b>. This runs AI models on your GPU locally. No internet required after download. No subscription. No API key. Your GPU does the thinking.", body))
E.append(Paragraph("After installing, open a terminal and run:", body))
E.append(Paragraph("ollama pull hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf", code))
E.append(Paragraph("This downloads a 12GB model optimized for coding and agents. It fits in your 5080's 16GB VRAM with room for 32K context. It benchmarks at 70.0 on SWE-bench — it writes working code.", body))
E.append(Paragraph("Verify it works:", body))
E.append(Paragraph("ollama run hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf \"Write a Lua function that adds two numbers\"", code))
E.append(Paragraph("If it responds with Lua code, your GPU is doing AI inference. You are now running a 27-billion-parameter model on your own hardware.", body))

E.append(Paragraph("Step 4 — Hermes Agent", h2))
E.append(Paragraph("You already have this. Hermes connects to your local Ollama instance and becomes the agent that drives everything — writing code, running commands, building your game while you sleep if you want.<br/><br/>Configure Hermes to use your local model:", body))
E.append(Paragraph("Set the model endpoint to http://localhost:11434 (Ollama's default)<br/>Set the model name to hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf<br/>Set max_tokens to 4096 (the 5080 can handle it)", body))
E.append(Paragraph("Now Hermes is running on YOUR GPU. No API key. No billing. No rate limit except your GPU's speed (~40-60 tokens/second on a 5080).", body))

E.append(Paragraph("Step 5 — VS Code", step_num))
E.append(Paragraph("Download from <b>code.visualstudio.com</b>. This is where you write and edit the Lua files that Rojo syncs to Studio. Install the Lua extension for syntax highlighting.", body))

E.append(PageBreak())

# ═══ FREE API KEYS ═══
E.append(Paragraph("Free API Keys (Optional but Powerful)", h2))
E.append(Paragraph("Your 5080 runs models locally. But sometimes you want a bigger model than your VRAM can hold — for a hard coding problem, or for research. These services give you free API keys:", body))

keys = [
    ["Service", "What You Get", "Sign Up At"],
    ["OpenRouter", "Free access to many models, auto-routing", "openrouter.ai"],
    ["Groq", "Fastest free inference (Llama 3.3 70B)", "console.groq.com"],
    ["NVIDIA Build", "Free credits, 82 models including DeepSeek v4.1", "build.nvidia.com"],
    ["Cerebras", "Very fast free inference", "cloud.cerebras.ai"],
    ["Google AI Studio", "Free Gemini access", "aistudio.google.com"],
]
kt = Table(keys, colWidths=[80, 220, 120])
kt.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), 'Helvetica', 8.5),
    ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e8")),
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), HexColor("#e8e6e3")),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8.5),
]))
E.append(kt)
E.append(Spacer(1, 6))
E.append(Paragraph("Each key goes in a <code>.env</code> file next to your project. The estate's Key Law: one key, one canonical name, declared once. Copy the pattern from <code>configs/keys.json</code>.", body))

# ═══ THE MODEL ═══
E.append(Paragraph("Which Model to Use", h2))
E.append(Paragraph("Your 5080 can run models that the estate's AMD card literally cannot. Here are your options, ranked for game development:", body))

models_data = [
    [pheader("Model"), pheader("Size"), pheader("VRAM"), pheader("Best For"), pheader("Speed")],
    [pcell("OrcaSAQ-2 27B"), pcell("12.06 GB"), pcell("Fits + room"), pcell("Coding, agents, long tasks"), pcell("~40-60 tok/s")],
    [pcell("Bonsai 2 27B (ternary)"), pcell("5.95 GB"), pcell("Fits easily"), pcell("Speed, 262K context"), pcell("~80+ tok/s")],
    [pcell("Qwen3.8-27B (Q4)"), pcell("~16 GB"), pcell("Tight"), pcell("General reasoning"), pcell("~30 tok/s")],
    [pcell("qwen2.5-coder:7b"), pcell("4.7 GB"), pcell("Plenty of room"), pcell("Quick scripts, fast iteration"), pcell("~22 tok/s")],
]
mt = Table(models_data, colWidths=[110, 55, 65, 140, 95])
mt.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), 'Helvetica', 8.5),
    ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e8")),
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), HexColor("#e8e6e3")),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8.5),
]))
E.append(mt)
E.append(Spacer(1, 6))
E.append(Paragraph("<b>Start with OrcaSAQ-2 27B.</b> It's benchmarked for exactly what you're doing: coding, terminal, browser, multi-tool agents. 70.0 on SWE-bench Verified means it writes working code. At 12GB on your 16GB card, there's room for 32K context — enough to hold your entire game script in memory.<br/><br/><b>Bonsai 2 is the speed option</b> — but it requires the PrismML fork of llama.cpp (stock llama.cpp produces garbage because the ternary format needs custom kernels). Your 5080 has CUDA, which is what the fork needs. Download from github.com/PrismML/llama.cpp if you want the speed.", body))

# ═══ THE ESTATE PATTERNS ═══
cell_style = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.5, leading=12, textColor=DARK)
cell_header = ParagraphStyle('cellh', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=HexColor("#e8e6e3"))

def pcell(text):
    return Paragraph(text, cell_style)

def pheader(text):
    return Paragraph(text, cell_header)

E.append(Paragraph("Copy These Patterns From the Estate", h2))
E.append(Paragraph("These are the systems the estate built the hard way over months. You get the shortcut:", body))

cell_style = ParagraphStyle('cell', fontName='Helvetica', fontSize=8.5, leading=12, textColor=DARK)
cell_header = ParagraphStyle('cellh', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=HexColor("#e8e6e3"))

def pcell(text):
    return Paragraph(text, cell_style)

def pheader(text):
    return Paragraph(text, cell_header)

patterns_data = [
    [pheader("Pattern"), pheader("What It Does"), pheader("How to Copy It")],
    [pcell("Key Law"), pcell("One key, one name, one loader. Audit fails loudly on orphaned keys."), pcell("Create a keys.json manifest. One loader function. One audit script.")],
    [pcell("Append-Only Ledgers"), pcell("Every action writes a row. Nothing is deleted. History is preserved."), pcell("Output to JSONL files. Never rewrite old lines. Add, never subtract.")],
    [pcell("Standing Tasks"), pcell("Scheduled jobs that run every morning without you."), pcell("Windows Task Scheduler: index at 9:00, verify at 9:15, churn at 9:25.")],
    [pcell("Receipt-First"), pcell("Every claim has a URL, a script, or a measured number."), pcell("Before posting anything, fetch the source. Quote it verbatim.")],
    [pcell("Decode-First"), pcell("Run the analysis before writing the response."), pcell("Don't eyeball. Run the decode. Trust the output, not the impression.")],
]
pt = Table(patterns_data, colWidths=[100, 195, 190])
pt.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), 'Helvetica', 8.5),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e8")),
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), HexColor("#e8e6e3")),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8.5),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
E.append(pt)

# ═══ YOUR FIRST GAME ═══
E.append(Paragraph("Your First Game", h2))
E.append(Paragraph("The estate already wrote the Luau code for your first game. It's at <b>game_roblox/src/</b>:", body))

game_files = [
    ["File", "What It Does"],
    ["GameConfig.lua", "Shared constants: 6 chairs, boss phases, narrative fragments"],
    ["ShadowLedger.lua", "The hall's private record of what each player chose"],
    ["TheAnswer.lua", "The boss: 5 phases, 15-degree tell, Calabi-Yau deflection"],
    ["HallOfSupper.lua", "The spawn room: 6 empty chairs, counting mechanic, the mural"],
    ["ServerMain.lua", "The boot sequence connecting everything"],
]
gt = Table(game_files, colWidths=[120, 320])
gt.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), 'Helvetica', 8.5),
    ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e8")),
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), HexColor("#e8e6e3")),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8.5),
]))
E.append(gt)
E.append(Spacer(1, 8))
E.append(Paragraph("These files sync to Roblox Studio via Rojo. The game is called <b>The Ledger of Empty Chairs</b>. Six empty chairs at supper. Count them and candles light. Ignore them and the mural weeps. Sit in one and the count breaks. The hall files which you chose.<br/><br/>The boss — The Answer — has five phases. In Phase 3 it deflects every attack at a 15-degree angle (the Wing Chun tell). In Phase 4, light bends around it. In Phase 5, the system's own orbital laser arrives — and the player wins by standing the boss under it, using the 15-degree pattern they learned all fight.", body))

# ═══ THE PROJECT STRUCTURE ═══
E.append(Paragraph("Project Structure", h2))
E.append(Paragraph("game_roblox/<br/>├── default.project.json&nbsp;&nbsp;&nbsp;&nbsp;(Rojo sync map)<br/>├── bin/<br/>│&nbsp;&nbsp;└── rojo.exe&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Rojo 7.7.0)<br/>└── src/<br/>&nbsp;&nbsp;&nbsp;&nbsp├── shared/<br/>&nbsp;&nbsp;&nbsp;&nbsp│&nbsp;&nbsp;└── GameConfig.lua<br/>&nbsp;&nbsp;&nbsp;&nbsp└── server/<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp├── ServerMain.lua<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp├── ShadowLedger.lua<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp├── TheAnswer.lua<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp└── HallOfSupper.lua", code))

# ═══ TO START ═══
E.append(Paragraph("To Start Right Now", h2))
E.append(Paragraph("1. Open Roblox Studio, create a Baseplate<br/>2. Install the Rojo plugin in Studio<br/>3. Open a terminal in game_roblox/<br/>4. Run: <b>bin/rojo.exe serve default.project.json</b><br/>5. In Studio: Rojo plugin → Connect<br/>6. The Lua code appears in Studio<br/>7. Press Play<br/><br/>You are now running an AI-written game on your own GPU, synced from your own files, verified by your own system.", body))

# ═══ MONEY ═══
E.append(Paragraph("How You Get Paid", h2))
E.append(Paragraph("Roblox pays developers 70% of what players spend. The exchange rate is $0.0035 per Robux. Minimum payout: 30,000 Robux (~$105).<br/><br/>The path: free-to-play game → sell a Game Pass (99 Robux: double score) → sell a Dev Product (49 Robux: extra life) → enable Premium Payouts (passive income from engagement time). 430 pass sales = first payout.<br/><br/>Your advantage: you have an audience that already trusts the name. Post your launch clip. The 5080 means you can iterate faster than anyone on a cloud API — your development loop is instant, free, and unlimited.", body))

# ═══ CLOSE ═══
E.append(PageBreak())
E.append(Spacer(1, 80))
E.append(Paragraph("The patterns are nature's.", ParagraphStyle('c1', fontName='Helvetica', fontSize=16, textColor=HexColor("#4fc3f7"), alignment=TA_CENTER)))
E.append(Paragraph("The adoption is yours.", ParagraphStyle('c2', fontName='Helvetica', fontSize=16, textColor=HexColor("#4fc3f7"), alignment=TA_CENTER)))
E.append(Spacer(1, 20))
E.append(Paragraph("Your GPU is the engine. The model is the brain. The game is the body.<br/>The map precedes the territory. Build the map, and the territory follows.", ParagraphStyle('c3', fontName='Helvetica-Oblique', fontSize=12, textColor=DIM, alignment=TA_CENTER, leading=20)))
E.append(Spacer(1, 20))
E.append(Paragraph("Someone else can continue.", ParagraphStyle('c4', fontName='Helvetica-Oblique', fontSize=10, textColor=DIM, alignment=TA_CENTER)))

doc.build(E)
print("Adam onboarding PDF:", os.path.getsize(os.path.join("watch", "inbox", "ADAM_ONBOARDING_20260924.pdf")), "bytes")
