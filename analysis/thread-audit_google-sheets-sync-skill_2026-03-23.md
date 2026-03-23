# Thread Audit: Google Sheets Sync Skill — 2026-03-23

## Thread Metadata
| Field | Value |
|-------|-------|
| Session name | google-sheets-sync-skill |
| Machine | ClawdBots-Mac-mini-8.local |
| Approximate duration | ~15 minutes |
| Tools used | 4 (Bash, Glob, Read, Skill) |
| Files created/modified | 0 (pre-debrief) |
| Skills triggered | 3 (keys-and-credentials, debrief, skill-sync) |
| Skills NOT triggered | 20 (expected — this was a planning thread) |
| Errors encountered | 2 (Supabase JWT "Invalid API key", psql connection failed) |
| Pivots | 1 (vision → blocker discovery → debrief) |
| Context health | Excellent — short thread, no degradation |

## Goal Assessment
- **Stated goal:** Build a reusable Google Sheets sync skill for ClawdBot — two-way data flow between Supabase and Sheets, human-in-the-loop review via spreadsheet
- **Was it achieved?** No — planning only, blocked by missing credentials
- **What's done:** Vision documented, 9 architecture questions defined, credential audit complete, blocker identified
- **What's left:** Answer remaining 8 questions, create Google Sheets service account, build the actual skill
- **Scope changes:** 0 — Ewing's vision stayed consistent throughout

## Items Found — Tagged

### Google Sheets Sync Skill (planned, not built)
- **Type:** skill
- **Created or Modified:** No — design phase only
- **Machine:** ClawdBots-Mac-mini-8
- **Anti-pattern tags:** 🏗️ (scaffolding without foundation — no credential to build on)
- **Offense tags:** 🟢 (correct to stop and scope before building)
- **What happened:** Ewing described a two-way Google Sheets sync skill. Claude scoped 9 architecture questions. Service account credential was missing, blocking all implementation.
- **Business impact:** HIGH — this would give Ewing a non-terminal interface to review and augment ClawdBot research data. Critical for scaling the human-in-the-loop workflow beyond just Ewing.
- **Recommendation:** Create service account in Google Cloud Console, download JSON, add to keys-and-credentials vault, then build skill

### Supabase JWT — Possible Expiration
- **Type:** decision
- **Created or Modified:** No — discovered
- **Machine:** ClawdBots-Mac-mini-8
- **Anti-pattern tags:** 🔑 (credential issue)
- **Offense tags:** 🟡 (needs investigation)
- **What happened:** Service role JWT returned "Invalid API key" when querying Supabase REST API during harvest. The truncated keys in the vault may not be the full JWTs.
- **Business impact:** If the stored JWTs are wrong, every skill that hits Supabase is broken or using a different credential source.
- **Recommendation:** Verify the full JWT values in keys-and-credentials. The vault shows truncated values — compare against what's in .openclaw/.env.

### Phoenix TAM Engine — 4 Unpushed Commits
- **Type:** repo
- **Created or Modified:** Previously modified, not in this thread
- **Machine:** ClawdBots-Mac-mini-8
- **Anti-pattern tags:** 🔄 (unpushed work accumulating)
- **Offense tags:** 🟡 (not urgent but risky if machine dies)
- **What happened:** 4 commits sitting unpushed on main branch, plus 2 uncommitted file changes
- **Business impact:** If this machine has issues, those fixes are lost. The TAM engine improvements (auto-agree, service role fix, dedup) are valuable.
- **Recommendation:** Push to GitHub. Run `cd ~/Projects/phoenix-tam-engine && git push origin main`

### OpenClaw Pipeline — 118 Uncommitted Changes
- **Type:** repo
- **Created or Modified:** Previously, not this thread
- **Machine:** ClawdBots-Mac-mini-8
- **Anti-pattern tags:** 🔄 (drift), 💀 (possibly abandoned session files)
- **Offense tags:** 🟡 (cleanup needed)
- **What happened:** 118 deleted session files (.jsonl.deleted) cluttering the working directory. Plus 6 unpushed commits.
- **Business impact:** Low — these are cleanup artifacts. But the 6 unpushed commits may contain real work.
- **Recommendation:** Clean up deleted session files, push the 6 commits

### Auto-Share Defaults
- **Type:** decision
- **Created or Modified:** Yes — locked in during this thread
- **Machine:** All
- **Anti-pattern tags:** None
- **Offense tags:** 🟢 (good decision, documented)
- **What happened:** Ewing specified that all Google Sheets/folders/projects should auto-share with mark@chapter.guide and Ewing@chapter.guide
- **Business impact:** Ensures Mark always has access to shared workspaces without manual sharing
- **Recommendation:** Keep — encode this as a config constant in the eventual skill

## Handoff Notes — CRITICAL

### What's unfinished
- The Google Sheets sync skill is 0% built. Only the requirements gathering started.
- 8 of 9 architecture questions remain unanswered

### What's broken
- Supabase service role JWT may be incorrect in the vault (returned "Invalid API key")
- phoenix-tam-engine has 4 unpushed commits at risk
- openclaw has 118 uncommitted changes (mostly session cleanup)

### What's blocking
- **Google Sheets service account JSON** — must be created in Google Cloud Console, downloaded, and added to this machine. Without it, no Sheets API access is possible.
- **Ewing's answers to questions 2-9** — specifically: what data flows, sync pattern, review UX, auto-create behavior

### What's next
1. Create Google Sheets service account in Google Cloud Console
2. Download the JSON key file to this machine
3. Add to keys-and-credentials vault
4. Answer the 8 remaining architecture questions
5. Build the skill (Python module with gspread + Supabase client)
6. Test with a real use case (e.g., pushing TAM engine results to a sheet for Ewing to review)

### What to NOT repeat
- Don't assume Google API keys work for Sheets — they're different auth mechanisms
- Don't try to query Supabase tables via REST without verifying the JWT first

### Files to read first
- `/Users/clawdbot/.claude/skills/keys-and-credentials/SKILL.md` — the credential vault
- `/Users/clawdbot/.claude/projects/-Users-clawdbot-Downloads-Claude-Code-on-this-computer-Desktop-Claude-Code/memory/project_infrastructure_map.md` — infrastructure context
- This audit file — for the 9 architecture questions and blocker status

## What This Thread Should Have Done Differently
1. **Should have verified Supabase JWT immediately** — the "Invalid API key" error means the vault may have truncated values. Should have cross-referenced with .openclaw/.env to confirm.
2. **Should have checked for the service account JSON earlier** — could have done this before asking all 9 questions, since it was a hard blocker.
3. **Should have offered to walk Ewing through creating the service account in Chrome** — Claude has Chrome browser automation. Could have opened Google Cloud Console and guided the process instead of just describing it.
4. **Could have started building the non-auth parts** — the Supabase-side schema, the skill skeleton, the config structure could all be built without the service account.
5. **The thread was too short** — only one answer was given before debrief was called. More progress was possible.

## Gotchas Discovered
1. **Supabase REST API key mismatch:** The JWTs stored in keys-and-credentials vault returned "Invalid API key." The vault may have truncated values or the keys may need rotation. Cross-reference with actual .env files.
2. **Google API key ≠ Google Sheets access:** Having Gemini/Maps/Custom Search API keys does NOT give you Sheets API access. Sheets requires either a service account JSON or OAuth credentials — completely separate auth path.
3. **psql not available on Mac mini:** Direct PostgreSQL connections to Supabase require psql, which is not installed. Use `brew install libpq` or the Supabase CLI for direct DB access.
