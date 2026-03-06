# Verification — Local Code RAG CLI

## Test: Index and search code

```bash
# 1. Create a test file
echo "def authenticate(user): return True" > /tmp/test-code/auth.py

# 2. Index a directory
python3 rag.py index /tmp/test-code/
# Output: Indexing /tmp/test-code/...
#         Indexed: 1 files, 1 functions, 0 classes

# 3. Search code
python3 rag.py search /tmp/test-code/ "auth"
# Output: 1. /tmp/test-code/auth.py:0 (py)
#         Score: 0.000
#         def authenticate(user): return True...

# 4. Search functions
python3 rag.py function /tmp/test-code/ authenticate
# Output: Found function: authenticate

# 5. Get stats
python3 rag.py stats
# Output: {'total_blocks': N, 'languages': [...], 'files': N}
```

## Verification: All Features

- ✅ index - Index a directory
- ✅ search - Search code using TF-IDF
- ✅ function - Search for functions
- ✅ class - Search for classes
- ✅ stats - Show index statistics

## Supported Languages

- Python (.py) ✓
- JavaScript (.js) ✓
- TypeScript (.ts) ✓
- Go (.go) ✓
- Rust (.rs) ✓
- C/C++ (.c, .h) ✓

---
*Verified: 2026-03-06*
