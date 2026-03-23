#!/usr/bin/env python3
"""
Finance Agent — Local API Server
FastAPI server that exposes financial data for the web dashboard.
Runs on localhost:8787, reads from the local SQLite database.

Usage:
  pip install fastapi uvicorn
  python3 api_server.py
"""

import sys
import json
from pathlib import Path
from datetime import date, datetime

sys.path.insert(0, str(Path(__file__).parent))

try:
    from fastapi import FastAPI, Query
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError:
    print("FastAPI and uvicorn required. Install with:")
    print("  pip install fastapi uvicorn")
    sys.exit(1)

from finance_db import (
    init_db, get_accounts, get_latest_balances, get_balance_history,
    get_all_holdings, get_allocation_breakdown, get_sector_breakdown,
    get_allocation_vs_target, get_transactions, get_cashflow_summary,
    get_manual_assets, get_manual_liabilities, calculate_net_worth,
    get_net_worth_history, record_net_worth_snapshot
)

app = FastAPI(title="Finance Agent API", version="1.0.0")

# Allow the Lovable dashboard to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


# ── Net Worth ────────────────────────────────────────────────────────

@app.get("/api/networth")
def api_net_worth():
    return calculate_net_worth()


@app.get("/api/networth/history")
def api_net_worth_history(days: int = Query(365)):
    return get_net_worth_history(days)


@app.post("/api/networth/snapshot")
def api_record_snapshot():
    return record_net_worth_snapshot()


# ── Accounts ─────────────────────────────────────────────────────────

@app.get("/api/accounts")
def api_accounts(institution: str = None, type: str = None):
    return get_accounts(institution=institution, acct_type=type)


@app.get("/api/accounts/balances")
def api_latest_balances():
    return get_latest_balances()


@app.get("/api/accounts/{account_id}/history")
def api_balance_history(account_id: int, days: int = Query(90)):
    return get_balance_history(account_id=account_id, days=days)


# ── Holdings / Portfolio ─────────────────────────────────────────────

@app.get("/api/holdings")
def api_holdings():
    return get_all_holdings()


@app.get("/api/allocation")
def api_allocation():
    return get_allocation_breakdown()


@app.get("/api/allocation/sectors")
def api_sectors():
    return get_sector_breakdown()


@app.get("/api/allocation/targets")
def api_allocation_targets():
    return get_allocation_vs_target()


# ── Transactions / Cash Flow ─────────────────────────────────────────

@app.get("/api/transactions")
def api_transactions(
    account_id: int = None,
    start_date: str = None,
    end_date: str = None,
    category: str = None,
    limit: int = Query(100),
):
    return get_transactions(
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
        category=category,
        limit=limit,
    )


@app.get("/api/cashflow")
def api_cashflow(start_date: str = None, end_date: str = None):
    return get_cashflow_summary(start_date=start_date, end_date=end_date)


# ── Manual Assets & Liabilities ──────────────────────────────────────

@app.get("/api/assets")
def api_manual_assets():
    return get_manual_assets()


@app.get("/api/liabilities")
def api_manual_liabilities():
    return get_manual_liabilities()


# ── Health Check ─────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    print("Starting Finance Agent API on http://localhost:8787")
    print("Dashboard should connect from http://localhost:5173")
    uvicorn.run(app, host="127.0.0.1", port=8787)
