#!/usr/bin/env python3
"""
Agent Memory - Web Dashboard
===========================
Simple web dashboard for memory management.

Usage:
    pip install flask
    python web_dashboard.py
    
    # Then open http://localhost:5000
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template_string, request, jsonify
from agent_memory import Memory

app = Flask(__name__)
memory = Memory(storage="json", path="./memory.json")

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Agent Memory Dashboard</title>
    <style>
        body { font-family: -apple-system, system-ui, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        .card { border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 12px 0; }
        .memory { background: #f9f9f9; padding: 12px; margin: 8px 0; border-radius: 4px; }
        .tag { display: inline-block; background: #e0e0e0; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-right: 4px; }
        input, textarea { width: 100%; padding: 8px; margin: 8px 0; box-sizing: border-box; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .stats { display: flex; gap: 20px; }
        .stat { background: #f0f0f0; padding: 16px; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 24px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🤖 Agent Memory Dashboard</h1>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-number">{{ count }}</div>
            <div>Memories</div>
        </div>
    </div>
    
    <div class="card">
        <h2>Add Memory</h2>
        <form method="POST" action="/add">
            <textarea name="text" rows="3" placeholder="Enter memory..."></textarea>
            <input name="tags" placeholder="Tags (comma separated)">
            <button type="submit">Add</button>
        </form>
    </div>
    
    <div class="card">
        <h2>Search</h2>
        <form method="GET" action="/">
            <input name="query" placeholder="Search memories..." value="{{ query }}">
            <button type="submit">Search</button>
        </form>
    </div>
    
    <div class="card">
        <h2>Recent Memories</h2>
        {% for mem in memories %}
        <div class="memory">
            {{ mem.text }}
            {% if mem.tags %}
            <div style="margin-top: 8px;">
                {% for tag in mem.tags %}
                <span class="tag">{{ tag }}</span>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''


@app.route("/")
def index():
    query = request.args.get("query", "")
    
    if query:
        memories = memory.search(query)
    else:
        memories = memory.get_recent(limit=20)
    
    return render_template_string(
        HTML_TEMPLATE,
        memories=memories,
        count=memory.count(),
        query=query
    )


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "")
    tags_str = request.form.get("tags", "")
    
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    
    if text:
        if tags:
            memory.add_with_tags(text, tags=tags)
        else:
            memory.add(text)
    
    return index()


if __name__ == "__main__":
    print("🌐 Starting Web Dashboard...")
    print("   Open http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
