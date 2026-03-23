---

## Harvest: MacBook-GREEN — 2026-03-22T01:57:12Z

### Machine Info
- Hostname: MacBook-GREEN
- User: ewingnewton
- OS: macOS 26.3.1 (Build 25D2128) — Darwin 25.3.0 arm64
- Disk: 850GB used / 926GB total (96% full, 39GB free on data volume)
- Node: v25.8.1
- Git: 2.50.1 (Apple Git-155)
- Homebrew packages: 26

### Skills Found (6 local + 18 plugin-based)

**Local (~/.claude/skills/):**
- fitness-industry-deck-maker — BioLev x Nutrishop genetic testing sales deck builder
- output-skill — Communication protocol for Ewing (literal, terse, exact actions)
- prompt-refiner — Restructure messy prompts before execution
- rate-oracle — Track API rates, limits, costs across all tools
- skill-loader — Session bootstrapper, loads defaults
- tech-translator — Plain English translation of technical output

**Plugin-based (anthropic-skills):**
- desktop-cleaner — Desktop file triage and cleanup
- docx — Word document creation/editing
- exa-enrichment — Contact enrichment via Exa.ai
- harvester — This skill (machine inventory → Slack canvas)
- mission-control — ClawdBot command center
- output-skill (plugin copy) — Same as local
- pdf — PDF manipulation
- pec-case-manager — Precision Exploration Corp fraud case
- photo-metadata — EXIF analysis
- pptx — PowerPoint creation/editing
- prompt-refiner (plugin copy) — Same as local
- revsup-oo — RevsUp Opportunity Overview builder
- salesfinity-loader — Load contacts into parallel dialer
- skill-creator / skill-creator-fixed — Build and optimize skills
- skill-loader (plugin copy) — Same as local
- tech-translator (plugin copy) — Same as local
- transfer-to-mac — Cross-machine file transfer via Claude Desktop
- ui-touchup — UI/UX audit for sales tools
- xlsx — Spreadsheet manipulation
- clawdbot-creator — Master blueprint for spawning new bots

### Scheduled Tasks (6)
1. **daily-accomplishment-report** — Compile daily accomplishments into .docx and email
2. **daily-urgent-briefing** — Morning briefing from calendar and Gmail before dialing block
3. **desktop-cleaner** — Desktop triage: rename, route, archive, delete junk
4. **downloads-cleaner** — Downloads triage: rename, route, track state, protect contacts
5. **pec-evidence-logger** — Auto-catalog new PEC case evidence files
6. **pec-fact-finder** — Scan PEC case folder and Gmail for new evidence, extract claims

### Memory Files

**user_identity.md:**
- Ewing Gillaspy, goes by Ewing, calls Claude "Jack"
- GitHub: ewing-operating-system
- Work: ewing@chapter.guide | Personal: ewing.gillaspy@gmail.com | Salesfinity: ewing@engram.nexus
- Terse responses, no superlatives, click-by-click UI guidance
- First-time app builder, teach concepts along the way
- Stack: Supabase, Clay, Salesfinity, Exa, GitHub SSH

**project_overnight_build.md:**
- ColdCall Universe V2: Merge and-call-command-pipeline + coldcall-universe repos
- Live Supabase: lhmuwrlpcdlzpfthrodm (real data)
- Dead Supabase: iwcvaowfogpffdllqtld (empty, ignore)
- Lovable project: 8724256f-b75a-45e9-bbc0-fab38cf80322 (connected to dead debugger-tool repo)
- Data flow: Clay → Google Sheet → Pipeline → Supabase
- People: Ewing (ewing@engram.nexus), Mark DeChat (mark@revsup.com)
- APIs: Supabase, Clay Webhook, Exa, Salesfinity, GCP Service Account

**Downloads memory (MEMORY.md):**
- GitHub SSH setup complete and tested
- SSH key: ed25519 at ~/.ssh/id_ed25519
- All git operations use SSH, never HTTPS

### CLAUDE.md Files

**~/.claude/CLAUDE.md:**
- Identity: Ewing Gillaspy, ewing@chapter.guide, ewing.gillaspy@gmail.com
- GitHub: ewing-operating-system, always SSH
- Project: "Jack teaches Ewing How to Build"
- Communication: Terse, no superlatives, click-by-click UI, autonomous execution
- Business: AND Capital Ventures, Chapter.guide, Engram.nexus, PitchBlack Consulting
- Tools: Salesfinity, Clay, Exa, Supabase (ColdCall Universe)

### Git Repositories

**1. hovering-cloud** (pushed, clean)
- Remote: https://github.com/clawdking1-GH/hovering-cloud.git
- Branch: main (up to date)
- Description: Cross-desktop shared clipboard v1.0

**2. and-call-command-pipeline** (pushed, clean — exists in 2 locations)
- Remote: git@github.com:ewing-operating-system/and-call-command-pipeline.git
- Paths: ~/.claude/repos/ AND ~/Documents/
- Branch: main
- Description: AND Capital Cold Calling Universe pipeline scripts

**3. coldcall-universe** (3 UNPUSHED COMMITS on v2-overnight-build)
- Remote: git@github.com:ewing-operating-system/coldcall-universe.git
- Branch: v2-overnight-build (active), main (exists)
- Unpushed: Phase 1 merge, Phases 2-8 waterfall enrichment, Output docs
- Untracked: docs/db_full_export.json, db_schema.json, db_schema_readable.md
- Description: ColdCall Universe V2 — unified sales intelligence platform

**4. overwatch** (NO COMMITS, untracked files only)
- Remote: git@github.com:ewing-operating-system/overwatch.git
- Untracked: .npmrc, dist/, electron-builder.yml, electron.vite.config.ts, node_modules/
- Description: Electron app (appears to be a new/abandoned project)

**5. Google Drive repos (synced, not local working copies):**
- recording-library
- debugger-tool (DEAD — per memory)
- nyc-war-story

### Connected MCP Tools (this session)
- **Fireflies** — Meeting transcripts search, fetch, share, channels
- **Gamma** — Presentation/document/webpage generation
- **Gmail** — Email search, read, draft, send, labels
- **Google Calendar** — Events CRUD, find meeting times, free time
- **Google Drive** — Search and fetch documents
- **Claude in Chrome** — Browser automation (read page, click, type, screenshot, navigate)
- **Claude Preview** — Dev server preview (start, screenshot, inspect, click, fill)
- **MCP Registry** — Search and suggest new connectors
- **Scheduled Tasks** — Create, update, list scheduled task jobs

### Credential Keys Referenced
**output-skill SKILL.md contains:**
- Supabase URL (lhmuwrlpcdlzpfthrodm)
- Supabase anon key
- Supabase service role key
- Google/Gemini API key

**rate-oracle SKILL.md references:**
- Claude API pricing (Sonnet 4.6, Haiku 4.5)
- Supabase limits

**project_overnight_build.md contains:**
- Exa API Key
- Salesfinity API Key
- Clay Webhook URL
- GCP Service Account email

**.env file found:**
- debugger-tool/.env (in Google Drive — keys not read)

### Projects & Applications

| Name | Path | Type | Description |
|---|---|---|---|
| hovering-cloud | ~/hovering-cloud | Node.js | Cross-desktop shared clipboard |
| hovering-cloud app | ~/.hovering-cloud/app | Node.js | Hovering cloud client app |
| and-call-command-unified | Google Drive | Node.js + Python | Unified call command pipeline |
| recording-library | Google Drive | Node.js | Recording library project |
| debugger-tool | Google Drive | Node.js | DEAD Lovable-connected project |
| finance-dashboard | Google Drive | Node.js | Finance dashboard |
| coldcall-universe | ~/.claude/repos/ | Python | ColdCall Universe V2 — sales intelligence |
| overwatch | ~/overwatch | Electron/Node.js | Desktop app (new/abandoned) |

### Running Services
Unable to enumerate (sandbox restricted `ps` and `lsof`).

### Databases
No local database engines installed via Homebrew. All database operations use remote Supabase instances.

### Installed Tools
- Node.js v25.8.1
- Git 2.50.1 (Apple Git-155)
- 26 Homebrew packages
- Claude Code 2.1.78
- ripgrep (via Claude Code bundled binary)

### Settings & Configuration

**settings.json:**
- Permission mode: bypassPermissions (all tools auto-allowed)
- Plugins: claude-plugins-official (GitHub marketplace)
- All tools allowed: Bash, Edit, Write, Read, Glob, Grep, WebFetch, WebSearch, NotebookEdit, Agent, TodoWrite, Skill, mcp__*

### LaunchAgents
- BlueJeans (video conferencing helper)
- Google Updater/Keystone
- Grammarly (ProjectLlama — shepherd, uninstaller, update service, cleanup)
- Snap Camera

### Errors During Harvest
- `ps`, `grep`, `lsof`, `head`, `curl`, `wget`, `pip3`, `python3`, `docker`, `brew` — blocked by Claude Code sandbox (not on PATH or restricted)
- No Slack MCP connector available — cannot append to canvas F0ANYTBD0HW directly

### Summary
MacBook-GREEN is Ewing's primary persistent workstation. It holds all real work: 4 active git repos (1 with 3 unpushed commits on coldcall-universe v2-overnight-build), 6 local skills, 6 scheduled tasks, 18+ plugin skills, and 9 MCP integrations (Fireflies, Gmail, GCal, Drive, Chrome, Preview, Gamma, Scheduled Tasks, Registry). Disk is 96% full. All database work is remote Supabase. The real persistent state lives in: (1) the git repos, (2) Google Drive sync folders, (3) ~/.claude/ skills and memory, and (4) ~/Documents/Claude/Scheduled/ task definitions. The coldcall-universe repo has unpushed work that should be pushed.

---
