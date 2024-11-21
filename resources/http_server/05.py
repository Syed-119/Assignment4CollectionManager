from http.server import HTTPServer,SimpleHTTPRequestHandler
import random



class ServerHandler(SimpleHTTPRequestHandler):    
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'html')
        self.end_headers()
        rand = random.randint(1,20)
        my_string = "<html>You rolled a {}</html>".format(rand)
        self.wfile.write(bytes(my_string, 'UTF-8'))

def run(server_class=HTTPServer, handler_class=ServerHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    print("running server")
    httpd.serve_forever()

run()