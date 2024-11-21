#############################################################
### This code takes advantage of the 'path' property that is
### added to a Request Handler when it is used. It represents
### the directory that was accessed, i.e. all the query after
### the domain name or ip. We use an if statement here.
### 1. Try the code. What happens if you go to the regular path.
###      What happens if you go to the domain/ip and add `/roll/`
### 2. Try to build a more advanced routing system using
###       this code as a base./
#############################################################

from http.server import HTTPServer,SimpleHTTPRequestHandler
import random

class ServerHandler(SimpleHTTPRequestHandler):    
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'html')
        self.end_headers()
        rand = random.randint(1,20)
        my_string = ""
        if (self.path == '/roll'):
          my_string = "<html>You rolled a {}</html>".format(rand)
        else:
          my_string = "<html>Everybody <b>roll</b> initiative!</html>"
        self.wfile.write(bytes(my_string, 'UTF-8'))
          

def run(server_class=HTTPServer, handler_class=ServerHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    print("running server")
    httpd.serve_forever()

run()