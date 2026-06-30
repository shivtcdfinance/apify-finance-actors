"""Stock & Financial Data Extractor — Yahoo Finance + SEC EDGAR"""
import json, urllib.request
from apify import Actor

MAX_RETRIES = 3
RETRY_DELAY = 2

async def _fetch_with_retry(fn, *args):
    """Retry wrapper with exponential backoff."""
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return await fn(*args)
        except Exception as e:
            last_err = e
            if attempt < MAX_RETRIES:
                await Actor._sleep(RETRY_DELAY * attempt)
    raise last_err


async def fetch(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=20) as f:
        return json.loads(f.read())

async def main():
    async with Actor() as a:
        a.log.info("Actor started")
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

        a.log.info("Pushing data to dataset")
        await a.push_data(result)
        a.log.info("Complete")
        await a.set_value("OUTPUT", result)
