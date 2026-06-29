import json
import urllib.request
import urllib.error

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
        err = e.read().decode()[:500] if e.fp else str(e)
        print('HTTP ' + str(e.code) + ': ' + err[:300])
        return None

categories_to_try = [
    ['AI'],
    ['Finance'],
    ['Finance', 'Developer tools'],
    ['Automation'],
    ['Jobs'],
    []  # empty list
]

for cats in categories_to_try:
    result = api('PUT', '/acts/' + aid, {
        'isPublic': True,
        'categories': cats
    })
    if result:
        print('OK with categories: ' + str(cats))
        print('isPublic: ' + str(result['data'].get('isPublic')))
        print('categories: ' + str(result['data'].get('categories', [])))
        print('Store: https://apify.com/theshivrao/stock-financial-extractor')
        break
    else:
        print('')
