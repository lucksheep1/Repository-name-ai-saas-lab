"""
Memory html_example3
html_example3
"""
import html.parser


class MyParser(html.parser.HTMLParser):
    def handle_data(self, data):
        print(f"Data: {data}")


def demo():
    parser = MyParser()
    parser.feed("<p>Hello</p>")


if __name__ == "__main__":
    demo()
