"""
agent-memory MCP Server
MCP (Model Context Protocol) server implementation for agent-memory.

Usage:
    from mcp_server import MemoryServer
    server = MemoryServer(storage="sqlite", path="./memory.db")
    server.run()  # Starts MCP server on stdin/stdout

MCP Tools exposed:
    - memory_search: Search memories by query
    - memory_add: Add a new memory
    - memory_get: Get memories with context
    - memory_clear: Clear all memories

Requirements: agent-memory, mcp[sse]>=1.0.0
Install: pip install agent-memory mcp
"""

from agent_memory import Memory
from typing import Optional, List, Any
import json


class MemoryServer:
    """MCP server for agent-memory."""

    def __init__(
        self,
        storage: str = "json",
        path: str = "./memory.json",
        ttl: Optional[str] = None,
        encryption_key: Optional[str] = None,
    ):
        self.memory = Memory(
            storage=storage,
            path=path,
            ttl=ttl,
            encryption_key=encryption_key,
        )
        self.tools = {
            "memory_search": self._search,
            "memory_add": self._add,
            "memory_get": self._get,
            "memory_clear": self._clear,
        }

    # -------------------------------------------------------------------------
    # MCP Tools
    # -------------------------------------------------------------------------

    def _search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search memories by query string."""
        results = self.memory.search(query, top_k=top_k)
        return [
            {
                "id": r.get("id") or i,
                "content": r.get("content", ""),
                "score": r.get("score", 0),
                "metadata": r.get("metadata", {}),
            }
            for i, r in enumerate(results)
        ]

    def _add(
        self,
        text: str,
        ttl: Optional[str] = None,
        encrypt: bool = False,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Add a new memory."""
        memory_id = self.memory.add(
            text,
            metadata=metadata or {},
            ttl=ttl,
            encrypt=encrypt,
        )
        return {"id": memory_id, "status": "added"}

    def _get(self, max_tokens: int = 2000, max_memories: int = 10) -> dict:
        """Get conversation context from memories."""
        ctx = self.memory.get_context(max_tokens=max_tokens, max_memories=max_memories)
        return {"context": ctx}

    def _clear(self) -> dict:
        """Clear all memories."""
        count = self.memory.count()
        self.memory.clear()
        return {"cleared": count, "status": "ok"}

    # -------------------------------------------------------------------------
    # MCP Protocol Handler
    # -------------------------------------------------------------------------

    def handle_request(self, request: dict) -> dict:
        """Handle incoming MCP JSON-RPC request."""
        method = request.get("method", "")
        request_id = request.get("id")

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": name,
                            "description": func.__doc__ or "",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                            },
                        }
                        for name, func in self.tools.items()
                    ]
                },
            }

        if method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})

            if tool_name in self.tools:
                try:
                    result = self.tools[tool_name](**tool_args)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result, ensure_ascii=False),
                                }
                            ]
                        },
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32603, "message": str(e)},
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                }

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Unknown method: {method}"},
        }

    def run(self):
        """Run MCP server on stdin/stdout."""
        import sys

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                if response:
                    print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "error": {"code": -32700, "message": "Parse error"},
                        }
                    ),
                    flush=True,
                )


if __name__ == "__main__":
    server = MemoryServer(storage="json", path="./memory.json")
    server.run()
