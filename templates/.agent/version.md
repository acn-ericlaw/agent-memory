# agent-memory install manifest

> Records which version of the agent-memory tool this repo is on, so `ENABLE.md`
> Mode B can detect drift and upgrade in place (see the tool's `UPGRADE.md`).
> `version` gates the upgrade ladder — don't hand-edit it unless you mean to.

- **version:**       {{AGENT_MEMORY_VERSION}}
- **enabled_with:**  {{AGENT_MEMORY_VERSION}}
- **last_upgraded:** {{TODAY}}
- **mode:**          {{ENABLE_MODE}}
