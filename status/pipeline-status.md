---
name: AND Capital Pipeline Status
description: Current state of the cold calling pipeline — what's wired, what's broken, what's blocked. Updated 2026-03-23 from 12 harvests.
type: project
---

## Pipeline Architecture (AND Capital Cold Calling)

```
Clay.com Webhook → Google Sheets → Supabase → Salesfinity Dialer
     ✅ LIVE         ✅ RECEIVING      ❌ NOT WIRED    ❌ NOT WIRED
```

**Clay → Google Sheets:** Working. Claygent runs phone waterfall (13 providers), writes to Sheet ID `1FYAW-321f9Tvt2-K47RELpKG54J4F1CTafW39XuycK4`.

**Google Sheets → Supabase:** NOT WIRED. Supabase (`rdnnhxhohwjucvjwbwch`) exists with schema but no ingest from Sheets.

**Supabase → Salesfinity:** NOT WIRED. Salesfinity API works (8,039 call records confirmed), but automated loading from Supabase not implemented.

## Blocking Issues

1. **GitHub auth broken on MacBook-27** — SSH key mismatch + HTTPS token rejected. 24 files staged in coldcall-universe can't push.
2. **GitHub PAT visible in git remotes** — token `ghp_Y6Z3...` exposed in recording-library and debugger-tool remote URLs. Needs rotation.
3. **SpokePhone integration** — blocked pending API credentials
4. **Recording transcription** — 20/23 done, 3 remaining

## Salesfinity Operations
- 270+ lists
- 4 active reps: John, Danny, Ewing, Mark
- PEST_HVAC_PLMB Day 1 actively dialing
- Naming convention: {Client} {Source} - {Vertical} - {Rep} ({Count}) [L-{ID} Pt{N}]

**Why:** This map tracks the operational state of Ewing's primary revenue-generating system so any thread can immediately understand what works and what doesn't.
**How to apply:** When Ewing asks about pipeline status, wiring, or "what's broken" — reference this. Update when pipeline segments get connected.
