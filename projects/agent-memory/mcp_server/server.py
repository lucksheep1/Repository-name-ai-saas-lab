#!/usr/bin/env python3
"""
Agent Memory MCP Server
Exposes Agent Memory as a Model Context Protocol (MCP) server.

Usage:
    python mcp_server.py

Then configure your MCP client to connect to stdout JSON-RPC.
"""

import sys
import json
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from agent_memory import Memory
except ImportError:
    print("Error: agent_memory not installed", file=sys.stderr)
    sys.exit(1)

# Import KnowledgeGraph for MCP exposure
import sys
import os
kg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kg.py')
if os.path.exists(kg_path):
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    try:
        from kg import KnowledgeGraph
        HAS_KG = True
    except ImportError:
        HAS_KG = False
else:
    HAS_KG = False

class AgentMemoryMCPServer:
    """MCP Server for Agent Memory."""
    
    def __init__(self):
        self.memory = Memory(storage="json", path="./memory.json")
        self._initialized = True
        # Initialize Knowledge Graph if available
        if HAS_KG:
            self.kg = KnowledgeGraph(self.memory)
        else:
            self.kg = None
    
    def handle_request(self, method, params=None):
        """Handle MCP request."""
        if params is None:
            params = {}
        
        handlers = {
            "initialize": self._initialize,
            "tools/list": self._list_tools,
            "tools/call": self._call_tool,
            "resources/list": self._list_resources,
            "resources/read": self._read_resource,
        }
        
        handler = handlers.get(method)
        if handler:
            return handler(params)
        return {"error": {"code": -32601, "message": f"Method not found: {method}"}}
    
    def _initialize(self, params):
        return {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "agent-memory",
                "version": "3.1.0"
            },
            "capabilities": {
                "tools": {},
                "resources": {}
            }
        }
    
    def _list_tools(self, params):
        # Base memory tools
        tools = [
            {
                "name": "memory_add",
                "description": "Add a new memory to the agent's memory store",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Memory text content"},
                        "ttl": {"type": "string", "description": "TTL in string format (e.g., '7d', '1h')"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for the memory"},
                        "encrypt": {"type": "boolean", "description": "Encrypt this memory"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "memory_search",
                "description": "Search memories by query",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "top_k": {"type": "integer", "description": "Max results", "default": 5}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "memory_get_recent",
                "description": "Get recent memories",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Max memories", "default": 10}
                    }
                }
            },
            {
                "name": "memory_get_by_tag",
                "description": "Get memories by tag",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tag": {"type": "string", "description": "Tag to filter by"}
                    },
                    "required": ["tag"]
                }
            },
            {
                "name": "memory_get_context",
                "description": "Get condensed context for agent",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "max_tokens": {"type": "integer", "default": 2000},
                        "max_memories": {"type": "integer", "default": 10}
                    }
                }
            },
            {
                "name": "memory_stats",
                "description": "Get memory statistics",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "memory_delete",
                "description": "Delete a memory by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "memory_id": {"type": "string", "description": "Memory ID to delete"}
                    },
                    "required": ["memory_id"]
                }
            },
            {
                "name": "memory_timeline",
                "description": "Get memories as timeline",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Max memories", "default": 20}
                    }
                }
            },
            {
                "name": "memory_export",
                "description": "Export memories to JSON file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "Output file path"}
                    },
                    "required": ["filepath"]
                }
            }
        ]
        
        # Add Knowledge Graph tools if available
        if HAS_KG:
            kg_tools = [
                {
                    "name": "kg_add_entity",
                    "description": "Add entity to knowledge graph",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Entity name"},
                            "entity_type": {"type": "string", "description": "Type (person, project, etc)"},
                            "observations": {"type": "array", "items": {"type": "string"}, "description": "List of observations"}
                        },
                        "required": ["name", "entity_type"]
                    }
                },
                {
                    "name": "kg_add_relation",
                    "description": "Add relation between entities",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "from_entity": {"type": "string", "description": "Source entity"},
                            "to_entity": {"type": "string", "description": "Target entity"},
                            "relation_type": {"type": "string", "description": "Relation type (uses, maintains, etc)"}
                        },
                        "required": ["from_entity", "to_entity", "relation_type"]
                    }
                },
                {
                    "name": "kg_query",
                    "description": "Query knowledge graph",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "entity_name": {"type": "string", "description": "Filter by entity name"},
                            "entity_type": {"type": "string", "description": "Filter by entity type"}
                        }
                    }
                },
                {
                    "name": "kg_neighbors",
                    "description": "Get entities connected to an entity",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "entity_name": {"type": "string", "description": "Entity to find neighbors for"},
                            "relation_type": {"type": "string", "description": "Filter by relation type"}
                        },
                        "required": ["entity_name"]
                    }
                },
                {
                    "name": "kg_export",
                    "description": "Export entire graph as JSON",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "kg_find_path",
                    "description": "Find path between two entities",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "from_entity": {"type": "string", "description": "Start entity"},
                            "to_entity": {"type": "string", "description": "Target entity"},
                            "max_depth": {"type": "integer", "description": "Max hops", "default": 3}
                        },
                        "required": ["from_entity", "to_entity"]
                    }
                }
            ]
            tools.extend(kg_tools)
        
        return {"tools": tools}
    
    def _call_tool(self, params):
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if name == "memory_add":
                tags = arguments.get("tags", [])
                if tags:
                    result = self.memory.add_with_tags(
                        text=arguments["text"],
                        tags=tags,
                        ttl=arguments.get("ttl"),
                        encrypt=arguments.get("encrypt", False)
                    )
                else:
                    result = self.memory.add(
                        text=arguments["text"],
                        ttl=arguments.get("ttl"),
                        encrypt=arguments.get("encrypt", False)
                    )
                return {"content": [{"type": "text", "text": f"Memory added: {result}"}]}
            
            elif name == "memory_search":
                results = self.memory.search(
                    query=arguments["query"],
                    top_k=arguments.get("top_k", 5)
                )
                return {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]}
            
            elif name == "memory_get_recent":
                results = self.memory.get_recent(limit=arguments.get("limit", 10))
                return {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]}
            
            elif name == "memory_get_by_tag":
                results = self.memory.get_by_tag(arguments["tag"])
                return {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]}
            
            elif name == "memory_get_context":
                context = self.memory.get_context(
                    max_tokens=arguments.get("max_tokens", 2000),
                    max_memories=arguments.get("max_memories", 10)
                )
                return {"content": [{"type": "text", "text": context}]}
            
            elif name == "memory_stats":
                stats = {
                    "total": self.memory.count(),
                    "recent": len(self.memory.get_recent(limit=100))
                }
                return {"content": [{"type": "text", "text": json.dumps(stats, indent=2)}]}
            
            elif name == "memory_delete":
                success = self.memory.delete(arguments["memory_id"])
                return {"content": [{"type": "text", "text": f"Deleted: {success}"}]}
            
            elif name == "memory_timeline":
                results = self.memory.get_timeline(limit=arguments.get("limit", 20))
                return {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]}
            
            elif name == "memory_export":
                self.memory.export(arguments["filepath"])
                return {"content": [{"type": "text", "text": f"Exported to {arguments['filepath']}"}]}
            
            # Knowledge Graph tools
            elif name == "kg_add_entity" and HAS_KG:
                result = self.kg.add_entity(
                    name=arguments["name"],
                    entity_type=arguments["entity_type"],
                    observations=arguments.get("observations", [])
                )
                return {"content": [{"type": "text", "text": f"Entity added: {result}"}]}
            
            elif name == "kg_add_relation" and HAS_KG:
                result = self.kg.add_relation(
                    from_entity=arguments["from_entity"],
                    to_entity=arguments["to_entity"],
                    relation_type=arguments["relation_type"]
                )
                return {"content": [{"type": "text", "text": f"Relation added: {result}"}]}
            
            elif name == "kg_query" and HAS_KG:
                result = self.kg.query(
                    entity_name=arguments.get("entity_name"),
                    entity_type=arguments.get("entity_type")
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "kg_neighbors" and HAS_KG:
                result = self.kg.get_neighbors(
                    entity_name=arguments["entity_name"],
                    relation_type=arguments.get("relation_type")
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "kg_export" and HAS_KG:
                result = self.kg.export_graph()
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "kg_find_path" and HAS_KG:
                result = self.kg.find_path(
                    from_entity=arguments["from_entity"],
                    to_entity=arguments["to_entity"],
                    max_depth=arguments.get("max_depth", 3)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            else:
                return {"error": {"code": -32602, "message": f"Unknown tool: {name}"}}
        
        except Exception as e:
            return {"error": {"code": -32603, "message": str(e)}}
    
    def _list_resources(self, params):
        return {"resources": []}
    
    def _read_resource(self, params):
        return {"error": {"code": -32601, "message": "Resources not implemented"}}


def main():
    """Run MCP server on stdin/stdout."""
    server = AgentMemoryMCPServer()
    
    # Read JSON-RPC requests from stdin
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            msg_id = request.get("id")
            
            result = server.handle_request(method, params)
            
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": result
            }
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()