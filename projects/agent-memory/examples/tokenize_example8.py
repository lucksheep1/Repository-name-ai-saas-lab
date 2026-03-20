"""
Memory tokenize_example8
tokenize_example8
"""
import tokenize
import io


def demo():
    text = "x = 1 + 2"
    tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    for tok in tokens:
        if tok.type != tokenize.ENCODING:
            print(tok.type, tok.string)


if __name__ == "__main__":
    demo()
