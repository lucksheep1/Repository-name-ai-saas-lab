#!/usr/bin/env python3
"""
Agent Memory - Simple Web API
=============================
A minimal FastAPI server exposing agent-memory via REST API.

Usage:
    pip install fastapi uvicorn
    python web_api.py
    
    # Then visit http://localhost:8000/docs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from agent_memory import Memory

app = FastAPI(title="Agent Memory API", version="1.0.0")

# Global memory instance (in production, use proper storage)
memory = Memory(storage="json", path="./memory.json")


class MemoryAdd(BaseModel):
    text: str
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None
    ttl_days: Optional[int] = None


class MemorySearch(BaseModel):
    query: str
    top_k: Optional[int] = 5


@app.get("/")
def root():
    return {
        "name": "Agent Memory API",
        "version": "1.0.0",
        "endpoints": [
            "GET /health",
            "POST /memory",
            "GET /memory",
            "POST /memory/search",
            "GET /memory/timeline",
            "GET /memory/context",
            "DELETE /memory"
        ]
    }


@app.get("/health")
def health():
    return {"status": "healthy", "count": memory.count()}


@app.post("/memory")
def add_memory(item: MemoryAdd):
    """Add a new memory."""
    if item.tags:
        memory_id = memory.add_with_tags(item.text, tags=item.tags, metadata=item.metadata)
    else:
        memory_id = memory.add(item.text, metadata=item.metadata, ttl_days=item.ttl_days)
    return {"id": memory_id, "status": "added"}


@app.get("/memory")
def get_memories(limit: int = 10):
    """Get recent memories."""
    return memory.get_recent(limit=limit)


@app.post("/memory/search")
def search_memory(search: MemorySearch):
    """Search memories."""
    results = memory.search(search.query, top_k=search.top_k)
    return {"results": results, "count": len(results)}


@app.get("/memory/timeline")
def get_timeline(limit: int = 20):
    """Get timeline of memories."""
    return memory.get_timeline(limit=limit)


@app.get("/memory/context")
def get_context(max_tokens: int = 2000):
    """Get context for an agent."""
    context = memory.get_context(max_tokens=max_tokens)
    return {"context": context}


@app.delete("/memory/{memory_id}")
def delete_memory(memory_id: str):
    """Delete a specific memory."""
    success = memory.delete(memory_id)
    if success:
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Memory not found")


@app.delete("/memory")
def clear_memory():
    """Clear all memories."""
    memory.clear()
    return {"status": "cleared"}


if __name__ == "__main__":
    print("🚀 Starting Agent Memory API...")
    print("📖 Visit http://localhost:8000/docs for interactive API docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
