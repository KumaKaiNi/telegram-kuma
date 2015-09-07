import json
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from helpers import logger

app = Flask(__name__)
auth = HTTPBasicAuth()
CON = logger.CON

try:
   file_ = open('./config.json', encoding='utf8')
   config = json.loads(file_.read())
   users = config['auth']['webui']
except:
   print(CON['err'], "config.json not found. Be sure to fill out default-config.json and rename it to config.json.")
file_.close()

@auth.get_password
def get_pw (username):
   if username in users:
      return users.get(username)
   return None


@app.route('/')
@auth.login_required
def index ():
   return render_template('index.html')


app.run(port = 5268, debug = False, threaded = True)