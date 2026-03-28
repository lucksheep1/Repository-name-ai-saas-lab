# PR Draft: Add agent-memory to awesome-openclaw

**Target:** https://github.com/vincentkoc/awesome-openclaw
**Section:** Memory and Context Systems
**Status:** DRAFT — Pending Founder approval to submit

---

## Proposed Addition

### Memory and Context Systems

```markdown
- [agent-memory](https://github.com/lucksheep1/Repository-name-ai-saas-lab) - Lightweight, open-source AI agent memory library with native MCP v3.2 support. Supports JSON, SQLite, and Redis backends with TTL expiration and AES encryption. No cloud required. ([compare.html](https://lucksheep1.github.io/Repository-name-ai-saas-lab/compare.html))
```

Alternative section — MCP and Tool Servers:

```markdown
- [agent-memory](https://github.com/lucksheep1/Repository-name-ai-saas-lab) - MCP v3.2 server for AI agent memory. Memory_search, memory_add, memory_get, memory_list, memory_clear. Works with Cursor, Claude Code, OpenClaw. TTL, encryption, tagging. MIT License.
```

---

## Why This PR Should Be Accepted

1. **OpenClaw ecosystem relevance**: OpenClaw has 250K+ GitHub stars (surpassing React). agent-memory is built specifically for OpenClaw's MCP protocol
2. **No duplicate**: No other local-first, API-key-free MCP memory in the list
3. **Quality**: MIT licensed, tested (4/4 backends), full feature set
4. **Category fit**: Perfect match for "Memory and Context Systems" section

---

## Competitors Already Listed (for reference)

- MemOS — MemOS Cloud plugin (cloud required)
- MoltBrain — Long-term memory plugin
- OpenAmnesia — Continual learning context engine
- Mem0 — Cloud-based memory

**agent-memory differentiates**: local-first, no API key, no cloud dependency

---

## PR Submission Plan

1. Fork vincentkoc/awesome-openclaw
2. Add agent-memory to Memory and Context Systems section
3. Submit PR with:
   - Clear description of agent-memory
   - Comparison to existing memory entries
   - Link to compare.html for full feature comparison
   - Note: MIT license, 100% free, no API key required

---

## Notes

- Awesome OpenClaw list: https://github.com/vincentkoc/awesome-openclaw
- Section: Memory and Context Systems
- This is a DRAFT — requires human approval before submission
- PR must be submitted by Founder (needs GitHub account with write access to fork)
