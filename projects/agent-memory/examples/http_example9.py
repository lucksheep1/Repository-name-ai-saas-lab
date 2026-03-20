"""
Memory http_example9
http_example9
"""
import http.client


def demo():
    conn = http.client.HTTPConnection("example.com", 80)
    conn.request("GET", "/")
    print(conn.getresponse().status)
    conn.close()


if __name__ == "__main__":
    demo()
