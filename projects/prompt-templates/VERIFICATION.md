# Verification — Prompt Templates Library

## Test: Generate prompts

```bash
# 1. List templates
python3 library.py list
# Output: Available templates (16): ...

# 2. Generate a code-review prompt
python3 library.py generate code-review --var language=python --var code="print('hello')"
# Output: The rendered prompt

# 3. Generate a summarize prompt
python3 library.py generate summarize --var max_length=100 --var text="Long text..."
# Output: The rendered prompt
```

## Verification: All 16 Templates

1. code-generation ✓
2. code-review ✓
3. summarize ✓
4. translate ✓
5. explain ✓
6. debug ✓
7. test-generation ✓
8. refactor ✓
9. write-documentation ✓
10. create-readme ✓
11. write-sql ✓
12. create-api-spec ✓
13. write-unit-test-prompt ✓
14. security-audit ✓
15. performance-optimize ✓
16. write-git-commit ✓

## CLI Commands

```bash
# List all templates
python3 library.py list

# Generate a prompt
python3 library.py generate <template-name> --var key=value

# Show template info
python3 library.py info <template-name>
```

---
*Verified: 2026-03-06*
