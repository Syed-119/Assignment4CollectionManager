#############################################################
### This code below uses variables. It will repeat what you add                   
### after the path. Try going to <SERVER_IP>/<YOURNAME>
### There are two challenges.
### 1. Try to make the text bold, italic, or marquee.
###     EXTRA: Try to make the browser run a script
### 2. Adjust the code to prevent a user from doing this.
###     HINT: https://pypi.org/project/MarkupSafe/
### 3. Notice there are two variables called name
### __name__ and name. Use print statements to find
### the difference!
#############################################################

from flask import Flask

app = Flask(__name__)

@app.route("/<name>")
def hello(name):
    return f"Hello, {name}!"



