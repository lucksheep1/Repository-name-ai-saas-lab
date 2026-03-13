# Agent Memory Manager - Examples

This folder contains example scripts demonstrating how to use agent-memory.

## Quick Demo (1-minute)

Run the integration demo to see the complete workflow:

```bash
cd projects/agent-memory
pip install -e .
cd examples
python integration_demo.py
```

**Expected output:**
- Initialize memory
- Write 7 sample memories
- Search for "AI agent programming"
- Generate context for agent
- Display simulated agent response
- Store agent response
- Show timeline view

See `VERIFICATION.md` for detailed验收步骤.

## Basic Usage

```python
from agent_memory import Memory

# Initialize memory with JSON storage
memory = Memory(storage="json", path="./my_memory.json")

# Add memories
memory.add("User prefers dark mode")
memory.add("User's name is John")
memory.add("Last project was a web app")

# Search memories
results = memory.search("user preferences")
print(results)

# Get context for an AI agent
context = memory.get_context(max_tokens=2000)
print(context)
```

## Using Tags

```python
from agent_memory import Memory

memory = Memory(storage="json", path="./tagged_memory.json")

# Add with tags
memory.add_with_tags("Bug in login flow", tags=["bug", "urgent"])
memory.add_with_tags("New feature request", tags=["feature", "enhancement"])
memory.add_with_tags("User feedback", tags=["feedback"])

# Get all bugs
bugs = memory.get_by_tag("bug")
print(bugs)

# Get all feedback items
feedback = memory.get_by_tag("feedback")
print(feedback)
```

## Using Priority

```python
from agent_memory import Memory

memory = Memory(storage="json", path="./priority_memory.json")

# Add with priority (1-5, higher = more important)
memory.add("Low priority task", metadata={"priority": 1})
memory.add("Medium priority task", metadata={"priority": 3})
memory.add("Critical production issue", metadata={"priority": 5})

# Get high priority items
important = memory.get_by_priority(4)
print(important)
```

## Timeline View

```python
from agent_memory import Memory

memory = Memory(storage="json", path="./timeline_memory.json")

# Add some memories
memory.add("Started working on project")
memory.add("Completed first milestone")
memory.add("Fixed critical bug")

# Get timeline
timeline = memory.get_timeline(limit=10)
for item in timeline:
    print(f"{item['created_at']}: {item['text']}")
```

## Export/Import

```python
from agent_memory import Memory

memory = Memory(storage="json", path="./export_memory.json")

# Add memories
memory.add("Important information")
memory.add("Another memory")

# Export to JSON
memory.export("backup.json")

# Export to Markdown (for human reading)
memory.export_markdown("memory.md")

# Import from JSON
memory.import_("backup.json")
```

## CLI Usage

```bash
# Initialize
agent-memory init

# Add memory
agent-memory add --text "User likes dark mode"

# Search
agent-memory search --text "preferences"

# Get context for LLM
agent-memory context

# Get recent memories
agent-memory recent --top-k 10

# Get statistics
agent-memory stats

# List all tags
agent-memory tags

# Get by tag
agent-memory by-tag --tag bug

# Get by priority
agent-memory by-priority --priority 4

# Export
agent-memory export --file backup.json
agent-memory export --file memory.md --format markdown

# Import
agent-memory import --file backup.json

# Timeline
agent-memory timeline --top-k 20
```

## Use Cases

### Chatbot Memory
```python
from agent_memory import Memory

memory = Memory(storage="json", path="./chatbot.json")

def handle_message(user_id, message):
    # Store user message
    memory.add(f"User said: {message}")
    
    # Get conversation context
    context = memory.get_context(max_tokens=1000)
    
    # Generate response using context
    response = generate_response(context, message)
    
    # Store bot response
    memory.add(f"Bot said: {response}")
    
    return response
```

### Agentic Workflow
```python
from agent_memory import Memory

memory = Memory(storage="json", path="./agent.json")

def agent_task(task):
    # Check relevant memories
    relevant = memory.search(task)
    
    # Get high priority items
    important = memory.get_by_priority(4)
    
    # Build context
    context = f"Relevant memories: {relevant}\nImportant: {important}"
    
    # Execute task with context
    result = execute_with_context(task, context)
    
    # Remember the result
    memory.add(f"Task '{task}' completed: {result}")
    
    return result
```

---
*Examples added: 2026-03-12*

## Additional Examples

### LangChain Integration (`langchain_example.py`)
Shows how to use agent-memory with LangChain for conversation context management.

```bash
python langchain_example.py
```

### Multi-Agent Sharing (`multi_agent_example.py`)
Demonstrates how multiple AI agents can share a central memory store.

```bash
python multi_agent_example.py
```

### FastAPI Server (`api_server.py`)
Exposes agent-memory as a REST API service.

```bash
pip install fastapi uvicorn
uvicorn api_server:app --reload
```
