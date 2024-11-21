#############################################################
### This code is a basic server using http.server in Python
### Run takes two things from the http.server class
### A server class, and a handler class. When the server class
### is constructed with `server_class()`, it takes two things
### an address containing an ip address and port, and a handler class.
### The handler class by default doesn't do anything much.
### It will just throw an error. But at least it responds!
### 1. Try changing `BaseHTTPRequestHandler` to `SimpleHTTPRequestHandler`
###         What happens?
#############################################################

from http.server import HTTPServer,BaseHTTPRequestHandler

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    print("running server")
    httpd.serve_forever()

run()