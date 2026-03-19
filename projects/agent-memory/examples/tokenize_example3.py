"""
Memory tokenize_example3
tokenize_example3
"""
import tokenize
import io


def demo():
    code = "x = 1 + 2"
    tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    print(len(tokens))


if __name__ == "__main__":
    demo()
