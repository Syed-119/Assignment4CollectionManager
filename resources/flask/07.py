#############################################################
### Putting the data dictionary into a function allows us to
### make it more private. 
### 1. Can we access get_data() directly from the client?
###      Why or why not?
#############################################################

from flask import Flask

app = Flask(__name__)

def get_data():
    data = {
    'England':'London',
    'Wales':'Cardiff',
    'Northern Ireland':'Belfast',
    'Scotland':'Edinburgh'
    }
    return data

@app.route("/")
def main():
    return f'add a country to the path to find its capital'


@app.route("/<key>")
def dict_access(key):
    data = get_data()
    if key in data.keys():
        return f'{data[key]}'
    return f'element not found'


if __name__ == "__main__":
    app.run()