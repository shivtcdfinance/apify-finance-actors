"""Crypto Market Data — CoinGecko free API."""
import json, urllib.request
from apify import Actor

async def main():
    async with Actor() as a:
        a.log.info("Crypto Market Data starting")
        i = await a.get_input() or {}
        coins_input = i.get("coins", "bitcoin")
        vs_currency = i.get("vs_currency", "usd").lower()
        if isinstance(coins_input, list):
            coins = coins_input
        else:
            coins = [c.strip() for c in coins_input.split(",")]
        if not coins:
            await a.fail("At least one coin required")
            return
        coin_ids = ",".join(coins[:50])
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={vs_currency}&ids={coin_ids}&order=market_cap_desc&per_page=50&page=1&sparkline=false&price_change_percentage=1h,24h,7d"
        headers = {"User-Agent": "Mozilla/5.0 (alliedcontra)"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        a.log.info(f"Fetched {len(data)} coins")
        result = {"vs_currency": vs_currency, "coin_count": len(data), "coins": []}
        for coin in data:
            result["coins"].append({
                "id": coin.get("id"), "symbol": coin.get("symbol"), "name": coin.get("name"),
                "current_price": coin.get("current_price"), "market_cap": coin.get("market_cap"),
                "market_cap_rank": coin.get("market_cap_rank"), "total_volume": coin.get("total_volume"),
                "high_24h": coin.get("high_24h"), "low_24h": coin.get("low_24h"),
                "price_change_24h_pct": coin.get("price_change_percentage_24h"),
                "circulating_supply": coin.get("circulating_supply"),
                "ath": coin.get("ath"), "ath_date": coin.get("ath_date"),
            })
        await a.push_data(result)
        await a.set_value("OUTPUT", result)
        a.log.info(f"Complete - {len(result['coins'])} coins")
