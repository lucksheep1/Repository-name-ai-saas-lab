"""
Memory http_example9
http_example9
"""
import http.server


def demo():
    server = http.server.HTTPServer(("localhost", 0), http.server.SimpleHTTPRequestHandler)
    print(server.server_address[1])
    server.server_close()


if __name__ == "__main__":
    demo()
