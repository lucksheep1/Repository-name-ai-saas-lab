"""
Memory http_example5
http_example5
"""
import http.client


def demo():
    conn = http.client.HTTPConnection("example.com")
    conn.request("GET", "/")
    print(conn.getresponse().status)
    conn.close()


if __name__ == "__main__":
    demo()
