#############################################################
### This code takes advantage of object-oriented coding.
### With the 'ServerHandler' class, we can define our own
### variant of the BaseHTTPRequestHandler, with a working get 
### response. The 'self' allows us to attach a function to the
### class (or subclass) itself - this is called a method.
### 1. What does the code after send_response mean? \
###    HINT: See http.cat for help
### 2. What happens if we don't add the 'end_headers' function
### 3. What happens if we don't add the bytes function?
#############################################################

from http.server import HTTPServer,SimpleHTTPRequestHandler

class ServerHandler(SimpleHTTPRequestHandler):    
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'html')
        self.end_headers()
        my_string = "<html><body>Test</body></html>"
        self.wfile.write(bytes(my_string, 'UTF-8'))

def run(server_class=HTTPServer, handler_class=ServerHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    print("running server")
    httpd.serve_forever()

run()