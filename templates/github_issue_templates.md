# GitHub Issue Templates - 可复用模板

## 1. Release Announcement Template

```
## {Product Name} v{Version} Released

We are excited to announce the release of {Product Name} v{Version} with new features:

- **{Feature 1}**: Description
- **{Feature 2}**: Description
- **{Feature 3}**: Description

### Quick Start

```{code_example}
```

More info: {link}
```

## 2. Feature Request Template

```
## Feature Request: {Feature Name}

### Problem
{Describe the problem users are facing}

### Proposed Solution
{Describe your proposed solution}

### Alternative Solutions
- Alternative 1
- Alternative 2

### Priority
Low / Medium / High

---
*This is an auto-generated feature request for product validation.*
```

## 3. Bug Report Template

```
## Bug Report: {Bug Title}

### Description
{Description of the bug}

### Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

### Expected Behavior
{What should happen}

### Actual Behavior
{What actually happens}

### Environment
- OS: 
- Version: 

---
*Auto-generated bug report*
```

## 4. Question Template

```
## Question: {Question Title}

### Context
{Provide context for your question}

### What I've Tried
- Attempt 1
- Attempt 2

### What I Need
{What information or help do you need}
```

---

## 快速使用示例

```bash
# 使用脚本创建 Issue
python3 scripts/github_issue.py \
  --title "[Release] Agent Memory v3.0" \
  --body "$(cat templates/issue_release.md)"

python3 scripts/github_issue.py \
  --title "[Feature] Web Dashboard" \
  --body "$(cat templates/issue_feature.md)" \
  --label "enhancement"
```
