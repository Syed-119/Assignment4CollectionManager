#############################################################
### This code below uses basic pathing. A secret is hidden.                   
### Use `flask app <FILENAME> run` to run it, then try to find
### the secret. It's not too challenging, to be honest.
#############################################################


from flask import Flask

app = Flask(__name__)

@app.route("/")
def basic():
    return f"No secrets here!"

@app.route("/secret")
def secret():
    return f"You found the secret!"