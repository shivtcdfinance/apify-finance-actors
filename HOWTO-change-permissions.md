# Apify Actor Permissions: LIMITED → FULL_PERMISSIONS

## Problem

When an Apify actor has `actorPermissionLevel: LIMITED_PERMISSIONS`, builds fail if the actor directory includes an `OUTPUT_SCHEMA.json` file. Only `FULL_PERMISSIONS` actors can build with output schema files.

The API does **not** expose a permissions endpoint — this must be done via the Apify Console web UI using Chrome CDP.

---

## Prerequisites

1. **Chrome with CDP on port 9222** — start with:
   ```
   open -a "Google Chrome" --args --remote-debugging-port=9222
   ```
2. **Apify Console authenticated** — logged into the target org (e.g. `crCwwLfU97q6VBpLE` for Allied Contractors)
3. **Hermes Agent** with `computer_use` tool available

---

## CDP Workflow (Hermes Agent)

For each actor, navigate to `https://console.apify.com/actors/<ACTOR_ID>/settings`.

Then:

1. **Capture the settings page** — find the permissions React-select dropdown
2. **Click on the permissions dropdown** — activates the React-select menu
3. **Type `FULL_PERMISSIONS`** — filters the dropdown list
4. **Press Enter** — selects the option
5. **Click Save** — submits the change
6. **Verify** — capture again; dropdown should show "Full permissions"

Keyboard method is far more reliable than trying to click the virtualised React-select option elements directly.

---

## Actor ID Reference (Allied Contractors — crCwwLfU97q6VBpLE)

| # | Actor | ID | Status |
|---|-------|----|--------|
| 1 | stock-financial-extractor | ixAEgo7pTFdnMcAYp | ✅ Already FULL |
| 2 | stock-financial-extractor-v2 | SxmgKbrsTqcXSO8MY | ✅ Fixed |
| 3 | company-valuation-engine | YiPOgO0iESk6VfCnL | ✅ Fixed |
| 4 | financial-ratios-analyzer | 6BdxL6hdDI1hcxAs1 | ✅ Fixed |
| 5 | portfolio-risk-optimizer | GHabYgLJu8slI5Tjz | ✅ Fixed |
| 6 | investment-memo-generator | 93SXYiSeSStCwNFct | ✅ Fixed |
| 7 | sec-filing-analyzer | RYIgANjZH6clDHuzO | ✅ Fixed |
| 8 | ma-deal-screener | qXhP2m36uXcbLjVfS | ✅ Fixed |
| 9 | dividend-analysis-tool | H3m9Q0eBlZmh3mAqI | ✅ Fixed |
| 10 | economic-indicators-dashboard | lpXTMOTOmhkcWT30O | ✅ Fixed |
| 11 | options-pricing-calculator | 8sDZHyewgqwA2BMaN | ✅ Fixed |

---

## After Permissions Fix

1. **Rebuild all actors** (via Apify API — POST to `/v2/acts/<ID>/builds`)
2. **Publish to Store** (up to 5/day via POST to `/v2/store/publishes`)
3. **Verify** each actor's Store listing shows a successful build
