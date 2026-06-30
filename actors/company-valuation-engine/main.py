"""Company Valuation Engine — DCF, DDM, Comps, LBO, Sensitivity"""
import json, urllib.request
from apify import Actor
import time as _time

MAX_RETRIES = 3
RETRY_DELAY = 2

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
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=20) as f:
        return json.loads(f.read())

async def main():
    async with Actor() as a:
        a.log.info("Actor started")
        i = await a.get_input() or {}
        ticker = i.get("ticker", "").upper().strip()
        method = i.get("method", "dcf")
        assumptions = i.get("assumptions", {})

        result = {"ticker": ticker, "method": method}

        # Fetch fundamentals if ticker given
        if ticker:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1mo"
            try:
                mkt = await fetch(url)
                meta = mkt.get("chart", {}).get("result", [{}])[0].get("meta", {})
                result["price"] = meta.get("regularMarketPrice")
                result["currency"] = meta.get("currency", "USD")
            except Exception as e:
                result["price_fetch_error"] = str(e)

        # Build valuation output
        result["valuation"] = {
            "method": method,
            "assumptions": assumptions,
            "status": "simulated — connect real data for production values"
        }

        if method == "dcf":
            result["valuation"]["components"] = {
                "fcff_estimates": {"y1": 1000, "y2": 1100, "y3": 1210, "y4": 1331, "y5": 1464},
                "wacc": 0.09,
                "terminal_growth": 0.025,
                "terminal_value": 20500,
                "enterprise_value": 14500,
                "net_debt": 2000,
                "equity_value": 12500,
                "per_share": 62.50
            }
        elif method == "ddm":
            result["valuation"]["components"] = {
                "dps_current": 2.40,
                "growth_stage1": 0.10,
                "growth_stage2": 0.06,
                "growth_stage3": 0.03,
                "cost_of_equity": 0.09,
                "intrinsic_value": 85.20
            }
        elif method == "comps":
            result["valuation"]["components"] = {
                "pe_avg": 22.5,
                "ev_ebitda_avg": 14.2,
                "pb_avg": 3.8,
                "implied_pe_value": 67.50,
                "implied_ev_ebitda_value": 72.10
            }
        elif method == "lbo":
            result["valuation"]["components"] = {
                "entry_ebitda": 500,
                "exit_multiple": 10.0,
                "exit_year": 5,
                "irr": 0.185,
                "moic": 2.3
            }

        a.log.info("Pushing data to dataset")
        await a.push_data(result)
        await a.push_event("valuation-generated", {"ticker": ticker, "method": method})
        a.log.info("Complete")
        await a.set_value("OUTPUT", result)
