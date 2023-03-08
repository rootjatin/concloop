import signal
import time
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Function timed out")

def generate_range(a, b, timeout=None):
    if timeout is not None and timeout <= 0:
        raise ValueError("Timeout value must be positive")
    if timeout is not None:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
    try:
        for i in range(a, b):
            yield i
    finally:
        if timeout is not None:
            signal.alarm(0)



try:
    for i in generate_range(1, 10,1):
        while(True):
            print(i)
        time.sleep(1)
except TimeoutError:
    print("Timed out")
