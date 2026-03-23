# Story: The Google Sheets Sync Skill — 2026-03-23

## The Thread

Ewing opened the thread on the Mac mini with a clear vision: he wanted to build a skill that would turn Google Sheets into a human-in-the-loop interface between himself and ClawdBot. The idea was elegant — ClawdBot would push research data and findings to Google Sheets, Ewing would review and augment the data (approve, reject, add notes, pick values), and ClawdBot would read those decisions back. No more terminal-only interaction. A proper two-way feedback loop with a spreadsheet as the shared workspace.

He framed it not just as a personal tool but as a **reusable package** — something any team member could configure and plug into their own ClawdBot setup. A "base install package." He specified that every sheet or folder created should auto-share with mark@chapter.guide and Ewing@chapter.guide, the two people who matter.

## The Planning Phase

Claude responded with a structured set of nine questions — infrastructure, data flow, human-in-the-loop UX, sync timing, and package scope. This was the right move. The skill was ambitious enough that jumping straight to code would have been a mistake. The questions covered:

1. Google Cloud project and auth method (service account vs OAuth)
2. Supabase instance — new or existing
3. What data flows to sheets (examples needed)
4. Sync direction and timing (polling vs on-demand vs both)
5. Sheet structure (per-project tabs vs master sheet)
6. The review pattern (ClawdBot fills columns A-F, human fills column G)
7. Auto-creation of sheets vs pre-made
8. Package format (Python module, skill file, or both)

Ewing answered question 1: "Yes I do, and you helped me do it." He confirmed the Google Cloud project existed.

## The Discovery

Claude pulled the keys-and-credentials vault to find what was already configured. The vault was comprehensive — Anthropic, Google (Gemini, Maps, Custom Search), Supabase, Exa.ai, Clay, GitHub — but the critical piece was missing: **no Google Sheets service account JSON file existed on this machine.** The Google API keys in the vault were for Gemini/Maps/Custom Search, not for Sheets API access.

A `find` command across the entire home directory confirmed it: no `*service*account*.json`, no `*credentials*.json`, nothing. The Google Cloud project existed (Ewing was right about that), but the specific credential file needed for programmatic Sheets access had never been generated, or it lived on a different machine.

## The Pivot

Claude laid out the blocker clearly: service account JSON is required, here are your two options (create one in Google Cloud Console or transfer from another machine). Then re-asked the remaining 8 questions with a "you decide" escape hatch for any Ewing didn't care about.

Before Ewing could answer the remaining questions, he called for a debrief. The thread was being closed.

## What Was Accomplished

This was a **planning-only thread**. No code was written. No skill was created. But the groundwork was laid:

- The **vision** is documented: Google Sheets as a human-in-the-loop interface between ClawdBot and Ewing
- The **architecture questions** are defined: 9 specific decisions that need answers before building
- The **blocker** is identified: no Google Sheets service account JSON on this machine
- The **credential vault** was reviewed and confirmed complete for everything except Sheets
- The **auto-share defaults** are locked: mark@chapter.guide and Ewing@chapter.guide on everything

## Emotional Arc

This was a short thread — energetic opening with a big vision, followed by methodical scoping, followed by a hard stop when the credential blocker was found. No frustration. Ewing pivoted to debrief cleanly. The thread had the feel of "planting a flag" — Ewing knew what he wanted, got the questions documented, and will return to finish when the service account is ready.

## Who Taught Whom

- **Ewing taught Claude:** The vision for Sheets as an interface, the team packaging requirement, the auto-share defaults
- **Claude taught Ewing:** The distinction between Google API keys (Gemini/Maps) and Google Sheets service account credentials — they're not the same thing

## Tools and Skills Touched

- **Skills triggered:** keys-and-credentials, debrief, skill-sync
- **Tools used:** Bash (machine scanning), Glob (file search), Read (credential vault)
- **APIs checked:** Supabase REST API (tables query failed — JWT may need rotation)
- **Repos scanned:** phoenix-tam-engine, hovering-cloud, clawdbot-pipeline, ewing-registry
- **No files created or modified** (until debrief outputs)
