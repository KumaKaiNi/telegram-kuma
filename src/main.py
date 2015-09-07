import threading, time

# from webui import flask


def core_worker():
   from core import kuma

def webui_worker():
   print("Test worker thread started.")
   return


if __name__ == '__main__':

   threading.Thread(target = core_worker).start()
   threading.Thread(target = webui_worker).start()