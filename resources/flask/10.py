#############################################################
### 1. How can we change this to allow it to go up and down
###      by different amounts?
### 2. How can we change this to allow a reset button?
### 3. How can we make two counters?
#############################################################

from flask import Flask,redirect

app = Flask(__name__)

class counter_maker:
    def __init__(self):
        self.value = 0
    def up(self):
        self.value = self.value + 1
    def down(self):
        self.value = self.value - 1  

data = {'counter': counter_maker()}

@app.route("/")
def main():
    return f'<a href="/up">up</a>{data["counter"].value}<a href="/down">down</a>'


@app.route("/up")
def counter_up():
    data['counter'].up()
    return redirect("/", code=302)

@app.route("/down")
def counter_down():
    data['counter'].down()
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()