import json
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from helpers import logger

app = Flask(__name__)
auth = HTTPBasicAuth()
CON = logger.CON


"""
Authentication
"""

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


"""
List preparations
"""

def send_to_index ():
   out = {
      'subreddits': [
         {
            'title': 'warshipporn',
            'generated': 'datecontext',
            'posts': 25
         }
      ],
      'wordlogs': [
         {
            'title': '-22706117',
            'messages': 272
         }
      ]
   }

   return out


"""
Routing
"""

@app.route('/')
@auth.login_required
def index (context=None):
   return render_template('index.html', context = send_to_index())


"""
Run the server
"""

app.run(port = 5268, debug = False, threaded = True)