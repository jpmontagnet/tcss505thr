# TCSS 505 - threading homework - question 1
# Student: JP Montagnet / jpmont

import threading
import time
import argparse

"""
Goal:
Write a program that uses at least two threads to access the same data.
At least one thread should read the data, and at least one thread should
modify the data.

First run the program with no protection in place for the data and
capture the output (which should show 'messiness').

Next, add protection to the data (a lock or something to synchronize)
so that a thread that wants to read the data cannot access that data
while a thread that is modifying the data is active. 

Solution:
The data modifier simply increments a single integer value in a loop.
The data reader thread simply reads that value in a loop -- twice per loop,
with a negligible amount of work between those reads.
If the successive reads do no match, this counts as a "strike" and is
reported to stdout, along with the observed jump in value, and how many
rounds of reading were necessary to encounter a mismatch.
"""

class Opts:
    max_runsecs = 5
    max_strikes = 3
    use_locking = False

g_opts = Opts()

g_exit_flag = False
g_lock = threading.Lock()
g_val = 0

def do_noop():
    pass

def lock_acquire():
    global g_opts
    if not g_opts.use_locking:
        return
    global g_lock
    g_lock.acquire()

def lock_release():
    global g_opts
    if not g_opts.use_locking:
        return
    global g_lock
    g_lock.release()

def do_zero():
    global g_opts
    global g_exit_flag
    global g_lock
    global g_val
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
        if strikes >= g_opts.max_strikes:
            print("Strike out!")
            g_exit_flag = True
        elif time.perf_counter() - t_start > g_opts.max_runsecs:
            print(f"Timeout after {g_opts.max_runsecs} secs, {rounds} rounds")
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
    global g_opts
    for opt in "max_runsecs max_strikes use_locking".split():
        print(f"Option {opt}: {getattr(g_opts, opt)}")
    print("---")
    funcs = (do_zero, do_incr)
    threads = []
    for fn in funcs:
        threads.append(threading.Thread(target=fn))
    for thr in threads:
        thr.start()
    for thr in threads:
        thr.join()

def parse_opts():
    global g_opts
    parser = argparse.ArgumentParser(description="Fiddle with thread synchronization")
    parser.add_argument("--max-runsecs", type=int, default=Opts.max_runsecs)
    parser.add_argument("--max-strikes", type=int, default=Opts.max_strikes)
    parser.add_argument("--use-locking", action="store_true")
    args = parser.parse_args()
    g_opts.max_runsecs = args.max_runsecs
    g_opts.max_strikes = args.max_strikes
    g_opts.use_locking = args.use_locking

if __name__ == "__main__":
    parse_opts()
    do_runit()

# END
