"""
Memory http_client_example
http_client_example
"""
import http.client


def demo():
    conn = http.client.HTTPConnection("example.com")
    print(conn)


if __name__ == "__main__":
    demo()
