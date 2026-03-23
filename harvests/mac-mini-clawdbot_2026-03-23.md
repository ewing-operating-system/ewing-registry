# Harvest: ClawdBots-Mac-mini-8
**Date:** 2026-03-23
**Hostname:** ClawdBots-Mac-mini-8.local
**OS:** macOS 26.3.1 (Darwin)
**User:** clawdbot
**Disk:** 228Gi total, 12Gi used, 155Gi free (7% used)

---

## Installed Tools & Versions
- Node.js: v25.8.1
- npm: 11.11.0
- Python: 3.9.6
- Git: 2.50.1

## Running Services
| Service | Port | Status |
|---|---|---|
| OpenClaw gateway | 18789 | Running |
| OpenClaw (additional) | 18791, 18792 | Running |
| Hovering Cloud | 51764 | Not running (was running earlier, likely restarted) |

## Git Repositories

### 1. hovering-cloud
- **Path:** /Users/clawdbot/Downloads/hovering-cloud (+ mirror at ~/.hovering-cloud/app)
- **Remote:** https://github.com/clawdking1-GH/hovering-cloud.git
- **Latest commits:**
  - 4d5bef1 Simplify click actions: single=preview, double=copy, right-click=paste text
  - 1a488a4 Remove recipient/user selection feature
  - c4c0ea9 Add categorized items, type-aware clicks, recipient tagging

### 2. phoenix-tam-engine
- **Path:** /Users/clawdbot/Projects/phoenix-tam-engine
- **Remote:** https://github.com/clawdking1-GH/phoenix-tam-engine.git
- **Latest commits:**
  - 67e6fe4 Auto-agree on single Gemini results
  - 7e41643 Fix TAM engine: service role key, city parser
  - 1542cfa Fix: parse_search_result before enrich_with_details

### 3. clawdbot-pipeline (OpenClaw)
- **Path:** /Users/clawdbot/.openclaw
- **Remote:** https://github.com/clawdking1-GH/clawdbot-pipeline.git
- **Latest commits:**
  - ac57dec All 3 companies in Supabase + LLM retrieval prompt
  - 3cdb82f LOVABLE_ENRICHED_FINAL.json
  - dced0ff Market multiples database

### 4. ewing-registry
- **Path:** /Users/clawdbot/ewing-registry
- **Remote:** https://github.com/ewing-operating-system/ewing-registry.git
- **Latest:** 828aba3 Debrief: phoenix-tam-engine-build — 2026-03-23

### 5. boomerang
- **Path:** /Users/clawdbot/Downloads/Claude Code on this computer/boomerang
- **No remote configured**

## Environment Files (KEY NAMES ONLY)
### .openclaw/.env
- SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_DB_PASSWORD, GOOGLE_API_KEY

### phoenix-tam-engine/.env.example
- ANTHROPIC_API_KEY, EXA_API_KEY, CLAY_API_KEY, GOOGLE_MAPS_API_KEY

### boomerang/.env
- SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_CX, ANTHROPIC_API_KEY, PORT

## Skills Installed (24 total)
clawdbot-creator, clawdbot-self-repair.md, cold-call-workflow, data-architect, debrief, disk-cleanup, ewing-connectors, file-share, finance-agent, harvester, keys-and-credentials, mission-control, output-skill, password-migration, prompt-refiner, rate-oracle, recording-collector, salesfinity-loader, skill-creator, skill-loader, skill-sync, storyteller, system-auditor, tech-translator

## Memory Files (Project: Desktop Claude Code)
- MEMORY.md (index)
- user_ewing_profile.md
- project_infrastructure_map.md
- project_pipeline_status.md
- reference_master_registry.md
- project_architecture_plan.md
- feedback_migration_gaps.md

## Scheduled Tasks
- phoenix-tam-engine (1 task configured)

## LaunchD Agents
- ai.openclaw.gateway.plist (OpenClaw auto-start)
- homebrew.mxcl.ollama.plist (Ollama LLM)
- Google Updater/Keystone agents

## Package.json Projects
1. /Users/clawdbot/Desktop/hovering-cloud/package.json
2. /Users/clawdbot/.hovering-cloud/app/package.json
3. /Users/clawdbot/Downloads/hovering-cloud/package.json
4. /Users/clawdbot/Downloads/Claude Code on this computer/boomerang/package.json

## MCP Configuration
- No ~/.claude/mcp.json found (MCP tools configured via Cowork/Desktop, not local CLI)
- Connected MCPs via Cowork: Gmail, Google Calendar, Google Drive, Slack, Fireflies, Gamma, Chrome, Claude Preview, Scheduled Tasks, MCP Registry
