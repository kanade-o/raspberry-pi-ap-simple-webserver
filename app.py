from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello, World!</h1>"

def start():
    app.run(host="0.0.0.0", port=8080)

