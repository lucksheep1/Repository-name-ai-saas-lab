#!/usr/bin/env python3
"""
Agent Memory - Webhook Handler
==============================
Receive memory updates via webhooks.

Usage:
    pip install flask
    python webhook.py
    
    # Then send POST requests:
    curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d '{"text": "Remember this"}'
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from agent_memory import Memory

app = Flask(__name__)

# Initialize memory (use environment variables for production)
STORAGE = os.environ.get("STORAGE", "json")
PATH = os.environ.get("PATH", "./memory.json")
memory = Memory(storage=STORAGE, path=PATH)


@app.route("/")
def index():
    return {
        "name": "Agent Memory Webhook",
        "endpoints": [
            "GET / - This info",
            "POST /webhook - Add memory",
            "POST /search - Search memories",
            "GET /context - Get context",
            "GET /recent - Recent memories",
            "GET /stats - Statistics"
        ]
    }


@app.route("/webhook", methods=["POST"])
def add_memory():
    """Add memory via webhook."""
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    text = data["text"]
    tags = data.get("tags")
    metadata = data.get("metadata")
    ttl_days = data.get("ttl_days")
    
    if tags:
        memory_id = memory.add_with_tags(text, tags=tags, metadata=metadata)
    else:
        memory_id = memory.add(text, metadata=metadata, ttl_days=ttl_days)
    
    return jsonify({"status": "added", "id": memory_id})


@app.route("/search", methods=["POST"])
def search():
    """Search memories via webhook."""
    data = request.get_json() or {}
    query = data.get("query", "")
    top_k = data.get("top_k", 5)
    
    results = memory.search(query, top_k=top_k)
    return jsonify({"results": results, "count": len(results)})


@app.route("/context", methods=["GET"])
def get_context():
    """Get context."""
    max_tokens = request.args.get("max_tokens", 2000, type=int)
    context = memory.get_context(max_tokens=max_tokens)
    return jsonify({"context": context})


@app.route("/recent", methods=["GET"])
def recent():
    """Get recent memories."""
    limit = request.args.get("limit", 10, type=int)
    recent_memories = memory.get_recent(limit=limit)
    return jsonify({"memories": recent_memories, "count": len(recent_memories)})


@app.route("/stats", methods=["GET"])
def stats():
    """Get statistics."""
    return jsonify({
        "count": memory.count(),
        "storage": STORAGE,
        "path": PATH
    })


if __name__ == "__main__":
    print("🚀 Starting Agent Memory Webhook Server...")
    print(f"📦 Storage: {STORAGE}, Path: {PATH}")
    print("🌐 Visit http://localhost:5000 for info")
    app.run(host="0.0.0.0", port=5000)
