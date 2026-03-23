---
name: live-site-audit
description: >
  Audit the published AND Call Command site by visiting it as a real user would.
  Checks if pages load, data renders, buttons work, navigation functions, and the
  app is alive on the web. Trigger on: "audit the live site", "check the published site",
  "is the app alive", "test the website", "check lovable", "site health check".
---

# Live Site Audit — Published App Health Check

## Published URL
**https://blank-canvas-start-6129.lovable.app/**

## What This Audit Does

Visit the published site as a normal user would — no editor, no code view, just the
finished product. Check every page, button, and data display to verify the app is
alive and functional.

## Audit Process

### Phase 1: Is It Alive?
1. Fetch the published URL
2. Check if HTML loads (not blank, not error page)
3. Check if the React app renders (look for sidebar, content area, data)
4. Check if Supabase data is flowing (real numbers, not placeholders)
5. Report: ALIVE / DEAD / PARTIALLY WORKING

### Phase 2: Navigation Check
Visit each route and verify it loads:

| Route | Page | What to Check |
|-------|------|---------------|
| `/` | Overview | 8 stat cards with real numbers |
| `/contacts` | Contacts | Table with person data |
| `/companies` | Companies | Table with company data |
| `/lists` | Lists | 22 lists showing |
| `/data-cleaner` | Data Cleaner | Health score gauge, issues table |
| `/orchestrator` | Dashboard | 7 KPI cards, rep cards, 30s refresh |
| `/orchestrator/queue` | Queue Manager | Rep cards, list table |
| `/orchestrator/dnc` | DNC Manager | Search, DNC list, scrub panel |
| `/orchestrator/decisions` | Decision Log | Timeline feed |
| `/orchestrator/create-list` | List Creator | Text input, search criteria |
| `/costs` | Cost Dashboard | Spend chart, unit economics |
| `/costs/configure` | Cost Config | Source tabs, pricing inputs |
| `/analysis` | Call Analysis | Waterfall, opener leaderboard |
| `/analysis/patterns` | Pattern Discovery | Heatmap, time grid |
| `/person/:id` | Person Record | Data blocks, shape-coded |
| `/company/:id` | Company Record | Company data, people cards |

### Phase 3: Data Verification
For pages that load, verify:
- Real data from Supabase (not 1,000 placeholders)
- Correct record counts (persons ~2,491, companies ~1,484, etc.)
- Date filtering works (today/week/month)
- No JavaScript console errors visible in page behavior

### Phase 4: Interactive Elements
Test key interactions:
- Sidebar navigation (click each item, verify page changes)
- "Ask AND" chat button (opens panel, accepts input)
- DNC search (type a name, see results)
- Data Cleaner filters (change category, severity)
- Revenue Dashboard auto-refresh (timestamp updates)

### Phase 5: Report Format

```
============================================================
AND CALL COMMAND — LIVE SITE AUDIT
URL: https://blank-canvas-start-6129.lovable.app/
Date: [timestamp]
============================================================

SITE STATUS: [ALIVE / DEAD / PARTIAL]

Pages Loading: X/17
Pages with Data: X/17
Pages with Errors: X/17

NAVIGATION:
✅ / (Overview) — loads, shows data
❌ /orchestrator — blank page
⚠️ /analysis — loads but empty (no call_analysis data)

DATA FLOW:
✅ Supabase connected
✅ Real data rendering (not placeholders)
❌ Pipeline shows $0 (expected — no deals)

INTERACTIONS:
✅ Sidebar navigation works
✅ "Ask AND" chat opens
❌ DNC search returns error

CRITICAL ISSUES:
1. [most important]
2. [next]

============================================================
```

## When to Run
- After every Lovable publish
- When the user asks "is the site alive" or "check lovable"
- As part of the weekly system audit rotation
- After fixing build errors

## How to Run
Use WebFetch to visit the published URL and each route.
Parse the HTML response to determine if the React app rendered.
Check for key DOM elements (sidebar, content, data values).
Report findings in the standard format.
