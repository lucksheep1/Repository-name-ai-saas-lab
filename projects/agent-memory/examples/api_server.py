"""
FastAPI Server Example for agent-memory

Run: uvicorn api_server:app --reload
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory

app = FastAPI(title="Agent Memory API")

# Initialize memory (in production, use Redis or database)
memory = Memory(storage="json", path="./api_memory.json")


class MemoryCreate(BaseModel):
    text: str
    tags: Optional[List[str]] = None
    priority: Optional[int] = 1


class MemorySearch(BaseModel):
    query: str
    limit: Optional[int] = 10


@app.get("/")
async def root():
    return {"message": "Agent Memory API", "version": "1.0.0"}


@app.post("/memories")
async def create_memory(item: MemoryCreate):
    """Add a new memory."""
    if item.tags:
        memory.add_with_tags(item.text, tags=item.tags)
    else:
        memory.add(item.text, metadata={"priority": item.priority})
    return {"status": "ok", "text": item.text}


@app.get("/memories")
async def list_memories(limit: int = 10):
    """List recent memories."""
    timeline = memory.get_timeline(limit=limit)
    return {"memories": timeline}


@app.post("/memories/search")
async def search_memories(search: MemorySearch):
    """Search memories."""
    results = memory.search(search.query    return {"results)
": results[:search.limit]}


@app.get("/memories/tags/{tag}")
async def get_by_tag(tag: str):
    """Get memories by tag."""
    results = memory.get_by_tag(tag)
    return {"tag": tag, "memories": results}


@app.get("/memories/context")
async def get_context(max_tokens: int = 2000):
    """Get context for LLM."""
    context = memory.get_context(max_tokens=max_tokens)
    return {"context": context}


@app.get("/stats")
async def get_stats():
    """Get memory statistics."""
    all_memories = memory.get_timeline(limit=1000)
    tags = {}
    for m in all_memories:
        for tag in m.get("tags", []):
            tags[tag] = tags.get(tag, 0) + 1
    return {
        "total_memories": len(memory.memories),
        "tags": tags,
    }


@app.delete("/memories")
async def clear_memories():
    """Clear all memories."""
    memory.memories = []
    memory.save()
    return {"status": "ok", "message": "All memories cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
