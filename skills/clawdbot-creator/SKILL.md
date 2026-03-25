---
name: clawdbot-creator
description: "Blueprint for spawning new bots. Master environment template containing all API keys, credentials, machine topology, connected tools, installed skills, rate limits, known errors, and setup procedures. Every new Claude Code or Cowork thread reads this first so Ewing never re-explains his setup or digs for keys again."
---

# ClawdBot Creator

This is the master blueprint for Ewing's entire operating environment. Every new ClawdBot, every new Claude Code session, every new Cowork thread should read this skill first. It contains everything needed to hit the ground running without asking Ewing a single question he's already answered.

## Who Is Ewing

- **Name:** Ewing Gillaspy
- **Email (primary):** ewing@engram.nexus
- **Email (business):** ewing@chapter.guide
- **Email (personal):** ewing.gillaspy@gmail.com
- **Companies:** Next Chapter (M&A advisory), RevsUp (staffing), AND Capital (PE)
- **Communication style:** Ewing is autistic and processes instructions literally. Give him exact commands, exact links, exact actions. One step at a time. No explanations unless he asks. See the `output-skill` for the full protocol — it is non-negotiable.
- **Priority:** Speed over security. Automation over manual work. If it can be automated, do it.
- **GitHub:** Setting up — username TBD (account creation in progress as of 2026-03-21)

## Machine Topology

### Mac Mini (ClawdBot Server)
- **Hostname:** ClawdBots-Mac-mini-5
- **User:** clawdbot
- **Role:** 24/7 automated pipeline server
- **OS:** macOS
- **Software installed:** Node.js, npm, Claude Code CLI, OpenClaw
- **Terminal tabs typically open:** OpenClaw TUI, Claude Code, Hovering Cloud file transfer, various zsh sessions

### MacBook Pro (Ewing's Daily Driver)
- **Role:** Ewing's personal machine, runs Cowork
- **Software:** Claude Desktop (Cowork), browser, standard apps
- **Skills installed via:** `clawdbot-setup.sh` (deployed from Mac Mini via Hovering Cloud)

### File Transfer Between Machines
- **Tool:** Hovering Cloud (npm package)
- **How it works:** Run `npx hovering-cloud` on Mac Mini → opens a local server → Ewing accesses from MacBook Pro browser to download files
- **Note:** Hovering Cloud has no web UI at `/` — shows "Cannot GET /" in browser. That's normal. Files download via direct links.

## API Keys & Credentials

Every key Ewing has ever shared, organized by service. When setting up a new ClawdBot, pull from here — never ask Ewing to go find a key.

### Anthropic (Claude API)
| Key | Value | Status |
|-----|-------|--------|
| API Key (Mac Mini) | `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` | ACTIVE |
| Organization | Ewing's Individual Org | — |
| Tier (as of 2026-03-21) | Tier 1 (checking if Tier 2 reached) | — |
| Billing | Auto-reload $15 when balance hits $5 | — |

**Where it lives:**
- Mac Mini terminal: `export ANTHROPIC_API_KEY=sk-ant-api03-...` (must add to `~/.zshrc` to persist)
- OpenClaw: hardcoded in `~/.openclaw/openclaw.json`

### Google Cloud / Gemini / Custom Search
| Key | Value | Status |
|-----|-------|--------|
| ClawdKing Gemini Key | `AIzaSyBdhczyRj6zEZzL37RVHlqY2cFb3Iuow_4` | ACTIVE |
| Original Gemini Key | `AIzaSyDVx92zD1CyrGNcnfEvDZkki6BlSFrW2e4` | ACTIVE |
| Custom Search Engine ID (cx) | `b5e920909f19a4466` | ACTIVE |

**Critical lesson learned:** Google has THREE separate search products with separate billing:
1. **Gemini API with grounding** (AI Studio) — 20 req/day free, separate paid upgrade
2. **Custom Search JSON API** — 100/day free, 10,000/day paid at $5/1000
3. **Google Search (browser)** — unlimited, no API

Paying for one does NOT unlock the others. Each has its own key, quota, and billing.

### Supabase (Pipeline Database)
| Key | Value | Status |
|-----|-------|--------|
| Project URL | `https://asavljgcnresdnadblse.supabase.co` | ACTIVE |
| Anon key | `sb_publishable_c_Y1tDzFFsePCQPmXIrelQ_dbJzRqZJ` | ACTIVE |
| Service role key | `sb_secret_f5FHU9OwvXWGQV_9rXlJew_gUTHyWXr` | ACTIVE |
| DB password | `QYEsjk1EwMBjBzZ0` | ACTIVE |

### Exa.ai (Search API)
| Key | Value | Status |
|-----|-------|--------|
| API Key | `4ecc9c5b-a981-4002-b080-e5a5319fead3` | ACTIVE |

### Clay (Data Enrichment)
| Key | Value | Status |
|-----|-------|--------|
| API Key | `f1f16b33f79964ce18e3` | ACTIVE |
| API Base URL | `https://api.clay.com/v3` | ACTIVE |
| Workspace ID | `211231` | ACTIVE |
| Webhook URL | `https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-5ea2383e-221b-46a2-99cc-b3986575c7ee` | ACTIVE |

**Where keys live on Mac Mini:**
- `~/.openclaw/.env` — Supabase URL and keys
- `~/.openclaw/openclaw.json` — Anthropic key (hardcoded, NOT read from .env)

## Connected Tools (Cowork MCP Integrations)

Ewing's Cowork has these services connected and available as MCP tools:

| Service | What It Does | MCP Prefix |
|---------|-------------|------------|
| Gmail | Read/search/draft emails | `gmail_*` |
| Slack | Read/send messages, search channels | `slack_*` |
| Google Calendar | List/create/update events | `gcal_*` |
| Google Drive | Search/fetch documents | `google_drive_*` |
| Fireflies | Meeting transcripts, summaries | `fireflies_*` |
| Chrome (Claude in Chrome) | Browser automation, page reading | `Claude_in_Chrome__*` |
| Gamma | Generate presentations | `generate`, `get_themes`, `get_folders` |
| Exa.ai | Contact enrichment (websets API) | Via exa-enrichment skill |
| Salesfinity | Parallel dialer, contact loading | Via salesfinity-loader skill |

## Installed Skills Library

These skills are available across Ewing's machines. When spawning a new ClawdBot, ensure the relevant ones are loaded.

### Core (Always Load)
| Skill | Purpose |
|-------|---------|
| `output-skill` | How to communicate with Ewing (literal, exact, one step at a time) |
| `prompt-refiner` | Restructure messy prompts before executing |
| `skill-creator` | Build, edit, and optimize skills |
| `tech-translator` | Translate terminal output and jargon into plain English |
| `skill-loader` | Bootstrap all default skills on session start |

### Operations
| Skill | Purpose |
|-------|---------|
| `keys-and-credentials` | Central vault for all API keys and tokens |
| `rate-oracle` | Track API rates, limits, costs, and workarounds |
| `clawdbot-creator` | This skill — master blueprint for spawning new bots |

### Business
| Skill | Purpose |
|-------|---------|
| `revsup-oo` | Build RevsUp Opportunity Overview documents |
| `pec-case-manager` | Manage Precision Exploration Corp fraud investigation |
| `exa-enrichment` | Enrich contact lists via Exa.ai Websets API |
| `salesfinity-loader` | Load contacts into Salesfinity parallel dialer |
| `ui-touchup` | Audit/optimize UI for sales tools |
| `desktop-cleaner` | Clean up Downloads, Desktop, find duplicates/junk |
| `photo-metadata` | Extract EXIF data from photos |

### Document Creation
| Skill | Purpose |
|-------|---------|
| `docx` | Create/edit Word documents |
| `pptx` | Create/edit PowerPoint presentations |
| `xlsx` | Create/edit Excel spreadsheets |
| `pdf` | Create/edit/merge/split PDFs |

### Utility
| Skill | Purpose |
|-------|---------|
| `schedule` | Create scheduled/recurring tasks |

## Rate Limits & Tier Intelligence

Before running any pipeline, check these limits. Getting throttled wastes hours.

### Anthropic Claude API
| Tier | Requirement | Sonnet Input Tokens/Min | Requests/Min |
|------|------------|------------------------|--------------|
| Free | $0 | 20,000 | 50 |
| Tier 1 | $5 credit | 60,000 | 60 |
| Tier 2 | $40 spend | 80,000 | 1,000 |
| Tier 3 | $200 spend | 160,000 | 2,000 |
| Tier 4 | $400 spend | 400,000 | 4,000 |

**Check tier:** https://console.anthropic.com/settings/limits
**Add credits:** https://console.anthropic.com/settings/billing

### Google Gemini (AI Studio)
- Free: 20 req/day (hard cap — NOT 1,500)
- 5 req/min rate limit
- Paid tier: ~60 req/min, higher daily limits

### Google Custom Search JSON API
- Free: 100 queries/day
- Paid: $5 per 1,000 queries (10,000/day cap)
- **Quota link:** https://console.cloud.google.com/apis/api/customsearch.googleapis.com/quotas

## Known Errors & Fixes

These are errors Ewing has hit before. If a new ClawdBot encounters them, apply the fix immediately instead of debugging from scratch.

### "permission denied" / EACCES
**Fix:** Prefix command with `sudo`

### OpenClaw retry loop on 429
**Cause:** Anthropic rate limit hit → retry → eats more quota → cascading failure
**Fix:** Restart OpenClaw. Consider adding exponential backoff. Don't run Scout + Next simultaneously on low tiers.

### "Cannot GET /" on Hovering Cloud
**Cause:** Normal — Hovering Cloud has no web UI at root URL
**Fix:** Ignore. Files transfer via direct download links, not browser UI.

### Google Custom Search 403 after enabling billing
**Cause:** Billing enabled ≠ API enabled. Must explicitly enable the Custom Search API AND wait for quota propagation (up to 1 hour in orgs).
**Fix:** https://console.cloud.google.com/apis/api/customsearch.googleapis.com/overview → Enable → wait

### Supabase JWT "Expected 3 parts" error
**Cause:** Using wrong key format in Authorization header
**Fix:** Use anon key for `apikey` header, full Bearer token for Authorization

### "zsh: parse error near '&'"
**Cause:** Pasting OpenClaw instructions into regular terminal instead of OpenClaw TUI
**Fix:** Launch `openclaw tui` first, THEN paste instructions

### Claude Code permission prompts ("Do you want to proceed?")
**Fix:** Type `/permissions` → type `Bash(*)` → save to User settings (option 3)

## Spawning a New ClawdBot — Step by Step

When Ewing says he wants a new ClawdBot, follow this sequence:

### 1. Define the Mission
Ask (using AskUserQuestion tool):
- What does this ClawdBot do? (one sentence)
- What tools/APIs does it need?
- Does it run 24/7 on Mac Mini, or on-demand in Cowork?

### 2. Set Up the Environment
Based on the mission, pull the right keys from this skill and configure:

**If Mac Mini (24/7 agent):**
```bash
# Export Anthropic key
export ANTHROPIC_API_KEY=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

# Add to ~/.zshrc so it persists
echo 'export ANTHROPIC_API_KEY=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' >> ~/.zshrc
```

**If Cowork session:**
- Keys are available via this skill — no export needed
- Connected tools are already wired via MCP integrations

### 3. Install Required Skills
Generate a setup script based on which skills the new bot needs:

```bash
#!/bin/bash
# ClawdBot skill installer
SKILL_DIR="$HOME/.claude/skills"
mkdir -p "$SKILL_DIR"

# Copy each required skill
for skill in output-skill prompt-refiner tech-translator keys-and-credentials rate-oracle; do
  mkdir -p "$SKILL_DIR/$skill"
  # Skill content gets written here by the creator
done
echo "Skills installed."
```

### 4. Load Default Skills
Every ClawdBot session starts by loading:
1. `output-skill` (communication protocol — always first)
2. `prompt-refiner` (catch messy prompts)
3. `skill-creator` (build/edit skills on the fly)
4. `tech-translator` (translate jargon for Ewing)

Then load mission-specific skills.

### 5. Configure Auto-Approve (Claude Code)
If running in Claude Code terminal:
- `/permissions` → `Bash(*)` → save to User settings (option 3)
- This prevents the "Do you want to proceed?" prompts Ewing hates

### 6. Verify Everything Works
Run a quick health check:
- Anthropic API: `curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-sonnet-4-6","max_tokens":10,"messages":[{"role":"user","content":"ping"}]}'`
- Check tier: https://console.anthropic.com/settings/limits
- Check rate limits against rate-oracle before running batch operations

### 7. Hand Off to Ewing
Give Ewing:
1. One command to launch the bot
2. What it will do when launched
3. How to stop it if needed

## Updating This Skill

When Ewing shares a new key, connects a new tool, installs a new skill, or discovers a new error pattern — update this skill immediately. This is the single source of truth. If it's not in here, the next ClawdBot won't know about it.

### When to update:
- New API key created or rotated → add to Keys section, mark old as RETIRED
- New MCP tool connected → add to Connected Tools table
- New skill created → add to Skills Library table
- New error pattern discovered → add to Known Errors section
- Machine config changed → update Machine Topology
- Rate limit tier changed → update Rate Limits section

This skill is Ewing's institutional memory. Treat it accordingly.
