---
name: internationalization-prep
description: Prepare a frontend for internationalization (i18n) — string extraction, ICU MessageFormat for plurals/genders/numbers, RTL support, locale-aware dates/numbers/currency, font fallbacks. Use when building an app that may be translated, when the user says "i18n", "translation", "localization", "RTL", "ICU MessageFormat", or before adding the first non-English locale.
---

# internationalization-prep

## Purpose

Retrofitting i18n is expensive. Preparing for i18n from the start adds modest discipline and unlocks markets without re-architecting later. This skill is the prep work that makes "add a locale" a content task, not an engineering project.

Title is "prep" because the actual translation workflow (TMS choice, vendor management, review processes) is a separate concern; this skill is the engineering foundations.

## When to use

- Building a frontend that may eventually be translated.
- Before adding the first non-English locale.
- After an audit revealed hardcoded strings, broken pluralization, or layout breaks on RTL.
- User says: "i18n", "internationalization", "translation", "localization", "RTL", "right-to-left", "ICU MessageFormat", "locale-aware", "translate this".

## The disciplines

### 1. No hardcoded strings in the UI
- Every user-visible string lives in a translation catalog keyed by ID.
- The component references the ID; the framework resolves the string for the current locale.
- Common libraries:
  - **react-intl** / **FormatJS** (ICU MessageFormat-based).
  - **i18next** + react-i18next.
  - **Lingui**.
  - Framework-native: **Next.js i18n**, **Remix i18next**, **SvelteKit Paraglide**.

### 2. No string concatenation
**The trap**:
```js
`You have ${count} messages`
```
Breaks in any language with non-trivial pluralization, gendered nouns, or different word order.

**The fix — ICU MessageFormat**:
```
{count, plural, =0 {No messages} one {You have 1 message} other {You have # messages}}
```
ICU handles plural rules per locale (English has 2 forms; Arabic has 6; Polish has 3-ish). Translators write the right form per language without engineers ever knowing the rules.

ICU also handles:
- **Gender** (`{gender, select, female {Her} male {His} other {Their}}`).
- **Number formatting** (`{amount, number, currency}`).
- **Dates** (`{date, date, long}`).
- **Nesting** (combine plural / gender in one message).

### 3. Locale-aware formatting

Don't roll your own. Use `Intl`:
- **`Intl.NumberFormat`** — `1,234.56` (US), `1.234,56` (DE), `1 234,56` (FR).
- **`Intl.DateTimeFormat`** — `Jan 5, 2026` vs. `5 ene 2026` vs. `2026年1月5日`.
- **`Intl.RelativeTimeFormat`** — "3 days ago" / "hace 3 días".
- **`Intl.PluralRules`** — locale-aware plural selection if you're rolling your own (don't; use ICU).
- **`Intl.ListFormat`** — "A, B, and C" / "A, B y C" / "A、B、C".
- **`Intl.Collator`** — locale-aware sorting (German "ä" sorts differently across countries).

For currency, always store amounts in minor units + currency code, format at display time with `Intl.NumberFormat(locale, { style: 'currency', currency: 'USD' })`.

### 4. RTL (right-to-left) support
Arabic, Hebrew, Persian, Urdu, and others read right-to-left. Common gotchas:

- **CSS logical properties** (`margin-inline-start` instead of `margin-left`) — auto-flip in RTL.
- **`dir="rtl"`** on the `<html>` (or container) — most CSS layout flips automatically with logical properties.
- **Icons that imply direction** (arrows, breadcrumbs, "next") may need to flip; icons that don't (search, settings) don't.
- **Numbers DON'T flip** — they're written LTR even within RTL text. Browsers handle this with bidi algorithm, but custom rendering (canvas, manual layout) often gets it wrong.
- **Flexbox + Grid** default to writing-mode-aware in modern CSS; verify with a manual `dir="rtl"` switch.

### 5. Allow space for expansion
- **German is often 30% longer than English**; Russian even more.
- **Japanese / Chinese / Korean often shorter** but have very different line-break behavior.
- **Buttons that fit "Save" in English** may not fit "Speichern" in German.
- Test with **pseudo-localization** — automatically expand strings (`"Saveeeeeee"`) to surface truncation early.

### 6. Font fallbacks
- The brand font likely doesn't support every script (Cyrillic, Greek, Arabic, CJK).
- Set up a font stack per locale or rely on `unicode-range` to load the right subset.
- Test that Japanese/Chinese characters render at all. Default browser fallbacks vary wildly.
- **Don't subset out characters needed by your supported locales.**

### 7. Date/time and timezones
- Store in UTC; display in user's timezone.
- Let the user override their displayed timezone (account setting).
- Use `Intl.DateTimeFormat` with the user's locale + timezone — don't reformat strings manually.
- For relative time ("3 hours ago"), use `Intl.RelativeTimeFormat` per locale.

### 8. Locale detection / selection
- **Default**: derive from `Accept-Language` header or `navigator.languages`.
- **Override**: explicit user setting > URL prefix (`/de/...`) > cookie > browser default.
- **URL-prefixed routing** is best for SEO and shareable links.
- Cache the user's choice; don't re-detect on every visit.

### 9. Translator-friendly catalogs
- **Use IDs that name intent**, not English text — `cta.signup` not `Sign Up`. Survives English rewrites.
- **Provide context** for translators — a description per string, or examples ("Used as a button label on the homepage").
- **Don't break strings into fragments** — `"Welcome" + " " + name` becomes two strings to translate, neither with context. Pass `name` as a variable.

### 10. Avoid idioms and culture-specific images
- "Hit it out of the park" doesn't translate.
- Hand gestures, animals, colors carry different meanings across cultures.
- Holidays, examples, mascots: be deliberate.

## Process

### Phase 1 — Foundations (do before any actual translation)
1. **Pick the i18n library** appropriate to the framework.
2. **Set up catalog structure** — one file per locale (`en.json`, `de.json`, ...) keyed by string ID.
3. **Extract existing strings** — move every user-visible string into the catalog. Tools (`babel-plugin-react-intl`, `i18next-parser`) can automate.
4. **Switch all formatting to `Intl` APIs.**
5. **Adopt ICU MessageFormat** for any pluralizable / gendered / parameterized strings.

### Phase 2 — RTL prep (if RTL locales are coming)
1. Audit CSS for `left`/`right`/`margin-left`/etc. → switch to logical properties.
2. Test with `dir="rtl"` on a page; fix breaks.
3. Test directional icons; mark ones that need to flip.

### Phase 3 — Translation workflow (separate concern)
- Pick a TMS (Crowdin, Lokalise, Phrase, Smartling).
- Define the source-of-truth catalog and the sync workflow.
- Hand off to localization team.

### Phase 4 — Per-locale launch
- Pseudo-localize first to find truncation / overflow.
- Beta with native-speaker users.
- Launch with the new locale; monitor for unsupported strings.

## Document at `docs/frontend/i18n.md`

- Supported locales + their status.
- Library / framework configuration.
- Catalog structure and IDs.
- Locale-detection logic.
- RTL support level.
- Pluralization rules used.

## Anti-patterns

- **Hardcoded English strings in components** that "we'll extract later."
- **Concatenation**: `"Hello, " + name`. Use parameterized strings.
- **Date strings built manually** instead of `Intl.DateTimeFormat`.
- **`if (lang === 'es') { ... } else { ... }`** branches scattered through code. Use the catalog.
- **Padding-left** and `margin-right` throughout instead of logical properties.
- **Icons that imply direction** that don't flip in RTL.
- **Asking translators to fit translations into the same character count** as English. Layouts need to flex.
- **Translation IDs that are the English text** — change "Submit" to "Send" and all translations break.

## Cross-references

- `ui-copy` — copy that translates well.
- `responsive-design` — RTL is a responsive concern.
- `frontend-design` — type, spacing, icons all interact with i18n.
- `a11y-audit` — `lang` attribute is an a11y requirement; locale affects screen-reader pronunciation.
- `pii-data-handling` — locale + timezone are PII fields in some jurisdictions.

## Output

Extracted strings + catalog structure, `Intl`-based formatting, RTL-ready CSS, plus `docs/frontend/i18n.md` documenting the setup.
