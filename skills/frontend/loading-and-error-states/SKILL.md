---
name: loading-and-error-states
description: Design and implement loading and error states — skeleton screens, spinners, optimistic UI, error boundaries, retry patterns, partial-failure handling. Use when building any async UI, when an interface "feels janky" on slow networks, when the user says "loading state", "skeleton", "error boundary", "retry", "optimistic UI", "empty state".
---

# loading-and-error-states

## Purpose

Most UIs are designed for the happy path: data loaded, network instant, no errors. Real users have slow networks, half-failed requests, and partial data. This skill is the patterns for the other 80% of the time — states that make a slow / broken interface still feel considered.

## When to use

- Building any UI that fetches data, calls an API, or runs async work.
- Existing UI feels "janky" on slow connections.
- After an incident where users saw a confusing failure.
- User says: "loading state", "skeleton", "spinner", "error boundary", "retry", "optimistic UI", "empty state", "fallback UI".

## The four async UI states

Every async UI has four states. Design each explicitly:

1. **Idle / empty** — no data yet, no fetch in progress.
2. **Loading** — fetch in progress.
3. **Success** — data loaded.
4. **Error** — fetch failed or returned an error.

Plus often:
5. **Partial / stale** — some data loaded, some still loading or failed.
6. **Refreshing** — re-fetching while showing old data.

## Loading patterns — pick the right one

### Spinner
- Use for: short waits (< 1-2s), full-page transitions where layout would shift, anywhere a skeleton doesn't add value.
- **Centered + animated**; size proportional to context.
- **Wait 200-300ms before showing** — for fast networks, the spinner appears and vanishes before the user perceives it, creating a "flash" that feels worse than no spinner.

### Skeleton screen
- Use for: list pages, profile cards, anything where the layout is known ahead of data.
- **Match the actual layout** — skeleton shape should resemble the real content.
- **Subtle animation** (shimmer or pulse) to indicate liveness.
- **Don't skeleton if data loads in < 300ms** — pop-in is fine for fast paths.

### Progress bar / determinate
- Use when you can measure progress: file uploads, multi-step jobs, batch operations.
- **Show percentage AND remaining time** if both are knowable.
- **Don't fake it** — if you don't have real progress, use indeterminate (spinner or skeleton).

### Optimistic UI
- Use when the action's success is very likely (≥99%): liking, voting, adding to cart, toggling settings.
- **Render the optimistic state immediately**, send the request in the background.
- **Reconcile on response**: roll back + show error if it failed.
- **Disable conflicting actions** during the pending state.
- Don't use for high-stakes actions (payment, irreversible destructive operations) — surprises are worse there.

### Streaming / progressive
- Use when content arrives incrementally: LLM token streaming, large data tables.
- Show data as it arrives; mark areas still loading.
- Resist the urge to wait for everything.

### No loading state at all
- Use when the response is genuinely instant (cached data, client-side computation).
- Or when the action gives instant visual feedback another way (a row appearing).

## Error patterns

### Inline error
- For form fields, individual actions: error appears next to the failing element.
- Cross-ref `form-design` for form-specific patterns.

### Toast / banner
- For non-blocking errors: "Couldn't save your preferences. Retry?" appears as a toast.
- Auto-dismissing fine for transient errors; sticky for ones requiring action.
- **Provide a retry button**; don't make the user re-do the whole action.
- **Don't bury the failure detail** — say what failed and what the user can do.

### Full-page error state
- For loading failures of the primary page content.
- Include:
  - **What happened** in plain language.
  - **A retry button** that re-runs the fetch.
  - **A way out** (back / home / contact support) if retry won't help.
  - **Diagnostic info** (request ID, error code) — usable by support but unobtrusive.
- Don't show a stack trace.

### Error boundaries (React) / equivalent in other frameworks
- Catch render-time errors so one broken component doesn't blank the page.
- Show a contained fallback UI for the broken section; rest of the app keeps working.
- Log the error to monitoring (cross-ref `logging-standards`).

### Network-offline state
- Detect offline (`navigator.onLine` + service worker for accuracy).
- Show a persistent banner: "You're offline. Changes will sync when you reconnect."
- Queue mutations locally if the app supports it.

### Partial failures
- Some data loaded, some failed.
- Show what you have; mark what failed with a per-item retry.
- Don't blank the page when 90% of it works.

## Patterns by surface

### Lists / tables
- **Loading**: skeleton rows matching the table structure.
- **Empty**: meaningful empty state with CTA (cross-ref `ui-copy`).
- **Error**: error state with retry, ideally keeping any cached data visible.
- **Loading more (infinite scroll)**: spinner at the bottom of the list.

### Detail pages
- **Loading**: skeleton matching the layout (header, body, sidebar).
- **Not found (404)**: explicit "not found" with link back.
- **Permission denied (403)**: "You don't have access" with contact path.

### Forms (cross-ref `form-design`)
- **Submitting**: button shows spinner + "Saving..."; disabled.
- **Async validation pending**: small indicator in the field.
- **Submit failure**: form-level error at top + restore button to enabled.

### Search
- **Empty**: "Try searching for..." with suggestions.
- **Searching**: spinner inline with the search bar (not full-page).
- **No results**: "No results for X" with suggestions / "Clear filters."
- **Slow search**: debounced; cancel previous request when a new one starts.

### Modals / dialogs
- **Opening with content from a fetch**: show modal with a skeleton; don't make user wait for fetch before opening.
- **Action fails**: error inline in the modal; don't close it.

## Error boundaries — implementation notes

- Wrap routes and significant sub-trees, not individual components.
- Reset on route change (otherwise an error sticks across navigations).
- Don't catch errors and silently re-render — that's a bug, not a recovery.
- Log to monitoring with full context.

## Retry strategy

- **User-initiated retry**: a button in the error UI. Always offer this.
- **Auto-retry**: only for transient errors (network blip), with exponential backoff and a max attempts cap. Don't auto-retry user errors.
- **Idempotency**: mutations need idempotency keys if you're going to retry (cross-ref `resilience-patterns`).
- **Don't retry on 4xx** (except 429). 401 / 403 / 404 won't change.

## Process

1. **List the async surfaces** in the UI being built.
2. **For each, decide the four states** (idle / loading / success / error) plus optional fifth (partial).
3. **Pick the loading pattern** per surface — skeleton, spinner, optimistic, streaming, none.
4. **Design the error UI** per surface — inline, toast, full-page, error boundary.
5. **Decide retry behavior** — manual, auto with backoff, none.
6. **Test with throttled network** (Chrome DevTools "Slow 3G") and offline mode.
7. **A11y**: spinners need `aria-live`; error messages need `role="alert"` (cross-ref `a11y-audit`).

## Anti-patterns

- **Spinner with no debounce** — flashes on fast loads.
- **Skeleton wildly different from the real content** — defeats the purpose.
- **"Error" with no detail or retry** — user has to guess and refresh.
- **Full-page error on any failure** — even partial failures blank the page.
- **No error boundary** — one broken component blanks the whole app.
- **Optimistic UI on irreversible actions** — silent rollback isn't possible.
- **Infinite spinner** — no timeout, no error state, just spins forever.
- **Loading state inside the spinner that loads** — recursive abyss.
- **Retries on 4xx errors** — never going to work.

## Cross-references

- `frontend-design` — these states are part of the design.
- `ui-copy` — what each state says.
- `form-design` — form-specific async states.
- `a11y-audit` — `aria-live`, `role="alert"`, focus handling on errors.
- `resilience-patterns` — backend retry / idempotency.

## Output

Components implementing each async state. For complex apps, `docs/frontend/async-patterns.md` documenting the conventions.
