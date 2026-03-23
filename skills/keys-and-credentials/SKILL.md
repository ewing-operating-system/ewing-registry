---
name: keys-and-credentials
description: "Permanent credential vault for all ClawdBots. Store, label, timestamp, and organize every API key, token, and credential Ewing provides. This is the SINGLE SOURCE OF TRUTH. Every bot reads from here. Never ask Ewing for a key that's already stored. When Ewing gives ANY key, update this file immediately."
---

# Keys & Credentials Vault

This is the permanent, organized vault for every API key, token, password, and credential across Ewing's ClawdBot fleet. Every new session reads from here. No key gets asked for twice.

## Rules

1. **When Ewing gives you ANY key:** Add it here immediately with label, value, timestamp, and status.
2. **Before asking Ewing for a key:** Check this file first. If it's here, use it.
3. **When a key is rotated:** Mark the old one as `RETIRED` with the date, add the new one as `ACTIVE`.
4. **When a key fails (401/403):** Mark it as `CHECK` with the error date. Don't delete it — Ewing will confirm.

## Key Status Legend

| Status | Meaning |
|--------|---------|
| ACTIVE | Working, use this one |
| CHECK | Failed recently, needs Ewing to verify |
| RETIRED | Replaced by a newer key, do not use |
| PLACEHOLDER | Ewing hasn't provided this yet |

---

## Anthropic (Claude API)

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Anthropic API Key (primary) | `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` | ACTIVE | 2026-03-21 |
| Tier | Tier 1 (checking Tier 2) | — | 2026-03-21 |
| Console | https://console.anthropic.com/settings/limits | — | — |

## Google Cloud / Gemini / Maps / Custom Search

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| ClawdKing Gemini Key | `AIzaSyBdhczyRj6zEZzL37RVHlqY2cFb3Iuow_4` | ACTIVE | 2026-03-21 |
| Original Gemini Key | `AIzaSyDVx92zD1CyrGNcnfEvDZkki6BlSFrW2e4` | ACTIVE | 2026-03-21 |
| OpenClaw Google Key | `AIzaSyD163kdidmqKJUpKU03SuDnJPuYGkHYMIg` | ACTIVE | 2026-03-21 |
| Custom Search Engine ID (cx) | `b5e920909f19a4466` | ACTIVE | 2026-03-21 |
| Google Maps API Key | Same as Original Gemini Key | ACTIVE | 2026-03-21 |

**Note:** Google has 3 separate search products with separate billing. Paying for one does NOT unlock the others:
1. Gemini API with grounding (AI Studio) — 20 req/day free
2. Custom Search JSON API — 100/day free, $5/1000 paid
3. Google Search (browser) — unlimited, no API

## Supabase

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Project URL | `https://asavljgcnresdnadblse.supabase.co` | ACTIVE | 2026-03-21 |
| Anon Key | `sb_publishable_c_Y1tDzFFsePCQPmXIrelQ_dbJzRqZJ` | ACTIVE | 2026-03-21 |
| Service Role Key | `sb_secret_f5FHU9OwvXWGQV_9rXlJew_gUTHyWXr` | ACTIVE | 2026-03-21 |
| DB Password | `QYEsjk1EwMBjBzZ0` | ACTIVE | 2026-03-21 |
| Full Anon JWT | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzYXZsamdjbnJlc2RuYWRibHNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkyMjMzNTMsImV4cCI6MjA1NDc5OTM1M30.Y1tDzFFsePCQPmXIrelQ_dbJzRqZJ` | ACTIVE | 2026-03-21 |
| Full Service Role JWT | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzYXZsamdjbnJlc2RuYWRibHNlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczOTIyMzM1MywiZXhwIjoyMDU0Nzk5MzUzfQ.f5FHU9OwvXWGQV_9rXlJew_gUTHyWXr` | ACTIVE | 2026-03-21 |

## Supabase — Transcripts Project (separate account)

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Project URL | `https://asavljgcnresdnadblse.supabase.co` | ACTIVE | 2026-03-22 |
| Anon Key (JWT) | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzYXZsamdjbnJlc2RuYWRibHNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwNzU1NDksImV4cCI6MjA4OTY1MTU0OX0.M25qlAT2bOFyOUBtr7xH6fnno7FzyB4eZGyh2ZgQNQM` | ACTIVE | 2026-03-22 |
| Service Role Key (JWT) | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzYXZsamdjbnJlc2RuYWRibHNlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDA3NTU0OSwiZXhwIjoyMDg5NjUxNTQ5fQ.2CieVmMlTjzheoDElhIq831PwkTrKWmM2O-X2fTJvnE` | ACTIVE | 2026-03-22 |

**Tables:** `transcripts` (call_name, prospect_company, status, correction_count)
**Needed for:** Call transcript storage and polishing. Separate account from the M&A pipeline Supabase above.

## Exa.ai

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Exa API Key | `4ecc9c5b-a981-4002-b080-e5a5319fead3` | ACTIVE | 2026-03-21 |

**Needed for:** Phoenix TAM Engine enrichment, exa-enrichment skill, contact discovery.

## Clay.com

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Clay API Key | `f1f16b33f79964ce18e3` | ACTIVE | 2026-03-21 |
| API Base URL | `https://api.clay.com/v3` | ACTIVE | 2026-03-21 |
| Workspace ID | `211231` | ACTIVE | 2026-03-21 |
| Webhook URL | `https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-5ea2383e-221b-46a2-99cc-b3986575c7ee` | ACTIVE | 2026-03-21 |
| Plan | Legacy — 50,000 credits / $800/mo (includes API) | — | 2026-03-21 |

**Needed for:** Phoenix TAM Engine waterfall phone enrichment.

## Apollo.io

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Apollo API Key | — | PLACEHOLDER | 2026-03-21 |

**Needed for:** Future contact enrichment.

## Instantly.ai

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Instantly API Key | — | PLACEHOLDER | 2026-03-21 |

**Needed for:** Future email outreach automation.

## Salesfinity

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Salesfinity API Key | — | PLACEHOLDER | 2026-03-21 |

**Needed for:** Parallel dialer, contact loading via salesfinity-loader skill.

## Handwrytten

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| Handwrytten API Key | — | PLACEHOLDER | 2026-03-21 |

**Needed for:** Automated handwritten letter sending to business owners.

## GitHub

| Label | Value | Status | Added |
|-------|-------|--------|-------|
| GitHub Username | `clawdking1-GH` | ACTIVE | 2026-03-21 |
| Auth Method | Keyring (via `gh auth`) | ACTIVE | 2026-03-21 |

---

## Where Keys Are Deployed

When a key is added, it should be propagated to these locations:

| Location | File | What Goes There |
|----------|------|-----------------|
| Mac Mini shell | `~/.zshrc` | `export KEY_NAME=value` for all keys used by terminal tools |
| OpenClaw | `~/.openclaw/.env` | Supabase keys, Google keys |
| OpenClaw config | `~/.openclaw/openclaw.json` | Anthropic key (hardcoded) |
| Phoenix TAM Engine | `~/Projects/phoenix-tam-engine/config.py` | All keys used by the TAM engine |
| This vault | This file | ALL keys (single source of truth) |

---

## Changelog

| Date | Action |
|------|--------|
| 2026-03-21 | Vault created. Migrated all known keys from clawdbot-creator, .openclaw/.env, and config files. |
