# Daily Financial Snapshot Template

Use this template when presenting the `/finance` daily snapshot.

```
═══════════════════════════════════════════════════
  FINANCIAL SNAPSHOT — {date}
═══════════════════════════════════════════════════

  NET WORTH:           ${net_worth}
  {net_worth_change_indicator}

  ┌─ ASSETS ─────────────────────────────────────┐
  │ Cash (checking/savings):   ${cash_position}   │
  │ Invested (brokerage/ret):  ${invested_total}   │
  │ Manual assets:             ${manual_assets}    │
  │                                               │
  │ TOTAL ASSETS:              ${total_assets}     │
  └───────────────────────────────────────────────┘

  ┌─ LIABILITIES ────────────────────────────────┐
  │ Account debt (CC/loans):   ${debt}             │
  │ Manual liabilities:        ${manual_liabilities}│
  │                                               │
  │ TOTAL LIABILITIES:         ${total_liabilities} │
  └───────────────────────────────────────────────┘

  CASH POSITION:       ${cash_position}

  ── TOP HOLDINGS ────────────────────────────────
  {holdings_table}

  ── ACCOUNTS ────────────────────────────────────
  {accounts_by_institution}

  ── CASH FLOW (MTD) ────────────────────────────
  Income:    ${income_mtd}
  Expenses:  ${expenses_mtd}
  Net:       ${net_cashflow_mtd}
═══════════════════════════════════════════════════
```

## Change Indicators
- Up from yesterday: ▲ $X,XXX (+X.X%)
- Down from yesterday: ▼ $X,XXX (-X.X%)
- No change: — (unchanged)
- No prior data: (first snapshot)

## Holdings Table Format
```
Symbol  | Name              | Value      | Day Chg  | Weight
--------|-------------------|------------|----------|-------
AAPL    | Apple Inc         | $12,345    | +1.2%    | 15.3%
VOO     | Vanguard S&P 500  | $45,678    | +0.8%    | 56.7%
```

## Accounts By Institution Format
```
Wells Fargo
  Checking         $X,XXX.XX    (updated today)
  Savings          $X,XXX.XX    (updated today)

Chase
  Total Checking   $X,XXX.XX    (updated today)
  Sapphire CC      -$X,XXX.XX   (updated today)
```
