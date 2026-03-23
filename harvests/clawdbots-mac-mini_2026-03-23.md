# Harvest: ClawdBots-Mac-mini-8 — 2026-03-23

## Machine Info
| Field | Value |
|-------|-------|
| Hostname | ClawdBots-Mac-mini-8.local |
| OS | macOS 26.3.1 (Darwin 25.3.0) |
| User | clawdbot (ClawdBot) |
| Disk | 228Gi total, 12Gi used, 155Gi free (7%) |
| Platform | darwin arm64 |

## Installed Tools
| Tool | Version |
|------|---------|
| node | v25.8.1 |
| npm | 11.11.0 |
| python3 | 3.9.6 |
| pip3 | 21.2.4 |
| git | 2.50.1 (Apple Git-155) |
| gh | 2.88.1 |
| brew | 5.1.0 |
| supabase CLI | 2.75.0 |
| claude (Claude Code) | 2.1.81 |
| ollama | installed (qwen3:4b model loaded) |

## .claude Directory

### Skills (23 total)
| Skill | Status |
|-------|--------|
| clawdbot-creator | Active |
| cold-call-workflow | Active |
| data-architect | Active |
| debrief | Active |
| disk-cleanup | Active |
| ewing-connectors | Active |
| file-share | Active |
| finance-agent | Active |
| harvester | Active |
| keys-and-credentials | Active |
| mission-control | Active |
| output-skill | Active |
| password-migration | Active |
| prompt-refiner | Active |
| rate-oracle | Active |
| recording-collector | Active |
| salesfinity-loader | Active |
| skill-creator | Active |
| skill-loader | Active |
| skill-sync | Active |
| storyteller | Active |
| system-auditor | Active |
| tech-translator | Active |

### Memory Files (7)
- MEMORY.md (index)
- user_ewing_profile.md
- project_infrastructure_map.md
- project_pipeline_status.md
- reference_master_registry.md
- project_architecture_plan.md
- feedback_migration_gaps.md

### Scheduled Tasks (1)
- **phoenix-tam-engine** — Phoenix metro home services TAM scraper, discovers/verifies/catalogs businesses city by city

### Settings
- Permissions: Bash, Fetch allowed
- Extra marketplace: claude-plugins-official (from anthropics/claude-plugins-official GitHub)

### Plans
- synchronous-petting-creek.md

## Git Repos

### 1. phoenix-tam-engine
- **Remote:** https://github.com/clawdking1-GH/phoenix-tam-engine.git
- **Branch:** main
- **Last commit:** 67e6fe4 Auto-agree on single Gemini results with confidence>=0.6
- **Uncommitted changes:** 2 files (scraper/dedup.py, storage/supabase_client.py)
- **Unpushed commits:** 4
  - 67e6fe4 Auto-agree on single Gemini results with confidence>=0.6
  - 7e41643 Fix TAM engine: service role key, city parser, Gemini model, junk filter, token limit
  - 1542cfa Fix: parse_search_result before enrich_with_details in discover phase
  - 757207d Cross-table dedup: check M&A pipeline targets before inserting into tam_businesses

### 2. hovering-cloud (deployed)
- **Remote:** https://github.com/clawdking1-GH/hovering-cloud.git
- **Location:** /Users/clawdbot/.hovering-cloud/app
- **Branch:** main
- **Last commit:** 4d5bef1 Simplify click actions: single=preview, double=copy, right-click=paste
- **Clean:** yes

### 3. clawdbot-pipeline (OpenClaw)
- **Remote:** https://github.com/clawdking1-GH/clawdbot-pipeline.git
- **Location:** /Users/clawdbot/.openclaw
- **Branch:** main
- **Last commit:** ac57dec All 3 companies in Supabase + LLM retrieval prompt
- **Uncommitted changes:** 118 (mostly deleted session files)
- **Unpushed commits:** 6

### 4. ewing-registry
- **Remote:** https://github.com/ewing-operating-system/ewing-registry.git
- **Branch:** main
- **Last commit:** e62f196 Debrief: macbook-27 skill-sync session — 2026-03-23
- **Clean:** yes

### 5. hovering-cloud (Downloads copy)
- **Location:** /Users/clawdbot/Downloads/hovering-cloud
- **Clean duplicate of .hovering-cloud/app**

## .env Files (KEY NAMES ONLY)
### /Users/clawdbot/.openclaw/.env
- SUPABASE_URL
- SUPABASE_ANON_KEY
- SUPABASE_SERVICE_ROLE_KEY
- SUPABASE_DB_PASSWORD
- GOOGLE_API_KEY

### /Users/clawdbot/Downloads/Claude Code on this computer/boomerang/.env
- SUPABASE_URL
- SUPABASE_ANON_KEY
- SUPABASE_SERVICE_KEY
- GOOGLE_SEARCH_API_KEY
- GOOGLE_SEARCH_CX
- ANTHROPIC_API_KEY
- PORT

## Projects / Applications
| Project | Type | Location |
|---------|------|----------|
| phoenix-tam-engine | Python (requirements.txt) | ~/Projects/phoenix-tam-engine |
| hovering-cloud | Node/Electron (package.json) | ~/.hovering-cloud/app |
| boomerang | Node/Express (package.json) | ~/Downloads/Claude Code.../boomerang |

## Supabase
- **Project URL:** https://asavljgcnresdnadblse.supabase.co
- **Tables accessible via REST:** hint, message (RLS may be hiding others)
- **Note:** Service role JWT in vault returned "Invalid API key" — may need rotation or full JWT

## Connected MCP Tools
Available via Claude Code connectors:
- Fireflies.ai (meeting transcripts, search, channels)
- Gmail (search, read, draft, labels)
- Gamma (presentation generation)
- Google Calendar (events, scheduling, free time)
- Slack (channels, messages, search, canvas, users)
- Google Drive (search, fetch documents)
- Claude in Chrome (browser automation, screenshots, forms)
- Claude Preview (dev server, screenshots, inspect)
- MCP Registry (search, suggest connectors)
- Scheduled Tasks (create, list, update)

## LaunchAgents
- ai.openclaw.gateway.plist
- com.google.GoogleUpdater.wake.plist
- com.google.keystone.agent.plist (x2)
- homebrew.mxcl.ollama.plist

## Running Services
- No active Node/Python/Postgres processes at scan time
- Ollama daemon likely running (launchd agent present, model loaded)

## Disk Usage
| Directory | Size |
|-----------|------|
| ~/Projects | 1.1M |
| ~/Downloads | 1.3G |
| ~/.claude | 33M |
| ~/.openclaw | 28M |
| ~/ewing-registry | 1.8M |

## Credential References in Skills
Keys referenced (names only, values in keys-and-credentials vault):
- Anthropic API Key
- ClawdKing Gemini Key, Original Gemini Key, OpenClaw Google Key
- Custom Search Engine ID (cx)
- Supabase URL, Anon Key, Service Role Key, DB Password, Full JWTs
- Exa.ai API Key
- Clay API Key, Workspace ID, Webhook URL
- GitHub username (clawdking1-GH)

## Google Sheets / Service Account Status
- **No service account JSON file found on this machine**
- Google Cloud project exists (API keys present) but no Sheets-specific credentials
- This was identified as the blocker for the Google Sheets sync skill being planned this session
