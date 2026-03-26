#!/usr/bin/env python3
"""
agent-memory analytics dashboard

Generates a standalone HTML analytics dashboard from agent-memory storage.

Usage:
    python dashboard.py --storage json --path ./memory.json --output dashboard.html
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))
from agent_memory import Memory


def time_ago(ts):
    try:
        dt = datetime.fromisoformat(ts)
        delta = datetime.now() - dt
        if delta.days > 30:
            return str(delta.days // 30) + "mo ago"
        if delta.days > 0:
            return str(delta.days) + "d ago"
        hours = delta.seconds // 3600
        if hours > 0:
            return str(hours) + "h ago"
        minutes = delta.seconds // 60
        return str(minutes) + "m ago"
    except:
        return "unknown"


def pct(a, b):
    if b == 0:
        return 0
    return min(int(a / b * 100), 100)


def generate_dashboard(memory_obj):
    memories = memory_obj.memories
    total = len(memories)

    encrypted_count = sum(1 for m in memories if m.get("metadata", {}).get("encrypted"))
    ttl_count = sum(1 for m in memories if m.get("expires_at"))
    texts = [m.get("text", "") or "" for m in memories]
    text_lengths = [len(t) for t in texts]
    avg_len = sum(text_lengths) / max(total, 1)
    max_len = max(text_lengths) if text_lengths else 0

    ttl_buckets = Counter()
    no_ttl = 0
    expired = 0
    now = datetime.now()
    for m in memories:
        exp = m.get("expires_at")
        if not exp:
            no_ttl += 1
        else:
            try:
                exp_dt = datetime.fromisoformat(exp)
                if exp_dt < now:
                    expired += 1
                else:
                    delta = exp_dt - now
                    seconds = delta.total_seconds()
                    if seconds < 3600:
                        ttl_buckets["<1h"] += 1
                    elif seconds < 86400:
                        ttl_buckets["<1d"] += 1
                    elif seconds < 604800:
                        ttl_buckets["<1w"] += 1
                    else:
                        ttl_buckets[">1w"] += 1
            except:
                pass

    all_tags = []
    for m in memories:
        tags = m.get("metadata", {}).get("tags", [])
        if isinstance(tags, list):
            all_tags.extend(tags)
    tag_counts = Counter(all_tags)
    top_tags = tag_counts.most_common(10)

    recent = sorted(memories, key=lambda m: m.get("created_at", ""), reverse=True)[:20]

    plain_count = total - encrypted_count
    storage = getattr(memory_obj, "storage", "unknown")

    tags_html = " ".join(
        '<span class="tag">' + str(t) + " &#215;" + str(c) + "</span>"
        for t, c in top_tags
    ) if top_tags else '<span style="color:#475569">No tags found</span>'

    memory_items_html = ""
    for m in recent:
        text = (m.get("text", "") or "")[:200]
        meta = m.get("metadata", {}) or {}
        is_enc = " &#128274;" if meta.get("encrypted") else ""
        source = meta.get("source", "local")
        age = time_ago(m.get("created_at", ""))
        memory_items_html += (
            '<div class="memory-item">'
            '<div class="memory-text">' + text + '</div>'
            '<div class="memory-meta">' + age + " &middot; " + source + is_enc + '</div>'
            '</div>'
        )

    recent_section = (
        '<h2>Recent Memories</h2>' + memory_items_html
        if memory_items_html
        else '<h2>Recent Memories</h2><div class="card" style="color:#475569">No memories</div>'
    )

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>agent-memory Analytics</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; padding: 2rem; }
  h1 { color: #f8fafc; font-size: 1.5rem; margin-bottom: 0.5rem; }
  h2 { color: #94a3b8; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em; margin: 1.5rem 0 0.75rem; }
  .badge { display: inline-block; background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 1rem 1.5rem; margin: 0.25rem; min-width: 120px; }
  .badge-num { font-size: 2rem; font-weight: 700; color: #38bdf8; }
  .badge-label { font-size: 0.75rem; color: #64748b; margin-top: 0.25rem; }
  .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; }
  .tag { display: inline-block; background: #0ea5e9; color: #0f172a; border-radius: 4px; padding: 0.2rem 0.5rem; margin: 0.2rem; font-size: 0.8rem; font-weight: 600; }
  .memory-item { border-left: 3px solid #0ea5e9; padding: 0.5rem 0.75rem; margin: 0.5rem 0; background: #0f172a; border-radius: 0 6px 6px 0; }
  .memory-text { font-size: 0.875rem; color: #cbd5e1; line-height: 1.5; }
  .memory-meta { font-size: 0.7rem; color: #475569; margin-top: 0.25rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.5rem; }
  .bar-chart { display: flex; flex-direction: column; gap: 0.4rem; }
  .bar-row { display: flex; align-items: center; gap: 0.5rem; }
  .bar-label { width: 60px; font-size: 0.75rem; color: #64748b; text-align: right; }
  .bar-track { flex: 1; height: 8px; background: #334155; border-radius: 4px; overflow: hidden; }
  .bar-fill { height: 100%; background: #0ea5e9; border-radius: 4px; }
  .bar-val { width: 40px; font-size: 0.75rem; color: #94a3b8; }
  .footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #1e293b; font-size: 0.7rem; color: #475569; }
</style>
</head>
<body>
<h1>&#128202; agent-memory Analytics</h1>
<p style="color:#475569;font-size:0.8rem;">Generated """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """</p>

<h2>Overview</h2>
<div class="grid">
  <div class="badge">
    <div class="badge-num">""" + str(total) + """</div>
    <div class="badge-label">Total Memories</div>
  </div>
  <div class="badge">
    <div class="badge-num">""" + str(encrypted_count) + """</div>
    <div class="badge-label">&#128274; Encrypted</div>
  </div>
  <div class="badge">
    <div class="badge-num">""" + str(ttl_count) + """</div>
    <div class="badge-label">&#9200; TTL Active</div>
  </div>
  <div class="badge">
    <div class="badge-num">""" + str(expired) + """</div>
    <div class="badge-label">&#9888; Expired</div>
  </div>
</div>

<h2>Text Statistics</h2>
<div class="grid">
  <div class="badge">
    <div class="badge-num">""" + str(int(avg_len)) + """</div>
    <div class="badge-label">Avg Chars</div>
  </div>
  <div class="badge">
    <div class="badge-num">""" + str(max_len) + """</div>
    <div class="badge-label">Max Chars</div>
  </div>
  <div class="badge">
    <div class="badge-num">""" + str(storage) + """</div>
    <div class="badge-label">Storage</div>
  </div>
</div>

<h2>TTL Distribution</h2>
<div class="card">
  <div class="bar-chart">
    <div class="bar-row">
      <div class="bar-label">No TTL</div>
      <div class="bar-track"><div class="bar-fill" style="width:""" + str(pct(no_ttl, total)) + """%;background:#64748b"></div></div>
      <div class="bar-val">""" + str(no_ttl) + """</div>
    </div>
    <div class="bar-row">
      <div class="bar-label">&lt;1h</div>
      <div class="bar-track"><div class="bar-fill" style="width:""" + str(pct(ttl_buckets["<1h"], total)) + """%"></div></div>
      <div class="bar-val">""" + str(ttl_buckets["<1h"]) + """</div>
    </div>
    <div class="bar-row">
      <div class="bar-label">&lt;1d</div>
      <div class="bar-track"><div class="bar-fill" style="width:""" + str(pct(ttl_buckets["<1d"], total)) + """%"></div></div>
      <div class="bar-val">""" + str(ttl_buckets["<1d"]) + """</div>
    </div>
    <div class="bar-row">
      <div class="bar-label">&lt;1w</div>
      <div class="bar-track"><div class="bar-fill" style="width:""" + str(pct(ttl_buckets["<1w"], total)) + """%"></div></div>
      <div class="bar-val">""" + str(ttl_buckets["<1w"]) + """</div>
    </div>
    <div class="bar-row">
      <div class="bar-label">&gt;1w</div>
      <div class="bar-track"><div class="bar-fill" style="width:""" + str(pct(ttl_buckets[">1w"], total)) + """%"></div></div>
      <div class="bar-val">""" + str(ttl_buckets[">1w"]) + """</div>
    </div>
  </div>
</div>

<h2>Top Tags</h2>
<div class="card">""" + tags_html + """</div>

""" + recent_section + """

<div class="footer">
  agent-memory analytics &middot; """ + str(total) + """ memories &middot; """ + str(storage) + """ backend
</div>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate agent-memory analytics dashboard")
    parser.add_argument("--storage", default="json", choices=["json", "sqlite", "redis"])
    parser.add_argument("--path", default="./memory.json")
    parser.add_argument("--output", default="dashboard.html")
    parser.add_argument("--ttl", default=None)
    parser.add_argument("--encryption-key", default=None)
    args = parser.parse_args()

    m = Memory(
        storage=args.storage,
        path=args.path,
        ttl=args.ttl,
        encryption_key=args.encryption_key,
    )

    html = generate_dashboard(m)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print("Dashboard generated:", args.output)
    print("Total memories:", m.count())
    print("Storage:", args.storage)


if __name__ == "__main__":
    main()
