"""
Memory ast_example4
ast_example4
"""
import ast


def demo():
    tree = ast.parse("x = 1 + 2")
    print(ast.dump(tree))


if __name__ == "__main__":
    demo()
