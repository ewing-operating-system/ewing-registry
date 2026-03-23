# Harvest: ClawdBots-Mac-mini-8 — 2026-03-22T21:26:02Z (Full Raw)

## Machine Info
- Hostname: ClawdBots-Mac-mini-8.local
- User: clawdbot
- OS: macOS 26.3.1 (Build 25D771280a)

## Skills Found (9)
- clawdbot-creator — Master blueprint for spawning new ClawdBots with full environment, keys, tools, and setup procedures
- file-share — Send files to Hovering Cloud shared clipboard across all connected Macs
- harvester — One-time consolidation harvester, scans machine and appends to central Slack canvas
- keys-and-credentials — Permanent credential vault for all ClawdBots (single source of truth for API keys)
- mission-control — Command center for all ClawdBots, fleet status and resource allocation
- output-skill — Governs all communication with Ewing (literal, exact actions, no fluff)
- rate-oracle — Tracks API rate limits, costs, tiers, incident history, and recovery protocols
- skill-loader — Session bootstrapper, loads default skills (output-skill, prompt-refiner, skill-creator, tech-translator)
- tech-translator — Translates terminal output and developer jargon into plain English

## Memory Files
- feedback_auto_proceed.md: Do not pause between pipeline records or agent handoffs to ask "proceed?" — run jobs to completion autonomously
- reference_consolidation_canvas.md: Central Slack canvas F0ANYTBD0HW for harvester output
- MEMORY.md: Index with feedback (auto-proceed) and reference (consolidation canvas) entries

## Git Repositories (4)

### 1. phoenix-tam-engine (~/Projects/phoenix-tam-engine/)
- Remote: https://github.com/clawdking1-GH/phoenix-tam-engine.git
- Branch: main
- Last 10 commits: Auto-agree Gemini results, fix service role key/city parser/Gemini model, parse_search_result fix, cross-table dedup, owner profile system, Places API v1 + fuzzy dedup, dual-model columns, autonomous run script, initial build
- Uncommitted: modified dedup.py, supabase_client.py

### 2. hovering-cloud (~/.hovering-cloud/app/)
- Remote: https://github.com/clawdking1-GH/hovering-cloud.git
- Branch: main
- Commits: Simplified click actions, removed recipient selection, universal installer, auto-update, v1.0 shared clipboard
- Clean (no uncommitted changes)

### 3. openclaw / clawdbot-pipeline (~/.openclaw/)
- Remote: https://github.com/clawdking1-GH/clawdbot-pipeline.git
- Branch: main
- Last 10 commits: Report index links fix, 79 live company report pages, story cards (Dr. Simmons, Agape Air), 11 outreach packages total, morning brief 2026-03-22, story intelligence layer, mission-control skill, rate-oracle skill
- Uncommitted: modified cron/jobs.json, mission-control skill, workspace memory; deleted session locks; untracked session files and CSV export

### 4. hovering-cloud (Downloads copy) (~/Downloads/hovering-cloud/)
- Remote: same as above
- Clean duplicate of the hovering-cloud repo

## Credential Keys (by file — NO VALUES)
- ~/.openclaw/.env: SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_DB_PASSWORD, GOOGLE_API_KEY
- ~/Downloads/Claude Code on this computer/boomerang/.env: SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_CX, ANTHROPIC_API_KEY, PORT

### keys-and-credentials skill vault references:
- Anthropic API Key (Tier 1, checking Tier 2)
- 3 Google/Gemini API Keys + Custom Search Engine ID
- Supabase Project URL + Anon Key + Service Role Key + DB Password + full JWTs
- Exa.ai API Key
- Clay.com API Key + Workspace ID + Webhook URL (Legacy plan, 50K credits/$800/mo)
- Apollo.io (PLACEHOLDER)
- Instantly.ai (PLACEHOLDER)
- Salesfinity (PLACEHOLDER)
- Handwrytten (PLACEHOLDER)
- GitHub: clawdking1-GH (auth via keyring/gh)

## Projects and Applications
- ~/Projects/phoenix-tam-engine/ — Python. Phoenix metro home services TAM scraper + M&A pipeline. Discovers, verifies, and catalogs HVAC/plumbing/electrical businesses. Includes owner profile builder, QR code generator, Lovable prompt for personalized sales pages. Connected to Supabase (asavljgcnresdnadblse.supabase.co).
- ~/.openclaw/ — ClawdBot Pipeline (OpenClaw). Agent orchestration with Next (Sonnet manager) and Scout (Haiku researcher). Runs M&A target research, quality reviews, outreach generation. 79 live company report pages on GitHub Pages. 11 outreach packages completed.
- ~/.hovering-cloud/app/ — Hovering Cloud. Electron app for cross-desktop shared clipboard. Click-to-preview, smart thumbnails, auto-update from GitHub.
- ~/Downloads/Claude Code on this computer/ — Contains boomerang project (.env present), various Claude Code working files.
- ~/Desktop/ — Contains screenshots, all_pipeline_data.csv, next_chapter_full_research.csv, hovering-cloud folder.
- ~/Documents/boomerang-clawdbot-plan.md — Planning doc for boomerang ClawdBot.

## Running Services
- Hovering Cloud (Electron) — running on port via npm/electron, PID 3570+

## Databases
- SQLite installed via brew
- Supabase CLI installed via brew (remote DB at asavljgcnresdnadblse.supabase.co)
- No local Postgres/MySQL/Redis/Mongo running

## Installed Tools
- node v25.8.1, npm, python3 3.9.6, pip3, git, gh, brew, java
- No docker, cargo, rustc, go
- Brew packages (30): ada-url, brotli, c-ares, ca-certificates, gh, mlx, mlx-c, node, ollama, openssl@3, python@3.12, python@3.14, readline, simdjson, sqlite, supabase, 1password-cli, and more

## Settings and Configuration
- settings.json: Permissions allow Bash and Fetch. Extra marketplace: claude-plugins-official (GitHub).
- settings.local.json: Granular permissions for mkdir, cp skills, npm install, openclaw, systemsetup, ollama, brew services, python3, find, WebSearch, and WebFetch for multiple HVAC/business domains.

## Scheduled Tasks
- phoenix-tam-engine — Phoenix metro home services TAM scraper, discovers/verifies/catalogs businesses city by city

## Plans
- synchronous-petting-creek.md — Phoenix TAM Lovable Owner Profile Pages. Full architecture for personalized web pages with QR codes for home services business owners. React + Tailwind + Supabase. 6-section page structure with hero, research narrative, market context, value turns, estimated range, and CTA.

## Data Assets on Desktop
- all_pipeline_data.csv — Full pipeline export
- next_chapter_full_research.csv — Research data export

## Errors During Harvest
- docker: not found (not installed)
- cargo/rustc/go: not found (not installed)
