"""
Memory ast_example8
ast_example8
"""
import ast


def demo():
    tree = ast.parse("x = 1 + 2")
    print(ast.dump(tree)[:50])


if __name__ == "__main__":
    demo()
