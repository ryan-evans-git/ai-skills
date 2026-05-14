---
name: secrets-hygiene
description: Audit the repo for accidentally committed secrets, verify .env handling and .gitignore coverage, and document the secrets-management policy. Use before a release, before open-sourcing a repo, after onboarding a new dev, or when the user says "secrets check", "scan for secrets", "gitleaks", "trufflehog", ".env audit".
---

# secrets-hygiene

## Purpose

Even one committed API key is a real incident. This skill scans for committed secrets, verifies that the workflows preventing them are in place, and documents how the team handles secrets going forward.

## When to use

- Before a release.
- Before making a repo public.
- After onboarding a new developer (their first PR is a high-leak risk).
- Periodically (recommend monthly).
- User says: "secrets check", "scan for secrets", "gitleaks", "trufflehog", "is my .env in git", "rotate keys".

## Process

### Scan
1. **Run a secrets scanner** (any available — install if needed):
   - `gitleaks detect --no-banner` (works on commit history).
   - `trufflehog filesystem .` or `trufflehog git file://.`.
   - `detect-secrets scan --all-files`.
2. **Scan history, not just HEAD.** Most leaks are in old commits. If the scanner doesn't do this by default, force it.
3. **Walk `git ls-files`** for typically-risky filenames:
   - `.env`, `.env.*` (except `.env.example`, `.env.template`)
   - `*.pem`, `*.key`, `*.pfx`, `id_rsa*`
   - `credentials.json`, `service-account*.json`
   - `.aws/`, `.kube/config`
4. **Grep for high-signal patterns** in tracked files:
   - `AKIA[0-9A-Z]{16}` (AWS access key)
   - `ghp_`, `gho_`, `ghs_`, `github_pat_` (GitHub tokens)
   - `xoxb-`, `xoxp-`, `xoxa-` (Slack tokens)
   - `sk-[a-zA-Z0-9]{32,}` (OpenAI / Anthropic-style keys)
   - `-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----`
   - JWT-shaped strings near literal keys.

### Triage
For each finding:
- **Is it a real secret?** (vs. a test fixture / example).
- **Is it currently valid?** (rotate immediately if yes, even if you'll also remove from history).
- **Is it in current HEAD or only in history?**

### Remediate
- **Always rotate the secret first**, regardless of remediation path. Git history rewrite is not a substitute for rotation — assume any committed secret is compromised.
- **For HEAD**: remove the secret, replace with a reference to env / secret manager.
- **For history**: use `git filter-repo` or BFG to scrub history, force-push, AND have every collaborator rebase. This is invasive — confirm with the team before doing it.

### Verify defenses
- `.gitignore` covers: `.env`, `.env.*` (with allowlist for `.env.example`), `*.pem`, `*.key`, `.aws/`, `.kube/config`, build outputs.
- `.env.example` exists with every required variable name and a placeholder value.
- A `pre-commit` hook for secret-scanning is configured (recommend `gitleaks pre-commit` or the `detect-secrets` pre-commit hook).
- CI runs a secret-scanning step on every PR.
- A secrets-management policy doc exists describing where secrets live (1Password / Vault / AWS Secrets Manager / SSM / Doppler), who has access, and the rotation cadence.

### Document
Write `docs/security/secrets-audit-YYYY-MM-DD.md`:
- Findings (with files + action taken — *do NOT include the secret values*).
- Defenses verified.
- Open follow-ups filed on `docs/plans/CURRENT.md`.

Maintain a separate single living doc `docs/security/secrets-policy.md` (created if missing) that documents:
- Where each class of secret lives.
- Who has access.
- Rotation cadence.
- Onboarding/offboarding procedures.

## What this skill does NOT do

- Decrypt encrypted vaults. Inspecting vault contents is out of scope.
- Replace a real DLP / secret-scanning service for sensitive orgs.

## Critical reminder

If a real secret was committed, **rotate first, scrub second, write up third**. Never block on the writeup.

## Output

- `docs/security/secrets-audit-YYYY-MM-DD.md` (point-in-time)
- `docs/security/secrets-policy.md` (living)
