"""Market News Aggregator — Financial news headlines."""
import json, urllib.request
from apify import Actor

POS = {"beat","surge","jump","rise","gain","record","profit","growth","upgrade","bullish","rally","soar","strong"}
NEG = {"drop","fall","decline","loss","crash","downgrade","bearish","slump","weak","plunge","risk","warning","cut","layoff"}

async def main():
    async with Actor() as a:
        a.log.info("Market News Aggregator starting")
        i = await a.get_input() or {}
        query = i.get("query", "").strip()
        max_articles = min(int(i.get("max_articles", 10)), 50)
        if not query:
            await a.fail("query required")
            return
        articles = []
        try:
            url = "https://finnhub.io/api/v1/news?category=general&token=demo"
            headers = {"User-Agent": "Mozilla/5.0 (alliedcontra)"}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                all_news = json.loads(r.read())
            for art in all_news:
                text = (art.get("headline","") + " " + art.get("summary","")).lower()
                if query.lower() in text:
                    articles.append(art)
                if len(articles) >= max_articles:
                    break
        except Exception as e:
            a.log.warning(f"News fetch: {e}")
        sentiments = {"positive": 0, "negative": 0, "neutral": 0}
        result_articles = []
        for art in articles[:max_articles]:
            h = art.get("headline","").lower()
            p = sum(1 for w in POS if w in h)
            n = sum(1 for w in NEG if w in h)
            s = "positive" if p > n else ("negative" if n > p else "neutral")
            sentiments[s] += 1
            result_articles.append({"title": art.get("headline",""), "source": art.get("source",""), "published": art.get("datetime",""), "url": art.get("url",""), "summary": (art.get("summary","") or "")[:200], "sentiment": s})
        result = {"query": query, "articles_found": len(result_articles), "sentiment_summary": sentiments, "articles": result_articles}
        a.log.info(f"Found {len(result_articles)} articles")
        await a.push_data(result)
        await a.set_value("OUTPUT", result)
        a.log.info("Complete")
