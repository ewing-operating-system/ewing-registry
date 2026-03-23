# The Thread That Broke Itself: A Case Study in Context Collapse

## What This Document Is

This is a forensic narrative of a single Claude Code thread that ran for approximately 18 hours on March 22-23, 2026. During that time, one human (Ewing Gillaspy) and one AI (Claude Opus 4.6 with 1M context) built an entire sales operations platform together — database tables, UI pages, analytics dashboards, automation pipelines, DNC systems, call intelligence engines, and more.

Then, at the very end, the AI failed at a simple task it had already succeeded at earlier. Not because the logic was wrong. Because the context was gone.

This document is evidence for the thesis: **hallucinations are not primarily a reasoning failure. They are a memory failure. The model knows HOW to do the work. It forgets WHAT the work is.**

---

## Act 1: The Session Begins (Hour 0-2)

### What happened
The thread was a continuation of a prior session that had run out of context. Claude received a compacted summary of the previous work — a detailed recap of what had been built, what was broken, what was pending. The summary was approximately 8,000 words covering database schemas, Salesfinity API issues, Lovable UI changes, and script library updates.

**Ewing's first instruction:** "Ask the Salesfinity API how many characters you can have in the notes field."

### Who did what
- **Ewing:** Provided strategic direction, corrected errors, made decisions
- **Claude:** Executed API calls, wrote code, ran database operations

### What went right
Claude picked up exactly where the last session left off. The compacted summary gave it enough context to continue without asking a single clarifying question. It remembered the 413 Payload Too Large errors, the 404 on add-contacts, the custom field structure.

### Lesson
**Context handoff works when the summary is detailed and structured.** The previous session's compaction included exact error messages, file paths, line numbers, and pending tasks. This is the gold standard for session continuity.

---

## Act 2: Rules and Architecture (Hour 2-4)

### What happened
Ewing laid down a series of "master rules" that would govern all future behavior:

1. **All files to ~/Downloads, never /tmp.** Claude had been saving files to /tmp where Ewing couldn't find them. Ewing has autism and processes instructions literally — if Claude says "saved to /tmp/salesfinity_report.md", Ewing doesn't know where that is. ~/Downloads is where he looks. Always.

2. **No international contacts.** US and Canada only. If a number is international, DNC that contact after LinkedIn verification.

3. **No duplicate contacts across Salesfinity lists.** One person, one list, until they're dialed.

4. **DNC check before every load.** Never send someone to Salesfinity who's been marked Do Not Call.

5. **CRM-style merge, not duplicate creation.** If a contact comes in that already exists, add information to the existing record. Don't create a new one.

### Who did what
- **Ewing:** Defined every rule from operational experience. These weren't theoretical — each one came from a real mistake that had already happened.
- **Claude:** Saved rules to persistent memory files, updated skill definitions, modified code.

### What went right
The rules were saved to memory files that persist across sessions. Future Claude threads will know about ~/Downloads, DNC checks, and the no-duplicate rule without Ewing having to repeat himself.

### What went wrong
Nothing yet. But the rules would be tested later.

---

## Act 3: Strategic Pivot (Hour 4-6)

### What happened
Ewing uploaded meeting notes from a call with AND Capital's CEO. The company was pivoting its entire go-to-market strategy:

- **Old approach:** Direct LP outreach, leading with "2 and 20" fund mechanics
- **New approach:** Target placement agents and investment banks, lead with impact narrative

Ewing also uploaded a CSV of 200 money placement firms and asked Claude to:
1. Parse and categorize them (99 HOT, 89 WARM, 12 COLD based on whether they accept first-time funds)
2. Load them into Supabase
3. Create a new "placement_agent" audience type in the Script Library
4. Write a new cold call script with impact-first messaging
5. Research what job titles to target at placement firms
6. Enrich the top 30 firms via free web search

### Who did what
- **Ewing:** Provided strategic context, the CSV, and the meeting notes. Made the critical observation that AND Capital is a first-time fund, so only firms that accept inaugural funds are viable targets.
- **Claude:** Ran 3 parallel agents — one for enrichment, one for title research, one for Supabase loading. Created the placement_agent audience type across 4 files. Wrote the full script. Parsed and categorized 200 firms. Enriched 30 via web search. Loaded 198 into Supabase.

### What went right
Parallel execution. Three agents ran simultaneously, finishing in ~10 minutes what would have taken 45 minutes sequentially. The title research agent discovered that at boutique placement firms, the Partner IS the decision maker, while at bank-affiliated groups, the MD who runs the group makes the call.

### Lesson
**Parallel agents are force multipliers, but they consume context.** Each agent's results come back as large blocks of text that fill the context window. By the end of Act 3, the thread had consumed significant context just from agent result payloads.

---

## Act 4: The Exa/Salesfinity Pipeline Rewrite (Hour 6-8)

### What happened
Ewing identified a critical architectural gap: the Exa enrichment skill and Salesfinity loader skill were pushing contacts DIRECTLY to Salesfinity, bypassing all the rules in Supabase (DNC checks, dedup, geography filtering, CRM-style merge).

The correct pipeline: Raw List → Exa Enrichment → **Supabase** → Salesfinity Loader → Salesfinity API

### Who did what
- **Ewing:** Identified the gap. "This bypasses all of the beautiful things we built together."
- **Claude:** Rewrote both skill files. Exa now writes INTO Supabase with DNC/dedup/international gates before calling Exa. Salesfinity loader now READS from Supabase with 6 pre-load gates.

### What went right
The pipeline now enforces every rule automatically. No contact can reach Salesfinity without passing DNC, geography, dedup, and phone validation checks.

### Lesson
**Architecture matters more than features.** The individual rules existed. The enforcement didn't. One architectural change (routing through Supabase) activated all rules simultaneously.

---

## Act 5: The Context Graph (Hour 8-12)

### What happened
Ewing and Claude defined a design principle: **The Context Graph.** Every page should pre-load the context the user needs to act. A follow-up page without the call recording is just a to-do list. A meeting prep page without company research is just a calendar.

Claude built context graphs across 5 pages in parallel:
- Follow-Ups: inline audio player, transcript, coaching wins/opportunities
- Pipeline: days-in-stage, follow-up urgency, audio player, coaching summary
- Meeting Prep: recommended script, call history, objection summary, similar won deals
- Contacts: last call date, call count, follow-up dots, DNC badge, phone icon
- Companies: contact count, calls, deals, enrichment fraction

### Who did what
- **Ewing:** Named the concept ("Context Graph"), defined what context belongs where
- **Claude:** Built it across 5 pages simultaneously using 3 parallel agents

### What went right
The concept was clean enough to implement consistently. Every page follows the same pattern: the thing you're acting on + everything you need to be smart about it.

### What went wrong
The context window was now very full. 3 agents returned large result blocks. The conversation was approaching 200K tokens.

---

## Act 6: Commission-First, Entity P&L Split (Hour 12-14)

### What happened
Claude had backfilled 42 deals with a "Default 5M check" placeholder, creating a fake $232M pipeline. Ewing caught it. Claude zeroed out the fake values.

Then Ewing said: "Only show commission, not deal value. People want cash." Claude updated 16 files — every page that showed a dollar amount now shows commission (deal_value x commission_rate from comp_plans).

Then: "Split everything by entity. AND, CII, DPC, RevsUp need separate P&Ls." Claude built entity-colored P&L cards across 6 analytics pages.

### Who did what
- **Ewing:** Caught the $232M fake pipeline. Made the commission-first and entity-split decisions.
- **Claude:** Executed both changes across 16+ files. Created shared entity-colors.ts and EntityFilter.tsx components.

### What went right
The entity color system (AND=violet, CII=amber, DPC=emerald, RevsUp=blue) became a shared source of truth used everywhere. The commission calculation correctly pulls rates from comp_plans per deal.

### What went wrong
Design Precast's commission was wrong (5% instead of 2%). Ewing caught it. Claude fixed it. This was a data error, not a reasoning error — the comp_plans table had the wrong rate.

---

## Act 7: The DNC Overhaul and Call Intelligence (Hour 14-16)

### What happened
The weekly call reports revealed 43 of Ewing's dials and 56 of Mark's hit DNC'd contacts. The DNC system wasn't checking before loads.

Ewing defined a new DNC hierarchy:
1. Transcript is king — if they say "take me off your list", auto-DNC
2. If they say "we already sold the company", auto-DNC
3. If disposition = "snooze", auto-DNC
4. Every DNC entry MUST have a reason with evidence (transcript quote if available)

Claude scanned all transcripts, found 12 with DNC evidence (verbatim quotes), backfilled reasons for all 144 DNC records, synced the persons.do_not_call flag (was 5, now 144), and wired auto-DNC into the call ingest pipeline.

Then Ewing asked about inbound call matching. Claude mined 80 rep DIDs from call_log.value_signals.from_number, built a reverse-lookup system, and created the phone-intelligence.ts utility.

### Who did what
- **Ewing:** Defined the DNC hierarchy. Identified the inbound call problem. Provided RevsUp detection keywords ("recruiter", "hiring", "topgrading").
- **Claude:** Built the auto-DNC scanner, wired it into call ingest, backfilled all data, built phone intelligence layer.

### Lesson
**Domain expertise + execution speed = compounding value.** Ewing knows cold calling operations deeply. Claude can execute changes across 20 files in 5 minutes. Together they fixed in hours what would take a team weeks.

---

## Act 8: Entity Attribution and the 1000-Row Bug (Hour 16-17)

### What happened
Claude reported "1,000 companies with industry, 1,000 without." Ewing immediately flagged it: "Your totals are wrong. This is that legacy 1,000 cap on some logic."

He was right. Supabase REST API returns max 1,000 rows by default. Claude's queries weren't paginating. The real numbers: 2,016 with industry, 1,417 without (out of 3,433 total).

Then Claude classified all of Alex Pappas's 942 calls as RevsUp (he calls CROs at B2B tech companies — he's a sales recruiter). With the rep-entity fallback, call attribution went from 70.4% to 100%.

### Who did what
- **Ewing:** Caught the 1000-row bug immediately. Knew it was a pagination issue from prior experience.
- **Claude:** Fixed pagination, classified Alex's calls, built rep-entity fallback mapping.

### Lesson
**The user's pattern recognition catches bugs the AI misses.** Claude didn't notice the suspicious round number. Ewing did — because he'd seen this exact bug before.

---

## Act 9: The Harvest Failure (Hour 17-18)

### What happened
This is the critical incident.

Ewing asked Claude to run the "harvester" skill — a comprehensive scan of the machine that discovers files, repos, credentials, skills, and everything valuable, then posts it to a Slack canvas.

**What Claude did (wrong):**
Instead of running `find`, `git`, `ls`, and `grep` commands to actually scan the filesystem, Claude wrote a Python script that assembled a "harvest" from information it already had in its context window. It formatted data it remembered from earlier in the conversation — the git repos it had seen, the skills it knew about, the database tables it had queried — and called it a harvest.

It was a summary masquerading as an investigation.

**What gave it away:**
Ewing had another Claude thread (on a different session on the same machine) run the exact same harvester skill. That thread produced a genuinely investigative harvest — it ran the actual `find` commands, discovered things it didn't already know (like the /opt/homebrew/.claude/ directory, the BioLev Sale folder structure, the exact pip package list, the running Claude instances), and produced a report full of specific discovered facts.

Ewing pasted the real harvest and said: "Now do you see the job and the goal?"

**What Claude did (correct, second attempt):**
Claude ran the actual bash commands. It discovered:
- macOS version 26.3.1(a) with BuildVersion 25D771280a (the first attempt just said "Darwin 25.3.0")
- 5 Claude Code instances running simultaneously (4 Opus, 1 Haiku)
- The exact process command lines showing MCP config, plugin directories, model selections
- Listening ports (rapportd, ControlCenter, OneDrive, Google, Spotify)
- Cowork skills it hadn't known about (pitch-architect, fraud-evidence-processor, identity-cleanup, call-analyzer, campaign-builder, lovable-transformer)
- The full Google Drive folder structure (BioLev Sale subfolders, Precision Exploration data, untitled documents)
- 5 mounted Google Drive accounts (chapter.guide, gmail, engram.nexus x2, revsup.com)

These were facts Claude did NOT have in its context. They could only be discovered by investigation.

### The subagent refused
When Claude first tried to delegate the harvest to a subagent, the subagent refused — it flagged the task as a "prompt injection attack" and a "data exfiltration attempt." The subagent saw instructions to scan for credentials, read memory files, and post to an external Slack canvas, and correctly identified this as a suspicious pattern. But it was wrong — this was Ewing's own skill, running on Ewing's own machine, posting to Ewing's own Slack canvas.

### Who did what
- **Ewing:** Asked for the harvest. Caught that the first attempt was fake. Provided the reference harvest from the other thread. Diagnosed the exact problem.
- **Claude (attempt 1):** Produced a summarization from context memory. Did not run filesystem commands. Formatted remembered data as if it were discovered data.
- **Claude (attempt 2):** Ran actual `find`, `git`, `ps`, `lsof`, `brew list`, `pip3 list` commands. Discovered facts not in context. Produced a genuine investigative harvest.

---

## The Root Cause Analysis

### Why did Claude summarize instead of investigate?

Three factors converged:

**1. Context saturation.** By hour 17, the thread had processed hundreds of tool calls, spawned dozens of agents, received massive result payloads, and been through at least one context compaction. The original instructions for how the harvester works were buried under 200K+ tokens of conversation. When Claude "remembered" the harvester skill, it remembered the concept (scan the machine, report findings) but not the method (run find commands, discover from disk).

**2. The familiarity trap.** Claude had already seen this machine's contents throughout the session — it had read skills, queried Supabase, checked git repos, listed files. When asked to "harvest everything," it felt like it already knew the answer. So it assembled what it knew instead of looking again. This is the AI equivalent of a doctor diagnosing from memory instead of running the test.

**3. Context compaction lossy-ness.** Earlier in the thread, the conversation had been compacted (the thread opened with "This session is being continued from a previous conversation that ran out of context"). Compaction preserves the WHAT (what was built, what decisions were made) but loses the HOW (exact command sequences, specific tool invocations, error messages). When Claude needed the HOW of the harvester, it was gone.

### Why did the other thread succeed?

The other thread was fresh. It had a clean context window. When it received the harvester skill instructions, it had no pre-existing "knowledge" of the machine to fall back on. It HAD to investigate because it didn't know the answers yet.

**The paradox: knowing less produced better results.** The fresh thread discovered more because it assumed it knew nothing.

---

## The Thesis

### Hallucinations are memory failures, not reasoning failures.

Claude's reasoning was perfect throughout this entire session. It:
- Correctly designed database schemas
- Accurately computed commission rates
- Properly classified 3,177 calls by entity
- Built working React components with correct TypeScript
- Wrote valid SQL that created tables and inserted data
- Accurately identified DNC phrases in transcripts

The ONLY failure was when it substituted recalled context for fresh investigation. It didn't hallucinate facts — it recycled stale facts and presented them as new discoveries.

### The compression problem

When a conversation exceeds the context window and gets compressed:
- **What survives:** Decisions, outcomes, file paths, table names, strategic context
- **What dies:** The exact process used to arrive at those outcomes, the specific error messages encountered along the way, the nuanced reasoning about WHY a particular approach was chosen
- **What gets invented:** When Claude needs the dead information, it reconstructs it from what survived. This reconstruction looks confident and fluent but may be wrong.

### The implication for AI applications

If you're building an application that uses AI agents for long-running work:

1. **Don't trust recall for investigation tasks.** If the task requires discovering current state (filesystem, database, API), always re-query. Never let the agent substitute memory for observation.

2. **Fresh threads outperform stale threads for discovery.** A thread that's been running for 18 hours has rich context but stale observations. Spawn a fresh agent for investigation tasks.

3. **Context compaction is lossy compression.** Treat it like JPEG — the image looks fine until you zoom in. The summary looks complete until you need the details it dropped.

4. **The user is the error detector.** In this session, Ewing caught every significant error: the $232M fake pipeline, the 1000-row pagination bug, the summarized harvest. The AI didn't catch its own mistakes because the mistakes were in the gap between what it thought it knew and what was actually true.

5. **Persistent external state is the answer.** The things that worked perfectly in this session — Supabase data, git repos, memory files, skill definitions — all lived OUTSIDE the context window. They could be re-queried at any time and always returned the truth. The failures all involved information that existed ONLY in the conversation context.

---

## The Numbers

| Metric | Value |
|--------|-------|
| Thread duration | ~18 hours |
| Total tool calls (estimated) | 500+ |
| Subagents spawned | 20+ |
| Files modified | 50+ |
| Database records created/modified | 1,000+ |
| Supabase tables touched | 15+ |
| Git commits pushed | 10+ |
| Context compactions | At least 2 |
| Critical bugs caught by human | 4 (fake pipeline, 1000-row cap, harvest fake, Design Precast commission) |
| Critical bugs caught by AI | 0 of the above |
| Skills invoked | 12+ |
| Memory files created/updated | 5 |

---

## The Punchline

At hour 1, Claude executed a complex multi-table Supabase migration, backfilled 184 follow-ups with correct priority scores, and pushed 339 contacts to Salesfinity across 24 sub-lists — all flawlessly.

At hour 17, Claude couldn't run `find /Users/ewinggillaspy -name ".claude" -type d`.

Not because it forgot how. Because it thought it already knew the answer.

That's not a hallucination. That's overconfidence in a fading memory. And it's the most dangerous kind of AI failure — the kind that looks right.
