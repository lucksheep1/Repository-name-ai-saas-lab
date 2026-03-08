# Local Code RAG CLI

Lightweight local code search using RAG.

## Problem

Developers need to search their local codebases, but:
- GitNexus is too complex
- Sourcegraph requires cloud
- grep is not intelligent

## Solution

A simple CLI for local code RAG:
- **Index** your codebase
- **Search** using natural language
- **Fast** and local-only

## Installation

```bash
pip install code-rag-cli
```

## Usage

```bash
# Index a directory
code-rag index ./my-project

# Search
code-rag search "how to authenticate users"

# Search with context
code-rag search "auth" --context 3

# Find functions by name
code-rag find-function authenticate

# Find classes by name
code-rag find-class User

# Find imports
code-rag find-import requests

# Export to Markdown
code-rag export

# Get statistics
code-rag stats
```

## Features

- Local-only (no cloud)
- Fast indexing
- Natural language search
- Code context awareness
- Find functions, classes, imports
- Export to Markdown
- Statistics dashboard

## Example

```bash
$ code-rag index ./src
Indexing... 125 files indexed

$ code-rag search "user authentication"
Found 3 matches:

1. src/auth.py:45
   def authenticate(user):
       ...

2. src/api/middleware.py:23
   def require_auth():
       ...

3. src/models/user.py:12
   class User:
       ...

$ code-rag stats
Total blocks: 125
Languages: ['python', 'javascript']
Files: 45
```

## How It Works

1. **Parse**: Extract code blocks from files
2. **Index**: Build TF-IDF index
3. **Search**: Find relevant code chunks
4. **Rank**: Return top results with context

## Limits

- Python only (for now)
- No semantic embeddings (TF-IDF based)
- Max file size: 1MB

## Next

- [ ] Add more language support
- [ ] Add semantic embeddings
- [ ] Add VS Code extension

---
*Built: 2026-03-06*
*Updated: 2026-03-08 - Added stats and export features*
