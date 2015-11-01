import time
import BaseHTTPServer


HOST_NAME = 'localhost'  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80  # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        print 1

    def do_GET(s):
        print 1
        # """Respond to a GET request."""
        # s.send_response(200)
        # s.send_header("Content-type", "text/html")
        # s.end_headers()
        # s.wfile.write("<html><head><title>Title goes here.</title></head>")
        # s.wfile.write("<body><p>This is a test.</p>")
        # # If someone went to "http://something.somewhere.net/foo/bar/",
        # # then s.path equals "/foo/bar/".
        # s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        # s.wfile.write("</body></html>")


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    for port in range(9100, 9105):
        httpd = server_class((HOST_NAME, port), MyHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()