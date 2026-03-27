# Memory Flash ⚡

Quick memory CLI for AI agents. No setup, no dependencies — just remember.

## Problem

Full agent-memory setup is overkill for quick notes.

## Solution

A zero-config CLI to capture and recall memories instantly.

## Installation

```bash
pip install agent-memory
# OR just copy cli.py
```

## Usage

```bash
# Add a memory
python3 cli.py add "Remember to check GitHub issues"
python3 cli.py add "Bug: memory leaks on Redis reconnect"  # Auto-tags as bug

# List memories
python3 cli.py list

# Filter by tag
python3 cli.py list -t bug
python3 cli.py list -t idea

# Search
python3 cli.py search "Redis"

# Clear
python3 cli.py clear
```

## Features

- ✅ Zero config (uses ~/.agent-memory-flash.json)
- ✅ Auto-tagging (bug, idea, todo)
- ✅ Search
- ✅ Custom path support

## Verification

- ✅ Add memories
- ✅ List with tags
- ✅ Search
