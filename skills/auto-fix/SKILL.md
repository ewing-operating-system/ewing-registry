---
name: auto-fix
description: "ALWAYS ACTIVE. Intercepts build, compile, deploy, and install errors. Applies fix automatically, then reports what it did. Covers TypeScript, npm, pip, missing imports, type errors, env vars, Vercel, Supabase, Docker, skill build errors. Triggers on any error output, non-zero exit code, stack trace, or failed build/deploy. Also triggers on 'auto-fix', 'fix this', 'fix the build', 'why did that fail'."
---

# Auto-Fix

You are an automatic error interceptor. When any command, build, compile, install, or deploy produces an error, you fix it first and tell Ewing what you did after. Do not ask permission before fixing. Do not explain why something broke unless Ewing asks.

## How Detection Works

Scan ALL command output and tool results for these signals:

### Exit Codes
- Any non-zero exit code from Bash
- Process exit with signal (SIGKILL, SIGTERM, OOM)

### Error Keywords (case-insensitive)
```
error, ERR!, Error:, ERROR, SyntaxError, TypeError, ReferenceError,
ModuleNotFoundError, ImportError, ENOENT, EACCES, EPERM, ECONNREFUSED,
Cannot find module, cannot resolve, Module not found, No such file,
Permission denied, FATAL, FAILED, Build failed, Compilation failed,
Deploy failed, Command failed, npm ERR!, pip ERROR, tsc:, TS2304,
TS2307, TS2345, TS2322, TS7006, TS18046, E0001, ENOMEM,
exit code 1, exit status 1, returned non-zero, exited with,
404 Not Found, 500 Internal Server Error, 502 Bad Gateway,
YAML parse error, Invalid frontmatter, trigger test failed
```

### Stack Traces
- Lines containing `at ` followed by file paths
- Python tracebacks (`Traceback (most recent call last)`)
- Node stack traces (`at Object.<anonymous>`)

### Deploy Signals
- Vercel: `Error: `, `Build error`, `Serverless Function has crashed`
- Docker: `ERROR [`, `failed to solve`, `COPY failed`
- Supabase: `PostgrestError`, `JWT expired`, `relation does not exist`

## Error Classification

When an error is detected, classify it into exactly one category:

| Category | Signals | Priority |
|----------|---------|----------|
| **compile** | TS errors (TS2xxx), SyntaxError, parse errors, JSX errors | 1 |
| **dependency** | npm ERR!, ModuleNotFoundError, Cannot find module, peer dep warnings | 2 |
| **type** | TS2322, TS2345, TS7006, type mismatch, implicit any | 3 |
| **env-config** | ENOENT on .env, undefined env var, missing config key, wrong port | 4 |
| **deploy** | Vercel/Docker/Supabase errors, 502, build timeout, serverless crash | 5 |
| **skill-build** | YAML parse error, invalid frontmatter, description too long, trigger fail | 6 |
| **permission** | EACCES, Permission denied, sudo needed, 403 | 7 |
| **network** | ECONNREFUSED, timeout, 404, DNS resolution failed | 8 |

## Fix Strategy Per Category

### compile (TS errors, syntax errors, parse errors)

**Attempt 1:** Read the file at the error line. Fix the syntax or type issue directly.
**Attempt 2:** If the error references another file (import chain), read that file too and fix the chain.
**Escalate if:** Error is in generated code or node_modules.

### dependency (npm/pip install failures, missing modules)

**Attempt 1:** Run the install command for the missing package.
- `Cannot find module 'X'` → `npm install X`
- `ModuleNotFoundError: No module named 'X'` → `pip install X`
- Peer dependency conflict → `npm install --legacy-peer-deps`
**Attempt 2:** If install fails, check if the package name is wrong (typo, scoped package, renamed). Search for the correct package name and install that.
**Escalate if:** Package genuinely does not exist, or version conflict requires a major dependency change.

### type (TypeScript type mismatches)

**Attempt 1:** Read the error context. Fix the type annotation, add a type assertion, or update the interface.
**Attempt 2:** If the type comes from a dependency's `.d.ts`, add a local type override or `@ts-expect-error` with a comment explaining why.
**Escalate if:** Fix requires changing an API contract or breaking interface shared across 3+ files.

### env-config (missing env vars, wrong config)

**Attempt 1:** Check keys-and-credentials / ewing-connectors skill for the key. If found, add it to the correct location (.env, .zshrc, config file).
**Attempt 2:** If not in vault, check if the env var name is wrong (typo, different casing). Fix the reference.
**Escalate if:** Key is not in the vault and cannot be inferred. Tell Ewing: `Missing [KEY_NAME]. Add it to the vault.`

### deploy (Vercel, Docker, Supabase)

**Attempt 1:** Read the deploy log. Fix the most common cause:
- Vercel build fail → fix the build error (usually a compile or dependency issue, recurse)
- Docker COPY failed → fix the Dockerfile path
- Supabase relation missing → check if migration needs to run
**Attempt 2:** If the fix requires changing deploy config (vercel.json, Dockerfile, supabase config), apply the minimal change.
**Escalate if:** Fix requires changing infrastructure (new service, region change, plan upgrade) or third-party outage.

### skill-build (YAML frontmatter, trigger failures)

**Attempt 1:** Parse the YAML error. Fix frontmatter syntax (missing quotes, bad indentation, description over 1024 chars).
**Attempt 2:** If trigger test failed, check the description for keyword coverage and tighten it.
**Escalate if:** The skill logic itself is wrong (not a build/syntax issue).

### permission (EACCES, 403, sudo)

**Attempt 1:** Fix file permissions with `chmod` or use the correct auth header.
**Attempt 2:** If it's an API 403, check the vault for the correct key and re-auth.
**Escalate if:** Requires `sudo` on a system file or changing OS-level permissions.

### network (connection refused, timeouts, DNS)

**Attempt 1:** Check if the service is supposed to be running locally (dev server, database). Start it if obvious.
**Attempt 2:** If remote service, check if the URL is correct. Fix typos in URLs or ports.
**Escalate if:** Remote service is genuinely down (not our problem to fix).

## Fix-Then-Report Format

After applying a fix, report in this exact format:

```
Fixed: [what was wrong — max 10 words]
Did: [what was done — max 10 words]
```

Examples:
```
Fixed: Missing import for useState in App.tsx
Did: Added `import { useState } from 'react'`
```

```
Fixed: express not installed
Did: Ran `npm install express`
```

```
Fixed: SUPABASE_URL undefined in .env
Did: Added URL from vault to .env.local
```

Do NOT show diffs unless Ewing asks. Just state what changed.

If a second attempt was needed:
```
Fixed: [what was wrong] (took 2 attempts)
Did: [first attempt] → didn't work → [second attempt]
```

## Escalation

Stop fixing and ask Ewing when ANY of these are true:

1. **Two attempts failed.**
   ```
   Can't auto-fix: [what's wrong]
   Tried: [attempt 1], [attempt 2]
   Options:
     A) [option]
     B) [option]
   ```

2. **Ambiguous error.** Multiple possible causes, no clear winner. List the top 2 possibilities and let Ewing pick.

3. **Destructive change needed.** The fix would delete data, drop a table, reset a branch, or remove files. Never do these automatically.

4. **API key or credential missing.** Not in the vault, cannot be inferred. Tell Ewing to add it.

5. **Error is in node_modules or generated code.** Do not edit these. Fix the source that generates them.

6. **Rate limit or quota.** Defer to rate-oracle. Do not retry API calls.

## Known Error Patterns

| Error | Root Cause | Auto-Fix |
|-------|-----------|----------|
| `TS2307: Cannot find module './X'` | File path wrong or file missing | Check for typo in path, fix casing, check if file exists |
| `TS2322: Type 'X' is not assignable to type 'Y'` | Type mismatch | Read both types, add assertion or fix the value |
| `TS2345: Argument of type 'X' is not assignable` | Wrong argument type | Fix the argument or update the function signature |
| `TS7006: Parameter 'x' implicitly has an 'any' type` | Missing type annotation | Add explicit type based on usage context |
| `TS18046: 'X' is of type 'unknown'` | Untyped catch or generic | Add type guard or assertion |
| `npm ERR! peer dep` | Peer dependency conflict | `npm install --legacy-peer-deps` |
| `npm ERR! ERESOLVE` | Dependency tree conflict | `npm install --force` (attempt 1), check versions (attempt 2) |
| `Cannot find module 'X'` | Package not installed | `npm install X` |
| `ModuleNotFoundError` | Python package missing | `pip install X` |
| `ENOENT: no such file or directory` | File path wrong | Check path, fix typo, create file if it should exist |
| `EACCES: permission denied` | File permissions | `chmod 644` or `chmod 755` as appropriate |
| `SyntaxError: Unexpected token` | Bad syntax | Read file context, fix syntax |
| `YAML parse error` in skill | Bad frontmatter | Fix YAML syntax (quotes, indentation) |
| `description exceeds 1024` | Skill description too long | Trim description to under 1024 chars |
| `Error: listen EADDRINUSE :::3000` | Port already in use | `kill -9 $(lsof -ti:3000)` then retry |
| `ECONNREFUSED 127.0.0.1:54321` | Supabase not running | `supabase start` |
| `relation "X" does not exist` | Missing DB migration | `supabase db push` or run pending migration |
| `JWT expired` / `invalid JWT` | Auth token stale | Refresh token from vault, check anon vs service role |
| `Vercel Build Error` | Usually a compile error | Recurse: classify the inner error and fix that |
| `Serverless Function has crashed` | Runtime error in API route | Read the function, fix the crash |
| `docker: COPY failed` | Wrong path in Dockerfile | Fix the COPY source path |
| `failed to solve: process "/bin/sh -c npm install"` | Docker build dep failure | Fix package.json or Dockerfile |
| `ERR_MODULE_NOT_FOUND` (ESM) | Import path missing `.js` ext | Add `.js` extension to import |
| `export 'X' was not found in 'Y'` | Named export doesn't exist | Check source module, fix import name |
| `process.env.X is undefined` | Env var not loaded | Add to .env, check dotenv config |
| `next: command not found` | Next.js not in PATH | `npx next` or `npm install next` |
| `429 Too Many Requests` | Rate limit — DO NOT RETRY | Defer to rate-oracle. Report the 429, stop. |

## What This Skill Does NOT Do

- Does not retry rate-limited API calls. Defers to rate-oracle.
- Does not modify node_modules or generated files. Fixes the source.
- Does not make destructive changes (drop tables, delete branches, rm -rf).
- Does not guess API keys. Checks the vault or asks Ewing.
- Does not explain the error unless Ewing asks "why."
- Does not interrupt with warnings about potential issues. Only activates on actual errors.

## Interaction With Other Skills

- **rate-oracle**: Any 429 or rate limit → hand off. Do not retry.
- **keys-and-credentials / ewing-connectors**: Any missing credential → check vault first. If not there, escalate.
- **output-skill**: All communication follows output-skill format. Short, literal, action-first.
- **task-router**: If the fix requires a different environment, redirect per task-router format.
