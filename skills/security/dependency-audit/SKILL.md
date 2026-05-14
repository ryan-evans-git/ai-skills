---
name: dependency-audit
description: Audit project dependencies for known CVEs, abandoned packages, and license-risk findings, using the right tool for the language. Use periodically, before releases, after lockfile changes, or when the user says "dep audit", "vuln scan", "are our deps safe", "check for CVEs".
---

# dependency-audit

## Purpose

Production-impacting vulnerabilities most often arrive through dependencies, not own-code. This skill produces a current, prioritized list of dependency findings and a clear "what to do" per finding.

## When to use

- Periodically (recommend monthly).
- Before any release.
- After `package-lock.json` / `poetry.lock` / `Cargo.lock` / `go.sum` changes.
- User says: "dep audit", "vuln scan", "are our deps safe", "check for CVEs", "dependabot".

## Process

1. **Detect the language(s)** and pick the right tool. Run the tool. If multiple ecosystems, run each.

   | Language / package manager | Command |
   | --- | --- |
   | Python (pip / poetry / uv) | `pip-audit -r requirements.txt` or `pip-audit` (poetry) |
   | JS / TS (npm / pnpm / yarn) | `npm audit --json` / `pnpm audit --json` / `yarn npm audit` |
   | Rust | `cargo audit --json` |
   | Go | `govulncheck ./...` |
   | Ruby | `bundler-audit` |
   | Java (maven/gradle) | OWASP `dependency-check` |
   | Container images | `trivy image <ref>` or `grype <ref>` |

   If a tool isn't installed, note the recommendation and proceed with what's available (e.g. GitHub Dependabot alerts via `gh api`).

2. **Cross-reference GitHub Dependabot alerts** if the repo is on GitHub: `gh api /repos/{owner}/{repo}/dependabot/alerts --jq '.[] | {state, severity, package: .security_advisory.summary}'`.

3. **Categorize findings**:
   - **Critical / High** — known exploit, network-reachable: must-fix before next release.
   - **Medium** — should-fix in the current cycle.
   - **Low** — track and address in the next dep-bump.
   - **Informational** — no fix available; document a workaround / mitigation / accept-risk note.

4. **For each finding, list**:
   - Package + version.
   - CVE / advisory ID + link.
   - Severity (from advisory + adjusted for actual exposure: do we use the affected code path?).
   - Fix: target version, or workaround, or accepted-risk reason.
   - Owner + due date for must-fix items.

5. **Check for soft signals** that aren't CVEs:
   - Abandoned packages (no release in >2 years; archived repo).
   - Single-maintainer critical deps (supply-chain risk).
   - Pre-1.0 deps in production-critical paths.

6. **Output**: `docs/security/dependency-audits/YYYY-MM-DD.md` with the structured findings + a one-paragraph summary + action items filed onto `docs/plans/CURRENT.md`.

7. **For automation**, recommend enabling Dependabot / Renovate if not already on, plus the relevant scanner in CI on a schedule.

## What this skill does NOT do

- Auto-upgrade. Bumping a major dep is a code change with its own risks — propose, don't execute.
- License audit beyond a quick flag. Use a dedicated license-audit skill for that.

## Output

`docs/security/dependency-audits/YYYY-MM-DD.md`
