# Credential Registry (Key Names Only — NEVER Values)

## Active Credentials
| Credential | Type | Referenced In | Status |
|---|---|---|---|
| ANTHROPIC_API_KEY | API Key | clawdbot-creator, mission-control, keys-and-credentials | Active, Tier 1 |
| Supabase Anon Key (sb_publishable_...) | Token | clawdbot-creator, ewing-connectors | Active |
| Supabase Service Role Key (sb_secret_...) | Token | clawdbot-creator, ewing-connectors | Active |
| Supabase DB Password | Password | clawdbot-creator | Active |
| Supabase CLI Token | Token | ewing-connectors | Active |
| Salesfinity API Key (sk_ff45...) | API Key | keys-and-credentials, salesfinity-loader, ewing-connectors, system-auditor, cold-call-workflow | Active |
| Exa.ai API Key | API Key | keys-and-credentials, exa-enrichment, ewing-connectors, cold-call-workflow, disk-cleanup | Active |
| Clay.com API Key | API Key | keys-and-credentials, ewing-connectors, cold-call-workflow | Active, $800/mo legacy plan |
| Clay.com Workspace ID | ID | keys-and-credentials | Active |
| Clay.com Webhook URL | URL | keys-and-credentials, ewing-connectors | Active |
| Google Custom Search API Key (AIzaSy...) | API Key | mission-control, GREEN memory | Active |
| Google Custom Search CX (843fa16cbc89f48b2) | ID | mission-control, GREEN memory | Active |
| Google Sheets OAuth (ewing-google-sheets) | OAuth | ewing-connectors | Active |
| Google Sheets ID (1FYAW-321f9Tv...) | ID | reference_supabase_and_call_command | Active, receiving Clay data |
| GCP Service Account Key Path | File Path | ewing-connectors, .env.example files | Active |
| GitHub Fine-Grained Tokens | Token | git remotes | Active |
| Google/Gemini API Keys (3) | API Key | keys-and-credentials | Active |

## Exposed / Needs Rotation
| Credential | Issue | Location |
|---|---|---|
| GitHub PAT (ghp_Y6Z3...) | Visible in git remote URLs | recording-library, debugger-tool on MacBook-27 |

## Placeholders (Not Yet Configured)
| Credential | Status |
|---|---|
| Apollo.io | PLACEHOLDER in keys-and-credentials |
| Instantly.ai | PLACEHOLDER in keys-and-credentials |
| Handwrytten | PLACEHOLDER in keys-and-credentials |
| SpokePhone | BLOCKED — no credentials available |

## Credential Vaults (Duplication Problem)
| Vault | Machine | Scope |
|---|---|---|
| keys-and-credentials (skill) | Mac mini | Broad — all API keys |
| ewing-connectors (skill) | MacBook-27 | Focused — Supabase, Salesfinity, Exa, Clay, Sheets |

**Action needed:** Merge into single vault.

## Duplication Map
| Key | Appears In (count) |
|---|---|
| Salesfinity API key | 5 skills |
| Exa API key | 5 skills |
| Supabase credentials | 4 skills |
| Anthropic API key | 3 skills |
| Clay credentials | 3 skills |
