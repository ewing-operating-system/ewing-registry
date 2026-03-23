# Harvest v2: clever-keen-noether — 2026-03-22 23:25 UTC (Deep Scan)

Broad scan of entire filesystem (/, /tmp, /opt, /var, /sessions). No hardcoded paths. maxdepth 8.

## Machine Info
| Field | Value |
|---|---|
| Hostname | claude |
| OS | Ubuntu 22.04.5 LTS |
| Kernel | Linux 6.8.0-94-generic aarch64 |
| User | clever-keen-noether |
| Home | /sessions/clever-keen-noether |
| Type | Cowork ephemeral VM |
| Account | ewing@engram.nexus (org dd4b8c7a-98b6-41d7-b013-f3f4ffdd1189) |
| Disk Root | 9.6G (77% used) |
| Disk Sessions | 9.8G (2% used) |
| Disk Bind mount | 229G (33% used) — this is the Mac mini's disk |

## .claude/ Directories Found (2)

### Location 1: /sessions/clever-keen-noether/mnt/.claude/ (bind-mounted from host Mac)
- .claude.json, CLAUDE.md, backups/, plans/ (empty), plugins/ (blocklist.json), projects/ (1 session JSONL), session-env/, shell-snapshots/

### Location 2: /sessions/clever-keen-noether/.claude/ (session-local)
- settings.local.json only. Permissions allow slack_update_canvas.

## CLAUDE.md (Full Contents)
- When I prompt you, use prompt skill, always
- When you tell me to do something, use output skill always
- When i'm creating a new skill, use skill creator skill, always
- Tell me if this is not understood.

## Connected MCP Tools (Full Enumeration)

### Gmail (mcp_44567b80)
gmail_search_messages, gmail_read_message, gmail_read_thread, gmail_create_draft, gmail_get_profile, gmail_list_drafts, gmail_list_labels

### Slack (mcp_ec43e366)
slack_send_message, slack_send_message_draft, slack_schedule_message, slack_search_public, slack_search_public_and_private, slack_search_channels, slack_search_users, slack_read_channel, slack_read_thread, slack_read_user_profile, slack_create_canvas, slack_read_canvas, slack_update_canvas

### Google Calendar (mcp_b5e9f0da)
gcal_list_events, gcal_list_calendars, gcal_get_event, gcal_create_event, gcal_update_event, gcal_delete_event, gcal_respond_to_event, gcal_find_my_free_time, gcal_find_meeting_times

### Google Drive (mcp_c1fc4002)
google_drive_search, google_drive_fetch

### Fireflies (mcp_3c523281)
fireflies_fetch, fireflies_get_transcript, fireflies_get_transcripts, fireflies_get_summary, fireflies_search, fireflies_get_user, fireflies_get_user_contacts, fireflies_get_active_meetings, fireflies_list_channels, fireflies_get_channel, fireflies_get_usergroups, fireflies_move_meeting, fireflies_share_meeting, fireflies_revoke_meeting_access

### Claude in Chrome
navigate, read_page, get_page_text, computer, form_input, find, javascript_tool, read_console_messages, read_network_requests, gif_creator, file_upload, upload_image, resize_window, shortcuts_execute, shortcuts_list, switch_browser, tabs_create_mcp, tabs_close_mcp, tabs_context_mcp

### Presentation Generator (mcp_969f118c)
generate, get_themes, get_folders

### Scheduled Tasks
create_scheduled_task, list_scheduled_tasks, update_scheduled_task

### Session Info
list_sessions, read_transcript

### Cowork
present_files, request_cowork_directory, allow_cowork_file_delete

### MCP Registry
search_mcp_registry, suggest_connectors

### Plugins
search_plugins, suggest_plugin_install

## Credential References in Skills

### clawdbot-creator (full vault)
- Anthropic API Key (sk-ant-api03-MX3p...TQAA) — ACTIVE, Tier 1
- Google/Gemini API Keys (3 referenced)
- Google Custom Search Engine ID
- Supabase Project URL (asavljgcnresdnadblse.supabase.co)
- Supabase Anon Key, Service Role Key, DB Password, JWTs
- Exa.ai API Key
- Clay.com API Key + Workspace ID + Webhook URL (Legacy plan, 50K credits/$800/mo)
- Apollo.io (PLACEHOLDER)
- Instantly.ai (PLACEHOLDER)
- Salesfinity (PLACEHOLDER)
- Handwrytten (PLACEHOLDER)
- GitHub: clawdking1-GH (keyring/gh auth)

### exa-enrichment
- x-api-key header for Exa.ai Websets API

### salesfinity-loader
- x-api-key header for Salesfinity client API

### mission-control
- Supabase DB URL

## Installed Tools
| Tool | Version |
|---|---|
| Node.js | v22.22.0 |
| npm | 10.9.4 |
| Python | 3.10.12 |
| pip | 25.3 |
| Git | 2.34.1 |
| Java | OpenJDK 11.0.30 |
| Ruby | 3.0.2 |
| ffmpeg | installed |
| jq | 1.6 |
| ripgrep | 13.0.0 |
| curl | 7.81.0 |
| wget | 1.21.2 |

NOT installed: docker, gh, kubectl, terraform, flyctl, vercel, supabase CLI, cargo, rustc, go, ollama, sqlite3, psql

## Notable Python Packages (90+)
beautifulsoup4, camelot-py, graphviz, imageio, lxml, magika, markdownify, markitdown, matplotlib, numpy, opencv-python, openpyxl, pandas, pdfminer.six, pdfplumber, pikepdf, pillow, pytesseract, python-docx, python-pptx, reportlab, seaborn, tabula-py, unoserver, xlsxwriter, Wand

## Running Services (18 systemd)
coworkd, cron, dbus, getty, irqbalance, multipathd, packagekit, polkit, rsyslog, serial-getty, snapd, ssh, journald, logind, resolved, timesyncd, udevd, unattended-upgrades

Listening ports: 53 (systemd-resolved), 22 (ssh)

## Databases
None local. Remote: Supabase at asavljgcnresdnadblse.supabase.co (per mission-control skill)

## Summary
Ephemeral Cowork VM with bind-mount to Mac mini (229G, 33% used). 21 skills, 11 MCP servers, 90+ Python packages. Full credential vault accessible via clawdbot-creator skill. No persistent state — everything on host Mac.
