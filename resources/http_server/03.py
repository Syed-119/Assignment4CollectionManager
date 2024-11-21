#############################################################
### This code takes advantage of object-oriented coding.
### With the 'ServerHandler' class, we can define our own
### variant of the BaseHTTPRequestHandler, with a working get 
### response. The 'self' allows us to attach a function to the
### class (or subclass) itself - this is called a method.
### 1. What is being returned in the console here when we 
### access the server from the browser. What is this?
#############################################################

from http.server import HTTPServer,SimpleHTTPRequestHandler

class ServerHandler(SimpleHTTPRequestHandler):    
    def do_GET(self):
        print(self.headers)
        SimpleHTTPRequestHandler.do_GET(self)

def run(server_class=HTTPServer, handler_class=ServerHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    print("running server")
    httpd.serve_forever()

run()