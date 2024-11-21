#############################################################
### Does this work? Why or why not?
### 1. How can we fix it?
###     HINT: Look at the previous exercise.
### 2. Can we fix the formatting of this?
#############################################################

from flask import Flask,redirect

app = Flask(__name__)
 
counter = 0

@app.route("/")
def main():
    return f'<a href="/up">up</a>{counter}<a href="/down">down</a>'


@app.route("/up")
def counter_up():
    counter = counter + 1
    return redirect("/", code=302)

@app.route("/down")
def counter_down():
    counter = counter - 1
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run()