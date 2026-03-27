# README Generator

CLI tool to generate README.md from project structure.

## Problem

Writing README is tedious.

## Solution

Auto-generate README from project structure.

## Usage

```bash
python3 cli.py /path/to/project -n "project-name" -d "Description"
python3 cli.py . -o README.md
```

## Verification

- ✅ Scans project structure
- ✅ Detects main file
- ✅ Generates template
