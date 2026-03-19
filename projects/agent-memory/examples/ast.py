"""
Memory ast
ast utilities
"""
import ast


def demo():
    tree = ast.parse("x = 1")
    print(ast.dump(tree)[:50])


if __name__ == "__main__":
    demo()
