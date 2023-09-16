from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<center><h1>Welcome to Bookify Club</h1></center>"
