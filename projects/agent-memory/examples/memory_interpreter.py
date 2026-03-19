"""
Memory Interpreter
Interpreter pattern
"""
from memory import Memory


class Expression:
    def interpret(self, context: str) -> bool:
        raise NotImplementedError


class ContainsExpression(Expression):
    def __init__(self, word: str):
        self.word = word
    
    def interpret(self, context: str) -> bool:
        return self.word.lower() in context.lower()


class AndExpression(Expression):
    def __init__(self, exp1: Expression, exp2: Expression):
        self.exp1 = exp1
        self.exp2 = exp2
    
    def interpret(self, context: str) -> bool:
        return self.exp1.interpret(context) and self.exp2.interpret(context)


def demo():
    memory = Memory(storage="json", path="./interpreter_demo.json")
    
    memory.add("Python is great")
    memory.add("JavaScript is ok")
    
    expr = ContainsExpression("python")
    
    for mem in memory.get_all():
        if expr.interpret(mem.get("content", "")):
            print(f"Match: {mem.get('content')}")


if __name__ == "__main__":
    demo()
