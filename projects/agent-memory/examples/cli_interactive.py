"""
Memory Command Line Interface
Full CLI for memory management
"""
from agent_memory import Memory
import sys
import json


class MemoryCLI:
    """Command-line interface for memory"""
    
    def __init__(self, storage="json", path="./cli_memory.json"):
        self.memory = Memory(storage=storage, path=path)
    
    def run(self, args: list = None):
        """Run CLI"""
        args = args or sys.argv[1:]
        
        if not args:
            self.help()
            return
        
        command = args[0]
        
        if command == "add":
            self.cmd_add(args[1:])
        elif command == "search":
            self.cmd_search(args[1:])
        elif command == "list":
            self.cmd_list(args[1:])
        elif command == "get":
            self.cmd_get(args[1:])
        elif command == "delete":
            self.cmd_delete(args[1:])
        elif command == "tags":
            self.cmd_tags(args[1:])
        elif command == "help":
            self.help()
        else:
            print(f"Unknown command: {command}")
            self.help()
    
    def cmd_add(self, args):
        """Add memory"""
        if not args:
            print("Usage: add <content>")
            return
        
        content = " ".join(args)
        mem_id = self.memory.add(content)
        print(f"Added: {mem_id}")
    
    def cmd_search(self, args):
        """Search memories"""
        if not args:
            print("Usage: search <query>")
            return
        
        query = " ".join(args)
        results = self.memory.search(query)
        
        print(f"Found {len(results)} results:")
        for r in results:
            print(f"  [{r.get('id')}] {r.get('content')[:60]}")
    
    def cmd_list(self, args):
        """List all memories"""
        all_mem = self.memory.get_all()
        
        print(f"Total: {len(all_mem)} memories")
        for m in all_mem[:20]:
            print(f"  [{m.get('id')}] {m.get('content')[:60]}")
    
    def cmd_get(self, args):
        """Get single memory"""
        if not args:
            print("Usage: get <id>")
            return
        
        mem_id = args[0]
        mem = self.memory.get(mem_id)
        
        if mem:
            print(json.dumps(mem, indent=2))
        else:
            print("Not found")
    
    def cmd_delete(self, args):
        """Delete memory"""
        if not args:
            print("Usage: delete <id>")
            return
        
        mem_id = args[0]
        self.memory.forget(mem_id)
        print(f"Deleted: {mem_id}")
    
    def cmd_tags(self, args):
        """List all tags"""
        tags = set()
        
        for mem in self.memory.get_all():
            tags.update(mem.get("tags", []))
        
        print(f"Tags: {sorted(tags)}")
    
    def help(self):
        """Show help"""
        print("""
Memory CLI

Commands:
  add <content>      Add a memory
  search <query>     Search memories
  list               List all memories
  get <id>           Get memory by ID
  delete <id>        Delete memory
  tags               List all tags
  help               Show this help
""")


def demo():
    """Demo CLI"""
    cli = MemoryCLI(storage="json", path="./cli_demo.json")
    
    print("=== Memory CLI Demo ===\n")
    
    # Simulate CLI commands
    print("$ add Hello world")
    cli.cmd_add(["Hello", "world"])
    
    print("$ add Python is great")
    cli.cmd_add(["Python", "is", "great"])
    
    print("$ search python")
    cli.cmd_search(["python"])
    
    print("$ tags")
    cli.cmd_tags([])
    
    # Cleanup
    import os
    if os.path.exists("./cli_demo.json"):
        os.remove("./cli_demo.json")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        cli = MemoryCLI()
        cli.run()
