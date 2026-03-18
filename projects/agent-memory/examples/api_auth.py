#!/usr/bin/env python3
"""
Agent Memory - API with Authentication
=====================================
Secure REST API with token-based auth.

Usage:
    python api_auth.py
    
    # Then test:
    curl -H "Authorization: Bearer token123" http://localhost:8000/memory
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
import time
from functools import wraps
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_memory import Memory

app = FastAPI(title="Agent Memory API (Auth)")

# In-memory token store (use database in production)
TOKENS = {
    "token123": {"user": "admin", "expires": time.time() + 86400},
    "readonly": {"user": "reader", "expires": time.time() + 86400, "readonly": True}
}

# Global memory
memory = Memory(storage="json", path="./memory.json")


def verify_token(authorization: str = Header(None)) -> dict:
    """Verify authorization token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization[7:]
    
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token_data = TOKENS[token]
    
    if token_data["expires"] < time.time():
        raise HTTPException(status_code=401, detail="Token expired")
    
    return token_data


def require_admin(token_data: dict):
    """Require admin privileges."""
    if token_data.get("user") != "admin":
        raise HTTPException(status_code=403, detail="Admin required")


# Models
class MemoryAdd(BaseModel):
    text: str
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None


# Routes
@app.get("/")
def root():
    return {"name": "Agent Memory API (Authenticated)", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy", "count": memory.count()}


@app.post("/memory", dependencies=[])
def add_memory(item: MemoryAdd, authorization: str = Header(None)):
    """Add a memory (requires admin or write token)."""
    token_data = verify_token(authorization)
    
    if token_data.get("readonly"):
        raise HTTPException(status_code=403, detail="Read-only token")
    
    if item.tags:
        memory_id = memory.add_with_tags(item.text, tags=item.tags, metadata=item.metadata)
    else:
        memory_id = memory.add(item.text, metadata=item.metadata)
    
    return {"id": memory_id, "status": "added"}


@app.get("/memory")
def get_memories(limit: int = 10, authorization: str = Header(None)):
    """Get recent memories."""
    verify_token(authorization)
    return memory.get_recent(limit=limit)


@app.post("/memory/search")
def search(query: str, top_k: int = 5, authorization: str = Header(None)):
    """Search memories."""
    verify_token(authorization)
    results = memory.search(query, top_k=top_k)
    return {"results": results, "count": len(results)}


@app.get("/memory/context")
def get_context(max_tokens: int = 2000, authorization: str = Header(None)):
    """Get context."""
    verify_token(authorization)
    context = memory.get_context(max_tokens=max_tokens)
    return {"context": context}


@app.delete("/memory/{memory_id}")
def delete_memory(memory_id: str, authorization: str = Header(None)):
    """Delete a memory."""
    token_data = verify_token(authorization)
    
    if token_data.get("readonly"):
        raise HTTPException(status_code=403, detail="Read-only token")
    
    success = memory.delete(memory_id)
    if success:
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Memory not found")


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Agent Memory API with Auth...")
    print("📝 Test tokens:")
    print("   Admin: Bearer token123")
    print("   Read-only: Bearer readonly")
    uvicorn.run(app, host="0.0.0.0", port=8000)
