#!/usr/bin/env python3
"""
agent-memory HTTP API server

Usage:
    python http_server.py --storage json --path ./memory.json --port 8080

Endpoints:
    GET  /memories          - List all memories
    GET  /memories/search   - Search memories ?q=query
    POST /memories           - Add memory {"text":"...", "ttl":"1h", "encrypt":false}
    GET  /memories/context   - Get conversation context ?max_tokens=2000
    DELETE /memories         - Clear all memories
    GET  /stats             - Memory statistics
    GET  /health            - Health check
"""

import argparse
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(__file__.rsplit("/", 1)[0] if "/" in __file__ else "."))
from agent_memory import Memory, _UNSET


class MemoryHandler(BaseHTTPRequestHandler):
    memory: Memory = None

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def send_json(self, status: int, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        try:
            if path == "/health":
                self.send_json(200, {"status": "ok"})
            elif path == "/stats":
                mems = self.memory.memories
                encrypted = sum(1 for m in mems if m.get("metadata", {}).get("encrypted"))
                ttl_count = sum(1 for m in mems if m.get("expires_at"))
                self.send_json(200, {
                    "count": len(mems),
                    "encrypted": encrypted,
                    "with_ttl": ttl_count,
                    "storage": self.memory.storage,
                })
            elif path == "/memories":
                self.send_json(200, {"memories": self.memory.memories})
            elif path == "/memories/context":
                max_tokens = int(qs.get("max_tokens", [2000])[0])
                max_memories = int(qs.get("max_memories", [10])[0])
                ctx = self.memory.get_context(max_tokens=max_tokens, max_memories=max_memories)
                self.send_json(200, {"context": ctx})
            elif path == "/memories/search":
                query = qs.get("q", [""])[0]
                top_k = int(qs.get("top_k", [5])[0])
                results = self.memory.search(query, top_k=top_k)
                self.send_json(200, {"results": results})
            else:
                self.send_json(404, {"error": "Not found"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length > 0 else {}

            if path == "/memories":
                text = body.get("text", "")
                ttl = body.get("ttl", _UNSET)
                encrypt = body.get("encrypt", False)
                metadata = body.get("metadata", {})

                if not text:
                    self.send_json(400, {"error": "text is required"})
                    return

                mid = self.memory.add(text=text, ttl=ttl, encrypt=encrypt, metadata=metadata)
                self.send_json(201, {"id": mid, "status": "added"})
            else:
                self.send_json(404, {"error": "Not found"})
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            if path == "/memories":
                count = self.memory.count()
                self.memory.clear()
                self.send_json(200, {"cleared": count})
            else:
                self.send_json(404, {"error": "Not found"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run_server(storage: str, path: str, port: int, ttl: str = None, encryption_key: str = None):
    MemoryHandler.memory = Memory(
        storage=storage,
        path=path,
        ttl=ttl,
        encryption_key=encryption_key,
    )
    server = HTTPServer(("0.0.0.0", port), MemoryHandler)
    print(f"🚀 agent-memory HTTP server running on http://0.0.0.0:{port}")
    print(f"   Storage: {storage} ({path})")
    print(f"   Docs: GET /health  GET /stats  GET /memories  POST /memories")
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="agent-memory HTTP API server")
    parser.add_argument("--storage", default="json", choices=["json", "sqlite", "redis"])
    parser.add_argument("--path", default="./memory.json")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--ttl", default=None)
    parser.add_argument("--encryption-key", default=None)
    args = parser.parse_args()
    run_server(args.storage, args.path, args.port, args.ttl, args.encryption_key)
