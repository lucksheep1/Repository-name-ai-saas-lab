# Verification — MCP Templates

## Test: Generate and run a database MCP server

```bash
# 1. Generate a new MCP server
python3 main.py new test-db --template database

# 2. Check the generated files
ls -la test-db/
# Should show: main.py, requirements.txt, README.md

# 3. Check main.py content
cat test-db/main.py
# Should contain MCP server code with "query" and "tables" tools
```

## Expected Output

```
Creating MCP server: test-db
Template: database
Output: ./test-db
Created: main.py
Created: requirements.txt
Created: README.md

Done! Run:
  cd test-db
  pip install -r requirements.txt
  python main.py
✓ Created test-db/
```

## Verification: All 6 Templates

1. **database** - SQLite query tool ✓
2. **api** - REST API integration ✓
3. **filesystem** - File operations ✓
4. **github** - GitHub API (issues, PRs) ✓
5. **slack** - Slack API (channels, messages) ✓
6. **notion** - Notion API (pages, databases) ✓

## CLI Commands

```bash
# List templates
python3 main.py list
# Output: Available templates: database, api, filesystem, github, slack, notion

# Generate a new server
python3 main.py new my-server --template database
```

---
*Verified: 2026-03-06*
