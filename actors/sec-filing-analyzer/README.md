# SEC Filing Analyzer

Parse and extract structured financial data from SEC EDGAR filings (10-K, 10-Q, 8-K, S-1).

## Features
- **Income Statement** — Revenue, COGS, GP, OpEx, EBIT, Net Income
- **Balance Sheet** — Assets, Liabilities, Equity breakdown
- **Cash Flow** — Operating, Investing, Financing
- **MD&A** — Management discussion highlights
- **Risk Factors** — Item 1A extraction
- **Segment Data** — Business/geographic reporting

## Input
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ticker | string | yes | AAPL | Stock ticker |
| filing_type | string | no | 10-K | 10-K, 10-Q, 8-K, S-1 |

## Use Cases
- Automated financial analysis
- Competitive intelligence
- Investment research

## Output

```json
{
  "ticker": "AAPL",
  "filingType": "10-K (Annual)",
  "filings_found": 1,
  "filings": [
    {
      "form": "10-K",
      "company": "Apple Inc.",
      "filing_date": "2025-10-31",
      "period": "2025-09-30",
      "cik": "0000320193",
      "url": "https://www.sec.gov/Archives/edgar/data/320193/...",
      "sics": "3571"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| ticker | string | Input ticker symbol |
| filingType | string | Filing type requested |
| filings_found | number | Number of filings matched |
| filings[].form | string | SEC form type (10-K, 10-Q, etc.) |
| filings[].company | string | Company legal name |
| filings[].filing_date | string | Date filed |
| filings[].period | string | Period ending date |
| filings[].cik | string | SEC Central Index Key |
| filings[].url | string | Link to full filing on SEC EDGAR |
| filings[].sics | string | SIC industry code |
