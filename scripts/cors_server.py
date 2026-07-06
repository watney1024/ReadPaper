import http.server, os, sys

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()
    def log_message(self, format, *args):
        pass  # 静默日志

os.chdir(sys.argv[1])
server = http.server.HTTPServer(("127.0.0.1", 18765), CORSHandler)
server.serve_forever()
