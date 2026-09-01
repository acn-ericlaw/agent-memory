- [ ] **(backlog) Bitbucket forge support — trigger-gated; mechanics pre-verified (2026-07-27).** From a
  maintainer question during the v4.31.0 GitLab release ("investigate viability to include Bitbucket").
  Verified against Atlassian docs (July 2026) so a future field report can act immediately: **(1) the
  clean win** — Bitbucket CLOUD supports a committed `.bitbucket/pull_request_template.md` (KB Apr
  2026; read from the PR's SOURCE branch; overrides the settings field) — the What/Why template is
  seedable file-based. **(2) The CI floor cannot keep its promise there** — committing
  `bitbucket-pipelines.yml` runs nothing until a repo ADMIN enables Pipelines (`repository:admin`, a
  forge setting the agent must never touch); free tier = 50 build-min/month; and there is NO additive
  include seam (the `import` mechanism is Premium **and** whole-pipeline replacement — adding to an
  existing file means inserting a step into their sequential list, against add-only). Advisory
  semantics do exist (`on-fail: strategy: ignore`); PR pipelines carry base-SHA vars
  (`BITBUCKET_PR_DESTINATION_COMMIT`); clone needs `depth: full`. **(3) Cloud-only** — Data Center has
  NO native Pipelines and NO committed template file (settings-UI only): enterprise Bitbucket gets
  nothing. **(4) Attribution** — squash message not templatable on Cloud, trailers mangle into bullet
  lists, UI ignores Co-authored-by (BSERV-10529 closed won't-fix) — the PR-description footer is the
  only durable record. **Decision (maintainer, 2026-07-27): defer — don't build speculatively.** The
  pre-scoped viable shape when a Bitbucket team reports the failure class:
  `.bitbucket/pull_request_template.md` (clean) + an optional fresh-file-only pipelines floor carrying
  the admin-toggle honest limit + never editing an existing pipelines file (report a recommendation
  instead). → serves: vision-agent-memory
  <!-- id: ot-bitbucket-forge-backlog | created: 2026-07-27 | last_used: 2026-07-27 | uses: 2 | tier: working | origin: 2026-07-27-203400 -->
