#!/usr/bin/env python3
"""
Agent Memory - AWS Lambda Handler
=================================
Deploy agent-memory as an AWS Lambda function.

Usage:
    1. Package: zip -r lambda_function.zip lambda_function.py agent_memory.py
    2. Upload to Lambda
    3. Set environment variables:
       - STORAGE: json or sqlite
       - PATH: /tmp/memory.json
    
    Invoke with:
    {
        "action": "add|search|context|recent|stats",
        "text": "...",
        "query": "...",
        ...
    }
"""

import os
import json
import sys

# Add package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_memory import Memory


def get_memory():
    """Get or create memory instance."""
    storage = os.environ.get("STORAGE", "json")
    path = os.environ.get("PATH", "/tmp/memory.json")
    return Memory(storage=storage, path=path)


def lambda_handler(event, context):
    """AWS Lambda handler."""
    memory = get_memory()
    
    action = event.get("action", "")
    
    if action == "add":
        text = event.get("text", "")
        if not text:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing text"})}
        
        tags = event.get("tags")
        metadata = event.get("metadata")
        ttl_days = event.get("ttl_days")
        
        if tags:
            memory_id = memory.add_with_tags(text, tags=tags, metadata=metadata)
        else:
            memory_id = memory.add(text, metadata=metadata, ttl_days=ttl_days)
        
        return {"statusCode": 200, "body": json.dumps({"status": "added", "id": memory_id})}
    
    elif action == "search":
        query = event.get("query", "")
        top_k = event.get("top_k", 5)
        
        results = memory.search(query, top_k=top_k)
        return {"statusCode": 200, "body": json.dumps({"results": results, "count": len(results)})}
    
    elif action == "context":
        max_tokens = event.get("max_tokens", 2000)
        context = memory.get_context(max_tokens=max_tokens)
        return {"statusCode": 200, "body": json.dumps({"context": context})}
    
    elif action == "recent":
        limit = event.get("limit", 10)
        recent = memory.get_recent(limit=limit)
        return {"statusCode": 200, "body": json.dumps({"memories": recent, "count": len(recent)})}
    
    elif action == "timeline":
        limit = event.get("limit", 20)
        timeline = memory.get_timeline(limit=limit)
        return {"statusCode": 200, "body": json.dumps({"timeline": timeline})}
    
    elif action == "stats":
        return {"statusCode": 200, "body": json.dumps({"count": memory.count()})}
    
    elif action == "clear":
        memory.clear()
        return {"statusCode": 200, "body": json.dumps({"status": "cleared"})}
    
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"Unknown action: {action}",
                "available_actions": ["add", "search", "context", "recent", "timeline", "stats", "clear"]
            })
        }


# Local testing
if __name__ == "__main__":
    # Test add
    print("Testing add...")
    result = lambda_handler({"action": "add", "text": "Test memory"}, None)
    print(result)
    
    # Test search
    print("\nTesting search...")
    result = lambda_handler({"action": "search", "query": "Test"}, None)
    print(result)
    
    # Test context
    print("\nTesting context...")
    result = lambda_handler({"action": "context"}, None)
    print(result)
