#############################################################
### The bottom part of the code checks the name and if we
### are running code via python, it uses app.run() to start
### the server.
### 1. What alert message do you get? What does it mean?
#############################################################

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return f"Check!"

if __name__ == "__main__":
    app.run()