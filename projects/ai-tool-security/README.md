# AI Tool Security Scanner

Lightweight security scanner for AI development tools.

## Problem

AI developer tools (Cline, GitHub Actions, npm packages) have unique security risks:
- **Prompt injection** via GitHub issues, PRs, comments
- **Malicious postinstall scripts** in npm packages
- **Cache poisoning** in CI/CD pipelines

Clinejection (Feb 2026) compromised 4,000 machines via prompt injection.

## Solution

A lightweight CLI scanner for AI tool security:
- **GitHub Actions** workflow security
- **npm package** manifest analysis
- **Prompt injection** pattern detection

## Installation

```bash
pip install ai-tool-security
```

## Usage

```bash
# Scan a GitHub repository
ai-tool-security scan https://github.com/user/repo

# Scan local directory
ai-tool-security scan ./my-project

# Scan npm package
ai-tool-security scan-package ./package.json
```

## Checks

### GitHub Actions
- ✅ Detects external action usage
- ✅ Detects untrusted trigger sources
- ✅ Detects secrets in logs

### npm packages
- ✅ Detects postinstall scripts
- ✅ Detects suspicious dependencies
- ✅ Checks for typosquatting

### Prompt Injection
- ✅ Detects unvalidated input in prompts
- ✅ Checks for direct interpolation

## Example Output

```
$ ai-tool-security scan ./my-project

Scanning ./my-project...

[WARNING] .github/workflows/ci.yml
  - Line 12: External action 'actions/checkout@v3' from untrusted source
  - Line 45: Secret 'NPM_TOKEN' may be exposed in logs

[WARNING] package.json
  - postinstall script detected: 'node scripts/postinstall.js'

2 issues found.
```

## Limits

- No network scanning yet
- Basic patterns only (no ML)
- GitHub API rate limits

## Next

- [ ] Add GitHub API integration
- [ ] Add more prompt injection patterns
- [ ] Add CI/CD integration (GitHub Actions)

---
*Built: 2026-03-06*
