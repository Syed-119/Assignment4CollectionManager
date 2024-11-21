#############################################################
### The extra challenge is difficult because the browser treats
### / as part of the directory structure. With path variables
### we can allow ourselves to pass in strings with slashes.
### 1. Try to get this server to run an alert script
###     HINT: <script></script> will wrap a script
###     HINT: alert(<MESSAGE>) will provide a popup
### 2. Try to change this so it accepts only integers.
#############################################################

from flask import Flask

app = Flask(__name__)

@app.route("/admin/<path:subpath>")
def hello(subpath):
    return f"Accessing {subpath}!"