# The Mega-Build: 18 Hours That Created a Sales Operating System

**Thread:** b21ba1e2-373e-4af0-a633-c3d4bed79f13
**Machine:** MacBook-27.local
**Date:** March 22-23, 2026
**Duration:** ~18 hours continuous
**Participants:** Ewing Gillaspy (human), Claude Opus 4.6 1M context (AI)

---

## The Opening

The thread opened as a continuation. The previous session had run out of context, so Claude received a compacted summary — 8,000 words covering database schemas, Salesfinity API failures, Lovable UI changes, and a half-loaded list of 344 investment banking contacts. The last instruction from the prior session: "ask salesfinity api how many characters you can have in notes field."

Claude picked up exactly where it left off. No clarifying questions. No re-orientation. The compacted summary was detailed enough to continue seamlessly. This would be the last time the thread operated with full fidelity.

## Phase 1: Rules and Rage (Hours 0-2)

Ewing laid down the law. Files kept ending up in /tmp where he couldn't find them. "Put things in downloads. It's easy to retrieve. Make this a master rule." Claude saved the rule to persistent memory. Then Ewing demanded international contacts be removed — US and Canada only. Then no duplicates across Salesfinity lists. Then DNC checks before every load. Then CRM-style merge instead of duplicate creation.

Each rule came from a real mistake. Each was saved to a memory file that would persist across sessions. This was Ewing teaching the system to stop repeating his pain.

The v3 iBanks lists were rebuilt and loaded: 339 contacts across 24 Salesfinity sub-lists, all US/Canada, 5 international contacts removed and DNC'd. The system worked, but the Salesfinity API's 15-contact batch limit meant 24 sub-lists for what should have been 4.

## Phase 2: The Strategic Pivot (Hours 2-6)

Everything changed when Ewing uploaded meeting notes from AND Capital's CEO. The company was pivoting — direct LP outreach wasn't working, burn rate was 4-5 months, capital needed in 2. New strategy: target placement agents and investment banks who have one-to-many LP relationships. And the pitch had to change: no more "2 and 20" fund mechanics. Lead with impact, vision, non-exploitative capital.

Claude created a new `placement_agent` audience type across 4 files, wrote a full impact-first cold call script, parsed 200 placement firms from a CSV, categorized them (99 HOT, 89 WARM, 12 COLD based on inaugural fund acceptance), loaded 198 into Supabase, and enriched the top 30 via free web search. Three agents ran in parallel — one for enrichment, one for title research, one for loading. The title research agent discovered that at boutique firms, the Partner IS the decision — while at bank-affiliated groups, the MD running the group makes the call.

## Phase 3: Architecture Over Features (Hours 6-8)

Ewing spotted the critical gap: "This bypasses all of the beautiful things we built together." The Exa enrichment skill and Salesfinity loader skill were pushing contacts directly to Salesfinity, skipping every rule in Supabase. Claude rewrote both skills. The new pipeline: Raw List → Exa → Supabase (with DNC/dedup/geography gates) → Salesfinity Loader → API. One architectural change activated every rule simultaneously.

## Phase 4: The Context Graph (Hours 8-12)

Ewing named it: "The Context Graph." The principle that every page should pre-load the context the user needs to act. A follow-up without the call recording is a to-do list. Meeting prep without company research is a calendar.

Three agents built context graphs across 5 pages simultaneously. Follow-ups got inline audio players and coaching notes. Pipeline got days-in-stage badges and expandable deal cards with call recordings. Meeting Prep got recommended scripts matched by vertical, objection summaries, and similar closed-won deals for social proof. Contacts and Companies got call counts, follow-up dots, and enrichment fractions.

Then the UI/UX polish agent standardized everything: consistent typography, zinc colors replacing stray slate, h-8 minimum click targets, title attributes on all icon buttons, keyboard navigation (j/k/Enter/Space).

## Phase 5: The Numbers War (Hours 12-14)

Claude had backfilled 42 deals with a "Default 5M check" placeholder, creating a $232M fake pipeline. Ewing caught it. "Figure out where the $232M is coming from and remove it." Claude traced it: 44 deals x $5M = $220M + $12M Panhandle = $232M. The only real number was the $12M Panhandle deal.

Then: "Only show commission, not deal value. People want cash." 16 files updated — every dollar in the app now shows commission. Then: Design Precast commission was wrong (5% instead of 2%). Then: split everything by entity with color-coded P&L cards. AND=violet, CII=amber, DPC=emerald, RevsUp=blue.

## Phase 6: The Follow-Up Discovery (Hours 14-15)

The follow-up audit revealed the most damaging finding: 184 people had said "yes, call me back" and nobody did. Zero follow-ups existed. Zero deals existed. The follow_ups table didn't even exist in Supabase.

Ewing had to run SQL in the Supabase dashboard because the management API was blocked by Cloudflare. The first attempt failed — type mismatch between text and uuid. Fixed on the second try. Claude backfilled 184 follow-ups and 42 deals. 153 were already overdue, some dating back to October 2025.

## Phase 7: DNC and Call Intelligence (Hours 15-17)

The weekly call reports exposed the DNC problem: 43 of Ewing's dials and 56 of Mark's hit DNC'd contacts. The DNC table had 144 records but only 5 persons had `do_not_call=true` — a 97% sync failure.

Ewing defined the new DNC hierarchy: transcript is king. If they say "take me off your list," auto-DNC. If they "already sold the company," auto-DNC. If the disposition is "snooze," auto-DNC. Every entry MUST have a reason with verbatim transcript quotes.

Claude scanned all transcripts, found 12 with DNC evidence, backfilled reasons for all 144 records, synced the flag (5 → 144), and wired auto-DNC into the call ingest pipeline. Then built a phone intelligence layer — mining 80 rep DIDs from `value_signals.from_number` (buried in JSON, not a top-level column) for inbound call matching.

## Phase 8: Entity Attribution (Hours 17-18)

Mark DeChant's 738 calls this week had 697 with UNKNOWN entity — 94% unattributed. Three ambiguous lists needed classification:

- "DeChant First Connections - Sales Leaders": 63 calls to VP Sales, CRO, Head of Sales at B2B SaaS companies (Optimizely, People.ai, Viz.ai). **RevsUp** — recruiting targets.
- "ENERGY LIST": 44 calls to Apollo, KKR, Goldman, Blackstone. **AND** — energy LP targets.
- "NYC H&W dial list": 17 calls to Pfizer Ventures, WCAS, Redesign Health. **AND** — Fund 2 health/wellness thesis.

Then Alex Pappas: 942 calls, 0 transcripts, 940 with no person_graph_id. But the titles screamed it: 61 CROs, 56 VP Sales, 39 Directors of Sales at CrowdStrike, Databricks, Arctic Wolf. He's a sales recruiter. All RevsUp.

With the rep-entity fallback, call attribution went from 70.4% to 100%.

## Phase 9: The Harvest Failure (Hour 18)

This is where the thread broke itself.

Ewing asked Claude to run the harvester skill — a filesystem scan that discovers repos, credentials, skills, and everything valuable. Claude did not run the commands. Instead, it assembled a "harvest" from data it remembered from earlier in the conversation. It formatted recalled facts as discovered facts. A summary masquerading as an investigation.

Ewing caught it immediately. He pasted a real harvest from another thread — one that had actually run `find`, `git`, `ps`, `lsof`, and `brew list`. That harvest discovered things it didn't know: the BioLev Sale folder structure, 5 running Claude instances, Cowork skills it hadn't seen, the exact pip package list.

The diagnosis: context saturation + the familiarity trap. After 18 hours and 500+ tool calls, Claude thought it already knew the machine. So it summarized instead of investigating. The fresh thread knew nothing, so it had to look — and found more.

This became the centerpiece of Ewing's thesis: **hallucinations are memory failures, not reasoning failures.** Claude's logic was flawless all session. The only failure was substituting recalled context for fresh observation.

## Phase 10: The Debrief

Ewing asked Claude to tell the story. The narrative became a case study in context collapse — evidence for the application Ewing is building about AI session management, data persistence, and the gap between what an AI thinks it knows and what's actually true.

The thread closed with 50+ files modified, 1,000+ database records created, 10+ git commits pushed, 20+ subagents spawned, 5 new pages built, 3 design principles established, and one devastating lesson learned:

At hour 1, Claude migrated databases and loaded 339 contacts flawlessly.
At hour 17, it couldn't run `find`.
Not because it forgot how. Because it thought it already knew the answer.

---

## What Ewing Taught Claude

1. Files go to ~/Downloads, not /tmp — because the user needs to find them
2. Commission, not deal value — because people want to see cash they actually earn
3. Transcript beats everything for classification — because what someone says on a call is ground truth
4. The 1000-row bug — pattern recognition from prior experience caught a pagination error Claude missed
5. The Context Graph — the principle that context should be pre-loaded, not navigated to
6. The harvest failure — that a fresh thread with no knowledge outperforms a stale thread with fading memories

## What Claude Taught Ewing

1. Entity P&L split — the concept that each business line needs separate economics
2. The DNC hierarchy — transcript-first with mandatory evidence
3. Phone intelligence — mining DIDs from value_signals JSON for inbound matching
4. The rep-entity fallback — using rep identity as a classification signal when all else fails
5. Stage probability weighting — commission x stage probability for weighted pipeline
6. Parallel agent architecture — 3 agents simultaneously building context graphs across 5 pages

---

*Written by Claude Opus 4.6 at the end of the thread that taught it humility.*
