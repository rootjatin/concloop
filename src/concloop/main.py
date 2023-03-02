import threading
import time

def before(timeout):
    def decorator(func):
        def wrapper(*args, **kwargs):
            end_time = time.time() + timeout # calculate end time
            stop_loop = threading.Event() # create stop event
            def check_time():
                while not stop_loop.is_set():
                    if time.time() > end_time:
                        stop_loop.set()
                        raise TimeoutError("Loop execution time exceeded")
                    time.sleep(0.05)
            check_time_thread = threading.Thread(target=check_time) # create thread
            check_time_thread.start() # start thread
            try:
                for i in func(*args, **kwargs):
                    yield i
                    if stop_loop.is_set():
                        break
            finally:
                stop_loop.set() # stop thread
                check_time_thread.join() # wait for thread to finish
        return wrapper
    return decorator

def generate_range(a, b, timeout=None):
    @before(timeout=timeout)
    def _generate_range(a, b):
        for i in range(a, b):
            yield i
    return _generate_range(a, b)

# for i in generate_range(1,3,4):
#     print(i)
