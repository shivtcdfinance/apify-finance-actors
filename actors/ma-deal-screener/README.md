# M&A Deal Screener

Screen and analyze merger & acquisition targets using financial metrics, deal precedents, and strategic fit scoring.

## Features
- **Target Screening** — Filter by sector, market cap, revenue, growth
- **Precedent Analysis** — Historical deal multiples
- **Accretion/Dilution** — EPS impact analysis
- **Synergy Modeling** — Revenue and cost synergy estimation

## Input
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| sector | string | no | technology | Target sector |
| min_market_cap | number | no | 100M | Minimum market cap |

## Use Cases
- M&A target identification
- Deal valuation
- Strategic planning
## Output

Results are pushed to the default dataset as JSON records. Each record contains the extracted/processed data with a timestamp.

| Field | Type | Description |
|-------|------|-------------|
| status | string | success or error |
| data | object | Processed output data |
| timestamp | string | ISO-8601 timestamp |
