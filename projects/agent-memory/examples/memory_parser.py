"""
Memory Parser
Parse memory queries
"""
from memory import Memory


class Parser:
    @staticmethod
    def parse(query: str) -> dict:
        parts = query.split()
        cmd = parts[0] if parts else ""
        
        return {"command": cmd, "args": parts[1:], "raw": query}


def demo():
    print(Parser.parse("add Hello World"))


if __name__ == "__main__":
    demo()
