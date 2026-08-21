# Memory Protocol Pointer — Post-Rebase Walkthrough

**Observed:** 2026-08-21 UTC  
**Release path:** 4.36.0 → 4.37.0  
**Fixture:** `/private/tmp/am437-walk.feCcL9/target`

The maintainer ran `/bin/bash /private/tmp/am437.sh` from the tool root. The script
created a real target Git repository stamped at 4.36.0, committed the old target
`AGENTS.md` with a repository-specific directive, and customized the pre-commit
dispatcher with local behavior.

Observed results:

- `git show HEAD:AGENTS.md` produced bytes identical to the live pre-collapse root.
- Unconfirmed `--apply` exited non-zero; a content-and-mode inventory taken before and
  after was byte-identical, and the report said no target files were written.
- The local root directive was merged once into `memory/PROTOCOL.md` before the exact
  one-line shim was installed.
- The local hook behavior was extracted to an executable, differently named fragment;
  confirmed apply installed the managed dispatchers and preserved that fragment.
- `--apply --pre-apply-complete` succeeded only after the protected boundary converged.
- After stamping 4.37.0, a repeated apply reported `0 mechanical change(s)`.

Result: **PASS** — committed-byte recovery, zero-write refusal, protocol-before-shim
ordering, customized-hook preservation, confirmed apply, and mechanical idempotence all
matched AC-MP-07 through AC-MP-09.
