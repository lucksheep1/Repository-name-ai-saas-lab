#!/usr/bin/env python3
"""
Agent Memory - Mobile API
=========================
Optimized API for mobile apps.

Features:
- Lightweight responses
- Compression
- Batch operations
- Offline sync

Usage:
    python mobile_api.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import zlib
import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_memory import Memory

app = FastAPI(title="Agent Memory Mobile API")

# Lightweight memory store
memory = Memory(storage="json", path="./memory.json")


# Lightweight models
class MemoryItem(BaseModel):
    id: str
    text: str
    timestamp: str


class AddRequest(BaseModel):
    text: str
    tags: Optional[List[str]] = None


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


# Routes
@app.get("/")
def root():
    return {"api": "Agent Memory Mobile", "version": "1.0"}


@app.get("/sync")
def sync(since: str = ""):
    """Get changes since timestamp."""
    # Get all memories (simplified)
    recent = memory.get_recent(limit=100)
    
    # Filter by timestamp if provided
    if since:
        recent = [m for m in recent if m.get("timestamp", "") > since]
    
    # Return lightweight format
    return {
        "memories": [
            {
                "i": m["id"][:8],  # Short ID
                "t": m["text"],
                "ts": m["timestamp"][:19],
                "tg": m.get("tags", [])
            }
            for m in recent
        ],
        "count": len(recent)
    }


@app.post("/add")
def add(item: AddRequest):
    """Add memory (lightweight)."""
    if item.tags:
        memory_id = memory.add_with_tags(item.text, tags=item.tags)
    else:
        memory_id = memory.add(item.text)
    
    return {"id": memory_id[:8], "status": "ok"}


@app.post("/batch")
def batch_add(items: List[AddRequest]):
    """Add multiple memories."""
    ids = []
    for item in items:
        if item.tags:
            memory_id = memory.add_with_tags(item.text, tags=item.tags)
        else:
            memory_id = memory.add(item.text)
        ids.append(memory_id[:8])
    
    return {"ids": ids, "count": len(ids)}


@app.post("/search")
def search(request: SearchRequest):
    """Search (lightweight)."""
    results = memory.search(request.query, top_k=request.limit)
    
    return {
        "results": [
            {
                "i": m["id"][:8],
                "t": m["text"],
                "tg": m.get("tags", [])
            }
            for m in results
        ]
    }


@app.get("/recent")
def recent(limit: int = 20):
    """Get recent memories (lightweight)."""
    recent = memory.get_recent(limit=limit)
    
    return {
        "memories": [
            {
                "i": m["id"][:8],
                "t": m["text"],
                "ts": m["timestamp"][:19],
                "tg": m.get("tags", [])
            }
            for m in recent
        ]
    }


@app.get("/context")
def context(max_tokens: int = 500):
    """Get context (lightweight)."""
    context = memory.get_context(max_tokens=max_tokens)
    return {"context": context}


@app.delete("/{memory_id}")
def delete(memory_id: str):
    """Delete memory (supports short ID)."""
    # Try full ID first
    success = memory.delete(memory_id)
    
    if not success:
        # Try short ID - search for it
        recent = memory.get_recent(limit=100)
        for m in recent:
            if m["id"].startswith(memory_id):
                success = memory.delete(m["id"])
                break
    
    if success:
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/stats")
def stats():
    """Get stats."""
    return {
        "count": memory.count(),
        "tags": list(set(
            tag 
            for mem in memory.get_recent(limit=100) 
            for tag in mem.get("tags", [])
        ))
    }


if __name__ == "__main__":
    import uvicorn
    print("📱 Starting Mobile API...")
    print("Endpoints:")
    print("  GET  /sync?since=<timestamp>")
    print("  POST /add")
    print("  POST /batch")
    print("  POST /search")
    print("  GET  /recent")
    print("  GET  /context")
    print("  DELETE /<id>")
    print("  GET  /stats")
    uvicorn.run(app, host="0.0.0.0", port=8001)
