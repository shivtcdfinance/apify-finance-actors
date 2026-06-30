"""Insider Trading Tracker — SEC Form 4 filings."""
import json, urllib.request, re
from apify import Actor

async def main():
    async with Actor() as a:
        a.log.info("Starting")
        i = await a.get_input() or {}
        ticker = i.get("ticker", "").upper().strip()
        if not ticker:
            await a.fail("ticker required")
            return
        h = {"User-Agent": "Mozilla/5.0 (alliedcontra)"}
        req = urllib.request.Request("https://www.sec.gov/files/company_tickers.json", headers=h)
        with urllib.request.urlopen(req, timeout=15) as r:
            companies = json.loads(r.read())
        cik = None
        for _, v in companies.items():
            if v.get("ticker","").upper() == ticker:
                cik = str(v["cik_str"]).zfill(10)
                break
        if not cik:
            await a.fail(f"Ticker {ticker} not found")
            return
        a.log.info(f"CIK: {cik}")
        req = urllib.request.Request(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=h)
        with urllib.request.urlopen(req, timeout=15) as r:
            filings = json.loads(r.read())
        result = {"ticker": ticker, "cik": cik, "company": filings.get("name",""), "transactions": []}
        recent = filings.get("filings",{}).get("recent",{})
        forms, dates, accs = recent.get("form",[]), recent.get("filingDate",[]), recent.get("accessionNumber",[])
        count = 0
        for idx, form in enumerate(forms):
            if form != "4": continue
            count += 1
            acc = accs[idx] if idx < len(accs) else ""
            try:
                u = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-','')}/{acc}-index.htm"
                req = urllib.request.Request(u, headers=h)
                with urllib.request.urlopen(req, timeout=10) as r2:
                    html = r2.read().decode("utf-8", errors="ignore")
            except: continue
            cells = re.findall(r"<td[^>]*>(.*?)</td>", html, re.DOTALL)
            result["transactions"].append({"filing_date": dates[idx] if idx < len(dates) else "", "cells": [re.sub(r"<[^>]+>","",c).strip() for c in cells[:8]]})
            if count >= 3: break
        result["count"] = len(result["transactions"])
        a.log.info(f"Found {result['count']} filings")
        await a.push_data(result)
        await a.set_value("OUTPUT", result)
        a.log.info("Complete")
