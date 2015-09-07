from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello ():
   return "Hello, kuma!"


app.run(port = 5268, debug = True, threaded = True)