import threading, time



def core_worker():
   from core import kuma

def webui_worker():
   from webui import flask


if __name__ == '__main__':

   threading.Thread(target = webui_worker).start()
   threading.Thread(target = core_worker).start()