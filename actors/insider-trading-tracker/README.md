# Insider Trading Tracker

Track SEC Form 4 insider transactions for any US ticker.

## Features
- **Form 4 Filings** — Buys, sells, grants by executives & directors
- **SEC EDGAR** — Direct SEC database access
- **Structured Output** — JSON with filing dates and transaction data

## Input
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ticker | string | yes | AAPL | Stock ticker symbol |
| lookback_days | number | no | 30 | Days to look back |

## Output
Results pushed to default dataset. Each record contains transaction data from Form 4 filings.

| Field | Type | Description |
|-------|------|-------------|
| ticker | string | Input ticker |
| cik | string | SEC Central Index Key |
| company | string | Company name |
| transactions | array | Form 4 transaction records |
| count | number | Number of filings found |

## Use Cases
- Executive sentiment tracking
- Pre-earnings insider activity monitoring
- Investment due diligence
