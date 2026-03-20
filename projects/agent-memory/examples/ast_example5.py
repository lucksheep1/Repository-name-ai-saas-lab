"""
Memory ast_example5
ast_example5
"""
import ast


def demo():
    tree = ast.parse("print('hello')")
    print(ast.dump(tree))


if __name__ == "__main__":
    demo()
