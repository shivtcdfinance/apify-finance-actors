"""SEC Filing Analyzer — Parse EDGAR 10-K, 10-Q, 8-K filings"""
import json, urllib.request, re
from apify import Actor
import time as _time

MAX_RETRIES = 3
RETRY_DELAY = 2

# Map user-friendly filing type values to SEC API form codes
FILING_TYPE_MAP = {
    "10-K (Annual)": "10-K",
    "10-Q (Quarterly)": "10-Q",
    "8-K (Current)": "8-K",
    "S-1 (IPO)": "S-1",
    "All Filings": "",
}

async def _fetch_with_retry(fn, *args):
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
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (theshivrao)"})
    with urllib.request.urlopen(r, timeout=30) as f:
        return f.read().decode()

async def main():
    async with Actor() as a:
        a.log.info("SEC Filing Analyzer starting...")
        i = await a.get_input() or {}
        ticker = i.get("ticker", "").upper().strip()
        filing_type_raw = i.get("filing_type", "10-K (Annual)")
        count = int(i.get("count", 1))

        # Map user-friendly value to SEC form code
        filing_form = FILING_TYPE_MAP.get(filing_type_raw, "10-K")
        a.log.info(f"Analyzing {ticker} — {filing_type_raw} (SEC form: {filing_form})")

        if not ticker:
            await a.fail("ticker required")
            return

        result = {"ticker": ticker, "filingType": filing_type_raw, "filingForm": filing_form}

        # Build SEC EDGAR search URL
        forms_query = f'%22{filing_form}%22' if filing_form else '%22%22'
        search_url = f"https://efts.sec.gov/LATEST/search-index?q=%7B%22q%22%3A%22{ticker}%22%2C%22forms%22%3A%5B{forms_query}%5D%2C%22limit%22%3A{count}%7D"
        try:
            search_r = json.loads(await fetch(search_url))
            hits = search_r.get("hits", {}).get("hits", [])
            result["filings_found"] = len(hits)
            result["filings"] = []
            for h in hits:
                src = h.get("_source", {})
                result["filings"].append({
                    "form": src.get("form"),
                    "company": src.get("company_name"),
                    "filing_date": src.get("filing_date"),
                    "period": src.get("period_ending"),
                    "cik": src.get("cik"),
                    "url": src.get("root_form"),
                    "sics": src.get("sics"),
                })
            a.log.info(f"Found {len(hits)} filing(s) for {ticker}")
        except Exception as e:
            a.log.warning(f"SEC search error: {e}")
            result["search_error"] = str(e)

        await a.push_data(result)
        await a.push_event("filing-parsed", {"ticker": ticker, "count": len(result.get("filings", []))})
        await a.set_value("OUTPUT", result)
        a.log.info("SEC Filing Analyzer complete")
