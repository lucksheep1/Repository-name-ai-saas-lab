"""
Memory Web Dashboard
Simple web UI for memory management
"""
from agent_memory import Memory
from flask import Flask, render_template_string, request, jsonify


app = Flask(__name__)
memory = Memory(storage="sqlite", path="./dashboard_memory.db")


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Agent Memory Dashboard</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 40px auto; padding: 20px; }
        h1 { color: #333; }
        .form { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; }
        .memory { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 4px; }
        .tags { color: #666; font-size: 12px; }
        .meta { color: #999; font-size: 11px; }
    </style>
</head>
<body>
    <h1>🧠 Agent Memory Dashboard</h1>
    
    <div class="form">
        <h3>Add Memory</h3>
        <form method="POST" action="/add">
            <textarea name="content" placeholder="Memory content..." rows="3"></textarea>
            <input name="tags" placeholder="Tags (comma separated)">
            <button type="submit">Add</button>
        </form>
    </div>
    
    <div class="form">
        <h3>Search</h3>
        <form method="GET" action="/">
            <input name="q" value="{{ request.args.get('q', '') }}" placeholder="Search...">
            <button type="submit">Search</button>
        </form>
    </div>
    
    <h3>Memories ({{ memories|length }})</h3>
    {% for mem in memories %}
    <div class="memory">
        <div>{{ mem.content }}</div>
        <div class="tags">Tags: {{ mem.tags|join(', ') }}</div>
        <div class="meta">{{ mem.created_at }}</div>
    </div>
    {% endfor %}
</body>
</html>
"""


@app.route("/")
def index():
    query = request.args.get("q", "")
    
    if query:
        memories = memory.search(query)
    else:
        memories = memory.get_all()
    
    return render_template_string(HTML, memories=memories, request=request)


@app.route("/add", methods=["POST"])
def add():
    content = request.form.get("content", "")
    tags_str = request.form.get("tags", "")
    
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    
    if content:
        memory.add(content, tags=tags)
    
    return index()


@app.route("/api/memories", methods=["GET"])
def api_list():
    return jsonify(memory.get_all())


@app.route("/api/memories", methods=["POST"])
def api_add():
    data = request.json
    mem_id = memory.add(
        content=data.get("content", ""),
        tags=data.get("tags", []),
        metadata=data.get("metadata", {})
    )
    return jsonify({"id": mem_id})


@app.route("/api/search", methods=["GET"])
def api_search():
    query = request.args.get("q", "")
    return jsonify(memory.search(query))


def run(host="0.0.0.0", port=5000):
    """Run dashboard"""
    print(f"Starting dashboard on http://{host}:{port}")
    app.run(host=host, port=port)


if __name__ == "__main__":
    run()
