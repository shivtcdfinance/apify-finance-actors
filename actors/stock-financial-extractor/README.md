# Stock & Financial Data Extractor

Real-time stock quotes, OHLCV historical data, and fundamental financial metrics from Yahoo Finance.

## Features
- **Live Quotes** — Price, change, volume, market cap, P/E, dividend yield
- **OHLCV History** — Daily/weekly/monthly bars with configurable date ranges
- **Financial Statements** — Income statement, balance sheet, cash flow
- **Key Statistics** — 50+ valuation metrics and ratios

## Input
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ticker | string | yes | AAPL | Stock ticker |
| mode | string | no | quote | quote, history, financials, or full |

## Use Cases
- Real-time stock dashboards
- Financial model data feeds
- Portfolio tracking
## Output

Results are pushed to the default dataset as JSON records. Each record contains the extracted/processed data with a timestamp.

| Field | Type | Description |
|-------|------|-------------|
| status | string | success or error |
| data | object | Processed output data |
| timestamp | string | ISO-8601 timestamp |
