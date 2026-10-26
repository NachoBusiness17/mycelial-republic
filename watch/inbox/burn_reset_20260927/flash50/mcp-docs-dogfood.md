# mcp-docs: document MCP tool dogfood census and fallback build

Item: mcp-docs, bank flash50. Date 2026-09-28.
Ask: dogfood the document MCP tools; create a DOCX (title page, headers, table of
contents, body paragraphs), a PPTX with 3 slides, and a PDF as real deliverables;
document the tool surface (what works, what is clunky, what is missing).
Banked byte-identical at flash50/mcp-docs.md and flash50/mcp-docs-dogfood.md (the ask
named both paths).

## 1. Headline: the named tool surface does not exist on this seat

The ask's check (create DOCX/PPTX/PDF through document MCP tools) was NOT run, because
this session exposes zero document-creation MCP tools. Verified two independent ways:

1. Seat surface census, counted from this session's own function list: 86 MCP tools in
   7 packs. mapbox core 31, mapbox-devkit 22, mapbox-docs 3, android-emulator 23,
   mimosa security scan 5, image-search 1, web-reader 1. None creates DOCX, PPTX or PDF.
2. Host config receipt `C:/Users/foste/.zcode/cli/config.json` (7,550 bytes, parsed with
   venv python json). The `mcp.servers` block names exactly: node_repl, cua_repl,
   web-search + web-search-sd (https://api.z.ai/api/mcp/web_search_prime/mcp), web-reader
   + web-reader-sd (https://api.z.ai/api/mcp/web_reader/mcp), zread + zread-sd, zai-vision
   + zai-vision-sd (stdio npx @z_ai/mcp-server@latest). Enabled plugins in the same file:
   github, mimosa, video-agent-kit, android-emulator, mcp-server-dev, mcp-tunnels,
   mcp-apps, mapbox, togetherai-skills. No office/document/pdf pack is configured or
   enabled. Repo check: `git ls-files "*.mcp.json" "*mcp_config*" "*.mcp*"` returned
   zero tracked files.

Per the harness instruction ("if you can't access them directly, research the patterns
and document what you find"), the item was executed as: dogfood the document-adjacent
tools that DO exist, research the document MCP server ecosystem from first-hand
fetched READMEs, then produce the three real deliverables through a clearly labeled
LOCAL fallback. The fallback is a substitute and is reported as a substitute.

## 2. What ran in this session (dogfood receipts)

- `mcp__web_reader__webReader` on
  https://github.com/GongRzhe/Office-Word-MCP-Server : SUCCESS, returned the full README
  (title, features, 8 tool groups, complete API reference, troubleshooting) as markdown.
- `mcp__web_reader__webReader` on
  https://github.com/GongRzhe/Office-PowerPoint-MCP-Server : SUCCESS, full README
  (34 tools, 11 modules).
- `mcp__web_reader__webReader` on https://github.com/mcp-dir/pdf-mcp-server : MCP error
  -500 (network error, error id 20260929090219a71c300b1a9f41d5...). That repo's existence
  is UNVERIFIED (the URL was a probe, it did not resolve through the reader).
- `mcp__web_reader__webReader` on https://github.com/hanweg/mcp-pdf-tools : MCP error
  -429 code 1302 (rate limit). NOT fetched; PDF-side claims below rest on search
  results, not first-hand reads.
- Built-in WebSearch tool (backed by the z.ai web_search_prime MCP server): across 3
  queries, the raw feed shows 6 explicit `MCP error -429 code 1302` attempts before
  successes (2 on query 1, 4 on query 2), plus silent empty attempts on query 3. All 3
  queries eventually returned results. Live confirmation of the envelope law: first
  rate-limit contact is a HOLD signal, the limit is rolling throughput.
- `mcp__plugin_mapbox_mapbox-docs__search_mapbox_docs_tool` (query "static map image
  export PDF report", limit 3): SUCCESS, 3 ranked results with URLs and blurbs.
- `mcp__plugin_mapbox_mapbox-docs__get_document_tool` on
  https://docs.mapbox.com/api/maps/static-images.md : SUCCESS, full API page returned
  as markdown. The read-side doc pattern (search then fetch) works end to end from
  this session.

## 3. The document MCP ecosystem, as researched

### Office-Word-MCP-Server (GongRzhe): first-hand README fetched this session

FastMCP server over python-docx, one-line install `uvx --from office-word-mcp-server
word_mcp_server`. About 50 tools in 8 groups:

- document management: create_document, get_document_info, get_document_text,
  get_document_outline, list_available_documents, copy_document, convert_to_pdf
- content: add_heading, add_paragraph, add_table, add_picture, add_page_break
- insert-near-text: insert_header_near_text, insert_line_or_paragraph_near_text,
  insert_numbered_list_near_text, insert_table_near_text
- formatting: format_text, search_and_replace, delete_paragraph, create_custom_style
- tables: about 15 tools (borders, shading, headers, merges, dimensions, alignment)
- comments: 3 extraction tools; plus document protection tools
- create-from-templates, and a custom-style workflow

Verified against the fetched API reference: NO table-of-contents tool, NO header/footer
tool, NO page-number tool. The ask's "title page, headers, table of contents" report is
exactly the shape this flagship server cannot fully express: you would fake a TOC as
plain paragraphs.

The README's own Troubleshooting section (their words, fetched first hand) admits the
sharp edges: missing styles need manual fallback, image paths must be absolute, table
cells index from zero, hex colors must omit the '#', padding units are inconsistent,
auto-fit overrides manual column widths, and cell text formatting must be applied AFTER
content or it is lost. MCP_DEBUG=1 enables logging.

### Office-PowerPoint-MCP-Server (GongRzhe): first-hand README fetched this session

python-pptx exposed as MCP: 34 tools over 11 modules (7 core: presentations, slides,
text formatting, images, tables, charts, shapes; 4 advanced: templates, notes, layout
info, hierarchical info). Covers the ask's "3 slides" case directly (create
presentation, add slide from layout, add text). No PDF export path exists
(python-pptx cannot render; needs LibreOffice headless or PowerPoint COM).

### PDF side: from search results only (reads rate-limited), flagged as such

- hanweg/mcp-pdf-tools: pypdf; merge PDFs and extract pages through MCP
- PDF Toolkit MCP Server (mcpservers.org listing): 16 TypeScript tools including create
  PDF from Markdown, fill forms, split, rotate, watermark, encrypt, QR codes
- mcp-pdf (PyPI): 49 tools: text extraction, form fill and create, merge/split/reorder
- xt765/mcp-document-converter: 5-format document conversion
- smelt (ndcorder): PDF/DOCX/PPTX/XLSX/audio/web to text (read side)

Pattern: the PDF ecosystem is merge/split/extract/form-fill first, CREATE second. The
one create-from-markdown tool found lives in a 16-tool toolkit, not a generation-first
server.

### Read-side giants (from search): Microsoft markitdown-class converters, Box MCP
(regex search inside binary docs). The ecosystem is far stronger at reading documents
than writing them.

## 4. What works

1. Read side of this session's surface, proven live: web-reader returned two full
   READMEs as clean markdown in one call each; mapbox-docs search-then-fetch ran end
   to end. This is the loop the fleet already knows from research-pack.
2. The flagship Office servers are real, not vaporware: high tool counts mapping closely
   onto python-docx/python-pptx, one-line uvx installs, FastMCP base (same stack the
   harness could self-host).
3. Table support in the Word server is unusually deep (about 15 formatting tools).
4. The fallback path itself: python-docx 1.2.0 + python-pptx 1.0.2 as pure wheels
   install cleanly to an isolated target dir with zero venv disturbance, and reportlab
   was already present.

## 5. What is clunky

1. One tool per operation: about 50 narrow Word tools means one formatted report costs
   dozens of agent round trips. A composite build-report tool (accept outline plus
   content, return file) would fit agent use far better; nobody ships one.
2. python-docx (and therefore every MCP server built on it) cannot compute a table of
   contents: a real TOC field only populates when Word itself opens and updates it.
   Same root cause for headers/footers/page numbers gaps. Word is required as the
   layout engine for anything beyond linear content.
3. The servers' own troubleshooting list is a wall of sharp edges (zero-based cells,
   absolute image paths, hash-less hex colors, format-after-content ordering,
   auto-fit overriding widths): the tool surface leaks python-docx internals instead of
   wrapping them.
4. Error surfacing: web-reader returns raw structured MCP errors (-500 with a bare
   network error id; -429 code 1302) with no retry/backoff semantics visible to the
   agent; the z.ai search backend rate limited 6 explicit attempts across this
   session's 3 queries (receipts in section 2).
5. Install friction is low but real: uvx/npx runtimes required; nothing here ships as
   a pip-installable plugin pack for this host.

## 6. What is missing

1. On this host: any document-creation pack at all (the actual blocker for this ask).
2. In the Word server: TOC, headers/footers, page numbers, tracked-changes authoring,
   PDF import (only convert_to_pdf out).
3. In the PPTX server: any export beyond PPTX (no PDF, no images).
4. Across PDF servers: generation-first tooling; create-from-markdown is a side dish in
   a form-filling toolkit.
5. Everywhere: one server spanning DOCX + PPTX + PDF with a single composite
   "build-report" verb. The ask's three deliverables are one intent, but the ecosystem
   would make an agent walk three servers and dozens of verbs to express it.

## 7. Fallback build receipt (the real deliverables)

Deliverables, built 2026-09-28 into flash50 by `_mcpdoc_build.py` (banked alongside):

- `mcp-docs-report.docx` (40,504 bytes): Title-style title page, live page header
  ("MCP Document Tools Dogfood Report | flash50 | 2026-09-28"), real Word TOC field
  (w:fldSimple, instr `TOC \o "1-3" \h \z \u`, verified present in word/document.xml)
  PLUS a manual static TOC so content shows without a field update, 8 Heading-1
  sections with body paragraphs, and a 3-column x 8-row Table Grid tool census.
- `mcp-docs-report.pptx` (30,382 bytes): exactly 3 slides (title slide; findings
  bullets; verdict bullets), python-pptx default template.
- `mcp-docs-report.pdf` (2,899 bytes): reportlab platypus, 1 page, 4 headed sections.

Libraries: python_docx-1.2.0 and python_pptx-1.0.2 wheels downloaded with
`pip download --dest %TEMP%\mcpdoc_wheels` then installed with
`pip install --target %TEMP%\mcpdoc_libs` (shared .venv untouched; reportlab and pypdf
were already in the venv, verified by import before use).

Verification output from the build script run (verbatim, this session):

```
== VERIFY ==
DOCX size 40504 paragraphs 33 headings+title 9 tables 1 headerText 'MCP Document Tools Dogfood Report | flash50 | 2026-09-28'
DOCX TOC field present: True | parts: 18 | header part in zip: True
PPTX size 30382 slides 3 titles ['MCP Document Tools: Dogfood Report', 'The reachable surface has no document tools', 'Ecosystem findings and the fallback verdict']
PDF size 2899 magic b'%PDF-1.4' pages 1
PDF page0 first 90 chars: MCP Document Tools: Dogfood Report / Item mcp-docs | flash50 | 2026-09-28 | fallback build v
```

This is a substitute for the ask's named check, reported as such: the DOCX/PPTX/PDF
were produced by local libraries, not by MCP tool calls, because no document MCP tool
is reachable from this seat.

## 8. Verdict and cheapest fix

The document-MCP pattern is sound where it exists: FastMCP over python-docx /
python-pptx / pypdf is thin glue over mature libraries, and this session proved the
read-side MCP document loop live. The gap is host-side, not ecosystem-side. Cheapest
fix for the fleet: enable one local FastMCP document pack (stdio server in
config.json mcp.servers) that wraps exactly the fallback code banked here, and expose
ONE composite build-report tool per format (outline plus content in, file path out)
instead of 50 one-verb tools. The three files in flash50 are the proof artifacts and
the seed of that server.

## Sources

- First-hand fetches this session (web-reader MCP): github.com/GongRzhe/Office-Word-MCP-Server,
  github.com/GongRzhe/Office-PowerPoint-MCP-Server
- Search results (z.ai web_search_prime MCP, rate-limited): [hanweg/mcp-pdf-tools](https://github.com/hanweg/mcp-pdf-tools),
  [mcpservers.org](https://mcpservers.org), [PyPI](https://pypi.org), mcpmarket.com,
  xt765/mcp-document-converter, github.com/ndcorder/smelt, [pulsemcp.com](https://www.pulsemcp.com)
- First-hand fetch this session (mapbox-docs MCP): docs.mapbox.com/api/maps/static-images.md
- Host config: C:/Users/foste/.zcode/cli/config.json (read this session)
