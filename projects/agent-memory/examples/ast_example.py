"""
Memory ast_example
ast_example
"""
import ast


def demo():
    tree = ast.parse("x = 1")
    print(ast.dump(tree))


if __name__ == "__main__":
    demo()
