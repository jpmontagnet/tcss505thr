# TCSS 505 - threading homework - question 1
# Student: JP Montagnet / jpmont

import threading
import time
import argparse

"""
Write a program that uses at least two threads to access the same data.
At least one thread should read the data, and at least one thread should
modify the data.

First run the program with no protection in place for the data and
capture the output (which should show 'messiness').

Next, add protection to the data (a lock or something to synchronize)
so that a thread that wants to read the data cannot access that data
while a thread that is modifying the data is active. 
"""

g_exit_flag = False
g_max_secs = 5
g_max_strikes = 3
g_use_locking = False
g_lock = threading.Lock()
g_val = 0

def do_noop():
    pass

def lock_acquire():
    global g_use_locking
    if not g_use_locking:
        return
    global g_lock
    g_lock.acquire()

def lock_release():
    global g_use_locking
    if not g_use_locking:
        return
    global g_lock
    g_lock.release()

def do_zero():
    global g_val
    global g_max_strikes
    global g_max_secs
    global g_exit_flag
    global g_lock
    t_start = time.perf_counter()
    rounds = 0
    strikes = 0
    while not g_exit_flag:
        rounds += 1
        lock_acquire()
        try:
            v1 = g_val
            do_noop()
            v2 = g_val
        finally:
            lock_release()
        if v2 - v1 != 0:
            strikes += 1
            print(f"Value mismatch (+{v2 - v1}) after {rounds} rounds")
            rounds = 0
        if strikes >= g_max_strikes:
            print("Strike out!")
            g_exit_flag = True
        elif time.perf_counter() - t_start > g_max_secs:
            print(f"Timeout after {g_max_secs} secs, {rounds} rounds")
            g_exit_flag = True

def do_incr():
    global g_val
    global g_exit_flag
    global g_lock
    while not g_exit_flag:
        lock_acquire()
        try:
            g_val += 1
        finally:
            lock_release()

def do_runit():
    global g_lock
    funcs = (do_zero, do_incr)
    threads = []
    for fn in funcs:
        threads.append(threading.Thread(target=fn))
    for thr in threads:
        thr.start()
    for thr in threads:
        thr.join()

def parse_opts():
    global g_use_locking
    parser = argparse.ArgumentParser(description="Fiddle with thread synchronization")
    parser.add_argument("--max-secs", type=int, default=g_max_secs)
    parser.add_argument("--max-strikes", type=int, default=g_max_strikes)
    parser.add_argument("--use-lock", action="store_true")
    args = parser.parse_args()
    g_use_locking = args.use_lock

if __name__ == "__main__":
    parse_opts()
    do_runit()

# END
