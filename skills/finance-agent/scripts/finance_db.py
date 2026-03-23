#!/usr/bin/env python3
"""
Finance Agent — SQLite Database Layer
Manages schema, queries, and helpers for the personal finance tracker.
"""

import sqlite3
import os
from datetime import datetime, date
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent.parent / "data" / "finance.db"


def get_db_path():
    return str(DB_PATH)


@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.executescript(SCHEMA_SQL)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    institution TEXT,
    type TEXT NOT NULL CHECK(type IN (
        'checking', 'savings', 'brokerage', 'retirement',
        'credit_card', 'loan', 'real_estate', 'other'
    )),
    subtype TEXT,
    plaid_account_id TEXT UNIQUE,
    is_manual INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS balances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    date TEXT NOT NULL,
    balance REAL NOT NULL,
    available REAL,
    currency TEXT NOT NULL DEFAULT 'USD',
    UNIQUE(account_id, date)
);

CREATE TABLE IF NOT EXISTS holdings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    symbol TEXT NOT NULL,
    name TEXT,
    quantity REAL NOT NULL DEFAULT 0,
    cost_basis REAL,
    current_price REAL,
    current_value REAL,
    asset_class TEXT CHECK(asset_class IN (
        'stock', 'etf', 'bond', 'mutual_fund', 'cash', 'option', 'other'
    )),
    sector TEXT,
    last_updated TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(account_id, symbol)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT,
    subcategory TEXT,
    merchant TEXT,
    description TEXT,
    is_income INTEGER NOT NULL DEFAULT 0,
    is_recurring INTEGER NOT NULL DEFAULT 0,
    plaid_transaction_id TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS manual_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN (
        'real_estate', 'vehicle', 'collectible', 'business', 'other'
    )),
    estimated_value REAL NOT NULL,
    purchase_price REAL,
    purchase_date TEXT,
    notes TEXT,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS manual_liabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN (
        'mortgage', 'auto_loan', 'student_loan', 'personal_loan',
        'credit_card_debt', 'other'
    )),
    balance REAL NOT NULL,
    interest_rate REAL,
    monthly_payment REAL,
    notes TEXT,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS net_worth_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    total_assets REAL NOT NULL,
    total_liabilities REAL NOT NULL,
    net_worth REAL NOT NULL,
    cash_position REAL,
    invested_total REAL
);

CREATE TABLE IF NOT EXISTS allocation_targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_class TEXT NOT NULL UNIQUE,
    target_pct REAL NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_balances_account_date ON balances(account_id, date);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_holdings_account ON holdings(account_id);
CREATE INDEX IF NOT EXISTS idx_net_worth_date ON net_worth_history(date);
"""


# ── Account Operations ──────────────────────────────────────────────

def add_account(name, institution, acct_type, subtype=None, plaid_account_id=None, is_manual=True):
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO accounts (name, institution, type, subtype, plaid_account_id, is_manual)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, institution, acct_type, subtype, plaid_account_id, int(is_manual))
        )
        return cur.lastrowid


def get_accounts(institution=None, acct_type=None):
    with get_connection() as conn:
        sql = "SELECT * FROM accounts WHERE 1=1"
        params = []
        if institution:
            sql += " AND institution = ?"
            params.append(institution)
        if acct_type:
            sql += " AND type = ?"
            params.append(acct_type)
        sql += " ORDER BY institution, type, name"
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def get_account_by_id(account_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM accounts WHERE id = ?", (account_id,)).fetchone()
        return dict(row) if row else None


# ── Balance Operations ───────────────────────────────────────────────

def record_balance(account_id, balance, available=None, as_of_date=None, currency="USD"):
    as_of_date = as_of_date or date.today().isoformat()
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO balances (account_id, date, balance, available, currency)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(account_id, date) DO UPDATE SET
                 balance=excluded.balance, available=excluded.available""",
            (account_id, as_of_date, balance, available, currency)
        )


def get_latest_balances():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT a.id, a.name, a.institution, a.type, a.subtype,
                   b.balance, b.available, b.date as balance_date
            FROM accounts a
            LEFT JOIN balances b ON a.id = b.account_id
                AND b.date = (SELECT MAX(b2.date) FROM balances b2 WHERE b2.account_id = a.id)
            ORDER BY a.institution, a.type, a.name
        """).fetchall()]


def get_balance_history(account_id=None, days=90):
    with get_connection() as conn:
        if account_id:
            return [dict(r) for r in conn.execute("""
                SELECT * FROM balances WHERE account_id = ?
                AND date >= date('now', ?)
                ORDER BY date
            """, (account_id, f"-{days} days")).fetchall()]
        else:
            return [dict(r) for r in conn.execute("""
                SELECT date, SUM(balance) as total_balance
                FROM balances
                WHERE date >= date('now', ?)
                GROUP BY date ORDER BY date
            """, (f"-{days} days",)).fetchall()]


# ── Holdings Operations ──────────────────────────────────────────────

def upsert_holding(account_id, symbol, name=None, quantity=0, cost_basis=None,
                   current_price=None, current_value=None, asset_class=None, sector=None):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO holdings (account_id, symbol, name, quantity, cost_basis,
                   current_price, current_value, asset_class, sector, last_updated)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
               ON CONFLICT(account_id, symbol) DO UPDATE SET
                 name=excluded.name, quantity=excluded.quantity,
                 cost_basis=excluded.cost_basis, current_price=excluded.current_price,
                 current_value=excluded.current_value, asset_class=excluded.asset_class,
                 sector=excluded.sector, last_updated=datetime('now')""",
            (account_id, symbol, name, quantity, cost_basis, current_price, current_value,
             asset_class, sector)
        )


def get_all_holdings():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT h.*, a.name as account_name, a.institution
            FROM holdings h JOIN accounts a ON h.account_id = a.id
            ORDER BY h.current_value DESC NULLS LAST
        """).fetchall()]


def get_allocation_breakdown():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT asset_class, SUM(current_value) as total_value,
                   COUNT(*) as num_holdings
            FROM holdings
            WHERE current_value IS NOT NULL
            GROUP BY asset_class
            ORDER BY total_value DESC
        """).fetchall()]


def get_sector_breakdown():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT sector, SUM(current_value) as total_value,
                   COUNT(*) as num_holdings
            FROM holdings
            WHERE current_value IS NOT NULL AND sector IS NOT NULL
            GROUP BY sector
            ORDER BY total_value DESC
        """).fetchall()]


# ── Transaction Operations ───────────────────────────────────────────

def add_transaction(account_id, txn_date, amount, category=None, subcategory=None,
                    merchant=None, description=None, is_income=False, is_recurring=False,
                    plaid_transaction_id=None):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO transactions
               (account_id, date, amount, category, subcategory, merchant, description,
                is_income, is_recurring, plaid_transaction_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(plaid_transaction_id) DO UPDATE SET
                 amount=excluded.amount, category=excluded.category,
                 merchant=excluded.merchant, description=excluded.description""",
            (account_id, txn_date, amount, category, subcategory, merchant, description,
             int(is_income), int(is_recurring), plaid_transaction_id)
        )


def get_transactions(account_id=None, start_date=None, end_date=None, category=None, limit=100):
    with get_connection() as conn:
        sql = "SELECT t.*, a.name as account_name FROM transactions t JOIN accounts a ON t.account_id = a.id WHERE 1=1"
        params = []
        if account_id:
            sql += " AND t.account_id = ?"
            params.append(account_id)
        if start_date:
            sql += " AND t.date >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND t.date <= ?"
            params.append(end_date)
        if category:
            sql += " AND t.category = ?"
            params.append(category)
        sql += " ORDER BY t.date DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def get_cashflow_summary(start_date=None, end_date=None):
    start_date = start_date or date.today().replace(day=1).isoformat()
    end_date = end_date or date.today().isoformat()
    with get_connection() as conn:
        income = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE is_income=1 AND date BETWEEN ? AND ?",
            (start_date, end_date)
        ).fetchone()[0]
        expenses = conn.execute(
            "SELECT COALESCE(SUM(ABS(amount)), 0) FROM transactions WHERE is_income=0 AND date BETWEEN ? AND ?",
            (start_date, end_date)
        ).fetchone()[0]
        by_category = [dict(r) for r in conn.execute("""
            SELECT category, SUM(ABS(amount)) as total, COUNT(*) as count
            FROM transactions
            WHERE is_income=0 AND date BETWEEN ? AND ?
            GROUP BY category ORDER BY total DESC
        """, (start_date, end_date)).fetchall()]
        recurring = [dict(r) for r in conn.execute("""
            SELECT merchant, category, amount, COUNT(*) as occurrences
            FROM transactions
            WHERE is_recurring=1 AND date BETWEEN ? AND ?
            GROUP BY merchant, category
            ORDER BY ABS(amount) DESC
        """, (start_date, end_date)).fetchall()]
        return {
            "period": {"start": start_date, "end": end_date},
            "income": income,
            "expenses": expenses,
            "net": income - expenses,
            "by_category": by_category,
            "recurring": recurring
        }


# ── Manual Assets & Liabilities ─────────────────────────────────────

def add_manual_asset(name, asset_type, estimated_value, purchase_price=None,
                     purchase_date=None, notes=None):
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO manual_assets (name, type, estimated_value, purchase_price, purchase_date, notes)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, asset_type, estimated_value, purchase_price, purchase_date, notes)
        )
        return cur.lastrowid


def update_manual_asset(asset_id, estimated_value=None, notes=None):
    with get_connection() as conn:
        if estimated_value is not None:
            conn.execute(
                "UPDATE manual_assets SET estimated_value=?, updated_at=datetime('now') WHERE id=?",
                (estimated_value, asset_id)
            )
        if notes is not None:
            conn.execute(
                "UPDATE manual_assets SET notes=?, updated_at=datetime('now') WHERE id=?",
                (notes, asset_id)
            )


def get_manual_assets():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM manual_assets ORDER BY estimated_value DESC"
        ).fetchall()]


def add_manual_liability(name, liability_type, balance, interest_rate=None,
                         monthly_payment=None, notes=None):
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO manual_liabilities (name, type, balance, interest_rate, monthly_payment, notes)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, liability_type, balance, interest_rate, monthly_payment, notes)
        )
        return cur.lastrowid


def update_manual_liability(liability_id, balance=None, notes=None):
    with get_connection() as conn:
        if balance is not None:
            conn.execute(
                "UPDATE manual_liabilities SET balance=?, updated_at=datetime('now') WHERE id=?",
                (balance, liability_id)
            )
        if notes is not None:
            conn.execute(
                "UPDATE manual_liabilities SET notes=?, updated_at=datetime('now') WHERE id=?",
                (notes, liability_id)
            )


def get_manual_liabilities():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM manual_liabilities ORDER BY balance DESC"
        ).fetchall()]


# ── Net Worth ────────────────────────────────────────────────────────

def calculate_net_worth():
    with get_connection() as conn:
        # Account balances (latest per account)
        account_total = conn.execute("""
            SELECT COALESCE(SUM(b.balance), 0)
            FROM accounts a
            JOIN balances b ON a.id = b.account_id
                AND b.date = (SELECT MAX(b2.date) FROM balances b2 WHERE b2.account_id = a.id)
            WHERE a.type IN ('checking', 'savings', 'brokerage', 'retirement')
        """).fetchone()[0]

        # Credit card / loan balances (negative)
        debt_total = conn.execute("""
            SELECT COALESCE(SUM(ABS(b.balance)), 0)
            FROM accounts a
            JOIN balances b ON a.id = b.account_id
                AND b.date = (SELECT MAX(b2.date) FROM balances b2 WHERE b2.account_id = a.id)
            WHERE a.type IN ('credit_card', 'loan')
        """).fetchone()[0]

        # Manual assets
        manual_asset_total = conn.execute(
            "SELECT COALESCE(SUM(estimated_value), 0) FROM manual_assets"
        ).fetchone()[0]

        # Manual liabilities
        manual_liability_total = conn.execute(
            "SELECT COALESCE(SUM(balance), 0) FROM manual_liabilities"
        ).fetchone()[0]

        # Cash position (checking + savings only)
        cash_position = conn.execute("""
            SELECT COALESCE(SUM(b.balance), 0)
            FROM accounts a
            JOIN balances b ON a.id = b.account_id
                AND b.date = (SELECT MAX(b2.date) FROM balances b2 WHERE b2.account_id = a.id)
            WHERE a.type IN ('checking', 'savings')
        """).fetchone()[0]

        # Invested total (brokerage + retirement)
        invested_total = conn.execute("""
            SELECT COALESCE(SUM(b.balance), 0)
            FROM accounts a
            JOIN balances b ON a.id = b.account_id
                AND b.date = (SELECT MAX(b2.date) FROM balances b2 WHERE b2.account_id = a.id)
            WHERE a.type IN ('brokerage', 'retirement')
        """).fetchone()[0]

        total_assets = account_total + manual_asset_total
        total_liabilities = debt_total + manual_liability_total
        net_worth = total_assets - total_liabilities

        return {
            "date": date.today().isoformat(),
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "net_worth": net_worth,
            "cash_position": cash_position,
            "invested_total": invested_total,
            "manual_assets": manual_asset_total,
            "manual_liabilities": manual_liability_total,
            "account_balances": account_total,
            "debt": debt_total
        }


def record_net_worth_snapshot():
    nw = calculate_net_worth()
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO net_worth_history (date, total_assets, total_liabilities, net_worth, cash_position, invested_total)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(date) DO UPDATE SET
                 total_assets=excluded.total_assets, total_liabilities=excluded.total_liabilities,
                 net_worth=excluded.net_worth, cash_position=excluded.cash_position,
                 invested_total=excluded.invested_total""",
            (nw["date"], nw["total_assets"], nw["total_liabilities"],
             nw["net_worth"], nw["cash_position"], nw["invested_total"])
        )
    return nw


def get_net_worth_history(days=365):
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT * FROM net_worth_history
            WHERE date >= date('now', ?)
            ORDER BY date
        """, (f"-{days} days",)).fetchall()]


# ── Allocation Targets ───────────────────────────────────────────────

def set_allocation_target(asset_class, target_pct):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO allocation_targets (asset_class, target_pct, updated_at)
               VALUES (?, ?, datetime('now'))
               ON CONFLICT(asset_class) DO UPDATE SET
                 target_pct=excluded.target_pct, updated_at=datetime('now')""",
            (asset_class, target_pct)
        )


def get_allocation_vs_target():
    actuals = get_allocation_breakdown()
    total = sum(a["total_value"] for a in actuals)
    if total == 0:
        return []
    with get_connection() as conn:
        targets = {r["asset_class"]: r["target_pct"]
                   for r in conn.execute("SELECT * FROM allocation_targets").fetchall()}
    result = []
    for a in actuals:
        actual_pct = (a["total_value"] / total) * 100
        target_pct = targets.get(a["asset_class"])
        drift = (actual_pct - target_pct) if target_pct else None
        result.append({
            "asset_class": a["asset_class"],
            "value": a["total_value"],
            "actual_pct": round(actual_pct, 1),
            "target_pct": target_pct,
            "drift": round(drift, 1) if drift is not None else None,
            "alert": abs(drift) > 5 if drift is not None else False
        })
    return result


# ── Initialization ───────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
