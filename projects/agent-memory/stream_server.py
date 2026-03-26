#!/usr/bin/env python3
"""
agent-memory SSE Streaming Server

Usage:
    python stream_server.py --storage json --path ./memory.json --port 8080

Endpoints:
    GET /stream          - SSE stream of memory events
    GET /health          - Health check
    GET /stats           - Memory statistics
    POST /emit           - Emit a custom event to all SSE clients

SSE Event Types:
    - memory:added       - New memory added
    - memory:cleared     - All memories cleared
    - custom:<type>      - Custom event from /emit
"""

import argparse
import json
import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from collections import defaultdict

from agent_memory import Memory, _UNSET


class SSEManager:
    """Manages SSE client connections."""

    def __init__(self):
        self.clients: list = []
        self._lock = threading.Lock()

    def add_client(self, queue):
        with self._lock:
            self.clients.append(queue)

    def remove_client(self, queue):
        with self._lock:
            if queue in self.clients:
                self.clients.remove(queue)

    def broadcast(self, event_type: str, data: dict):
        message = f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
        dead = []
        with self._lock:
            for queue in self.clients:
                try:
                    queue.put_nowait(message)
                except:
                    dead.append(queue)
            for q in dead:
                self.clients.remove(q)


class StreamHandler(BaseHTTPRequestHandler):
    sse_manager: SSEManager = None
    memory: Memory = None

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def send_json(self, status: int, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_sse(self, event_type: str, data: dict):
        message = f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
        self.wfile.write(message.encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

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
                "sse_clients": len(self.sse_manager.clients),
            })
        elif path == "/stream":
            self._handle_sse()
        else:
            self.send_json(404, {"error": "Not found"})

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
                # Broadcast to SSE clients
                self.sse_manager.broadcast("memory:added", {
                    "id": mid,
                    "text": text,
                    "ttl": str(ttl) if ttl is not None else None,
                })
                self.send_json(201, {"id": mid, "status": "added"})
            elif path == "/emit":
                event_type = body.get("type", "custom")
                data = body.get("data", {})
                self.sse_manager.broadcast(f"custom:{event_type}", data)
                self.send_json(200, {"broadcast": "ok"})
            elif path == "/clear":
                count = self.memory.count()
                self.memory.clear()
                self.sse_manager.broadcast("memory:cleared", {"count": count})
                self.send_json(200, {"cleared": count})
            else:
                self.send_json(404, {"error": "Not found"})
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _handle_sse(self):
        import queue
        q = queue.Queue()
        self.sse_manager.add_client(q)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # Send initial ping
        self.send_sse("ping", {"time": time.time()})

        try:
            while True:
                try:
                    msg = q.get(timeout=30)
                    self.wfile.write(msg.encode())
                    self.wfile.flush()
                except queue.Empty:
                    # Send keepalive
                    self.send_sse("ping", {"time": time.time()})
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            self.sse_manager.remove_client(q)


def run_server(storage: str, path: str, port: int):
    manager = SSEManager()
    StreamHandler.sse_manager = manager
    StreamHandler.memory = Memory(storage=storage, path=path)
    server = HTTPServer(("0.0.0.0", port), StreamHandler)
    print(f"🚀 agent-memory SSE server running on http://0.0.0.0:{port}")
    print(f"   SSE stream: GET /stream")
    print(f"   Stats: GET /stats  |  Add: POST /memories  |  Emit: POST /emit")
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="agent-memory SSE streaming server")
    parser.add_argument("--storage", default="json", choices=["json", "sqlite", "redis"])
    parser.add_argument("--path", default="./memory.json")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    run_server(args.storage, args.path, args.port)
