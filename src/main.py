import threading, time
from webui import flask


def core_worker():
   from core import kuma


if __name__ == '__main__':

   threading.Thread(target = core_worker).start()
   flask.app.run(port = 5268, debug = True, threaded = True)