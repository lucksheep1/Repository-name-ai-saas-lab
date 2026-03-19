"""
Memory GraphQL API
GraphQL interface for memory
"""
from agent_memory import Memory


class GraphQLResolver:
    """Simple GraphQL resolver for memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def resolve(self, query: str, variables: dict = None) -> dict:
        """Resolve GraphQL query"""
        variables = variables or {}
        
        # Simple query parsing
        if "memories" in query:
            if "search" in query:
                # Extract search term from variables
                search = variables.get("search", "")
                results = self.memory.search(search)
                return {"data": {"memories": results}}
            else:
                # Return all
                return {"data": {"memories": self.memory.get_all()}}
        
        if "memory" in query and "id" in variables:
            mem = self.memory.get(variables["id"])
            return {"data": {"memory": mem}}
        
        return {"errors": [{"message": "Unknown query"}]}
    
    def execute(self, query: str, variables: dict = None) -> dict:
        """Execute query with error handling"""
        try:
            return self.resolve(query, variables)
        except Exception as e:
            return {"errors": [{"message": str(e)}]}


# Example GraphQL schema
SCHEMA = """
type Memory {
    id: ID!
    content: String!
    tags: [String!]
    created_at: String
}

type Query {
    memories(search: String): [Memory]
    memory(id: ID!): Memory
}

type Mutation {
    addMemory(content: String!, tags: [String]): Memory
    deleteMemory(id: ID!): Boolean
}
"""


def demo():
    """Demo GraphQL"""
    memory = Memory(storage="json", path="./graphql_demo.json")
    resolver = GraphQLResolver(memory)
    
    print("=== Memory GraphQL Demo ===\n")
    
    # Add some memories
    memory.add("First memory", tags=["test"])
    memory.add("Second memory", tags=["test"])
    
    # Execute queries
    print("Query: memories")
    result = resolver.execute("memories", {})
    print(f"Result: {len(result['data']['memories'])} memories")
    
    print("\nQuery: memories(search='first')")
    result = resolver.execute("memories", {"search": "first"})
    print(f"Result: {len(result['data']['memories'])} found")
    
    # Cleanup
    import os
    if os.path.exists("./graphql_demo.json"):
        os.remove("./graphql_demo.json")


if __name__ == "__main__":
    demo()
