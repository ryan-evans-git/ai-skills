---
name: browser-use
description: Drive a real browser programmatically — for testing, scraping, agent workflows, automation — using Playwright / Puppeteer / CDP, with safety rails (rate limit, robots.txt, headless detection, consent, error handling). Use when the user says "browser automation", "Playwright", "Puppeteer", "scrape", "headless browser", "automate this site", "e2e test framework", "agent that uses a browser".
---

# browser-use

## Purpose

Browsers are the universal interface to the web — increasingly the right tool for agents, scrapers, and end-to-end tests. This skill covers the patterns for driving browsers reliably (selectors, waits, retries), the safety rails for being a polite citizen (rate limit, robots.txt, consent), and the failure modes that catch teams off guard (headless detection, dynamic content, anti-bot).

## When to use

- Writing e2e tests (Playwright, Cypress).
- Building a scraper or data-collection script.
- Agent workflows that need to operate a web UI (filing forms, navigating dashboards).
- Automating workflows on a SaaS app with no API.
- User says: "browser automation", "Playwright", "Puppeteer", "scrape", "headless browser", "automate this site", "agent that uses a browser", "CDP", "Chrome DevTools Protocol".

## Pick a tool

| Tool | Use when |
| --- | --- |
| **Playwright** | Default. Best DX, multi-browser (Chromium, Firefox, WebKit), built-in auto-wait, video / trace recording. |
| **Puppeteer** | Node + Chromium-only. Slightly more mature for Chrome-specific quirks. Choose if Playwright doesn't fit. |
| **Selenium** | Use if existing infrastructure demands it. Other tools are usually nicer. |
| **CDP (Chrome DevTools Protocol)** directly | Low-level access, network interception, performance tracing. Use sparingly — usually Playwright exposes what you need. |
| **`fetch`/HTTP** | If the data has a real API endpoint behind the page, talk to it directly. Always preferable to scraping when possible. |

## Core patterns (Playwright examples; same principles in others)

### 1. Use semantic locators
```ts
// Good — resilient to markup changes
page.getByRole('button', { name: 'Submit' })
page.getByLabel('Email')
page.getByPlaceholder('Search...')
page.getByText('Welcome')

// Avoid — fragile to refactor
page.locator('#submit-btn-2024')
page.locator('.css-1f2g3h4')
page.locator('xpath=//*[@id="root"]/div[2]/...')
```
- Locators that match how a user / assistive tech sees the page survive markup churn.
- Test IDs (`data-testid`) are fine for test-only purposes but worse for production-aware tasks.

### 2. Auto-wait, don't sleep
- Playwright auto-waits for elements to be visible / actionable before clicking.
- **`page.waitForLoadState('networkidle')`** for "page has stopped fetching."
- **`expect(...).toBeVisible()`** with timeout for explicit waits.
- **NEVER `page.waitForTimeout(5000)`** as the primary wait strategy. Flaky.

### 3. Handle dynamic content
- Modern apps load incrementally. Wait for the specific thing you need, not "the page."
- For infinite-scroll: scroll incrementally, wait for new content per scroll.
- For SPA route changes: wait for the new URL AND a known element.

### 4. Retries — yes for scraping, no for testing
- **Scraping**: networks are flaky; built-in retry-with-backoff (3-5 attempts, exponential).
- **Testing**: retries hide flake. Use only at the test-runner level for genuinely-flaky environments, not per-action.

### 5. Headless vs. headed
- **Headless** for CI / production scraping.
- **Headed** when debugging — you can see what's happening.
- **`PWDEBUG=1` / `--debug`** opens Playwright Inspector — step through, inspect state.
- **Video / trace recording** for failures: `playwright.config.ts` → `video: 'retain-on-failure'`, `trace: 'retain-on-failure'`. Lifesaver for debugging CI flakes.

### 6. Network interception
- Mock external APIs in tests for determinism: `page.route('**/api/external/*', route => route.fulfill({ ... }))`.
- For scraping: monitor network to catch the actual data endpoint (often a hidden JSON API).

## Safety rails — being a polite citizen

When the target site is NOT yours:

### Respect robots.txt
- Read `/robots.txt` before crawling at scale.
- Honor `Disallow` directives.
- Honor `Crawl-delay` if specified.
- Tools: `robotparser` (Python), `robots-parser` (Node).

### Rate limit yourself
- Default: ≤ 1 request per second per origin. Slower if the site is small.
- **Backoff on 429 / 503** — exponential, with jitter.
- **Don't run N=100 parallel scrapers** against one origin.

### Identify your user agent
- Send a real user-agent that says who you are: `MyCompany-Bot/1.0 (+https://mycompany.com/bot-info)`.
- Hosts can contact you about misuse if your UA is honest.

### Don't scrape what's behind auth without permission
- A site's auth-wall is a "no" signal. Even if you have valid credentials, the site's ToS usually prohibits automated access.
- Check the ToS. Many forbid scraping outright.

### Personal data
- Scraping public web data is one thing. Scraping personal data — names, emails, photos — has GDPR, CCPA, and ethical implications even when technically public.
- Don't aggregate personal data without a lawful basis.
- Don't republish.

### Anti-bot bypass
- Bypassing CAPTCHAs, rotating fingerprints to dodge detection, etc. — these signal that the site doesn't want your traffic.
- Don't fight the site. Either work with them (ask for API access) or find another data source.

## Headless detection — and what to do about it

Many sites detect headless browsers and serve different (or no) content:

- **Indicators they check**: `navigator.webdriver`, missing fonts, headless-specific properties, missing user-input events.
- **Solutions** (in order of preference):
  1. **Ask for an API.** The polite thing.
  2. **Use a headed browser** in a dedicated machine if scale allows.
  3. **Playwright in `--headed` mode** for stubborn cases.
  4. **`playwright-extra` with stealth plugins** — masks headless indicators. Brittle; sites' detection evolves.
- For YOUR OWN site, don't fight your own tests — disable detection for known user-agents in test environments.

## Agent-use patterns

When an LLM agent operates a browser (e.g. via tool calls):

- **Tool surface should match the page semantics**: `click_button(name)`, `fill_field(label, value)`, `read_page()` — not raw selectors.
- **Confirm before destructive actions**: agent should pause before submitting forms, sending messages, completing purchases (cross-ref `agent-design`).
- **Read-only by default**: most agent browser tasks should be navigate + read, not interact.
- **Trace every action** for audit (cross-ref `audit-log-retention`).
- **Bound the action count** — agents in browser loops can rack up costs fast (cross-ref `agent-design`'s iteration cap).

## Process

1. **Pick the tool** — Playwright unless a specific constraint pushes elsewhere.
2. **Set up trace + video recording** for failed runs.
3. **Write the script using semantic locators + auto-waits.**
4. **For scraping**: respect robots, rate-limit, identify your UA.
5. **For testing**: integrate with CI; use the test runner's retry only at the run level.
6. **Document at `docs/frontend/browser-automation/<purpose>.md`** for non-trivial scripts:
   - Target site / use case.
   - Frequency.
   - Permissions / ToS notes.
   - Owner.
   - How to debug a failure.
7. **Monitor** in production: success rate, error categories, slow runs.

## Anti-patterns

- **`waitForTimeout(N)` as primary wait.** Flaky now and forever.
- **CSS selectors from minified class names.** They WILL change.
- **No trace / video on failures.** Debugging headless CI flakes blind is misery.
- **Hardcoded credentials in scripts.** Use a secret manager.
- **Scraping at high concurrency without rate limits.** You'll be IP-blocked or sued.
- **Ignoring robots.txt because "we're not really a bot."** You are.
- **Headless detection bypass for sites that clearly don't want you.** Wrong fight.
- **Browser automation when an API exists.** Slow, fragile, expensive.

## Cross-references

- `agent-design` — agents using browsers need scoping + audit.
- `audit-log-retention` — browser actions are audit-worthy when agent-driven.
- `qa-test-plan` — browser tests are the e2e tier.
- `flaky-test-management` — browser tests are the flake hotspot.
- `pii-data-handling` — scraped personal data raises classification questions.
- `security-review` — browser automation has its own threat surface (credential exposure, scraper-as-injection-vector).

## Output

The automation / test scripts, plus `docs/frontend/browser-automation/<purpose>.md` for non-trivial uses.
