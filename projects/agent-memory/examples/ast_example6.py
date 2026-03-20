"""
Memory ast_example6
ast_example6
"""
import ast


def demo():
    print(ast.walk(ast.parse("x = 1")))


if __name__ == "__main__":
    demo()
