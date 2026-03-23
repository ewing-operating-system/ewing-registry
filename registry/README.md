---
name: Master Registry — All Identities, Credentials, URLs, Projects
description: Complete deduplicated registry of every email, username, API key name, URL, project, repo, and database across all machines. Source of truth from 12 harvests on 2026-03-23.
type: reference
---

## Email Identities (deduplicated)

**Active Work:**
- ewing@chapter.guide (primary work, Google Drive, Gmail)
- ewing@andcapital.ventures
- ewing@andcapitalventures.com
- ewing@engram.nexus (Claude/Anthropic account, Google Drive x2 mounts)
- ewing@revsup.com (Google Drive mounted)
- ewing@gopitch.black
- ewing@thepitch.black

**Personal:**
- ewing.gillaspy@gmail.com (Apple ID, 176+ logins)
- derekewingg@gmail.com
- hottytoddy_olemiss@yahoo.com
- crexltp@gmail.com

**Past Ventures:**
- ewing@topia.io
- ewing@top10salestalent.com

## Usernames (deduplicated)

- ewinggillaspy (AmEx, Fidelity, Edward Jones, Golf, TriNet, macOS user)
- derekgillaspy (Southwest, Anthem, Chase)
- ewinggillaspy1
- ewinggillaspy111
- ewingpersonal1
- lookingforai
- ewing_gillaspy
- ewing-operating-system (GitHub org)
- clawdking1-GH (GitHub, Mac mini)

## GitHub Accounts

| Account | Auth Method | Used On |
|---|---|---|
| ewing-operating-system | SSH (primary) | MacBook-27, MacBook-GREEN |
| clawdking1-GH | HTTPS/keyring | Mac-mini-8 |

**GitHub PAT (EXPOSED in git remotes, needs rotation):** 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 — found in recording-library and debugger-tool remote URLs on MacBook-27.

## API Key Names & Credential References (names only, NEVER values)

| Credential | Where Referenced | Status |
|---|---|---|
| ANTHROPIC_API_KEY | clawdbot-creator, mission-control, keys-and-credentials | Active, Tier 1 |
| Supabase Anon Key (sb_publishable_...) | clawdbot-creator, ewing-connectors | Active |
| Supabase Service Role Key (sb_secret_...) | clawdbot-creator, ewing-connectors | Active |
| Supabase DB Password | clawdbot-creator | Active |
| Supabase CLI Token | ewing-connectors | Active |
| Salesfinity API Key (sk_ff45...) | keys-and-credentials, salesfinity-loader, ewing-connectors, system-auditor, cold-call-workflow | Active |
| Exa.ai API Key | keys-and-credentials, exa-enrichment, ewing-connectors, cold-call-workflow, disk-cleanup | Active |
| Clay.com API Key | keys-and-credentials, ewing-connectors, cold-call-workflow | Active, $800/mo legacy plan |
| Clay.com Workspace ID | keys-and-credentials | Active |
| Clay.com Webhook URL | keys-and-credentials, ewing-connectors | Active |
| Google Custom Search API Key (AIzaSy...) | mission-control, GREEN memory | Active |
| Google Custom Search CX (843fa...) | mission-control, GREEN memory | Active |
| Google Sheets OAuth (ewing-google-sheets) | ewing-connectors | Active |
| Google Sheets ID (1FYAW-321f9Tv...) | reference_supabase_and_call_command | Active, receiving Clay data |
| GCP Service Account Key Path | ewing-connectors, .env.example | Active |
| GitHub Fine-Grained Tokens | git remotes | Active (one exposed, needs rotation) |
| Google/Gemini API Keys (3) | keys-and-credentials | Active |
| Apollo.io | keys-and-credentials | PLACEHOLDER — not configured |
| Instantly.ai | keys-and-credentials | PLACEHOLDER — not configured |
| Handwrytten | keys-and-credentials | PLACEHOLDER — not configured |
| SpokePhone | referenced in tasks | BLOCKED — no credentials yet |

**Credential Duplication Problem:** The same keys appear in multiple skills:
- Salesfinity key: in 5 different skills
- Exa key: in 5 different skills
- Supabase creds: in 4 different skills
- Two credential vaults exist: `keys-and-credentials` (Mac mini) and `ewing-connectors` (MacBook-27)

## Supabase Instances (4 live, 1 dead)

| Instance ID | Purpose | Region | Referenced By | Status |
|---|---|---|---|---|
| rdnnhxhohwjucvjwbwch | AND Call Command CRM (14 tables, 1,844 persons) | West US Oregon / us-east-1 | ewing-connectors, exa-enrichment, debugger-tool, .env files | LIVE — primary |
| ginqabezgxaazkhuuvvw | ewing-operating-system's Project | East US | clawdbot-creator | LIVE |
| asavljgcnresdnadblse | Phoenix TAM Engine / OpenClaw / mission-control | Unknown | clawdbot-creator, mission-control | LIVE |
| lhmuwrlpcdlzpfthrodm | ColdCall Universe pipeline | Unknown | Supabase CLI on MB-27 | LIVE |
| iwcvaowfogpffdllqtld | debugger-tool (old) | N/A | legacy refs | DEAD — remove all refs |

**Overlap/confusion:** `rdnnhxhohwjucvjwbwch` is referenced as both "and-call-command" AND "Exa enrichment" — may be the same DB serving both, or may need separation.

## Git Repositories (10 unique, deduplicated)

| Repo | GitHub Account | Machines Found On | Status | Risk |
|---|---|---|---|---|
| coldcall-universe | ewing-operating-system | GREEN + MB-27 | GREEN: 3 unpushed on v2-overnight-build; MB-27: 24 staged, push blocked | HIGH — auth broken |
| and-call-command-pipeline | ewing-operating-system | GREEN + MB-27 | Clean everywhere | OK |
| and-call-command-unified | ewing-operating-system | MB-27 (Google Drive) | Clean | OK |
| blank-canvas | ewing-operating-system | MB-27 | Untracked db-export/ dir | MEDIUM |
| debugger-tool | ewing-operating-system | MB-27 (Google Drive) | 2 unpushed commits (Branch2) | MEDIUM |
| nyc-war-story | ewing-operating-system | MB-27 (Google Drive) | Modified index.html | LOW |
| recording-library | ewing-operating-system | MB-27 (Google Drive) | Clean | OK |
| finance-dashboard | ewing-operating-system | MB-27 (Google Drive) | Unknown | OK |
| hovering-cloud | clawdking1-GH | Mac mini + MB-27 | Clean everywhere | OK |
| phoenix-tam-engine | clawdking1-GH | Mac mini | Uncommitted dedup.py | MEDIUM |
| openclaw/clawdbot-pipeline | clawdking1-GH | Mac mini | Clean, 79 reports, 11 outreach | OK |

**Overlap:** coldcall-universe exists on both GREEN and MB-27 with DIFFERENT states. GREEN has a v2-overnight-build branch with 3 unpushed commits. MB-27 has 24 staged files that can't push.

## Lovable Projects (deployed web apps)

| App | Lovable ID | URL | Status |
|---|---|---|---|
| AND Call Command CRM | 8724256f-b75a-45e9-bbc0-fab38cf80322 | and-call-command.lovable.app | Live |
| Precision Exploration (Official) | starred | Published | Live |
| Gym Wellness Hub | — | Published | Live |
| Fitness Pitch Builder | — | — | Edited 6 days ago |
| Remix of Precision Exploration | — | — | Edited 7 days ago |

**Note:** No Lovable projects are connected to GitHub repos. Code hosted internally by Lovable.

## Google Drive Accounts (4 mounted on MacBook-27)

| Account | Purpose |
|---|---|
| ewing@chapter.guide | Primary work — AND Capital, deals, repos |
| ewing.gillaspy@gmail.com | Personal |
| ewing@engram.nexus | AI/agent platform (x2 mounts) |
| ewing@revsup.com | Past venture |

## Google Drive Folder Structure (ewing@chapter.guide)

| Folder | Content |
|---|---|
| 00 - BioLev Sale | 31 PPTX files, 4 Python scripts, 1 Excel model |
| 01 - Next Chapter Main Docs | Primary docs |
| 02 - AND Capital | Deal docs |
| 03 - CII Advisors | Client docs |
| 04 - Sea Sweet | Deal docs |
| 05 - Other Deals | Misc deals |
| 06 - Biz-Dev Application | Business development |
| 07 - Company Training | Training materials |
| 08 - Third-Party Research | External research |
| 09 - Ole Miss Summer School | Education |
| 10 - Strategic Vendors | Vendor info |
| 11 - P&L (PRIVATE) | Financial data |
| 12 - Cold calling project | ColdCall Universe |
| 13 - New Roofing Rollup | New deal vertical |
| Github Ewing/ | 5 git repos |

## Skills (30 unique, deduplicated across all machines)

**MacBook-27 local (8):**
cold-call-workflow, disk-cleanup, ewing-connectors, finance-agent, password-migration, prompt-refiner, recording-collector, system-auditor

**Mac mini local (9):**
clawdbot-creator, file-share, harvester, keys-and-credentials, mission-control, output-skill, rate-oracle, skill-loader, tech-translator

**MacBook-GREEN local (6):**
fitness-industry-deck-maker, output-skill, prompt-refiner, rate-oracle, skill-loader, tech-translator

**Cowork session layer (22):**
clawdbot-creator, desktop-cleaner, docx, exa-enrichment, harvester, mission-control, output-skill, pdf, pec-case-manager, photo-metadata, pptx, prompt-refiner, revsup-oo, salesfinity-loader, schedule, skill-creator, skill-creator-fixed, skill-loader, tech-translator, transfer-to-mac, ui-touchup, xlsx

**Marketplace (28 on MB-27):**
All 22 Cowork skills + amazon-location-service + 5 others

**Skills that exist on ONLY ONE machine:**
- cold-call-workflow: MB-27 only
- disk-cleanup: MB-27 only
- ewing-connectors: MB-27 only
- finance-agent: MB-27 only
- password-migration: MB-27 only
- recording-collector: MB-27 only
- system-auditor: MB-27 only
- fitness-industry-deck-maker: GREEN only
- file-share: Mac mini only
- harvester: Mac mini only
- keys-and-credentials: Mac mini only
- rate-oracle: Mac mini + GREEN only

## Scheduled Tasks (10 on MB-27, 3 disabled on GREEN, 1 active on Cowork)

| Task | Machine | Schedule | Active |
|---|---|---|---|
| call-ingest-hourly | MB-27 | Hourly | YES |
| call-sync | MB-27 | Every 4 hours | YES |
| daily-maintenance | MB-27 | Daily 6:00 AM | YES |
| daily-tasks-created | MB-27 | Daily 8:00 AM | YES |
| dnc-salesfinity-sync | MB-27 | Every evening | YES |
| email-monitor | MB-27 | Hourly :05 | YES |
| nightly-system-audit | MB-27 | Weekly | YES |
| priority-rebuild | MB-27 | Sun 5pm + Wed 6pm | YES |
| queue-autocheck | MB-27 | Daily | YES |
| company-valuation-backfill | MB-27 | On demand | YES |
| daily-urgent-briefing | Cowork VM | Daily 6:06 AM | YES |
| pec-evidence-logger | Cowork VM | Daily 9:05 AM | NO |
| pec-fact-finder | Cowork VM | Daily 9:34 AM | NO |
| downloads-cleaner | Cowork VM | One-time | NO |
| daily-tasks | GREEN | — | NO |
| email-monitor | GREEN | — | NO |
| downloads-cleaner | GREEN | — | NO |

## MCP Tools (deduplicated across all environments)

| Tool | Available On |
|---|---|
| Fireflies.ai | All machines |
| Gmail | All machines |
| Google Calendar | All machines |
| Google Drive | All machines |
| Gamma | All machines |
| Claude in Chrome | All machines |
| Claude Preview | MB-27 |
| Control Chrome | MB-27, Cowork VMs |
| Vibe Prospecting (Explorium) | MB-27, Cowork VMs |
| Playwright | MB-27 (5-7 instances) |
| Cowork tools | Cowork VMs |
| MCP Registry | All machines |
| Scheduled Tasks | All machines |
| Session Info | Cowork VMs |
| Amazon Location Service | MB-27 (plugin) |
| GitHub plugin | MB-27 (plugin) |

## Memory Files (20 across 2 project contexts on MB-27)

**Project: My Drive (ewing@chapter.guide) — 9 files:**
- user_identity_map.md — All email identities, Apple IDs, Chrome profiles
- feedback_call_me_jack.md — Ewing calls Claude "Jack"
- feedback_list_naming.md — Salesfinity naming convention
- feedback_speak_in_clicks.md — Click-by-click UI directions
- project_clay_enrichment_pipeline.md — Clay webhook pipeline
- project_salesfinity_setup.md — Team structure (John, Danny, Ewing, Mark)
- project_master_life_cleanse.md — Life consolidation project
- reference_supabase_and_call_command.md — Supabase schema + GCP SA
- (1 unnamed)

**Project: Github Ewing — 11 files:**
- user_sales_role.md — Ewing's sales role and tools
- user_communication_preferences.md — Exact URLs, buttons, step-by-step
- design_context_graph.md — Zero-Navigation UX principle
- feedback_file_output_location.md — All outputs to ~/Downloads
- feedback_no_international_contacts.md — US/Canada only
- feedback_proactive_skill_usage.md — Use skills without asking
- feedback_salesfinity_loading_rules.md — 6 pre-load gates
- project_and_capital_strategic_pivot.md — March 2026 pivot to placement agents
- project_cold_call_workflow.md — Cold call workflow structure
- project_finance_agent.md — Finance agent + SQLite + Lovable
- (1 unnamed)

## Data Assets on MacBook-27

| Asset | Location | Size |
|---|---|---|
| Salesfinity call logs (8,039 records) | ~/Downloads/salesfinity-data/call-log-all.json | 15 MB |
| AI-scored calls (201) | ~/Downloads/salesfinity-data/scored-calls.json | 1.6 MB |
| Follow-ups (190) | ~/Downloads/salesfinity-data/follow-ups.json | 374 KB |
| Call transcripts (23) | ~/Downloads/transcripts/ | ~700 KB |
| Raw .m4a recordings (24) | ~/Downloads/*.m4a | ~600 MB |
| BioLev pitch decks (31 PPTX) | Google Drive/00 - BioLev Sale/ | Unknown |
| Google Drive total | ~/Library/CloudStorage/ | 106 GB |
