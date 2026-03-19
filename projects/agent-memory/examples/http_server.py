"""
Memory HTTP Server
Simple HTTP server for memory
"""
from agent_memory import Memory
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class MemoryHandler(BaseHTTPRequestHandler):
    """HTTP handler for memory"""
    
    memory = None
    
    def do_GET(self):
        """Handle GET"""
        if self.path == "/memories":
            memories = self.memory.get_all()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(memories).encode())
        elif self.path.startswith("/memories/"):
            mem_id = self.path.split("/")[-1]
            mem = self.memory.get(mem_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(mem or {}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST"""
        if self.path == "/memories":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            
            mem_id = self.memory.add(
                content=data.get("content", ""),
                tags=data.get("tags", [])
            )
            
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"id": mem_id}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_DELETE(self):
        """Handle DELETE"""
        if self.path.startswith("/memories/"):
            mem_id = self.path.split("/")[-1]
            self.memory.forget(mem_id)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"deleted": True}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass


def run_server(host="0.0.0.0", port=8080, storage="json", path="./http_memory.json"):
    """Run HTTP server"""
    memory = Memory(storage=storage, path=path)
    MemoryHandler.memory = memory
    
    server = HTTPServer((host, port), MemoryHandler)
    print(f"Server running on http://{host}:{port}")
    server.serve_forever()


def demo():
    """Demo server"""
    print("=== HTTP Server Demo ===\n")
    print("To run server:")
    print("  python -c \"from examples.http_server import run_server; run_server()\"")
    print("\nEndpoints:")
    print("  GET  /memories     - List all")
    print("  GET  /memories/<id> - Get one")
    print("  POST /memories     - Add new")
    print("  DELETE /memories/<id> - Delete")


if __name__ == "__main__":
    demo()
