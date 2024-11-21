#############################################################
### Can we access data from a dictionary? Sure!
### Let's try from a basic dictionary.
### 1. Do the nations of england work?
### 2. What about Northern Ireland? It has a space!
### 3. How could we fix this so the data dictionary was
###       less exposed!
#############################################################

from flask import Flask

app = Flask(__name__)

data = {
    'England':'London',
    'Wales':'Cardiff',
    'Northern Ireland':'Belfast',
    'Scotland':'Edinburgh'
}

@app.route("/")
def main():
    return f'add a country to the path to find its capital'

@app.route("/<key>")
def dict_access(key):
    if key in data.keys():
        return f'{data[key]}'
    return f'element not found'

if __name__ == "__main__":
    app.run()