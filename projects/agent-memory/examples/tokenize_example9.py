"""
Memory tokenize_example9
tokenize_example9
"""
import tokenize
import io


def demo():
    text = "x = 1"
    toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    print(len(toks))


if __name__ == "__main__":
    demo()
