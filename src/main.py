import threading, time
from webui import flask


def core_worker():
   from core import kuma

def webui_worker():
   flask.app.run(port = 5268, debug = True, threaded = True)


if __name__ == '__main__':

   threading.Thread(target = webui_worker).start()
   threading.Thread(target = core_worker).start()