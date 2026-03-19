"""
Memory string_example2
string_example2
"""
import string


def demo():
    print(string.Template("$name is $age years old").substitute(name="Alice", age=30))


if __name__ == "__main__":
    demo()
