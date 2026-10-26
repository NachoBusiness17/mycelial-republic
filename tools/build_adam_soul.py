from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
import os

DARK = HexColor("#1a1a2e")
GOLD = HexColor("#d4a040")
BLUE = HexColor("#1565c0")
DIM = HexColor("#6b7280")

styles = getSampleStyleSheet()
h2 = ParagraphStyle("H2x", parent=styles["Heading2"], fontSize=13, spaceBefore=14, spaceAfter=6)
h3 = ParagraphStyle("H3x", parent=styles["Heading3"], fontSize=11, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("Bodyx", parent=styles["BodyText"], fontSize=9.5, leading=14)
mono = ParagraphStyle("Monox", parent=styles["Code"], fontSize=8, leading=11, backColor=HexColor("#f1f5f9"), borderPadding=4, leftIndent=8)
small = ParagraphStyle("Smallx", parent=styles["Normal"], fontSize=8, textColor=DIM)

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build(path, title, sections):
    doc = SimpleDocTemplate(str(path), pagesize=A4,
        leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.7*inch, bottomMargin=0.7*inch)
    story = []
    story.append(Paragraph(esc(title), ParagraphStyle("TX", parent=styles["Title"], fontSize=18, spaceAfter=6)))
    story.append(Paragraph("Nacho Business × Adam · Soul Frontier · 2026-09-24", ParagraphStyle("SX", parent=styles["Normal"], fontSize=9, textColor=DIM)))
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

# ═══ YOUR GAME ═══
sections.append({"h": "Your Game: Soul Frontier", "c": [
    {"t": "p", "text": "Death Must Die × Dark Souls — top-down survivors roguelite. Your game. Your name on it. The estate provides the research, the models, and the infrastructure. You build the game."},
    {"t": "p", "text": "The prototype already exists at dashboard/static/games/soul_frontier/soul_frontier.html (44KB, playable in a browser). Three characters: Twin Pistols (fast/light), Shotgun-Axe (mixed/medium), and a third slot. Canvas-based rendering with HUD, death screen, level transitions."},
    {"t": "p", "text": "The research brief is at memory/runs/soul_frontier_research_20260923.md. It defines the combat DNA (Dark Souls) and the game loop DNA (Death Must Die) and how they fuse."},
]})

# ═══ COMBAT SYSTEM ═══
sections.append({"h": "Combat System (Dark Souls DNA)", "c": [
    {"t": "p", "text": "Stamina-based. One bar governs everything: attack, dodge, block, sprint. Resource management is the core loop. Risk-reward per action."},
    {"t": "table", "data": [
        ["Action", "Stamina Cost", "Notes"],
        ["Light swing", "1", "Fast, low damage, can spam"],
        ["Heavy swing", "3", "Slow, high damage, telegraphed"],
        ["Dodge roll", "1", "i-frames, can roll THROUGH enemies"],
        ["Block", " stamina", "NOT available (all chars)"],
        ["Sprint", "1/tick", "Hold to move faster"],
    ]},
    {"t": "p", "text": "Enemies telegraph their attacks. Slow, readable wind-ups. The threat you can read is the threat you can master. Death is education — every death teaches the pattern."},
    {"t": "p", "text": "No auto-attack. No lock-on. No backstab. No persistent upgrades within a run. Manual movement + manual attack + dodge-roll with i-frames."},
]})

# ═══ GAME LOOP ═══
sections.append({"h": "Game Loop (Death Must Die DNA)", "c": [
    {"t": "p", "text": "Wave-based survival. Survive hordes, descend deeper, defeat guardians. Runs reset on death."},
    {"t": "table", "data": [
        ["System", "Description"],
        ["God blessing system", "Choose 3 gods per run, strategic blessing synergy"],
        ["Character roster", "Multiple heroes with distinct playstyles"],
        ["Wave progression", "Survive, descend, guardian fight, repeat"],
        ["Death loop", "Death teaches the pattern, runs reset, you get better"],
    ]},
    {"t": "p", "text": "Between runs: persistent progression through equipment and character mastery. Within runs: everything is temporary. The tension is between building your character THIS run and learning the patterns for NEXT run."},
]})

# ═══ YOUR MODEL ═══
sections.append({"h": "Your AI Model (OrcaSAQ-2 27B on your 5080)", "c": [
    {"t": "p", "text": "12GB, fits your 16GB VRAM, 70.0 SWE-bench, 262K context. This model can hold your ENTIRE game codebase in context and reason about it. Point Hermes at http://localhost:11434."},
    {"t": "p", "text": "What to ask it:"},
    {"t": "code", "text": "# Design questions:\n\"Review my stamina system. Is the cost balance right for a souls-like?\"\n\"Design 3 enemy types for the first wave that teach dodge-rolling\"\n\"Write a Luau boss AI that telegraphs attacks before striking\"\n\n# Code generation:\n\"Write the wave spawner module in Luau for Roblox\"\n\"Implement a stamina bar UI that drains on attack and refills over time\"\n\"Create a character selection screen with 3 classes\"\n\n# Debug:\n\"My enemies are walking through walls. Here's my collision code: [paste]\""},
]})

# ═══ THE RESEARCH CORPUS ═══
sections.append({"h": "The Gaming Research Corpus (Your Model's Library)", "c": [
    {"t": "p", "text": "The estate has a gaming corpus you feed to your model so it knows game design. Load these into Hermes as context documents:"},
    {"t": "table", "data": [
        ["File", "What It Contains"],
        ["soul_frontier_research_20260923.md", "Your game's design doc: combat DNA, loop DNA, fusion design"],
        ["soul_frontier.html", "Your playable prototype (44KB, full source)"],
        ["game_design corpus/*", "Design patterns from the estate's 35 games"],
        ["ARISTOCRACY_LEDGER_RECEIPTS", "Evidence verification methodology (for game mechanics too)"],
    ]},
    {"t": "p", "text": "Feed these to Hermes before asking design questions. The model needs to know what you've already decided before it can help you build the next thing."},
    {"t": "p", "text": "Also load the arXiv metadata index (1.6GB, all 3.15M papers) so when you ask about pathfinding algorithms, procedural generation, or roguelite design patterns, the model can find and cite the actual research papers."},
]})

# ═══ ROBLOX SETUP ═══
sections.append({"h": "Roblox Setup (PowerShell)", "c": [
    {"t": "code", "text": "# 1. Roblox Studio\n# Go to roblox.com/create, download and install\n\n# 2. Ollama\nwinget install Ollama.Ollama\nollama pull hf.co/OrcaRouter/OrcaSAQ-2-27B-gguf\n\n# 3. Rojo\nmkdir C:\\tools -Force; cd C:\\tools\ncurl -L -o rojo.zip \"https://github.com/rojo-rbx/rojo/releases/download/v7.7.0/rojo-7.7.0-windows-x86_64.zip\"\nExpand-Archive rojo.zip -DestinationPath rojo\n$env:PATH += \";C:\\tools\\rojo\"\n\n# 4. VS Code\nwinget install Microsoft.VisualStudioCode\ncode --install-extension sumneko.lua\n\n# 5. Git\nwinget install Git.Git"},
    {"t": "p", "text": "Then: rojo serve your-game.project.json. Open Roblox Studio. Connect. Build."},
]})

# ═══ FREE ASSETS ═══
sections.append({"h": "Free Assets", "c": [
    {"t": "table", "data": [
        ["Type", "Source", "License"],
        ["2D sprites", "itch.io/game-assets/free", "Various (check each)"],
        ["Tilesets", "opengameart.org", "CC0 and CC-BY"],
        ["3D models", "sketchfab.com (free section)", "Various"],
        ["Textures", "polyhaven.com", "CC0"],
        ["Sound effects", "freesound.org", "CC0"],
        ["Music", "freepd.com", "Public domain"],
        ["Fonts", "fonts.google.com", "Open source"],
        ["GameDev OS", "github.com/Scenario-Games/GameDev-OS", "Open source"],
    ]},
    {"t": "p", "text": "GameDev OS: 9 AI specialists and 64 skills for game asset generation. 2D sprites, 3D rigging, textures, skyboxes, walkable worlds, music, SFX, trailers. Wire into Hermes via ComfyUI workflows."},
]})

# ═══ MONETIZATION ═══
sections.append({"h": "How You Get Paid", "c": [
    {"t": "p", "text": "Roblox pays 70%. $0.0035 per Robux. Minimum payout: 30,000 Robux (~$105)."},
    {"t": "p", "text": "Soul Frontier is an Action/Roguelite — mid-tier earning potential. The key monetization hooks for this genre:"},
    {"t": "table", "data": [
        ["Item", "Type", "Price (Robux)", "What It Does"],
        ["Extra Character Slot", "Game Pass", "199", "Unlock a 4th character"],
        ["Stamina Refill", "Dev Product", "49", "Instant stamina refill (once per wave)"],
        ["Soul Doubler", "Dev Product", "99", "2x souls for 30 minutes"],
        ["The Frontier Pass", "Game Pass", "499", "Access to deeper levels"],
    ]},
    {"t": "p", "text": "Roguelites monetize through repeat runs. Every death = another run = another chance to buy a stamina refill or soul doubler. The death loop IS the monetization loop."},
    {"t": "p", "text": "Target: 430 pass sales = first payout (~$105). With the estate's X audience driving traffic, 2-4 weeks is realistic."},
]})

# ═══ PRINCIPLES ═══
sections.append({"h": "Design Principles (from the corpus)", "c": [
    {"t": "p", "text": "1. Death is education. Every death teaches the pattern. Difficulty is fair, never cheating."},
    {"t": "p", "text": "2. Stamina is the core loop. Attack, dodge, sprint all draw from one bar. Every action is a resource decision."},
    {"t": "p", "text": "3. Telegraph and punish. Enemies wind up slowly. The player reads the tell and responds. Mastery is pattern recognition."},
    {"t": "p", "text": "4. The map precedes the territory. Pre-register your boss patterns, your wave compositions, your level layouts. Then build to the map."},
    {"t": "p", "text": "5. The game is a tool for the player, not a substitute for the player. The system presents challenges. The player overcomes them. The game doesn't play itself."},
]})

# ═══ BIBLIOGRAPHY ═══
sections.append({"h": "Bibliography", "c": [
    {"t": "body", "text": "FromSoftware (2011). Dark Souls. Namco Bandai. [Combat system reference: stamina, telegraph-and-punish, dodge-roll i-frames, bonfire loop]"},
    {"t": "body", "text": "Belmonte, A. (2024). Death Must Die. Realm Archive. [Survivors loop reference: wave-based, god blessings, character roster, persistent progression]"},
    {"type": "body", "text": "Gilens & Page (2014). Perspectives on Politics, 12(3). DOI 10.1017/S1537592714001595. [Methodology reference: how to verify claims with primary data]"},
    {"t": "body", "text": "Lermen et al. (2026). Large-scale deanonymization with LLMs. USENIX Security. arXiv:2602.16800. [Privacy reference: your model usage is not anonymous]"},
    {"t": "body", "text": "Roblox Creator Hub. create.roblox.com/docs. [Platform documentation: Luau, DataStore, monetization]"},
    {"t": "body", "text": "Rojo. rojo.space. [Code sync tool: file-based Roblox development]"},
]})

sz = build("watch/inbox/ADAM_SOUL_FRONTIER_20260924.pdf", "Soul Frontier — Setup, Design, and Build Guide", sections)
print(f"Soul Frontier guide: {sz} bytes")
