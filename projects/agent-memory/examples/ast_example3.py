"""
Memory ast_example3
ast_example3
"""
import ast


def demo():
    tree = ast.parse("print('hello')")
    print(ast.dump(tree)[:50])


if __name__ == "__main__":
    demo()
