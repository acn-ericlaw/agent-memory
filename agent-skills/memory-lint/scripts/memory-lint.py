#!/usr/bin/env python3
"""memory-lint — deterministic integrity checks for an agent-memory repo.

Removes the LLM from the decay arithmetic. It counts session files and verifies
archival / tiers / supersession against *observable evidence* — the agent judges
meaning, this script does the counting. Pure Python 3 stdlib; no dependencies.

Usage:
    python3 memory-lint.py [--root PATH] [--strict]

Exit: 0 = clean (no errors), 1 = integrity error(s) (or warnings under --strict),
2 = could not locate the memory/ layer.
"""
import glob
import os
import re
import sys

ID_RE = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+")
FOOTER_RE = re.compile(r"<!--\s*id:\s*([a-z0-9-]+)\s*\|(.*?)-->", re.S)


def find_root(start):
    for cand in (start, os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
        if not cand:
            continue
        d = os.path.abspath(cand)
        while True:
            if os.path.isfile(os.path.join(d, "memory", "continuity.md")):
                return d
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
    return None


def parse_footers(text):
    out = {}
    for m in FOOTER_RE.finditer(text):
        fields = {}
        for part in m.group(2).split("|"):
            if ":" in part:
                k, _, v = part.partition(":")
                fields[k.strip()] = v.strip()
        out[m.group(1)] = fields
    return out


def pinned_open_threads(text):
    """ids whose nearest preceding list bullet is an unchecked '- [ ]' (never decay)."""
    pinned, state = set(), None
    for ln in text.split("\n"):
        st = ln.lstrip()
        if st.startswith("- [ ]"):
            state = "open"
        elif st.startswith(("- [x]", "- [X]")):
            state = "done"
        elif st.startswith(("- ", "* ")):
            state = None
        m = re.search(r"<!--\s*id:\s*([a-z0-9-]+)", ln)
        if m and state == "open":
            pinned.add(m.group(1))
    return pinned


def memref_ids(text):
    idx = text.find("## Memory References")
    if idx == -1:
        return set()
    block = text[idx:]
    nxt = block.find("\n## ", 4)
    if nxt != -1:
        block = block[:nxt]
    return set(ID_RE.findall(block))


def load_windows(root):
    w = {"working_window": 3, "active_window": 8, "archive_window": 20}
    p = os.path.join(root, "memory", "decay-policy.md")
    if os.path.isfile(p):
        t = open(p, encoding="utf-8").read()
        for k in w:
            m = re.search(rf"{k}\s*:\s*(\d+)", t)
            if m:
                w[k] = int(m.group(1))
    return w


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    root_arg = None
    for i, a in enumerate(args):
        if a == "--root" and i + 1 < len(args):
            root_arg = args[i + 1]

    root = find_root(root_arg or os.getcwd())
    if not root:
        print("memory-lint: could not find memory/continuity.md", file=sys.stderr)
        return 2

    mem = os.path.join(root, "memory")
    cont_text = open(os.path.join(mem, "continuity.md"), encoding="utf-8").read()
    cont = parse_footers(cont_text)
    pinned = pinned_open_threads(cont_text)

    archive_text = ""
    for f in glob.glob(os.path.join(mem, "archive", "*.md")):
        if os.path.basename(f).upper().startswith("INDEX"):
            continue
        archive_text += open(f, encoding="utf-8").read() + "\n"
    arch = parse_footers(archive_text)

    sessions = sorted(glob.glob(os.path.join(mem, "sessions", "*.md")))
    refs = [memref_ids(open(s, encoding="utf-8").read()) for s in sessions]

    w = load_windows(root)
    aw, acw = w["archive_window"], w["active_window"]

    def sslu(fid):
        last = -1
        for i, ids in enumerate(refs):
            if fid in ids:
                last = i
        return None if last == -1 else len(refs) - 1 - last

    errors, warns = [], []

    # (1) a fact must live in exactly one place
    for fid in sorted(set(cont) & set(arch)):
        errors.append(f"[both] {fid} is in BOTH continuity.md and the archive")

    # (2) the decay miscount guard: archived-as-faded but still referenced in-window
    for fid, fields in arch.items():
        if "superseded-by" in fields or fields.get("tier") == "superseded":
            continue  # superseded archives on truth-state, not recency
        s = sslu(fid)
        if s is not None and s <= aw:
            errors.append(
                f"[over-archived] {fid} archived as faded but last referenced {s} "
                f"session(s) ago (<= archive_window {aw}) — reactivate it"
            )

    # (3) advisory: continuity fact overdue for archival
    #     (core, superseded, and pinned unchecked open threads never decay)
    for fid, fields in cont.items():
        if fields.get("tier") in ("core", "superseded") or fid in pinned:
            continue
        s = sslu(fid)
        if s is not None and s > aw:
            warns.append(f"[overdue] {fid} sslu {s} > archive_window {aw} — review may archive it")

    # (4) supersession links resolve
    allf = {**cont, **arch}
    for fid, fields in allf.items():
        for key in ("superseded-by", "supersedes"):
            tgt = fields.get(key)
            if tgt and tgt not in allf:
                warns.append(f"[dangling] {fid} {key} {tgt}, which has no footer anywhere")

    print(
        f"memory-lint: {len(cont)} continuity facts, {len(arch)} archived, "
        f"{len(sessions)} sessions; windows active={acw} archive={aw}"
    )
    for line in warns:
        print("WARN  " + line)
    for line in errors:
        print("ERROR " + line)
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warns)} warning(s)")
        return 1
    if warns and strict:
        print(f"FAIL (strict): {len(warns)} warning(s)")
        return 1
    print(f"OK: 0 errors, {len(warns)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
