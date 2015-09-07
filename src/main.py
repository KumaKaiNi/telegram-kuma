import threading, time
from flask import Flask
app = Flask(__name__)

"""
Worker definitions
"""

def core_worker():
   from core import kuma

def webui_worker():
   app.run(port = 5268, debug = True)


"""
Flask settings
"""

@app.route('/')
def hello ():
   return "Hello, kuma!"


if __name__ == '__main__':
   threading.Thread(target = core_worker).start()
   threading.Thread(target = webui_worker).start()