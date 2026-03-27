# GitHub Repository Analyzer

CLI tool to analyze GitHub repositories for trends, issues, and opportunities.

## Problem

Want to understand a GitHub repo's health and find opportunities? Manually checking stars, issues, and PRs is time-consuming.

## Solution

A CLI tool that analyzes any GitHub repo and outputs:
- Basic stats (stars, forks, watchers, language)
- Recent issues with labels
- Keyword clustering for pain points
- Differentiation opportunities

## Installation

```bash
cd projects/github-repo-analyzer
python3 cli.py owner/repo
```

## Usage

```bash
# Analyze a repo
python3 cli.py mem0ai/mem0

# Output as JSON
python3 cli.py mem0ai/mem0 --json
```

## Example Output

```
🔍 Analyzing mem0ai/mem0...

📊 Basic Info
  Stars:     51,160
  Forks:    5,723
  Language: Python
  Open Issues: 304

📝 Recent Open Issues (top 10)
  1. #4557 feat: add close() method
  2. #4556 fix: use persistent dirs
  ...

🎯 Issue Analysis
  Common keywords: fail(2), memory(1), api(1)

🎯 Differentiation for agent-memory:
  → Focus on easier installation & cross-platform support
```

## Verification

- ✅ Analyzes mem0ai/mem0 (51k stars)
- ✅ Analyzes any public repo
- ✅ JSON output for automation
