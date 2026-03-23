# Technical Audit: File Cleanup Session

**Thread ID:** d15908b5-96f6-47f8-ae8d-964814a689ef
**Machine:** MacBook-GREEN
**Date range:** 2026-03-19 to 2026-03-22
**Duration:** ~4 days (multi-session)

## Scope

| Location | Files In | Files Out | Status |
|---|---|---|---|
| Downloads | ~3,525 files + 40 dirs | 1 file + 1 artifact | CLEAN |
| Documents | ~30 actionable files | Only active/intentional items | CLEAN |
| Desktop | ~100+ files + 4.7GB folder | iCloud placeholder + system dirs | CLEAN |

## Actions Taken

### Moves (to Google Drive — business)
- 85 individually renamed files → entity-specific folders
- 826 contact CSVs → Master Contact Files
- 79 transcripts → Classify Later
- 82 media files → Classify Later
- 517 post-May misc → Classify Later
- 1,674 pre-May misc → Downloads Archive Pre-May-2025
- 14 directories → various Google Drive destinations
- ~20 RIOT/Topia videos → Classify Later (10GB+)

### Moves (to Google Drive — personal)
- 6 tax documents → Tax Documents folder

### Moves (to local)
- 8 credential files → ~/Documents/Personal/
- 3 LLC formation directories → ~/Documents/Personal/
- 1 MRI CD → ~/Documents/Personal/
- ~10GB videos → ~/Documents/Desktop-Cleanup-RIOT-Topia-Videos-Pre-2025/ (disk space constraint)

### Deletes
- 212 RevsUp files (candidates, resumes, scoring)
- 27 HTML artifacts
- 33 DMG/PKG installers (Claude.dmg, TeamViewer.dmg, ChatGPT Atlas, etc.)
- 13 mom's QuickBooks exports (Sidwell, Enterprise Grain)
- ~15 duplicate files
- 4 intermediate blueprint directories
- 12 Snagit .snagx files
- 8 RevsUp candidate PDFs from Documents
- 6 screenshots from Desktop
- ~28 macOS alias files, .webloc, .textClipping files
- Word temp files (~$ prefix) — auto-deleted by scheduled task

### Folders Created
- `05 - Other Deals/20 - Opolee ERP/`
- `Classify Later/`
- `Classify Later/Master Contact Files/`
- `Classify Later/Downloads Archive Pre-May-2025/`
- `~/My Drive (ewing.gillaspy@gmail.com)/Tax Documents/`
- `~/Documents/Personal/`
- `~/Documents/Desktop-Cleanup-RIOT-Topia-Videos-Pre-2025/`

## Skills Created/Modified

### downloads-cleaner (created + rewritten 3x)
- Path: `~/Documents/Claude/Scheduled/downloads-cleaner/SKILL.md`
- Size: ~280 lines
- Features: entity routing, Clay CSV pipeline, content-aware naming, Never Delete rules, auto-delete rules, Google Drive timeout handling
- State: `processed.log` (53 entries), `audit-log-2026-03-19.md` (367 lines)

### desktop-cleaner (created)
- Path: `~/Documents/Claude/Scheduled/desktop-cleaner/SKILL.md`
- Features: 30-day auto-archive, active-work protection, large file eviction, same entity routing

### Scheduled task
- Downloads cleaner runs every 2 hours
- Has auto-processed: TeamViewer.dmg, Word temp files, duplicate PDF — all logged in processed.log batches 3-6

## Errors Encountered and Resolutions

| Error | Resolution |
|---|---|
| Google Drive `mv` timeout on large files/deep paths | Use `cp + rm` instead of `mv` |
| Google Drive `mv` timeout on specific folders (GeoSense, Training Materials) | Try parent folder; shorten filename |
| `pymupdf` not installed — can't read PDFs | `pip3 install pymupdf` |
| `python-docx` not installed — can't read DOCX | `pip3 install python-docx` |
| `~/` not expanding in Bash variables | Use full path `/Users/ewingnewton/` |
| Parallel tool calls cascade when one fails | Run Google Drive ops sequentially |
| Disk at 92% (7.6GB free) during video copy | Stop sync copies; archive locally instead |
| Sandbox blocks `ps`, `lsof`, `grep`, `head` in harvest | Use alternative commands or skip |

## Risk Items

1. **Disk at 96% full** — 850GB/926GB used. Need to offload ~10GB of RIOT/Topia videos from local archive to Google Drive via web upload.
2. **coldcall-universe has 3 unpushed commits** on v2-overnight-build branch. Should be pushed.
3. **Classify Later folder** has ~2,300 files that need eventual human review.
4. **Master Contact Files** has 826+ CSVs that should be deduplicated and consolidated into a single master contact database.
5. **overwatch repo** has untracked files but zero commits — appears abandoned. Should be deleted or initialized.

## Naming Convention Established

**Format:** `YYYY-MM-DD — {Specifics} — {Entity}.ext`

**Specifics must answer:** "Why would I open this?"

| Bad | Good |
|---|---|
| contact-list (9).csv | 2025-12-18 — Salesfinity Call Log 91 Calls — Opolee OilGas and Precast VPs COOs — 2 Meetings 4 Callbacks.csv |
| Design-Precast-Pipe-Next-Chapter.pdf | 2025-12-16 — Fireflies 60pg — Dechant Pipeline Review for Chris Fore — 49 Targets 14 Active — Design Precast.pdf |
| unified_deck.pdf | 2025-12-01 — CII Partnership Overview Deck 30pg — Deal Structures EBITDA Ranges Fee Logic.pdf |

## Entity Routing Map

| Entity | Google Drive Path | Drive Account |
|---|---|---|
| AND Capital | 02 - AND Capital/ | ewing@chapter.guide |
| Next Chapter | 01 - Next Chapter Main Docs/ | ewing@chapter.guide |
| Design Precast | 05 - Other Deals/04 - Design Precast/ | ewing@chapter.guide |
| Opolee | 05 - Other Deals/20 - Opolee ERP/ | ewing@chapter.guide |
| CII Advisors | 03 - CII Advisors/ | ewing@chapter.guide |
| Cold Calling | 12 - Cold calling project/ | ewing@chapter.guide |
| Research | 08 - Third-Party Artifacts - Research/ | ewing@chapter.guide |
| Personal | ~/Documents/Personal/ | LOCAL ONLY |
| Tax | Tax Documents/ | ewing.gillaspy@gmail.com |
