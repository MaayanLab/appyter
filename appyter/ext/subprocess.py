import os
import signal
import multiprocessing as mp

def interrupt(proc: mp.Process):
  try:
    os.kill(proc.pid, signal.SIGINT)
  except ProcessLookupError:
    pass
  except KeyboardInterrupt:
    raise
  except:
    proc.terminate()
