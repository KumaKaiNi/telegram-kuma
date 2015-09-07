import json, os
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from helpers import folders, logger

app = Flask(__name__)
auth = HTTPBasicAuth()
CACHE = folders.CACHE
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
   out = {}

   out['subreddits'] = []
   sub_dir = os.listdir(CACHE['subreddits'])
   for item in sub_dir:
      file_ = open(CACHE['subreddits'] + item)
      data = json.loads(file_.read())
      file_.close()

      title = item.split('.')[0]
      date = data['time']
      posts = str(len(data['posts']))

      out['subreddits'].append({'title': title, 'date': date, 'posts': posts})

   out['wordlogs'] = []
   sub_dir = os.listdir(CACHE['wordlogs'])
   for item in sub_dir:
      file_ = open(CACHE['wordlogs'] + item)
      messages = file_.read().splitlines()
      title = item.split('.')[0]
      messages = str(len(messages))
      file_.close()

      out['wordlogs'].append({'title': title, 'messages': messages})

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