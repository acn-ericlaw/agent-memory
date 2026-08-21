#!/usr/bin/env node
// Mirror tests for scripts/reconcile.mjs (Python twin: test_reconcile.py).
// Run: node --test scripts/test_reconcile.mjs
// Tests run against the REAL tool checkout as the source of truth, writing only to
// temp dirs — so they double as a validation of MANIFEST.md itself.

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import {
  POLICIES, FORGES, parseSemver, parseManifest, detectInstalled, detectForge,
  buildPlan, applyMechanical, safeTargetPath, main,
} from "./reconcile.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TOOL_ROOT = fs.realpathSync(path.join(HERE, ".."));
const MANIFEST = parseManifest(TOOL_ROOT);
const CURRENT = fs.readFileSync(path.join(TOOL_ROOT, "VERSION"), "utf-8").trim();

function tmpdir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "reconcile-test-"));
}

function makeTarget(tmp, forgeUrl = null, hookspath = null) {
  const t = path.join(tmp, "target");
  fs.mkdirSync(path.join(t, ".git"), { recursive: true });
  let cfg = "";
  if (forgeUrl) cfg += '[remote "origin"]\n\turl = ' + forgeUrl + "\n";
  if (hookspath) cfg += "[core]\n\thookspath = " + hookspath + "\n";
  fs.writeFileSync(path.join(t, ".git", "config"), cfg);
  return t;
}

function stampVersion(t, version) {
  fs.mkdirSync(path.join(t, ".agent"), { recursive: true });
  fs.writeFileSync(path.join(t, ".agent", "version.md"),
    "- **version:**       " + version + "\n- **enabled_with:**  " + version +
    "\n- **last_upgraded:** 2026-01-01\n- **mode:**          A\n");
}

function snapshotTree(root) {
  const snapshot = {};
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile()) {
        snapshot[path.relative(root, full)] = fs.readFileSync(full).toString("base64");
      }
    }
  }
  walk(root);
  return snapshot;
}

function runCli(t, ...args) {
  return spawnSync(process.execPath, [path.join(HERE, "reconcile.mjs"), "--target", t, ...args],
    { encoding: "utf-8" });
}

function plan(t, forge = null) {
  const installed = detectInstalled(t);
  return buildPlan(TOOL_ROOT, t, MANIFEST, forge || detectForge(t), installed, CURRENT);
}

// -- parsing --------------------------------------------------------------

test("parse_semver", () => {
  assert.deepEqual(parseSemver("4.14.1"), [4, 14, 1]);
  assert.deepEqual(parseSemver("2.x"), [2, 0, 0]);
  assert.equal(parseSemver("not-a-version"), null);
});

test("manifest shape", () => {
  assert.ok(MANIFEST.rows.length >= 35);
  assert.ok(MANIFEST.rows.every((r) => POLICIES.has(r.policy)));
  assert.ok(MANIFEST.rows.every((r) => FORGES.has(r.forge)));
  assert.ok(MANIFEST.semantic.length >= 14);
  for (const s of MANIFEST.semantic) assert.notEqual(parseSemver(s.below), null);
  const agents = MANIFEST.rows.filter((r) => r.target === "AGENTS.md");
  assert.equal(agents[0].source, "templates/AGENTS.md"); // never the root dispatcher
  const protocol = MANIFEST.rows.filter((r) => r.target === "memory/PROTOCOL.md");
  assert.equal(protocol[0].source, "templates/memory/PROTOCOL.md");
  assert.equal(protocol[0].policy, "seed-copy");
  const targets = MANIFEST.rows.map((r) => r.target);
  assert.ok(targets.indexOf("memory/PROTOCOL.md") < targets.indexOf("AGENTS.md"));
});

// -- fresh enable ---------------------------------------------------------

test("fresh plan and apply", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  const [mech, agent, semantic] = plan(t);
  assert.deepEqual(semantic, []); // fresh: nothing to migrate
  const verbs = new Set(mech.map(([v, r]) => v + " " + r.target));
  assert.ok(verbs.has("copy DECAY.md"));
  assert.ok(verbs.has("copy agent-skills/memory-lint/"));
  const gen = new Set(agent.filter(([v]) => v === "generate").map(([, p]) => p));
  assert.ok(gen.has("memory/continuity.md"));
  assert.ok(gen.has("memory/sessions/"));
  assert.ok(agent.some(([v]) => v === "stamp"));

  applyMechanical(TOOL_ROOT, t, mech);
  assert.ok(fs.readFileSync(path.join(TOOL_ROOT, "DECAY.md")).equals(
    fs.readFileSync(path.join(t, "DECAY.md"))));
  assert.ok((fs.statSync(path.join(t, ".githooks", "pre-commit")).mode & 0o100) !== 0);
  const [mech2] = plan(t);
  assert.deepEqual(mech2, []); // idempotent
});

test("seed-generate reported, not written", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  const [mech] = plan(t);
  applyMechanical(TOOL_ROOT, t, mech);
  assert.ok(!fs.existsSync(path.join(t, "CLAUDE.md")));
  assert.ok(!fs.existsSync(path.join(t, "memory", "continuity.md")));
  assert.ok(!fs.existsSync(path.join(t, ".agent", "version.md"))); // stamp is agent-owned
});

// -- drift and preservation -----------------------------------------------

test("verbatim drift recopied", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  const [mech] = plan(t);
  applyMechanical(TOOL_ROOT, t, mech);
  fs.appendFileSync(path.join(t, "REVIEW.md"), "LOCAL EDIT\n");
  const [mech2] = plan(t);
  assert.ok(mech2.some(([v, r]) => v === "recopy" && r.target === "REVIEW.md"));
  applyMechanical(TOOL_ROOT, t, mech2);
  assert.ok(fs.readFileSync(path.join(TOOL_ROOT, "REVIEW.md")).equals(
    fs.readFileSync(path.join(t, "REVIEW.md"))));
});

test("seed-copy never overwritten", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  const [mech] = plan(t);
  applyMechanical(TOOL_ROOT, t, mech);
  const marker = "# my local waiver\n";
  fs.appendFileSync(path.join(t, ".agent", "secret-scan-ignore"), marker);
  const [mech2, , , notes2] = plan(t);
  assert.ok(!mech2.some(([, r]) => r.target === ".agent/secret-scan-ignore"));
  assert.ok(notes2.some(([v, p]) => v === "keep" && p === ".agent/secret-scan-ignore"));
  applyMechanical(TOOL_ROOT, t, mech2);
  assert.ok(fs.readFileSync(path.join(t, ".agent", "secret-scan-ignore"), "utf-8").includes(marker));
});

test("seed-generate content untouched", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.writeFileSync(path.join(t, "memory", "continuity.md"), "user content\n");
  const [mech, agent] = plan(t);
  applyMechanical(TOOL_ROOT, t, mech);
  const gen = new Set(agent.filter(([v]) => v === "generate").map(([, p]) => p));
  assert.ok(!gen.has("memory/continuity.md"));
  assert.equal(fs.readFileSync(path.join(t, "memory", "continuity.md"), "utf-8"), "user content\n");
});

test("exec bit repaired", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  const [mech] = plan(t);
  applyMechanical(TOOL_ROOT, t, mech);
  const hook = path.join(t, ".githooks", "post-commit");
  fs.chmodSync(hook, 0o644);
  const [mech2] = plan(t);
  assert.ok(mech2.some(([v, r]) => v === "chmod" && r.target === ".githooks/post-commit"));
  applyMechanical(TOOL_ROOT, t, mech2);
  assert.ok((fs.statSync(hook).mode & 0o100) !== 0);
});

// -- sentinel merge ---------------------------------------------------------

test("sentinel merge is add-only and deduped", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.writeFileSync(path.join(t, ".gitignore"), "node_modules/\n.claude/\n");
  const [mech] = plan(t);
  applyMechanical(TOOL_ROOT, t, mech);
  const text = fs.readFileSync(path.join(t, ".gitignore"), "utf-8");
  assert.ok(text.startsWith("node_modules/\n.claude/\n")); // never reordered
  assert.equal(text.split("\n").filter((l) => l.trim() === ".claude/").length, 1); // deduped
  assert.ok(text.includes("agent-memory: AI infrastructure"));
  assert.ok(text.includes("review-scratch/"));
  const [mech2] = plan(t);
  assert.ok(!mech2.some(([, r]) => r.target === ".gitignore")); // idempotent
});

// -- forge handling ---------------------------------------------------------

test("forge filtering", () => {
  const tGh = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  const [mech] = plan(tGh);
  const targets = mech.map(([, r]) => r.target);
  assert.ok(targets.includes(".github/workflows/agent-memory.yml"));
  assert.ok(!targets.includes(".gitlab/agent-memory-ci.yml"));
  assert.ok(!targets.includes(".azuredevops/agent-memory-ci.yml"));

  const tUnknown = makeTarget(tmpdir());
  const [mechU] = plan(tUnknown);
  const targetsU = mechU.map(([, r]) => r.target);
  assert.ok(targetsU.includes(".github/workflows/agent-memory.yml"));
  assert.ok(targetsU.includes(".gitlab/agent-memory-ci.yml"));
  assert.ok(!targetsU.includes(".azuredevops/agent-memory-ci.yml")); // positive detection only
});

test("gitlab wire item on pre-existing root CI", () => {
  const t = makeTarget(tmpdir(), "git@gitlab.com:acme/demo.git");
  fs.writeFileSync(path.join(t, ".gitlab-ci.yml"),
    "stages:\n  - build\nmyjob:\n  stage: build\n  script: [echo hi]\n");
  const [mech, agent] = plan(t);
  assert.ok(agent.some(([v]) => v === "wire"));
  applyMechanical(TOOL_ROOT, t, mech);
  assert.ok(!fs.readFileSync(path.join(t, ".gitlab-ci.yml"), "utf-8").includes("agent-memory"));
});

test("azdo detection and activation note", () => {
  const t = makeTarget(tmpdir(), "https://dev.azure.com/org/proj/_git/repo");
  assert.equal(detectForge(t), "azdo");
  const [, , , notes] = plan(t);
  assert.ok(notes.some(([v]) => v === "forge"));
});

// -- versions and semantic gating -------------------------------------------

test("semantic gating", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.writeFileSync(path.join(t, "memory", "instructions.md"), "");
  stampVersion(t, "4.14.1");
  const [, , semantic] = plan(t);
  const belows = semantic.map((s) => s.below);
  assert.ok(belows.includes("4.16.0"));
  assert.ok(belows.includes("4.29.0"));
  assert.ok(!belows.includes("3.0.0")); // already above
  stampVersion(t, CURRENT);
  const [, , semantic2] = plan(t);
  assert.deepEqual(semantic2, []);
});

test("protocol pointer is a 4.37 pre-apply step", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.writeFileSync(path.join(t, "memory", "instructions.md"), "");
  stampVersion(t, "4.36.0");
  const [, , semantic] = plan(t);
  const pointer = semantic.filter((s) => s.below === "4.37.0");
  assert.equal(pointer.length, 1);
  assert.ok(pointer[0].step.startsWith("PRE-APPLY:"));
  stampVersion(t, "4.37.0");
  const [, , semantic2] = plan(t);
  assert.ok(!semantic2.map((s) => s.below).includes("4.37.0"));
});

test("apply blocks legacy boundaries without writing", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  stampVersion(t, "4.35.0");
  fs.writeFileSync(path.join(t, "AGENTS.md"), "legacy project instructions\n");
  fs.mkdirSync(path.join(t, ".githooks"), { recursive: true });
  fs.writeFileSync(path.join(t, ".githooks", "pre-commit"),
    "#!/usr/bin/env bash\necho local-check\n");
  const before = snapshotTree(t);
  const stopped = runCli(t, "--apply");
  assert.equal(stopped.status, 1);
  assert.deepEqual(snapshotTree(t), before);
  assert.ok(!fs.existsSync(path.join(t, "DECAY.md")));
});

function dryRunResult(t) {
  const done = runCli(t);
  const lines = done.stdout.trim().split("\n");
  return [done.status, lines[lines.length - 1]];
}

test("dry-run hint names the apply refusal", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  stampVersion(t, "4.36.0");
  fs.writeFileSync(path.join(t, "AGENTS.md"), "legacy project instructions\n");
  const [status, result] = dryRunResult(t);
  assert.equal(status, 3);
  assert.ok(result.includes("--apply refuses until the PRE-APPLY boundary converges for: " +
    "AGENTS.md, memory/PROTOCOL.md"), result);
  assert.ok(!result.includes("re-run with --apply for the mechanical part"), result);
  // The dry-run is the consent artifact: its hint must agree with --apply.
  const blocked = runCli(t, "--apply");
  assert.equal(blocked.status, 1);
  assert.ok(blocked.stdout.includes("AGENTS.md, memory/PROTOCOL.md"), blocked.stdout);
});

test("dry-run hint names the confirmation flag", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.copyFileSync(path.join(TOOL_ROOT, "templates", "AGENTS.md"), path.join(t, "AGENTS.md"));
  fs.writeFileSync(path.join(t, "memory", "PROTOCOL.md"), "repository-specific instructions\n");
  const [status, result] = dryRunResult(t);
  assert.equal(status, 3);
  assert.ok(result.includes("re-run with --apply --pre-apply-complete once the listed " +
    "PRE-APPLY checks are done"), result);
});

test("dry-run hint stays plain with no boundary", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  const [status, result] = dryRunResult(t);
  assert.equal(status, 3);
  assert.ok(result.includes("re-run with --apply for the mechanical part"), result);
});

test("apply proceeds after explicit pre-apply completion", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  stampVersion(t, "4.35.0");
  fs.mkdirSync(path.join(t, ".githooks", "pre-commit.d"), { recursive: true });
  const local = path.join(t, ".githooks", "pre-commit.d", "40-local-check");
  fs.writeFileSync(local, "#!/usr/bin/env bash\necho preserved\n");
  fs.chmodSync(local, 0o755);
  for (const hook of ["pre-commit", "post-commit"]) {
    const hookPath = path.join(t, ".githooks", hook);
    fs.writeFileSync(hookPath, "#!/usr/bin/env bash\necho inspected-stock-monolith\n");
    fs.chmodSync(hookPath, 0o755);
  }
  const installs = new Map([
    ["AGENTS.md", "templates/AGENTS.md"],
    ["memory/PROTOCOL.md", "templates/memory/PROTOCOL.md"],
  ]);
  for (const [targetRel, sourceRel] of installs) {
    const targetPath = path.join(t, targetRel);
    const sourcePath = path.join(TOOL_ROOT, sourceRel);
    fs.mkdirSync(path.dirname(targetPath), { recursive: true });
    fs.copyFileSync(sourcePath, targetPath);
    fs.chmodSync(targetPath, fs.statSync(sourcePath).mode);
  }
  const beforeConfirmation = snapshotTree(t);
  const stopped = runCli(t, "--apply");
  assert.equal(stopped.status, 1);
  assert.deepEqual(snapshotTree(t), beforeConfirmation);
  const applied = runCli(t, "--apply", "--pre-apply-complete");
  assert.equal(applied.status, 0, applied.stdout + applied.stderr);
  assert.ok(fs.existsSync(path.join(t, "DECAY.md")));
  assert.equal(fs.readFileSync(local, "utf-8"), "#!/usr/bin/env bash\necho preserved\n");
  for (const hook of ["pre-commit", "post-commit"]) {
    assert.deepEqual(fs.readFileSync(path.join(t, ".githooks", hook)),
      fs.readFileSync(path.join(TOOL_ROOT, ".githooks", hook)));
  }
});

test("fresh custom protocol collision blocks without writing", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.writeFileSync(path.join(t, "memory", "PROTOCOL.md"),
    "repository-specific instructions\n");
  const before = snapshotTree(t);
  const stopped = runCli(t, "--apply");
  assert.equal(stopped.status, 1);
  assert.deepEqual(snapshotTree(t), before);
});

test("fresh exact shim custom protocol requires confirmation", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.copyFileSync(path.join(TOOL_ROOT, "templates", "AGENTS.md"), path.join(t, "AGENTS.md"));
  const protocol = path.join(t, "memory", "PROTOCOL.md");
  fs.writeFileSync(protocol, "repository-specific instructions\n");
  const before = snapshotTree(t);
  const stopped = runCli(t, "--apply");
  assert.equal(stopped.status, 1);
  assert.deepEqual(snapshotTree(t), before);
  const applied = runCli(t, "--apply", "--pre-apply-complete");
  assert.equal(applied.status, 0, applied.stdout + applied.stderr);
  assert.equal(fs.readFileSync(protocol, "utf-8"), "repository-specific instructions\n");
});

test("current stamp cannot authorize root recopy", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  stampVersion(t, "4.37.0");
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.writeFileSync(path.join(t, "AGENTS.md"), "legacy root instructions\n");
  fs.writeFileSync(path.join(t, "memory", "PROTOCOL.md"), "custom protocol\n");
  const before = snapshotTree(t);
  const stopped = runCli(t, "--apply", "--pre-apply-complete");
  assert.equal(stopped.status, 1);
  assert.deepEqual(snapshotTree(t), before);
});

test("current hook drift requires confirmation", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  stampVersion(t, "4.37.0");
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.mkdirSync(path.join(t, ".githooks", "pre-commit.d"), { recursive: true });
  fs.copyFileSync(path.join(TOOL_ROOT, "templates", "AGENTS.md"), path.join(t, "AGENTS.md"));
  fs.copyFileSync(path.join(TOOL_ROOT, "templates", "memory", "PROTOCOL.md"),
    path.join(t, "memory", "PROTOCOL.md"));
  const hook = path.join(t, ".githooks", "pre-commit");
  fs.writeFileSync(hook, "#!/usr/bin/env bash\necho inspected-local-hook\n");
  fs.chmodSync(hook, 0o755);
  const local = path.join(t, ".githooks", "pre-commit.d", "40-local-check");
  fs.writeFileSync(local, "#!/usr/bin/env bash\necho preserved\n");
  fs.chmodSync(local, 0o755);
  const managed = path.join(t, ".githooks", "pre-commit.d",
    "50-agent-memory-secret-guard");
  fs.writeFileSync(managed, "#!/usr/bin/env bash\necho inspected-managed-drift\n");
  fs.chmodSync(managed, 0o755);
  const before = snapshotTree(t);
  const stopped = runCli(t, "--apply");
  assert.equal(stopped.status, 1);
  assert.deepEqual(snapshotTree(t), before);
  const applied = runCli(t, "--apply", "--pre-apply-complete");
  assert.equal(applied.status, 0, applied.stdout + applied.stderr);
  assert.equal(fs.readFileSync(local, "utf-8"), "#!/usr/bin/env bash\necho preserved\n");
  assert.deepEqual(fs.readFileSync(hook),
    fs.readFileSync(path.join(TOOL_ROOT, ".githooks", "pre-commit")));
  assert.deepEqual(fs.readFileSync(managed), fs.readFileSync(path.join(
    TOOL_ROOT, ".githooks", "pre-commit.d", "50-agent-memory-secret-guard")));
});

test("2.x baseline detection", () => {
  const t = makeTarget(tmpdir());
  fs.mkdirSync(path.join(t, "memory"), { recursive: true });
  fs.writeFileSync(path.join(t, "memory", "instructions.md"), "");
  assert.equal(detectInstalled(t), "2.x");
  const [, , semantic] = plan(t);
  assert.ok(semantic.map((s) => s.below).includes("3.0.0"));
});

test("hooksPath activation item", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git", ".githooks");
  const [, agent] = plan(t);
  assert.ok(!agent.some(([v]) => v === "activate"));
  const t2 = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  const [, agent2] = plan(t2);
  assert.ok(agent2.some(([v]) => v === "activate"));
});

// -- safety -------------------------------------------------------------------

test("safe_target_path blocks escape", () => {
  const t = makeTarget(tmpdir());
  assert.throws(() => safeTargetPath(t, "../outside.md"));
});

// -- hardening (adversarial pre-ship review, v4.35.0) ---------------------------

test("newer target refused", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  stampVersion(t, "9.9.9");
  assert.throws(() => main(["--target", t]), /newer than this tool checkout/); // Mode B: stop
});

test("symlink escape refused and victim intact", () => {
  const tmp = tmpdir();
  const t = makeTarget(tmp, "https://github.com/acme/demo.git");
  const outside = path.join(tmp, "outside");
  fs.mkdirSync(outside);
  const victim = path.join(outside, "victim.md");
  fs.writeFileSync(victim, "victim content\n");
  fs.symlinkSync(victim, path.join(t, "DECAY.md")); // file symlink out of the target
  assert.throws(() => plan(t), /escapes the target/);
  fs.unlinkSync(path.join(t, "DECAY.md"));
  fs.symlinkSync(outside, path.join(t, ".github")); // dir symlink out of the target
  assert.throws(() => plan(t), /escapes the target/);
  assert.equal(fs.readFileSync(victim, "utf-8"), "victim content\n");
});

test("CRLF target preserved", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.writeFileSync(path.join(t, ".gitignore"), Buffer.from("node_modules/\r\n.claude/\r\n"));
  const [mech] = plan(t);
  applyMechanical(TOOL_ROOT, t, mech);
  const data = fs.readFileSync(path.join(t, ".gitignore"));
  const prefix = Buffer.from("node_modules/\r\n.claude/\r\n");
  assert.ok(data.subarray(0, prefix.length).equals(prefix)); // user bytes untouched
  assert.ok(data.toString("utf-8").includes("review-scratch/"));
  const [mech2] = plan(t);
  assert.ok(!mech2.some(([, r]) => r.target === ".gitignore")); // CRLF dedup holds
});

test("wrong-kind target refused", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.mkdirSync(path.join(t, "DECAY.md"));
  assert.throws(() => plan(t), /expected a file/);
});

test("non-UTF8 sentinel refused", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.writeFileSync(path.join(t, ".gitignore"), Buffer.from([0x63, 0x61, 0x66, 0xe9, 0x2f, 0x0a]));
  assert.throws(() => plan(t), /not valid UTF-8/);
});

test("home target refused", () => {
  const tmp = tmpdir();
  const fakeHome = path.join(tmp, "home");
  fs.mkdirSync(fakeHome);
  const saved = process.env.HOME;
  try {
    process.env.HOME = fakeHome;
    assert.throws(() => main(["--target", fakeHome]), /home directory/);
  } finally {
    process.env.HOME = saved;
  }
});

test("hooksPath variants", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git", ".githooks/");
  const [, agent] = plan(t);
  assert.ok(!agent.some(([v]) => v === "activate")); // trailing slash = activated
  const t2 = makeTarget(tmpdir(), "https://github.com/acme/demo.git", ".husky");
  const [, agent2] = plan(t2);
  const details = agent2.filter(([v]) => v === "activate").map(([, , d]) => d);
  assert.ok(details.length && details[0].includes("currently: .husky")); // arbitration, not "unset"
});

test("N.x stamp refused", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  stampVersion(t, "4.x");
  assert.throws(() => detectInstalled(t));
});

test("sessions with only .DS_Store not present", () => {
  const t = makeTarget(tmpdir(), "https://github.com/acme/demo.git");
  fs.mkdirSync(path.join(t, "memory", "sessions"), { recursive: true });
  fs.writeFileSync(path.join(t, "memory", "sessions", ".DS_Store"), "");
  const [, agent] = plan(t);
  const gen = new Set(agent.filter(([v]) => v === "generate").map(([, p]) => p));
  assert.ok(gen.has("memory/sessions/"));
});
