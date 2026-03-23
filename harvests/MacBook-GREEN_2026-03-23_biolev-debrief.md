## Debrief: MacBook-GREEN — 2026-03-23 — BioLev x Nutrishop Deck Build

### Machine Info
- Hostname: MacBook-GREEN
- User: ewingnewton
- OS: macOS 26.3.1 (Darwin 25.3.0 arm64)
- Disk: 926GB total, 96% used (39GB free)
- Timestamp: 2026-03-23T01:57:24Z

---

### Thread Summary

**Duration:** ~8 hours across 2 sessions (Mar 20-21, continued Mar 22-23)
**Project:** BioLev x Nutrishop genetic testing pitch decks for gym chain CEOs
**Primary tools used:** Gamma.app (deck generation), Google Drive MCP, Slack MCP, Chrome MCP, Claude Skills

### What Was Built

| Deliverable | Description |
|-------------|-------------|
| **31-slide mega-deck content** | Complete BioLev x Nutrishop pitch narrative, 800 lines, all numbers sourced |
| **Gamma prompt file** | `~/Downloads/biolev-gamma-prompt.md` — 58K chars, INTENT+LAYOUT+CONTENT per slide |
| **Gamma deck v1** | 31-slide dark navy theme |
| **Gamma deck v2** | 31-slide Nutrishop branded |
| **24 Hour Fitness CEO deck** | 5 slides, `rush` theme, Karl Sanft quote, $76M-$114M math |
| **Anytime Fitness CEO deck** | 5 slides, `indigo` theme, Tom Leverton + Stacy Anderson quotes, $13.9M-$19.7M math |
| **Life Time CEO deck** | 5 slides, `editoria` theme, Bahram Akradi quotes, $51.5M-$103.5M math |
| **Branded CEO deck regen** | All 3 remade with proper `themeId` + AI-generated brand-matched imagery |
| **Fitness Industry Deck Maker skill** | `~/.claude/skills/fitness-industry-deck-maker/` — SKILL.md + 4 reference files |
| **Pricing & economics reference** | All test pricing, Evolt financing, chain-level TAM, staff incentives |
| **Audit findings reference** | Love/hate/missing for 5 original decks + cross-deck gap mapping |
| **Ingredient science reference** | Sucralose, Ace-K, silicon dioxide, digestive enzyme research with citations |

### What Was Fixed

| Issue | Fix |
|-------|-----|
| Chain member counts wrong (400/5000/175) | Corrected to 244/2500/185 from SEC filings, FDD, corporate data |
| Evolt pricing ($8K/mo lease) | Changed to $199/mo at 0%, $8K total, owned after 40 months |
| Evolt "doubles conversion" claim | Softened to "~50% increase in test adoption" |
| S1P/Travis Helm throughout | Stripped from all files per user direction |
| WRKETHIC enzyme attribution | Corrected: protease/bromelain/papain (not Aminogen) |
| Protein per serving (25g) | Corrected to 30g |
| Training time (2 hours) | Corrected to 30 minutes |
| Gene categories (invented) | Corrected to actual BioLev: GC/CYP2R1/DHCR7, MTHFR, CRP/IL-6/TNF-α, SOD2/GPX1/CAT, FUT2/BCMO1/SLC23A1 |
| Gamma branding (ignored hex codes) | Fixed by using `themeId` parameter instead of additionalInstructions |

### Strategic Additions

- Three-layer math model (addressable → BioLev → Evolt)
- Sensitivity analysis (3%/5%/8% conversion scenarios)
- Membership retention value ($244-$735/member)
- Nutrishop vs GNC positioning slide
- 40-month Evolt payoff timeline
- Life Time premium AOV model ($150/mo)
- Habit loop integration (SCAN → TEST → BUY → RESCAN → REORDER)
- CEO quotes from public statements on each brand-specific deck
- 31-slide → 5-slide CEO compression

### Key Files on This Machine

```
~/.claude/skills/fitness-industry-deck-maker/SKILL.md
~/.claude/skills/fitness-industry-deck-maker/references/mega-deck-content.md (36K)
~/.claude/skills/fitness-industry-deck-maker/references/pricing-and-economics.md (5K)
~/.claude/skills/fitness-industry-deck-maker/references/audit-findings.md (5K)
~/.claude/skills/fitness-industry-deck-maker/references/ingredient-science.md (4.5K)
~/Downloads/biolev-gamma-prompt.md (58K)
~/Downloads/biolev-drive-files/ (5 files from Google Drive)
~/Downloads/BioLev-Nutrishop.pdf
~/Downloads/BioLev-Nutrishop.pptx
~/Downloads/Genetic-Testing-Meets-Supplement-Retail-For-Gyms.pdf
~/Downloads/Genetic-Testing-Meets-Supplement-Retail-For-Gyms.pptx
```

### Skills on This Machine

| Skill | Description |
|-------|-------------|
| fitness-industry-deck-maker | BioLev x Nutrishop deck builder — single source of truth |
| output-skill | Communication protocol for Ewing |
| prompt-refiner | Restructures messy prompts before execution |
| rate-oracle | API rate limit tracking |
| skill-loader | Session bootstrapper |
| tech-translator | Jargon to plain English |
| + 25 more synced from ewing-registry | debrief, harvester, storyteller, mission-control, etc. |

### Memory Files

| File | Content |
|------|---------|
| `user_identity.md` | Ewing's identity, emails, GitHub, communication prefs |
| `project_overnight_build.md` | ColdCall Universe V2 merge project, Supabase/Clay/Salesfinity integration |
| `MEMORY.md` (Downloads) | GitHub SSH setup complete |
| `MEMORY.md` (Github) | Index pointing to user_identity + project_overnight_build |

### Git Repos on This Machine

| Repo | Remote | Status |
|------|--------|--------|
| ~/hovering-cloud | clawdking1-GH/hovering-cloud | Clean, 1 commit |
| ~/overwatch | ewing-operating-system/overwatch | Untracked files (new Electron project) |
| ~/Documents/and-call-command-pipeline | ewing-operating-system/and-call-command-pipeline | Clean, 1 commit |
| ~/.claude/repos/and-call-command-pipeline | same as above | Clean |
| ~/.claude/repos/coldcall-universe | ewing-operating-system/coldcall-universe | 3 unpushed commits, untracked docs |
| ~/ewing-registry | ewing-operating-system/ewing-registry | Active — skills + harvests |

### Credential References Found

| Skill/File | Keys Referenced |
|------------|----------------|
| output-skill | supabase.co reference |
| project_overnight_build.md | Supabase URL, Clay webhook, Exa API key, Salesfinity key, GCP service account |
| debugger-tool/.env | VITE_SUPABASE_PROJECT_ID, VITE_SUPABASE_PUBLISHABLE_KEY, VITE_SUPABASE_URL |

### Installed Tools

- Node v25.8.1, Python 3.9.6, Git 2.50.1
- Brew packages: node, pnpm, gh, typescript, fnm, cursor, sqlite
- Claude Code 2.1.78

### Connected MCP Tools (this session)

- Fireflies (meeting transcripts)
- Gamma (presentation generation)
- Gmail
- Google Calendar
- Google Drive
- Slack
- Claude in Chrome (browser automation)
- Claude Preview (dev server)
- Scheduled Tasks
- MCP Registry

### Settings

- Permission mode: bypassPermissions
- All tools allowed (Bash, Edit, Write, Read, Glob, Grep, WebFetch, WebSearch, Agent, mcp__*)
- Plugin: github@claude-plugins-official

### Open Items

| Item | Status |
|------|--------|
| Google Doc with Gamma links still in My Drive root | Not moved to target folder |
| Market Analysis docx (46K chars) | Not read |
| BioLev_Gym Market.pptx | Not read |
| BioLevSolutionOneDealTerms.pptx | Not read |
| coldcall-universe has 3 unpushed commits | Needs `git push` |
| Final creative review of 3 branded CEO decks | Pending Ewing's review |

### Anti-Pattern Tags Observed

- **CONTEXT_LOSS** — Session hit context limit, required continuation summary
- **GAMMA_SPA_EXTRACTION** — get_page_text returns CSS noise on Gamma; had to use GraphQL workaround
- **THEME_IGNORED** — Gamma ignores hex codes in additionalInstructions; must use themeId parameter
- **STALE_DATA** — Multiple data points corrected mid-session (member counts, Evolt pricing, enzyme attribution)
- **SCOPE_CREEP_RECOVERED** — Started with 31 slides, user correctly pushed to 5-slide CEO versions

### Summary

MacBook-GREEN is Ewing's primary development Mac (macOS 26.3.1, arm64). Disk is at 96% capacity — needs cleanup. This thread was a multi-hour BioLev x Nutrishop pitch deck build spanning data research, content creation, Gamma generation, brand theming, and CEO-level compression. The fitness-industry-deck-maker skill is the primary artifact — it contains all pricing, science, and deck content as a reusable skill for future sessions. Three brand-specific CEO decks (24HF, Anytime, Life Time) were generated with proper Gamma themes and AI imagery. The ewing-registry GitHub repo is the persistent home for all skills and harvests.
