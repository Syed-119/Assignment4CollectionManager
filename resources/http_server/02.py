#############################################################
### Simple HTTP server models the traditional functionality
### of a web server.
### 1. Try adding a html file to your directory and clicking it.
###      What happens?
#############################################################

from http.server import HTTPServer,SimpleHTTPRequestHandler

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    print("running server")
    httpd.serve_forever()

run()