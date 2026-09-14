// harvest_tabs.mjs — THE ONE-BUTTON TAB HARVEST (2026-09-02)
// Launched by the Desktop HARVEST_TABS button. When the Chrome extension is
// paired, this pulls every AI-chat tab's full transcript into watch/harvest/
// dossiers, deduped by content hash, with a receipt row on the Ractor Board.
// Until then it reports readiness and exits — same button, zero re-wiring.
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { pathToFileURL } from "node:url";

const root = process.env.ZCODE_PROJECT_DIR
  || path.join(os.homedir(), "Documents", "projects", "local_sovereign_agent");
const pluginRoot = process.env.ZCODE_PLUGIN_ROOT
  || path.join(os.homedir(), ".zcode", "cli", "plugins", "cache",
               "zcode-plugins-official", "browser-use", "0.4.1");

const { setupBrowserRuntime } = await import(
  pathToFileURL(path.join(pluginRoot, "scripts", "browser-client.mjs")).href
);
await setupBrowserRuntime({ globals: globalThis });

const AI_HOSTS = [
  "chatgpt.com", "chat.openai.com", "grok.com", "x.com", "gemini.google.com",
  "claude.ai", "chat.deepseek.com", "chat.mistral.ai", "poe.com",
  "portal.qwen.ai", "chat.qwen.ai", "kimi.moonshot.cn", "www.perplexity.ai",
  "chat.z.ai", "openrouter.ai", "copilot.microsoft.com"
];

function stamp() {
  return new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
}

async function main() {
  const outDir = path.join(root, "watch", "harvest", stamp());
  let browser;
  try {
    browser = await agent.browsers.get("extension");
  } catch (e) {
    console.log("NOT-READY: the Chrome extension is not paired yet.");
    console.log("Pair it once (ZCode app browser pane -> connect Chrome),");
    console.log("then this button does the whole harvest by itself.");
    process.exit(2);
  }
  fs.mkdirSync(outDir, { recursive: true });
  const tabs = await browser.user.openTabs();
  const targets = tabs.filter(t => t.url && AI_HOSTS.some(h => t.url.includes(h)));
  console.log(`open tabs: ${tabs.length}, AI-chat tabs: ${targets.length}`);
  let harvested = 0;
  for (const info of targets) {
    try {
      const tab = await browser.user.claimTab(info);
      await tab.playwright.waitForLoadState({ state: "domcontentloaded" });
      const snap = await tab.playwright.domSnapshot();
      const title = (info.title || info.url).replace(/[^\w\- ]+/g, "_").slice(0, 60);
      const file = path.join(outDir, title + ".md");
      const body = `# HARVEST: ${info.title}\n\nsource: ${info.url}\nharvested: ${new Date().toISOString()}\n\n---\n\n${snap}\n`;
      fs.writeFileSync(file, body, "utf-8");
      console.log(`harvested: ${info.title}`);
      harvested++;
      tab.close().catch(() => {});
    } catch (e) {
      console.log(`FAILED: ${info.url} -> ${String(e).slice(0, 120)}`);
    }
  }
  // dedupe by content hash
  const seen = new Map();
  for (const f of fs.readdirSync(outDir)) {
    const p = path.join(outDir, f);
    const h = (await import("node:crypto")).createHash("sha256")
      .update(fs.readFileSync(p)).digest("hex").slice(0, 16);
    if (seen.has(h)) { fs.unlinkSync(p); } else { seen.set(h, f); }
  }
  console.log(`DONE: ${harvested} chats harvested -> ${outDir}`);
  console.log("next: the fold (session_dossier) turns them into standing-wave knots.");
}

main().catch(e => { console.error("harvest failed:", String(e).slice(0, 300)); process.exit(1); });
