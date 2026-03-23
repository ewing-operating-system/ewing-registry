# Thread Audit: Phoenix TAM Engine Build
**Session:** phoenix-tam-engine-build
**Machine:** ClawdBots-Mac-mini-8
**Date:** 2026-03-23
**Approximate duration:** ~3 hours
**Model:** Claude Opus 4.6 (1M context)

---

## Thread Metadata
| Metric | Value |
|--------|-------|
| Tools used | ~25 (Bash, Write, Read, Edit, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, TodoWrite, Agent, Skill, mcp__scheduled-tasks, various MCP tools) |
| Files created | 18 (15 Python + schema.sql + .gitignore + .env.example) |
| Files modified | 6+ (config.py, main.py, google_maps.py, supabase_client.py, consensus.py, gemini_agent.py — by ClawdBot in parallel session) |
| Skills triggered | clawdbot-creator, debrief, output-skill (implicit) |
| Skills NOT triggered (should have been) | prompt-refiner (the initial wall-of-text was a textbook trigger), keys-and-credentials (Ewing explicitly asked for it), ewing-connectors |
| Errors encountered | 2 (Supabase REST API DDL failure → fixed with psycopg2; 1Password interactive terminal → abandoned) |
| Pivots | 3 (REST→psycopg2 for schema, 1Password→skip, Lovable project→deferred) |
| Context health | Good — Opus 4.6 with 1M context handled the full build without degradation |

## Goal Assessment
- **Stated goal:** Build a scraping engine for every home services business in Phoenix metro with dual-model verification, cost tracking, and enrichment via Exa + Clay
- **Achieved:** YES — engine built, tables created, GitHub repo pushed, code running on Mac Mini
- **Scope changes:** 3 — added Lovable frontend (deferred), added 1Password vault (abandoned), added permanent credential vault (started)

---

## Items Found — Tagged

### Phoenix TAM Engine (Python Application)
- **Type:** repo
- **Created:** yes — full 15-file Python application
- **Machine:** Mac Mini
- **Anti-pattern tags:** 🏗️ (large build in single session)
- **Offense tags:** 🟢
- **What happened:** Built from scratch in ~90 minutes. Google Maps scraper, awards list scraper (7 sources), AZ ROC scraper, Gemini Flash verifier, Haiku verifier, consensus engine, Exa enricher, Clay enricher, cost tracker, Supabase client, main orchestrator.
- **Business impact:** Direct — this is the target list for AND Capital's M&A outreach in Phoenix metro
- **Recommendation:** Keep. Run discovery phase on remaining cities.

### Supabase TAM Schema (6 tables + 2 views)
- **Type:** database
- **Created:** yes
- **Machine:** Remote (asavljgcnresdnadblse.supabase.co)
- **Anti-pattern tags:** None
- **Offense tags:** 🟢
- **What happened:** tam_businesses, tam_verifications, tam_disagreements, tam_enrichments, tam_awards_sources, tam_cost_log, plus tam_cost_summary and tam_cost_per_record views. Cross-table dedup against M&A targets table added by parallel ClawdBot.
- **Business impact:** Permanent data store for all Phoenix metro business intelligence
- **Recommendation:** Keep. Schema is clean and extensible.

### GitHub Repo (clawdking1-GH/phoenix-tam-engine)
- **Type:** repo
- **Created:** yes — private repo
- **Machine:** GitHub
- **Anti-pattern tags:** 🏠 (repo under clawdking1-GH, not ewing-operating-system)
- **Offense tags:** 🟡
- **What happened:** Created under clawdking1-GH account. Should probably be under ewing-operating-system for consistency with ewing-registry.
- **Business impact:** Low — repo location doesn't affect function
- **Recommendation:** Consider transferring to ewing-operating-system org

### 1Password Integration Attempt
- **Type:** decision
- **Created:** no — abandoned
- **Machine:** Mac Mini
- **Anti-pattern tags:** 🔁 (circular conversation), 🖐️ (required Ewing manual intervention that couldn't happen)
- **Offense tags:** 🟡
- **What happened:** Ewing wanted 1Password CLI connected so ClawdBots could pull credentials automatically. The `op account add` command requires interactive terminal input (email, secret key, master password). Multiple Claude sessions tried to guide Ewing through it. He got frustrated and abandoned.
- **Business impact:** Low — credentials are stored in skills instead. 1Password would be better long-term.
- **Recommendation:** Revisit when Ewing is on a video call with someone who can walk him through it. Or set it up next time someone has physical access to the Mac Mini.

### Permanent Credential Vault Request
- **Type:** decision
- **Created:** started but not completed
- **Machine:** Mac Mini
- **Anti-pattern tags:** 🔑 (credential management gap)
- **Offense tags:** 🟡
- **What happened:** Ewing explicitly asked for a permanent credential vault — "from now on, any time I give you a key of any kind, label it, store it, time stamp it, and organize it." The keys-and-credentials skill exists but wasn't fully populated in this thread.
- **Business impact:** Medium — Ewing wastes time re-providing keys across sessions
- **Recommendation:** Wire. Populate keys-and-credentials skill with ALL known keys from clawdbot-creator and ewing-connectors. Make it the single source.

### Parallel ClawdBot Modifications
- **Type:** file modifications
- **Created:** no — modified existing files
- **Machine:** Mac Mini
- **Anti-pattern tags:** 🐙 (multiple bots modifying same repo simultaneously)
- **Offense tags:** 🟡
- **What happened:** While this thread was building the engine, a parallel ClawdBot session upgraded the Google Maps scraper to v1 API, added junk filtering, cross-table dedup, auto-agree logic, and dual-model column storage. The changes are good but happened outside this thread's awareness.
- **Business impact:** Positive — the engine is now better. But concurrent modification is risky.
- **Recommendation:** Establish clear ownership per session. One bot writes code, others read-only.

---

## Handoff Notes — CRITICAL

### What's unfinished
1. **Lovable frontend** — Ewing asked for a Lovable page with personal narratives, industry multiples, and valuation parameters. Not started.
2. **Credential vault population** — keys-and-credentials skill needs ALL keys consolidated
3. **Remaining cities** — only Phoenix/HVAC has been run. 23 more cities and 9 more categories to go.
4. **Haiku verification** — ANTHROPIC_API_KEY not set in env, so only Gemini is running. Dual-model verification is single-model right now.

### What's broken
- Nothing critical. Engine runs. 2 uncommitted changes in phoenix-tam-engine repo (from parallel ClawdBot).

### What's blocking
1. **ANTHROPIC_API_KEY** needs to be exported in Mac Mini shell for Haiku to work
2. **Clay API integration** untested — Clay's v3 API may need webhook-based enrichment rather than direct REST calls
3. **1Password** abandoned — credentials still spread across multiple skill files

### What's next
1. Export ANTHROPIC_API_KEY on Mac Mini (`echo 'export ANTHROPIC_API_KEY=sk-ant-api03-...' >> ~/.zshrc`)
2. Run full discovery across all 24 cities: `python3 main.py --phase discover`
3. Run verification: `python3 main.py --phase verify`
4. Build the Lovable frontend with industry multiples and valuation parameters
5. Commit the 2 uncommitted changes in phoenix-tam-engine

### What to NOT repeat
- Don't attempt 1Password CLI setup via Claude — it requires interactive input
- Don't run multiple ClawdBots modifying the same repo simultaneously without coordination
- Don't ask Ewing what `openclaw tui` is — just tell him

### Files to read first
- `/Users/clawdbot/Projects/phoenix-tam-engine/config.py` — all keys and settings
- `/Users/clawdbot/Projects/phoenix-tam-engine/main.py` — orchestrator with all CLI flags
- `~/.claude/skills/keys-and-credentials/SKILL.md` — credential vault
- `~/.claude/skills/clawdbot-creator/SKILL.md` — full environment blueprint

---

## What This Thread Should Have Done Differently
1. **Should have run prompt-refiner on Ewing's initial wall-of-text.** It was a textbook trigger — multiple competing intentions (scrape + verify + enrich + build lovable + track costs + research phone sources). Would have saved scope creep.
2. **Should have set ANTHROPIC_API_KEY in .zshrc immediately** instead of leaving Haiku verification broken. The key was right there in clawdbot-creator.
3. **Should have committed the parallel ClawdBot's changes** before starting this thread's work. Two uncommitted changes sitting in the repo means merge risk.
4. **Should have answered "openclaw tui" instantly** instead of guessing `claude` first. The clawdbot-creator skill says OpenClaw is installed on Mac Mini.
5. **Should have consolidated credentials into one vault** before building the engine, rather than scattering keys across config.py, .env.example, and skills.

## Gotchas Discovered
- **Supabase REST API cannot execute DDL (CREATE TABLE, etc.)** — must use direct Postgres connection via psycopg2 or psql
- **Google Places API v1 (new) returns `displayName` as `{"text": "name"}` object**, not a plain string — parser must handle both formats
- **1Password CLI `op account add` requires fully interactive terminal** — cannot be automated via Claude's Bash tool
- **Multiple Claude Code sessions can modify the same repo simultaneously** without any locking mechanism — coordination must be manual
