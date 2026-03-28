# Outreach Kit — agent-memory Launch

**Status:** DRAFT — Requires Founder approval to distribute
**Created:** 2026-03-29

This kit contains ready-to-post content for launching agent-memory to the world. Each piece is formatted for its platform and includes optimal posting times and strategies.

---

## Platform Strategy

| Platform | Audience | Difficulty | Expected Impact |
|----------|----------|------------|----------------|
| **Hacker News** | Developers, founders, investors | High | Very High |
| **r/programming** | General programmers | Medium | High |
| **r/SideProject** | Indie hackers | Low | Medium |
| **Discord (OpenClaw)** | OpenClaw community | Low | High (targeted) |
| **Twitter/X** | Dev community | Low | Medium |

---

## 1. Hacker News — Show HN

**When to post:** Tuesday–Thursday, 10:00–11:00 AM ET (11:00 PM–12:00 AM China)
**Title check:** HN algorithm favors "Show HN" + specific numbers

### Draft:

```
Show HN: I built an open-source MCP server for AI agent memory (MIT, no API key required)

I've been building AI agents for a while and noticed a pattern: every session starts from scratch because the agent forgets everything.

I built agent-memory to solve this. It's an MCP v3.2 server that gives AI agents persistent memory:

- Works with OpenClaw, Cursor, Claude Code (any MCP client)
- JSON / SQLite / Redis backends
- TTL expiration, AES encryption, tagging
- 100% local, no API key, MIT license

The key differentiator: unlike Mem0 OpenMemory ($19–249/mo + OpenAI key required), this runs entirely on your machine.

GitHub: https://github.com/lucksheep1/Repository-name-ai-saas-lab
Live demo: https://lucksheep1.github.io/Repository-name-ai-saas-lab/demo.html
Comparison: https://lucksheep1.github.io/Repository-name-ai-saas-lab/compare.html

Would love feedback on the architecture. Is local-first the right bet, or is cloud the only viable business model for agent memory?
```

### HN Tips:
- DO NOT include images in initial post
- DO respond to comments within first 2 hours
- DO be honest about limitations (0 stars currently)
- DO NOT spam "please upvote"
- The "honest question at the end" typically gets more engagement

---

## 2. Reddit — r/programming

**When to post:** Tuesday–Thursday, 6:00–9:00 AM ET
**Title format:** [Showcase] or [Discussion]

### Draft:

```
[Showcase] agent-memory: an open-source MCP server for AI agent memory — local-first, no API key required

Hey r/programming 👋

I've been working on persistent memory for AI agents. The problem: every new session = starting from scratch.

agent-memory exposes memory tools via MCP v3.2 (the same protocol Cursor/Claude/OpenClaw use):

github.com/lucksheep1/Repository-name-ai-saas-lab

Quick example:
python
from agent_memory import Memory
m = Memory(storage="json", path="./memory.json")
m.add("User prefers dark mode", ttl="30d")
m.search("dark mode preference")
```

```
- Works with any MCP client
- TTL expiration, AES encryption, tagging
- JSON / SQLite / Redis backends
- 100% local, MIT license

The inspiration: Mem0 OpenMemory is great but requires OpenAI API key + $19–249/mo. I wanted something that runs entirely offline.

Looking for: feedback on the API design and whether local-first is actually useful or just a niche concern.
```

---

## 3. Reddit — r/SideProject

**When to post:** Anytime (less strict timing)

### Draft:

```
Started: 3 weeks ago | Completed: Today | Made with: Python, MCP v3.2

agent-memory: give your AI agents a memory that doesn't forget

I built this because I was tired of re-explaining my codebase to Cursor every single session.

What it does:
- MCP v3.2 server for AI agent memory
- Semantic search over your codebase context
- TTL expiration (memories auto-expire after N days)
- AES encryption for sensitive data
- JSON/SQLite/Redis backends
- MIT license, no account needed

The catch: it's brand new (0 stars, honest). But it's tested and works.

github.com/lucksheep1/Repository-name-ai-saas-lab

Would appreciate any early feedback — especially on whether the API feels intuitive or if the concepts are confusing.
```

---

## 4. Discord — OpenClaw Community

**Channel:** `#showcase` or `#skills` or `#plugins`
**Check Discord link:** Check OpenClaw Discord invite

### Draft:

```
👋 Hey OpenClaw community!

I've been building agent-memory — an MCP v3.2 server specifically for AI agent memory.

It's designed to work with OpenClaw's MCP integration:
- memory_search, memory_add, memory_get, memory_list, memory_clear tools
- Local-first: JSON/SQLite/Redis, no cloud
- TTL expiration, AES encryption
- 100% MIT license

GitHub: github.com/lucksheep1/Repository-name-ai-saas-lab
Demo: lucksheep1.github.io/Repository-name-ai-saas-lab/demo.html

I've also submitted a PR to awesome-openclaw (waiting on review).

Would love to know if this is useful for the OpenClaw ecosystem — and happy to adjust the MCP interface based on what works best for OpenClaw agents.
```

---

## 5. Twitter/X

**Format:** Thread or single tweet
**Optimal:** Tuesday–Thursday, 8:00–10:00 AM ET
**Hashtags:** #AI #OpenSource #MCP #AIAgents #Python

### Thread Draft:

```
🧵 I built an MCP server for AI agent memory.

Problem: Every AI agent session starts from scratch. The agent forgets everything.

Solution: agent-memory, an open-source MCP v3.2 server that gives agents persistent memory.

Features:
→ Semantic memory search
→ TTL expiration (auto-cleanup)
→ AES encryption
→ JSON / SQLite / Redis backends
→ 100% local, MIT license

No API key. No account. No cloud.

GitHub: [link]
Demo: [link]

(0 stars, 3 weeks old, but tested and working. Would love feedback from the #AIAgents community.)
```

---

## 6. Product Hunt

**When to post:** Monday–Wednesday, 12:00 AM ET (upcoming day starts here)
**Category:** Developer Tools or AI

### Draft:

```
🚀 agent-memory

AI agents forget everything between sessions. agent-memory gives them persistent memory via the Model Context Protocol.

What makes it different:
- MCP v3.2 native (works with OpenClaw, Cursor, Claude Code)
- 100% local — no cloud, no API key, MIT license
- JSON / SQLite / Redis backends
- TTL expiration, AES encryption, tagging

Why it matters: Mem0 OpenMemory requires OpenAI API key + $19/mo. agent-memory is the privacy-first, free alternative.

Links:
🌐 Live Demo: https://lucksheep1.github.io/Repository-name-ai-saas-lab/demo.html
📊 Comparison: https://lucksheep1.github.io/Repository-name-ai-saas-lab/compare.html
⭐ GitHub: https://github.com/lucksheep1/Repository-name-ai-saas-lab
```

---

## 7. LinkedIn (Personal)

### Draft:

```
Just shipped: agent-memory — an open-source MCP server for AI agent memory.

After 3 weeks of building, it's finally ready for honest feedback.

The problem I solved: AI agents forget everything. Every new session = starting from scratch.

My solution: an MCP v3.2 server that gives agents persistent memory across sessions. Works locally, no API key, MIT license.

Is it useful? I honestly don't know yet — the repo has 0 stars. But it's tested and functional.

Would love your take: Is local-first the right bet for AI agent memory, or is cloud the only model that makes business sense?

GitHub in comments.
```

---

## Outreach Priority Checklist

**Before posting anywhere, update these first:**
- [ ] GitHub repo README with clear installation steps
- [ ] Demo page working and accessible
- [ ] Compare page with honest positioning
- [ ] At least 3 commits showing ongoing development

**Start with (in order):**
1. ⭐ Discord (OpenClaw) — lowest barrier, highest relevance audience
2. ⭐ r/SideProject — indie hacker audience, forgiving of 0 stars
3. ⭐ r/programming — larger audience
4. ⭐ HN Show HN — highest potential impact, also highest bar
5. ⭐ Twitter/X — if you have a dev audience
6. ⭐ Product Hunt — when you have at least 1 other signal

---

## Metrics to Track

After posting, track:
- GitHub stars (watch for spike after each post)
- website traffic (if you have analytics)
- Twitter/X followers
- Reddit upvotes/comments
- Discord member count

Post the links in #results channel so we can correlate.

---

## Legal/Safe Posting Notes

- DO be honest: "0 stars, 3 weeks old, looking for feedback"
- DO NOT fake engagement
- DO NOT use upvote groups
- DO respond to all comments personally
- DO accept criticism gracefully

---

*This outreach kit was created by an autonomous AI agent as part of an AI SaaS Lab experiment. All content is original.*
