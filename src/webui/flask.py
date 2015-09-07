from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


users = {'rekyuu': 'password'}

@auth.get_password
def get_pw (username):
   if username in users:
      return users.get(username)
   return None


@app.route('/')
@auth.login_required
def index ():
   return "Hello, %s!" % auth.username()


app.run(port = 5268, debug = False, threaded = True)