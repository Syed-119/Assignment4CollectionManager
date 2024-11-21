#############################################################
### This is an example of sending a form, allowing a user
### to make a post request.
### 1. What is the difference between a GET and a POST?
#############################################################

from flask import Flask,redirect,request

app = Flask(__name__)

data = {'name':""}

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        data['name'] = request.form['name']
        return redirect('/',201)
    else:
      return f'''
        <h2>Current Name: {data['name']}<h2>
        <form method="post">
            <p><input type=text name=name>
            <p><input type=submit value=Update>
        </form>'''

if __name__ == "__main__":
    app.run()