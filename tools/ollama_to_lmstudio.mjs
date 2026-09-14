#!/usr/bin/env node
/**
 * Ollama -> Bionic/LM Studio bridge.
 *
 * Ollama stores GGUF payloads as content-addressed files without a .gguf
 * suffix. LM Studio/Bionic indexes named GGUF files under its own models
 * root. This tool preserves Ollama, imports through the native `lms import`
 * command, and writes the shared registry consumed by Mag.
 *
 * Usage:
 *   node tools/ollama_to_lmstudio.mjs --inventory
 *   node tools/ollama_to_lmstudio.mjs --all
 *   node tools/ollama_to_lmstudio.mjs --all --include-embeddings
 */
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";

const home = process.env.USERPROFILE || os.homedir();
const ollamaRoot = process.env.OLLAMA_MODELS_DIR || path.join(home, ".ollama", "models");
const lmRoot = process.env.LMSTUDIO_MODELS_DIR || path.join(home, ".lmstudio", "models");
const lms = process.env.LMS_CLI || path.join(home, ".lmstudio", "bin", "lms.exe");
const repoRoot = process.env.MAG_ROOT || process.cwd();
const registryPath = process.env.MODEL_REGISTRY || path.join(repoRoot, "watch", "MODEL_REGISTRY.json");
const manifestRoot = path.join(ollamaRoot, "manifests", "registry.ollama.ai", "library");
const blobRoot = path.join(ollamaRoot, "blobs");
const inboxRoot = path.join(lmRoot, "bridge-inbox");

const explicitRepos = new Map([
  ["deepseek-r1", ["deepseek-ai", "DeepSeek-R1-Distill-Qwen-1.5B"]],
  ["gemma", ["google", "Gemma-2B"]],
  ["gemma4", ["google", "Gemma-4-12B"]],
  ["qwen2.5", ["Qwen", "Qwen2.5-3B-Instruct"]],
  ["qwen2.5-coder", ["Qwen", "Qwen2.5-Coder-7B-Instruct"]],
  ["qwen2.5vl", ["Qwen", "Qwen2.5-VL-3B-Instruct"]],
  ["qwen-desk", ["Qwen", "Qwen2.5-3B-Instruct"]],
  ["nomic-embed-text", ["nomic-ai", "nomic-embed-text-v1.5-GGUF"]],
]);

function args() {
  const a = new Set(process.argv.slice(2));
  const requested = process.argv.slice(2).find(x => !x.startsWith("-"));
  return { all: a.has("--all"), inventory: a.has("--inventory"), embeddings: a.has("--include-embeddings"), requested };
}

function safeName(s) {
  return s.replace(/[^A-Za-z0-9._-]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "");
}

function modelTag(relative) {
  const p = relative.split(path.sep).join("/");
  const bits = p.split("/");
  const leaf = bits.pop();
  const parent = bits.pop() || "unknown";
  return `${parent}:${leaf}`;
}

function baseName(tag) {
  return tag.split(":", 1)[0];
}

function repoFor(tag) {
  if (tag === "qwen2.5:32b") return ["Qwen", "Qwen2.5-32B-Instruct"];
  if (tag.startsWith("gemma4:")) return ["google", "Gemma-4-12B"];
  const base = baseName(tag);
  if (explicitRepos.has(base)) return explicitRepos.get(base);
  const repo = safeName(tag.replace(":", "-"));
  return ["ollama", repo];
}

function isAlias(tag) {
  const base = baseName(tag).toLowerCase();
  return base.endsWith("-desk") || base.endsWith("-hermes") || base === "qwen-desk";
}

function prefer(a, b) {
  if (!a) return b;
  if (!b) return a;
  if (isAlias(a) && !isAlias(b)) return b;
  if (isAlias(b) && !isAlias(a)) return a;
  return a.localeCompare(b) <= 0 ? a : b;
}

function isGguf(file) {
  if (!fs.existsSync(file)) return false;
  const fd = fs.openSync(file, "r");
  const head = Buffer.alloc(4);
  try { fs.readSync(fd, head, 0, 4, 0); return head.toString("ascii") === "GGUF"; }
  finally { fs.closeSync(fd); }
}

function readManifests() {
  if (!fs.existsSync(manifestRoot)) throw new Error(`Ollama manifest root missing: ${manifestRoot}`);
  const rows = [];
  const walk = dir => {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, ent.name);
      if (ent.isDirectory()) walk(full);
      else {
        try {
          const doc = JSON.parse(fs.readFileSync(full, "utf8"));
          const layer = (doc.layers || []).find(x => String(x.mediaType || "").includes("model"));
          if (!layer || !String(layer.digest || "").startsWith("sha256:")) continue;
          const digest = layer.digest.slice("sha256:".length);
          const blob = path.join(blobRoot, `sha256-${digest}`);
          rows.push({
            tag: modelTag(path.relative(manifestRoot, full)),
            manifest: full,
            digest,
            source: blob,
            source_size_bytes: Number(layer.size || 0),
            source_exists: fs.existsSync(blob),
            source_is_gguf: isGguf(blob),
          });
        } catch { /* ignore non-manifest files */ }
      }
    }
  };
  walk(manifestRoot);
  return rows;
}

function uniqueModels(rows) {
  const grouped = new Map();
  for (const row of rows) {
    const prior = grouped.get(row.digest);
    if (!prior) grouped.set(row.digest, { ...row, aliases: [row.tag] });
    else {
      prior.tag = prefer(prior.tag, row.tag);
      prior.aliases.push(row.tag);
    }
  }
  return [...grouped.values()].sort((a, b) => a.tag.localeCompare(b.tag));
}

function ggufTarget(owner, repo) {
  return path.join(lmRoot, owner, repo, `${repo}.gguf`);
}

function findExistingBySize(bytes) {
  if (!fs.existsSync(lmRoot)) return null;
  let found = null;
  const walk = dir => {
    if (found) return;
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, ent.name);
      if (ent.isDirectory()) walk(full);
      else if (ent.name.toLowerCase().endsWith(".gguf") && fs.statSync(full).size === bytes) { found = full; return; }
    }
  };
  walk(lmRoot);
  return found;
}

function resolvedTarget(model) {
  const [owner, repo] = repoFor(model.tag);
  const canonical = ggufTarget(owner, repo);
  if (fs.existsSync(canonical) && fs.statSync(canonical).size === model.source_size_bytes) return { owner, repo, target: canonical, imported: true };
  const existing = findExistingBySize(model.source_size_bytes);
  if (existing) return { owner, repo, target: existing, imported: true, discovered: true };
  return { owner, repo, target: canonical, imported: false };
}

function apiVisible() {
  try {
    const probe = spawnSync(process.env.CURL || "curl.exe", ["-sf", "http://127.0.0.1:1234/v1/models"], { encoding: "utf8", timeout: 5000 });
    if (probe.status !== 0) return [];
    return (JSON.parse(probe.stdout).data || []).map(x => String(x.id));
  } catch { return []; }
}

function loadedModels() {
  try {
    const probe = spawnSync(lms, ["ps"], { encoding: "utf8", timeout: 10000 });
    if (probe.status !== 0) return [];
    return probe.stdout.split(/\r?\n/).slice(2).map(line => line.trim().split(/\s+/)[0]).filter(x => x && x !== "IDENTIFIER");
  } catch { return []; }
}

function entry(model, visible, loaded) {
  const resolved = resolvedTarget(model);
  const { owner, repo, target, imported } = resolved;
  const targetStat = fs.existsSync(target) ? fs.statSync(target) : null;
  const id = safeName(path.basename(target, ".gguf")).toLowerCase();
  return {
    id,
    tag: model.tag,
    aliases: model.aliases,
    roles: baseName(model.tag).includes("coder") ? ["worker", "coder"] : ["worker", "research"],
    source: { manifest: model.manifest, blob: model.source, sha256: model.digest, bytes: model.source_size_bytes },
    bionic: { repository: `${owner}/${repo}`, path: target, imported, bytes_match: imported, discovered_existing_path: Boolean(resolved.discovered), api_visible: visible.includes(id), loaded: loaded.includes(id) },
    runtime: "bionic-lmstudio",
    status: imported ? (loaded.includes(id) ? "loaded" : visible.includes(id) ? "present-jit" : "present") : (model.source_exists ? "source-only" : "missing-source"),
    bionic_runnable: loaded.includes(id) ? "verified-chat" : imported ? "unverified" : "not-imported",
  };
}

function writeRegistry(rows, visible, loaded) {
  fs.mkdirSync(path.dirname(registryPath), { recursive: true });
  const doc = {
    schema: "model_registry.v1",
    generated_at: new Date().toISOString(),
    law: "Clients do not own weights; registry records source, runtime, path, and evidence.",
    source_store: ollamaRoot,
    bionic_models_root: lmRoot,
    bionic_api: "http://127.0.0.1:1234/v1",
    api_visible_ids: visible,
    loaded_ids: loaded,
    models: rows.map(x => entry(x, visible, loaded)),
  };
  fs.writeFileSync(registryPath, JSON.stringify(doc, null, 2) + "\n", "utf8");
  return doc;
}

function importModel(model) {
  const resolved = resolvedTarget(model);
  const { owner, repo, target } = resolved;
  if (resolved.imported) return { action: "already-present", target };
  if (!model.source_exists || !model.source_is_gguf) return { action: "blocked", reason: "source missing or not GGUF", target };
  fs.mkdirSync(inboxRoot, { recursive: true });
  const staged = path.join(inboxRoot, `${repo}.gguf`);
  fs.copyFileSync(model.source, staged);
  const run = spawnSync(lms, ["import", "-y", "--copy", "--user-repo", `${owner}/${repo}`, staged], { encoding: "utf8", timeout: 900000 });
  try { fs.unlinkSync(staged); } catch { /* preserve evidence if cleanup is denied */ }
  if (run.status !== 0) return { action: "failed", reason: (run.stderr || run.stdout || `exit ${run.status}`).trim().slice(-500), target };
  return { action: "imported", target, output: (run.stdout || "").trim().slice(-300) };
}

const opt = args();
const allRows = uniqueModels(readManifests());
const chosen = opt.requested && !opt.all
  ? allRows.filter(x => x.tag === opt.requested || baseName(x.tag) === opt.requested)
  : allRows;
if (opt.requested && !chosen.length) throw new Error(`No Ollama manifest matched: ${opt.requested}`);
const eligible = chosen.filter(x => opt.embeddings || !x.tag.toLowerCase().includes("embed"));

if (opt.inventory) {
  const doc = writeRegistry(eligible, apiVisible(), loadedModels());
  console.log(JSON.stringify({ registry: registryPath, models: doc.models.length, imported: doc.models.filter(x => x.bionic.imported).length }, null, 2));
  process.exit(0);
}

if (!opt.all && !opt.requested) {
  console.error("Use --inventory, --all, or provide an Ollama tag.");
  process.exit(2);
}

for (const model of eligible) {
  const result = importModel(model);
  console.log(`${result.action.padEnd(15)} ${model.tag.padEnd(28)} ${result.target}`);
}
const doc = writeRegistry(eligible, apiVisible(), loadedModels());
console.log(`REGISTRY ${registryPath}`);
console.log(`MODELS ${doc.models.length} IMPORTED ${doc.models.filter(x => x.bionic.imported).length} LOADED ${doc.models.filter(x => x.bionic.loaded).length}`);
