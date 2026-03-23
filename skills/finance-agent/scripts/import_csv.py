#!/usr/bin/env python3
"""
Finance Agent — CSV Import Tool
Auto-detects and imports Wells Fargo and Chase bank/credit card CSV exports.
"""

import csv
import sys
import os
import re
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from finance_db import init_db, add_account, get_accounts, add_transaction, record_balance

# ── Format Detection ─────────────────────────────────────────────────

def detect_format(file_path):
    """Detect whether a CSV is from Wells Fargo, Chase, or generic."""
    with open(file_path, "r", encoding="utf-8-sig") as f:
        first_lines = [f.readline() for _ in range(5)]
        header = first_lines[0].lower().strip()

    # Wells Fargo: no header row, 5 columns: date, amount, *, *, description
    # Or has header: "Date","Amount","*","*","Description"
    if "wells fargo" in " ".join(first_lines).lower():
        return "wells_fargo"

    # Chase: header row with specific columns
    if "posting date" in header or "transaction date" in header:
        return "chase"

    # Wells Fargo checking/savings (headerless, 5 columns)
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            first_row = next(reader)
            if len(first_row) == 5:
                # Try to parse first field as date
                try:
                    datetime.strptime(first_row[0].strip(), "%m/%d/%Y")
                    return "wells_fargo"
                except ValueError:
                    pass
    except Exception:
        pass

    # Chase credit card: "Transaction Date,Post Date,Description,Category,Type,Amount"
    if "transaction date" in header and "category" in header:
        return "chase_credit"

    # Generic fallback
    if "date" in header and "amount" in header:
        return "generic"

    return "unknown"


# ── Wells Fargo Parser ───────────────────────────────────────────────

def parse_wells_fargo(file_path):
    """
    Wells Fargo CSV format (checking/savings):
    Date, Amount, *, *, Description
    No header row. Date format: MM/DD/YYYY
    """
    transactions = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue
            date_str = row[0].strip().strip('"')
            amount_str = row[1].strip().strip('"')
            description = row[4].strip().strip('"')

            # Skip header-like rows
            try:
                txn_date = datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
                amount = float(amount_str.replace(",", ""))
            except (ValueError, IndexError):
                continue

            is_income = amount > 0
            category = categorize_transaction(description, amount)

            transactions.append({
                "date": txn_date,
                "amount": amount,
                "description": description,
                "merchant": extract_merchant(description),
                "category": category,
                "is_income": is_income,
            })

    return transactions


# ── Chase Parser ─────────────────────────────────────────────────────

def parse_chase_checking(file_path):
    """
    Chase checking CSV format:
    Details, Posting Date, Description, Amount, Type, Balance, Check or Slip #
    """
    transactions = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = [f.strip().lower() for f in (reader.fieldnames or [])]

        for row in reader:
            # Normalize keys
            row = {k.strip().lower(): v.strip() for k, v in row.items()}

            date_str = row.get("posting date", row.get("post date", ""))
            description = row.get("description", "")
            amount_str = row.get("amount", "0")

            try:
                txn_date = datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
                amount = float(amount_str.replace(",", ""))
            except (ValueError, KeyError):
                continue

            is_income = amount > 0
            category = row.get("category", categorize_transaction(description, amount))

            transactions.append({
                "date": txn_date,
                "amount": amount,
                "description": description,
                "merchant": extract_merchant(description),
                "category": category,
                "is_income": is_income,
            })

    return transactions


def parse_chase_credit(file_path):
    """
    Chase credit card CSV format:
    Transaction Date, Post Date, Description, Category, Type, Amount
    """
    transactions = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip().lower(): v.strip() for k, v in row.items()}

            date_str = row.get("transaction date", row.get("posting date", ""))
            description = row.get("description", "")
            amount_str = row.get("amount", "0")
            category = row.get("category", "")

            try:
                txn_date = datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
                amount = float(amount_str.replace(",", ""))
            except (ValueError, KeyError):
                continue

            # Chase credit: negative = purchase, positive = payment/credit
            is_income = amount > 0

            transactions.append({
                "date": txn_date,
                "amount": amount,
                "description": description,
                "merchant": extract_merchant(description),
                "category": category or categorize_transaction(description, amount),
                "is_income": is_income,
            })

    return transactions


def parse_generic(file_path):
    """Generic CSV with at least date and amount columns."""
    transactions = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip().lower(): v.strip() for k, v in row.items()}

            # Try common date column names
            date_str = ""
            for col in ["date", "transaction date", "posting date", "post date", "trans date"]:
                if col in row:
                    date_str = row[col]
                    break

            amount_str = row.get("amount", row.get("debit", row.get("credit", "0")))
            description = row.get("description", row.get("memo", row.get("name", "")))

            if not date_str:
                continue

            # Try multiple date formats
            txn_date = None
            for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y", "%d/%m/%Y", "%m-%d-%Y"]:
                try:
                    txn_date = datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue

            if not txn_date:
                continue

            try:
                amount = float(amount_str.replace(",", "").replace("$", ""))
            except ValueError:
                continue

            is_income = amount > 0

            transactions.append({
                "date": txn_date,
                "amount": amount,
                "description": description,
                "merchant": extract_merchant(description),
                "category": row.get("category", categorize_transaction(description, amount)),
                "is_income": is_income,
            })

    return transactions


# ── Categorization Helpers ───────────────────────────────────────────

CATEGORY_PATTERNS = {
    "Payroll/Income": [r"payroll", r"direct dep", r"salary", r"wages", r"ach credit"],
    "Transfer": [r"transfer", r"xfer", r"zelle", r"venmo", r"paypal"],
    "Food & Dining": [r"restaurant", r"doordash", r"uber eats", r"grubhub", r"mcdonald",
                       r"starbucks", r"chipotle", r"chick-fil", r"pizza"],
    "Groceries": [r"grocery", r"kroger", r"heb", r"walmart", r"target", r"costco",
                   r"whole foods", r"trader joe", r"aldi"],
    "Gas & Auto": [r"shell", r"exxon", r"chevron", r"bp ", r"gas", r"fuel", r"auto"],
    "Shopping": [r"amazon", r"best buy", r"apple\.com", r"ebay"],
    "Bills & Utilities": [r"electric", r"water", r"gas bill", r"internet", r"phone",
                          r"at&t", r"verizon", r"t-mobile", r"comcast", r"spectrum"],
    "Insurance": [r"insurance", r"geico", r"state farm", r"allstate", r"progressive"],
    "Healthcare": [r"pharmacy", r"cvs", r"walgreens", r"doctor", r"medical", r"dental"],
    "Rent/Mortgage": [r"rent", r"mortgage", r"hoa"],
    "Entertainment": [r"netflix", r"spotify", r"hulu", r"disney", r"youtube", r"gaming"],
    "Travel": [r"airline", r"hotel", r"airbnb", r"flight", r"uber ", r"lyft"],
    "ATM/Cash": [r"atm", r"cash withdrawal", r"cash advance"],
    "Fee": [r"fee", r"overdraft", r"service charge", r"monthly maintenance"],
}


def categorize_transaction(description, amount=None):
    desc_lower = description.lower()
    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, desc_lower):
                return category
    return "Uncategorized"


def extract_merchant(description):
    """Extract a clean merchant name from transaction description."""
    # Remove common prefixes
    merchant = description
    for prefix in ["POS ", "ACH ", "DEBIT ", "CREDIT ", "CHECK ", "WIRE ",
                    "PURCHASE ", "PAYMENT ", "SQ *", "TST* ", "SP "]:
        if merchant.upper().startswith(prefix):
            merchant = merchant[len(prefix):]
    # Take first meaningful chunk
    merchant = merchant.split("  ")[0].strip()
    merchant = re.sub(r"\s+\d{2,}.*$", "", merchant)  # Remove trailing numbers
    return merchant[:50]


# ── Main Import Logic ────────────────────────────────────────────────

def detect_institution_and_type(fmt, file_path):
    """Return (institution, account_type) based on format."""
    if fmt == "wells_fargo":
        return "Wells Fargo", "checking"
    elif fmt == "chase":
        return "Chase", "checking"
    elif fmt == "chase_credit":
        return "Chase", "credit_card"
    return "Unknown", "checking"


def import_csv(file_path, account_id=None):
    """Import a CSV file into the database. Returns summary dict."""
    init_db()

    file_path = os.path.expanduser(file_path)
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    fmt = detect_format(file_path)
    if fmt == "unknown":
        return {"error": "Could not detect CSV format. Supported: Wells Fargo, Chase, generic CSV with date+amount columns."}

    # Parse based on detected format
    if fmt == "wells_fargo":
        transactions = parse_wells_fargo(file_path)
    elif fmt == "chase":
        transactions = parse_chase_checking(file_path)
    elif fmt == "chase_credit":
        transactions = parse_chase_credit(file_path)
    else:
        transactions = parse_generic(file_path)

    if not transactions:
        return {"error": "No transactions found in file."}

    # Create or find account if not specified
    if account_id is None:
        institution, acct_type = detect_institution_and_type(fmt, file_path)
        accounts = get_accounts(institution=institution, acct_type=acct_type)
        if accounts:
            account_id = accounts[0]["id"]
        else:
            account_id = add_account(
                name=f"{institution} {acct_type.replace('_', ' ').title()}",
                institution=institution,
                acct_type=acct_type,
                is_manual=True
            )

    # Import transactions
    imported = 0
    skipped = 0
    for txn in transactions:
        try:
            add_transaction(
                account_id=account_id,
                txn_date=txn["date"],
                amount=txn["amount"],
                category=txn["category"],
                merchant=txn["merchant"],
                description=txn["description"],
                is_income=txn["is_income"],
            )
            imported += 1
        except Exception:
            skipped += 1

    # Determine date range
    dates = [t["date"] for t in transactions]
    min_date = min(dates)
    max_date = max(dates)

    return {
        "format_detected": fmt,
        "file": os.path.basename(file_path),
        "account_id": account_id,
        "total_in_file": len(transactions),
        "imported": imported,
        "skipped": skipped,
        "date_range": f"{min_date} to {max_date}",
        "income_total": sum(t["amount"] for t in transactions if t["is_income"]),
        "expense_total": sum(abs(t["amount"]) for t in transactions if not t["is_income"]),
    }


# ── CLI Entry Point ──────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    if len(sys.argv) < 2:
        print("Usage: import_csv.py <file_path> [account_id]")
        print("\nSupported formats:")
        print("  - Wells Fargo checking/savings CSV")
        print("  - Chase checking CSV")
        print("  - Chase credit card CSV")
        print("  - Generic CSV (must have date + amount columns)")
        sys.exit(1)

    file_path = sys.argv[1]
    acct_id = int(sys.argv[2]) if len(sys.argv) > 2 else None

    result = import_csv(file_path, acct_id)
    print(json.dumps(result, indent=2))
