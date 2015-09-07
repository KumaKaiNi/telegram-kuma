import threading, time

# from core import kuma
# from webui import flask


def core_worker():
   time.sleep(5)
   print("Core worker thread started.")
   return

def test_worker():
   print("Test worker thread started.")
   return


if __name__ == '__main__':

   threading.Thread(target = core_worker).start()
   threading.Thread(target = test_worker).start()