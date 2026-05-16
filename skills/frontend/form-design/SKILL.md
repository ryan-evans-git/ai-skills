---
name: form-design
description: Design and implement forms — field types, labels, validation timing, error UX, multi-step flows, complex inputs (autocomplete, date, file), and accessibility. Use when building any form (signup, checkout, settings, search, profile, contact, anything with user input), or when the user says "form", "input validation", "form UX", "multi-step form", "wizard", "autocomplete", "date picker", "file upload".
---

# form-design

## Purpose

Forms are most of frontend by surface area. Done well, they make hard tasks feel easy; done badly, they're the #1 source of abandonment, accessibility complaints, and "this app feels janky" feedback. This skill covers the patterns that separate the two.

## When to use

- Building any form: signup, login, checkout, settings, search, profile, contact, multi-step wizard.
- Improving an existing form that has high abandonment / error rates.
- User says: "form", "input validation", "form UX", "multi-step", "wizard", "autocomplete", "date picker", "file upload".

## Principles

### 1. Ask for the minimum
- Every field has a cost. Cut what isn't load-bearing.
- Optional fields visibly marked optional (not the other way — required-by-default is the right baseline).
- "Why do you need this?" should be answerable for every field; if it isn't, drop the field.

### 2. Label everything
- Visible, persistent labels — not placeholders-as-labels. Placeholders disappear on input, fail for screen readers, and have low contrast.
- `<label for="id">` linked to the input. Required for a11y.
- Top-aligned labels are most scannable; left-aligned is sometimes OK for short forms with strong vertical alignment.
- Helper text below the field for non-obvious context ("We'll use this to send your receipts").

### 3. Validation timing
The single most-important decision. Three patterns:

| Pattern | When to use | Notes |
| --- | --- | --- |
| **On submit only** | Short forms (login, search) | Simplest; classic. |
| **On blur (per field)** | Most forms | Gives feedback without nagging while typing. |
| **On change (real-time)** | High-stakes inputs (password strength), or fields with strong format (postal code, phone) | Risky — easy to nag. Combine with debounce (200-300ms). |

**Hybrid is best for most forms**: validate on blur, re-validate on change *after the user has seen an error* (so they get faster feedback while fixing it).

### 4. Error UX
- **Error messages near the field**, not in a banner at the top (unless also at the top for a screen-reader pass).
- **Specific, actionable**: "Email must include `@`" beats "Invalid email."
- **Don't blame the user**: "Try a different format" not "You entered this wrong."
- **Inline errors persist** until the user fixes them; don't dismiss on focus.
- **Form-level error** at the top for submit-time issues, with a link to the first field with an error.
- **Error styling**: red is necessary but not sufficient — include an icon, position, and ARIA announcement. Color alone is not accessible.

### 5. Field success / "you did it right"
- Mostly NOT needed inline (avoids visual noise).
- For high-stakes formats (matching passwords, secure password strength), a small success indicator helps.
- For long forms, indicate progress (X of Y completed).

### 6. Input types — use the right HTML one
- `<input type="email">` — keyboards on mobile show `@`.
- `<input type="tel">` — number pad on mobile.
- `<input type="url">`, `type="number">`, `type="date">`, etc.
- **Native pickers** for date/time when possible — they're a11y-correct and free.

### 7. Autofill cooperation
- `autocomplete` attribute with proper tokens: `name`, `email`, `tel`, `address-line1`, `cc-number`, `current-password`, etc.
- Browsers learn from these. Forms that ignore autocomplete take 4× longer to fill.
- Password fields: `autocomplete="current-password"` for login, `new-password` for signup/change.

### 8. Multi-step forms (wizards)
- Use when:
  - The form is genuinely too long for one page.
  - Steps have meaningful logical separation.
  - Some steps are conditional based on earlier answers.
- Don't use just to "feel modern."
- **Progress indicator** showing where the user is + how much remains.
- **Allow back navigation** without losing data.
- **Save progress** if the form is non-trivial — losing 20 minutes of typing is unforgivable.
- **One step = one decision area**, not arbitrary chunks.

### 9. Submit button
- Single primary button per form. Bold; high contrast; clear label ("Create account" not "Submit").
- Disable during submission OR show a loading state — don't allow double-submit.
- Loading state: replace label with spinner-and-text ("Creating account..."), disable; don't move the button.
- After success: clear feedback (toast, navigation, or inline confirmation).

### 10. Complex inputs

**Autocomplete / Combobox**
- Use a vetted library (Downshift, Headless UI Combobox, React Aria) — implementing the WAI-ARIA pattern correctly is hard.
- Keyboard: arrows navigate; Enter selects; ESC closes; type filters.
- Surface selected value clearly.
- Handle "no results" with a useful message + maybe a "create new" affordance.

**Date pickers**
- Use the native `<input type="date">` if the form's UX allows. It's a11y-correct, free, and works.
- Custom date picker only if you need a range, multi-date, or specific localization features. Then use a vetted library.

**File upload**
- Visible button + drag-and-drop affordance.
- Show file name + size after selection.
- Progress for uploads > 1MB.
- Allow removal.
- Validate type and size client-side (with server-side as the real check).

**Password fields**
- Toggleable visibility ("show password" eye icon).
- Real-time strength feedback if it's a signup/change flow.
- `autocomplete` correct.
- Don't disable paste.

**Phone numbers**
- Country code picker if international users.
- Format as user types (helpful, not nagging).
- Store in E.164 internally.

**Address forms**
- Country selector first — fields below adapt to that country's format.
- Don't require state/province for countries that don't have them.
- Postal code optional in some countries.

## Accessibility (cross-ref `a11y-audit`)

- Every field has a `<label>` linked by `for`/`id`.
- Required fields marked with `aria-required="true"` AND a visible indicator.
- Errors linked via `aria-describedby` pointing at the error message element.
- Errors announced via `role="alert"` or `aria-live="assertive"` when they appear.
- Field groupings use `<fieldset>` + `<legend>`.
- Logical tab order (matches visual reading order).
- Focus visible on every input.

## Process

1. **List the fields** — each justified.
2. **Decide validation timing** (typically hybrid blur + on-change-after-error).
3. **Design every state per field**: default, focused, filled, error, success, disabled, loading (for async validation).
4. **Implement** using the appropriate input type + autocomplete attribute.
5. **A11y verification** (cross-ref `a11y-audit`).
6. **Test the failure paths**: bad input, network failure mid-submit, slow validation, duplicate submission.

## Anti-patterns

- **Placeholder as label.** Disappears, fails a11y, low contrast.
- **Validating every keystroke** without debounce. Nagging.
- **Generic "Invalid input" errors.** Useless.
- **Disabling submit until "valid"** without telling the user what's wrong. They click, nothing happens, no feedback.
- **Auto-advancing inputs** (e.g. credit card field that jumps when 4 chars typed). Frustrating with paste; breaks keyboard nav.
- **Multi-step wizard with no progress save.** User loses everything on accidental refresh.
- **Required-field indicator inconsistent.** Asterisk on some, "(required)" on others, color on a third.
- **No client + server validation paired.** Either alone is insufficient.

## Cross-references

- `a11y-audit` — forms are the highest-stakes a11y surface.
- `frontend-design` — input states are a design choice.
- `ui-copy` — error messages, button labels, helper text.
- `component-architecture` — Form / Field / Input composition.
- `loading-and-error-states` — async form states.

## Output

Form components implemented + tested. For non-trivial forms, a brief design rationale in `docs/frontend/forms/<form-name>.md` documenting the fields, validation, and UX decisions.
