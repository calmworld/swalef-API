from flask import Flask



DEBUG = True
PORT = 8000

app = Flask(__name__)

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    my_list = ["Hey", "check", "this", "out"]
    return my_list[0] # Works!

# run app
if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)