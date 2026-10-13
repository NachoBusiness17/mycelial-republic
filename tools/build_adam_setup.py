from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
import os

DARK = HexColor("#1a1a2e")
BLUE = HexColor("#1565c0")
DIM = HexColor("#6b7280")
ACCENT = HexColor("#0d213f")

styles = getSampleStyleSheet()
h2 = ParagraphStyle("H2x", parent=styles["Heading2"], fontSize=13, spaceBefore=14, spaceAfter=6)
h3 = ParagraphStyle("H3x", parent=styles["Heading3"], fontSize=11, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("Bodyx", parent=styles["BodyText"], fontSize=9.5, leading=14)
mono = ParagraphStyle("Monox", parent=styles["Code"], fontSize=8, leading=11, backColor=HexColor("#f1f5f9"), borderPadding=4, leftIndent=8)
small = ParagraphStyle("Smallx", parent=styles["Normal"], fontSize=8, textColor=DIM, spaceAfter=4)

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build(path, title, sections):
    doc = SimpleDocTemplate(str(path), pagesize=A4,
        leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.7*inch, bottomMargin=0.7*inch)
    story = []
    story.append(Paragraph(esc(title), ParagraphStyle("TX", parent=styles["Title"], fontSize=18, spaceAfter=6)))
    story.append(Paragraph("Nacho Business × Adam · 2026-09-24", ParagraphStyle("SX", parent=styles["Normal"], fontSize=9, textColor=DIM)))
    story.append(Spacer(1, 12))
    for s in sections:
        if s.get("h"):
            story.append(Paragraph(esc(s["h"]), h2))
        for item in s.get("c", []):
            if item.get("t") == "p":
                story.append(Paragraph(esc(item["text"]), body))
            elif item.get("t") == "code":
                story.append(Paragraph(esc(item["text"]), mono))
                story.append(Spacer(1, 4))
            elif item.get("t") == "table":
                t = Table(item["data"], colWidths=item.get("w"))
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
            elif item.get("t") == "note":
                story.append(Paragraph(esc(item["text"]), small))
    doc.build(story)
    return os.path.getsize(str(path))


sections = []

# ═══ WHAT YOU HAVE ═══
sections.append({"h": "What You Have", "c": [
    {"t": "p", "text": "An NVIDIA RTX 5080 (16GB VRAM, CUDA). This runs AI models locally that most people need cloud APIs for. Hermes Agent is already installed. Here is everything else you need, in order, with the exact commands."},
]})

# ═══ SOFTWARE ═══
sections.append({"h": "Software Setup (PowerShell)", "c": [
    {"t": "h", "text": ""} if False else {"t": "p", "text": "Open PowerShell as Administrator. Run these in order."},
    {"t": "h", "text": "Step 1: Roblox Studio"},
    {"t": "code", "text": "# Download and install Roblox Studio\n# Go to https://www.roblox.com/create and click \"Start Creating\"\n# Follow the installer prompts. Free account required.\n\n# Verify: open Roblox Studio after install\n# You should see the Baseplate template"},
    {"t": "h", "text": "Step 2: Ollama (local AI runtime)"},
    {"t": "code", "text": "# Download and install from https://ollama.com/download/windows\n# Or use winget:\nwinget install Ollama.Ollama\n\n# Verify:\nollama --version"},
    {"t": "h", "text": "Step 3: Pull your model (OrcaSAQ-2 27B — fits your 5080)"},
    {"t": "code", "text": "ollama pull hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf\n\n# Verify it generates:\nollama run hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf \"Write a Lua function that prints hello\"\n\n# Type /bye to exit"},
    {"t": "h", "text": "Step 4: Rojo (code sync for Roblox Studio)"},
    {"t": "code", "text": "# Create a tools directory\nmkdir C:\\tools -Force\ncd C:\\tools\n\n# Download Rojo 7.7.0\ncurl -L -o rojo.zip \"https://github.com/rojo-rbx/rojo/releases/download/v7.7.0/rojo-7.7.0-windows-x86_64.zip\"\nExpand-Archive rojo.zip -DestinationPath rojo\n\n# Add to PATH (permanent)\n$env:PATH += \";C:\\tools\\rojo\"\n[System.Environment]::SetEnvironmentVariable(\"PATH\", $env:PATH + \";C:\\tools\\rojo\", \"User\")\n\n# Verify:\nrojo --version"},
    {"t": "h", "text": "Step 5: VS Code + Lua extension"},
    {"t": "code", "text": "winget install Microsoft.VisualStudioCode\n\n# Install Lua extension\ncode --install-extension sumneko.lua\n\n# Install Rojo extension (for Studio integration)\ncode --install-extension rojo-rbx.rojo"},
    {"t": "h", "text": "Step 6: Git (for cloning the game code)"},
    {"t": "code", "text": "winget install Git.Git\n\n# Clone the game project\ngit clone https://github.com/NachoBusiness/game_roblox.git\ncd game_roblox\n\n# If the repo is private, ask for access"},
]})

# ═══ CONNECT HERMES ═══
sections.append({"h": "Connect Hermes to Your Local Model", "c": [
    {"t": "p", "text": "Hermes needs to know about your local Ollama instance. In your Hermes config or chat, set:"},
    {"t": "code", "text": "Model endpoint: http://localhost:11434\nModel name: hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf\nMax tokens: 4096\nTemperature: 0.2"},
    {"t": "p", "text": "Now Hermes runs on YOUR GPU. No API key. No billing. Your 5080 does the thinking at ~40-60 tokens/second. You can also connect Hermes to free API keys for bigger models when you need them (see Free API Keys below)."},
]})

# ═══ FREE API KEYS ═══
sections.append({"h": "Free API Keys (for bigger models)", "c": [
    {"t": "p", "text": "Your 5080 handles most tasks locally. For harder problems, these services give free API keys:"},
    {"t": "table", "data": [
        ["Service", "What You Get", "Sign Up At"],
        ["OpenRouter", "Free access to many models", "openrouter.ai"],
        ["Groq", "Fastest free inference", "console.groq.com"],
        ["NVIDIA Build", "Free credits, 82 models", "build.nvidia.com"],
        ["Cerebras", "Very fast free inference", "cloud.cerebras.ai"],
    ]},
    {"t": "p", "text": "Put keys in a .env file next to your project. Format: KEY_NAME=value"},
]})

# ═══ THE GAME CODE ═══
sections.append({"h": "The Game Code (Already Written)", "c": [
    {"t": "p", "text": "The estate already wrote the Luau code for your first game. Clone it and sync:"},
    {"t": "code", "text": "# Clone the game project\ngit clone https://github.com/NachoBusiness/game_roblox.git\ncd game_roblox\n\n# Start the Rojo sync server\nrojo serve default.project.json\n\n# Keep this terminal open. It serves on port 34872."},
    {"t": "p", "text": "Then in Roblox Studio:\n1. Install the Rojo plugin (Plugins > Manage Plugins)\n2. Click Rojo > Connect\n3. Enter localhost:34872\n4. The Lua code appears in Studio\n5. Press Play"},
    {"t": "table", "data": [
        ["File", "What It Does"],
        ["GameConfig.lua", "Shared constants: 6 chairs, boss phases, narrative"],
        ["ShadowLedger.lua", "The hall's private record of what each player chose"],
        ["TheAnswer.lua", "The boss: 5 phases, 15-degree tell, light deflection"],
        ["HallOfSupper.lua", "The spawn room: 6 empty chairs, counting, the mural"],
        ["ServerMain.lua", "Boot sequence connecting everything"],
    ]},
]})

# ═══ THE GAME ITSELF ═══
sections.append({"h": "What The Game Is", "c": [
    {"t": "p", "text": "The Ledger of Empty Chairs. Six empty chairs at supper. Count them and candles light. Ignore them and the mural weeps. Sit in one and the count breaks. The hall files which you chose."},
    {"t": "p", "text": "The boss is called The Answer. Five phases. In Phase 3 it deflects every attack at a 15-degree angle — that angle comes from real research data in the estate's corpus. In Phase 4, light bends around it. In Phase 5, the system's own orbital laser arrives. The player wins by standing the boss under it."},
    {"t": "p", "text": "The rule: never state the truth. Hint. Let the player connect it themselves."},
]})

# ═══ FREE ASSETS ═══
sections.append({"h": "Free Game Assets and Tools", "c": [
    {"t": "h", "text": "GameDev OS by Scenario (open source)"},
    {"t": "p", "text": "9 AI specialists and 64 skills for game asset generation: 2D sprites, 3D models, rigging, textures, skyboxes, walkable worlds, music, SFX, cinematic trailers, store art. Wire into your coding agent via ComfyUI workflows."},
    {"t": "code", "text": "git clone https://github.com/scenario-gamedev/gamedev-os.git"},
    {"t": "h", "text": "Free asset sources"},
    {"t": "code", "text": "# 2D sprites and tilesets\n# itch.io/game-assets/free — thousands of free packs\n# opengameart.org — CC0 and CC-BY assets\n\n# 3D models\n# sketchfab.com — free section\n# polyhaven.com — CC0 HDRIs, textures, models\n\n# Sound and music\n# freesound.org — CC0 sound effects\n# freepd.com — public domain music\n# sonicpix.org — free game music\n\n# Fonts\n# fonts.google.com — open source fonts"},
    {"t": "h", "text": "Roblox-specific tools"},
    {"t": "code", "text": "# Roblox default assets (free, built into Studio)\n# Toolbox in Studio: models, meshes, sounds, images\n\n# Rojo for code sync (already installed above)\n# Wally for package management: https://wally.run/\n# TestEZ for unit testing: https://github.com/Roblox/TestEZ"},
]})

# ═══ MONETIZATION ═══
sections.append({"h": "How You Get Paid", "c": [
    {"t": "p", "text": "Roblox pays developers 70% of what players spend. $0.0035 per Robux. Minimum payout: 30,000 Robux (~$105)."},
    {"t": "p", "text": "The path: free-to-play game, sell a Game Pass (99 Robux: double score), sell a Dev Product (49 Robux: extra life), enable Premium Payouts. 430 pass sales = first payout. Post your launch clip. Your 5080 means instant, free, unlimited development."},
]})

# ═══ QUICK REFERENCE ═══
sections.append({"h": "Quick Reference Card", "c": [
    {"t": "table", "data": [
        ["Command", "What It Does"],
        ["rojo serve default.project.json", "Start the code sync server"],
        ["ollama pull <model>", "Download a new AI model"],
        ["ollama run <model>", "Chat with a local model"],
        ["ollama ps", "See what's loaded in VRAM"],
        ["git pull", "Get the latest game code"],
        ["code .", "Open VS Code in current directory"],
    ]},
    {"t": "h", "text": "Daily workflow"},
    {"t": "code", "text": "1. cd game_roblox\n2. rojo serve default.project.json\n3. Open Roblox Studio + Rojo plugin + Connect\n4. Edit Lua files in VS Code — changes sync instantly\n5. Press Play in Studio to test\n6. When ready: File > Publish to Roblox"},
    {"t": "h", "text": "When you need help"},
    {"t": "code", "text": "# Ask Hermes (running on your 5080):\n# \"Write a Lua script that [does X]\"\n# \"How do I make a part glow in Roblox?\"\n# \"Debug this Roblox error: [paste error]\"\n\n# The estate's free lanes (all metered):\n# DeepSeek API — $0.14/M tokens, fastest workhorse\n# OpenRouter — free tier, auto-routing\n# NVIDIA Build — free credits, 82 models"},
]})

# ═══ BIBLIOGRAPHY ═══
sections.append({"h": "References", "c": [
    {"t": "body", "text": "Roblox Creator Hub: create.roblox.com/docs. Rojo: rojo.space. Ollama: ollama.com. GameDev OS: github.com/Scenario-Games/GameDev-OS. Luau documentation: luau.org. Roblox Lua style guide: roblox.dev/articles/style-guide."},
]})

sz = build("watch/inbox/ADAM_SETUP_GUIDE_20260924.pdf", "Adam's Setup Guide — AI Game Development", sections)
print(f"Adam setup guide PDF: {sz} bytes")
