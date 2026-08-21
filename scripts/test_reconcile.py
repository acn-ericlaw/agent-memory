#!/usr/bin/env python3
"""Mirror tests for scripts/reconcile.py (Node twin: test_reconcile.mjs).

Run: python3 -m unittest scripts/test_reconcile.py  (or cd scripts && python3 -m unittest test_reconcile)
Tests run against the REAL tool checkout as the source of truth, writing only to
temp dirs — so they double as a validation of MANIFEST.md itself.
"""

import contextlib
import importlib.util
import io
import os
import shutil
import stat
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL_ROOT = os.path.realpath(os.path.join(HERE, ".."))

spec = importlib.util.spec_from_file_location("reconcile", os.path.join(HERE, "reconcile.py"))
rec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rec)


def make_target(tmp, forge_url=None, hookspath=None):
    t = os.path.join(tmp, "target")
    os.makedirs(os.path.join(t, ".git"), exist_ok=True)
    cfg = ""
    if forge_url:
        cfg += '[remote "origin"]\n\turl = ' + forge_url + "\n"
    if hookspath:
        cfg += "[core]\n\thookspath = " + hookspath + "\n"
    with open(os.path.join(t, ".git", "config"), "w", encoding="utf-8") as f:
        f.write(cfg)
    return t


def stamp(t, version):
    os.makedirs(os.path.join(t, ".agent"), exist_ok=True)
    with open(os.path.join(t, ".agent", "version.md"), "w", encoding="utf-8") as f:
        f.write("- **version:**       " + version + "\n- **enabled_with:**  " + version +
                "\n- **last_upgraded:** 2026-01-01\n- **mode:**          A\n")


def snapshot_tree(root):
    snapshot = {}
    for base, _dirs, files in os.walk(root):
        for name in files:
            path = os.path.join(base, name)
            rel = os.path.relpath(path, root)
            with open(path, "rb") as f:
                snapshot[rel] = f.read()
    return snapshot


class ReconcileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="reconcile-test-")
        self.manifest = rec.parse_manifest(TOOL_ROOT)
        with open(os.path.join(TOOL_ROOT, "VERSION"), encoding="utf-8") as f:
            self.current = f.read().strip()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def plan(self, target, forge=None):
        installed = rec.detect_installed(target)
        forge = forge or rec.detect_forge(target)
        return rec.build_plan(TOOL_ROOT, target, self.manifest, forge, installed, self.current)

    # -- parsing --------------------------------------------------------------

    def test_parse_semver(self):
        self.assertEqual(rec.parse_semver("4.14.1"), (4, 14, 1))
        self.assertEqual(rec.parse_semver("2.x"), (2, 0, 0))
        self.assertIsNone(rec.parse_semver("not-a-version"))

    def test_manifest_shape(self):
        rows = self.manifest["rows"]
        self.assertGreaterEqual(len(rows), 35)
        self.assertTrue(all(r["policy"] in rec.POLICIES for r in rows))
        self.assertTrue(all(r["forge"] in rec.FORGES for r in rows))
        self.assertGreaterEqual(len(self.manifest["semantic"]), 14)
        for s in self.manifest["semantic"]:
            self.assertIsNotNone(rec.parse_semver(s["below"]))
        agents = [r for r in rows if r["target"] == "AGENTS.md"]
        self.assertEqual(agents[0]["source"], "templates/AGENTS.md")  # never the root dispatcher
        protocol = [r for r in rows if r["target"] == "memory/PROTOCOL.md"]
        self.assertEqual(protocol[0]["source"], "templates/memory/PROTOCOL.md")
        self.assertEqual(protocol[0]["policy"], "seed-copy")
        targets = [r["target"] for r in rows]
        self.assertLess(targets.index("memory/PROTOCOL.md"), targets.index("AGENTS.md"))

    # -- fresh enable ---------------------------------------------------------

    def test_fresh_plan_and_apply(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        mech, agent, semantic, notes = self.plan(t)
        self.assertEqual(semantic, [])  # fresh: nothing to migrate
        verbs = {(v, r["target"]) for v, r, _f, _d in mech}
        self.assertIn(("copy", "DECAY.md"), verbs)
        self.assertIn(("copy", "agent-skills/memory-lint/"), verbs)
        gen = {p for v, p, _d in agent if v == "generate"}
        self.assertIn("memory/continuity.md", gen)
        self.assertIn("memory/sessions/", gen)
        self.assertTrue(any(v == "stamp" for v, _p, _d in agent))

        rec.apply_mechanical(TOOL_ROOT, t, mech)
        with open(os.path.join(TOOL_ROOT, "DECAY.md"), "rb") as a, \
             open(os.path.join(t, "DECAY.md"), "rb") as b:
            self.assertEqual(a.read(), b.read())
        self.assertTrue(os.stat(os.path.join(t, ".githooks", "pre-commit")).st_mode & stat.S_IXUSR)
        mech2, _a2, _s2, _n2 = self.plan(t)
        self.assertEqual(mech2, [])  # idempotent

    def test_seed_generate_reported_not_written(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        mech, _agent, _s, _n = self.plan(t)
        rec.apply_mechanical(TOOL_ROOT, t, mech)
        self.assertFalse(os.path.exists(os.path.join(t, "CLAUDE.md")))
        self.assertFalse(os.path.exists(os.path.join(t, "memory", "continuity.md")))
        self.assertFalse(os.path.exists(os.path.join(t, ".agent", "version.md")))  # stamp is agent-owned

    # -- drift and preservation -----------------------------------------------

    def test_verbatim_drift_recopied(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        mech, _a, _s, _n = self.plan(t)
        rec.apply_mechanical(TOOL_ROOT, t, mech)
        with open(os.path.join(t, "REVIEW.md"), "a", encoding="utf-8") as f:
            f.write("LOCAL EDIT\n")
        mech2, _a2, _s2, _n2 = self.plan(t)
        drifted = [(v, r["target"]) for v, r, _f, _d in mech2]
        self.assertIn(("recopy", "REVIEW.md"), drifted)
        rec.apply_mechanical(TOOL_ROOT, t, mech2)
        with open(os.path.join(TOOL_ROOT, "REVIEW.md"), "rb") as a, \
             open(os.path.join(t, "REVIEW.md"), "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_seed_copy_never_overwritten(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        mech, _a, _s, _n = self.plan(t)
        rec.apply_mechanical(TOOL_ROOT, t, mech)
        marker = "# my local waiver\n"
        with open(os.path.join(t, ".agent", "secret-scan-ignore"), "a", encoding="utf-8") as f:
            f.write(marker)
        mech2, _a2, _s2, notes2 = self.plan(t)
        self.assertNotIn(".agent/secret-scan-ignore", [r["target"] for _v, r, _f, _d in mech2])
        self.assertIn(("keep", ".agent/secret-scan-ignore"),
                      [(v, p) for v, p, _d in notes2 if v == "keep"])
        rec.apply_mechanical(TOOL_ROOT, t, mech2)
        with open(os.path.join(t, ".agent", "secret-scan-ignore"), encoding="utf-8") as f:
            self.assertIn(marker, f.read())

    def test_seed_generate_content_untouched(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        with open(os.path.join(t, "memory", "continuity.md"), "w", encoding="utf-8") as f:
            f.write("user content\n")
        mech, agent, _s, _n = self.plan(t)
        rec.apply_mechanical(TOOL_ROOT, t, mech)
        self.assertNotIn("memory/continuity.md", {p for v, p, _d in agent if v == "generate"})
        with open(os.path.join(t, "memory", "continuity.md"), encoding="utf-8") as f:
            self.assertEqual(f.read(), "user content\n")

    def test_exec_bit_repaired(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        mech, _a, _s, _n = self.plan(t)
        rec.apply_mechanical(TOOL_ROOT, t, mech)
        hook = os.path.join(t, ".githooks", "post-commit")
        os.chmod(hook, 0o644)
        mech2, _a2, _s2, _n2 = self.plan(t)
        self.assertIn(("chmod", ".githooks/post-commit"),
                      [(v, r["target"]) for v, r, _f, _d in mech2])
        rec.apply_mechanical(TOOL_ROOT, t, mech2)
        self.assertTrue(os.stat(hook).st_mode & stat.S_IXUSR)

    # -- sentinel merge ---------------------------------------------------------

    def test_sentinel_merge_add_only_dedup(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        original = "node_modules/\n.claude/\n"
        with open(os.path.join(t, ".gitignore"), "w", encoding="utf-8") as f:
            f.write(original)
        mech, _a, _s, _n = self.plan(t)
        rec.apply_mechanical(TOOL_ROOT, t, mech)
        with open(os.path.join(t, ".gitignore"), encoding="utf-8") as f:
            text = f.read()
        self.assertTrue(text.startswith("node_modules/\n.claude/\n"))  # never reordered
        self.assertEqual(text.count("\n.claude/\n") + text.startswith(".claude/\n"), 1)  # deduped
        self.assertIn("agent-memory: AI infrastructure", text)
        self.assertIn("review-scratch/", text)
        mech2, _a2, _s2, _n2 = self.plan(t)
        self.assertNotIn(".gitignore", [r["target"] for _v, r, _f, _d in mech2])  # idempotent

    # -- forge handling ---------------------------------------------------------

    def test_forge_filtering(self):
        t_gh = make_target(self.tmp, "https://github.com/acme/demo.git")
        mech, _a, _s, _n = self.plan(t_gh)
        targets = [r["target"] for _v, r, _f, _d in mech]
        self.assertIn(".github/workflows/agent-memory.yml", targets)
        self.assertNotIn(".gitlab/agent-memory-ci.yml", targets)
        self.assertNotIn(".azuredevops/agent-memory-ci.yml", targets)

        os.makedirs(os.path.join(self.tmp, "u", "target", ".git"), exist_ok=True)
        t_unknown = os.path.join(self.tmp, "u", "target")
        open(os.path.join(t_unknown, ".git", "config"), "w").close()
        mech_u, _au, _su, _nu = self.plan(t_unknown)
        targets_u = [r["target"] for _v, r, _f, _d in mech_u]
        self.assertIn(".github/workflows/agent-memory.yml", targets_u)
        self.assertIn(".gitlab/agent-memory-ci.yml", targets_u)
        self.assertNotIn(".azuredevops/agent-memory-ci.yml", targets_u)  # positive detection only

    def test_gitlab_wire_item_on_preexisting_root_ci(self):
        t = make_target(self.tmp, "git@gitlab.com:acme/demo.git")
        with open(os.path.join(t, ".gitlab-ci.yml"), "w", encoding="utf-8") as f:
            f.write("stages:\n  - build\nmyjob:\n  stage: build\n  script: [echo hi]\n")
        mech, agent, _s, _n = self.plan(t)
        self.assertIn("wire", [v for v, _p, _d in agent])
        rec.apply_mechanical(TOOL_ROOT, t, mech)
        with open(os.path.join(t, ".gitlab-ci.yml"), encoding="utf-8") as f:
            self.assertNotIn("agent-memory", f.read())  # never scripted into a user CI file

    def test_azdo_detection_and_note(self):
        t = make_target(self.tmp, "https://dev.azure.com/org/proj/_git/repo")
        self.assertEqual(rec.detect_forge(t), "azdo")
        _m, _a, _s, notes = self.plan(t)
        self.assertTrue(any(v == "forge" for v, _p, _d in notes))

    # -- versions and semantic gating -------------------------------------------

    def test_semantic_gating(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        open(os.path.join(t, "memory", "instructions.md"), "w").close()
        stamp(t, "4.14.1")
        _m, _a, semantic, _n = self.plan(t)
        belows = [s["below"] for s in semantic]
        self.assertIn("4.16.0", belows)
        self.assertIn("4.29.0", belows)
        self.assertNotIn("3.0.0", belows)  # already above
        stamp(t, self.current)
        _m2, _a2, semantic2, _n2 = self.plan(t)
        self.assertEqual(semantic2, [])

    def test_protocol_pointer_is_a_437_pre_apply_step(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        open(os.path.join(t, "memory", "instructions.md"), "w").close()
        stamp(t, "4.36.0")
        _m, _a, semantic, _n = self.plan(t)
        pointer = [s for s in semantic if s["below"] == "4.37.0"]
        self.assertEqual(len(pointer), 1)
        self.assertTrue(pointer[0]["step"].startswith("PRE-APPLY:"))
        stamp(t, "4.37.0")
        _m2, _a2, semantic2, _n2 = self.plan(t)
        self.assertNotIn("4.37.0", [s["below"] for s in semantic2])

    def test_apply_blocks_legacy_boundaries_without_writing(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        stamp(t, "4.35.0")
        with open(os.path.join(t, "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("legacy project instructions\n")
        os.makedirs(os.path.join(t, ".githooks"), exist_ok=True)
        with open(os.path.join(t, ".githooks", "pre-commit"), "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\necho local-check\n")
        before = snapshot_tree(t)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as stopped:
            rec.main(["--target", t, "--apply"])
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(snapshot_tree(t), before)
        self.assertFalse(os.path.exists(os.path.join(t, "DECAY.md")))

    def dry_run(self, target):
        """Return (exit code, last printed line) for a dry-run."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as done:
            rec.main(["--target", target])
        return done.exception.code, buf.getvalue().strip().splitlines()[-1]

    def test_dry_run_hint_names_the_apply_refusal(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        stamp(t, "4.36.0")
        with open(os.path.join(t, "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("legacy project instructions\n")
        code, result = self.dry_run(t)
        self.assertEqual(code, 3)
        self.assertIn("--apply refuses until the PRE-APPLY boundary converges for: "
                      "AGENTS.md, memory/PROTOCOL.md", result)
        self.assertNotIn("re-run with --apply for the mechanical part", result)
        # The dry-run is the consent artifact: its hint must agree with --apply.
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as blocked:
            rec.main(["--target", t, "--apply"])
        self.assertEqual(blocked.exception.code, 1)
        self.assertIn("AGENTS.md, memory/PROTOCOL.md", buf.getvalue())

    def test_dry_run_hint_names_the_confirmation_flag(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        shutil.copy2(os.path.join(TOOL_ROOT, "templates", "AGENTS.md"),
                     os.path.join(t, "AGENTS.md"))
        with open(os.path.join(t, "memory", "PROTOCOL.md"), "w", encoding="utf-8") as f:
            f.write("repository-specific instructions\n")
        code, result = self.dry_run(t)
        self.assertEqual(code, 3)
        self.assertIn("re-run with --apply --pre-apply-complete once the listed "
                      "PRE-APPLY checks are done", result)

    def test_dry_run_hint_stays_plain_with_no_boundary(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        code, result = self.dry_run(t)
        self.assertEqual(code, 3)
        self.assertIn("re-run with --apply for the mechanical part", result)

    def test_apply_proceeds_after_explicit_pre_apply_completion(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        stamp(t, "4.35.0")
        os.makedirs(os.path.join(t, ".githooks", "pre-commit.d"), exist_ok=True)
        local = os.path.join(t, ".githooks", "pre-commit.d", "40-local-check")
        with open(local, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\necho preserved\n")
        os.chmod(local, 0o755)
        for hook in ("pre-commit", "post-commit"):
            hook_path = os.path.join(t, ".githooks", hook)
            with open(hook_path, "w", encoding="utf-8") as f:
                f.write("#!/usr/bin/env bash\necho inspected-stock-monolith\n")
            os.chmod(hook_path, 0o755)
        installs = {
            "AGENTS.md": "templates/AGENTS.md",
            "memory/PROTOCOL.md": "templates/memory/PROTOCOL.md",
        }
        for target_rel, source_rel in installs.items():
            target_path = os.path.join(t, target_rel)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(os.path.join(TOOL_ROOT, source_rel), target_path)
        before_confirmation = snapshot_tree(t)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as stopped:
            rec.main(["--target", t, "--apply"])
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(snapshot_tree(t), before_confirmation)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as applied:
            rec.main(["--target", t, "--apply", "--pre-apply-complete"])
        self.assertEqual(applied.exception.code, 0)
        self.assertTrue(os.path.isfile(os.path.join(t, "DECAY.md")))
        with open(local, "rb") as f:
            self.assertEqual(f.read(), b"#!/usr/bin/env bash\necho preserved\n")
        for hook in ("pre-commit", "post-commit"):
            with open(os.path.join(t, ".githooks", hook), "rb") as actual, \
                    open(os.path.join(TOOL_ROOT, ".githooks", hook), "rb") as expected:
                self.assertEqual(actual.read(), expected.read())

    def test_fresh_custom_protocol_collision_blocks_without_writing(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        with open(os.path.join(t, "memory", "PROTOCOL.md"), "w", encoding="utf-8") as f:
            f.write("repository-specific instructions\n")
        before = snapshot_tree(t)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as stopped:
            rec.main(["--target", t, "--apply"])
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(snapshot_tree(t), before)

    def test_fresh_exact_shim_custom_protocol_requires_confirmation(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        shutil.copy2(os.path.join(TOOL_ROOT, "templates", "AGENTS.md"),
                     os.path.join(t, "AGENTS.md"))
        protocol = os.path.join(t, "memory", "PROTOCOL.md")
        with open(protocol, "w", encoding="utf-8") as f:
            f.write("repository-specific instructions\n")
        before = snapshot_tree(t)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as stopped:
            rec.main(["--target", t, "--apply"])
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(snapshot_tree(t), before)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as applied:
            rec.main(["--target", t, "--apply", "--pre-apply-complete"])
        self.assertEqual(applied.exception.code, 0)
        with open(protocol, encoding="utf-8") as f:
            self.assertEqual(f.read(), "repository-specific instructions\n")

    def test_current_stamp_cannot_authorize_root_recopy(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        stamp(t, "4.37.0")
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        with open(os.path.join(t, "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("legacy root instructions\n")
        with open(os.path.join(t, "memory", "PROTOCOL.md"), "w", encoding="utf-8") as f:
            f.write("custom protocol\n")
        before = snapshot_tree(t)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as stopped:
            rec.main(["--target", t, "--apply", "--pre-apply-complete"])
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(snapshot_tree(t), before)

    def test_current_hook_drift_requires_confirmation(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        stamp(t, "4.37.0")
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        os.makedirs(os.path.join(t, ".githooks", "pre-commit.d"), exist_ok=True)
        shutil.copy2(os.path.join(TOOL_ROOT, "templates", "AGENTS.md"),
                     os.path.join(t, "AGENTS.md"))
        shutil.copy2(os.path.join(TOOL_ROOT, "templates", "memory", "PROTOCOL.md"),
                     os.path.join(t, "memory", "PROTOCOL.md"))
        hook = os.path.join(t, ".githooks", "pre-commit")
        with open(hook, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\necho inspected-local-hook\n")
        os.chmod(hook, 0o755)
        local = os.path.join(t, ".githooks", "pre-commit.d", "40-local-check")
        with open(local, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\necho preserved\n")
        os.chmod(local, 0o755)
        managed = os.path.join(
            t, ".githooks", "pre-commit.d", "50-agent-memory-secret-guard")
        with open(managed, "w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\necho inspected-managed-drift\n")
        os.chmod(managed, 0o755)
        before = snapshot_tree(t)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as stopped:
            rec.main(["--target", t, "--apply"])
        self.assertEqual(stopped.exception.code, 1)
        self.assertEqual(snapshot_tree(t), before)
        with mock.patch("builtins.print"), self.assertRaises(SystemExit) as applied:
            rec.main(["--target", t, "--apply", "--pre-apply-complete"])
        self.assertEqual(applied.exception.code, 0)
        with open(local, "rb") as f:
            self.assertEqual(f.read(), b"#!/usr/bin/env bash\necho preserved\n")
        with open(hook, "rb") as actual, \
                open(os.path.join(TOOL_ROOT, ".githooks", "pre-commit"), "rb") as expected:
            self.assertEqual(actual.read(), expected.read())
        with open(managed, "rb") as actual, open(
                os.path.join(TOOL_ROOT, ".githooks", "pre-commit.d",
                             "50-agent-memory-secret-guard"), "rb") as expected:
            self.assertEqual(actual.read(), expected.read())

    def test_2x_baseline_detection(self):
        t = make_target(self.tmp)
        os.makedirs(os.path.join(t, "memory"), exist_ok=True)
        open(os.path.join(t, "memory", "instructions.md"), "w").close()
        self.assertEqual(rec.detect_installed(t), "2.x")
        _m, _a, semantic, _n = self.plan(t)
        self.assertIn("3.0.0", [s["below"] for s in semantic])

    def test_hookspath_activation_item(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git", hookspath=".githooks")
        _m, agent, _s, _n = self.plan(t)
        self.assertNotIn("activate", [v for v, _p, _d in agent])
        t2 = make_target(os.path.join(self.tmp, "b"), "https://github.com/acme/demo.git")
        _m2, agent2, _s2, _n2 = self.plan(t2)
        self.assertIn("activate", [v for v, _p, _d in agent2])

    # -- safety -------------------------------------------------------------------

    def test_safe_target_path_blocks_escape(self):
        t = make_target(self.tmp)
        with self.assertRaises(SystemExit):
            rec.safe_target_path(t, "../outside.md")

    # -- hardening (adversarial pre-ship review, v4.35.0) ---------------------------

    def test_newer_target_refused(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        stamp(t, "9.9.9")
        with self.assertRaises(SystemExit) as cm:
            rec.main(["--target", t])
        self.assertEqual(cm.exception.code, 1)  # Mode B: stop — never downgrade

    def test_symlink_escape_refused_and_victim_intact(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        outside = os.path.join(self.tmp, "outside")
        os.makedirs(outside)
        victim = os.path.join(outside, "victim.md")
        with open(victim, "w", encoding="utf-8") as f:
            f.write("victim content\n")
        os.symlink(victim, os.path.join(t, "DECAY.md"))  # file symlink out of the target
        with self.assertRaises(SystemExit):
            self.plan(t)
        os.unlink(os.path.join(t, "DECAY.md"))
        os.symlink(outside, os.path.join(t, ".github"))  # dir symlink out of the target
        with self.assertRaises(SystemExit):
            self.plan(t)
        with open(victim, encoding="utf-8") as f:
            self.assertEqual(f.read(), "victim content\n")

    def test_crlf_target_preserved(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        with open(os.path.join(t, ".gitignore"), "wb") as f:
            f.write(b"node_modules/\r\n.claude/\r\n")
        mech, _a, _s, _n = self.plan(t)
        rec.apply_mechanical(TOOL_ROOT, t, mech)
        with open(os.path.join(t, ".gitignore"), "rb") as f:
            data = f.read()
        self.assertTrue(data.startswith(b"node_modules/\r\n.claude/\r\n"))  # user bytes untouched
        self.assertIn(b"review-scratch/", data)
        mech2, _a2, _s2, _n2 = self.plan(t)
        self.assertNotIn(".gitignore", [r["target"] for _v, r, _f, _d in mech2])  # CRLF dedup holds

    def test_wrong_kind_target_refused(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        os.makedirs(os.path.join(t, "DECAY.md"))
        with self.assertRaises(SystemExit):
            self.plan(t)

    def test_non_utf8_sentinel_refused(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        with open(os.path.join(t, ".gitignore"), "wb") as f:
            f.write(b"caf\xe9-dir/\n")
        with self.assertRaises(SystemExit):
            self.plan(t)

    def test_home_target_refused(self):
        fake_home = os.path.join(self.tmp, "home")
        os.makedirs(fake_home)
        with mock.patch.dict(os.environ, {"HOME": fake_home}):
            with self.assertRaises(SystemExit) as cm:
                rec.main(["--target", fake_home])
        self.assertEqual(cm.exception.code, 1)

    def test_hookspath_variants(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git", hookspath=".githooks/")
        _m, agent, _s, _n = self.plan(t)
        self.assertNotIn("activate", [v for v, _p, _d in agent])  # trailing slash = activated
        t2 = make_target(os.path.join(self.tmp, "b"), "https://github.com/acme/demo.git",
                         hookspath=".husky")
        _m2, agent2, _s2, _n2 = self.plan(t2)
        details = [d for v, _p, d in agent2 if v == "activate"]
        self.assertTrue(details and "currently: .husky" in details[0])  # arbitration, not "unset"

    def test_nx_stamp_refused(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        stamp(t, "4.x")
        with self.assertRaises(SystemExit):
            rec.detect_installed(t)

    def test_sessions_with_only_ds_store_not_present(self):
        t = make_target(self.tmp, "https://github.com/acme/demo.git")
        os.makedirs(os.path.join(t, "memory", "sessions"))
        open(os.path.join(t, "memory", "sessions", ".DS_Store"), "w").close()
        _m, agent, _s, _n = self.plan(t)
        self.assertIn("memory/sessions/", {p for v, p, _d in agent if v == "generate"})


if __name__ == "__main__":
    unittest.main()
