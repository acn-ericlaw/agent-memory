#!/usr/bin/env python3
"""reconcile — converge a target repo to the agent-memory target state (MANIFEST.md).

Tool-operator-side (runs from this checkout; never installed into targets). Python 3
stdlib only. A byte-parity Node twin lives at scripts/reconcile.mjs.

Usage:
  python3 scripts/reconcile.py --target <path> [--apply] [--pre-apply-complete]
      [--forge github|gitlab|azdo|unknown]
  python3 scripts/reconcile.py --check-manifest

Default is a dry-run report. --apply performs the mechanical policies only
(verbatim / verbatim-dir / seed-copy / sentinel-merge / chmod); everything else is
printed as the agent's work list. The script never deletes anything, never touches a
seed-generate or existing seed-copy file, and never writes .agent/version.md (the
stamp is the agent's closing step). Exit codes: 0 converged (dry-run) or applied
(--apply) or manifest OK (--check-manifest); 3 pending actions (dry-run); 1 error.
"""

import os
import re
import shutil
import sys

EXCLUDED_DIRS = {"__pycache__", ".DS_Store"}
EXCLUDED_FILE_RE = re.compile(r"(\.py[co]|\.DS_Store)$")
POLICIES = {"verbatim", "verbatim-dir", "seed-copy", "sentinel-merge", "seed-generate", "stamp"}
FORGES = {"all", "github", "gitlab", "azdo"}


def die(msg):
    print("error: " + msg)
    sys.exit(1)


def read_text(path):
    # newline="" preserves the file's own line endings: a sentinel merge on a CRLF
    # target must not silently rewrite the user's whole file to LF (add-only means
    # bytes too), and it keeps the Node twin's behavior byte-identical.
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def parse_semver(s):
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", s)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d+)\.x", s)
    if m:
        return (int(m.group(1)), 0, 0)
    return None


def parse_manifest(tool_root):
    path = os.path.join(tool_root, "MANIFEST.md")
    if not os.path.isfile(path):
        die("MANIFEST.md not found in the tool checkout: " + path)
    text = read_text(path)
    sections = {}
    current = None
    for line in text.split("\n"):
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            current = m.group(1)
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    def table_rows(section):
        rows = []
        for line in sections.get(section, []):
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or cells[0].startswith("---") or set(cells[0]) <= {"-", " "}:
                continue
            rows.append(cells)
        return rows

    rows = []
    for cells in table_rows("Install manifest"):
        if cells[0] == "Target":
            continue
        if len(cells) != 5:
            die("malformed install-manifest row: " + " | ".join(cells))
        target, source, policy, forge, attrs = cells
        if policy not in POLICIES:
            die("unknown policy '" + policy + "' for " + target)
        if forge not in FORGES:
            die("unknown forge '" + forge + "' for " + target)
        rows.append({"target": target, "source": source, "policy": policy,
                     "forge": forge, "attrs": attrs})

    semantic = []
    for cells in table_rows("Semantic steps"):
        if cells[0] == "Below":
            continue
        if len(cells) != 3:
            die("malformed semantic-step row: " + " | ".join(cells))
        below, rung, step = cells
        if parse_semver(below) is None:
            die("bad version in semantic step: " + below)
        semantic.append({"below": below, "rung": rung, "step": step})

    tool_only_text = "\n".join(sections.get("Tool-only (never installed)", []))
    if not rows:
        die("MANIFEST.md has no install-manifest rows")
    return {"rows": rows, "semantic": semantic, "tool_only": tool_only_text}


def detect_installed(target):
    """Returns version string, '2.x', or None for a fresh target. Dies on malformed."""
    vpath = os.path.join(target, ".agent", "version.md")
    if os.path.isfile(vpath):
        text = read_text(vpath)
        # a stamp must be a full semver; the "N.x" form is internal to the no-stamp
        # 2.x baseline and is malformed when written into a target's version.md
        m = re.search(r"\*\*version:\*\*\s*(\S+)", text) or re.search(r"^version:\s*(\S+)", text, re.M)
        if not m or not re.fullmatch(r"\d+\.\d+\.\d+", m.group(1)):
            die("unreadable .agent/version.md in the target — repair it first "
                "(memory-lint check_version_manifest); found no valid version value")
        return m.group(1)
    if os.path.isfile(os.path.join(target, "memory", "instructions.md")):
        return "2.x"
    return None


def git_config_get(target, section, key):
    cfg = os.path.join(target, ".git", "config")
    if not os.path.isfile(cfg):
        return None
    current = None
    for line in read_text(cfg).split("\n"):
        m = re.match(r"^\s*\[(.+?)\]\s*$", line)
        if m:
            current = m.group(1).strip().lower()
            continue
        if current == section.lower():
            m = re.match(r"^\s*" + re.escape(key) + r"\s*=\s*(.+?)\s*$", line, re.I)
            if m:
                return m.group(1)
    return None


def detect_forge(target):
    url = git_config_get(target, 'remote "origin"', "url")
    if url is None:
        return "unknown"
    u = url.lower()
    if "github.com" in u:
        return "github"
    if "gitlab" in u:
        return "gitlab"
    if "dev.azure.com" in u or "visualstudio.com" in u:
        return "azdo"
    return "unknown"


def row_applies(row_forge, forge):
    if row_forge == "all" or row_forge == forge:
        return True
    return forge == "unknown" and row_forge in ("github", "gitlab")


def safe_target_path(target_root, rel):
    rel = rel.rstrip("/")
    root = os.path.realpath(target_root)
    p = os.path.realpath(os.path.join(root, rel))
    if p != root and not p.startswith(root + os.sep):
        die("manifest path escapes the target: " + rel)
    return p


def is_executable(path):
    return os.path.isfile(path) and (os.stat(path).st_mode & 0o111) != 0


def walk_files(root):
    """Sorted relative file paths under root, excluding caches."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)
        for f in sorted(filenames):
            if EXCLUDED_FILE_RE.search(f):
                continue
            out.append(os.path.relpath(os.path.join(dirpath, f), root))
    return sorted(out)


def entry_lines(template_text):
    """Non-comment, non-blank lines of a sentinel template (the managed entries)."""
    return [l for l in template_text.split("\n") if l.strip() and not l.strip().startswith("#")]


def comment_head(template_text):
    """The leading comment block of a sentinel template (sentinel line + comments)."""
    head = []
    for l in template_text.split("\n"):
        if l.strip().startswith("#"):
            head.append(l)
        else:
            break
    return head


def plan_sentinel(row, tgt_path, src_path):
    """Returns (state, missing_entries). state: 'copy' | 'ok' | 'merge'."""
    template = read_text(src_path)
    if not os.path.isfile(tgt_path):
        return "copy", []
    try:
        text = read_text(tgt_path)
    except UnicodeDecodeError:
        die("target " + row["target"] + " is not valid UTF-8 — merge the managed block by hand")
    existing = {l.strip() for l in text.split("\n")}
    existing_norm = {" ".join(l.split()) for l in existing}
    missing = [e for e in entry_lines(template)
               if e.strip() not in existing and " ".join(e.split()) not in existing_norm]
    return ("ok", []) if not missing else ("merge", missing)


def apply_sentinel(tgt_path, src_path, missing):
    template = read_text(src_path)
    if not os.path.isfile(tgt_path):
        shutil.copy2(src_path, tgt_path)
        return
    text = read_text(tgt_path)
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    sentinel = template.split("\n")[0].strip()
    idx = next((i for i, l in enumerate(lines) if l.strip() == sentinel), None)
    if idx is None:
        lines.append("")
        lines.extend(comment_head(template))
        lines.extend(missing)
    else:
        insert_at = idx + 1
        while insert_at < len(lines) and lines[insert_at].strip().startswith("#"):
            insert_at += 1
        lines[insert_at:insert_at] = missing
    with open(tgt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# The one sanctioned deviation from a verbatim root shim (v4.38.0): a short
# contributor/consumer routing fork for repos that are also consumable products
# (field report: mercury-composable). Structure-checked, never content-trusted —
# the contributor line must carry the canonical read-imperative, the consumer
# route must be repo-local, and the whole file stays a bounded routing stub.
# Anything else is ordinary drift (recopy + the PRE-APPLY hard stop).
FORK_LEAD_RE = re.compile(
    r"(\*\*[^*\n]{1,80}\*\* )?Read \[memory/PROTOCOL\.md\]\(memory/PROTOCOL\.md\) "
    r"and follow it\.")
FORK_LINK_RE = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")


def is_sanctioned_fork(raw):
    # Bounds sized to the live field artifact (mercury-composable's ratified
    # three-paragraph fork: 11 non-empty lines, 945 bytes) with headroom — a
    # routing stub with a disambiguation paragraph fits; an instruction file
    # does not.
    if len(raw) > 2048:
        return False
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2 or len(lines) > 16:
        return False
    if not FORK_LEAD_RE.fullmatch(lines[0]):
        return False
    for line in lines[1:]:
        for m in FORK_LINK_RE.finditer(line):
            dest = m.group(1)
            if dest == "memory/PROTOCOL.md":
                continue
            if ":" in dest or dest.startswith("/") or ".." in dest:
                continue
            return True
    return False


def build_plan(tool_root, target, manifest, forge, installed, current_version):
    """Returns (mechanical, agent, semantic, notes) action lists."""
    mechanical, agent, notes = [], [], []
    fresh = installed is None
    for row in manifest["rows"]:
        if not row_applies(row["forge"], forge):
            continue
        src = os.path.join(tool_root, row["source"])
        tgt = safe_target_path(target, row["target"])
        policy = row["policy"]

        # a target path of the wrong kind would corrupt on copy (a dir named like a
        # file makes copy2 write INTO it) — refuse with a sane error instead
        if row["target"].endswith("/") or policy == "verbatim-dir":
            if os.path.isfile(tgt):
                die("target path is a file, expected a directory: " + row["target"])
        elif os.path.isdir(tgt):
            die("target path is a directory, expected a file: " + row["target"])

        if policy == "verbatim":
            if not os.path.isfile(src):
                die("manifest source missing in the tool checkout: " + row["source"])
            if not os.path.isfile(tgt):
                mechanical.append(("copy", row, [], "missing"))
            elif read_bytes(src) != read_bytes(tgt):
                if "fork-ok" in row["attrs"] and is_sanctioned_fork(read_bytes(tgt)):
                    notes.append(("ok", row["target"],
                                  "sanctioned consumer fork — structure verified"))
                else:
                    mechanical.append(("recopy", row, [], "drifted from the tool copy"))
            elif "exec" in row["attrs"] and not is_executable(tgt):
                mechanical.append(("chmod", row, [], "content ok, not executable"))
            else:
                notes.append(("ok", row["target"], ""))

        elif policy == "verbatim-dir":
            if not os.path.isdir(src):
                die("manifest source dir missing in the tool checkout: " + row["source"])
            src_files = walk_files(src)
            pending = []
            for rel in src_files:
                sf, tf = os.path.join(src, rel), os.path.join(tgt, rel)
                if not os.path.isfile(tf) or read_bytes(sf) != read_bytes(tf):
                    pending.append(rel)
            if os.path.isdir(tgt):
                extras = [rel for rel in walk_files(tgt) if rel not in set(src_files)]
                for rel in extras:
                    notes.append(("extra", row["target"] + rel, "not in the tool copy — left alone"))
            if not pending:
                notes.append(("ok", row["target"], str(len(src_files)) + " file(s)"))
            elif len(pending) == len(src_files) and not os.path.isdir(tgt):
                mechanical.append(("copy", row, pending, "missing — " + str(len(src_files)) + " file(s)"))
            else:
                mechanical.append(("recopy", row, pending,
                                   str(len(pending)) + " of " + str(len(src_files)) + " file(s) stale"))

        elif policy == "seed-copy":
            if not os.path.isfile(src):
                die("manifest source missing in the tool checkout: " + row["source"])
            if not os.path.isfile(tgt):
                mechanical.append(("copy", row, [], "missing"))
            elif read_bytes(src) != read_bytes(tgt):
                notes.append(("keep", row["target"], "present, differs — seed-copy never overwrites"))
                if "wire" in row["attrs"] and ".gitlab/agent-memory-ci.yml" not in read_text(tgt):
                    agent.append(("wire", row["target"],
                                  "pre-existing root CI without the include — wire it per ENABLE.md Step 6 "
                                  "(add-only include + stage check; never touch workflow:rules)"))
            else:
                notes.append(("ok", row["target"], ""))

        elif policy == "sentinel-merge":
            state, missing = plan_sentinel(row, tgt, src)
            if state == "copy":
                mechanical.append(("copy", row, [], "missing"))
            elif state == "merge":
                mechanical.append(("merge", row, missing, str(len(missing)) + " entries missing"))
                if "renorm" in row["attrs"]:
                    agent.append(("renorm", "git add --renormalize .",
                                  "after the .gitattributes merge; on a CRLF repo check the staged "
                                  "diff stays within agent-memory files"))
            else:
                notes.append(("ok", row["target"], ""))

        elif policy == "seed-generate":
            if row["target"].endswith("/"):
                entries = [e for e in os.listdir(tgt)
                           if e not in EXCLUDED_DIRS and not EXCLUDED_FILE_RE.search(e)] \
                    if os.path.isdir(tgt) else []
                present = len(entries) > 0
            else:
                present = os.path.isfile(tgt)
            if present:
                notes.append(("ok", row["target"], "present — never touched"))
            else:
                step = row["attrs"].replace("step:", "ENABLE.md Step ")
                agent.append(("generate", row["target"], step))

        elif policy == "stamp":
            if installed == current_version:
                notes.append(("ok", row["target"], "v" + current_version))
            else:
                src_note = "(fresh)" if fresh else installed
                agent.append(("stamp", row["target"],
                              src_note + " -> " + current_version +
                              " — the agent's closing step, after the semantic steps"))

    hooks = git_config_get(target, "core", "hookspath")
    gitpath = os.path.join(target, ".git")
    if os.path.isfile(gitpath):
        agent.append(("activate", "verify hooks + forge by hand",
                      "target .git is a worktree/submodule pointer file — confirm "
                      "core.hooksPath (.githooks) and the forge in the main repository"))
    elif not os.path.isdir(gitpath):
        agent.append(("activate", "git config core.hooksPath .githooks",
                      "target has no .git directory — init git first, then activate"))
    elif hooks is not None and hooks.rstrip("/") == ".githooks":
        pass
    elif hooks is None:
        agent.append(("activate", "git config core.hooksPath .githooks", "currently unset"))
    else:
        agent.append(("activate", "git config core.hooksPath .githooks",
                      "currently: " + hooks + " — a different hooks path is configured; "
                      "arbitrate before switching (chain it or keep theirs)"))

    notes.append(("run", "sync skill adapters",
                  "bash agent-skills/sync-adapters/scripts/sync-adapters.sh — idempotent, "
                  "gitignored-only; run after any enable or upgrade"))
    if forge == "unknown":
        notes.append(("forge", "hosting forge undetermined",
                      "GitHub + GitLab sets installed (additive-safe); Azure DevOps needs "
                      "positive detection — pass --forge to override"))
    if forge == "azdo":
        notes.append(("forge", "Azure DevOps CI floor",
                      "inert until the one-time az pipelines create binding — report the command, "
                      "run only at the user's direction, after push (ENABLE.md Step 6)"))

    semantic = []
    if not fresh:
        iv = parse_semver(installed)
        for s in manifest["semantic"]:
            if iv < parse_semver(s["below"]):
                semantic.append(s)
    return mechanical, agent, semantic, notes


PRE_APPLY_TARGETS = {
    "4.36.0": {
        ".githooks/pre-commit",
        ".githooks/post-commit",
        ".githooks/pre-commit.d/50-agent-memory-secret-guard",
        ".githooks/post-commit.d/50-agent-memory-ritual-capture",
    },
    "4.37.0": {"memory/PROTOCOL.md", "AGENTS.md"},
}


def pre_apply_state(installed, semantic, mechanical, notes):
    """Return (steps, hard blockers, explicit-confirmation reasons).

    The activation boundary is state-gated, not merely version-gated: a current
    stamp cannot authorize replacement of live root instructions, and fresh
    custom protocols still require provenance confirmation. Unknown future
    PRE-APPLY steps fail closed until they gain a completion rule here.
    """
    steps = [s for s in semantic if s["step"].startswith("PRE-APPLY:")]
    pending_by_target = {item[1]["target"]: item[0] for item in mechanical}
    hard = set()
    confirmation = set()
    protocol_custom = any(
        note[0] == "keep" and note[1] == "memory/PROTOCOL.md"
        for note in notes)

    # Existing root instructions are never mechanically replaced. A missing root
    # may be installed only when it cannot activate an unclassified custom protocol.
    agents_action = pending_by_target.get("AGENTS.md")
    if agents_action == "recopy":
        hard.add("AGENTS.md")
    elif agents_action == "copy" and protocol_custom:
        hard.update({"AGENTS.md", "memory/PROTOCOL.md"})

    # Hook drift can contain local policy/security behavior. The dry-run exposes
    # it; the explicit handshake attests that behavior was preserved or approved.
    for target in PRE_APPLY_TARGETS["4.36.0"]:
        if pending_by_target.get(target) == "recopy":
            confirmation.add(target)

    for step in steps:
        targets = PRE_APPLY_TARGETS.get(step["below"])
        if targets is None:
            hard.add("<unknown PRE-APPLY boundary for " + step["below"] + ">")
        elif step["below"] == "4.36.0":
            # Hook drift is confirmable after inspection/extraction: the explicit
            # handshake authorizes the dispatcher re-copy. The protocol boundary
            # below is different—it must converge before any mechanical apply.
            pass
        else:
            hard.update(targets & set(pending_by_target))

    if installed is None and protocol_custom:
        confirmation.add("memory/PROTOCOL.md")
    return steps, hard, confirmation


def print_report(mechanical, agent, semantic, notes, mode):
    def line(verb, path, detail):
        out = "  " + verb.ljust(9) + path
        if detail:
            out += "  (" + detail + ")"
        print(out)

    print("")
    print("[mechanical]")
    if mechanical:
        for verb, row, _files, detail in mechanical:
            line(verb, row["target"], detail)
    else:
        print("  (nothing to do)")
    print("")
    print("[agent work]")
    if agent:
        for verb, path, detail in agent:
            line(verb, path, detail)
    else:
        print("  (nothing to do)")
    print("")
    print("[semantic steps]")
    if semantic:
        for s in semantic:
            line("< " + s["below"], "rung " + s["rung"], "")
            print("           " + s["step"])
    else:
        print("  (none apply)")
    print("")
    print("[notes]")
    for verb, path, detail in notes:
        line(verb, path, detail)
    print("")


def apply_mechanical(tool_root, target, mechanical):
    applied = 0
    for verb, row, files, _detail in mechanical:
        src = os.path.join(tool_root, row["source"])
        tgt = safe_target_path(target, row["target"])
        if row["policy"] == "verbatim-dir":
            for rel in files:
                dst = os.path.join(tgt, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(os.path.join(src, rel), dst)
                applied += 1
        elif row["policy"] == "sentinel-merge":
            os.makedirs(os.path.dirname(tgt), exist_ok=True) if os.path.dirname(tgt) else None
            apply_sentinel(tgt, src, files)
            applied += 1
        elif verb == "chmod":
            os.chmod(tgt, 0o755)
            applied += 1
        else:
            os.makedirs(os.path.dirname(tgt), exist_ok=True)
            shutil.copy2(src, tgt)
            if "exec" in row["attrs"]:
                os.chmod(tgt, 0o755)
            applied += 1
    return applied


def check_manifest(tool_root, manifest):
    problems = []
    covered_files, covered_dirs = set(), []
    for row in manifest["rows"]:
        src = os.path.join(tool_root, row["source"])
        if row["policy"] == "verbatim-dir":
            if not os.path.isdir(src):
                problems.append("source dir missing: " + row["source"])
            else:
                covered_dirs.append(row["source"].rstrip("/"))
        else:
            if not os.path.isfile(src):
                problems.append("source missing: " + row["source"])
            else:
                covered_files.add(os.path.normpath(row["source"]))

    def covered(rel):
        n = os.path.normpath(rel)
        if n in covered_files:
            return True
        return any(n == d or n.startswith(d + os.sep) for d in covered_dirs)

    for root in ("templates", ".githooks"):
        base = os.path.join(tool_root, root)
        for rel in walk_files(base):
            full = os.path.join(root, rel)
            if not covered(full):
                problems.append("uncovered file (no manifest row): " + full)

    skills_root = os.path.join(tool_root, "agent-skills")
    for name in sorted(os.listdir(skills_root)):
        d = os.path.join(skills_root, name)
        if not os.path.isdir(d):
            continue
        rel = "agent-skills/" + name + "/"
        if rel.rstrip("/") not in [c for c in covered_dirs] and rel not in manifest["tool_only"]:
            problems.append("skill dir neither installed nor listed tool-only: " + rel)

    current = read_text(os.path.join(tool_root, "VERSION")).strip()
    for s in manifest["semantic"]:
        if parse_semver(s["below"]) > parse_semver(current):
            problems.append("semantic step gated above the current version: " + s["below"])

    if problems:
        for p in problems:
            print("  gap: " + p)
        print("")
        print("result: manifest check FAILED (" + str(len(problems)) + " gap(s))")
        sys.exit(1)
    print("  sources: " + str(len(manifest["rows"])) + " rows verified")
    print("  coverage: templates/, .githooks/, agent-skills/ fully covered")
    print("  semantic steps: " + str(len(manifest["semantic"])) + " rows, all gated <= v" + current)
    print("")
    print("result: manifest OK")
    sys.exit(0)


def main(argv):
    target, forge_override = None, None
    do_apply, do_check, pre_apply_complete = False, False, False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--target":
            i += 1
            target = argv[i] if i < len(argv) else die("--target needs a path")
        elif a == "--forge":
            i += 1
            forge_override = argv[i] if i < len(argv) else die("--forge needs a value")
            if forge_override not in ("github", "gitlab", "azdo", "unknown"):
                die("--forge must be github|gitlab|azdo|unknown")
        elif a == "--apply":
            do_apply = True
        elif a == "--pre-apply-complete":
            pre_apply_complete = True
        elif a == "--check-manifest":
            do_check = True
        else:
            die("unknown argument: " + a)
        i += 1

    tool_root = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    current_version = read_text(os.path.join(tool_root, "VERSION")).strip()
    manifest = parse_manifest(tool_root)

    print("agent-memory reconcile — tool v" + current_version)
    if do_check:
        print("mode:      check-manifest")
        print("")
        check_manifest(tool_root, manifest)
        return

    if not target:
        die("--target <path> is required (or --check-manifest)")
    target = os.path.realpath(os.path.expanduser(target))
    if not os.path.isdir(target):
        die("target does not exist: " + target)
    if target == os.path.realpath(os.path.expanduser("~")):
        die("the target is the user's home directory — never a repo target (target-repo scope only)")
    if target == tool_root:
        die("the target is the agent-memory tool itself — nothing to enable")

    installed = detect_installed(target)
    if installed is not None and installed != "2.x" and \
            parse_semver(installed) > parse_semver(current_version):
        die("target is on v" + installed + " — newer than this tool checkout (v" +
            current_version + "); update the tool instead (ENABLE.md Mode B: stop)")
    forge = forge_override or detect_forge(target)
    forge_how = "--forge" if forge_override else "detected"

    print("target:    " + target)
    if installed is None:
        print("installed: (fresh — no memory layer)")
    elif installed == "2.x":
        print("installed: 2.x baseline (memory present, no version stamp)")
    else:
        print("installed: " + installed)
    print("forge:     " + forge + " (" + forge_how + ")")
    print("mode:      " + ("apply" if do_apply else "dry-run"))

    mechanical, agent, semantic, notes = build_plan(
        tool_root, target, manifest, forge, installed, current_version)
    print_report(mechanical, agent, semantic, notes, "apply" if do_apply else "dry-run")

    pending = len(mechanical) + len(agent) + len(semantic)
    if do_apply:
        pre_steps, hard, confirmation = pre_apply_state(
            installed, semantic, mechanical, notes)
        if hard:
            blocked = sorted(hard)
            print("result: blocked — PRE-APPLY boundary unresolved for: " +
                  ", ".join(blocked))
            print("no target files were written; complete the listed preservation, "
                  "provenance, merge, and hash checks, then rerun the dry-run")
            sys.exit(1)
        if (pre_steps or confirmation) and not pre_apply_complete:
            print("result: blocked — no hard PRE-APPLY boundary writes remain, but "
                  "explicit confirmation is required")
            print("no target files were written; after completing the listed checks, "
                  "rerun with --apply --pre-apply-complete")
            sys.exit(1)
        applied = apply_mechanical(tool_root, target, mechanical)
        remaining = len(agent) + len(semantic)
        print("result: applied " + str(applied) + " mechanical change(s); " +
              str(remaining) + " agent item(s) remain (listed above)")
        sys.exit(0)
    if pending == 0:
        print("result: converged — nothing to do")
        sys.exit(0)
    # The dry-run is the consent artifact: its closing hint must name the next
    # real move. Sending the agent to --apply when --apply would refuse with zero
    # writes is the one way this line can mislead.
    pre_steps, hard, confirmation = pre_apply_state(
        installed, semantic, mechanical, notes)
    if hard:
        hint = ("--apply refuses until the PRE-APPLY boundary converges for: " +
                ", ".join(sorted(hard)))
    elif pre_steps or confirmation:
        hint = ("re-run with --apply --pre-apply-complete once the listed "
                "PRE-APPLY checks are done")
    elif mechanical:
        hint = "re-run with --apply for the mechanical part"
    else:
        hint = "all pending items are agent work"
    print("result: " + str(len(mechanical)) + " mechanical + " +
          str(len(agent) + len(semantic)) + " agent item(s) pending "
          "(dry-run — " + hint + ")")
    sys.exit(3)


if __name__ == "__main__":
    main(sys.argv[1:])
