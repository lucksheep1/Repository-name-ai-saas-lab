# Feedback Wanted - agent-memory

> ⚡ **Give Feedback = Shape the Roadmap!**  
> 📢 **[Feedback Wanted: What do you need? →](./FEEDBACK_WANTED.md)**

---

## One-Minute Feedback

**Answer 3 Yes/No questions → Help us prioritize:**

### Q1: Is LangChain memory too heavy for you?

- ❌ Yes, I want something lighter
- ✅ No, LangChain is fine

### Q2: Do you need this right now?

- ❌ Yes, I need agent memory ASAP
- ✅ No, not urgent

### Q3: Would you try a demo if it took 30 seconds?

- ❌ Yes, show me the demo
- ✅ No, I don't have time

---

## Quick Demo (30 seconds)

```python
pip install agent-memory

from agent_memory import Memory
memory = Memory(storage="json")
memory.add("User likes dark mode")
context = memory.get_context(max_tokens=2000)
print(context)
```

**Expected output:**
```
Recent memories:
- User likes dark mode

Context ready for agent.
```

---

## Who Should Feedback

**✅适合反馈:**
- You build AI agents / chatbots
- You've tried LangChain memory and found it too heavy
- You want simpler memory management

**❌不适合反馈:**
- You're happy with LangChain
- You don't work with AI agents

---

## Where to Give Feedback

**Quickest way:** [GitHub Issues - Feedback](https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues/new?labels=feedback)

**Or discuss:** [GitHub Discussions](https://github.com/lucksheep1/Repository-name-ai-saas-lab/discussions)

---

## Why It Matters

| Your answer | We prioritize |
|-------------|---------------|
| "Yes, too heavy" → | Simplify API further |
| "Yes, need now" → | Ship faster |
| "Yes, show demo" → | Build better demo |

---

*Last updated: 2026-03-16*
