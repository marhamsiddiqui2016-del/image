from flask import Flask
app = Flask(__name__) # <-- Must be lowercase 'app'

@app.route('/')
def home():
    return "Hello World"
