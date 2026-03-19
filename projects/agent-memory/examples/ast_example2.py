"""
Memory ast_example2
ast_example2
"""
import ast


def demo():
    tree = ast.parse("x = 1 + 2")
    print(ast.dump(tree))


if __name__ == "__main__":
    demo()
