---
name: salesfinity-loader
description: >
  Push contacts from Supabase to Salesfinity's AI parallel dialer. This skill READS
  from Supabase (persons + phone_numbers + companies + lists + list_assignments),
  enforces all pre-load gates (DNC table, DNC flag, dedup across lists, geography,
  phone required, naming convention), and then pushes to Salesfinity via API. The
  preferred workflow is: create ONE list, then add contacts to it via the add-contact
  endpoint (up to 2,000 per list). It NEVER accepts raw contact data directly — all
  data must exist in Supabase first. Use this skill whenever the user wants to push
  to Salesfinity, create a dialing list, queue contacts for dialing, manage
  Salesfinity lists, or check call logs. Also trigger on "salesfinity", "parallel
  dialer", "dialing queue", "load into dialer", "push to dialer". The exa-enrichment
  skill writes data INTO Supabase; this skill reads it OUT. NOTE: Salesfinity also
  has an official MCP — if installed in Claude Code, it can auto-add contacts from
  CSV without manual API calls.
---

# Salesfinity Loader — Supabase → Salesfinity Pipeline

This skill reads enriched contacts FROM Supabase and pushes them to Salesfinity's AI
parallel dialer. It enforces all pre-load gates before any contact reaches Salesfinity.

## CRITICAL ARCHITECTURE RULE

```
Supabase (persons + phone_numbers + companies + do_not_call) → 6 Gates → Salesfinity API
```

**This skill's input is ALWAYS Supabase.** It queries:
- `persons` — people records with enrichment data
- `phone_numbers` — phone numbers linked to person_graph_id
- `companies` — company records for company name/vertical context
- `lists` — dialing list metadata
- `list_assignments` — person-to-list mappings with status tracking
- `do_not_call` — authoritative DNC list (separate table)

**This skill NEVER:**
- Accepts raw CSV/JSON contact files and pushes them to Salesfinity
- Skips Supabase to push contacts directly
- Creates contacts that don't exist in Supabase
- Bypasses any gate for any reason

**If the user gives you a raw list of contacts:**
1. STOP. Tell them the data needs to go through Supabase first.
2. Either use the `exa-enrichment` skill to enrich and write to Supabase,
   or write the contacts to Supabase directly (companies + persons + phone_numbers).
3. THEN come back to this skill to push to Salesfinity.

## Credentials

### Salesfinity
- **Base URL**: `https://client-api.salesfinity.co/v1`
- **API Key**: Read from ewing-connectors skill
- **Auth Header**: `x-api-key: <API_KEY>`
- **Users:**
  - Ewing: `680edc0d1504192884a148e0` (ewing@engram.nexus)
  - Mark: `68d1caac41d11ac1ce5df7a2` (mark@revsup.com)

### Supabase
- **URL:** `https://rdnnhxhohwjucvjwbwch.supabase.co`
- **Anon Key:** Read from ewing-connectors skill
- **REST API base:** `https://rdnnhxhohwjucvjwbwch.supabase.co/rest/v1`
- **Auth headers for every Supabase call:**
  ```
  apikey: <ANON_KEY>
  Authorization: Bearer <ANON_KEY>
  Content-Type: application/json
  Prefer: return=representation
  ```

## Table Schemas

**companies** (3433+ rows):
- `company_id` (uuid PK), `name`, `domain`, `website`, `vertical`
- `employee_count`, `revenue_estimate`, `year_founded`
- `city`, `state`, `country`, `location`, `source`, `calling_for`
- `industry`, `sub_vertical`
- `do_not_call` (boolean)

**persons** (4586+ rows):
- `person_graph_id` (uuid PK), `company_id` (FK)
- `first_name`, `last_name`, `full_name`, `title`
- `linkedin_url`, `email`, `personal_email`
- `state`, `city`, `timezone`, `zip`
- `source`, `source_detail`, `is_active`, `do_not_call` (boolean)
- `segment_tags`, `enrichment_status`, `calling_for`, `role_category`

**phone_numbers** (4216+ rows):
- `phone_id` (uuid PK), `person_graph_id` (FK)
- `phone_number` (e.g., "+17735752142")
- `phone_type`, `status`, `is_primary`
- `source`, `call_count`, `connect_count`

**lists** (26+ rows):
- `list_id` (uuid PK), `name`, `description`, `list_type`, `status`
- `total_persons`, `vertical_focus`, `salesfinity_id`
- `calling_for`, `contacted_count`, `connected_count`

**list_assignments** (1909+ rows):
- `assignment_id` (uuid PK), `list_id` (FK), `person_graph_id` (FK)
- `rep_id`, `position`, `status`, `priority`
- `last_attempt_at`, `attempt_count`, `next_call_after`, `notes`, `pushed_at`

**do_not_call** (authoritative DNC table):
- `id` (uuid PK)
- `person_graph_id` (FK, nullable)
- `company_id` (FK, nullable)
- `reason` (text)
- `reason_category`, `reason_text`
- `added_by` (text)
- `block_company` (boolean)
- `blocked_from_lists` (array)
- `created_at` (timestamp)

## Known Salesfinity API Pitfalls (Updated March 23, 2026 — post CEO bug fixes)

**The users endpoint is `/v1/team`, NOT `/v1/users`.** `/v1/users` returns 404.

**~~The `user` field in list responses ROTATES on every request.~~** FIXED March 2026.
The ID mismatch between list creation and list responses has been patched by
Salesfinity engineering. The `user` field should now return a stable, valid user_id.
If you still see rotating IDs, fall back to the hardcoded user_id above.

**~~413 Payload Too Large with >15 contacts per create-list call.~~** No longer the
bottleneck. Use the add-contact endpoint (`POST /v1/contact-lists/{id}/contacts`) to
load contacts after list creation. No batching of 15 required. No sub-list splitting.

**~~POST /v1/contact-lists/{id}/contacts returns 404.~~** FIXED March 2026 per
Salesfinity CEO. The add-contact endpoint works. This is now the primary method.
Docs: https://docs.salesfinity.ai/api-reference/endpoint/add-contact

**Max contacts per list: 2,000.** Only create a new list when the current one hits 2K.

**DELETE /v1/contact-lists/{id} returns 404.** Still broken. You cannot delete lists.

**Salesfinity MCP:** If installed in Claude Code, the official Salesfinity MCP can
auto-add contacts from a CSV without manual API calls. Install it for fastest workflow.

## MANDATORY PRE-LOAD GATES

These 6 gates are non-negotiable. Every contact must pass ALL 6 before being sent
to Salesfinity. Run them in order. **All gate checks happen in Supabase, not in
Salesfinity.** If ANY gate fails, that contact is SKIPPED.

### Gate 1: DNC Check — `do_not_call` Table (Person)

Query the authoritative DNC table for this person:
```
GET /rest/v1/do_not_call?person_graph_id=eq.{person_graph_id}
```

- If any row is returned → **SKIP** this person. Log reason.

### Gate 2: DNC Check — `persons.do_not_call` Flag

```
-- Already available from the main query; check the field
persons.do_not_call = true → SKIP
```

- If `do_not_call = true` on the person record → **SKIP**.

### Gate 3: DNC Check — Company

Check both the `do_not_call` table and the company record:
```
GET /rest/v1/do_not_call?company_id=eq.{company_id}
```
Also check `companies.do_not_call = true`.

- If the person's company is DNC (either source) → **SKIP**.
- Only Ewing can remove DNC status — never auto-un-DNC.

### Gate 4: Duplicate Check — No Person on Multiple Active Salesfinity Lists

```
GET /rest/v1/list_assignments?person_graph_id=eq.{id}&status=not.in.(completed,skipped)&pushed_at=not.is.null
```

- If the person already has an active list_assignment with a non-null `pushed_at`
  (meaning they were already pushed to Salesfinity and haven't completed) → **SKIP**.
- A person can be re-listed ONLY after their prior assignment status is "completed"
  or "skipped".
- No duplicates across lists, ever.

### Gate 5: Geography Check — US/Canada Only

Check the person's primary phone number:
```
GET /rest/v1/phone_numbers?person_graph_id=eq.{id}&is_primary=eq.true
```

- Phone MUST start with `+1` (US or Canada).
- Accepted Canadian area codes: 204, 226, 236, 249, 250, 289, 306, 343, 365, 367,
  382, 403, 416, 418, 431, 437, 438, 450, 506, 514, 519, 548, 579, 581, 587, 604,
  613, 639, 647, 672, 705, 709, 742, 778, 780, 782, 807, 819, 825, 867, 873, 902,
  905 (and any other valid Canadian area code).
- All other +1 area codes are US — valid.
- Any number that does NOT start with +1 → **SKIP**.
  - Set `persons.do_not_call = true` with reason "International" if confirmed international.
  - Or set `enrichment_status = 'needs_enrichment'` if the person may actually be US-based
    but has a foreign number.

### Gate 6: Phone Number Required

- Person MUST have at least one phone number in `phone_numbers` table.
- If no phone number exists → **SKIP**.
- Flag as "needs enrichment" and include in report.
- Salesfinity is a dialer — contacts without phones are useless.

### Gate Summary Report

After running all 6 gates, display this report. **Do NOT proceed without showing it
and getting user confirmation.**

```
=== PRE-LOAD GATE REPORT ===
Total contacts queried from Supabase: 150
Gate 1 — DNC table (person):         3 blocked  [names]
Gate 2 — DNC flag (person):          1 blocked  [names]
Gate 3 — DNC (company):              2 blocked  [company names]
Gate 4 — Duplicate (active list):   12 blocked  [on which lists]
Gate 5 — International phone:        2 blocked  [numbers]
Gate 6 — Missing phone:              8 blocked  [names — needs enrichment]
─────────────────────────────────────
Total blocked:                       28
✓ Passing all gates:                122

Proceed with loading 122 contacts to Salesfinity? (y/n)
```

## Custom Fields: Research-First Personalization (MOST IMPORTANT)

**Custom fields are the #1 most valuable real estate on a Salesfinity contact.** They're
what the caller SEES on screen when the phone rings. Generic pitch templates are the
fallback — custom researched intelligence is the priority.

When loading contacts, ALWAYS check if researched intel exists for this person or company.
If it does, that intel goes into custom_fields FIRST, displacing templated pitch content
if necessary. The caller needs context that makes them sound like they did homework, not
like they're reading from a script.

### Hook Priority Order (from draft-outreach skill)

Thread researched info into custom_fields in this priority:

1. **Trigger event** (funding, hiring, acquisition, news) → Most timely, highest connect
2. **Mutual connection** (shared contact, same network, same event) → Social proof
3. **Their content** (post, article, podcast, talk) → Shows you researched them personally
4. **Company initiative** (new market, product launch, strategic shift) → Relevant to priorities
5. **Role-based pain point** (common challenge for their title/vertical) → Least personal

### How to Build Research-Enhanced Custom Fields

If research data exists (from Supabase, enrichment, or web scraping), build custom_fields
like this — the researched hook REPLACES the generic "Pitch Intro":

```json
"custom_fields": [
  {"type": "string", "label": "Hook", "value": "Saw your firm just closed a $200M fund — congrats. We're launching a complementary thesis."},
  {"type": "string", "label": "Context", "value": "You placed 3 energy deals in 2025 — our O&G fund is counter-cyclical, satellite AI geology."},
  {"type": "string", "label": "Differentiator", "value": "Non-exploitative capital. Interconnected portfolio companies."},
  {"type": "string", "label": "The Ask", "value": "15-min call — see if our thesis fits your LP appetite."},
  {"type": "string", "label": "Source", "value": "PitchBook profile + LinkedIn post 3/15/26"}
]
```

**The `Hook` and `Context` fields are what make the call feel warm instead of cold.**
The caller reads these and sounds like they know the person. That's the difference
between a 2% and a 15% connect rate.

### Where Research Data Comes From

- `persons.segment_tags` — may contain enrichment insights
- `companies.industry`, `companies.sub_vertical` — firmographic context
- Supabase custom columns if research pipeline has populated them
- The `exa-enrichment` skill writes research data INTO Supabase
- The `draft-outreach` skill documents the full research methodology
- Web scraping results stored in Supabase by the engineer agent pipeline

### Rules for Research-Enhanced Custom Fields

1. **Research hook beats template pitch every time.** If you have a trigger event, use it.
2. **Source attribution matters.** Include a `Source` field so the caller knows WHERE the
   intel came from — builds their confidence that it's real and current.
3. **Keep each field under 200 chars.** The caller is scanning while the phone rings.
4. **Max 5 custom_fields per contact.** If you have both research AND pitch, prioritize:
   Hook > Context > Differentiator > The Ask > Source. Drop template fields first.
5. **Never fabricate research.** If no researched intel exists, fall back to the vertical
   pitch templates below. A generic pitch is better than a wrong hook.

---

## AND Capital Pitch Templates — Fallback (Updated March 2026)

These templates are the DEFAULT when no custom research exists for a contact. If research
IS available, replace "Pitch Intro" with a researched "Hook" per the section above.

**CRITICAL:** Never lead with "2 and 20", fund mechanics, IRR, or financial engineering.
Lead with impact, mission, differentiation, non-exploitative capital, and portfolio synergy.

### Placement Agent Pitch (Custom Fields)
```json
"custom_fields": [
  {"type": "string", "label": "Pitch Intro", "value": "AND Capital — impact-driven PE firm, two differentiated fund strategies"},
  {"type": "string", "label": "Fund 1", "value": "O&G Exploration — satellite AI geology, counter-cyclical, hard-asset floor"},
  {"type": "string", "label": "Fund 2", "value": "Wellness & Longevity — diagnostics, robotics, bioprinting, demographic tailwind"},
  {"type": "string", "label": "Differentiator", "value": "Non-exploitative capital. Portfolio companies are interconnected and synergistic."},
  {"type": "string", "label": "The Ask", "value": "Explore placement partnership — LP introductions, fundraising support"}
]
```

### iBanking Pitch (Custom Fields)
```json
"custom_fields": [
  {"type": "string", "label": "Pitch Intro", "value": "AND Capital — impact-driven PE firm seeking ibanking partnerships"},
  {"type": "string", "label": "Fund 1", "value": "O&G Exploration — satellite AI geology, counter-cyclical, hard-asset floor"},
  {"type": "string", "label": "Fund 2", "value": "Wellness & Longevity — diagnostics, robotics, bioprinting, demographic tailwind"},
  {"type": "string", "label": "Differentiator", "value": "Conviction-driven thesis. Societal outcomes plus institutional returns."},
  {"type": "string", "label": "The Ask", "value": "Deal flow, LP introductions, transaction support"}
]
```

### Direct LP Pitch (Custom Fields)
```json
"custom_fields": [
  {"type": "string", "label": "Pitch Intro", "value": "AND Capital — impact-driven PE, two thesis-driven fund strategies"},
  {"type": "string", "label": "Fund 1", "value": "O&G Exploration — satellite AI geology, counter-cyclical, hard-asset floor"},
  {"type": "string", "label": "Fund 2", "value": "Wellness & Longevity — diagnostics, robotics, bioprinting, demographic tailwind"},
  {"type": "string", "label": "Differentiator", "value": "Non-exploitative capital. Interconnected portfolio. Societal impact + returns."},
  {"type": "string", "label": "The Ask", "value": "20-min intro call — walk through thesis and diligence materials"}
]
```

### Notes Field (Short — under 50 chars, for ALL audiences)
`"notes": "AND Capital — impact PE, partnership pitch"`

**Pitch selection logic:**
- If `companies.vertical` contains "placement" → Placement Agent pitch
- If `companies.vertical` contains "ibank" → iBanking pitch
- If `companies.vertical` contains "LP" or "family_office" or "endowment" or "pension" → Direct LP pitch
- Default: Direct LP pitch

## Workflow

### Step 1: Query Supabase for Contacts to Load

The user will specify what to load. Common patterns:
- "Push the placement agents to Salesfinity"
- "Load the iBanking list"
- "Push all AND Capital contacts that are enriched"
- "Load list {list_name} to Salesfinity"

**Option A: Query by list name/ID (preferred)**
If the user references a specific list:
```
GET /rest/v1/list_assignments?list_id=eq.{list_id}&select=*,persons(*),phone_numbers(*)
```
Or join manually:
1. Get list_assignments for the list
2. For each person_graph_id, get the person + their primary phone + their company

**Option B: Query by vertical/entity/status**
Build a filtered query:
```
GET /rest/v1/persons?do_not_call=is.false&enrichment_status=in.(enriched,partial)&calling_for=eq.AND&select=*,phone_numbers(*),companies(*)
```

Filter further by vertical, timezone, etc. based on user request.

### Step 2: Run All 6 Gates

Execute gates 1-6 in order for EVERY contact returned by the query.
Build the gate report. Show it to the user. **Wait for confirmation before proceeding.**

### Step 3: Create List Records in Supabase

For contacts passing all gates, create tracking records:

#### List Naming Convention (ENFORCED — Gate 4.5)

Format: `{Entity} — {Vertical} — {Timezone Group} (v{N})`

- Use proper em-dash ( — ), not hyphen (-) or en-dash (-)
- Entity: "AND" for AND Capital, "CII" for CII
- Vertical: "Placement Agent", "iBanking", "Home Services", "Finance", "Direct LP", etc.
- Timezone groups: "ET Block 1", "ET Block 2", "CT + Intl", "PT + MT"
- Version: increment from last list with same Entity + Vertical + Timezone
- Examples:
  - `AND — Placement Agent — ET Block 1 (v3)`
  - `AND — iBanking — CT + Intl (v1)`
  - `CII — Home Services — PT + MT (v2)`
- No more sub-list splitting — the add-contact endpoint supports up to 2,000 per list.
  Only create a new version if you exceed 2,000 contacts in a timezone group.
- **NEVER create a list without this format.** If the user gives an informal name,
  reformat it to match the convention and confirm with them.
- **NEVER strip special characters.** The em-dash and + must survive encoding.

#### Group by Timezone

After gates pass, group contacts by timezone:
- `America/New_York` or state in (CT, DC, DE, FL, GA, IN, KY, MA, MD, ME, MI, NC,
  NH, NJ, NY, OH, PA, RI, SC, TN, VA, VT, WV) → **ET**
  - Split into Block 1 / Block 2 if >50 contacts
- `America/Chicago` or state in (AL, AR, IA, IL, KS, LA, MN, MO, MS, ND, NE, OK,
  SD, TX, WI) → **CT + Intl**
- `America/Denver` or `America/Los_Angeles` or state in (AK, AZ, CA, CO, HI, ID,
  MT, NM, NV, OR, UT, WA, WY) → **PT + MT**
- Unknown timezone → default to CT + Intl

#### Create Supabase Records

1. Create a `lists` record:
   ```
   POST /rest/v1/lists
   {
     "name": "AND — Placement Agent — ET Block 1 (v3)",
     "list_type": "salesfinity",
     "status": "queued",
     "calling_for": "AND",
     "vertical_focus": "placement_agent",
     "total_persons": 52
   }
   ```

2. Create `list_assignments` for each person:
   ```
   POST /rest/v1/list_assignments
   {
     "list_id": "...",
     "person_graph_id": "...",
     "status": "queued",
     "priority": 1
   }
   ```

### Step 4: Build Salesfinity Contact JSON

For each contact passing all gates, build the Salesfinity format:

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "phone_numbers": [{"type": "mobile", "number": "+14155551234", "country_code": "US"}],
  "email": "john@acme.com",
  "company": "Acme Corp",
  "title": "Managing Director",
  "notes": "AND Capital — impact PE, partnership pitch",
  "priority": 1,
  "timezone": "America/New_York",
  "custom_fields": [/* selected pitch template based on vertical */]
}
```

**Pitch field mapping:**
- `custom_fields` → selected pitch template (see templates above)
- `notes` → short version, under 50 characters
- Do NOT put pitch content in `notes` — use `custom_fields` only

**Data integrity:**
- Every field MUST come from Supabase. NEVER fabricate or guess.
- If a field is null in Supabase, leave it out of the Salesfinity payload.
- Phone number format: always `+1XXXXXXXXXX`

### Step 5: Push to Salesfinity (Create List + Add Contacts)

**Preferred workflow (2 steps, per Salesfinity CEO March 2026):**

**Step 5a: Create the list (one time)**
```bash
curl -X POST "https://client-api.salesfinity.co/v1/contact-lists" \
  -H "x-api-key: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AND — Placement Agent — ET Block 1 (v3)",
    "user": "680edc0d1504192884a148e0",
    "contacts": []
  }'
```
Save the returned list ID.

**Step 5b: Add contacts to that list (repeat as needed)**
```bash
curl -X POST "https://client-api.salesfinity.co/v1/contact-lists/{LIST_ID}/contacts" \
  -H "x-api-key: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "contacts": [... batch of contacts ...]
  }'
```
API docs: https://docs.salesfinity.ai/api-reference/endpoint/add-contact

**Max 2,000 contacts per list.** Only create a new list when the current one is full.
No more sub-list splitting with "(pt 2)", "(pt 3)" suffixes — just keep adding to
the same list.

**If >2,000 contacts for a timezone group:** Create a second list with (v{N+1}).

**Alternative: Salesfinity MCP (fastest)**
If the Salesfinity MCP is installed in Claude Code, skip the API entirely:
- Give it your CSV file
- It auto-adds contacts to the specified list
- No manual API calls needed
- Install MCP if not already present for future loads

### Step 6: Update Supabase After Push

After each successful Salesfinity API call:

1. **Update `lists` record** with the Salesfinity list ID:
   ```
   PATCH /rest/v1/lists?list_id=eq.{list_id}
   {"salesfinity_id": "RETURNED_LIST_ID", "status": "active"}
   ```

2. **Update `list_assignments.pushed_at`** for every person in this batch:
   ```
   PATCH /rest/v1/list_assignments?list_id=eq.{list_id}&person_graph_id=in.({id1},{id2},...)
   {"pushed_at": "2026-03-21T12:00:00Z", "status": "active"}
   ```

This timestamp is what Gate 4 checks — it proves the contact was pushed and prevents
duplicates across lists.

### Step 7: Confirm and Report

```
=== SALESFINITY LOAD COMPLETE ===
Lists created: 4
Total contacts pushed: 122

  AND — Placement Agent — ET Block 1 (v3):     52
  AND — Placement Agent — ET Block 2 (v3):     38
  AND — Placement Agent — CT + Intl (v3):      22
  AND — Placement Agent — PT + MT (v3):        10

Blocked by gates: 28 (see gate report above)

Supabase updates:
  list_assignments updated with pushed_at: 122
  lists records created: 4

All contacts are now queued in Salesfinity for dialing.
```

## Salesfinity API Reference

- **Base URL**: `https://client-api.salesfinity.co/v1`
- **Auth**: `x-api-key` header

### Endpoints That Work
- `POST /v1/contact-lists` — Create list (can include initial contacts)
- `POST /v1/contact-lists/{id}/contacts` — **Add contacts to existing list** (CONFIRMED WORKING March 2026 by Salesfinity CEO). Docs: https://docs.salesfinity.ai/api-reference/endpoint/add-contact. This is the preferred method — create list once, add contacts to it. Max 2,000 per list.
- `GET /v1/contact-lists` — Get all lists
- `GET /v1/team` — Get users (NOT /v1/users)
- `GET /v1/scored-calls` — AI-scored calls
- `GET /v1/dispositions` — Disposition types
- `GET /v1/analytics/overview` — Metrics

### Endpoints That DON'T Work (Known Bugs)
- `DELETE /v1/contact-lists/{id}` — Returns 404. Cannot delete lists.
- `GET /v1/users` — Returns 404. Use `/v1/team` instead.

### Contact Schema
- `first_name` (required), `last_name`, `email`, `company`, `title`
- `phone_numbers` — `[{"type": "mobile", "number": "+1...", "country_code": "US"}]`
- `linkedin`, `website`, `notes` (under 50 chars), `account`, `priority` (1-5), `timezone`
- `custom_fields` — `[{"type": "string", "label": "...", "value": "..."}]` (up to 5 for pitch)

## Managing Existing Lists

```bash
python <skill-path>/scripts/salesfinity_api.py --action get-lists
python <skill-path>/scripts/salesfinity_api.py --action get-users
python <skill-path>/scripts/salesfinity_api.py --action get-call-logs
```

## Error Handling

- **401**: API key invalid — check ewing-connectors skill.
- **400 "user_id must be object id"**: Invalid user_id. Use hardcoded ID above.
- **404 on /v1/users**: Wrong endpoint. Use `/v1/team`.
- **413 Payload Too Large**: Create list with minimal/empty contacts, then use add-contact endpoint.
- **500 on list creation**: Bad user_id. Use hardcoded IDs above or fetch from `/v1/team`. (ID mismatch bug was fixed March 2026 but if it recurs, this is likely the cause.)
- **Supabase errors**: Check anon key, check table names, check field names.

## Important Rules

1. **ALL input comes from Supabase.** NEVER accept raw files and push directly.
2. **ALL 6 gates must pass** before any contact reaches Salesfinity.
3. **Show the gate report and wait for user confirmation** before pushing.
4. **Max 2,000 contacts per list.** Use add-contact endpoint to append to existing lists.
5. **Never load a person onto multiple active lists.** Gate 4 enforces this.
6. **DNC is permanent** until Ewing manually removes it.
7. **CRM-style merge** — new data enriches existing records, never creates duplicates.
8. **Phone numbers are required** — contacts without phones are flagged, not loaded.
9. **Naming convention is enforced** — `{Entity} — {Vertical} — {Timezone} (v{N})`.
10. **Researched intel goes in custom_fields FIRST.** Pitch templates are the fallback. Notes field stays under 50 chars.
11. **Update `pushed_at` in Supabase** after every successful Salesfinity push.
12. **ALL backup files go to ~/Downloads.** NEVER write to /tmp.
13. **NEVER fabricate contact data.** Every field comes from Supabase or is omitted.
