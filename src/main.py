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


threads = [
   threading.Thread(target = core_worker),
   threading.Thread(target = test_worker),
]


if __name__ == '__main__':

   i = 0
   for thread in threads:
      thread[i].start()
      i += 1