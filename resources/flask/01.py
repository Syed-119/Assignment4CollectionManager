#############################################################
### This code is a basic server using Flask, a similar                   
### module to the HTTP.server module we looked at before.
### If flask is not installed, we can use `pip install flask`
### to install it. Then `flask app <FILENAME> run` to run it.
### By default, it runs on port 5000 > http://127.0.0.1:5000/ 
### You can change this with `flask app <FN> run --port <PORT>`
### It uses decorators, which add functionality to a function.
#############################################################

from flask import Flask

app = Flask(__name__)

# This decorator takes the function below
# and runs it in response to the specific route.
@app.route("/")
def flask_time():
    return "<p>Flask time!</p>"