# Market News Aggregator

Aggregate financial news headlines for stocks, sectors, and topics. Multi-source with sentiment scoring.

## Features
- **Headline Aggregation** — News from financial sources
- **Sentiment Scoring** — Positive/negative/neutral classification
- **Source Attribution** — Publisher and date per article

## Input
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | yes | Apple | Ticker, company, or topic |
| max_articles | number | no | 10 | Max articles (1-50) |

## Output
Articles array with titles, sources, URLs, and sentiment pushed to dataset.

| Field | Type | Description |
|-------|------|-------------|
| title | string | Article headline |
| source | string | Publisher name |
| sentiment | string | positive/negative/neutral |
| url | string | Article link |

## Use Cases
- Pre-market research
- Event-driven signals
- Risk monitoring
