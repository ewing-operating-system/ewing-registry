# Plaid Integration Guide

## Overview
Plaid connects to Wells Fargo and Chase to automatically pull account balances, transactions, and investment holdings. This replaces manual CSV imports for day-to-day tracking.

## Status: AWAITING SETUP
Plaid requires a developer account and API keys before it can be used. The finance agent works fully without Plaid via manual entry and CSV imports.

## Setup Steps

### 1. Create a Plaid Developer Account
- Sign up at https://dashboard.plaid.com/signup
- Free for development/sandbox use
- Production access requires application (free for personal use)

### 2. Get API Keys
From the Plaid Dashboard → Keys:
- `PLAID_CLIENT_ID`
- `PLAID_SECRET` (use Sandbox secret for testing, Development for real accounts)
- `PLAID_ENV` — `sandbox` for testing, `development` for real bank connections

### 3. Store Credentials
Create `~/.config/finance-agent/credentials.json`:
```json
{
  "plaid_client_id": "YOUR_CLIENT_ID",
  "plaid_secret": "YOUR_SECRET",
  "plaid_env": "sandbox",
  "access_tokens": {}
}
```

### 4. Link Bank Accounts
Run `python3 ~/.claude/skills/finance-agent/scripts/setup_plaid.py` to:
- Start a local server for Plaid Link
- Open browser to connect Wells Fargo and Chase
- Store access tokens in credentials file

### 5. First Sync
Run `python3 ~/.claude/skills/finance-agent/scripts/sync_accounts.py` or use `/finance sync`

## API Endpoints Used

| Endpoint | Purpose | Data Pulled |
|----------|---------|-------------|
| `/accounts/balance/get` | Account balances | Current + available balance per account |
| `/transactions/sync` | Transactions | All new/modified/removed transactions |
| `/investments/holdings/get` | Investment holdings | Securities, quantities, values |
| `/investments/transactions/get` | Investment transactions | Buys, sells, dividends |

## Cost
- **Sandbox**: Free, unlimited (uses test data)
- **Development**: Free, 100 live items (accounts)
- **Production**: Requires application, free tier available for personal use

## Security Notes
- Access tokens stored locally only (`~/.config/finance-agent/`)
- Tokens are never committed to git or sent anywhere besides Plaid's API
- Each linked institution gets its own access token
- Tokens can be revoked via Plaid Dashboard at any time

## Dependencies
```
pip install plaid-python
```
