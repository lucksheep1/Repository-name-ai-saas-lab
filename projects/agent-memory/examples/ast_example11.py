"""
Memory ast_example11
ast_example11
"""
import ast


def demo():
    tree = ast.parse("x = 1")
    print(ast.dump(tree))


if __name__ == "__main__":
    demo()
