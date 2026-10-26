from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
import os

DARK = HexColor("#1a1a2e")
GOLD = HexColor("#d4a040")
BLUE = HexColor("#1565c0")
DIM = HexColor("#6b7280")
LINK = HexColor("#1565c0")

styles = getSampleStyleSheet()
h2 = ParagraphStyle("H2x", parent=styles["Heading2"], fontSize=13, spaceBefore=14, spaceAfter=6)
h3 = ParagraphStyle("H3x", parent=styles["Heading3"], fontSize=11, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("Bodyx", parent=styles["BodyText"], fontSize=9.5, leading=14)
mono = ParagraphStyle("Monox", parent=styles["Code"], fontSize=8, leading=11,
                       backColor=HexColor("#f0f4f8"), borderPadding=6, leftIndent=8, spaceAfter=6)
small = ParagraphStyle("Smallx", parent=styles["Normal"], fontSize=8, textColor=DIM, spaceAfter=4)
link = ParagraphStyle("Link", parent=styles["BodyText"], fontSize=9.5, leading=14)

def link_text(url, label=None):
    return f'<link href="{url}" color="#1565c0"><u>{label or url}</u></link>'

link_body = ParagraphStyle("LinkBody", parent=body)
def link_cell(url, label=None):
    return Paragraph(f'<link href="{url}" color="#1565c0"><u>{label or url}</u></link>', link_body)

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build(path, title, sections):
    doc = SimpleDocTemplate(str(path), pagesize=A4,
        leftMargin=0.7*inch, rightMargin=0.7*inch, topMargin=0.65*inch, bottomMargin=0.65*inch)
    story = []
    story.append(Paragraph(esc(title), ParagraphStyle("TX", parent=styles["Title"], fontSize=20, spaceAfter=6)))
    story.append(Paragraph("Nacho Business × Adam · Soul Frontier · 2026-09-24", ParagraphStyle("SX", parent=styles["Normal"], fontSize=9, textColor=DIM)))
    story.append(Spacer(1, 14))
    for s in sections:
        if s.get("h"):
            story.append(Paragraph(esc(s["h"]), h2))
        for item in s.get("c", []):
            if item.get("t") == "p":
                story.append(Paragraph(item["text"], body))
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

# ═══ YOUR GAME ═══
sections.append({"h": "Soul Frontier — Your Game", "c": [
    {"t": "p", "text": "Death Must Die × Dark Souls. Top-down survivors roguelite. Stamina-based combat, wave survival, god blessings, permadeath runs. Your name on it. The estate provides the research corpus, the models, and the infrastructure. You build the game."},
    {"t": "p", "text": "A playable prototype already exists. Three characters: Twin Pistols (fast/light), Shotgun-Axe (mixed/medium), and a third slot. Canvas rendering, HUD, death screen, level transitions. The design doc defines the combat DNA (Dark Souls) and the game loop DNA (Death Must Die) and how they fuse."},
]})

# ═══ SOFTWARE SETUP ═══
sections.append({"h": "Step 1 — Software Setup", "c": [
    {"t": "p", "text": "Open PowerShell as Administrator. Run these in order."},
    {"t": "h", "text": "1a. Roblox Studio"},
    {"t": "p", "text": f'Download from {link_text("https://www.roblox.com/create", "roblox.com/create")} — click Start Creating. Free account required.'},
    {"t": "h", "text": "1b. Ollama (runs AI models on your GPU)"},
    {"t": "code", "text": "winget install Ollama.Ollama\nollama --version"},
    {"t": "h", "text": "1c. Pull your model"},
    {"t": "code", "text": "ollama pull hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf\n# 12GB, 70.0 SWE-bench, 262K context, agent-optimized\n# Verify it works:\nollama run hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf \"Write a Lua function\""},
    {"t": "h", "text": "1d. Rojo (syncs code files to Roblox Studio)"},
    {"t": "code", "text": "mkdir C:\\tools -Force; cd C:\\tools\ncurl -L -o rojo.zip \"https://github.com/rojo-rbx/rojo/releases/download/v7.7.0/rojo-7.7.0-windows-x86_64.zip\"\nExpand-Archive rojo.zip -DestinationPath rojo\n$env:PATH += \";C:\\tools\\rojo\"\n[System.Environment]::SetEnvironmentVariable(\"PATH\", $env:PATH + \";C:\\tools\\rojo\", \"User\")\nrojo --version"},
    {"t": "h", "text": "1e. VS Code + extensions"},
    {"t": "code", "text": "winget install Microsoft.VisualStudioCode\ncode --install-extension sumneko.lua\ncode --install-extension rojo-rbx.rojo"},
    {"t": "h", "text": "1f. Git"},
    {"t": "code", "text": "winget install Git.Git"},
]})

# ═══ CONNECT HERMES ═══
sections.append({"h": "Step 2 — Connect Hermes to Your Model", "c": [
    {"t": "p", "text": "Point Hermes at your local Ollama instance. In your Hermes config or chat settings:"},
    {"t": "table", "data": [
        ["Setting", "Value"],
        ["Model endpoint", "http://localhost:11434"],
        ["Model name", "hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf"],
        ["Max tokens", "4096"],
        ["Temperature", "0.2"],
    ]},
    {"t": "p", "text": "Now Hermes runs on YOUR GPU. No API key. No billing. ~40-60 tokens/second on the 5080."},
]})

# ═══ FREE API KEYS ═══
sections.append({"h": "Step 3 — Free API Keys (for bigger models)", "c": [
    {"t": "p", "text": "Your 5080 handles most tasks. For harder problems:"},
    {"t": "table", "data": [
        ["Service", "What You Get", "Sign Up"],
        ["OpenRouter", "Free access to many models", link_cell("https://openrouter.ai")],
        ["Groq", "Fastest free inference (Llama 3.3 70B)", link_cell("https://console.groq.com")],
        ["NVIDIA Build", "Free credits, 82 models", link_cell("https://build.nvidia.com")],
        ["Cerebras", "Very fast free inference", link_cell("https://cloud.cerebras.ai")],
        ["Google AI Studio", "Free Gemini access", link_cell("https://aistudio.google.com")],
    ]},
    {"t": "p", "text": "Put keys in a .env file next to your project."},
]})

# ═══ THE GAME ═══
sections.append({"h": "Step 4 — Soul Frontier Design Document", "c": [
    {"t": "h", "text": "Combat System (Dark Souls DNA)"},
    {"t": "p", "text": "Stamina-based. One bar governs everything. Resource management is the core loop."},
    {"t": "table", "data": [
        ["Action", "Stamina", "Notes"],
        ["Light swing", "1", "Fast, low damage, spammable"],
        ["Heavy swing", "3", "Slow, high damage, telegraphed"],
        ["Dodge roll", "1", "i-frames, roll THROUGH enemies"],
        ["Sprint", "1/tick", "Hold to move faster"],
    ]},
    {"t": "p", "text": "No auto-attack. No lock-on. No backstab. Enemies telegraph — slow readable wind-ups. Death is education."},
    {"t": "h", "text": "Game Loop (Death Must Die DNA)"},
    {"t": "p", "text": "Wave-based survival. Choose 3 gods per run for blessing synergy. Survive hordes, descend, defeat guardians. Runs reset on death. Persistent progression between runs through equipment and character mastery."},
]})

# ═══ THE PROTOTYPE ═══
sections.append({"h": "Step 5 — Your Prototype", "c": [
    {"t": "p", "text": "A playable prototype exists in the estate. 44KB, three characters, canvas rendering, HUD, death screen."},
    {"t": "p", "text": "The source code is at:"},
    {"t": "p", "text": link_text("C:/Users/foste/Documents/projects/local_sovereign_agent/dashboard/static/games/soul_frontier/soul_frontier.html", "dashboard/static/games/soul_frontier/soul_frontier.html")},
    {"t": "p", "text": "The design brief is at:"},
    {"t": "p", "text": link_text("C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/soul_frontier_research_20260923.md", "memory/runs/soul_frontier_research_20260923.md")},
    {"t": "p", "text": "Feed both files to Hermes as context before asking design questions. The model needs to know what's already decided."},
]})

# ═══ ROBLOX BUILD ═══
sections.append({"h": "Step 6 — Build in Roblox", "c": [
    {"t": "p", "text": "Create a new project folder. Write a Rojo project file. Sync to Studio."},
    {"t": "code", "text": "mkdir SoulFrontier\ncd SoulFrontier\n\n# Create default.project.json:\n# {\n#   \"name\": \"SoulFrontier\",\n#   \"tree\": {\n#     \"$className\": \"DataModel\",\n#     \"ServerScriptService\": {\n#       \"GameConfig\": { \"$path\": \"src/GameConfig.luau\" },\n#       \"CombatSystem\": { \"$path\": \"src/Combat.luau\" },\n#       \"WaveSpawner\": { \"$path\": \"src/Waves.luau\" },\n#       \"StaminaSystem\": { \"$path\": \"src/Stamina.luau\" }\n#     }\n#   }\n# }\n\nrojo serve default.project.json\n# Open Roblox Studio + Rojo plugin + Connect\n# Start building"},
    {"t": "p", "text": "What to build first:"},
    {"t": "table", "data": [
        ["Module", "What It Does", "Ask Your Model"],
        ["Stamina.luau", "One bar: attack, dodge, sprint all drain it", "Write a stamina system with regen and costs"],
        ["Combat.luau", "Light/heavy attacks, dodge roll with i-frames", "Write a melee combat system with hitboxes"],
        ["Waves.luau", "Spawn enemies in waves, escalate difficulty", "Write a wave spawner with difficulty scaling"],
        ["Telegraph.luau", "Enemy wind-up animations before attacking", "Write an enemy AI that telegraphs before striking"],
    ]},
]})

# ═══ FREE ASSETS ═══
sections.append({"h": "Step 7 — Free Game Assets", "c": [
    {"t": "table", "data": [
        ["Type", "Source", "License"],
        ["2D sprites", link_cell("https://itch.io/game-assets/free"), "Various"],
        ["Tilesets", link_cell("https://opengameart.org"), "CC0 / CC-BY"],
        ["3D models", link_cell("https://sketchfab.com"), "Various (free section)"],
        ["Textures", link_cell("https://polyhaven.com"), "CC0"],
        ["Sound FX", link_cell("https://freesound.org"), "CC0"],
        ["Music", link_cell("https://freepd.com"), "Public domain"],
        ["Fonts", link_cell("https://fonts.google.com"), "Open source"],
        ["GameDev OS", link_cell("https://github.com/Scenario-Games/GameDev-OS"), "Open source"],
        ["Roblox Toolbox", "Built into Studio", "Free"],
    ]},
    {"t": "p", "text": "GameDev OS: 9 AI specialists, 64 skills for game assets. Sprites, 3D rigging, textures, skyboxes, walkable worlds, music, SFX, trailers, store art. Wire into Hermes via ComfyUI workflows."},
]})

# ═══ MONETIZATION ═══
sections.append({"h": "Step 8 — How You Get Paid", "c": [
    {"t": "p", "text": "Roblox pays 70%. $0.0035 per Robux. Minimum payout: 30,000 Robux (~$105)."},
    {"t": "p", "text": "Roguelites monetize through repeat runs. Every death = another run = another chance to buy. The death loop IS the monetization loop."},
    {"t": "table", "data": [
        ["Item", "Type", "Price", "What It Does"],
        ["Extra Character", "Game Pass", "199", "Unlock a 4th character"],
        ["Stamina Refill", "Dev Product", "49", "Instant refill (once per wave)"],
        ["Soul Doubler", "Dev Product", "99", "2x souls for 30 min"],
        ["Frontier Pass", "Game Pass", "499", "Access to deeper levels"],
    ]},
    {"t": "p", "text": "Target: 430 pass sales = first payout. Post your launch clip. Your 5080 means instant, free, unlimited development iteration."},
]})

# ═══ RESEARCH CORPUS ═══
sections.append({"h": "Step 9 — The Research Corpus (Your Model's Library)", "c": [
    {"t": "p", "text": "Feed these to Hermes before asking design questions. The model needs to know what's already decided."},
    {"t": "table", "data": [
        ["File", "Feed It Because"],
        ["soul_frontier_research_20260923.md", "Your design doc: combat DNA, loop DNA, fusion"],
        ["soul_frontier.html", "Your playable prototype source"],
        ["The gaming corpus (35 games)", "Design patterns from the estate's games"],
        ["The arXiv metadata index", "3.15M papers for pathfinding, procedural gen, roguelite patterns"],
    ]},
]})

# ═══ DESIGN PRINCIPLES ═══
sections.append({"h": "Design Principles", "c": [
    {"t": "p", "text": "1. Death is education. Every death teaches the pattern. Difficulty is fair, never cheating."},
    {"t": "p", "text": "2. Stamina is the core loop. Every action is a resource decision."},
    {"t": "p", "text": "3. Telegraph and punish. Enemies wind up slowly. Mastery is pattern recognition."},
    {"t": "p", "text": "4. The map precedes the territory. Pre-register boss patterns and wave compositions. Then build to the map."},
    {"t": "p", "text": "5. The game is a tool for the player, not a substitute for the player."},
]})

# ═══ QUICK REFERENCE ═══
sections.append({"h": "Quick Reference", "c": [
    {"t": "table", "data": [
        ["Command", "What It Does"],
        ["rojo serve default.project.json", "Start code sync server"],
        ["ollama run <model>", "Chat with local model"],
        ["ollama ps", "See what's in VRAM"],
        ["git pull", "Get latest code"],
        ["code .", "Open VS Code here"],
    ]},
    {"t": "h", "text": "Daily Workflow"},
    {"t": "code", "text": "1. rojo serve default.project.json\n2. Open Roblox Studio + Rojo Connect\n3. Edit Lua in VS Code — syncs instantly\n4. Press Play to test\n5. File > Publish to Roblox when ready"},
]})

# ═══ LINKS ═══
sections.append({"h": "All Links", "c": [
    {"t": "table", "data": [
        ["Resource", "URL"],
        ["Roblox Studio", link_text("https://www.roblox.com/create")],
        ["Roblox Creator Docs", link_text("https://create.roblox.com/docs")],
        ["Luau Language", link_text("https://luau.org")],
        ["Rojo", link_text("https://rojo.space")],
        ["Ollama", link_text("https://ollama.com")],
        ["OrcaSAQ-2 Model", link_text("https://huggingface.co/OrcaRouter/OrcaSAQ-2-27B-gguf")],
        ["GameDev OS", link_cell("https://github.com/Scenario-Games/GameDev-OS")],
        ["OpenRouter", link_cell("https://openrouter.ai")],
        ["Groq Console", link_cell("https://console.groq.com")],
        ["NVIDIA Build", link_cell("https://build.nvidia.com")],
        ["itch.io Free Assets", link_cell("https://itch.io/game-assets/free")],
        ["OpenGameArt", link_cell("https://opengameart.org")],
        ["Poly Haven", link_cell("https://polyhaven.com")],
        ["FreeSound", link_cell("https://freesound.org")],
        ["FreePD", link_cell("https://freepd.com")],
        ["Hermes Docs", link_text("https://hermes-agent.nousresearch.com/docs")],
    ]},
]})

# ═══ CLOSE ═══
sections.append({"h": "Close", "c": [
    {"t": "p", "text": "Your GPU is the engine. The model is the brain. The game is the body. The map precedes the territory — build the map, and the territory follows. The research corpus is loaded. The model is pulled. The prototype exists. The design doc is written. Now build."},
]})

sz = build("watch/inbox/ADAM_SOUL_FRONTIER_SETUP_20260924.pdf", "Soul Frontier — Complete Setup and Build Guide", sections)
print(f"Soul Frontier complete guide: {sz} bytes")
