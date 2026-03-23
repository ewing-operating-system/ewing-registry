# Thread Narrative: The Great File Purge

**Machine:** MacBook-GREEN
**Thread span:** 2026-03-19 through 2026-03-22
**Thread type:** Multi-day marathon session

## What Happened

Ewing asked Claude to revisit a previously-built downloads-cleaner skill, audit it, and improve it. What started as a skill review turned into a four-day file organization campaign that processed every file on three major folders: Downloads (3,525 files + 40 directories), Documents (~30 files), and Desktop (100+ files + a 4.7GB cleanup folder).

### Day 1: The Skill and the First 15

The session opened with Ewing wanting to improve his downloads-cleaner skill using his audit and prompt-refiner skills. He wanted Downloads to be permanently empty — a safe workspace during the day, cleaned automatically every 2 hours.

Claude set up a 2-hour recurring scheduled task and processed the first 15 files as a test batch. Ewing rejected the initial naming. His feedback was direct: "Your label is terrible. Why would I wanna open that file?" This became the defining constraint of the entire session — every filename must answer "why would I open this?" with specifics: page counts, call stats, participant names, meeting outcomes, target companies.

Three rewrites of the SKILL.md followed as rules crystallized through hands-on processing.

### Day 2-3: The Bulk Processing

With naming rules established, Claude processed the remaining 3,500+ files. Key operations:

- **826 contact CSVs** preserved in Master Contact Files. Ewing was emphatic: "Emails and phone numbers are expensive. We paid for them. We should not delete or lose any of them."
- **212 RevsUp files** deleted (candidates, resumes — old recruiting data)
- **13 of his mom's QuickBooks exports** auto-deleted (she'd used his computer; pattern: `{Company}_{Report}.csv` for Sidwell/Enterprise Grain entities)
- **33 installers** (.dmg/.pkg) deleted
- **27 HTML artifacts** deleted
- **79 transcripts** preserved (Fireflies, Otter.ai, Gong — never delete recordings)
- **1,674 pre-May-2025 files** bulk archived
- **8 credential files** (1Password kits, Dashlane exports, passport) secured to ~/Documents/Personal/ — local only, never Google Drive

The 40 directories each required individual assessment. Design Precast alone was 6.1GB/150 files routed to Google Drive. A 900MB Gong recordings folder from the Topia era went to Classify Later.

### Day 3-4: Documents and Desktop

Documents was straightforward: delete RevsUp candidates, secure credentials, route tax docs to personal Drive, move research articles to Third-Party Artifacts.

Desktop was messier. A 4.7GB "Desktop Cleanup" folder contained RIOT/Topia demo videos (10GB+), LLC formation docs, cold case investigation files, consulting contracts, and scattered contact CSVs. Google Drive sync hit disk space limits at 92% capacity — Claude switched to local archiving for the largest videos.

### The Harvest

After all three folders were clean, Ewing triggered a full machine harvest. Claude inventoried: 4 git repos (1 with unpushed commits), 6 local skills, 6 scheduled tasks, 18+ plugin skills, 9 MCP integrations, memory files, credentials, and running services.

## Key Decisions Made

1. **May 1, 2025 cutoff** — older files get bulk archived, not hand-sorted
2. **Two Google Drives** — business (ewing@chapter.guide) and personal (ewing.gillaspy@gmail.com) with entity-based routing
3. **Never Delete rules** — contact data, transcripts/recordings, financial/legal docs, credentials
4. **Auto-delete rules** — RevsUp candidates, mom's QuickBooks, HTML artifacts, installers, Word temp files
5. **Classify Later > wrong guess** — when ambiguous, route to holding folder
6. **`cp + rm` over `mv`** — Google Drive operations timeout with mv; copy then remove is reliable

## Anti-Patterns Observed

- **GENERIC-NAMING**: First batch used names like "Danny Shneyder Call Transcript" — no specifics about content, outcomes, or why you'd open it. Fixed after Ewing's feedback.
- **PARALLEL-CASCADE**: Parallel Bash calls to Google Drive caused cascade failures when one timed out. Fixed by going sequential for Drive operations.
- **PATH-EXPANSION**: `~/` doesn't expand inside Bash variables. Hit this multiple times before switching to full `/Users/ewingnewton/` paths.
- **DISK-FULL-SURPRISE**: Hit 92% disk capacity mid-copy on large video files. Should have checked `df -h` before attempting 10GB+ copies to Google Drive sync folder.
- **MISSING-DEPS**: `pymupdf` and `python-docx` weren't installed, blocking PDF/DOCX content reading. Should check deps before starting content-aware processing.

## What Was Built

1. **downloads-cleaner skill** (SKILL.md — ~280 lines, rewritten 3x)
2. **desktop-cleaner skill** (SKILL.md — new)
3. **2-hour recurring scheduled task** for downloads cleaning
4. **processed.log** state tracking system
5. **audit-log-2026-03-19.md** (367-line complete action log)
6. **Naming convention**: `YYYY-MM-DD — {Specifics} — {Entity}.ext`
7. **Entity routing system**: AND Capital, Next Chapter, Other Deals, CII Advisors, Personal → two Google Drives
8. **Clay CSV classification pipeline**: Detection → Classification (5 types) → Naming with row counts → Routing by deal
9. **7 new Google Drive folders** created for proper organization

## Thread Value

This thread eliminated ~3,600 files of digital debt spanning 4 years of business operations across multiple ventures (RIOT, Topia, AND Capital, Next Chapter, Design Precast, Opolee, RevsUp, PitchBlack). The automated cleaner now runs every 2 hours. The naming convention and routing rules are codified in skills that persist across sessions. Contact data worth thousands of dollars in enrichment costs was preserved and consolidated.
