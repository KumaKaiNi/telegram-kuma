from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


try:
   file_ = open('./config.json', encoding='utf8')
   config = json.loads(file_.read())
   auth = config['auth']
except:
   print(CON['err'], "config.json not found. Be sure to fill out default-config.json and rename it to config.json.")

users = auth['webui']

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