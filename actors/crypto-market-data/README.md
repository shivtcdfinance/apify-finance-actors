# Crypto Market Data

Live cryptocurrency prices, market cap, volume, and rankings from CoinGecko API.

## Features
- **Live Prices** — Current price in 50+ fiat currencies
- **Market Data** — Cap, volume, circulating supply
- **Price Changes** — 1h, 24h, 7d changes
- **All-Time Highs** — ATH price and date

## Input
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| coins | string | yes | bitcoin | Comma-separated CoinGecko IDs |
| vs_currency | string | no | usd | Fiat currency |

## Output
JSON with coin data arrays pushed to default dataset.

| Field | Type | Description |
|-------|------|-------------|
| symbol | string | Ticker (BTC, ETH) |
| current_price | number | Current price |
| market_cap | number | Market capitalization |
| price_change_24h_pct | number | 24h change % |

## Use Cases
- Portfolio tracking
- Market monitoring
- Trading bot integration
