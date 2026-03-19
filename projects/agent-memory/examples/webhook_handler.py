"""
Webhook Handler for Memory Updates
Handle incoming webhook events to add/update memories
"""
from agent_memory import Memory
from flask import Flask, request, jsonify
import hmac
import hashlib
import json


app = Flask(__name__)
memory = Memory(storage="sqlite", path="./webhook_memory.db")


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify webhook signature"""
    if not signature:
        return False
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


@app.route("/webhook/memory", methods=["POST"])
def add_memory():
    """Add memory from webhook payload"""
    # Verify signature (optional)
    signature = request.headers.get("X-Signature", "")
    secret = request.json.get("secret", "default_secret")
    
    # Skip verification in demo mode
    # if not verify_signature(request.data, signature, secret):
    #     return jsonify({"error": "Invalid signature"}), 401
    
    data = request.json
    
    content = data.get("content", "")
    tags = data.get("tags", [])
    metadata = data.get("metadata", {})
    ttl_days = data.get("ttl_days")
    
    if not content:
        return jsonify({"error": "content required"}), 400
    
    mem_id = memory.add(content, tags=tags, metadata=metadata, ttl_days=ttl_days)
    
    return jsonify({
        "success": True,
        "memory_id": mem_id,
        "content": content
    })


@app.route("/webhook/search", methods=["GET"])
def search_memory():
    """Search memories via webhook"""
    query = request.args.get("q", "")
    limit = int(request.args.get("limit", 10))
    
    results = memory.search(query, limit=limit)
    
    return jsonify({
        "query": query,
        "count": len(results),
        "results": results
    })


@app.route("/webhook/memories", methods=["GET"])
def list_memories():
    """List all memories"""
    all_memories = memory.get_all()
    
    return jsonify({
        "total": len(all_memories),
        "memories": all_memories[:50]  # Limit to 50
    })


@app.route("/webhook/memory/<mem_id>", methods=["DELETE"])
def delete_memory(mem_id):
    """Delete a memory"""
    memory.forget(mem_id)
    return jsonify({"success": True, "memory_id": mem_id})


@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "ok", "memories": len(memory.get_all())})


def run_server(host="0.0.0.0", port=5000):
    """Run the webhook server"""
    print(f"Starting webhook server on {host}:{port}")
    app.run(host=host, port=port)


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            run_server()
        elif sys.argv[1] == "demo":
            # Quick demo without starting server
            memory.add("Webhook demo memory", tags=["demo", "webhook"])
            results = memory.search("webhook")
            print(f"Added and found: {len(results)} memories")
    else:
        print("Usage: python webhook_handler.py [server|demo]")
