# Bug: <Short name>

- **Reported:** YYYY-MM-DD by <name / source>
- **Investigated:** YYYY-MM-DD by <name>
- **Severity:** P0 | P1 | P2 | P3
- **Status:** Investigating | Fixed | Won't fix
- **Related:** PR, incident postmortem if any

## Report

<Verbatim from the reporter. What they did, what they expected, what they observed.>

## Environment

- Version: ...
- OS / browser / device: ...
- Frequency: always | sometimes | once
- Customer impact: ...

## Reproduction

<Final minimized steps to reproduce.>

1. ...
2. ...
3. ...

## Root cause

<The actual underlying problem. Cite file / line / commit if known.>

## Trigger

<What made it surface now — recent change, specific data, race condition.>

## Fix

<Summary of the change. Link PR / commit.>

## Regression test

<Path and test name of the test that now covers this bug. e.g. `tests/test_billing.py::test_zero_amount_invoice_returns_400`>

## Sibling risks

<Where else this anti-pattern might exist. What was checked, what was found.>

- ...

## Lessons

<Anything to feed forward — monitoring, tests, process.>

- ...
