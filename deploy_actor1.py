#!/usr/bin/env python3
"""Deploy Stock & Financial Data Extractor to theshivrao account."""
import json, urllib.request, urllib.error, time

import os
TOKEN = os.environ.get("APIFY_API_TOKEN", "apify_api_placeholder_token_here")
API_BASE = "https://api.apify.com/v2"

def api(method, path, data=None):
    h = {'Authorization': f'Bearer {TOKEN}'}
    if data:
        h['Content-Type'] = 'application/json'
    b = json.dumps(data).encode() if data else None
    r = urllib.request.Request(f'{API_BASE}{path}', data=b, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=30) as f:
            return json.loads(f.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:500] if e.fp else str(e)
        print(f'  ❌ HTTP {e.code}: {err}')
        return None

SOURCE_CODE = r'''"""Stock & Financial Data Extractor — Yahoo Finance + SEC EDGAR"""
import json, urllib.request
from apify import Actor

async def fetch(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=20) as f:
        return json.loads(f.read())

async def main():
    async with Actor() as a:
        i = await a.get_input() or {}
        t = i.get("ticker", "").upper().strip()
        m = i.get("mode", "quote")

        if not t:
            await a.fail("ticker required — try 'AAPL' or 'MSFT'")
            return

        result = {"ticker": t, "mode": m}

        try:
            if m == "quote":
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?interval=1d&range=1d"
                result["data"] = await fetch(url)
                await a.push_event("data-fetched", {"ticker": t, "mode": "quote"})

            elif m == "history":
                period = i.get("period", "10y")
                interval = i.get("interval", "1d")
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range={period}&interval={interval}"
                result["data"] = await fetch(url)
                await a.push_event("data-fetched", {"ticker": t, "mode": "history"})

            elif m == "financials":
                url = f"https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{t}?symbol={t}&type=annualFinancials"
                result["data"] = await fetch(url)
                await a.push_event("data-fetched", {"ticker": t, "mode": "financials"})

            elif m == "sec-filing":
                cik_url = f"https://efts.sec.gov/LATEST/search-index?q=%7B%22q%22%3A%22{t}%22%2C%22forms%22%3A%5B%2210-K%22%5D%2C%22limit%22%3A1%7D"
                cik_r = await fetch(cik_url)
                filings = cik_r.get("hits", {}).get("hits", [])
                if filings:
                    result["filing_url"] = filings[0].get("_source", {}).get("root_form")
                    result["filing_metadata"] = filings[0]["_source"]
                else:
                    result["filing_url"] = None
                    result["message"] = f"No recent 10-K found for {t}"
                await a.push_event("data-fetched", {"ticker": t, "mode": "sec-filing"})

            else:
                await a.fail(f"Unknown mode: {m}. Use: quote, history, financials, sec-filing")
                return

        except Exception as e:
            await a.fail(f"Failed to fetch {m} for {t}: {str(e)}")
            return

        await a.push_data(result)
        await a.set_value("OUTPUT", result)
'''

def deploy():
    print("📦 Creating: stock-financial-extractor")
    r = api('POST', '/acts', {
        'name': 'stock-financial-extractor',
        'title': 'Stock & Financial Data Extractor — Quotes, History, SEC Filings',
        'description': 'Get live stock quotes, 40+ years of historical OHLCV data, financial statements, and SEC EDGAR filings for any US ticker — all from one tool. No API keys needed.'
    })
    if not r:
        print("❌ Create failed")
        return None
    aid = r['data']['id']
    print(f"  ✅ Created: {aid}")

    # Upload source
    up = api('PUT', f'/acts/{aid}/versions/0.0', {
        'versionNumber': '0.0',
        'sourceType': 'SOURCE_FILES',
        'sourceFiles': [{'name': 'main.py', 'content': SOURCE_CODE}],
        'buildTag': 'latest',
    })
    print(f"  {'✅' if up else '❌'} Source uploaded")

    # Ultra-low pricing: $0.001 per fetch (1 cent)
    pr = api('PUT', f'/acts/{aid}/pricing', {
        'pricingModel': 'PAY_PER_EVENT',
        'payPerEventPrices': {'data-fetched': 1}
    })
    print(f"  {'✅' if pr else '⚠️ (may need UI fallback)'} Pricing: $0.01/data-fetched")

    # Metadata — isPublic False for now (we'll publish via browser)
    meta = api('PUT', f'/acts/{aid}', {
        'isPublic': False,
        'categories': ['Finance'],
        'title': 'Stock & Financial Data Extractor',
        'description': 'Get live stock quotes, 40+ years of historical OHLCV data, financial statements, and SEC EDGAR filings for any US ticker. No API keys. 4 modes: quote, history, financials, sec-filing.'
    })
    print(f"  {'✅' if meta else '⚠️'} Metadata set")

    # Build
    b = api('POST', f'/acts/{aid}/builds', {'version': '0.0'})
    if b:
        print(f"  ✅ Build: {b['data']['id']}")
    else:
        print("  ⚠️ Build may have failed")

    return aid

if __name__ == '__main__':
    aid = deploy()
    if aid:
        print(f"\n🏁 Actor: https://console.apify.com/actors/{aid}")
    else:
        print("\n❌ Deployment failed")
