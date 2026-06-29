# Apify theshivrao — Production Deployment Plan (Updated v2)

**Date:** 2026-06-27 (Updated)  
**Account:** theshivrao@gmail.com  
**Role:** Production/monetization account for ApplyGen AI Finance Actors

## Strategy

| Aspect | shivtcdfinance (dev) | theshivrao (production) |
|--------|---------------------|------------------------|
| Actor count | 10+ individual | **11 smart actors** |
| Source | Public | **Hidden** (private) |
| Pricing | Market-tested | Ultra-low → raise after 100 users |
| Purpose | Dev/staging | Revenue + store ranking |
| Public Profile | ✅ Live | ✅ Live (just enabled) |

## Actor Roadmap — All 11 Actors

| # | Name | Methods | Pricing | Build | Published |
|---|------|---------|---------|-------|-----------|
| 1 | Stock & Financial Data Extractor | Yahoo quote/history/financials + SEC EDGAR | $0.01/data-fetched | ✅ Built | ❌ Needs terms |
| 2 | Company Valuation Engine | DCF, DDM, Comps, LBO, sensitivity | $0.03/valuation-generated | ✅ Built | ❌ Needs terms |
| 3 | Financial Ratios Analyzer | 25+ ratios, DuPont, Altman Z, EPS | $0.01/analysis-completed | ✅ Built | ❌ Needs terms |
| 4 | Portfolio Risk & Optimizer | Monte Carlo, VaR/CVaR, Mean-Variance, BL | $0.04/optimization-completed | ✅ Built | ❌ Needs terms |
| 5 | Investment Memo Generator | Full workflow → formatted report | $0.08/memo-generated | ✅ Built | ❌ Needs terms |
| 6 | SEC Filing Analyzer | Parse 10-K/10-Q/8-K from EDGAR | $0.03/filing-parsed | ✅ Built | ❌ Needs terms |
| 7 | M&A Deal Screener | Accretion/dilution, premiums, synergies | $0.05/deal-analyzed | ✅ Built | ❌ Needs terms |
| 8 | Dividend Analysis Tool | History, yield, growth, coverage | $0.01/dividend-analyzed | ✅ Built | ❌ Needs terms |
| 9 | Economic Indicators Dashboard | GDP, CPI, rates, employment, PMI | $0.01/indicators-fetched | ✅ Built | ❌ Needs terms |
| 10 | Options Pricing Calculator | Black-Scholes, Greeks, strategies | $0.02/option-priced | ✅ Built | ❌ Needs terms |

## Actor IDs & Console URLs

| # | Name | ID | Console |
|---|------|----|---------|
| 1 | stock-financial-extractor | ixAEgo7pTFdnMcAYp | [Link](https://console.apify.com/actors/ixAEgo7pTFdnMcAYp) |
| 2 | company-valuation-engine | YiPOgO0iESk6VfCnL | [Link](https://console.apify.com/actors/YiPOgO0iESk6VfCnL) |
| 3 | financial-ratios-analyzer | 6BdxL6hdDI1hcxAs1 | [Link](https://console.apify.com/actors/6BdxL6hdDI1hcxAs1) |
| 4 | portfolio-risk-optimizer | GHabYgLJu8slI5Tjz | [Link](https://console.apify.com/actors/GHabYgLJu8slI5Tjz) |
| 5 | investment-memo-generator | 93SXYiSeSStCwNFct | [Link](https://console.apify.com/actors/93SXYiSeSStCwNFct) |
| 6 | sec-filing-analyzer | RYIgANjZH6clDHuzO | [Link](https://console.apify.com/actors/RYIgANjZH6clDHuzO) |
| 7 | ma-deal-screener | qXhP2m36uXcbLjVfS | [Link](https://console.apify.com/actors/qXhP2m36uXcbLjVfS) |
| 8 | dividend-analysis-tool | H3m9Q0eBlZmh3mAqI | [Link](https://console.apify.com/actors/H3m9Q0eBlZmh3mAqI) |
| 9 | economic-indicators-dashboard | lpXTMOTOmhkcWT30O | [Link](https://console.apify.com/actors/lpXTMOTOmhkcWT30O) |
| 10 | options-pricing-calculator | 8sDZHyewgqwA2BMaN | [Link](https://console.apify.com/actors/8sDZHyewgqwA2BMaN) |

## Blocker

- [ ] **Accept Apify Store Terms** — Go to https://console.apify.com/actors/ixAEgo7pTFdnMcAYp/publication in incognito, sign in with Google as theshivrao, accept terms once
- [ ] After terms accepted → I can batch-publish all 10 via API

## Deployment Scripts
- `deploy_actor1.py` → Actor #1
- `deploy_actors_2-5.py` → Actors #2-#5  
- `deploy_actors_6-10.py` → Actors #6-#10 (sec-filing, ma-screener, dividend, economics, options)
- `publish_all.py` → API-based publishing script
