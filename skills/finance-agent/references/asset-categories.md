# Asset & Account Categories Reference

## Account Types

| Type | Description | Examples | Counts As |
|------|-------------|----------|-----------|
| `checking` | Checking accounts | WF Checking, Chase Total Checking | Cash (asset) |
| `savings` | Savings accounts | WF Way2Save, Chase Savings | Cash (asset) |
| `brokerage` | Taxable investment accounts | WF Advisors, Chase You Invest | Invested (asset) |
| `retirement` | Tax-advantaged retirement | 401(k), IRA, Roth IRA | Invested (asset) |
| `credit_card` | Credit cards | Chase Sapphire, WF Active Cash | Debt (liability) |
| `loan` | Loans | Auto loan, personal loan | Debt (liability) |
| `real_estate` | Property (manual entry) | Primary home, rental property | Manual asset |
| `other` | Anything else | HSA, 529, etc. | Depends |

## Investment Asset Classes

| Class | Description | Examples |
|-------|-------------|----------|
| `stock` | Individual stocks | AAPL, MSFT, TSLA |
| `etf` | Exchange-traded funds | VOO, QQQ, VTI |
| `bond` | Bonds and bond funds | BND, AGG, Treasury |
| `mutual_fund` | Mutual funds | VTSAX, FXAIX |
| `cash` | Cash/money market in investment accounts | SPAXX, settlement fund |
| `option` | Options contracts | Calls, puts |
| `other` | Other investment types | REITs, commodities |

## Manual Asset Types

| Type | Description |
|------|-------------|
| `real_estate` | Property — home, land, rental |
| `vehicle` | Cars, boats, motorcycles |
| `collectible` | Art, watches, coins, wine |
| `business` | Business ownership / equity |
| `other` | Anything else of value |

## Manual Liability Types

| Type | Description |
|------|-------------|
| `mortgage` | Home mortgage |
| `auto_loan` | Car/vehicle loan |
| `student_loan` | Student loans |
| `personal_loan` | Personal / unsecured loans |
| `credit_card_debt` | Carried credit card balance (beyond monthly) |
| `other` | Any other debt |

## Transaction Categories

Auto-categorization maps merchants/descriptions to these categories:

| Category | Pattern Matches |
|----------|----------------|
| Payroll/Income | payroll, direct deposit, salary |
| Transfer | transfer, Zelle, Venmo, PayPal |
| Food & Dining | restaurants, DoorDash, Starbucks |
| Groceries | Kroger, HEB, Walmart, Costco |
| Gas & Auto | Shell, Exxon, gas stations |
| Shopping | Amazon, Best Buy, Apple |
| Bills & Utilities | electric, water, internet, phone |
| Insurance | insurance providers |
| Healthcare | pharmacy, CVS, medical, dental |
| Rent/Mortgage | rent, mortgage, HOA |
| Entertainment | Netflix, Spotify, gaming |
| Travel | airlines, hotels, Uber, Lyft |
| ATM/Cash | ATM withdrawals |
| Fee | bank fees, overdraft |
| Uncategorized | anything unmatched |
