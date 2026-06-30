# Company Valuation Engine

Multi-method company valuation using DCF, comparable company analysis, and precedent transactions.

## Features
- **DCF Model** — Free cash flow projection, WACC, terminal value
- **Comparable Analysis** — EV/EBITDA, P/E, P/B, P/S multiples vs peers
- **Precedent Transactions** — Historical M&A deal multiples
- **Sensitivity Analysis** — Monte Carlo simulation

## Input
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ticker | string | yes | AAPL | Stock ticker |
| method | string | no | dcf | dcf, comparables, precedents, or all |

## Use Cases
- Investment thesis development
- M&A target valuation
- Equity research
## Output

Results are pushed to the default dataset as JSON records. Each record contains the extracted/processed data with a timestamp.

| Field | Type | Description |
|-------|------|-------------|
| status | string | success or error |
| data | object | Processed output data |
| timestamp | string | ISO-8601 timestamp |
