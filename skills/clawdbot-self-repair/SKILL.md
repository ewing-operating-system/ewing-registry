---
name: clawdbot-self-repair
description: "Automatic error recovery for bots. Protocol for handling the seven most common ClawdBot failures ranked by hours lost. Covers Anthropic rate limits, Google API confusion, Supabase auth errors, and looping behaviors. Enforces exponential backoff (30s, 60s, 120s, then skip) and prevents tight retry loops that waste credits."
---

# ClawdBot Self-Repair Protocol

## Rule Zero
Never retry in a loop. Exponential backoff: 30s → 60s → 120s → SKIP.

## 7 Known Issues Ranked by Hours Lost

### 1. Anthropic Rate Limits (6+ hrs lost)
Scout + Next ran simultaneously on Tier 1. Hit 429. Retried in tight loop.
Fix: NEVER run two agents simultaneously on Tier 1. Hit 429 → stop ALL agents → wait 2 min → restart ONE.

### 2. Google API Confusion (4-6 hrs lost)
Billing enabled ≠ API enabled. Three separate search products.
Fix: Enable API separately at console.cloud.google.com. Wait 1 hour for propagation.

### 3. Fetch Permission Prompts (2+ hrs lost)
Claude Code asking "Do you want to proceed?" on every command.
Fix: /permissions → Bash(*) → save to User settings (option 3).

### 4. OpenClaw Config Confusion
API key in ~/.zshrc but OpenClaw reads ~/.openclaw/openclaw.json.
Fix: Key must be in BOTH files.

### 5. Supabase Auth Headers
Wrong key in wrong header.
Fix: anon key → apikey header. Service role → Authorization Bearer header.

### 6. API Key Not Persisting
Key gone in new terminal tab.
Fix: echo 'export ANTHROPIC_API_KEY=...' >> ~/.zshrc && source ~/.zshrc

### 7. Wrong Terminal Tab
OpenClaw commands in zsh → parse error.
Fix: OpenClaw commands → openclaw tui only. Bash → regular terminal only.

## Speed Rules
1. One agent at a time on Tier 1.
2. Haiku for grunt work. Sonnet for thinking.
3. Cheapest search first: Google ($0.005) → Gemini (free) → Claude (expensive).
4. Batch 5, pause 90s, batch 5. Don't fire 50 at once.
5. 4 attempts max then skip.
6. Pre-flight every time
