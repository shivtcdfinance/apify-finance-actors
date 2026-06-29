import json
import urllib.request
import urllib.error
import time

p = chr(47) + 'tmp' + chr(47) + 'apify_theshivrao_token'
with open(p) as f:
    T = f.read().strip()
B = 'https://api.apify.com/v2'
aid = 'ixAEgo7pTFdnMcAYp'

def api(m, pt, d=None):
    h = {'Authorization': 'Bearer ' + T}
    if d:
        h['Content-Type'] = 'application/json'
    b = json.dumps(d).encode() if d else None
    r = urllib.request.Request(B + pt, data=b, headers=h, method=m)
    try:
        with urllib.request.urlopen(r, timeout=30) as f:
            return json.loads(f.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:300] if e.fp else str(e)
        print('HTTP ' + str(e.code) + ': ' + err[:200])
        return None

for i in range(8):
    time.sleep(3)
    b = api('GET', '/acts/' + aid + '/builds/qBjfG36u1Rz4UKcZm')
    if b:
        s = b['data']['status']
        print('[' + str(i+1) + '] ' + s)
        if s in ('SUCCEEDED', 'FAILED'):
            break

pr = api('PUT', '/acts/' + aid + '/pricing', {'pricingModel': 'PAY_PER_EVENT', 'payPerEventPrices': {'data-fetched': 1}})
print('Pricing: ' + ('OK' if pr else 'FAIL'))

pub = api('PUT', '/acts/' + aid, {'title': 'Stock & Financial Data Extractor', 'description': 'Get live stock quotes, 40yr historical OHLCV, financials, and SEC EDGAR filings for any ticker. 4 modes: quote history financials sec-filing. No API keys needed. Export JSON CSV.', 'isPublic': True})
print('Publish: ' + ('OK' if pub else 'FAIL'))

info = api('GET', '/acts/' + aid)
if info:
    d = info['data']
    print('Store: https://apify.com/theshivrao/' + d['name'])
    print('Public: ' + str(d.get('isPublic')))
