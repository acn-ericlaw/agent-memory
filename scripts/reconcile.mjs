#!/usr/bin/env node
// reconcile — converge a target repo to the agent-memory target state (MANIFEST.md).
//
// Tool-operator-side (runs from this checkout; never installed into targets). Node
// stdlib only. Byte-parity twin of scripts/reconcile.py — keep outputs identical.
//
// Usage:
//   node scripts/reconcile.mjs --target <path> [--apply] [--pre-apply-complete]
//       [--forge github|gitlab|azdo|unknown]
//   node scripts/reconcile.mjs --check-manifest
//
// Exit codes: 0 converged / applied / manifest OK; 3 pending actions (dry-run); 1 error.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const EXCLUDED_DIRS = new Set(["__pycache__", ".DS_Store"]);
const EXCLUDED_FILE_RE = /(\.py[co]|\.DS_Store)$/;
export const POLICIES = new Set(["verbatim", "verbatim-dir", "seed-copy", "sentinel-merge", "seed-generate", "stamp"]);
export const FORGES = new Set(["all", "github", "gitlab", "azdo"]);

class Die extends Error {}

function die(msg) {
  throw new Die(msg);
}

const readText = (p) => fs.readFileSync(p, "utf-8");
const readBytes = (p) => fs.readFileSync(p);

// os.path.realpath semantics for possibly-nonexistent paths: resolve symlinks along
// the longest existing ancestor, then re-append the remainder. path.resolve alone is
// lexical — a symlinked component inside the target could smuggle a write outside it.
function realpathNonStrict(p) {
  let base = p;
  const rest = [];
  while (!fs.existsSync(base)) {
    const parent = path.dirname(base);
    if (parent === base) break;
    rest.unshift(path.basename(base));
    base = parent;
  }
  const real = fs.existsSync(base) ? fs.realpathSync(base) : base;
  return rest.length ? path.join(real, ...rest) : real;
}

export function parseSemver(s) {
  let m = /^(\d+)\.(\d+)\.(\d+)$/.exec(s);
  if (m) return [Number(m[1]), Number(m[2]), Number(m[3])];
  m = /^(\d+)\.x$/.exec(s);
  if (m) return [Number(m[1]), 0, 0];
  return null;
}

function semverLt(a, b) {
  for (let i = 0; i < 3; i++) {
    if (a[i] !== b[i]) return a[i] < b[i];
  }
  return false;
}

export function parseManifest(toolRoot) {
  const p = path.join(toolRoot, "MANIFEST.md");
  if (!fs.existsSync(p)) die("MANIFEST.md not found in the tool checkout: " + p);
  const sections = {};
  let current = null;
  for (const line of readText(p).split("\n")) {
    const m = /^## (.+?)\s*$/.exec(line);
    if (m) {
      current = m[1];
      sections[current] = [];
    } else if (current !== null) {
      sections[current].push(line);
    }
  }
  const tableRows = (section) => {
    const rows = [];
    for (const line of sections[section] || []) {
      if (!line.startsWith("|")) continue;
      const cells = line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
      if (!cells.length || cells[0].startsWith("---") || /^[-\s]*$/.test(cells[0])) continue;
      rows.push(cells);
    }
    return rows;
  };

  const rows = [];
  for (const cells of tableRows("Install manifest")) {
    if (cells[0] === "Target") continue;
    if (cells.length !== 5) die("malformed install-manifest row: " + cells.join(" | "));
    const [target, source, policy, forge, attrs] = cells;
    if (!POLICIES.has(policy)) die("unknown policy '" + policy + "' for " + target);
    if (!FORGES.has(forge)) die("unknown forge '" + forge + "' for " + target);
    rows.push({ target, source, policy, forge, attrs });
  }

  const semantic = [];
  for (const cells of tableRows("Semantic steps")) {
    if (cells[0] === "Below") continue;
    if (cells.length !== 3) die("malformed semantic-step row: " + cells.join(" | "));
    const [below, rung, step] = cells;
    if (parseSemver(below) === null) die("bad version in semantic step: " + below);
    semantic.push({ below, rung, step });
  }

  const toolOnly = (sections["Tool-only (never installed)"] || []).join("\n");
  if (!rows.length) die("MANIFEST.md has no install-manifest rows");
  return { rows, semantic, toolOnly };
}

export function detectInstalled(target) {
  const vpath = path.join(target, ".agent", "version.md");
  if (fs.existsSync(vpath)) {
    const text = readText(vpath);
    // a stamp must be a full semver; the "N.x" form is internal to the no-stamp
    // 2.x baseline and is malformed when written into a target's version.md
    const m = /\*\*version:\*\*\s*(\S+)/.exec(text) || /^version:\s*(\S+)/m.exec(text);
    if (!m || !/^\d+\.\d+\.\d+$/.test(m[1])) {
      die("unreadable .agent/version.md in the target — repair it first " +
        "(memory-lint check_version_manifest); found no valid version value");
    }
    return m[1];
  }
  if (fs.existsSync(path.join(target, "memory", "instructions.md"))) return "2.x";
  return null;
}

export function gitConfigGet(target, section, key) {
  const cfg = path.join(target, ".git", "config");
  if (!fs.existsSync(cfg) || !fs.statSync(cfg).isFile()) return null;
  let current = null;
  const keyRe = new RegExp("^\\s*" + key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\s*=\\s*(.+?)\\s*$", "i");
  for (const line of readText(cfg).split("\n")) {
    const m = /^\s*\[(.+?)\]\s*$/.exec(line);
    if (m) {
      current = m[1].trim().toLowerCase();
      continue;
    }
    if (current === section.toLowerCase()) {
      const k = keyRe.exec(line);
      if (k) return k[1];
    }
  }
  return null;
}

export function detectForge(target) {
  const url = gitConfigGet(target, 'remote "origin"', "url");
  if (url === null) return "unknown";
  const u = url.toLowerCase();
  if (u.includes("github.com")) return "github";
  if (u.includes("gitlab")) return "gitlab";
  if (u.includes("dev.azure.com") || u.includes("visualstudio.com")) return "azdo";
  return "unknown";
}

export function rowApplies(rowForge, forge) {
  if (rowForge === "all" || rowForge === forge) return true;
  return forge === "unknown" && (rowForge === "github" || rowForge === "gitlab");
}

export function safeTargetPath(targetRoot, rel) {
  rel = rel.replace(/\/+$/, "");
  const root = fs.realpathSync(targetRoot);
  const p = realpathNonStrict(path.resolve(root, rel));
  if (p !== root && !p.startsWith(root + path.sep)) die("manifest path escapes the target: " + rel);
  return p;
}

function isExecutable(p) {
  return fs.existsSync(p) && fs.statSync(p).isFile() && (fs.statSync(p).mode & 0o111) !== 0;
}

export function walkFiles(root) {
  const out = [];
  const recurse = (dir) => {
    const entries = fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
    for (const e of entries) {
      if (e.isDirectory()) {
        if (!EXCLUDED_DIRS.has(e.name)) recurse(path.join(dir, e.name));
      } else if (!EXCLUDED_FILE_RE.test(e.name)) {
        out.push(path.relative(root, path.join(dir, e.name)));
      }
    }
  };
  recurse(root);
  return out.sort();
}

function copyWithMode(src, dst) {
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.copyFileSync(src, dst);
  fs.chmodSync(dst, fs.statSync(src).mode & 0o777);
}

function entryLines(templateText) {
  return templateText.split("\n").filter((l) => l.trim() && !l.trim().startsWith("#"));
}

function commentHead(templateText) {
  const head = [];
  for (const l of templateText.split("\n")) {
    if (l.trim().startsWith("#")) head.push(l);
    else break;
  }
  return head;
}

function planSentinel(row, tgtPath, srcPath) {
  const template = readText(srcPath);
  if (!fs.existsSync(tgtPath)) return ["copy", []];
  const raw = readBytes(tgtPath);
  const text = raw.toString("utf-8");
  if (!Buffer.from(text, "utf-8").equals(raw)) {
    die("target " + row.target + " is not valid UTF-8 — merge the managed block by hand");
  }
  const lines = text.split("\n");
  const existing = new Set(lines.map((l) => l.trim()));
  const existingNorm = new Set(lines.map((l) => l.trim().split(/\s+/).join(" ")));
  const missing = entryLines(template).filter(
    (e) => !existing.has(e.trim()) && !existingNorm.has(e.trim().split(/\s+/).join(" "))
  );
  return missing.length ? ["merge", missing] : ["ok", []];
}

function applySentinel(tgtPath, srcPath, missing) {
  const template = readText(srcPath);
  if (!fs.existsSync(tgtPath)) {
    copyWithMode(srcPath, tgtPath);
    return;
  }
  const lines = readText(tgtPath).split("\n");
  if (lines.length && lines[lines.length - 1] === "") lines.pop();
  const sentinel = template.split("\n")[0].trim();
  const idx = lines.findIndex((l) => l.trim() === sentinel);
  if (idx === -1) {
    lines.push("");
    lines.push(...commentHead(template));
    lines.push(...missing);
  } else {
    let insertAt = idx + 1;
    while (insertAt < lines.length && lines[insertAt].trim().startsWith("#")) insertAt += 1;
    lines.splice(insertAt, 0, ...missing);
  }
  fs.writeFileSync(tgtPath, lines.join("\n") + "\n");
}

export function buildPlan(toolRoot, target, manifest, forge, installed, currentVersion) {
  const mechanical = [], agent = [], notes = [];
  const fresh = installed === null;
  for (const row of manifest.rows) {
    if (!rowApplies(row.forge, forge)) continue;
    const src = path.join(toolRoot, row.source);
    const tgt = safeTargetPath(target, row.target);
    const policy = row.policy;

    // a target path of the wrong kind would corrupt on copy (a dir named like a
    // file makes the copy write INTO it) — refuse with a sane error instead
    if (row.target.endsWith("/") || policy === "verbatim-dir") {
      if (fs.existsSync(tgt) && fs.statSync(tgt).isFile()) {
        die("target path is a file, expected a directory: " + row.target);
      }
    } else if (fs.existsSync(tgt) && fs.statSync(tgt).isDirectory()) {
      die("target path is a directory, expected a file: " + row.target);
    }

    if (policy === "verbatim") {
      if (!fs.existsSync(src)) die("manifest source missing in the tool checkout: " + row.source);
      if (!fs.existsSync(tgt)) {
        mechanical.push(["copy", row, [], "missing"]);
      } else if (!readBytes(src).equals(readBytes(tgt))) {
        mechanical.push(["recopy", row, [], "drifted from the tool copy"]);
      } else if (row.attrs.includes("exec") && !isExecutable(tgt)) {
        mechanical.push(["chmod", row, [], "content ok, not executable"]);
      } else {
        notes.push(["ok", row.target, ""]);
      }
    } else if (policy === "verbatim-dir") {
      if (!fs.existsSync(src) || !fs.statSync(src).isDirectory()) {
        die("manifest source dir missing in the tool checkout: " + row.source);
      }
      const srcFiles = walkFiles(src);
      const pending = [];
      for (const rel of srcFiles) {
        const sf = path.join(src, rel), tf = path.join(tgt, rel);
        if (!fs.existsSync(tf) || !readBytes(sf).equals(readBytes(tf))) pending.push(rel);
      }
      if (fs.existsSync(tgt) && fs.statSync(tgt).isDirectory()) {
        const srcSet = new Set(srcFiles);
        for (const rel of walkFiles(tgt)) {
          if (!srcSet.has(rel)) notes.push(["extra", row.target + rel, "not in the tool copy — left alone"]);
        }
      }
      if (!pending.length) {
        notes.push(["ok", row.target, String(srcFiles.length) + " file(s)"]);
      } else if (pending.length === srcFiles.length && !fs.existsSync(tgt)) {
        mechanical.push(["copy", row, pending, "missing — " + String(srcFiles.length) + " file(s)"]);
      } else {
        mechanical.push(["recopy", row, pending,
          String(pending.length) + " of " + String(srcFiles.length) + " file(s) stale"]);
      }
    } else if (policy === "seed-copy") {
      if (!fs.existsSync(src)) die("manifest source missing in the tool checkout: " + row.source);
      if (!fs.existsSync(tgt)) {
        mechanical.push(["copy", row, [], "missing"]);
      } else if (!readBytes(src).equals(readBytes(tgt))) {
        notes.push(["keep", row.target, "present, differs — seed-copy never overwrites"]);
        if (row.attrs.includes("wire") && !readText(tgt).includes(".gitlab/agent-memory-ci.yml")) {
          agent.push(["wire", row.target,
            "pre-existing root CI without the include — wire it per ENABLE.md Step 6 " +
            "(add-only include + stage check; never touch workflow:rules)"]);
        }
      } else {
        notes.push(["ok", row.target, ""]);
      }
    } else if (policy === "sentinel-merge") {
      const [state, missing] = planSentinel(row, tgt, src);
      if (state === "copy") {
        mechanical.push(["copy", row, [], "missing"]);
      } else if (state === "merge") {
        mechanical.push(["merge", row, missing, String(missing.length) + " entries missing"]);
        if (row.attrs.includes("renorm")) {
          agent.push(["renorm", "git add --renormalize .",
            "after the .gitattributes merge; on a CRLF repo check the staged " +
            "diff stays within agent-memory files"]);
        }
      } else {
        notes.push(["ok", row.target, ""]);
      }
    } else if (policy === "seed-generate") {
      let present;
      if (row.target.endsWith("/")) {
        const entries = fs.existsSync(tgt) && fs.statSync(tgt).isDirectory()
          ? fs.readdirSync(tgt).filter((e) => !EXCLUDED_DIRS.has(e) && !EXCLUDED_FILE_RE.test(e))
          : [];
        present = entries.length > 0;
      } else {
        present = fs.existsSync(tgt) && fs.statSync(tgt).isFile();
      }
      if (present) {
        notes.push(["ok", row.target, "present — never touched"]);
      } else {
        agent.push(["generate", row.target, row.attrs.replace("step:", "ENABLE.md Step ")]);
      }
    } else if (policy === "stamp") {
      if (installed === currentVersion) {
        notes.push(["ok", row.target, "v" + currentVersion]);
      } else {
        const srcNote = fresh ? "(fresh)" : installed;
        agent.push(["stamp", row.target,
          srcNote + " -> " + currentVersion + " — the agent's closing step, after the semantic steps"]);
      }
    }
  }

  const hooks = gitConfigGet(target, "core", "hookspath");
  const gitpath = path.join(target, ".git");
  if (fs.existsSync(gitpath) && fs.statSync(gitpath).isFile()) {
    agent.push(["activate", "verify hooks + forge by hand",
      "target .git is a worktree/submodule pointer file — confirm " +
      "core.hooksPath (.githooks) and the forge in the main repository"]);
  } else if (!fs.existsSync(gitpath) || !fs.statSync(gitpath).isDirectory()) {
    agent.push(["activate", "git config core.hooksPath .githooks",
      "target has no .git directory — init git first, then activate"]);
  } else if (hooks !== null && hooks.replace(/\/+$/, "") === ".githooks") {
    // activated
  } else if (hooks === null) {
    agent.push(["activate", "git config core.hooksPath .githooks", "currently unset"]);
  } else {
    agent.push(["activate", "git config core.hooksPath .githooks",
      "currently: " + hooks + " — a different hooks path is configured; " +
      "arbitrate before switching (chain it or keep theirs)"]);
  }

  notes.push(["run", "sync skill adapters",
    "bash agent-skills/sync-adapters/scripts/sync-adapters.sh — idempotent, " +
    "gitignored-only; run after any enable or upgrade"]);
  if (forge === "unknown") {
    notes.push(["forge", "hosting forge undetermined",
      "GitHub + GitLab sets installed (additive-safe); Azure DevOps needs " +
      "positive detection — pass --forge to override"]);
  }
  if (forge === "azdo") {
    notes.push(["forge", "Azure DevOps CI floor",
      "inert until the one-time az pipelines create binding — report the command, " +
      "run only at the user's direction, after push (ENABLE.md Step 6)"]);
  }

  const semantic = [];
  if (!fresh) {
    const iv = parseSemver(installed);
    for (const s of manifest.semantic) {
      if (semverLt(iv, parseSemver(s.below))) semantic.push(s);
    }
  }
  return [mechanical, agent, semantic, notes];
}

const PRE_APPLY_TARGETS = new Map([
  ["4.36.0", new Set([
    ".githooks/pre-commit",
    ".githooks/post-commit",
    ".githooks/pre-commit.d/50-agent-memory-secret-guard",
    ".githooks/post-commit.d/50-agent-memory-ritual-capture",
  ])],
  ["4.37.0", new Set(["memory/PROTOCOL.md", "AGENTS.md"])],
]);

export function preApplyState(installed, semantic, mechanical, notes) {
  const steps = semantic.filter((s) => s.step.startsWith("PRE-APPLY:"));
  const pendingByTarget = new Map(mechanical.map((item) => [item[1].target, item[0]]));
  const hard = new Set();
  const confirmation = new Set();
  const protocolCustom = notes.some((note) =>
    note[0] === "keep" && note[1] === "memory/PROTOCOL.md");

  const agentsAction = pendingByTarget.get("AGENTS.md");
  if (agentsAction === "recopy") {
    hard.add("AGENTS.md");
  } else if (agentsAction === "copy" && protocolCustom) {
    hard.add("AGENTS.md");
    hard.add("memory/PROTOCOL.md");
  }

  for (const target of PRE_APPLY_TARGETS.get("4.36.0")) {
    if (pendingByTarget.get(target) === "recopy") confirmation.add(target);
  }

  for (const step of steps) {
    const targets = PRE_APPLY_TARGETS.get(step.below);
    if (!targets) {
      hard.add("<unknown PRE-APPLY boundary for " + step.below + ">");
      continue;
    }
    for (const target of targets) {
      if (step.below === "4.36.0") {
        // Hook drift is confirmable after inspection/extraction: the explicit
        // handshake authorizes the dispatcher re-copy. The protocol boundary
        // below must instead converge before any mechanical apply.
        continue;
      } else if (pendingByTarget.has(target)) {
        hard.add(target);
      }
    }
  }

  if (installed === null && protocolCustom) confirmation.add("memory/PROTOCOL.md");
  return [steps, hard, confirmation];
}

function printReport(mechanical, agent, semantic, notes) {
  const line = (verb, p, detail) => {
    let out = "  " + verb.padEnd(9) + p;
    if (detail) out += "  (" + detail + ")";
    console.log(out);
  };
  console.log("");
  console.log("[mechanical]");
  if (mechanical.length) for (const [verb, row, , detail] of mechanical) line(verb, row.target, detail);
  else console.log("  (nothing to do)");
  console.log("");
  console.log("[agent work]");
  if (agent.length) for (const [verb, p, detail] of agent) line(verb, p, detail);
  else console.log("  (nothing to do)");
  console.log("");
  console.log("[semantic steps]");
  if (semantic.length) {
    for (const s of semantic) {
      line("< " + s.below, "rung " + s.rung, "");
      console.log("           " + s.step);
    }
  } else {
    console.log("  (none apply)");
  }
  console.log("");
  console.log("[notes]");
  for (const [verb, p, detail] of notes) line(verb, p, detail);
  console.log("");
}

export function applyMechanical(toolRoot, target, mechanical) {
  let applied = 0;
  for (const [verb, row, files] of mechanical) {
    const src = path.join(toolRoot, row.source);
    const tgt = safeTargetPath(target, row.target);
    if (row.policy === "verbatim-dir") {
      for (const rel of files) {
        copyWithMode(path.join(src, rel), path.join(tgt, rel));
        applied += 1;
      }
    } else if (row.policy === "sentinel-merge") {
      applySentinel(tgt, src, files);
      applied += 1;
    } else if (verb === "chmod") {
      fs.chmodSync(tgt, 0o755);
      applied += 1;
    } else {
      copyWithMode(src, tgt);
      if (row.attrs.includes("exec")) fs.chmodSync(tgt, 0o755);
      applied += 1;
    }
  }
  return applied;
}

function checkManifest(toolRoot, manifest) {
  const problems = [];
  const coveredFiles = new Set();
  const coveredDirs = [];
  for (const row of manifest.rows) {
    const src = path.join(toolRoot, row.source);
    if (row.policy === "verbatim-dir") {
      if (!fs.existsSync(src) || !fs.statSync(src).isDirectory()) problems.push("source dir missing: " + row.source);
      else coveredDirs.push(row.source.replace(/\/+$/, ""));
    } else if (!fs.existsSync(src) || !fs.statSync(src).isFile()) {
      problems.push("source missing: " + row.source);
    } else {
      coveredFiles.add(path.normalize(row.source));
    }
  }
  const covered = (rel) => {
    const n = path.normalize(rel);
    if (coveredFiles.has(n)) return true;
    return coveredDirs.some((d) => n === d || n.startsWith(d + path.sep));
  };
  for (const root of ["templates", ".githooks"]) {
    for (const rel of walkFiles(path.join(toolRoot, root))) {
      const full = path.join(root, rel);
      if (!covered(full)) problems.push("uncovered file (no manifest row): " + full);
    }
  }
  const skillsRoot = path.join(toolRoot, "agent-skills");
  for (const name of fs.readdirSync(skillsRoot).sort()) {
    const d = path.join(skillsRoot, name);
    if (!fs.statSync(d).isDirectory()) continue;
    const rel = "agent-skills/" + name + "/";
    if (!coveredDirs.includes(rel.replace(/\/+$/, "")) && !manifest.toolOnly.includes(rel)) {
      problems.push("skill dir neither installed nor listed tool-only: " + rel);
    }
  }
  const current = readText(path.join(toolRoot, "VERSION")).trim();
  for (const s of manifest.semantic) {
    if (semverLt(parseSemver(current), parseSemver(s.below))) {
      problems.push("semantic step gated above the current version: " + s.below);
    }
  }
  if (problems.length) {
    for (const p of problems) console.log("  gap: " + p);
    console.log("");
    console.log("result: manifest check FAILED (" + problems.length + " gap(s))");
    process.exit(1);
  }
  console.log("  sources: " + manifest.rows.length + " rows verified");
  console.log("  coverage: templates/, .githooks/, agent-skills/ fully covered");
  console.log("  semantic steps: " + manifest.semantic.length + " rows, all gated <= v" + current);
  console.log("");
  console.log("result: manifest OK");
  process.exit(0);
}

function main(argv) {
  let target = null, forgeOverride = null, doApply = false, doCheck = false;
  let preApplyComplete = false;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--target") {
      i += 1;
      if (i >= argv.length) die("--target needs a path");
      target = argv[i];
    } else if (a === "--forge") {
      i += 1;
      if (i >= argv.length) die("--forge needs a value");
      forgeOverride = argv[i];
      if (!["github", "gitlab", "azdo", "unknown"].includes(forgeOverride)) {
        die("--forge must be github|gitlab|azdo|unknown");
      }
    } else if (a === "--apply") {
      doApply = true;
    } else if (a === "--pre-apply-complete") {
      preApplyComplete = true;
    } else if (a === "--check-manifest") {
      doCheck = true;
    } else {
      die("unknown argument: " + a);
    }
  }

  const toolRoot = fs.realpathSync(path.join(path.dirname(fileURLToPath(import.meta.url)), ".."));
  const currentVersion = readText(path.join(toolRoot, "VERSION")).trim();
  const manifest = parseManifest(toolRoot);

  console.log("agent-memory reconcile — tool v" + currentVersion);
  if (doCheck) {
    console.log("mode:      check-manifest");
    console.log("");
    checkManifest(toolRoot, manifest);
    return;
  }

  if (!target) die("--target <path> is required (or --check-manifest)");
  if (target === "~" || target.startsWith("~/")) target = path.join(os.homedir(), target.slice(1));
  const resolved = realpathNonStrict(path.resolve(target));
  if (!fs.existsSync(resolved) || !fs.statSync(resolved).isDirectory()) {
    die("target does not exist: " + resolved);
  }
  target = fs.realpathSync(resolved);
  if (target === fs.realpathSync(os.homedir())) {
    die("the target is the user's home directory — never a repo target (target-repo scope only)");
  }
  if (target === toolRoot) die("the target is the agent-memory tool itself — nothing to enable");

  const installed = detectInstalled(target);
  if (installed !== null && installed !== "2.x" &&
      semverLt(parseSemver(currentVersion), parseSemver(installed))) {
    die("target is on v" + installed + " — newer than this tool checkout (v" +
      currentVersion + "); update the tool instead (ENABLE.md Mode B: stop)");
  }
  const forge = forgeOverride || detectForge(target);
  const forgeHow = forgeOverride ? "--forge" : "detected";

  console.log("target:    " + target);
  if (installed === null) console.log("installed: (fresh — no memory layer)");
  else if (installed === "2.x") console.log("installed: 2.x baseline (memory present, no version stamp)");
  else console.log("installed: " + installed);
  console.log("forge:     " + forge + " (" + forgeHow + ")");
  console.log("mode:      " + (doApply ? "apply" : "dry-run"));

  const [mechanical, agent, semantic, notes] = buildPlan(
    toolRoot, target, manifest, forge, installed, currentVersion);
  printReport(mechanical, agent, semantic, notes);

  const pending = mechanical.length + agent.length + semantic.length;
  if (doApply) {
    const [preSteps, hard, confirmation] = preApplyState(
      installed, semantic, mechanical, notes);
    const blocked = [...hard].sort();
    if (blocked.length) {
      console.log("result: blocked — PRE-APPLY boundary unresolved for: " + blocked.join(", "));
      console.log("no target files were written; complete the listed preservation, " +
        "provenance, merge, and hash checks, then rerun the dry-run");
      process.exit(1);
    }
    if ((preSteps.length || confirmation.size) && !preApplyComplete) {
      console.log("result: blocked — no hard PRE-APPLY boundary writes remain, but " +
        "explicit confirmation is required");
      console.log("no target files were written; after completing the listed checks, " +
        "rerun with --apply --pre-apply-complete");
      process.exit(1);
    }
    const applied = applyMechanical(toolRoot, target, mechanical);
    const remaining = agent.length + semantic.length;
    console.log("result: applied " + applied + " mechanical change(s); " +
      remaining + " agent item(s) remain (listed above)");
    process.exit(0);
  }
  if (pending === 0) {
    console.log("result: converged — nothing to do");
    process.exit(0);
  }
  const hint = mechanical.length
    ? "re-run with --apply for the mechanical part"
    : "all pending items are agent work";
  console.log("result: " + mechanical.length + " mechanical + " +
    (agent.length + semantic.length) + " agent item(s) pending " +
    "(dry-run — " + hint + ")");
  process.exit(3);
}

export { main };

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    main(process.argv.slice(2));
  } catch (e) {
    if (e instanceof Die) {
      console.log("error: " + e.message);
      process.exit(1);
    }
    throw e;
  }
}
