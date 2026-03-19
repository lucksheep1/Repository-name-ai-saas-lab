"""
Memory http_example2
http_example2
"""
import http.client


def demo():
    conn = http.client.HTTPSConnection("example.com")
    print(conn)


if __name__ == "__main__":
    demo()
