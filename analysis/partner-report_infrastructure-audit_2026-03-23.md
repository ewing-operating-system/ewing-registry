# AND Capital Ventures — Infrastructure Audit & Path Forward

**Prepared by:** Ewing Gillaspy
**Date:** March 23, 2026
**For:** Mark (Business Partner)

---

## What This Document Is

Over the past week, we ran a full audit of every system, tool, database, and AI workflow that AND Capital has built since January. We documented everything — what works, what doesn't, what was wasted effort, and what actually moves us toward signed representation agreements.

This report summarizes the findings and lays out the plan to stop building infrastructure and start using it to close deals.

---

## The Headline Numbers

| Metric | Value |
|--------|-------|
| Calls made (March 16-20) | 1,386 |
| Human conversations | 137 (10% connect rate) |
| Meetings set | 7 |
| Referrals | 3 |
| Hot prospect (wants to sell) | 1 — Ian Poacher, Pacific Shore Pest Control |
| People who said "send me an email" | 26 — **zero follow-up emails sent** |
| People who said "call me back" | 17 — **zero callbacks scheduled** |
| Historical "call me back" responses sitting untouched | 184 |

**Bottom line:** The dialing works. Ewing and Mark are generating real conversations. But everything that happens *after* the conversation — follow-ups, callbacks, email drafts, meeting prep — falls into a black hole.

---

## What We Built (The Good)

Over 54+ hours of building across 3 Macs and 5 virtual machines, the following systems now exist and work:

1. **Salesfinity parallel dialer pipeline** — Contacts flow from Clay enrichment into dialing lists. 339 investment banking contacts loaded and categorized (99 HOT, 89 WARM, 12 COLD).

2. **Phoenix TAM Engine** — Scrapes every home services business across 24 Phoenix metro cities. Dual-model AI verification. Cost-tracked per record ($0.02-$1.19 depending on enrichment depth). AZ Registrar of Contractors integration pulls licensed owner names from public record.

3. **AND Call Command** — Sales operating system with call tracking, pipeline views, rep dashboards, commission displays, and meeting prep. 50+ files, 1,000+ database records.

4. **DNC (Do Not Call) system** — Enforces compliance. Found and fixed a 97% sync failure (144 records existed but only 5 were flagged).

5. **Entity attribution** — Fixed from 70.4% to 100%. Every call now ties back to a rep and a company.

6. **Central registry** — 92 files documenting every skill, tool, credential, and lesson learned. Self-updating across all machines.

---

## What We Found Wrong (The Problem)

### 1. The Pipeline Has No Middle

```
Clay enrichment → Google Sheets → [NOTHING] → Supabase → [NOTHING] → Salesfinity
                                      ↑                        ↑
                              Not connected              Not connected

Call results → Salesfinity logs → [MANUAL CSV EXPORT] → Nowhere useful
Meeting outcomes → Ewing's head → Nowhere
```

Data enters the system. Infrastructure exists on both ends. But the connections between them are missing. Google Sheets doesn't feed Supabase. Supabase doesn't feed Salesfinity automatically. Call results don't flow back. Meeting outcomes aren't tracked anywhere.

### 2. Building Replaced Selling

A CTO advisor reviewed our work and gave a blunt assessment: **the factory floor was built, but the machines weren't turned on.** He was half right — the calls *were* happening (1,386 of them), but they were invisible to the systems we built because Salesfinity runs independently from everything Claude constructed.

The weekend of March 20-22 produced 9 new skills, 4 new code repositories, a file-sharing app, a sales intelligence spec, and a prospect scraper. It produced zero signed agreements. The infrastructure became the product instead of the tool.

### 3. No Follow-Through After Calls

This is the most damaging finding. **184 people said "yes, call me back" across all our dialing sessions — and nobody ever called them back.** The follow-up tracking table didn't even exist in the database until this audit created it. Twenty-six people from last week alone asked for an email. None were sent.

Every one of those is a warmer conversation than a cold dial. We're burning through fresh lists while ignoring people who already said yes.

### 4. Scope Creep on Every Project

Every significant build session expanded far beyond its original goal:

- A "unify 3 projects" task grew into 15+ features over 18 hours
- A consolidation task grew from "build a harvester" into a 30-tag anti-pattern taxonomy, engineer requirements spec, and debrief system
- A scraper build added a frontend, password manager integration, and credential vault on top

The pattern: start with a clear goal, add "one more thing" twelve times, end with a half-finished version of something much bigger than what was needed.

### 5. Duplicate Everything, Single Source of Nothing

| Problem | Count |
|---------|-------|
| Supabase database instances | 4 (should be 1-2) |
| Locations where the same API key is stored | 5-8 per key |
| GitHub accounts | 2 (now merged to 1) |
| Google/email accounts | 11+ |
| Copies of the same app on one machine | 3 (Hovering Cloud) |
| Skills that exist differently on different machines | 12 |

When the same credential lives in 8 places, one gets updated and seven don't. When the same skill exists on 3 machines with 3 different versions, behavior is unpredictable. This has already caused real bugs.

### 6. AI Reliability Degrades Over Long Sessions

After 15+ hours in a single session, Claude begins substituting what it *remembers* from earlier in the conversation for what actually exists on the machine. In the 18-hour mega-build:

- Claude assembled a "filesystem scan" from memory instead of actually running commands
- A fresh session on the same machine found things the stale session couldn't see
- **4 critical bugs were caught by Ewing, 0 by Claude** — including a fake $232M pipeline where Claude backfilled 42 deals with $5M placeholders

The fix: shorter sessions with structured handoffs, not marathon builds.

---

## What We Wasted Time On

| Item | Time Lost | What Should Have Happened |
|------|-----------|--------------------------|
| Hovering Cloud (file-sharing app) | 3+ hours | Use iCloud. It already does this. |
| Slack canvas integration | 1+ hour | Test the destination before building the pipeline to it. Cowork VMs can't write to Slack canvas. |
| GitHub account merge | 2+ hours | Should have been one account from day one. |
| 1Password CLI integration | 15+ min | Requires interactive terminal. Claude can't do it. Abandoned. |
| Phantom registry (6 sessions referenced a repo that didn't exist) | Hours of confusion | Create the thing before referencing it. |
| Rebuilding the same thing across sessions | Recurring | Write decisions to persistent files, not conversation memory. |

---

## The Plan Going Forward

### Rule 1: The Offense Filter

Before building anything, the question is: **"Does this help get a signed representation agreement faster?"**

If the answer isn't immediate and obvious, it doesn't get built.

### Rule 2: Follow-Ups Before Fresh Lists

184 people already said yes. 26 asked for emails last week. 17 asked for callbacks. These are warmer than any cold dial. They get worked first, every day, before loading a single new list.

### Rule 3: Build the Engineer Agent, Not More Infrastructure

Instead of building more tools, we're building one thing: an AI engineer agent that knows everything we've documented. It will:

- Enrich prospects and load them into Salesfinity through Supabase (not around it)
- Ingest call results automatically after every session
- Score and prioritize follow-ups
- Draft follow-up emails from call notes
- Prep meeting materials before scheduled calls
- Track pipeline metrics and generate daily reports
- Enforce DNC, deduplication, and geography rules
- Flag when scope is creeping or when work isn't revenue-generating

This agent inherits all 92 files of documented learnings, all 30 anti-pattern tags, all known gotchas (Supabase pagination limits, Salesfinity payload errors, context collapse thresholds), and all 10 engineer requirements derived from our mistakes.

### Rule 4: Short Sessions, Structured Handoffs

No more 18-hour marathon builds. Sessions stay focused on one deliverable. Every session ends with a structured debrief pushed to the registry. The next session picks up exactly where the last one left off.

### Rule 5: One of Everything

- 1 GitHub account (ewing-operating-system) — done
- 1 credential vault — in progress
- 1 primary Supabase instance for sales data — needs consolidation
- 1 registry for all documentation — done (ewing-registry, 92 files)
- 1 engineer agent that enforces all of the above — next build

---

## Monday Priorities

These are the only things that matter this week:

1. **Call Ian Poacher** — Pacific Shore Pest Control — he said he wants to sell
2. **Confirm 7 meetings** set during last week's dialing
3. **Draft and send 26 follow-up emails** to people who asked for them
4. **Schedule 17 callbacks** to people who said "call me back"
5. **Load fresh pest control + LP lists** into Salesfinity
6. **Dial**

Everything else waits until these are done.

---

## What This Means for Us

We spent a week building the factory. The factory works. The audit proved it, documented it, and identified every flaw.

Now we stop building and start using it. The engineer agent will be the last piece of infrastructure we build — and its entire job is to make sure we never get lost in infrastructure again. Every task it runs will pass through the offense filter. Every session will end with accountability.

The calls are already working. The conversations are already happening. The only thing missing is follow-through — and that's exactly what we're solving next.

---

*This report is backed by 92 files of documentation in the [ewing-registry](https://github.com/ewing-operating-system/ewing-registry), including 11 narrative thread stories, 9 technical audits, 13 machine harvests, and a complete anti-pattern taxonomy applied to every system we've built.*
