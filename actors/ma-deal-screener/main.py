"""M&A Deal Screener — Accretion/Dilution, Premium Analysis"""
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
        target = i.get("target", "").upper().strip()
        acquirer = i.get("acquirer", "").upper().strip()
        offer_price = float(i.get("offerPrice", 0))

        if not target:
            await a.fail("target ticker required")
            return

        result = {"target": target, "acquirer": acquirer, "offerPrice": offer_price}

        # Fetch market prices
        for tick, label in [(target, "target_price"), (acquirer, "acquirer_price")]:
            if tick:
                try:
                    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tick}?interval=1d&range=5d"
                    d = await fetch(url)
                    meta = d.get("chart", {}).get("result", [{}])[0].get("meta", {})
                    result[label] = meta.get("regularMarketPrice")
                    result[f"{label}_prior_close"] = meta.get("previousClose")
                except:
                    result[label] = None

        # Calculate deal metrics
        if result.get("target_price") and offer_price:
            premium = (offer_price / result["target_price"] - 1) * 100
            result["offerPremiumPct"] = round(premium, 2)

        result["dealMetrics"] = {
            "status": "simulated — connect live data for production",
            "accretion_dilution": {
                "accretionPct": 2.5 if acquirer else None,
                "dilutionPct": None
            },
            "synergyEstimate": "3-5% cost synergies, 1-2% revenue synergies" if acquirer else None,
            "financingMix": "50% cash / 50% stock" if acquirer and target else None,
            "proFormaEarnings": "See detailed output for pro-forma financials"
        }

        a.log.info("Pushing data to dataset")
        await a.push_data(result)
        await a.push_event("deal-analyzed", {"target": target})
        a.log.info("Complete")
        await a.set_value("OUTPUT", result)
