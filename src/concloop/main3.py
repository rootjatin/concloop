
import threading
import time
import curses

def before(timeout=None, stop_key=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            stop_event = threading.Event() # create stop event
            if timeout is not None:
                end_time = time.time() + timeout # calculate end time
                def check_time():
                    while not stop_event.is_set():
                        if time.time() > end_time:
                            stop_event.set()
                            raise TimeoutError("Loop execution time exceeded")
                        time.sleep(0.05)
                check_time_thread = threading.Thread(target=check_time) # create thread
                check_time_thread.start() # start thread

            if stop_key is not None:
                def check_key():
                    # initialize curses
                    stdscr = curses.initscr()
                    curses.noecho()
                    curses.cbreak()
                    stdscr.keypad(True)

                    # wait for stop_key
                    while not stop_event.is_set():
                        if stdscr.getch() == ord(stop_key):
                            stop_event.set()

                    # clean up curses
                    curses.nocbreak()
                    stdscr.keypad(False)
                    curses.echo()
                    curses.endwin()
                check_key_thread = threading.Thread(target=check_key) # create thread
                check_key_thread.start() # start thread

            try:
                for i in func(*args, **kwargs):
                    yield i
                    if stop_event.is_set():
                        break
            finally:
                stop_event.set() # stop threads
                if timeout is not None:
                    check_time_thread.join() # wait for check_time thread to finish
                if stop_key is not None:
                    check_key_thread.join() # wait for check_key thread to finish
        return wrapper
    return decorator



    
print(1)    

def generate_range(a, b, timeout=None):
    @before(timeout=timeout)
    def _generate_range(a, b):
        for i in range(a, b):
            yield i
    return _generate_range(a, b)
    
for i in before(timeout=5, stop_key='j')(generate_range)(1, 10):
    print(i)
    time.sleep(1)

print(1)