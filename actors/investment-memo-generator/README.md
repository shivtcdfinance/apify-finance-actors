# Investment Memo Generator

Generate professional investment thesis documents with automated data aggregation and narrative structuring.

## Features
- **Company Overview** — Business, industry, competitive advantages
- **Financial Analysis** — 5-year trends, ratios, peer comparison
- **Valuation** — DCF, comparables, scenario analysis
- **Risk Assessment** — Market, operational, financial, regulatory
- **Thesis** — Bull/bear case, catalysts, price targets

## Input
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ticker | string | yes | AAPL | Stock ticker |
| template | string | no | standard | standard, detailed, executive, or pitch |

## Use Cases
- Investment committee memos
- Client portfolio reviews
- Personal investment journaling
## Output

Results are pushed to the default dataset as JSON records. Each record contains the extracted/processed data with a timestamp.

| Field | Type | Description |
|-------|------|-------------|
| status | string | success or error |
| data | object | Processed output data |
| timestamp | string | ISO-8601 timestamp |
