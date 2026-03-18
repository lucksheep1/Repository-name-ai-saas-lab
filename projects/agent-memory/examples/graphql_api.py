#!/usr/bin/env python3
"""
Agent Memory - GraphQL API
==========================
GraphQL API for memory.

Usage:
    python graphql_api.py
    
    # Query example:
    # {
    #   memories(limit: 5) { id text tags }
    # }
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_memory import Memory

# Simple GraphQL implementation (for demo)
memory = Memory(storage="json", path="./memory.json")


class GraphQLSchema:
    """Simple GraphQL schema."""
    
    def __init__(self):
        self.memory = memory
    
    def resolve(self, query: str, variables: dict = None):
        """Resolve GraphQL query."""
        query = query.strip()
        variables = variables or {}
        
        # Parse query
        if "memories" in query:
            limit = variables.get("limit", 10)
            memories = self.memory.get_recent(limit=limit)
            
            # Extract fields
            fields = self._extract_fields(query, "memories")
            
            result = []
            for mem in memories:
                item = {}
                if "id" in fields:
                    item["id"] = mem["id"]
                if "text" in fields:
                    item["text"] = mem["text"]
                if "tags" in fields:
                    item["tags"] = mem.get("tags", [])
                if "timestamp" in fields:
                    item["timestamp"] = mem.get("timestamp", "")
                if "priority" in fields:
                    item["priority"] = mem.get("priority", 0)
                result.append(item)
            
            return {"data": {"memories": result}}
        
        if "search" in query:
            query_text = variables.get("query", "")
            limit = variables.get("limit", 5)
            results = self.memory.search(query_text, top_k=limit)
            
            fields = self._extract_fields(query, "search")
            
            result = []
            for mem in results:
                item = {}
                if "text" in fields:
                    item["text"] = mem["text"]
                result.append(item)
            
            return {"data": {"search": result}}
        
        if "context" in query:
            max_tokens = variables.get("max_tokens", 2000)
            context = self.memory.get_context(max_tokens=max_tokens)
            return {"data": {"context": context}}
        
        if "stats" in query:
            return {"data": {"stats": {"count": self.memory.count()}}}
        
        return {"errors": [{"message": "Unknown query"}]}
    
    def _extract_fields(self, query: str, root_field: str) -> List[str]:
        """Extract requested fields."""
        fields = []
        
        # Find the block for this field
        import re
        pattern = f"{root_field}\\s*{{([^}}]+)}}"
        match = re.search(pattern, query)
        
        if match:
            block = match.group(1)
            # Extract field names
            for line in block.split("\n"):
                line = line.strip().rstrip("{").strip()
                if line and not line.startswith("#"):
                    fields.append(line.split(" ")[0].split("(")[0])
        
        return fields


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "graphql_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - GraphQL API Demo")
    print("=" * 50)
    
    # Create memory with data
    memory = Memory(storage="json", path=demo_path)
    memory.add_with_tags("Fix bug", tags=["bug", "urgent"])
    memory.add_with_tags("Add feature", tags=["feature"])
    memory.add_with_tags("Write tests", tags=["testing"])
    
    # Create GraphQL schema
    schema = GraphQLSchema()
    schema.memory = memory
    
    # Query 1: Get memories
    print("\n1. Query: memories(limit: 2)")
    query1 = """
    {
        memories(limit: 2) {
            id
            text
            tags
        }
    }
    """
    result1 = schema.resolve(query1)
    print(f"   Result: {result1}")
    
    # Query 2: Search
    print("\n2. Query: search(query: 'bug')")
    query2 = """
    {
        search(query: "bug") {
            text
        }
    }
    """
    result2 = schema.resolve(query2, {"query": "bug"})
    print(f"   Result: {result2}")
    
    # Query 3: Stats
    print("\n3. Query: stats")
    query3 = "{ stats { count } }"
    result3 = schema.resolve(query3)
    print(f"   Result: {result3}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
