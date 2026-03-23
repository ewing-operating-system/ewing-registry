#!/usr/bin/env python3
"""
Finance Agent — Plaid Account Sync
Pulls latest balances, transactions, and holdings from connected institutions.

STATUS: STUB — requires plaid-python and configured credentials.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from finance_db import (
    init_db, add_account, get_accounts, record_balance,
    add_transaction, upsert_holding, record_net_worth_snapshot
)

CREDENTIALS_PATH = Path.home() / ".config" / "finance-agent" / "credentials.json"


def load_credentials():
    if not CREDENTIALS_PATH.exists():
        return None
    with open(CREDENTIALS_PATH) as f:
        return json.load(f)


def get_plaid_client(creds):
    """Initialize Plaid API client."""
    try:
        import plaid
        from plaid.api import plaid_api
    except ImportError:
        print("Error: plaid-python not installed. Run: pip install plaid-python")
        return None

    env_map = {
        "sandbox": plaid.Environment.Sandbox,
        "development": plaid.Environment.Development,
        "production": plaid.Environment.Production,
    }

    configuration = plaid.Configuration(
        host=env_map.get(creds["plaid_env"], plaid.Environment.Sandbox),
        api_key={
            "clientId": creds["plaid_client_id"],
            "secret": creds["plaid_secret"],
        },
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)


def sync_balances(client, access_token, institution_name):
    """Pull account balances from Plaid."""
    from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

    request = AccountsBalanceGetRequest(access_token=access_token)
    response = client.accounts_balance_get(request)

    synced = []
    for account in response["accounts"]:
        plaid_id = account["account_id"]
        name = account["name"]
        acct_type_map = {
            "depository": {"checking": "checking", "savings": "savings"},
            "investment": {"401k": "retirement", "ira": "retirement",
                          "roth": "retirement", "brokerage": "brokerage"},
            "credit": {"credit card": "credit_card"},
            "loan": {"mortgage": "loan", "student": "loan", "auto": "loan"},
        }
        plaid_type = account["type"]
        plaid_subtype = account.get("subtype", "")

        # Map to our account types
        type_group = acct_type_map.get(plaid_type, {})
        acct_type = type_group.get(plaid_subtype, plaid_type if plaid_type in
                                    ("checking", "savings", "brokerage", "retirement",
                                     "credit_card", "loan") else "other")

        # Find or create account
        existing = get_accounts(institution=institution_name, acct_type=acct_type)
        matching = [a for a in existing if a.get("plaid_account_id") == plaid_id]

        if matching:
            account_id = matching[0]["id"]
        else:
            account_id = add_account(
                name=name,
                institution=institution_name,
                acct_type=acct_type,
                subtype=plaid_subtype,
                plaid_account_id=plaid_id,
                is_manual=False,
            )

        balance = account["balances"]["current"] or 0
        available = account["balances"].get("available")

        record_balance(account_id, balance, available)
        synced.append({
            "account": name,
            "type": acct_type,
            "balance": balance,
        })

    return synced


def sync_transactions(client, access_token, institution_name):
    """Pull recent transactions from Plaid."""
    from plaid.model.transactions_get_request import TransactionsGetRequest
    from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

    start_date = (datetime.now() - timedelta(days=30)).date()
    end_date = datetime.now().date()

    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
        options=TransactionsGetRequestOptions(count=500, offset=0),
    )
    response = client.transactions_get(request)

    imported = 0
    for txn in response["transactions"]:
        plaid_id = txn["transaction_id"]
        plaid_account_id = txn["account_id"]

        # Find matching account
        accounts = get_accounts(institution=institution_name)
        matching = [a for a in accounts if a.get("plaid_account_id") == plaid_account_id]
        if not matching:
            continue

        account_id = matching[0]["id"]
        amount = -txn["amount"]  # Plaid: positive = money out, we flip it

        try:
            add_transaction(
                account_id=account_id,
                txn_date=txn["date"],
                amount=amount,
                category=txn.get("category", [None])[0] if txn.get("category") else None,
                merchant=txn.get("merchant_name"),
                description=txn.get("name", ""),
                is_income=amount > 0,
                plaid_transaction_id=plaid_id,
            )
            imported += 1
        except Exception:
            pass

    return {"imported": imported, "total_available": response["total_transactions"]}


def sync_holdings(client, access_token, institution_name):
    """Pull investment holdings from Plaid."""
    from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest

    try:
        request = InvestmentsHoldingsGetRequest(access_token=access_token)
        response = client.investments_holdings_get(request)
    except Exception as e:
        # Not all accounts have investments
        return {"holdings": 0, "note": f"No investment data: {e}"}

    securities = {s["security_id"]: s for s in response.get("securities", [])}
    accounts = get_accounts(institution=institution_name)

    synced = 0
    for holding in response.get("holdings", []):
        plaid_account_id = holding["account_id"]
        matching = [a for a in accounts if a.get("plaid_account_id") == plaid_account_id]
        if not matching:
            continue

        account_id = matching[0]["id"]
        security = securities.get(holding["security_id"], {})

        symbol = security.get("ticker_symbol", "UNKNOWN")
        name = security.get("name", "")
        asset_type = security.get("type", "other").lower()

        asset_class_map = {
            "equity": "stock", "etf": "etf", "mutual fund": "mutual_fund",
            "fixed income": "bond", "cash": "cash", "derivative": "option",
        }

        upsert_holding(
            account_id=account_id,
            symbol=symbol,
            name=name,
            quantity=holding.get("quantity", 0),
            cost_basis=holding.get("cost_basis"),
            current_price=security.get("close_price"),
            current_value=holding.get("institution_value"),
            asset_class=asset_class_map.get(asset_type, "other"),
        )
        synced += 1

    return {"holdings": synced}


def run_full_sync():
    """Sync all connected institutions."""
    init_db()

    creds = load_credentials()
    if not creds:
        return {
            "error": "No Plaid credentials found.",
            "help": "See ~/.claude/skills/finance-agent/references/plaid-integration.md for setup instructions.",
            "alternative": "Use /finance import to import CSV files, or /finance add for manual entry."
        }

    if not creds.get("access_tokens"):
        return {
            "error": "No bank accounts linked yet.",
            "help": "Run: python3 ~/.claude/skills/finance-agent/scripts/setup_plaid.py"
        }

    client = get_plaid_client(creds)
    if not client:
        return {"error": "Could not initialize Plaid client"}

    results = {}
    for institution_name, token_data in creds["access_tokens"].items():
        access_token = token_data["access_token"]
        inst_result = {"balances": [], "transactions": {}, "holdings": {}}

        try:
            inst_result["balances"] = sync_balances(client, access_token, institution_name)
        except Exception as e:
            inst_result["balances_error"] = str(e)

        try:
            inst_result["transactions"] = sync_transactions(client, access_token, institution_name)
        except Exception as e:
            inst_result["transactions_error"] = str(e)

        try:
            inst_result["holdings"] = sync_holdings(client, access_token, institution_name)
        except Exception as e:
            inst_result["holdings_error"] = str(e)

        results[institution_name] = inst_result

    # Record daily net worth snapshot
    nw = record_net_worth_snapshot()
    results["net_worth_snapshot"] = nw

    return results


if __name__ == "__main__":
    result = run_full_sync()
    print(json.dumps(result, indent=2, default=str))
