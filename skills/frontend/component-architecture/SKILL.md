---
name: component-architecture
description: Design component APIs and composition patterns that scale — prop design, when to lift state, compound components vs. render props vs. context, controlled vs. uncontrolled, hooks vs. higher-order patterns. Use when designing a new component, when an existing one is becoming unwieldy, or when the user says "component API", "props design", "lift state", "compound components", "headless component", "render props".
---

# component-architecture

## Purpose

The worst component APIs accumulate: ten boolean flags, one giant `options` object, four mutually-exclusive variants in the same prop. This skill is the discipline to design components that compose well, expose the right surface, and don't fight their consumers.

## When to use

- Designing a new component or family of components.
- An existing component has accumulated too many props or special cases.
- Building a reusable component library (cross-ref `design-system-keeper`).
- User says: "component API", "props design", "lift state", "compound components", "headless component", "render props", "controlled component", "compound component", "polymorphic".

## Core principles

### 1. Composition > configuration
- **Configuration** — exposes options as props. Easy to start; explodes over time.
- **Composition** — exposes pieces the consumer assembles. More verbose, dramatically more flexible.
- **Rule of thumb**: 3+ booleans that affect the same area → switch to composition.

Bad:
```tsx
<Modal showHeader showFooter showClose title="..." footerContent={...}>
  ...
</Modal>
```

Better:
```tsx
<Modal>
  <Modal.Header>
    <Modal.Title>...</Modal.Title>
    <Modal.Close />
  </Modal.Header>
  <Modal.Body>...</Modal.Body>
  <Modal.Footer>...</Modal.Footer>
</Modal>
```

### 2. One prop, one purpose
- Avoid props that mean different things in different combinations.
- **Variants as a single prop**: `variant: "primary" | "secondary" | "ghost"`, not `primary={true}` `secondary={true}`.
- **Sizes as single prop**: `size: "sm" | "md" | "lg"`.

### 3. Controlled, uncontrolled, or both — decide deliberately
- **Uncontrolled** — component owns its state. `<input defaultValue="..." />`. Simplest API.
- **Controlled** — consumer owns the state. `<input value={...} onChange={...} />`. Necessary for cross-component coordination, validation, undo, etc.
- **Hybrid** (the React standard): if `value` prop is passed → controlled. If not → uncontrolled with `defaultValue`. Document explicitly.

Most reusable components offer both. The consumer chooses.

### 4. Children as the default content slot
- `children` is the most flexible "what goes in the middle." Reach for it before specific content props.
- Use specific content props (`title`, `description`) only when the slot is constrained and named.

### 5. Render props and "function-as-children" for flexible content
- When the consumer needs the component's internal state to render: render prop or function children.
- Modern React: hooks usually replace this — but for headless components, render props still shine.

```tsx
<Combobox>
  {({ inputProps, isOpen, options }) => (...)}
</Combobox>
```

### 6. Headless first, styled second
- **Headless components** = behavior + accessibility + state, no visual styling. Examples: Radix UI, Headless UI, React Aria.
- Pattern: build the headless layer; layer styling on top via your design system.
- Benefit: visual redesigns don't touch the behavior layer.

### 7. Polymorphic `as` prop sparingly
- `<Button as="a" href="..." />` — useful for "this looks like a button but is semantically a link."
- Type it well in TypeScript (props of the rendered element).
- Don't use to skip the design system ("`as="div"` to get the button styles without semantics").

### 8. Forwarded refs by default for primitives
- Buttons, inputs, anything an external consumer might want to focus / measure / animate: `forwardRef`.
- Mandatory for design-system primitives.

### 9. Imperative API only when necessary
- Most React APIs are declarative. Sometimes you need imperative (focus a field, scroll to row, open a modal from a side-effect):
  - **`useImperativeHandle`** for component instances.
  - **Context with a method bag** for cross-tree imperatives.
- Don't reach for imperatives if a state prop will do.

## State lifting — when to do it

Lift state up when:
- **Multiple components need the same state** (most common reason).
- **Parent needs to read or mutate it** (validation, submission, undo).
- **The state is part of the URL or persisted** (route, query, localStorage).

Keep state local when:
- Only the component needs it.
- It would otherwise pollute the parent's API.
- Examples: hover state, focus state, open/closed of nested popover.

## Compound components

A pattern where related components share state via context, exposed as namespaced sub-components.

```tsx
<Tabs defaultValue="account">
  <Tabs.List>
    <Tabs.Trigger value="account">Account</Tabs.Trigger>
    <Tabs.Trigger value="billing">Billing</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="account">...</Tabs.Content>
  <Tabs.Content value="billing">...</Tabs.Content>
</Tabs>
```

When to use:
- Multi-part UI patterns: Tabs, Accordion, Menu, Combobox, Dialog with custom internals.
- When the consumer needs to control the layout or ordering of the parts.
- When sub-components need access to shared state but the consumer shouldn't have to wire it.

## Prop design checklist

For each prop:
- [ ] **Does it name intent**, not appearance? (`variant="warning"` over `color="yellow"`.)
- [ ] **Is the type constrained**? (Enum/union over `string`.)
- [ ] **Default value sensible**? (Document it.)
- [ ] **Required vs. optional**? (Required when the component genuinely can't work without it; optional otherwise.)
- [ ] **Naming consistent** across the library? (Same prop name = same meaning everywhere.)
- [ ] **Boolean traps avoided**? (Two booleans for three states = bug. Use a union.)

## File / folder layout

A common pattern for a component:

```
components/Button/
├── Button.tsx           ← the component
├── Button.stories.tsx   ← Storybook
├── Button.test.tsx      ← unit tests
├── Button.css           ← or styled-components / Tailwind classes inline
└── index.ts             ← re-exports
```

For compound components, single file is often clearer than separate files for each sub-part.

## Process

1. **Sketch the API** before implementing. Write the JSX a consumer would write.
2. **List the states** (default, hover, focus, active, loading, error, empty, disabled).
3. **Decide controlled/uncontrolled** (or both).
4. **Pick composition vs. configuration** per slot.
5. **Implement** — keep state local where possible; lift only when needed.
6. **Story-fy** — Storybook for every variant + state.
7. **Test** — Testing Library; assert behavior, not implementation. (Cross-ref `tdd-enforcer`.)
8. **A11y check** (cross-ref `a11y-audit`).

## Anti-patterns

- **Boolean explosion**: 6+ boolean flags. Switch to a `variant` union or composition.
- **`options` mega-prop**: an opaque config object that's just hidden props.
- **Component that knows about its parent**: prop-drilling parent state down to children that shouldn't care.
- **Render in a child what the parent should own**: business logic inside a presentational component.
- **No forwardRef**: imperative consumers (`ref.current.focus()`) can't reach the component.
- **`any` as the prop type**: lose all autocomplete and type-safety.
- **Components that render different things based on combinations of unrelated props.** Refactor into separate components.

## Cross-references

- `design-system-keeper` — primitives this skill builds for.
- `frontend-design` — the visual design these components express.
- `a11y-audit` — every component has a11y obligations.
- `form-design` — form components have specific compound patterns.
- `modal-and-dialog-design` — a canonical compound-component case.

## Output

Components implemented with clean APIs; design rationale captured in Storybook docs or `docs/frontend/component-patterns.md` for non-obvious choices.
