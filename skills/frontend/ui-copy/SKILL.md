---
name: ui-copy
description: Write microcopy that respects the user — button labels, error messages, empty states, confirmation prompts, voice and tone. Use when designing any UI text, when error messages feel robotic, when buttons say "Submit" / "Click here", or when the user says "microcopy", "UX writing", "error messages", "empty state copy", "voice and tone", "button labels".
---

# ui-copy

## Purpose

The words in a UI are part of the UI. A button that says "Submit" treats the user worse than one that says "Create account." Most generated UIs have technically-correct copy that no human would write. This skill is the discipline to do better.

## When to use

- Any UI being designed or built.
- Error messages feel generic / blame-y / unhelpful.
- Empty states say "No data."
- Buttons say "Submit", "OK", "Click here."
- Confirmation prompts say "Are you sure?" with no specifics.
- User says: "microcopy", "UX writing", "error messages", "empty state copy", "voice and tone", "button labels".

## Voice and tone — pick deliberately

**Voice** is consistent across the product: who is this product, in language?
**Tone** shifts by context: an error tone differs from a celebration tone.

Pick a voice early, write it down, hold the line. Common dimensions:

- **Formal ↔ casual** ("Please confirm" vs. "Got it?").
- **Serious ↔ playful** ("Account created." vs. "You're in! 🎉").
- **Sparse ↔ verbose** ("Done." vs. "We've sent your request to the team and they'll be in touch soon.").
- **Reserved ↔ enthusiastic** ("Saved." vs. "Saved successfully!" — the "ly" is the giveaway).

Document the voice in `docs/frontend/voice-tone.md` with do/don't examples. Without that, every engineer makes a different micro-decision.

## Buttons — say what happens

Bad → Better:

| Bad | Better |
| --- | --- |
| Submit | Create account |
| OK | Got it |
| Click here | Read the guide |
| Save | Save changes |
| Submit form | Send message |
| Delete | Delete this comment |
| Confirm | Buy now |
| Cancel | Keep editing |

Pattern: **verb + object**. Tells the user exactly what will happen.

**The "Cancel" trap**: in a confirmation dialog, "Cancel" often means "go back to the dangerous thing." Be specific: "Keep editing" / "Don't delete" / "Stay subscribed."

## Errors — specific, blameless, actionable

Bad → Better:

| Bad | Better |
| --- | --- |
| Invalid email | Email must contain `@` |
| Required field | Enter your name |
| Server error | Something went wrong on our end. Try again in a few seconds. |
| You entered this wrong | The email you entered doesn't match an account |
| Failed | Couldn't save changes. Check your connection and try again. |
| Error 500 | Something broke. We've been notified; try again shortly. |
| You don't have permission | Only admins can delete users |

Patterns:
- **What's wrong**: specific, no jargon.
- **How to fix**: when known.
- **Whose fault**: when it's us, say so ("on our end"). When it's the user, don't blame ("Try a different password" not "Your password is weak").
- **Next action**: link or button when there's something to do.

## Empty states — give the user a next step

A blank "No data" is worst-case. Empty states should:
1. **Explain what would be here** when populated.
2. **Tell the user how to fill it** (with a CTA when applicable).
3. **Maybe show a friendly illustration / icon** that fits the design system.

Bad: "No items."
Better: "Your inbox is empty. New messages will show up here. [Compose a message]"

For first-time experiences, empty states are onboarding moments. Don't waste them.

## Confirmation prompts

Bad: "Are you sure?"
Better: "Delete this comment? You can't undo this."

Patterns:
- **What's about to happen** ("Delete this comment?").
- **The consequence** ("This can't be undone." / "Your team won't have access.").
- **Buttons that name the actions** ("Delete comment" / "Keep it").

## Loading states

Bad: "Loading..."
Better: depends on context:
- Short waits (< 1s): probably no copy needed; spinner is fine.
- Medium (1-5s): "Saving changes..." / "Looking that up..."
- Long (> 5s): "This is taking a moment. We're still working on it."
- Very long (> 30s): "This may take a few minutes. We'll email you when it's ready."

Cross-ref `loading-and-error-states`.

## Success messages

Don't over-celebrate. Most actions are routine.

Bad: "Successfully saved!"
Better: "Saved" / "Changes saved" / no message + visual confirmation (e.g. button briefly turns green).

Reserve excited copy for genuine milestones (account created, big purchase completed, year-in-review).

## General language rules

- **Active voice**: "We sent the email" not "The email was sent."
- **Second person**: "Your account" not "The user's account."
- **Present tense**: "Save changes" not "Saved changes" (button) / "We sent..." not "We have sent..." (past success).
- **No "please" everywhere**: it's nice but adds noise. "Enter your email" is fine.
- **No needless capitalization**. "Account Settings" or "Account settings" — pick one.
- **Sentence case** for most UI; Title Case only when the language requires it (proper nouns, brand names).
- **Numbers**: spell out one through nine in prose; numerals for 10+. In dense UI, numerals throughout.
- **Real punctuation**: em dash for ranges and asides, curly quotes, ellipsis as `…`. Or commit to ASCII; just be consistent.

## Internationalization (cross-ref `internationalization-prep`)

If the product will be localized:
- **Don't concatenate strings**: `"You have " + count + " messages"` breaks in any language with pluralization rules. Use ICU MessageFormat or equivalent.
- **Allow space for expansion**: German is often 30% longer than English; Japanese is often shorter.
- **Avoid idioms**: "On the same page" doesn't translate.
- **Pluralization**: many languages have more than singular/plural (Arabic has six forms).

## Reading-level

- **8th-grade reading level** is a common target for consumer products. (Tools: Hemingway, Flesch-Kincaid.)
- Higher for specialist tools (developer tooling, professional software) — but plain language still beats jargon.
- Test on people who aren't experts.

## Process

1. **Audit current copy** — collect buttons, errors, empty states, loading messages, confirmation prompts. Surface inconsistency.
2. **Document the voice** at `docs/frontend/voice-tone.md` — 1 page, with do/don't examples.
3. **Replace generic copy** with specific copy, one component at a time. Cross-ref `design-system-keeper` — get the system's primitives right first.
4. **A11y check**: copy is part of a11y. Error messages must be specific enough that a screen-reader user can act on them.
5. **Localization-proof** if applicable — no concatenation; use ICU.

## Anti-patterns

- **"Submit"** — meaningless.
- **"Successfully saved!"** — over-celebration.
- **"Error: Something went wrong."** — useless.
- **"Are you sure?"** — what am I being asked to be sure about?
- **"User", "Item", "Entity"** — code words leaking into the UI.
- **Inconsistent terminology**: "team" in one place, "workspace" in another.
- **Robotic apologies**: "We apologize for the inconvenience." Say "Sorry that broke" or just fix it.
- **Tooltip copy that explains the visible label** ("Submit: click to submit the form").

## Cross-references

- `frontend-design` — words ARE design.
- `form-design` — error messages.
- `loading-and-error-states` — what each state says.
- `a11y-audit` — copy is the screen-reader experience.
- `internationalization-prep` — copy that translates.
- `design-system-keeper` — voice / tone in the design system doc.

## Output

UI text in code, plus `docs/frontend/voice-tone.md` documenting the voice and key patterns.
