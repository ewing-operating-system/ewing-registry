# Ewing Registry

Master registry of all machines, credentials, projects, skills, and harvests across Ewing's infrastructure.

**Created:** 2026-03-23
**Last updated:** 2026-03-23
**Harvests collected:** 12 (across 3 persistent Macs + 4 ephemeral Cowork VMs)

## Structure

```
ewing-registry/
├── harvests/              # Raw harvest files (one per machine per run)
├── registry/              # Deduplicated reference tables
│   ├── README.md          # Master registry (all data combined)
│   ├── emails.md          # All email identities
│   ├── credentials.md     # API keys, tokens, secrets (names only)
│   ├── supabase-instances.md
│   ├── github-repos.md
│   ├── skills.md
│   ├── scheduled-tasks.md
│   ├── mcp-tools.md
│   ├── projects.md
│   └── google-drive.md
├── status/                # Living status docs
│   ├── pipeline-status.md
│   └── risk-register.md
└── README.md
```

## Machines
| Machine | Type | Primary Value |
|---|---|---|
| MacBook-27.local | Primary Mac | 8 skills, 10 tasks, 8 repos, 20 memory files |
| MacBook-GREEN | Secondary Mac | coldcall-universe dev, 96% disk |
| ClawdBots-Mac-mini-8 | Server Mac | Hovering Cloud, Phoenix TAM, OpenClaw |
| Cowork VMs (x4) | Ephemeral | 22 session skills, MCP tools |

## Quick Reference
- **Supabase instances:** 4 live, 1 dead
- **GitHub repos:** 10 unique (across 2 accounts)
- **Skills:** 30+ unique
- **Scheduled tasks:** 10 production (MB-27) + 7 others
- **MCP tools:** 16+ unique
- **Google Drive accounts:** 4 mounted
