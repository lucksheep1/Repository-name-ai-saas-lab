"""
Memory CLI Advanced
Advanced CLI features
"""
from agent_memory import Memory
import sys


class AdvancedCLI:
    """Advanced CLI"""
    
    def __init__(self):
        self.memory = Memory(storage="json", path="./cli_adv.json")
        self.commands = {
            "add": self.cmd_add,
            "search": self.cmd_search,
            "list": self.cmd_list,
            "tag": self.cmd_tag,
            "export": self.cmd_export,
            "stats": self.cmd_stats,
        }
    
    def run(self, args):
        """Run command"""
        if not args:
            self.help()
            return
        
        cmd = args[0]
        
        if cmd in self.commands:
            self.commands[cmd](args[1:])
        else:
            print(f"Unknown: {cmd}")
            self.help()
    
    def cmd_add(self, args):
        """Add memory"""
        if not args:
            print("Usage: add <content> [--tags t1,t2]")
            return
        
        content = " ".join(args)
        
        tags = []
        if "--tags" in content:
            idx = content.index("--tags")
            tags = content[idx+1].split(",")
            content = " ".join(content[:idx])
        
        mem_id = self.memory.add(content, tags=tags)
        print(f"Added: {mem_id}")
    
    def cmd_search(self, args):
        """Search"""
        if not args:
            print("Usage: search <query>")
            return
        
        query = " ".join(args)
        results = self.memory.search(query)
        
        print(f"Found {len(results)}:")
        for r in results[:5]:
            print(f"  {r.get('content')[:50]}")
    
    def cmd_list(self, args):
        """List all"""
        limit = int(args[0]) if args else 10
        
        for mem in self.memory.get_all()[:limit]:
            print(f"  {mem.get('id')[:8]} | {mem.get('content')[:40]}")
    
    def cmd_tag(self, args):
        """Tag operations"""
        if len(args) < 2:
            print("Usage: tag <mem_id> <tag>")
            return
        
        mem_id, tag = args[0], args[1]
        
        mem = self.memory.get(mem_id)
        if mem:
            tags = mem.get("tags", [])
            tags.append(tag)
            self.memory.update(mem_id, tags=tags)
            print(f"Tagged: {mem_id}")
    
    def cmd_export(self, args):
        """Export"""
        print(f"Total: {len(self.memory.get_all())} memories")
    
    def cmd_stats(self, args):
        """Stats"""
        stats = {"total": len(self.memory.get_all())}
        print(f"Stats: {stats}")
    
    def help(self):
        """Help"""
        print("Commands: add, search, list, tag, export, stats")


if __name__ == "__main__":
    cli = AdvancedCLI()
    cli.run(sys.argv[1:])
