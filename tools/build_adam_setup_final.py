from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
import os

DARK = HexColor("#1a1a2e")
BLUE = HexColor("#1565c0")
DIM = HexColor("#6b7280")

styles = getSampleStyleSheet()
h2 = ParagraphStyle("H2x", parent=styles["Heading2"], fontSize=14, spaceBefore=16, spaceAfter=6)
h3 = ParagraphStyle("H3x", parent=styles["Heading3"], fontSize=12, spaceBefore=12, spaceAfter=4)
body = ParagraphStyle("Bodyx", parent=styles["BodyText"], fontSize=10, leading=15)
code = ParagraphStyle("Codex", parent=styles["Code"], fontSize=9, leading=13,
                       backColor=HexColor("#f0f4f8"), borderPadding=6, leftIndent=10, spaceAfter=8)
small = ParagraphStyle("Smallx", parent=styles["Normal"], fontSize=8.5, textColor=DIM, spaceAfter=4)
step = ParagraphStyle("Stepx", fontName="Helvetica-Bold", fontSize=12, textColor=BLUE, spaceBefore=16, spaceAfter=6)

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

doc = SimpleDocTemplate(
    os.path.join("watch", "inbox", "ADAM_SETUP_20260924.pdf"),
    pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch,
    leftMargin=0.75*inch, rightMargin=0.75*inch,
    title="Adam's Setup — AI Game Development")

E = []

E.append(Paragraph("Adam's Setup Guide", ParagraphStyle("T", parent=styles["Title"], fontSize=22, spaceAfter=4)))
E.append(Paragraph("AI-assisted game development on your RTX 5080", ParagraphStyle("S", parent=styles["Normal"], fontSize=11, textColor=DIM)))
E.append(Spacer(1, 16))

# ═══ HARDWARE ═══
E.append(Paragraph("What You Have", h2))
E.append(Paragraph("An RTX 5080 with 16GB VRAM and CUDA acceleration. This runs AI models locally — no cloud, no subscription, no rate limit. You can run a 27-billion-parameter model that writes working code at reading speed.", body))

# ═══ STEP 1 ═══
E.append(Paragraph("Step 1 — Roblox Studio", step))
E.append(Paragraph("Download from <b>roblox.com/create</b>. Click Start Creating. Free account required.", body))
E.append(Paragraph("<b>Verify:</b> Open Roblox Studio. You should see the template picker (Baseplate, Platformer, Racing, etc.). Pick Baseplate.", body))

# ═══ STEP 2 ═══
E.append(Paragraph("Step 2 — Ollama", step))
E.append(Paragraph("This runs AI models on your GPU. No internet needed after download.", body))
E.append(Paragraph("<b>Install:</b> Open PowerShell as Administrator and run:", body))
E.append(Paragraph("winget install Ollama.Ollama", code))
E.append(Paragraph("<b>Pull your model:</b>", body))
E.append(Paragraph("ollama pull hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf", code))
E.append(Paragraph("This downloads 12GB. It fits in your 16GB VRAM. It writes working code (70.0 SWE-bench).", body))
E.append(Paragraph("<b>Verify:</b>", body))
E.append(Paragraph("ollama run hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf \"Write a Lua function that prints hello\"", code))
E.append(Paragraph("If it responds with Lua code, your GPU is doing AI. Type /bye to exit.", body))
E.append(Paragraph("<b>Check GPU is being used:</b>", body))
E.append(Paragraph("ollama ps", code))
E.append(Paragraph("Look at the PROCESSOR column. It should say 100% GPU. If it says 100% CPU, your NVIDIA driver needs updating — go to nvidia.com/drivers, download the latest, install, restart.", body))
E.append(Paragraph("<b>Gotcha:</b> Ollama's default context window is 4096 tokens. For game development you need more. Create a Modelfile:", body))
E.append(Paragraph("FROM hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf<br/>PARAMETER num_ctx 32768", code))
E.append(Paragraph("ollama create orcasaq-32k -f Modelfile", code))
E.append(Paragraph("Now use orcasaq-32k as your model name. You have 32K context — enough to hold your entire game script.", body))

# ═══ STEP 3 ═══
E.append(Paragraph("Step 3 — Rojo", step))
E.append(Paragraph("Rojo syncs code files from your computer into Roblox Studio automatically. Write code in VS Code, save, and it appears in Studio.", body))
E.append(Paragraph("<b>Install:</b>", body))
E.append(Paragraph("mkdir C:\\tools -Force; cd C:\\tools\ncurl -L -o rojo.zip \"https://github.com/rojo-rbx/rojo/releases/download/v7.7.0/rojo-7.7.0-windows-x86_64.zip\"\nExpand-Archive rojo.zip -DestinationPath rojo", code))
E.append(Paragraph("<b>Verify:</b>", body))
E.append(Paragraph("C:\\tools\\rojo\\rojo.exe --version", code))
E.append(Paragraph("Should print: Rojo 7.7.0", body))
E.append(Paragraph("<b>Gotcha:</b> You also need the Rojo plugin inside Roblox Studio. Open Studio, go to Plugins → Manage Plugins → search for Rojo → Install.", body))

# ═══ STEP 4 ═══
E.append(Paragraph("Step 4 — Connect Hermes to Your Local Model", step))
E.append(Paragraph("Hermes is already installed. Point it at Ollama:", body))
E.append(Paragraph("In Hermes config or chat settings:<br/>Model endpoint: http://localhost:11434/v1<br/>Model name: orcasaq-32k<br/>Max tokens: 4096<br/>Temperature: 0.2", body))
E.append(Paragraph("<b>Verify:</b> Ask Hermes to write a Lua function. If it responds, you're running AI on your own GPU with zero API cost.", body))
E.append(Paragraph("<b>Gotcha:</b> If Hermes can't connect, make sure Ollama is running (ollama serve in a terminal). If the model is slow, check that the PROCESSOR column in ollama ps says GPU, not CPU.", body))

# ═══ STEP 5 ═══
E.append(Paragraph("Step 5 — VS Code", step))
E.append(Paragraph("winget install Microsoft.VisualStudioCode\ncode --install-extension sumneko.lua\ncode --install-extension rojo-rbx.rojo", code))
E.append(Paragraph("<b>Verify:</b> Open VS Code, create a new file, type print(\"hello\"), save it as test.lua. You should see Lua syntax highlighting.", body))

# ═══ STEP 6 ═══
E.append(Paragraph("Step 6 — Git", step))
E.append(Paragraph("winget install Git.Git", code))
E.append(Paragraph("<b>Verify:</b> git --version", body))

# ═══ STEP 7 ═══
E.append(Paragraph("Step 7 — Get the Game Code", step))
E.append(Paragraph("The starter Luau code for your game is already written. Your dad will share the repo or the files. The five modules:", body))
game_files = [
    ["File", "What It Does"],
    ["GameConfig.lua", "Game constants and settings"],
    ["ShadowLedger.lua", "Tracks what players do"],
    ["TheAnswer.lua", "The boss fight logic"],
    ["HallOfSupper.lua", "The starting room"],
    ["ServerMain.lua", "Connects everything"],
]
gt = Table(game_files, colWidths=[150, 300])
gt.setStyle(TableStyle([
    ("FONT", (0,0), (-1,-1), "Helvetica", 9),
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), HexColor("#e8e6e3")),
    ("FONT", (0,0), (-1,0), "Helvetica-Bold", 9),
    ("GRID", (0,0), (-1,-1), 0.5, HexColor("#ddd")),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
E.append(gt)
E.append(Spacer(1, 6))
E.append(Paragraph("Put them in a folder with a default.project.json (Rojo's config). Run rojo serve, connect from Studio, and the code syncs.", body))

# ═══ FREE API KEYS ═══
E.append(Paragraph("Free API Keys (Optional)", step))
E.append(Paragraph("Sometimes you want a bigger model than your GPU can run. These are free:", body))
keys = [
    ["Service", "Sign Up At"],
    ["OpenRouter", "openrouter.ai"],
    ["Groq", "console.groq.com"],
    ["NVIDIA Build", "build.nvidia.com"],
    ["Cerebras", "cloud.cerebras.ai"],
]
kt = Table(keys, colWidths=[150, 250])
kt.setStyle(TableStyle([
    ("FONT", (0,0), (-1,-1), "Helvetica", 9),
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), HexColor("#e8e6e3")),
    ("FONT", (0,0), (-1,0), "Helvetica-Bold", 9),
    ("GRID", (0,0), (-1,-1), 0.5, HexColor("#ddd")),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
E.append(kt)
E.append(Spacer(1, 6))
E.append(Paragraph("Put keys in a .env file. One key per line: KEY_NAME=value", body))

# ═══ DAILY WORKFLOW ═══
E.append(Paragraph("Your Daily Workflow", h2))
E.append(Paragraph("Every day, same steps:", body))
E.append(Paragraph("1. Open a terminal in your game folder<br/>2. Run: rojo serve default.project.json<br/>3. Open Roblox Studio → Rojo plugin → Connect<br/>4. Ask Hermes to write code: \"Write a stamina system for a souls-like game\"<br/>5. Hermes writes the Lua file — it syncs to Studio instantly<br/>6. Press Play in Studio to test<br/>7. If it breaks, paste the error back into Hermes: \"Fix this: [error]\"<br/>8. Repeat until it works<br/>9. Publish: File → Publish to Roblox", body))

# ═══ COMMON MISTAKES ═══
E.append(Paragraph("Common Mistakes", h2))
mistakes = [
    ["Mistake", "Fix"],
    ["Ollama says 100% CPU", "Update your NVIDIA driver. Restart Ollama completely."],
    ["Rojo won't connect", "Make sure rojo serve is running in a terminal. Check the port number matches."],
    ["Script doesn't run in Studio", "Check the Output panel (View → Output). The error tells you what's wrong."],
    ["Hermes gives empty responses", "Your model consumed the token budget on thinking. Add thinking: disabled to your request."],
    ["Everything is slow", "Check ollama ps. If it says CPU, fix your GPU driver. If it says GPU but slow, reduce context length."],
]
mt = Table(mistakes, colWidths=[200, 280])
mt.setStyle(TableStyle([
    ("FONT", (0,0), (-1,-1), "Helvetica", 9),
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), HexColor("#e8e6e3")),
    ("FONT", (0,0), (-1,0), "Helvetica-Bold", 9),
    ("GRID", (0,0), (-1,-1), 0.5, HexColor("#ddd")),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
]))
E.append(mt)

# ═══ HOW YOU GET PAID ═══
E.append(Paragraph("How You Get Paid", h2))
E.append(Paragraph("Roblox pays 70% of what players spend. $0.0035 per Robux. Minimum payout: 30,000 Robux (~$105).<br/><br/>Free-to-play game → Game Pass (99 Robux: double score) → Dev Product (49 Robux: extra life) → Premium Payouts (passive income from engagement time). 430 pass sales = first payout.<br/><br/>Post your launch clip. Your development loop is instant, free, and unlimited.", body))

# ═══ LINKS ═══
E.append(Paragraph("All Links", h2))
links = [
    ["Resource", "URL"],
    ["Roblox Studio", "roblox.com/create"],
    ["Roblox Docs", "create.roblox.com/docs"],
    ["Luau Language", "luau.org"],
    ["Rojo", "rojo.space"],
    ["Ollama", "ollama.com"],
    ["OrcaSAQ-2 Model", "huggingface.co/OrcaRouter/OrcaSAQ-2-27B-gguf"],
    ["GameDev OS (free assets)", "github.com/Scenario-Games/GameDev-OS"],
    ["OpenRouter", "openrouter.ai"],
    ["Groq", "console.groq.com"],
    ["NVIDIA Build", "build.nvidia.com"],
    ["Free Game Assets", "itch.io/game-assets/free"],
    ["Free Sound Effects", "freesound.org"],
    ["Free Music", "freepd.com"],
    ["Hermes Docs", "hermes-agent.nousresearch.com/docs"],
]
lt = Table(links, colWidths=[180, 280])
lt.setStyle(TableStyle([
    ("FONT", (0,0), (-1,-1), "Helvetica", 9),
    ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), HexColor("#e8e6e3")),
    ("FONT", (0,0), (-1,0), "Helvetica-Bold", 9),
    ("GRID", (0,0), (-1,-1), 0.5, HexColor("#ddd")),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
E.append(lt)

E.append(Spacer(1, 20))
E.append(Paragraph("Build the map. The territory follows.", ParagraphStyle("close", parent=styles["Normal"], fontSize=10, textColor=BLUE, alignment=TA_CENTER)))

doc.build(E)
print("Adam setup PDF:", os.path.getsize(os.path.join("watch", "inbox", "ADAM_SETUP_20260924.pdf")), "bytes")
