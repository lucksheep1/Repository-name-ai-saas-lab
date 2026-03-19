"""
Memory HTTP Server
Simple HTTP API for memory
"""
from agent_memory import Memory
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class MemoryHandler(BaseHTTPRequestHandler):
    """HTTP handler for memory"""
    
    memory = Memory(storage="sqlite", path="./http_memory.db")
    
    def do_GET(self):
        """Handle GET"""
        if self.path == "/memories":
            memories = self.memory.get_all()
            self.send_json({"memories": memories})
        
        elif self.path.startswith("/memories/"):
            mem_id = self.path.split("/")[-1]
            mem = self.memory.get(mem_id)
            self.send_json(mem or {"error": "not found"})
        
        elif self.path.startswith("/search?"):
            import urllib.parse
            query = urllib.parse.parse_qs(self.path[8:]).get("q", [""])[0]
            results = self.memory.search(query)
            self.send_json({"results": results})
        
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST"""
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))
        
        if self.path == "/memories":
            mem_id = self.memory.add(
                content=data.get("content", ""),
                tags=data.get("tags", []),
                metadata=data.get("metadata", {})
            )
            self.send_json({"id": mem_id})
        
        else:
            self.send_error(404)
    
    def do_DELETE(self):
        """Handle DELETE"""
        if self.path.startswith("/memories/"):
            mem_id = self.path.split("/")[-1]
            self.memory.forget(mem_id)
            self.send_json({"deleted": mem_id})
        else:
            self.send_error(404)
    
    def send_json(self, data: dict):
        """Send JSON response"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        """Suppress logs"""
        pass


def run_server(host="0.0.0.0", port=8080):
    """Run HTTP server"""
    server = HTTPServer((host, port), MemoryHandler)
    print(f"Memory server running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        print("HTTP Server Demo")
        print("Run: python -m http.server 8080")
    else:
        run_server()
