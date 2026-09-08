#!/usr/bin/env python3
import argparse
import http.server
import os
import socketserver

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8080
HOST = "127.0.0.1"


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the SweetQR web app")
    parser.add_argument("--host", default=HOST, help="Address to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=PORT, help="Port (default: 8080)")
    args = parser.parse_args()

    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(BASE_DIR)

    with socketserver.TCPServer((args.host, args.port), handler) as httpd:
        print(f"SweetQR available at http://{args.host}:{args.port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()