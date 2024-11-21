#############################################################
### Answer for 8
#############################################################

from flask import Flask,redirect

app = Flask(__name__)

data = {'counter': 0}

@app.route("/")
def main():
    return f'<a href="/up">up</a>{data["counter"]}<a href="/down">down</a>'

@app.route("/up")
def counter_up():
    data['counter'] = data['counter'] + 1
    return redirect("/", code=302)

@app.route("/down")
def counter_down():
    data['counter'] = data['counter'] - 1
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run()