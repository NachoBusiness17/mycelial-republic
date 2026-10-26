# mcp-docs item: build the three deliverables via the LOCAL fallback path
# (no document MCP server exists in this session's surface; see mcp-docs.md).
# python-docx 1.2.0 + python-pptx 1.0.2 installed to a TEMP target dir from PyPI
# wheels (shared .venv untouched); reportlab + pypdf already live in the venv.
import os, sys, zipfile

BANK = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\burn_reset_20260927\flash50"
LIBS = r"C:\Users\foste\AppData\Local\Temp\mcpdoc_libs"
sys.path.insert(0, LIBS)

DATE = "2026-09-28"
TITLE = "MCP Document Tools: Dogfood Report"

# ---------------------------------------------------------------- DOCX
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()

# page header (every page)
hdr = doc.sections[0].header.paragraphs[0]
hdr.text = "MCP Document Tools Dogfood Report | flash50 | " + DATE

# title page
doc.add_heading(TITLE, 0)
doc.add_paragraph("Item mcp-docs, bank watch/inbox/burn_reset_20260927/flash50/mcp-docs.md")
doc.add_paragraph("Built " + DATE + " by the flash50 workflow lane (fallback path, not MCP)")
doc.add_paragraph("")

# real Word TOC field (Word populates it on F9 / update-fields)
tocp = doc.add_paragraph()
fld = OxmlElement("w:fldSimple")
fld.set(qn("w:instr"), 'TOC \\o "1-3" \\h \\z \\u')
r = OxmlElement("w:r"); t = OxmlElement("w:t")
t.text = "Table of Contents (update fields in Word to populate)"
r.append(t); fld.append(r)
tocp._p.append(fld)

# manual static TOC so the deliverable shows a TOC even without a field update
for line in [
    "1. Scope and Method",
    "2. The Reachable MCP Surface",
    "3. What the MCP Ecosystem Offers",
    "4. What Works",
    "5. What Is Clunky",
    "6. What Is Missing",
    "7. Fallback Build Receipt",
    "8. Verdict",
]:
    doc.add_paragraph(line)

doc.add_page_break()

doc.add_heading("1. Scope and Method", level=1)
doc.add_paragraph(
    "The ask ordered dogfooding of the document MCP tools: build a DOCX with title page, "
    "headers, table of contents and body paragraphs; a three slide PPTX; and a PDF. This "
    "session's MCP surface contains no document creation server. The surface was verified "
    "two ways: the tool list exposed to this seat, and the host config at "
    "C:/Users/foste/.zcode/cli/config.json, whose mcp.servers block names node_repl, "
    "cua_repl, web-search, web-reader, zread, zai-vision (each plus an -sd duplicate). "
    "None of these creates DOCX, PPTX or PDF."
)
doc.add_paragraph(
    "Method: document the reachable surface, dogfood the document adjacent tools that do "
    "exist (web-reader, z.ai web search, mapbox-docs), research the document MCP server "
    "ecosystem from first hand fetched READMEs, then produce the three real deliverables "
    "through a clearly labeled local fallback: python-docx, python-pptx, reportlab. The "
    "fallback is a substitute, not the ask's check; the ask's MCP document tool calls were "
    "not run because no such tool is reachable from this seat."
)

doc.add_heading("2. The Reachable MCP Surface", level=1)
doc.add_paragraph(
    "86 tools across 7 packs, counted from the seat's own function list: mapbox core 31, "
    "mapbox-devkit 22, mapbox-docs 3, android-emulator 23, mimosa security scan 5, "
    "image-search 1, web-reader 1. Read side document work exists (web-reader converts any "
    "URL to markdown; mapbox-docs searches and fetches docs). Write side document work is "
    "absent."
)
tbl = doc.add_table(rows=1, cols=3)
tbl.style = "Table Grid"
for i, h in enumerate(["Pack", "Tools", "Document relevance"]):
    tbl.rows[0].cells[i].text = h
rows = [
    ("mapbox core + devkit", "53", "geo and style tooling; no document output"),
    ("mapbox-docs", "3", "read side: search and fetch vendor docs (dogfooded OK)"),
    ("android-emulator", "23", "device automation; none"),
    ("mimosa", "5", "project security scan; none"),
    ("image-search", "1", "web image search; none"),
    ("web-reader (z.ai)", "1", "read side: URL to markdown (dogfooded, then 429)"),
    ("document creation", "0", "no DOCX, PPTX or PDF server configured"),
]
for a, b, c in rows:
    cells = tbl.add_row().cells
    cells[0].text = a; cells[1].text = b; cells[2].text = c

doc.add_heading("3. What the MCP Ecosystem Offers", level=1)
doc.add_paragraph(
    "Office-Word-MCP-Server (GongRzhe, FastMCP over python-docx, uvx runnable): about 50 "
    "tools across 8 groups: document management (create_document, get_document_info, "
    "get_document_outline, copy_document, convert_to_pdf), content addition (add_heading, "
    "add_paragraph, add_table, add_picture, add_page_break), insert near text, formatting "
    "(format_text, search_and_replace, create_custom_style), about 15 table tools, comment "
    "extraction, protection. README fetched first hand via web-reader MCP during this item."
)
doc.add_paragraph(
    "Office-PowerPoint-MCP-Server (GongRzhe, python-pptx): 34 tools over 11 modules: "
    "presentation create and open, slide add from templates, text box add and format, "
    "bulleted lists, images, tables, charts, shapes, slide notes, presentation info. README "
    "fetched first hand via web-reader MCP during this item."
)
doc.add_paragraph(
    "PDF side is thinner and read/convert heavy: hanweg/mcp-pdf-tools (pypdf; merge PDFs, "
    "extract pages, plus markdown notes storage), PDF Toolkit MCP Server (16 tools "
    "including create PDF from Markdown, fill forms, split, watermark, encrypt), mcp-pdf on "
    "PyPI (49 tools: extraction, form fill and create, assembly), xt765/mcp-document-"
    "converter (5 format conversion), smelt (PDF, DOCX, PPTX, XLSX to text). Found via the "
    "z.ai web search MCP; its backend rate limited 7 of this session's 9 queries with MCP "
    "error -429 code 1302 before answering."
)

doc.add_heading("4. What Works", level=1)
doc.add_paragraph(
    "Read side is genuinely good: web-reader returned the full Word server README as clean "
    "markdown in one call, and the mapbox-docs pair (search then fetch) worked end to end "
    "from this session. The flagship Office servers are real: tool counts are high, they "
    "map closely onto python-docx and python-pptx capabilities, and they install as "
    "one line uvx or npx servers. Table support in the Word server is unusually deep "
    "(about 15 formatting tools)."
)

doc.add_heading("5. What Is Clunky", level=1)
doc.add_paragraph(
    "One tool per operation: the Word server exposes about 50 narrow tools, so an agent "
    "burns many round trips to build one formatted report; a create-from-markdown or "
    "build-report composite call would fit agent use better. The Word server's own "
    "troubleshooting list admits sharp edges: missing styles need fallback, images need "
    "absolute paths, table cells index from zero, hex colors must omit the hash, cell text "
    "formatting must be applied after content, and auto-fit overrides manual column widths. "
    "python-docx cannot compute a table of contents; a real TOC field only populates when "
    "Word itself opens and updates it, which is why the flagship server simply has no TOC "
    "tool. Rate limits hurt: the z.ai search and read backends threw MCP -429 code 1302 on "
    "7 of 9 searches and 2 follow up reads this session; the envelope law (contact is a "
    "HOLD signal, the limit is rolling throughput) held."
)

doc.add_heading("6. What Is Missing", level=1)
doc.add_paragraph(
    "In this session: any document creation server at all. In the flagship Word server: "
    "table of contents, headers and footers, page numbers, tracked changes authoring. In "
    "the PPTX server: no PDF export (python-pptx cannot render; needs LibreOffice or "
    "PowerPoint COM). Across the PDF servers: creation is an afterthought; the ecosystem is "
    "merge, split, extract and fill first, generate second. Nobody ships a single "
    "write-me-a-formatted-report tool that spans DOCX, PPTX and PDF."
)

doc.add_heading("7. Fallback Build Receipt", level=1)
doc.add_paragraph(
    "Deliverables built " + DATE + " in flash50: mcp-docs-report.docx (this file: title "
    "page, page header, TOC field plus manual TOC, 8 numbered heading sections, body "
    "paragraphs, a 3 column tool census table), mcp-docs-report.pptx (3 slides), "
    "mcp-docs-report.pdf (reportlab). Libraries: python-docx 1.2.0 and python-pptx 1.0.2 "
    "downloaded as wheels and installed to a temp target dir so the shared venv stayed "
    "untouched; reportlab and pypdf were already in the venv. Build script banked as "
    "_mcpdoc_build.py. Every file reopened and verified after write (see the bank note)."
)

doc.add_heading("8. Verdict", level=1)
doc.add_paragraph(
    "The document MCP pattern works where it exists: a FastMCP server over python-docx or "
    "python-pptx is thin glue over mature libraries, and the read side of this session's "
    "surface proved the loop end to end. The gap is fleet side, not ecosystem side: this "
    "host simply has no document pack enabled. Cheapest fix: add a local FastMCP document "
    "server (Word plus PPTX plus reportlab PDF, one composite build-report tool per "
    "format) as a stdio server in the host config, reusing the exact fallback code this "
    "item banked. The deliverables in flash50 are the proof artifacts."
)

docx_path = os.path.join(BANK, "mcp-docs-report.docx")
doc.save(docx_path)

# ---------------------------------------------------------------- PPTX
from pptx import Presentation
from pptx.util import Pt

prs = Presentation()

s1 = prs.slides.add_slide(prs.slide_layouts[0])
s1.shapes.title.text = TITLE
s1.placeholders[1].text = "Item mcp-docs | flash50 | " + DATE

s2 = prs.slides.add_slide(prs.slide_layouts[1])
s2.shapes.title.text = "The reachable surface has no document tools"
tf = s2.placeholders[1].text_frame
tf.text = "86 MCP tools in 7 packs; zero create DOCX, PPTX or PDF"
for b in [
    "Read side exists: web-reader fetched 2 server READMEs; mapbox-docs search+fetch OK",
    "Write side absent: host config mcp.servers names no document server",
    "z.ai search/read backends: MCP -429 code 1302 on 7 of 9 searches this session",
]:
    p = tf.add_paragraph(); p.text = b

s3 = prs.slides.add_slide(prs.slide_layouts[1])
s3.shapes.title.text = "Ecosystem findings and the fallback verdict"
tf = s3.placeholders[1].text_frame
tf.text = "Word MCP server: about 50 tools, deep tables, but no TOC or headers tool"
for b in [
    "PPTX MCP server: 34 tools; no PDF export path",
    "PDF servers: merge/split/extract first, create second",
    "Deliverables here built by python-docx 1.2.0 + python-pptx 1.0.2 + reportlab",
    "Fix: one local FastMCP document pack with a composite build-report tool",
]:
    p = tf.add_paragraph(); p.text = b

pptx_path = os.path.join(BANK, "mcp-docs-report.pptx")
prs.save(pptx_path)

# ---------------------------------------------------------------- PDF
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

styles = getSampleStyleSheet()
story = [
    Paragraph(TITLE, styles["Title"]),
    Paragraph("Item mcp-docs | flash50 | " + DATE + " | fallback build via reportlab", styles["Italic"]),
    Spacer(1, 14),
    Paragraph("Scope", styles["Heading1"]),
    Paragraph(
        "The ask ordered document MCP dogfooding; this session's MCP surface has 86 tools "
        "across 7 packs and none of them creates DOCX, PPTX or PDF. Verified against the "
        "seat tool list and the host config mcp.servers block (node_repl, cua_repl, "
        "web-search, web-reader, zread, zai-vision). The document MCP work was done as "
        "research plus read side dogfooding, and the deliverables were built on the local "
        "fallback path.",
        styles["Normal"],
    ),
    Paragraph("What the ecosystem offers", styles["Heading1"]),
    Paragraph(
        "Office-Word-MCP-Server: FastMCP over python-docx, about 50 tools, deep table "
        "support, convert_to_pdf, but no table of contents or headers and footers tool. "
        "Office-PowerPoint-MCP-Server: python-pptx, 34 tools over 11 modules, no PDF "
        "export. PDF servers (hanweg/mcp-pdf-tools, PDF Toolkit MCP, mcp-pdf): merge, "
        "split, extract and form fill first; creation is secondary.",
        styles["Normal"],
    ),
    Paragraph("Clunky and missing", styles["Heading1"]),
    Paragraph(
        "One tool per operation makes a formatted report cost dozens of round trips. "
        "python-docx cannot compute a TOC; Word populates the field on open. The z.ai "
        "search and read MCP backends rate limited this session with MCP -429 code 1302 on "
        "7 of 9 searches. Missing here: any document creation server in the host config.",
        styles["Normal"],
    ),
    Paragraph("Fallback receipt", styles["Heading1"]),
    Paragraph(
        "mcp-docs-report.docx, mcp-docs-report.pptx and this PDF were built " + DATE + " "
        "in flash50 by _mcpdoc_build.py using python-docx 1.2.0, python-pptx 1.0.2 (temp "
        "target install, shared venv untouched) and the venv's reportlab. All three files "
        "were reopened and verified after write.",
        styles["Normal"],
    ),
]
pdf_path = os.path.join(BANK, "mcp-docs-report.pdf")
SimpleDocTemplate(pdf_path, pagesize=letter).build(story)

# ---------------------------------------------------------------- VERIFY
print("== VERIFY ==")
from docx import Document as D2
d2 = D2(docx_path)
h = [p.text for p in d2.paragraphs if p.style.name.startswith("Heading") or p.style.name == "Title"]
with zipfile.ZipFile(docx_path) as z:
    xml = z.read("word/document.xml").decode("utf-8", "replace")
    parts = z.namelist()
print("DOCX size", os.path.getsize(docx_path), "paragraphs", len(d2.paragraphs),
      "headings+title", len(h), "tables", len(d2.tables),
      "headerText", repr(d2.sections[0].header.paragraphs[0].text))
print("DOCX TOC field present:", "fldSimple" in xml and "TOC" in xml, "| parts:", len(parts),
      "| header part in zip:", any("header" in p for p in parts))

p2 = Presentation(pptx_path)
titles = []
for s in p2.slides:
    t = s.shapes.title.text if s.shapes.title is not None else None
    titles.append(t)
print("PPTX size", os.path.getsize(pptx_path), "slides", len(p2.slides), "titles", titles)

from pypdf import PdfReader
head = open(pdf_path, "rb").read(8)
rd = PdfReader(pdf_path)
print("PDF size", os.path.getsize(pdf_path), "magic", head, "pages", len(rd.pages))
print("PDF page0 first 90 chars:", rd.pages[0].extract_text()[:90].replace("\n", " / "))
