import http.server
import socketserver
import os

PORT = 12001  # Using port 12001 for E-Borrow

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('X-Frame-Options', 'ALLOWALL')
        super().end_headers()

    def do_GET(self):
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

Handler = CORSHTTPRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"E-Borrow server running at http://0.0.0.0:{PORT}")
    print(f"Access the website at https://work-2-ktgelzsfqhtmxoqe.prod-runtime.all-hands.dev")
    print("\nAvailable pages:")
    print("- Homepage: /")
    print("- Login/Register: /login.html")
    print("- Browse Items: /search.html")
    print("- Post Item: /post-item.html")
    print("- Item Details: /item-detail.html")
    print("- User Dashboard: /dashboard.html")
    print("- Admin Dashboard: /admin.html")
    httpd.serve_forever()