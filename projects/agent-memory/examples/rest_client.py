#!/usr/bin/env python3
"""
Agent Memory - REST Client
==========================
Python client for Agent Memory API server.

Usage:
    from rest_client import AgentMemoryClient
    
    client = AgentMemoryClient("http://localhost:8000")
    client.add("Remember this")
    results = client.search("remember")
    context = client.get_context()
"""

import requests
from typing import List, Optional, Dict, Any


class AgentMemoryClient:
    """REST client for Agent Memory API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request."""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def add(self, text: str, tags: List[str] = None, metadata: dict = None, ttl_days: int = None) -> str:
        """Add a memory."""
        data = {"text": text}
        if tags:
            data["tags"] = tags
        if metadata:
            data["metadata"] = metadata
        if ttl_days:
            data["ttl_days"] = ttl_days
        
        result = self._request("POST", "/memory", json=data)
        return result.get("id")
    
    def search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search memories."""
        result = self._request("POST", "/memory/search", json={"query": query, "top_k": top_k})
        return result.get("results", [])
    
    def get_context(self, max_tokens: int = 2000) -> str:
        """Get context for agent."""
        result = self._request("GET", f"/memory/context?max_tokens={max_tokens}")
        return result.get("context", "")
    
    def get_recent(self, limit: int = 10) -> List[dict]:
        """Get recent memories."""
        result = self._request("GET", f"/memory?limit={limit}")
        return result
    
    def get_timeline(self, limit: int = 20) -> List[dict]:
        """Get timeline."""
        result = self._request("GET", f"/memory/timeline?limit={limit}")
        return result
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory."""
        try:
            self._request("DELETE", f"/memory/{memory_id}")
            return True
        except requests.exceptions.HTTPError:
            return False
    
    def clear(self) -> None:
        """Clear all memories."""
        self._request("DELETE", "/memory")
    
    def stats(self) -> dict:
        """Get statistics."""
        return self._request("GET", "/health")


# Demo
if __name__ == "__main__":
    print("Agent Memory REST Client")
    print("=" * 40)
    print("Use with API server:")
    print("  python web_api.py")
    print("then:")
    print("  client = AgentMemoryClient('http://localhost:8000')")
    print("  client.add('Hello')")
    print("=" * 40)
