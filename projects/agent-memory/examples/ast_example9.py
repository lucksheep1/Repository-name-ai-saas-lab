"""
Memory ast_example9
ast_example9
"""
import ast


def demo():
    tree = ast.parse("""
def greet(name):
    return f"Hello, {name}!"
""")
    print(ast.dump(tree, indent=2)[:100])


if __name__ == "__main__":
    demo()
