---
name: cold-call-workflow
description: Use this skill whenever Ewing mentions daily summary, morning prep, cold calling, call review, prospect tracking, call scoring, meeting templates, daily activity, sparkline, call outcomes, number quality, prospect status, BANT, MEDDIC, daily report, or asks to review yesterday's work. This is the master orchestrator for Ewing's daily sales workflow.
version: 1.0.0
---

# Cold Call Workflow - Daily Sales Orchestrator

This skill orchestrates Ewing's complete daily sales workflow by pulling data from all connected sources, analyzing it, scoring calls, tracking prospects, and generating actionable output.

## Workflow Trigger

Run this workflow when Ewing asks for his daily summary, morning prep, or when the scheduled task fires.

## Step 1: Data Retrieval (Yesterday's Activity)

Calculate yesterday's date and pull from all sources in parallel:

### 1a. Email (Gmail MCP)
Use `gmail_search_messages` with query: `after:YYYY/MM/DD before:YYYY/MM/DD` (yesterday's date range)
- Capture: sender, subject, snippet, labels, thread IDs
- Flag emails related to prospects, meetings, follow-ups
- Identify any meeting confirmations or reschedules

### 1b. Calendar (Google Calendar MCP)
Use `gcal_list_events` with `timeMin` and `timeMax` set to yesterday, `condenseEventDetails: false`
- Capture: event title, attendees, start/end times, descriptions, meeting links
- Categorize: cold calls vs. meetings vs. internal vs. personal

### 1c. Fireflies Transcripts (Fireflies MCP)
Use `fireflies_get_transcripts` with `fromDate` and `toDate` set to yesterday
- For each transcript found, fetch full content with `fireflies_fetch` or `fireflies_get_summary`
- Extract: key topics, action items, attendee names, duration
- Score against BANT/MEDDIC framework (see references/call-scoring.md)

### 1d. SpokePhone Call Data (when API connected)
- Pull call logs via SpokePhone API
- Extract: number dialed, call duration, call outcome/disposition, recording URL, caller ID
- Cross-reference numbers against prospect database

### 1e. Salesfinity Call Data (when API connected)
- Pull call logs via Salesfinity API
- Extract: number dialed, attempts count, outcome, connect rate, list membership
- Cross-reference with prospect status tracker

### 1f. iPhone Native Calls (manual input)
- If Ewing reports calls made on native dialer, capture them manually
- Ask for: number, name, outcome, duration, notes

## Step 2: Unified Analysis

### 2a. Cross-Reference All Sources
- Match calendar events to Fireflies transcripts (by time overlap and attendees)
- Match email threads to prospects contacted by phone
- Match phone numbers across SpokePhone, Salesfinity, and prospect database
- Identify gaps: meetings without transcripts, calls without follow-up emails

### 2b. Call Outcome Classification
For each call, determine:
- **Connected**: Spoke to target prospect
- **Voicemail**: Left message
- **Gatekeeper**: Spoke to someone other than target
- **No Answer**: No pickup, no VM
- **Bad Number**: Wrong number, disconnected, fax
- **Meeting Set**: Outcome was a booked meeting
- **Callback Requested**: Prospect asked to call back at specific time
- **Not Interested**: Explicit rejection
- **Referral**: Directed to someone else

### 2c. Number Quality Assessment
For each number dialed, update the Number Quality Database:
- Mark as GOOD (reached intended prospect)
- Mark as BAD (wrong person, disconnected, fax)
- Mark as UNKNOWN (voicemail, no answer - needs more attempts)
- Mark as DNC (do not call requested)
See: data/number-quality.json

### 2d. Call Scoring (BANT + MEDDIC)
Apply scoring framework from references/call-scoring.md to any connected calls or meetings.

## Step 3: Output Generation

### 3a. Daily Summary Document
Generate a summary including:
- **Activity Counts**: calls made, connects, meetings set, emails sent
- **Sparkline Graph**: ASCII sparkline showing activity over rolling 7-day period
- **Call Outcomes Breakdown**: pie chart or table of dispositions
- **Meetings Set**: details of any new meetings booked
- **Follow-Up Tasks**: drafted emails, callback reminders, research needed
- **Number Quality Updates**: new bad numbers flagged, database stats

### 3b. Task List with Drafted Solutions
For each action item discovered:
- Draft the email reply or follow-up
- Draft the meeting invite with correct attendee info
- Draft research notes for upcoming meetings
- Set calendar appointments for callbacks
- Queue prospect list updates

### 3c. Meeting Template Drafting
When a new type of meeting is identified (first occurrence):
- Draft a meeting template based on the context
- Ask Ewing to review and refine (once per day, batch all new templates)
- Save approved templates to templates/ directory

### 3d. Sparkline Activity Graph
Track daily metrics in data/daily-metrics.json:
```
Dials:     ▁▃▅▇▅▃▁  (last 7 days)
Connects:  ▁▂▃▅▃▂▁
Meetings:  ▁▁▃▁▅▁▁
Emails:    ▃▅▇▅▃▅▇
```

### 3e. Velocity Metrics
Calculate and display:
- Dials-to-Connect ratio
- Connect-to-Meeting ratio
- Meeting-to-Opportunity ratio
- Week-over-week trends

## Step 4: Prospect Pipeline Updates

### 4a. Update Prospect Statuses
Based on call outcomes, move prospects through the pipeline:
- Cold → Attempted (first dial)
- Attempted → Contacted (connected)
- Contacted → Meeting Set (meeting booked)
- Meeting Set → Meeting Held (meeting completed)
- Meeting Held → Opportunity (qualified)
See: data/prospect-tracker.json

### 4b. Prospecting Pipeline
- Check Exa.ai websets for new enriched contacts
- Queue new prospects for Salesfinity loading
- Flag prospects needing Clay.com enrichment for waterfall

## Step 5: Present to Ewing

Present everything in a clean summary format. Ask for approval on:
1. Drafted emails and follow-ups (send or edit?)
2. Calendar appointments to create
3. New meeting templates to save
4. Prospect status changes to confirm
5. Any items needing manual input (iPhone calls, etc.)

Do NOT send emails or create calendar events without explicit approval.
