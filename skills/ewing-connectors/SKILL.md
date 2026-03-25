---
name: ewing-connectors
description: "Unified API credential vault. Single source of truth for all service credentials including Supabase (live and old), Salesfinity, Exa.ai, Clay, Google Sheets service accounts, and Lovable project IDs. Stores base URLs, auth headers, user IDs, workspace IDs, and webhook URLs. Claude checks here before ever asking Ewing for a key."
---

# Ewing Connectors — Unified Credential Store

All API keys and credentials for Ewing's integrated services. **Check here first before asking Ewing for any key.**

## Supabase (Live Database — AND Call Command)

- **Project ID:** `rdnnhxhohwjucvjwbwch`
- **URL:** `https://rdnnhxhohwjucvjwbwch.supabase.co`
- **Anon Key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkbm5oeGhvaHdqdWN2andid2NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM4NzI3MzYsImV4cCI6MjA4OTQ0ODczNn0.SZJlQgqtAtdF11CDGofgkF-tz_2W2bCQx3q4hpGRlPU`
- **Service Role Key (Secret):** `sb_secret_SvETD7BujnizJJcE5xB1Sg_YhFX0l03`
- **CLI Access Token:** `sbp_9e7c8ccca6a0d3c09c50ab3d569da2425e231800` (added 2026-03-19)

## Supabase (Old Project — Reference Only)

- **Project ID:** `lhmuwrlpcdlzpfthrodm`
- **URL:** `https://lhmuwrlpcdlzpfthrodm.supabase.co`
- **Anon Key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxobXV3cmxwY2RsenBmdGhyb2RtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM3MjQxNzQsImV4cCI6MjA4OTMwMDE3NH0.dcedlyfYYW25i5imrpzY0NjrwK2A0CH4U65bvaRVJqE`

## Salesfinity (AI Parallel Dialer)

- **Base URL:** `https://client-api.salesfinity.co/v1`
- **API Key:** `sk_ff45bc29-e5c1-4a3f-b1e5-f9776d94cbe7`
- **Auth Header:** `x-api-key: <API_KEY>`
- **Users:**
  - Ewing: `680edc0d1504192884a148e0` (ewing@engram.nexus)
  - Mark: `68d1caac41d11ac1ce5df7a2` (mark@revsup.com)
- **Key Endpoints:**
  - `GET /v1/scored-calls` — AI-scored calls (use instead of /call-logs)
  - `GET /v1/contact-lists` — All lists
  - `POST /v1/contact-lists` — Create list
  - `GET /v1/dispositions` — Disposition types
  - `GET /v1/analytics/overview` — Metrics

## Exa.ai (Contact Enrichment)

- **API Key:** `4ecc9c5b-a981-4002-b080-e5a5319fead3`
- **Search URL:** `https://api.exa.ai/search`
- **Websets URL:** `https://api.exa.ai/websets/v0/websets`

## Clay.com (Enrichment Platform)

- **API Key:** `f1f16b33f79964ce18e3` (added 2026-03-19)
- **API Base URL:** `https://api.clay.com/v3`
- **Workspace ID:** `211231`
- **Webhook URL:** `https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-5ea2383e-221b-46a2-99cc-b3986575c7ee`

## Google Sheets

- **Clay Sheet ID:** `1FYAW-321f9Tvt2-K47RELpKG54J4F1CTafW39XuycK4`
- **Tab:** `Pushed From Clay`
- **Service Account:** `and-call-command-sheets@and-capital-coldcall.iam.gserviceaccount.com`
- **SA Key Path:** Check `/Users/ewinggillaspy/Downloads/and-capital-coldcall-205c63f2d6c9.json`

## Lovable (Frontend App)

- **Project ID:** `cd956a91-3866-4da3-8f18-bd3f6d085dbd`
- **Old Project ID:** `8724256f-b75a-45e9-bbc0-fab38cf80322`
- **App URL:** `https://and-call-command.lovable.app`
- **Alt URL:** `https://blank-canvas-start-6129.lovable.app/`
- **GitHub:** `ewing-operating-system/blank-canvas` (local clone: `/tmp/lovable-deploy/`)

## Client Codes

- **CII:** Trade businesses (home services)
- **AND:** AND Capital (banking/PE)
- **DPC:** Design Precast (concrete)

## Reps

| Name | Email | Role |
|------|-------|------|
| Ewing Gillaspy | ewing@chapter.guide | Caller |
| Mark Dechant | mark@revsup.com | Caller |
| Danny Shneyder | danny@revsup.com | Caller |
| John Kelly | john@andcapitalventures.com | Caller |
| Sarah Avdeeff | sarah@andcapitalventures.com | Caller |
| Jaiera Braswell | jaiera@andcapitalventures.com | Caller |

---

## How to Use

When any skill or script needs credentials:

1. Read this file first
2. Use the appropriate key directly
3. If a key is missing, ask Ewing to provide it and update this file

When Ewing provides a new API key:
1. Add it to the appropriate section above
2. Note the date it was added
