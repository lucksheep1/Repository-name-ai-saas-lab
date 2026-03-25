#!/usr/bin/env python3
"""
Agent Memory Dashboard - Flask Web Interface
"""
import os
import sys
import json
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agent_memory import Memory
except ImportError:
    print("Error: agent_memory not installed. Run: pip install -e .")
    sys.exit(1)

from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Memory instance
memory = None

def get_memory():
    global memory
    if memory is None:
        # Try different backends
        for storage in ['sqlite', 'json']:
            try:
                path = './memory.db' if storage == 'sqlite' else './memory.json'
                if storage == 'sqlite' and not os.path.exists(path):
                    continue
                memory = Memory(storage=storage, path=path)
                print(f"Loaded memory with {memory.count()} entries from {storage}")
                break
            except Exception as e:
                continue
    return memory

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Memory Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f23; color: #fff; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 30px; text-align: center; }
        .header h1 { font-size: 2rem; margin-bottom: 10px; }
        .stats { display: flex; justify-content: center; gap: 30px; margin-top: 20px; }
        .stat { background: rgba(255,255,255,0.1); padding: 15px 30px; border-radius: 10px; }
        .stat-value { font-size: 2rem; font-weight: bold; color: #22c55e; }
        .stat-label { color: #9ca3af; font-size: 0.9rem; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .controls { display: flex; gap: 10px; margin-bottom: 20px; }
        .search { flex: 1; padding: 12px; border: 1px solid #374151; border-radius: 8px; background: #1f2937; color: #fff; font-size: 1rem; }
        .btn { padding: 12px 24px; background: #3b82f6; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; }
        .btn:hover { background: #2563eb; }
        .btn-secondary { background: #374151; }
        .btn-secondary:hover { background: #4b5563; }
        .memories { display: grid; gap: 15px; }
        .memory { background: #1f2937; border-radius: 12px; padding: 20px; border-left: 4px solid #22c55e; }
        .memory-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .memory-id { color: #6b7280; font-size: 0.8rem; }
        .memory-text { font-size: 1.1rem; margin-bottom: 10px; }
        .memory-meta { display: flex; gap: 15px; flex-wrap: wrap; }
        .tag { background: #374151; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; }
        .priority { color: #f59e0b; }
        .ttl { color: #ef4444; }
        .created { color: #9ca3af; }
        .empty { text-align: center; padding: 60px; color: #6b7280; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Agent Memory Dashboard</h1>
        <div class="stats">
            <div class="stat">
                <div class="stat-value" id="total">{{ total }}</div>
                <div class="stat-label">Total Memories</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="tags">{{ tags }}</div>
                <div class="stat-label">Tags</div>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="controls">
            <input type="text" class="search" id="search" placeholder="Search memories..." value="{{ search }}">
            <button class="btn" onclick="searchMemories()">Search</button>
            <button class="btn btn-secondary" onclick="exportData()">Export JSON</button>
        </div>
        <div class="memories" id="memories">
            {% for m in memories %}
            <div class="memory">
                <div class="memory-header">
                    <span class="memory-id">#{{ m.id[:8] }}</span>
                    {% if m.ttl_remaining %}
                    <span class="ttl">⏰ {{ m.ttl_remaining }}</span>
                    {% endif %}
                </div>
                <div class="memory-text">{{ m.text }}</div>
                <div class="memory-meta">
                    <span class="created">{{ m.created }}</span>
                    {% if m.tags %}
                    {% for tag in m.tags %}
                    <span class="tag">{{ tag }}</span>
                    {% endfor %}
                    {% endif %}
                </div>
            </div>
            {% endfor %}
            {% if not memories %}
            <div class="empty">No memories found. Add some with agent-memory CLI!</div>
            {% endif %}
        </div>
    </div>
    <script>
        function searchMemories() {
            const q = document.getElementById('search').value;
            window.location.href = '/?q=' + encodeURIComponent(q);
        }
        function exportData() {
            window.location.href = '/api/export';
        }
        document.getElementById('search').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') searchMemories();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    m = get_memory()
    if m is None:
        return render_template_string(HTML, total=0, tags=0, memories=[], search='')
    
    q = request.args.get('q', '')
    try:
        if q:
            results = m.search(q, top_k=50)
        else:
            results = m.get_recent(limit=50)
        
        # Get all tags
        all_tags = set()
        for r in results:
            if r.get('tags'):
                all_tags.update(r['tags'])
        
        memories = []
        for r in results:
            mem = {
                'id': r.get('id', ''),
                'text': r.get('text', ''),
                'created': r.get('created', '')[:19],
                'tags': r.get('tags', []),
                'ttl_remaining': r.get('ttl_remaining', '')
            }
            memories.append(mem)
        
        return render_template_string(HTML, total=m.count(), tags=len(all_tags), memories=memories, search=q)
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/api/memories')
def api_memories():
    m = get_memory()
    if m is None:
        return jsonify({'error': 'No memory found'})
    return jsonify(m.get_recent(limit=100))

@app.route('/api/stats')
def api_stats():
    m = get_memory()
    if m is None:
        return jsonify({'total': 0, 'tags': 0})
    
    all_tags = set()
    for r in m.get_recent(limit=100):
        if r.get('tags'):
            all_tags.update(r['tags'])
    
    return jsonify({'total': m.count(), 'tags': len(all_tags)})

@app.route('/api/export')
def api_export():
    m = get_memory()
    if m is None:
        return jsonify({'error': 'No memory found'})
    return jsonify(m.get_recent(limit=1000))

if __name__ == '__main__':
    print("Starting Agent Memory Dashboard on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)