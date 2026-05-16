---
name: modal-and-dialog-design
description: Design and implement accessible, robust modal dialogs — focus trap, scroll lock, ESC handling, ARIA roles, click-outside behavior, route-awareness, mobile patterns (bottom sheet vs. full-screen). Use when building any modal / dialog / drawer / bottom sheet, or when the user says "modal", "dialog", "drawer", "popover", "bottom sheet", "overlay".
---

# modal-and-dialog-design

## Purpose

Modals are deceptively hard. They have an accessibility specification (WAI-ARIA dialog pattern) most implementations get wrong, plus UX subtleties around focus, scroll, dismissal, and routing that bite when ignored. This skill is the patterns + the WAI-ARIA conformance checklist.

## When to use

- Building any modal, dialog, drawer, popover, or bottom sheet.
- Reviewing an existing modal that's "kinda working but flaky."
- After an a11y audit that flagged modals.
- User says: "modal", "dialog", "drawer", "popover", "bottom sheet", "overlay", "lightbox", "confirmation prompt".

## First — should it be a modal?

Modals interrupt. Use them when the user must act before continuing. Don't use them for:
- **Confirmations of common actions** that have undo. Use a toast with undo instead.
- **Form input** that could be inline. Inline is usually better.
- **Marketing / upsell**. Disruptive.
- **Onboarding tours**. Tooltips on the actual UI are usually better.

Use modals for:
- **Destructive confirmations** (delete account, irreversible operations).
- **Multi-field input** that doesn't fit inline (compose message, create resource).
- **Workflow interruptions** where context is helpful (pick a payment method during checkout).
- **Image / video lightbox**.

Use **drawers** (side panels) instead when the user might want to keep referring to the underlying page (e.g. a settings panel, a detail view).

Use **bottom sheets** on mobile when a modal would feel intrusive — slides up from the bottom, feels native.

## The WAI-ARIA dialog pattern (mandatory)

A modal that's *actually* accessible must:

### Markup
- Root element: `role="dialog"` (or `role="alertdialog"` for urgent prompts that need immediate response).
- `aria-modal="true"` to indicate it's modal.
- `aria-labelledby` pointing at the title element (or `aria-label` if no visible title).
- Optionally `aria-describedby` pointing at the description / body.

### Focus management
- **On open**: focus moves into the modal — typically to the first interactive element, OR to the modal's container if it has a focusable wrapper. For destructive confirmations, focus the SAFE option (Cancel), not the dangerous one.
- **Focus trap**: Tab cycles within the modal. Shift+Tab cycles backward. Tab from the last element wraps to the first.
- **On close**: focus returns to the element that opened the modal. Critical — without this, screen reader users are stranded.

### Keyboard
- **ESC closes the modal** (unless explicitly disabled for destructive workflows — even then, prefer to dismiss).
- Enter on the default action.

### Backdrop / overlay
- Click outside (on the backdrop) typically closes — but NOT for:
  - Destructive confirmations (accidental dismiss = bad).
  - Forms with unsaved input (warn first).
- Backdrop has its own ARIA semantics: shouldn't be a clickable button reachable by keyboard.

### Scroll lock
- The page behind the modal must NOT scroll when the modal is open. Otherwise scrolling within the modal can leak to the page.
- Common bug: `body { overflow: hidden }` works on desktop but on iOS Safari, the page scrolls anyway. Use a tested library or lock with `position: fixed` + scroll-restoration.

### Inert background
- Content outside the modal should be unreachable by screen readers and not focusable.
- HTML `inert` attribute (modern) or `aria-hidden="true"` on background.

### Route-awareness
- **Back button closes the modal** (or navigates to a prior step in multi-step modals). Implement as either:
  - History entry per modal-open (`window.history.pushState`); back button triggers close.
  - Route-based modals where the URL contains the modal state (`/users/123?modal=delete`).
- Especially important on mobile where back is muscle memory.

## Don't build modals from scratch

Implementing the WAI-ARIA dialog pattern correctly is hard. Use:
- **Radix Dialog** / **Headless UI Dialog** / **React Aria Dialog** — headless, accessible.
- **shadcn/ui Dialog** — Radix-based with styled defaults.
- **Reach Dialog** — minimal accessible dialog.

Implementing it yourself is acceptable only if you're maintaining a design system that has its own component primitives — and even then, lean on these libraries' implementations as reference.

## UX patterns

### Title and structure
- Clear title (`<h2>` typically).
- Body content.
- Action area at the bottom: primary action on the right (in LTR languages), cancel/secondary on the left.
- Close button (X) typically in the top-right.

### Confirmations (alertdialog)
- Use `role="alertdialog"` for destructive prompts — screen readers announce it more aggressively.
- Cross-ref `ui-copy`: specific prompt + named action buttons.
  - Bad: "Are you sure?" / OK / Cancel.
  - Better: "Delete this comment?" / "This can't be undone." / [Delete comment] [Keep it].

### Multi-step modals (wizards inside dialogs)
- Show progress (step X of Y).
- Allow Back without losing data.
- ESC asks "you have unsaved changes — close anyway?" if the user has made progress.

### Mobile patterns
- **Bottom sheet**: slides up from bottom, sticky at the top of the visible viewport (above on-screen keyboard).
- **Full-screen takeover**: for complex tasks, opens like a new page.
- **Avoid centered desktop modals on phones** — usually too small, hard to dismiss.

### Stacked modals
- Mostly: avoid. Stacked modals are a UX smell.
- If unavoidable (e.g. a confirm inside a modal): only one is "the focus"; the underneath modal becomes inert.
- Closing the top should return to the bottom, not all the way out.

## Implementation checklist

For any new modal, verify:

- [ ] `role="dialog"` (or `"alertdialog"`).
- [ ] `aria-modal="true"`.
- [ ] `aria-labelledby` pointing at title.
- [ ] Focus moves in on open.
- [ ] Focus trapped within (Tab cycles).
- [ ] Focus returns to opener on close.
- [ ] ESC closes (or warns for destructive flows).
- [ ] Backdrop click closes (or warns).
- [ ] Background scroll locked.
- [ ] Background inert / aria-hidden.
- [ ] Back button closes (mobile).
- [ ] Tested with screen reader.
- [ ] Tested at small screens (mobile pattern works).
- [ ] Works with on-screen keyboard up (mobile).
- [ ] States designed: loading, error, success-and-close.

## Process

1. **Decide if it should be a modal** at all. Often the answer is no.
2. **Pick the pattern**: dialog / alertdialog / drawer / bottom sheet / full-screen.
3. **Use a vetted headless library**. Don't roll your own dialog primitive.
4. **Implement the checklist above.**
5. **Test**:
   - Keyboard only.
   - Screen reader (VoiceOver / NVDA).
   - Mobile (touch, on-screen keyboard, back button).
6. **Cross-ref `a11y-audit`** — modals are a frequent finding.

## Anti-patterns

- **`<div>` with `display: none/block` and no ARIA.** Invisible to screen readers; no focus management.
- **`tabindex="0"` everywhere** to enable focus instead of using semantic elements.
- **Custom close button without aria-label.** Just an X icon; screen reader says "button."
- **No focus trap.** Tab leaves the modal into the background; user gets lost.
- **No focus restoration.** After closing, focus is at the body root.
- **ESC ignored.** Frustrating for keyboard users.
- **Background scrolls behind the modal.** Especially on iOS Safari.
- **Stacked modals with all-active focus.** Chaos.
- **Centered desktop modal on phone.** Tiny, hard to dismiss.

## Cross-references

- `a11y-audit` — modals are a top a11y failure point.
- `frontend-design` — dialog styling.
- `ui-copy` — what dialogs say.
- `component-architecture` — compound components for dialog parts.
- `form-design` — forms-in-modals have their own state management.
- `loading-and-error-states` — modal-internal async.

## Output

Modal components using a vetted headless library + design-system styling, with the implementation checklist verified.
