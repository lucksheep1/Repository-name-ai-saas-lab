"""
Memory tokenize_example7
tokenize_example7
"""
import tokenize
import io


def demo():
    code = "x = 1 + 2\ny = 3"
    for tok in tokenize.generate_tokens(io.StringIO(code).readline):
        if tok.type == tokenize.NUMBER:
            print(tok.string)


if __name__ == "__main__":
    demo()
