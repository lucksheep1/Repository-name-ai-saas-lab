"""
Memory keyword_example2
keyword_example2
"""
import keyword


def demo():
    print(keyword.iskeyword("if"))
    print(keyword.iskeyword("foo"))


if __name__ == "__main__":
    demo()
