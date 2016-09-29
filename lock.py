from multiprocessing import Lock
import time

lock = Lock()

def get_id(n):
   lock.acquire()
   for i in range(n, n+2):
      print("work %s" % i)
      time.sleep(1)
   lock.release()
   return 0
